import os

import discord
import mysql.connector
from dotenv import load_dotenv
import mysql.connector

load_dotenv()
# Pew Pew bot token
TOKEN = os.getenv('BOT_TOKEN')
# Server token
GUILD = os.getenv('SERVER_TOKEN')

client = discord.Client()

mydb = mysql.connector.connect(
    host='34.84.228.251',
    user='root',
    password='iI5knykhgxA0JfKw',
    database='PewPew'
)

mycursor = mydb.cursor()

sql = "INSERT INTO PewPew,PewPew (User, Value, Wins, Loses) VALUES (%s, %d, %d, %d)"
val = ("TeamDuck#0876", 0.5, 2, 3)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

# def connect():
#     # Connect to MySQL database
#     conn = None
#     try:
#         conn = mysql.connector.connect(
#             host='34.84.228.251',
#             user='root',
#             password='iI5knykhgxA0JfKw',
#             database='PewPew')
#         if conn.is_connected():
#             print('Connected to MySQL database')
#
#     except Error as e:
#         print(e)
#
#     finally:
#         if conn is not None and conn.is_connected():
#             conn.close()
#
#
# def insert_user(user):
#     query = "INSERT INTO PewPew(user) " \
#             "VALUES(%s)"
#     args = user
#
#     try:
#         db_config = read_db_config()
#         conn = MySQLConnection(**db_config)
#
#         cursor = conn.cursor()
#         cursor.execute(query, args)
#
#         if cursor.lastrowid:
#             print('last insert id', cursor.lastrowid)
#         else:
#             print('last insert id not found')
#
#         conn.commit()
#     except Error as error:
#         print(error)
#
#     finally:
#         cursor.close()
#         conn.close()


# Test connection with bot/guild and MySQL connection
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    # connect()
    #
    # insert_user('TeamDuck')


client.run(TOKEN)
