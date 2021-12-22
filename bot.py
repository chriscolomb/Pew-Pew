from typing import Optional, Set
import nextcord
from nextcord import embeds
from nextcord import message
from nextcord.ext import commands
import os
import sys

from nextcord.ext.commands.core import group

from cogs.help_commands import MyHelpCommand

# sys.path.append("C:\Users\Chapm\GitHub\Pew_Pew\cogs")
#from cogs import help_commands

intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "=", intents = intents, description="MatchMaking bot for discord")
client.help_command = MyHelpCommand()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
    
client.run('NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.AfDsH6U1x5GNlE_1tjGwmjjuNVU')