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
    client.run(TOKEN)
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
    wol = 'w'
    user = "DamagedTwitch"

    PewPewDatabaseAccess.update_values_columns(user, conn, cursor, wol)

    cursor.close()
    conn.close()
    client.close()

main()

def database_entries():
    # insert method for table entry method

    # modify entries
    user = 'DamagedTwitch'
    wins = 10
    losses = 5
    value = round(wins / (wins + losses), 4)

    profile_data = {
        'User': user,
        'Value': value,
        'Wins': wins,
        'Losses': losses,
    }
    update_user_wins = ("UPDATE Profile set Wins = %s "
                        "where user = %s")
    update_user_value = ("UPDATE Profile set Value = %s "
                         "where user = %s")

    cursor.execute(update_user_wins, (wins, user))
    cursor.execute(update_user_value, (value, user))
    conn.commit()



