import nextcord
from nextcord.interactions import Interaction
import mongodb
import UpdateELO
from battle import Battle



#Buttons to start fights, figure out how to timeout button
class AttackButtons(nextcord.ui.View):
    def __init__(self, p1=None, p2=None, client = None):
        super().__init__(timeout=None)
        self.p1 = p1
        self.p2 = p2
        self.client = client

    async def interaction_check(player_to_check, interaction):
        return player_to_check == interaction.user

    async def handleApproveorDeny(self,button,interaction, approveClicked):
        
        button.disable = True
        if approveClicked:
            if self.interaction_check(self.p1, interaction):
                #gets user and mention username
                user_id = self.p1.id
                user_id2 = self.p2.id
                guild_id = interaction.message.guild.id
                server = self.client.get_guild(guild_id)
                #retrieves username from discord - the numbers
                p1_name = str(server.get_member(user_id))
                p2_name = str(server.get_member(user_id2))
                p1_name = p1_name[:-4]
                p2_name = p2_name[:-4]

                #creates thread and sends the view to that thread
                battle_thread = await nextcord.TextChannel.create_thread(interaction.channel,name ="{} vs {}".format(p1_name,p2_name), message = interaction.message, auto_archive_duration= 60, reason = None)
                await battle_thread.send(content = "let the fight begin", view = WinorLose(self.p1, self.p2,battle_thread))
            else:
                interaction.responce.send_message("only {} can click approve".format(self.p2)) 
        else:
            await interaction.response.edit_message(content ="Fight Denied, try again another time", view =self)

    #approve button for matches, should check to see if the @mention is the one who clicked it
    @nextcord.ui.button(label= "ACCEPT", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "fight01")
    async def approve_button(self, button, interaction):
        
        self.handleApproveorDeny(self, button, interaction, True)       
    
    #deny button for matches
    @nextcord.ui.button(label= "DENY", emoji= "<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "deny01")
    async def deny_button(self, button, interaction):
        
        self.handleApproveorDeny(self, button, interaction, False)
        


class WinorLose(nextcord.ui.View):
    def __init__(self, p1=None, p2=None, battle_thread = None):
        super().__init__(timeout=None)
        self.clicks = 0
        self.p1 = p1
        self.p2 = p2
        self.battle_thread = battle_thread    

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
            #deletes battle collection
            delete_query = {}
            for player in mongodb.battle_collection.find():
                if player["p1"] == winner.get_id():
                    delete_query = {"p1": winner.get_id()}
                else:
                    delete_query = {"p1": loser.get_id()}
            mongodb.battle_collection.delete_one(delete_query)
            await interaction.response.edit_message(content = "<@{}> Wins Against <@{}>!".format(winner.get_id(), loser.get_id()), view=MatchComplete(self.p1,self.p2,self.battle_thread))  
        else:
            await interaction.response.edit_message(content="let the fight begin", view=self)        

    #button for winning
    @nextcord.ui.button(label= "WIN", disabled = False, emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "iWin01")
    async def win_button(self, button, interaction):
        
        if self.interaction_check(self.p2, interaction) or self.interaction_check(self.p1, interaction):
            button.disabled = True
            self.clicks+=1 
            button.disabled = True
            await self.handle_win_or_lose(button,interaction, True)
        else:
            interaction.response.send_message("only {} or {} can click the button".format(self.p1,self.p2))     
        
    #button for losing
    @nextcord.ui.button(label= "LOSE", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "iLose01")
    async def loss_button(self, button, interaction):
        
        if self.interaction_check(self.p2, interaction) or self.interaction_check(self.p1, interaction):
            button.disabled = True
            self.clicks += 1
            button.disabled = True
            await self.handle_win_or_lose(button,interaction, False)
        else:
            interaction.response.send_message("only {} or {} can click the button".format(self.p1,self.p2))

class MatchComplete(nextcord.ui.View,):
    def __init__(self, p1=None, p2=None, battle_thread = None):
        super().__init__(timeout=None)
        self.p1 = p1
        self.p2 = p2
        self.battle_thread = battle_thread  
    
    @nextcord.ui.button(label= "REMATCH",emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.primary, custom_id= "rematch01")
    async def rematch_button(self, interaction):
        if self.interaction_check(self.p2, interaction) or self.interaction_check(self.p1, interaction):
            await interaction.send_message("new match", view = WinorLose(self.p1,self.p2,self.battle_thread))
    
    @nextcord.ui.button(label= "End Match",emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.primary, custom_id= "endMatch01")
    async def endMatch_button(self, interaction):        
        if self.interaction_check(self.p2, interaction) or self.interaction_check(self.p1, interaction):
            await interaction.send_message("Goodbye", view = self)
            self.battle_thread.delete