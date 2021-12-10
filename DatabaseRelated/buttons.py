import nextcord
import mongodb
import updateELO

#Buttons to start fights
class AttackButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    #handles the interaction between the approve button, deny button and the win or loss button
    #still need to implement: if the wrong user clicks approve it won't go through
    async def handle_approve(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("let the fight begin", view = WinorLose())
    
    #handles the deny button, deletes the entry if fight was denied.
    async def handle_deny(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        
        delete_battle_query = {""}
        mongodb.delete_one(delete_battle_query)
        await interaction.response.send_message("Fight Denied, try again another time")

    
    #approve button for matches
    @nextcord.ui.button(label= "approve", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.primary, custom_id= "fight01")
    async def approve_button(self, button, interaction):
        await self.handle_approve(button,interaction)      
    
    #deny button for matches
    @nextcord.ui.button(label= "deny", emoji= "<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "deny01")
    async def deny_button(self, button, interaction):
        await interaction.response.send_message("Fight Denied, try again another time")

class WinorLose(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    #Where the magic will happen; the buttons will call the updateELO class from here, also need to disable buttons here
    async def handle_win_or_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        #placeholder, this is where the button will interact with the database
        win_button.disabled == True
        loss_button.disabled == True

    #button for winning
    @nextcord.ui.button(label= "win", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "Iwin01")
    async def win_button(self, button, interaction):
        get_user = interaction.user.id
        await interaction.response.send_message("Lucky you")
        await self.handle_win_or_lose(button,interaction)
    #button for losing
    @nextcord.ui.button(label= "lose", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "Ilose01")
    async def loss_button(self, button, interaction):
        get_user = interaction.user.id
        await interaction.response.send_message("I'm sorry for your loss")
    
    #button for dispute
    @nextcord.ui.button(label= "dispute", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "dispute01")
    async def dispute_button(self, button, interaction):
        get_user = interaction.user.id
        await interaction.response.send_message("uhoh")
    #button for confirm, could timeout this then erase after 1 minute
    @nextcord.ui.button(label= "confirm", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "confirm01")
    async def confirm_button(self, button, interaction):
        get_user = interaction.user.id
        await interaction.response.send_message("battle confirmed")

    