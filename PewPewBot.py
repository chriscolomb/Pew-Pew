import asyncio

import discord
import PewPewDatabaseAccess


def pew_bot_start(connection, cursor_name, client):

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('!add'):
            await message.channel.send('added wins to user')
            PewPewDatabaseAccess.update_values_columns('DamagedTwitch', connection, cursor_name, 'w')
    @client.event
    async def on_message(message):
        dragon = client.get_emoji(794999307048321044)
        if message.content.startswith('!match'):
            channel = message.channel
            await channel.send('Send me that 👍 reaction, mate')


            def check(reaction, user):
                # without custom, can do str(reaction.emoji)=='👎'
                return user == message.author and reaction.emoji == dragon


            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('👎')
            else:
                await channel.send(dragon)