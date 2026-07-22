import discord
import sqlite3

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
