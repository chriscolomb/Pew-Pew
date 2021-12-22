import nextcord
from nextcord.abc import _Overwrites
from nextcord.interactions import Interaction
import mongodb
import UpdateELO
from battle import Battle
from datetime import datetime as dt



#Buttons to start fights, figure out how to timeout button
class AttackButtons(nextcord.ui.View):
    def __init__(self, p1=None, p2=None, client = None, battle_thread=None):
        super().__init__(timeout=None)
        self.p1 = p1
        self.p2 = p2
        self.client = client
        self.battle_thread = battle_thread
        
    async def interaction_check1(self, player_to_check,interaction):
        return player_to_check.id == interaction.user.id

    async def handleApproveorDeny(self,button: nextcord.ui.Button, interaction: nextcord.Interaction, approveClicked):
        button.disable = True
        if approveClicked:
                #gets user and mention username
                user_id = self.p1.id
                user_id2 = self.p2.id
                guild_id = interaction.message.guild.id
                server = self.client.get_guild(guild_id)
                #retrieves username from discord - the numbers
                p1_name = str(server.get_member(user_id))[:-5]
                p2_name = str(server.get_member(user_id2))[:-5]

                if await self.interaction_check1(self.p2,interaction):
                    embed = nextcord.Embed(
                        title = "Fight Accepted!",
                        colour = nextcord.Colour.from_rgb(121,180,183)
                    )
                    #creates thread and sends the view to that thread
                    self.battle_thread = await nextcord.TextChannel.create_thread(interaction.channel,name ="{} vs {}".format(p1_name,p2_name), 
                    message = interaction.message, auto_archive_duration= 60, reason = None)
                    await interaction.response.edit_message(embed=embed, view =None)
                    thread_embed = nextcord.Embed(
                        title = "Let the Fight Begin!",
                        description = "Win or lose?",
                        colour = nextcord.Colour.from_rgb(121,180,183)
                    )
                    await self.battle_thread.send(embed=thread_embed, view = WinorLose(self.p1, self.p2, self.battle_thread))
                else:
                    await interaction.response.send_message("only {} can click approve".format(p2_name)) 
        else:
            embed = nextcord.Embed(
                title = "Fight Denied!",
                description = "Try again some other time.",
                colour = nextcord.Colour.from_rgb(121,180,183)
            )
            await interaction.response.edit_message(embed=embed, view =None)

    
    #approve button for matches, should check to see if the @mention is the one who clicked it
    @nextcord.ui.button(label= "ACCEPT", emoji = None, style= nextcord.ButtonStyle.green, custom_id= "fight01")
    async def approve_button(self, button, interaction):
        await self.handleApproveorDeny(button, interaction, True)       
    
    #deny button for matches
    @nextcord.ui.button(label= "DENY", emoji = None, style= nextcord.ButtonStyle.danger, custom_id= "deny01")
    async def deny_button(self, button, interaction):
        
        await self.handleApproveorDeny(button, interaction, False)
        


