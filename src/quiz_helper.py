import discord
import sqlite3

from src.database import *

def db_path(guild_id):
    
    return "data/" + str(guild_id) + ".db"


def check_player(db_path, discord_member):
    new_player = Player(db_path)
    query = "SELECT id FROM players WHERE discord_id = ?"
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    res = cur.execute(query, (discord_member.id,))
    player = res.fetchone()
    con.close()
    if player is None:
        new_player.name = discord_member.name
        new_player.discord_id = discord_member.id
        new_player.insert()
