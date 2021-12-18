import nextcord
from nextcord.ext import commands
import sys

#parent directory import
sys.path.append('DatabaseRelated')
import mongodb
from player import Player
from buttons import AttackButtons
from buttons import WinorLose 
import editdatabase
import random

class Bot_Commands(commands.Cog):

    def __init__(self,client):
        self.client = client
    

    def Character_dictionary():
        global character_dictionary
        character_dictionary = {}
        characters = open("server_emojis.txt")
        for line in characters:
            key,value = line.split()
            character_dictionary[key] = value
        characters.close()

    @commands.command()
    async def stats(self,ctx, user: nextcord.Member=None):
        """This will reveal all stats for player"""
        if user != None:
            for id in mongodb.player_collection.find():
                if id["_id"] == user.id:
                    title = "Stats for {0}".format(user)

                    embed = nextcord.Embed(
                        title = title,
                        colour = nextcord.Colour.from_rgb(121,180,183)
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
                        colour = nextcord.Colour.from_rgb(121,180,183)
                    )

                    embed.add_field(name="Rating", value=id.get("rating"))
                    embed.add_field(name="Win Count", value=id.get("win_count"))
                    embed.add_field(name="Lose Count", value=id.get("lose_count"))
                    embed.add_field(name="Win Streak", value=id.get("win_streak"))
                    embed.add_field(name="Best Win Streak", value=id.get("best_win_streak"))

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
        fighters = ['mario', 'donkey_kong', 'link', 'samus', 'dark_samus', 'yoshi', 'kirby', 'fox', 'pikachu', 'luigi', 'ness', 'captain_falcon', 'jigglypuff', 'peach', 'daisy', 'bowser', 'ice_climbers', 'sheik', 'zelda', 'dr_mario','pichu', 'falco', 'marth', 'lucina', 'young_link', 'ganondorf', 'mewtwo', 'roy', 'chrom','mr_game_and_watch', 'meta_knight', 'pit', 'dark_pit', 'zero_suit_samus', 'wario', 'snake', 'ike','pokemon_trainer', 'diddy_kong', 'lucas', 'sonic', 'king_dedede', 'olimar', 'lucario', 'rob', 'toon_link','wolf', 'villager', 'mega_man', 'wii_fit_trainer', 'rosalina_and_luma', 'little_mac', 'greninja','mii_fighter', 'palutena', 'pac_man', 'robin', 'shulk', 'bowser_jr', 'duck_hunt', 'ryu', 'ken', 'cloud','corrin', 'bayonetta', 'inkling', 'ridley', 'simon', 'richter', 'king_k_rool', 'isabelle', 'incineroar','piranha_plant', 'joker', 'dq_hero', 'banjo_and_kazooie', 'terry', 'byleth', 'minmin', 'steve', 'sephiroth', 'pyra', 'kazuya', 'sora']

        alts = ['main', 'main2', 'main3', 'main4', 'main5', 'main6', 'main7', 'main8']

        character_images = []

        url = "https://raw.githubusercontent.com/chriscolomb/ssbu/master/OPTIMIZED%20PORTRAITS/"
        for fighter in fighters:
            if fighter != 'mii_fighter':
                for alt in alts:
                    image_url = url + fighter + '_' + alt + '.png'
                    character_images.append(image_url)
            elif fighter == 'mii_fighter':
                image_url = url + fighter + '_' + alts[0] + '.png'
                character_images.append(image_url)
        
        await ctx.channel.send(content=random.choice(character_images))

    @commands.command()
    async def addCharacter(self, ctx, character):
        #TTD 753129805318455356
        # emoji = None
        # player_id = {"_id": ctx.author.id}
        # TTD_server = self.client.get_guild(575869943346757682)
        # for emoji in TTD_server.emojis:
        #     if str(emoji.name) == character:
        #         update_main_query = {"$set": {"main": emoji}}
        #         mongodb.player_collection.update_one(player_id, update_main_query)
        player_id = {"_id": ctx.author.id}
        for character in character_dictionary:
            if character == character_dictionary[character]:
                ctx.message.send("character found")
        

def setup(client):
    client.add_cog(Bot_Commands(client))