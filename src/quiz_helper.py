import discord

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

async def game_available(ctx, db_path, gamemaster):
    game = Game(db_path)
    game.gamemaster = gamemaster
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
            await ctx.send(f"Please launch the quiz command with a game ID")
    return nbr_games, games_available
