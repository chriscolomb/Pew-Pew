# pew pew bot.
# Matchmaking bot for TTD.
# Author: Brandon Chapman (chapman.brandon2@gmail.com).
import os
import discord
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
# bot token.
TOKEN = os.getenv('BOT_TOKEN')
# discord server, insert method here to get servers; this is for future reference.
guildName = os.getenv('SERVER_TOKEN')
profiles = os.getenv('PROFILES')
client = discord.Client()

# Accessing google spreadsheet
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive",
         "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('SpreadClientSecret.json', scope)
spreadClient = gspread.authorize(credentials)
sheetProfiles = spreadClient.open('Profiles').sheet1


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == guildName:
            break

    print(f'{client.user} has connected to Discord!')
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    resp = 'hello world'

    if message.content == 'hello':
        await message.channel.send(resp)


client.run(TOKEN)
