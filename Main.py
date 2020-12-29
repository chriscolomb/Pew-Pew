# pew pew bot.
# Matchmaking bot for TTD.
# Author: Brandon Chapman (chapman.brandon2@gmail.com).
import os
import discord
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
import pymysql


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
    cursor = conn.cursor()

    # add entries
    user = 'TeamDuck'
    wins = 4
    losses = 125
    value = round(wins / (wins + losses), 4)

    conn_query = (
        "INSERT INTO `Profile` (`User`, `Value`, `Wins`, `Losses`)"
        "VALUES (%(User)s, %(Value)s, %(Wins)s, %(Losses)s)")
    profile_data = {
        'User': user,
        'Value': value,
        'Wins': wins,
        'Losses': losses,
    }

    # re-format this to cover other.
    try:
        cursor.execute(conn_query, profile_data)
    except mysql.connector.errors.IntegrityError:
        # other errors can happen but not to figure out this try except statement.
        print('The user already exist')

    conn.commit()

    # modify entries
    edit_wins = ()

    cursor.close()
    conn.close()


main()


def add_table(cursor):
    DB_NAME = 'PewPew'
    TABLES = {}

    TABLES['Profile'] = (
        "CREATE TABLE `Profile` ("
        "  `User` varchar(37) NOT NULL,"
        "  `Value` float(20) NOT NULL,"
        "  `Wins` int(11) NOT NULL,"
        "  `Losses` int(11) NOT NULL,"
        "  PRIMARY KEY (`User`)"
        ") ENGINE=InnoDB")

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
