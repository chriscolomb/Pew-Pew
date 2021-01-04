# pew pew bot.
# Matchmaking bot for TTD.
# Author: Brandon Chapman (chapman.brandon2@gmail.com).
import os
import discord
from dotenv import load_dotenv
import mysql.connector
import PewPewBot


def main():
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

    # connect to database
    conn = None
    conn = mysql.connector.connect(
        host='34.84.228.251',
        user='root',
        password='iI5knykhgxA0JfKw',
        database='PewPew'
    )

    if conn.is_connected():
        print('Connected to MySQL database')
    cursor = conn.cursor(buffered=True)

    PewPewBot.pew_bot_start(conn, cursor, client)
    client.run(TOKEN)
    cursor.close()
    conn.close()
    client.close()
    if conn.is_connected():
        print('Connected to MySQL database')
    else:
        print("isn't connected")

main()
