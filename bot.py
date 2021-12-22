import nextcord
from nextcord.ext import commands
import os
#pip3 freeze > requirements.txt helpful command for updating versions

intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "=", intents = intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
    
client.run('NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.AfDsH6U1x5GNlE_1tjGwmjjuNVU')