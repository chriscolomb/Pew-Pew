# This class will handle events regarding matches, reacts, messages
# useful methods and such for right now.
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
