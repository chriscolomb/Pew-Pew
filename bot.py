import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = 'NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.nUj2RmF7ZjdO-wCL9oEvGJiNf4Q'
GUILD = '575869943346757682'

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)