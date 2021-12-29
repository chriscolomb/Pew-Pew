import nextcord
from nextcord.ext import commands
import os

from cogs import help_commands

from nextcord.ext.commands.core import group

# sys.path.append("C:\Users\Chapm\GitHub\Pew_Pew\cogs")
#from cogs import help_commands


intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "=", intents = intents, description="**Ranked Matchmaking Bot for SSBU with ELO Rating!**\n> To see a description for each command based on category: \n> `=help command_category`\n> For help with specific commands: \n> `=help command_name`")
#test
#server
#switch
#client = commands.Bot(command_prefix = "??", intents = intents, description="**Ranked Matchmaking Bot for SSBU with ELO Rating!**\n> To see a description for each command based on category: \n> `=help command_category`\n> For help with specific commands: \n> `=help command_name`")
client.help_command = help_commands.MyHelpCommand()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
client.run('NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.AfDsH6U1x5GNlE_1tjGwmjjuNVU')    
#test
#server
#switch
#client.run('OTIzNzk0ODAyNTM1OTY4Nzg5.YcVM9A.M6kP6qwzaKDO3PvlXXh07kzX6kk')
