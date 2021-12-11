import nextcord
from nextcord.client import Client
from nextcord.ext import commands
import sys

#parent directory import
sys.path.append('DatabaseRelated')
import mongodb
from player import Player
from buttons import AttackButtons
from multipledispatch import dispatch



class Bot_Commands(commands.Cog):

    def __init__(self,client):
        self.client = client
    
    @commands.command()
    # @dispatch(nextcord.ext.commands.context.Context, nextcord.member.Member)
    async def stats(self,ctx, user: nextcord.Member=None):
        """This will reveal all stats for player"""
        if user != None:
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
        else:
            for id in mongodb.player_collection.find():
                if id["_id"] == ctx.author.id:
                    title = "Stats for {0.author}".format(ctx)

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
    
    
    # @commands.command()
    # @dispatch(nextcord.ext.commands.context.Context)
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
    

    #was going to make self stats but this didn't work, weird overload.

    

    #if this command is activated, it should delete BattleInProgress of previous battle
    @commands.command()
    async def fight(self,ctx, user: nextcord.Member):
        """initiates fight process"""
        #checks if both users are in the database
        for id in mongodb.player_collection.find():
            if id["_id"] == user.id:
                for idTwo in mongodb.player_collection.find():
                    if idTwo["_id"] == ctx.author.id:
                        await ctx.channel.send("both players found")
                        p1_entry = Player(idTwo["_id"], rating=idTwo["rating"], win_count=idTwo["win_count"], lose_count=idTwo["lose_count"], win_streak=idTwo["win_streak"], best_win_streak=idTwo["best_win_streak"])
                        p2_entry = Player(id["_id"], rating=id["rating"], win_count=id["win_count"], lose_count=id["lose_count"], win_streak=id["win_streak"], best_win_streak=id["best_win_streak"])
                        await ctx.channel.send("Settle it in Smash.", view =AttackButtons(p1_entry, p2_entry))
                        return
        
        await ctx.channel.send("One or two players not found.")
        #can implement later, adds one user or another in the database if not found.
                
                
            


def setup(client):
    client.add_cog(Bot_Commands(client))