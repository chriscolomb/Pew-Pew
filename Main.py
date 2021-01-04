# pew pew bot.
# Matchmaking bot for TTD.
# Author: Brandon Chapman (chapman.brandon2@gmail.com).
import os
import discord
from dotenv import load_dotenv
import mysql.connector
import PewPewBot
import PewPewDatabaseAccess

# connect to discord bot
load_dotenv()
# bot token.
TOKEN = os.getenv('BOT_TOKEN')
# discord server, insert method here to get servers; this is for future reference.
client = discord.Client()
GUILD = os.getenv('SERVER_TOKEN')

# checks status of discord
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} has connected to Discord!')
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

PewPewBot.pew_bot_start(client)
client.run(TOKEN)

