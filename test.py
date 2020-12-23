# pew pew bot.
# Matchmaking bot for TTD.
# Author: Brandon Chapman (chapman.brandon2@gmail.com).
import os

import discord
from dotenv import load_dotenv

load_dotenv()
# bot token.
TOKEN = os.getenv('BOT_TOKEN')
# discord server, insert method here to get servers; this is for future reference.
guildName = os.getenv('SERVER_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == guild:
            break

    print(f'{client.user} has connected to Discord!')
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)
