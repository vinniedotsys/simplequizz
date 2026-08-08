import discord
import io

from src.database import *

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


def get_answer(question, question_message):
    for answer in question_message.reactions:
        print(answer)



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
        def check(reaction, user):            
                return user.id == gamemaster.discord_id and str(reaction.emoji) == '☑️'
        question = Question(db_path, id)
        question.get()
        await ctx.send(f"Question {nbr} :")
        question_message = await ctx.send(file=discord.File(io.BytesIO(question.question_image), f"question_{nbr}.jpg"))
        for emoji in emojis:
            await question_message.add_reaction(emoji)
        await bot.wait_for('reaction_add', check=check)
        nbr +=1
