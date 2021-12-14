import nextcord
from nextcord import message
from nextcord import channel
from nextcord import threads
from nextcord.client import Client
from nextcord.ext import commands
import sys

from nextcord.threads import ThreadMember

#parent directory import
sys.path.append('DatabaseRelated')
import mongodb
from player import Player
from buttons import AttackButtons
from buttons import WinorLose 
import editdatabase



class Bot_Commands(commands.Cog):

    def __init__(self,client):
        self.client = client
    
    @commands.command()
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
            await ctx.channel.send("<@{0.user}> is not in the database.".format(ctx))
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
            await ctx.channel.send("<@{0.author.id}> is not in the database.".format(ctx))
    

    #if this command is activated, it should delete BattleInProgress of previous battle
    @commands.command()
    async def fight(self,ctx, user: nextcord.Member):
        """initiates fight process"""
        not_in_db_count = 0
        entries_added = False
        while not entries_added:
            #checks if both users are in the database, if not it adds them
            for id in mongodb.player_collection.find():
                if id["_id"] == user.id:
                    for idTwo in mongodb.player_collection.find():
                        if idTwo["_id"] == ctx.author.id:
                            await ctx.channel.send("both players found")
                            p1_entry = Player(idTwo["_id"], rating=idTwo["rating"], win_count=idTwo["win_count"], lose_count=idTwo["lose_count"], win_streak=idTwo["win_streak"], best_win_streak=idTwo["best_win_streak"])
                            p2_entry = Player(id["_id"], rating=id["rating"], win_count=id["win_count"], lose_count=id["lose_count"], win_streak=id["win_streak"], best_win_streak=id["best_win_streak"])
                            entries_added = True
                            #channelT = self.client.get_channel(ThreadMember.thread_id)
                            #await channelT.send(content = "Settle it in Smash.")
                    
                            #gets the desired username without the #
                            guild_id = ctx.message.guild.id
                            server = self.client.get_guild(guild_id)
                            member_name = str(server.get_member(ctx.author.id))
                            username = member_name[0:len(member_name)-5]
                            username = username + member_name[len(member_name)- 4: len(member_name)]

                            #checks to see if the username is the title (which would be just the thread) and if it is, only do win or lose view
                            if str(ctx.message.channel) == username:
                                viewButton = WinorLose(p1_entry, p2_entry)                                   
                            else:
                                viewButton = AttackButtons(p1_entry, p2_entry, self.client)
                                
                                
                            await ctx.channel.send("Settle it in Smash.", view= viewButton)                            
                            return
                        else:
                            not_in_db_count += 1
                            author = ctx.author.id
                            
                else:
                    not_in_db_count += 1
                    author = user.id
            if not_in_db_count == 1:
                editdatabase.EditDatabase.createPlayer(author)
            else:
                editdatabase.EditDatabase.createPlayer(ctx.author.id)
                editdatabase.EditDatabase.createPlayer(user.id)

        
        await ctx.channel.send("added user to database")
        #can implement later, adds one user or another in the database if not found.
                
                
            


def setup(client):
    client.add_cog(Bot_Commands(client))