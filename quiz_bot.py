import os
import random
import discord

from dotenv import load_dotenv
from src.quiz_helper import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'Connected to {guild.name}, ID : {guild.id}')

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    
    if channel == "random":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')


@client.event
async def on_reaction_add(reaction, user):
    username = str(user).split("#")[0]
    print(f"User {username} reacted to a message")
    if reaction.message.author == client.user:
        db = db_path(reaction.message.guild.id)
        check_player(db, user)





client.run(TOKEN)
