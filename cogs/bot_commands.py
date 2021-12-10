import nextcord
from nextcord.ext import commands
import sys

#parent directory import
sys.path.append('DatabaseRelated')
import mongodb
from player import Player
from buttons import AttackButtons
from battle import Battle

class Bot_Commands(commands.Cog):

    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def stats(self,ctx, user: nextcord.Member):
        """This will reveal all stats for player"""
        for id in mongodb.player_collection.find():
            if id["_id"] == user.id:
                title = "Stats for {0}".format(user)

                embed = nextcord.Embed(
                    title = title,
                    colour = nextcord.Colour.green()
                )

                embed.add_field(name="Rating", value=id.get("rating"))
                embed.add_field(name="Win Count", value=id.get("win_count"))
                embed.add_field(name="Lose Count", value=id.get("lose_count"))
                embed.add_field(name="Win Streak", value=id.get("win_streak"))
                embed.add_field(name="Best Win Streak", value=id.get("best_win_streak"))
                
                await ctx.channel.send(embed = embed)
                return

        await ctx.channel.send("<@{0.user}> is not in the database.".format(ctx))
    
    #was going to make self stats but this didn't work, weird overload.

    # @commands.command()
    # @dispatch()
    # async def stats(self,ctx):
    #     for id in mongodb.player_collection.find():
    #         if id["_id"] == ctx.author.id:
    #             title = "Stats for {0.author}".format(ctx)

    #             embed = nextcord.Embed(
    #                 title = title,
    #                 colour = nextcord.Colour.green()
    #             )

    #             embed.add_field(name="Rating", value=id.get("rating"))
    #             embed.add_field(name="Win Count", value=id.get("win_count"))
    #             embed.add_field(name="Lose Count", value=id.get("lose_count"))
    #             embed.add_field(name="Win Streak", value=id.get("win_streak"))
    #             embed.add_field(name="Best Win Streak", value=id.get("best_win_streak"))

    #             await ctx.channel.send(embed = embed)
    #             return
            
    #         await ctx.channel.send("<@{0.author.id}> is not in the database.".format(ctx))

    #if this command is activated, it should delete BattleInProgress of previous battle
    @commands.command()
    async def fight(self,ctx, user: nextcord.Member):
        """initiates fight process"""
        #checks if both users are in the database
        for id in mongodb.player_collection.find():
            if id["_id"] == user.id:

                for idTwo in mongodb.player_collection.find():
                    if idTwo["_id"] == ctx.author.id:

                        p1 = ctx.author.id
                        p2 = user.id
                        battle = Battle(p1,p2)
                        battle_entry = {
                            "p1": battle.p1,
                            "p2": battle.p2,
                            "gained_rank": battle.gained_rank,                            
                            "lost_rank": battle.lost_rank,
                            "dispute": battle.dispute,
                            "p1Win": battle.p1Win  
                        }
                        mongodb.battle_collection.insert_one(battle_entry)
                        await ctx.channel.send("settle it in smash", view =AttackButtons())
                        return
            else:
                await ctx.channel.send("user {0} and {1} is not in the database".format(user.id,ctx.author.id))
                #can implement later, adds one user or another in the database if not found.
                
                
            


def setup(client):
    client.add_cog(Bot_Commands(client))