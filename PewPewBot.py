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
