import os
import discord
import logging

from dotenv import load_dotenv
from src.quiz_helper import *
from discord.ext import commands
from typing import Optional

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='q!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        logging.info(f'Connected to {guild.name}, ID : {guild.id}')

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
    logging.info(f"User {username} reacted to a message")
    if reaction.message.author == bot.user:
        db = db_path(reaction.message.guild.id)
        check_player(db, user)

@bot.command(name='quiz', help='Launch an available quiz where the user is the gamemaster')
async def quiz(ctx: commands.Context, arg: Optional[int]):
    username = str(ctx.author).split("#")[0]
    logging.info(f"User {username} launched command quiz")

    db = db_path(ctx.guild.id)
    gamemaster = check_player(db, ctx.author)
    nbr_games, games_available = await game_available(ctx, db, gamemaster.id)
    if arg is None:
        match nbr_games:
            case 0:
                pass
            case 1:
                await quiz_logic(ctx, db, games_available[0][0], bot)
            case _:
                await ctx.send(f"Please launch the quiz command with a game ID")
    else:
        match nbr_games:
            case 0:
                pass
            case 1:
                await quiz_logic(ctx, db, games_available[0][0], bot)
            case _:
                await quiz_logic(ctx, db, games_available[arg][0], bot)


bot.run(TOKEN)
