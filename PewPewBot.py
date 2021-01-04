import asyncio
import mysql.connector
import PewPewDatabaseAccess
import os
import discord
from dotenv import load_dotenv


def pew_bot_start(client):
    # image for confirming fight matchmaking
    fight_image = 'PewPewBot_StartFight.jpg'

    # connect to database
    conn = None
    conn = mysql.connector.connect(
        host='130.211.119.74',
        user='root',
        password='togcow-nuvgyQ-7fydme',
        database='PewPew'
    )
    if conn.is_connected():
        print('Connected to MySQL database')
    cursor = conn.cursor(buffered=True)

    @client.event
    async def on_message(message):

        # The bot waits for the user to type !match and then executes a command
        dragon = client.get_emoji(794999307048321044)
        if message.content.startswith('!match'):
            channel = message.channel
            # enter user, get user id @ here and place it in match.
            await channel.send('ready for a match? user, reply with kirby knife to confirm',
                               file=discord.File(fight_image))

            def check(reaction, user):
                # without custom, can do, "str(reaction.emoji)=='👎'"
                return user == message.author and reaction.emoji == dragon

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('Sorry, user did not respond in time. Request cancelled')
            else:
                # This is where a response can happen, if the user reacts.
                await channel.send(dragon)

        # testing adding wins to user in SQL database, this will not be needed later.
        # Will be a different async module, this is only for testing.
        if message.content.startswith('!add'):
            channel = message.channel
            await message.channel.send('added wins to user')
            PewPewDatabaseAccess.update_values_columns('TeamDuck', 'w')

    # closes connection
    cursor.close()
    conn.close()
