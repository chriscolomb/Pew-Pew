import nextcord
import mongodb
import updateELO
from player import Player


#Buttons to start fights
class AttackButtons(nextcord.ui.View):
    def __init__(self, p1=None, p2=None):
        super().__init__(timeout=None)
        self.p1 = p1
        self.p2 = p2

    #handles the interaction between the approve button, deny button and the win or loss button
    #still need to implement: if the wrong user clicks approve it won't go through
    async def handle_approve(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.edit_message(content = "let the fight begin", view = WinorLose(self.p1, self.p2))
    
    #handles the deny button, deletes the entry if fight was denied.
    async def handle_deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        
        delete_battle_query = {""}
        mongodb.delete_one(delete_battle_query)
        await interaction.response.send_message("Fight Denied, try again another time")

    
    #approve button for matches
    @nextcord.ui.button(label= "ACCEPT", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.primary, custom_id= "fight01")
    async def approve_button(self, button, interaction):
        await self.handle_approve(button,interaction)      
    
    #deny button for matches
    @nextcord.ui.button(label= "DENY", emoji= "<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "deny01")
    async def deny_button(self, button, interaction):
        await interaction.response.send_message("Fight Denied, try again another time")

class WinorLose(nextcord.ui.View):
    def __init__(self, p1=None, p2=None):
        super().__init__(timeout=None)
        #self.clicks = clicks
        self.p1 = p1
        self.p2 = p2
    

    #Where the magic will happen; the buttons will call the updateELO class from here, also need to disable buttons here
    async def handle_win_or_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        #placeholder, this is where the button will interact with the database
        button.disabled = True
        
        

    #button for winning
    @nextcord.ui.button(label= "WIN", disabled = False, emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "Iwin01")
    async def win_button(self, button, interaction):
        get_user = interaction.user.id
        #await interaction.response.send_message("Lucky you")
        await self.handle_win_or_lose(button,interaction)
        await interaction.response.edit_message(content = "<@{}> Wins".format(get_user), view=self)
        for player in mongodb.battle_collection.find({}, {"p1": 1, "p2": 1}):
            if player["p1"] == get_user:
                UpdateELO.update_elo_rating(self.p1, self.p2, True)
            elif player["p2"] == get_user:
                UpdateELO.update_elo_rating(self.p1, self.p2, False)
            # for p2 in mongodb.battle_collection.find({}, {"p1": 0, "p2": 1}):
            #     if p2["p1"] == get_user:
            #         p2_entry = Player.get_player(p2)
            #         if 
            #         UpdateELO.update_elo_rating(p1_entry, p2_entry, )
                
                

    #button for losing
    @nextcord.ui.button(label= "Lose", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "Ilose01")
    async def loss_button(self, button, interaction):
        get_user = interaction.user.id
        #await interaction.response.send_message("I'm sorry for your loss")
        await self.handle_win_or_lose(button,interaction)
        await interaction.response.edit_message(content = "<@{}> Loses".format(get_user),view=self)
    
    #button for dispute
    @nextcord.ui.button(label= "dispute", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "dispute01")
    async def dispute_button(self, button, interaction):
        get_user = interaction.user.id
        await interaction.response.send_message("uhoh")
    #button for confirm, could erase battle query from here
    @nextcord.ui.button(label= "confirm", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "confirm01")
    async def confirm_button(self, button, interaction):
        get_user = interaction.user.id
        await interaction.response.send_message("battle confirmed")