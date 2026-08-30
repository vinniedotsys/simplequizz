import discord
import io


from src.database import *

### Return DB path
### guild_id = discord.Guild.id
### return str
def db_path(guild_id):
    return "data/" + str(guild_id) + ".db"


def check_player(db_path, discord_member):
    player = Player(db_path)
    if discord_member.nick is not None:
        player.name = discord_member.nick
    else:
        player.name = discord_member.name
    player.discord_id = discord_member.id
    player.is_player()
    return player

### For a reaction, create player answer if none already exist
### player = Player Object
### answer = str
### question_id = str
def get_answer(player, answer, question_id):
    question = Question(player.db_path)
    question.get(question_id)
    choice = Choice(player.db_path)
    choice.emoji = str(answer)
    choice.game = question.game
    choice.get_from_emoji()
    player_answer = PlayerAnswer(db_path=player.db_path)
    player_answer.question = question_id
    player_answer.player = player.id
    if player_answer.has_answered():
        return
    player_answer.answer = choice.id

    if question.answer == choice.id:
        player_answer.result = 1
    else:
        player_answer.result = 0

    player_answer.insert()

### Return an embed with the results for a question
### question_nbr = int
### question = Question Object
### return discord.Embed
def question_results(question_nbr, question):
    results = question.get_results()
    embed = discord.Embed(title=f"Question {question_nbr} results :", color=0x81a1c1)
    for result in results:
        player = Player(question.db_path)
        player.get(result[0])
        embed.add_field(name="\u200b", value=f"**{player.name}**: {('❌','✅')[result[1]]}", inline=False)
    return embed

### Return and embed with the game rankings
### game = Game object
### return discord.Embed
def game_rankings(game):
    rank_emojis = {
    1: "🥇",
    2: "🥈",
    3: "🥉",
    }
    rankings = game.rankings()
    embed = discord.Embed(title="Score :", color=0x81a1c1)
    for rank in rankings:
        emoji = rank_emojis.get(rank[0], "")
        prefix = f"{emoji} " if emoji else f"{rank[0]} "
        embed.add_field(name="\u200b", value=f"{prefix} **{rank[2]}** : {rank[3]}/{rank[4]} *({rank[5]}%)*")
    return embed

### Check for unplayed game(s) where the user launching the comand is the game master
### ctx = discord.Context
### db_path = str
### gamemaster = str
### return int, str
async def game_available(ctx, db_path, gamemaster):
    game = Game(db_path)
    game.gamemaster = str(gamemaster)
    games_available = game.available()
    nbr_games = len(games_available)

    match nbr_games:
        case 0:
            await ctx.send("No games where you are the gamemaster are available to play ! Load a game first")
        case 1:
            await ctx.send("Game available !")
        case _:
            nb = 1
            await ctx.send(f"You have {nbr_games} games available :")
            for game in games_available:
                await ctx.send(f"Game {nb} : {game[1]} questions")
    return nbr_games, games_available

### Main game logic
### ctx = discord.Context
### db_path = str
### game = str
### bot = discord.Bot
async def quiz_logic(ctx, db_path, game, bot):
    current_quiz = Game(db_path)
    current_quiz.get(game)
    questions = current_quiz.questions()
    emojis = current_quiz.emojis()
    emojis.append("☑️")
    gamemaster = Player(db_path, current_quiz.gamemaster)
    gamemaster.get()
    nbr = 1


    for id in questions:
        def check_res(reaction, user):            
                return user.id == gamemaster.discord_id and str(reaction.emoji) == '☑️'
        
        def check_next(reaction, user):
            return user.id == gamemaster.discord_id and str(reaction.emoji) == '⏭️'

        question = Question(db_path, id)
        question.get()
        await ctx.send(f"Question {nbr} :")
        question_message = await ctx.send(file=discord.File(io.BytesIO(question.question_image), f"question_{nbr}.jpg"))
        for emoji in emojis:
            await question_message.add_reaction(emoji)
        await bot.wait_for('reaction_add', check=check_res)
        complete_question_message = await question_message.channel.fetch_message(question_message.id)
        for answer in complete_question_message.reactions:
            if str(answer) not in emojis or answer == '☑️' :
                continue
            async for user in answer.users(limit=None):
                player = Player(db_path)
                player.discord_id = user.id
                player.is_player()
                if player.id == gamemaster.id or user == bot.user:
                    continue
                else:
                    get_answer(player, answer, id)
        result_embed = question_results(nbr, question)
        ranking_embed = game_rankings(current_quiz)

        await ctx.send(f"Answer : {question.get_answer_emoji()}")
        answer_message = await ctx.send(file=discord.File(io.BytesIO(question.answer_image), f"answer_{nbr}.jpg"))
        await answer_message.add_reaction("⏭️")
        await ctx.send(embed=result_embed)
        await ctx.send(embed=ranking_embed)

        await bot.wait_for('reaction_add', check=check_next)
        nbr +=1
