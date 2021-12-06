import discord
from discord.ext import commands
import sys

#parent directory import
sys.path.append('DatabaseRelated')
import mongodb
from player import Player

class Bot_Commands(commands.Cog):

    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def stats(self,ctx, user: discord.Member):
        for id in mongodb.player_collection.find():
            if id["_id"] == user.id:
                title = "Stats for {0.user}".format(ctx)

                embed = discord.Embed(
                    title = title,
                    colour = discord.Colour.green()
                )

                embed.add_field(name="Rating", value=id.get("rating"))
                embed.add_field(name="Win Count", value=id.get("win_count"))
                embed.add_field(name="Lose Count", value=id.get("lose_count"))
                embed.add_field(name="Win Streak", value=id.get("win_streak"))
                embed.add_field(name="Best Win Streak", value=id.get("best_win_streak"))

                await ctx.channel.send(embed = embed)
                return

        await ctx.channel.send("<@{0.user}> is not in the database.".format(ctx))

    @commands.command()
    async def fight(self,ctx):
        await ctx.send('not ready yet')


def setup(client):
    client.add_cog(Bot_Commands(client))