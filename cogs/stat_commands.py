import nextcord
from nextcord.ext import commands
import sys
import random


#parent directory import
sys.path.append('DatabaseRelated')
sys.path.append('cogs')
import mongodb
from player import Player
import operator

class Statistic(commands.Cog):
    """Statistic Commands"""

    def __init__(self,client: commands.Bot):
        self.client = client

    async def check_empty(self,array):
        return not array
        
    @commands.command()
    async def stats(self,ctx, user: nextcord.Member=None):
        """
        See player statistics\n
        **Usage:**
        > For yourself: `=stats`
        > For others: `=stats @player`
        """
        #TTD 753129805318455356 
        #Test 575869943346757682
        server = self.client.get_guild(575869943346757682)
        if user != None:
            for id in mongodb.player_collection.find():
                if id["_id"] == user.id:
                    title = "Stats for {0}".format(user)[:-5]

                    embed = nextcord.Embed(
                        title = title,
                        colour = nextcord.Colour.from_rgb(121,180,183)
                    )

                    embed.add_field(name="Rating", value=id.get("rating"))
                    embed.add_field(name="Win Count", value=id.get("win_count"))
                    embed.add_field(name="Lose Count", value=id.get("lose_count"))
                    embed.add_field(name="Win Streak", value=id.get("win_streak"))
                    embed.add_field(name="Best Win Streak", value=id.get("best_win_streak"))
                    
                    main_array = id.get("main")
                    array_check = await self.check_empty(main_array)
                    if not array_check:
                        emoji_display = {}
                        main_tuple = id.get("main")
                        emoji_array = []
                        
                        #get mains by emoji
                        for emoji in main_tuple:
                            emoji_name_id =await server.fetch_emoji(emoji)
                            emoji_name = emoji_name_id.name 
                            emoji_display[emoji_name] = emoji_name_id.id
                            emoji_array.append("<:{}:{}>".format(emoji_name, emoji_display[emoji_name]))
                        
                        value = ""
                        for emoji in emoji_array:
                            value += emoji + " "
                        
                        embed.add_field(name="Mains", value = value)

                    secondary_array = id.get("secondary")
                    array_check2 = await self.check_empty(secondary_array)
                    if not array_check2:
                        emoji_display = {}
                        secondary_tuple = id.get("secondary")
                        emoji_array = []

                        for emoji in secondary_tuple:
                            emoji_name_id =await server.fetch_emoji(emoji)
                            emoji_name = emoji_name_id.name 
                            emoji_display[emoji_name] = emoji_name_id.id
                            emoji_array.append("<:{}:{}>".format(emoji_name, emoji_display[emoji_name]))
                        
                        value = ""
                        for emoji in emoji_array:
                            value += emoji + " "

                        embed.add_field(name="Secondaries", value = value)
                    
                    await ctx.channel.send(embed = embed)
                    return
        else:
            for id in mongodb.player_collection.find():
                if id["_id"] == ctx.author.id:
                    title = "Stats for {0.author}".format(ctx)[:-5]

                    embed = nextcord.Embed(
                        title = title,
                        colour = nextcord.Colour.from_rgb(121,180,183)
                    )

                    embed.add_field(name="Rating", value=id.get("rating"))
                    embed.add_field(name="Win Count", value=id.get("win_count"))
                    embed.add_field(name="Lose Count", value=id.get("lose_count"))
                    embed.add_field(name="Win Streak", value=id.get("win_streak"))
                    embed.add_field(name="Best Win Streak", value=id.get("best_win_streak"))

                    main_array = id.get("main")
                    array_check = await self.check_empty(main_array)
                    if not array_check:
                        emoji_display = {}
                        main_tuple = id.get("main")
                        emoji_array = []
                        
                        #get mains by emoji
                        for emoji in main_tuple:
                            emoji_name_id =await server.fetch_emoji(emoji)
                            emoji_name = emoji_name_id.name 
                            emoji_display[emoji_name] = emoji_name_id.id
                            emoji_array.append("<:{}:{}>".format(emoji_name, emoji_display[emoji_name]))
                        
                        value = ""
                        for emoji in emoji_array:
                            value += emoji + " "
                        
                        embed.add_field(name="Mains", value = value)

                    secondary_array = id.get("secondary")
                    array_check2 = await self.check_empty(secondary_array)
                    if not array_check2:
                        emoji_display = {}
                        secondary_tuple = id.get("secondary")
                        emoji_array = []

                        for emoji in secondary_tuple:
                            emoji_name_id =await server.fetch_emoji(emoji)
                            emoji_name = emoji_name_id.name 
                            emoji_display[emoji_name] = emoji_name_id.id
                            emoji_array.append("<:{}:{}>".format(emoji_name, emoji_display[emoji_name]))
                        
                        value = ""
                        for emoji in emoji_array:
                            value += emoji + " "

                        embed.add_field(name="Secondaries", value = value)
                    

                                        
                    #key, value = emoji_display.popitem()
                    # for key in emoji_display:
                    #     new_value = int(emoji_display[key])                            
                    #     embed.add_field(name="main(s)", value = {"<:{}:{}>".format( str(key), int(new_value))})

                    #embed.add_field(name="main(s)", value = emoji_array)

                    # embed.set_footer(text="Generated on " + dt.now().strftime("%m/%d/%y at %I:%M %p"))

                    await ctx.channel.send(embed = embed)
                    return
        embed = nextcord.Embed(
            title = "Player is not in the database.",
            colour = nextcord.Colour.from_rgb(121,180,183)
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def rankings(self,ctx):
        """
        See server player rankings\n
        **Usage:** `=rankings`
        > Players are divided by tiers:
        > `Diamond:  2200 or more`
        > `Platinum: 1850 to 2199`
        > `Gold:     1500 to 1849`
        > `Silver:   1150 to 1499`
        > `Bronze:      0 to 1149`
        """
        rankings = []
        player = {
            "id": None,
            "rating": 0,
            "tier": None
        }

        guild_members = []
        async for member in ctx.guild.fetch_members(limit=None):
            guild_members.append(member.id)
        for id in mongodb.player_collection.find().sort("rating", -1):
            if id["_id"] in guild_members:
                player["id"] = id["_id"]
                player["rating"] = id["rating"]
                player["tier"] = Player.get_tier(player["rating"])
                rankings.append(player.copy())
                player.clear()

        embed = nextcord.Embed(
            title = "Rankings",
            colour = nextcord.Colour.from_rgb(121,180,183)
        )
        # embed.set_footer(text="Generated on " + dt.now().strftime("%m/%d/%y at %I:%M %p"))

        diamond_rankings = []
        platinum_rankings = []
        gold_rankings = []
        silver_rankings = []
        bronze_rankings = []
        for element in rankings:
            if element["tier"] == "Diamond":
                diamond_rankings.append(element)
            elif element["tier"] == "Platinum":
                platinum_rankings.append(element)
            elif element["tier"] == "Gold":
                gold_rankings.append(element)
            elif element["tier"] == "Silver":
                silver_rankings.append(element)
            elif element["tier"] == "Bronze":
                bronze_rankings.append(element)
        
        rank = 1
        if diamond_rankings:
            diamond_value = ""
            for element in diamond_rankings:
                diamond_value += str(rank) + ". " + str(self.client.get_user(element["id"]))[:-5] + " - `" + str(element["rating"]) + "`\n"
                rank += 1
            embed.add_field(name="Diamond", value=diamond_value)
        if platinum_rankings:
            platinum_value = ""
            for element in platinum_rankings:
                platinum_value += str(rank) + ". " + str(self.client.get_user(element["id"]))[:-5] + " - `" + str(element["rating"]) + "`\n"
                rank += 1
            embed.add_field(name="Platinum", value=platinum_value)
        if gold_rankings:
            gold_value = ""
            for element in gold_rankings:
                gold_value += str(rank) + ". " + str(self.client.get_user(element["id"]))[:-5] + " - `" + str(element["rating"]) + "`\n"
                rank += 1
            embed.add_field(name="Gold", value=gold_value)
        if silver_rankings:
            silver_value = ""
            for element in silver_rankings:
                silver_value += str(rank) + ". " + str(self.client.get_user(element["id"]))[:-5] + " - `" + str(element["rating"]) + "`\n"
                rank += 1
            embed.add_field(name="Silver", value=silver_value)
        if bronze_rankings:
            bronze_value = ""
            for element in bronze_rankings:
                bronze_value += str(rank) + ". " + str(self.client.get_user(element["id"]))[:-5] + " - `" + str(element["rating"]) + "`\n"
                rank += 1
            embed.add_field(name="Bronze", value=bronze_value)

        await ctx.channel.send(embed = embed)

    @commands.command()
    async def wins(self,ctx, user: nextcord.Member=None):
        """
        See win/lose counts against players\n
        **Usage:** `=wins`
        > Shows top 10 win/lose counts against players
        """

        server = self.client.get_guild(575869943346757682)
        if user != None:
            for id in mongodb.player_collection.find():
                if id["_id"] == user.id:
                    title = "Wins/Loses for {0}".format(user)[:-5] + " (`{}`)".format(str(id["rating"]))

                    embed = nextcord.Embed(
                        title = title,
                        colour = nextcord.Colour.from_rgb(121,180,183)
                    )

                    wins = id["match_history"][0]
                    sorted_wins = sorted(wins.items(), key=operator.itemgetter(1), reverse=True)
                    win_value = ""
                    count = 0
                    for win in sorted_wins:
                        if count != 10:
                            win_value += "`" + str(win[1]) + "x` " + str(self.client.get_user(int(win[0])))[:-5] + "\n"
                            count += 1

                    loses = id["match_history"][1]
                    sorted_loses = sorted(loses.items(), key=operator.itemgetter(1), reverse=True)
                    lose_value = ""
                    count = 0
                    for lose in sorted_loses:
                        if count != 10:
                            lose_value += "`" + str(lose[1]) + "x` " + str(self.client.get_user(int(lose[0])))[:-5] + "\n"
                            count += 1
                    

                    if len(wins) != 0:
                        embed.add_field(name="Wins", value=win_value)
                    if len(loses) != 0:
                        embed.add_field(name="Loses", value=lose_value)

                    await ctx.channel.send(embed = embed)
                    return
        else:
            for id in mongodb.player_collection.find():
                if id["_id"] == ctx.author.id:
                    title = "Wins/Loses for {0.author}".format(ctx)[:-5] + " (`{}`)".format(str(id["rating"]))

                    embed = nextcord.Embed(
                        title = title,
                        colour = nextcord.Colour.from_rgb(121,180,183)
                    )

                    wins = id["match_history"][0]
                    sorted_wins = sorted(wins.items(), key=operator.itemgetter(1), reverse=True)
                    win_value = ""
                    count = 0
                    for win in sorted_wins:
                        if count != 10:
                            win_value += "`" + str(win[1]) + "x` " + str(self.client.get_user(int(win[0])))[:-5] + "\n"
                            count += 1

                    loses = id["match_history"][1]
                    sorted_loses = sorted(loses.items(), key=operator.itemgetter(1), reverse=True)
                    lose_value = ""
                    count = 0
                    for lose in sorted_loses:
                        if count != 10:
                            lose_value += "`" + str(lose[1]) + "x` " + str(self.client.get_user(int(lose[0])))[:-5] + "\n"
                            count += 1
                    
                    if len(wins) != 0:
                        embed.add_field(name="Wins", value=win_value)
                    if len(loses) != 0:
                        embed.add_field(name="Loses", value=lose_value)

                    await ctx.channel.send(embed = embed)
                    return
        embed = nextcord.Embed(
            title = "Player is not in the database.",
            colour = nextcord.Colour.from_rgb(121,180,183)
        )
        await ctx.channel.send(embed=embed)


    

    

    
def setup(client):
    client.add_cog(Statistic(client))
