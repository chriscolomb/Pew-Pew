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

class Bot_Commands(commands.Cog):

    def __init__(self,client):
        self.client = client    

    async def character_dictionary_method(self):
        character_dictionary = {}
        value = []
        characters = open("server_emojis.txt")
        for line in characters:
            key,value = line.split()
            character_dictionary[key] = value
        characters.close()

        return character_dictionary

    @commands.command()
    async def stats(self,ctx, user: nextcord.Member=None):
        """This will reveal all stats for player"""
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
                    
                    # embed.set_footer(text="Generated on " + dt.now().strftime("%m/%d/%y at %I:%M %p"))
                    
                    await ctx.channel.send(embed = embed)
                    return
        else:
            #TTD 753129805318455356 
            server = self.client.get_guild(575869943346757682)
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

                    emoji_display = {}
                    main_tupple = id.get("main")
                    secondary_tupple = id.get("secondary")
                    emoji_array = []
                    emoji_array2 = []
                    #get mains by emoji
                    for emojis in main_tupple:
                        emoji_name_id =await server.fetch_emoji(emojis)
                        emoji_name = emoji_name_id.name 
                        emoji_display[emoji_name] = emoji_name_id.id
                        emoji_array.append("<:{}:{}>".format(emoji_name, emoji_display[emoji_name]))
                    
                    embed.add_field(name="main(s)", value = emoji_array)

                    for emojis2 in secondary_tupple:
                        emoji_name_id =await server.fetch_emoji(emojis2)
                        emoji_name = emoji_name_id.name 
                        emoji_display[emoji_name] = emoji_name_id.id
                        emoji_array2.append("<:{}:{}>".format(emoji_name, emoji_display[emoji_name]))

                    embed.add_field(name="secondaries", value = emoji_array2)

                                        
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
    

    

    #if this command is activated, it should delete BattleInProgress of previous battle
    @commands.command()
    async def fight(self,ctx, user: nextcord.Member):
        """initiates fight process"""
        if user.id == ctx.author.id:
            embed = nextcord.Embed(
                title = "You cannot fight yourself.",
                colour = nextcord.Colour.from_rgb(121,180,183)
            )
            await ctx.channel.send(embed=embed)

            return
        not_in_db_count = 0
        entries_added = False
        while not entries_added:
            #checks if both users are in the database, if not it adds them
            for id in mongodb.player_collection.find():
                if id["_id"] == user.id:
                    for idTwo in mongodb.player_collection.find():
                        if idTwo["_id"] == ctx.author.id:
                            #creates entry for player object
                            p1_entry = Player(idTwo["_id"], rating=idTwo["rating"], win_count=idTwo["win_count"], lose_count=idTwo["lose_count"], win_streak=idTwo["win_streak"], best_win_streak=idTwo["best_win_streak"])
                            p2_entry = Player(id["_id"], rating=id["rating"], win_count=id["win_count"], lose_count=id["lose_count"], win_streak=id["win_streak"], best_win_streak=id["best_win_streak"])
                            entries_added = True
                    
                            #gets the desired username without the #
                            guild_id = ctx.message.guild.id
                            server = self.client.get_guild(guild_id)
                            member_name1 = str(server.get_member(ctx.author.id))
                            member_name2 = str(server.get_member(user.id))
                            username1 = member_name1[0:len(member_name1)-5]
                            username2 = member_name2[0:len(member_name2)-5]
                            #checks to see if the username is the title (which would be just the thread) and if it is, only do win or lose view
                            if str(ctx.message.channel) == "{} vs {}".format(username1,username2):
                                viewButton = WinorLose(p1_entry, p2_entry,ctx.message.channel)                                   
                            else:
                                viewButton = AttackButtons(p1_entry, p2_entry, self.client)                               
                            

                            embed = nextcord.Embed(
                                title = "Settle it in Smash!",
                                description = "<@{}>, do you accept match against <@{}>?".format(p2_entry.get_id(), p1_entry.get_id()),
                                colour = nextcord.Colour.from_rgb(121,180,183)
                            )

                            #Sends the view to the right channel and the corresponding view associated with the thread or channel
                            await ctx.channel.send(embed=embed, view= viewButton)                            
                            return
                        
                        #if user is not in database adds them to the database    
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

    @commands.command()
    async def random(self, ctx):
        fighters = ['mario', 'donkey_kong', 'link', 'samus', 'dark_samus', 'yoshi', 'kirby', 'fox', 'pikachu', 'luigi', 'ness', 'captain_falcon', 'jigglypuff', 'peach', 'daisy', 'bowser', 'ice_climbers', 'sheik', 'zelda', 'dr_mario','pichu', 'falco', 'marth', 'lucina', 'young_link', 'ganondorf', 'mewtwo', 'roy', 'chrom','mr_game_and_watch', 'meta_knight', 'pit', 'dark_pit', 'zero_suit_samus', 'wario', 'snake', 'ike','pokemon_trainer', 'diddy_kong', 'lucas', 'sonic', 'king_dedede', 'olimar', 'lucario', 'rob', 'toon_link','wolf', 'villager', 'mega_man', 'wii_fit_trainer', 'rosalina_and_luma', 'little_mac', 'greninja', 'mii_brawler', 'mii_gunner', 'mii_swordfighter', 'palutena', 'pac_man', 'robin', 'shulk', 'bowser_jr', 'duck_hunt', 'ryu', 'ken', 'cloud','corrin', 'bayonetta', 'inkling', 'ridley', 'simon', 'richter', 'king_k_rool', 'isabelle', 'incineroar','piranha_plant', 'joker', 'dq_hero', 'banjo_and_kazooie', 'terry', 'byleth', 'minmin', 'steve', 'sephiroth', 'pyra', 'kazuya', 'sora']

        alts = ['main', 'main2', 'main3', 'main4', 'main5', 'main6', 'main7', 'main8']

        character_images = []

        url = "https://raw.githubusercontent.com/chriscolomb/ssbu/master/OPTIMIZED%20PORTRAITS/"
        for fighter in fighters:
            if "mii" not in fighter:
                for alt in alts:
                    image_url = url + fighter + '_' + alt + '.png'
                    character_images.append(image_url)
            else:
                image_url = url + fighter + '.png'
                character_images.append(image_url)
        
        embed = nextcord.Embed()
        embed.set_image(url=random.choice(character_images))
        embed.colour = nextcord.Colour.from_rgb(121,180,183)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def rankings(self,ctx):
        rankings = []
        player = {
            "id": None,
            "rating": 0,
            "tier": None
        }

        for id in mongodb.player_collection.find().sort("rating", -1):
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
    async def addCharacter(self,ctx, *args):
        """adds main to your account"""
        dictionary = await self.character_dictionary_method()
        character_array = []

        for characters in args:
            isIn = True
            player_id = {"_id": ctx.author.id}
            try: dictionary[characters]
            except KeyError:
                await ctx.channel.send("character {} doesn't exist".format(characters))
                isIn = False
                return
            if isIn:
                characterID = int(dictionary[characters])
                character_array.append(characterID)
                await ctx.channel.send("lucky you")
        
        update_main_query = { "$set": { "main": character_array } }
        mongodb.player_collection.update_one(player_id, update_main_query)

    @commands.command()
    async def addSecondary(self,ctx, *args):
        """add seconary to your account"""
        dictionary = await self.character_dictionary_method()
        character_array = []

        for characters in args:
            isIn = True
            player_id = {"_id": ctx.author.id}
            try: dictionary[characters]
            except KeyError:
                await ctx.channel.send("character {} doesn't exist".format(characters))
                isIn = False
                return
            if isIn:
                characterID = int(dictionary[characters])
                character_array.append(characterID)
                await ctx.channel.send("lucky you")
        
        update_main_query = { "$set": { "secondary": character_array } }
        mongodb.player_collection.update_one(player_id, update_main_query)


def setup(client):
    client.add_cog(Bot_Commands(client))