import nextcord
from nextcord.ext import commands
import sys
import random


#parent directory import
sys.path.append('DatabaseRelated')
sys.path.append('cogs')
import mongodb
from player import Player
from buttons import AttackButtons
from buttons import WinorLose 
import editdatabase
import operator

class Stat_Commands(commands.Cog):
    """stat commands"""

    def __init__(self,client: commands.Bot):
        self.client = client
    
    
def setup(client):
    client.add_cog(Stat_Commands(client))