class WinorLose(nextcord.ui.View):
    def __init__(self, p1=None, p2=None, battle_thread=None):
        super().__init__(timeout = None)
        self.clicks = 0
        self.p1 = p1
        self.p2 = p2
        self.battle_thread = battle_thread

    async def interaction_check1(self, player_to_check,interaction):
        return player_to_check.id == interaction.user.id

    #Where the magic will happen; the buttons will call the updateELO class from here, also need to disable buttons here
    async def handle_win_or_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction, clicker_wins):

        #retrieves the user and depending who the last past who clicks the button, updates the ELO and player_collection
        get_user = interaction.user.id
        
        #number of clicks in the view
        if self.clicks == 2:
            #creates battle collection
            battle = Battle(self.p1.get_id(),self.p2.get_id())
            battle_entry = {
                "p1": battle.p1,
                "p2": battle.p2,
                }
            mongodb.battle_collection.insert_one(battle_entry)

            #if last person clicks win
            if clicker_wins:
                for player in mongodb.battle_collection.find():
                    if player["p1"] == get_user:
                        winner = self.p1
                        loser = self.p2
                    elif player["p2"] == get_user:
                        winner = self.p2
                        loser = self.p1  
            else:
                for player in mongodb.battle_collection.find():
                    if player["p1"] == get_user:
                        winner = self.p2                       
                        loser = self.p1
                    elif player["p2"] == get_user:
                        winner = self.p1
                        loser = self.p2  
            UpdateELO.update_elo_rating(winner, loser)

            #add battle to history collection
            history_entry = {
                "winner": winner.get_id(),
                "loser": loser.get_id(),
                "date": dt.now()
            }
            mongodb.history_collection.insert_one(history_entry)

            for player in mongodb.player_collection.find():
                if player["_id"] == winner.get_id():
                    copy = player["match_history"]
                    if player["match_history"][0].get(str(loser.get_id())) != None:
                        copy[0][str(loser.get_id())] += 1
                    else:                 
                        copy[0][str(loser.get_id())] = 1    
                    query = {
                        "_id": winner.get_id(),
                    }
                    update_query = { "$set": { "match_history": copy } }
                    mongodb.player_collection.update_one(query, update_query)
                elif player["_id"] == loser.get_id():
                    copy = player["match_history"]
                    if player["match_history"][1].get(str(winner.get_id())) != None:
                        copy[1][str(winner.get_id())] += 1
                    else:                 
                        copy[1][str(winner.get_id())] = 1    
                    query = {
                        "_id": loser.get_id(),
                    }
                    update_query = { "$set": { "match_history": copy } }
                    mongodb.player_collection.update_one(query, update_query)
                    
            

            

            #deletes battle collection
            delete_query = {}
            for player in mongodb.battle_collection.find():
                if player["p1"] == winner.get_id():
                    delete_query = {"p1": winner.get_id()}
                else:
                    delete_query = {"p1": loser.get_id()}
            mongodb.battle_collection.delete_one(delete_query)

            embed_end_match = nextcord.Embed(
                title = "Match Complete!",
                description = "<@{}> Wins Against <@{}>!".format(winner.get_id(), loser.get_id()),
                colour = nextcord.Colour.from_rgb(121,180,183)
            )

            await interaction.response.edit_message(embed= embed_end_match, 
            view=MatchComplete(self.p1, self.p2, self.battle_thread))
        else:
            await interaction.response.edit_message(view=self)  
      

    #button for winning
    @nextcord.ui.button(label= "WIN", disabled = False, emoji = None, style= nextcord.ButtonStyle.green, custom_id= "iWin01")
    async def win_button(self, button, interaction):
        
        if await self.interaction_check1(self.p2, interaction) or await self.interaction_check1(self.p1, interaction):
            button.disabled = True
            self.clicks+=1
            await self.handle_win_or_lose(button,interaction, True)
        
    #button for losing
    @nextcord.ui.button(label= "LOSE", emoji = None, style= nextcord.ButtonStyle.danger, custom_id= "iLose01")
    async def loss_button(self, button, interaction):
        
        if await self.interaction_check1(self.p2, interaction) or await self.interaction_check1(self.p1, interaction):
            button.disabled = True
            self.clicks += 1
            await self.handle_win_or_lose(button,interaction, False)
    
    #button for losing
    @nextcord.ui.button(label= "RESET", emoji = None, style= nextcord.ButtonStyle.secondary, custom_id= "reset01")
    async def reset_button(self, button, interaction):
        thread_embed = nextcord.Embed(
            title = "Buttons Have Been Reset.",
            description = "Win or lose?",
            colour = nextcord.Colour.from_rgb(121,180,183)
        )
        await interaction.response.edit_message(embed=thread_embed, view=WinorLose(self.p1,self.p2, self.battle_thread))

class MatchComplete(nextcord.ui.View):
    def __init__(self, p1=None, p2=None, battle_thread = None):
        super().__init__(timeout=None)
        self.p1 = p1
        self.p2 = p2

        self.p1_clicks = 0
        self.p2_clicks = 0
        self.battle_thread = battle_thread 

    async def interaction_check1(self, player_to_check, interaction):
        return player_to_check.id == interaction.user.id
    
    
    @nextcord.ui.button(label= "REMATCH",emoji = None, style= nextcord.ButtonStyle.green, custom_id= "rematch01")
    async def rematch_button(self,button, interaction):
        if await self.interaction_check1(self.p2, interaction):
            self.p2_clicks +=1
        elif await self.interaction_check1(self.p1, interaction):
            self.p1_clicks += 1
        if self.p1_clicks >= 1 and self.p2_clicks >= 1:
            thread_embed = nextcord.Embed(
                title = "Let the Fight Begin!",
                description = "Win or lose?",
                colour = nextcord.Colour.from_rgb(121,180,183)
            )
            await interaction.message.delete()
            await interaction.response.send_message(embed=thread_embed, view = WinorLose(self.p1, self.p2, self.battle_thread))
    
    @nextcord.ui.button(label= "GGs",emoji = None, style= nextcord.ButtonStyle.secondary, custom_id= "endMatch01")
    async def endMatch_button(self, button, interaction):        
        
        if await self.interaction_check1(self.p2, interaction) or await self.interaction_check1(self.p1, interaction):
            thread_embed = nextcord.Embed(
                title = "GGs!",
                description = "Thanks for playing!",
                colour = nextcord.Colour.from_rgb(121,180,183)
            )
            await interaction.response.edit_message(embed=thread_embed, view = None)
            # await self.battle_thread.delete()
            