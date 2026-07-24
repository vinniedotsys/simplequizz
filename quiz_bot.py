import os
import random
import discord

from dotenv import load_dotenv
from src.quiz_helper import *
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='q!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'Connected to {guild.name}, ID : {guild.id}')

@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    
    if channel == "random":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    username = str(user).split("#")[0]
    print(f"User {username} reacted to a message")
    if reaction.message.author == bot.user:
        db = db_path(reaction.message.guild.id)
        check_player(db, user)

@bot.command(name='quiz', help='Launch an available quiz where the user is the gamemaster')
async def quiz(ctx):
    username = str(ctx.author).split("#")[0]
    print(f"User {username} launched command quiz")

    db = db_path(ctx.guild.id)
    gamemaster = check_player(db, ctx.author)
    await game_available(ctx, db, gamemaster.id)



bot.run(TOKEN)
