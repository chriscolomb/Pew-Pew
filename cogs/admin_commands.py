import discord
import sys
from discord.ext import commands
from discord.utils import get

#parent directory import
sys.path.append('DatabaseRelated')
import mongodb
from player import Player
### this would be used for only admin in TTD server
class Admin_Commands(commands.Cog):

    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("bot ready")
         #print('Logged on as {0}!'.format(discord.client.user.name))

    @commands.command()
    async def createPlayer(self,ctx, user: discord.Member):
        #print('ctx from {0.author}: {0.content}'.format(ctx))
        if ctx.author.guild_permissions.administrator:
            for id in mongodb.player_collection.find({},
                                                        {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                if id["_id"] == user.id:
                    await ctx.channel.send("<@{0.user.id}> is already in the database.".format(ctx))
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
            await ctx.channel.send("<@{0.user.id}> entry for database created.".format(ctx))
        else:
            await ctx.channel.send("no admin permissions")
    @commands.command()
    async def deletePlayer(self,ctx, user: discord.Member):
        if ctx.author.guild_permissions.administrator:        
        
            for id in mongodb.player_collection.find({},
                                                    {"_id": 1, "rating": 0, "win_count": 0, "lose_count": 0, "win_streak": 0, "best_win_streak": 0}):
                if id["_id"] == user.id:
                    delete_id = {"_id": ctx.author.id}
                    mongodb.player_collection.delete_one(delete_id)
                    await ctx.channel.send("Entry for <@{0.user.id}> has been deleted.".format(ctx))
                    return

            await ctx.channel.send("<@{0.user.id}> is not in the database.".format(ctx))
        else:
            await ctx.channel.send("You don't have admin privilages to do this command")

def setup(client):
    client.add_cog(Admin_Commands(client))