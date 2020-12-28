# This class will handle events regarding matches, reacts, messages
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


# add user
total = 0
add_player_label = ("INSERT INTO PewPew"
                    "(User, Win, Losses, Value) "
                    "VALUES (%s, %s, %s, %s)")

add_player = ('DamagedTwitch',float (10.0), float(3.0), total)

db_cursor.execute(add_player)

conSQL.commit()