import nextcord
import sys
from nextcord.ext import commands
#from nextcord.utils import get

#parent directory import
sys.path.append('DatabaseRelated')
import mongodb
from player import Player
from buttons import AttackButtons
from buttons import WinorLose
# this would be used for only admin in TTD server, need to implement this
# need to implement our own help command, need to disable this
# need a comand to edit entries
# need a ban from ranked battles command and entry
# need a way to settle disputes, maybe have the bot submit it to another database?
# p1,p2,gained_rank,lost_rank,p1Win = False could be stored in the dispute database to be viewed for later.
class Admin_Commands(commands.Cog):
    """Admin Commands"""

    def __init__(self,client: commands.Bot):
        self.client = client
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("bot ready")
        self.client.add_view(AttackButtons())
        self.client.add_view(WinorLose())
        #print('Logged on as {0}!'.format(self.user.name))

    @commands.command()
    async def createPlayer(self,ctx, user: nextcord.Member):
        """adds player to database"""
        #print('ctx from {0.author}: {0.content}'.format(ctx))
        if ctx.author.guild_permissions.administrator:
            for id in mongodb.player_collection.find({},
                                                        {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                if id["_id"] == user.id:
                    await ctx.channel.send("<@{0}> is already in the database.".format(user))
                    return

            p1 = Player(user.id)
            p1_entry = {
                "_id": p1.id,
                "rating": p1.rating,
                "win_count": p1.win_count,
                "lose_count": p1.lose_count,
                "win_streak": p1.win_streak,
                "best_win_streak": p1.best_win_streak
            }
            mongodb.player_collection.insert_one(p1_entry)
            await ctx.channel.send("<@{0}> entry for database created.".format(user))
        else:
            await ctx.channel.send("no admin permissions")

    @commands.command()
    async def deletePlayer(self,ctx, user: nextcord.Member):
        """deletes user from database"""
        if ctx.author.guild_permissions.administrator:        
        
            for id in mongodb.player_collection.find({},
                                                    {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                if id["_id"] == user.id:
                    delete_id = {"_id": user.id}
                    mongodb.player_collection.delete_one(delete_id)
                    await ctx.channel.send("Entry for <@{0}> has been deleted.".format(user))
                    return

            await ctx.channel.send("<@{0}> is not in the database.".format(user))
        else:
            await ctx.channel.send("You don't have admin privilages to do this command")
    
    

def setup(client):
    client.add_cog(Admin_Commands(client))