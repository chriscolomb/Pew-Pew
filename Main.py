# pew pew bot.
# Matchmaking bot for TTD.
# Author: Brandon Chapman (chapman.brandon2@gmail.com).
import os
import discord
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

import PewPewDatabaseAccess


def main():
    # connect to discord bot
    load_dotenv()
    # bot token.
    TOKEN = os.getenv('BOT_TOKEN')
    # discord server, insert method here to get servers; this is for future reference.
    guildName = os.getenv('SERVER_TOKEN')
    profiles = os.getenv('PROFILES')
    client = discord.Client()
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
    # changed buffer = True 12.29.2020
    cursor = conn.cursor(buffered=True)
    wol = 'l'
    user = "DamagedTwitch"

    PewPewDatabaseAccess.update_values_columns(user, conn, cursor, wol)

    client.run(TOKEN)
    cursor.close()
    conn.close()
    client.close()


main()
