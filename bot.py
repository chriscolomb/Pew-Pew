from typing import Optional, Set
import nextcord
from nextcord import embeds
from nextcord import message
from nextcord.ext import commands
import os
import sys

from nextcord.ext.commands.core import group

# sys.path.append("C:\Users\Chapm\GitHub\Pew_Pew\cogs")
#from cogs import help_commands
class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def _help_embed(self, title: str, description: Optional[str] = None, 
    mapping:Optional[dict] = None, command_set: Optional[Set[commands.Command]] = None):
        avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
        embed= embeds.Embed(title= title)
        if description:
            embed.description = description
        if command_set:
            #show help for all commands in column
            filtered = await self.filter_commands(command_set, sort = True)
            for command in filtered:
                embed.add_field(name = self.get_command_signature(command),value = command.short_doc or "...", inline = False)
        elif mapping:
            #add short description of cogs
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort =True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "no category"
                cmd_list = "\u2002".join(
                    f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered
                )
                value = (
                    f"{cog.description}\n{cmd_list}"
                    if cog and cog.description
                    else cmd_list
                )
                embed.set_author(name=self.context.bot.user.name, icon_url=avatar.url)
                embed.add_field(name=name, value=value)





        return embed 
    
    async def send_bot_help(self, mapping:dict):
        embed =await self._help_embed(
            title = "Bot Commands",
            description=self.context.bot.description,
            mapping = mapping
        )      
       
        await self.get_destination().send(embed= embed)
        

    async def send_command_help(self, command: commands.Command):
        embed = await self._help_embed(
            title= command.qualified_name,
            description= command.help,
            command_set = commands.commands if isinstance(command,commands.Group) else None
        )
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog:commands.Cog):
        embed = await self._help_embed(
            title= cog.qualified_name,
            description= cog.description,
            command_set=cog.get_commands()
        )
        await self.get_destination().send(embed=embed)

            

    send_group_help = send_command_help

    

class Help_Commands(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "=", intents = intents, description="MatchMaking bot for discord")
client.help_command = MyHelpCommand()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
    
client.run('NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.AfDsH6U1x5GNlE_1tjGwmjjuNVU')