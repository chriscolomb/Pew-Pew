import nextcord
import mongodb
import updateELO
from player import Player
from battle import Battle


#Buttons to start fights, figure out how to timeout button
class AttackButtons(nextcord.ui.View):
    def __init__(self, p1=None, p2=None):
        super().__init__(timeout=None)
        self.p1 = p1
        self.p2 = p2

    #approve button for matches, should check to see if the @mention is the one who clicked it
    @nextcord.ui.button(label= "ACCEPT", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "fight01")
    async def approve_button(self, button, interaction):
        battle = Battle(self.p1.get_id(),self.p2.get_id())
        battle_entry = {
            "p1": battle.p1,
            "p2": battle.p2,
            }
        mongodb.battle_collection.insert_one(battle_entry) 
        await interaction.response.edit_message(content = "let the fight begin", view = WinorLose(self.p1, self.p2))         
    
    #deny button for matches
    @nextcord.ui.button(label= "DENY", emoji= "<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "deny01")
    async def deny_button(self, button, interaction):
        button.disabled = True
        await interaction.response.edit_message(content ="Fight Denied, try again another time", view =MatchComplete())


class WinorLose(nextcord.ui.View):
    def __init__(self, p1=None, p2=None):
        super().__init__(timeout=None)
        self.clicks = 0
        self.p1 = p1
        self.p2 = p2    

    #Where the magic will happen; the buttons will call the updateELO class from here, also need to disable buttons here
    async def handle_win_or_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        button.disabled = True
        viewClass = None
        get_user = interaction.user.id
        if self.clicks == 2:
            viewClass = self
        else:
            viewClass = ConfirmorDispute()

        await interaction.response.edit_message(content = "<@{}> Wins".format(get_user), view=viewClass)
        for player in mongodb.battle_collection.find({}, {"p1": 1, "p2": 1}):
            if player["p1"] == get_user:
                updateELO.update_elo_rating(self.p1, self.p2)
            if player["p2"] == get_user:
                updateELO.update_elo_rating(self.p2, self.p1)
        #mongodb.battle_collection.delete_many({})        

    #button for winning
    @nextcord.ui.button(label= "WIN", disabled = False, emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "Iwin01")
    async def win_button(self, button, interaction):
        self.clicks+=1 
        await self.handle_win_or_lose(button,interaction)     
    
    #button for losing
    @nextcord.ui.button(label= "LOSE", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "Ilose01")
    async def loss_button(self, button, interaction):
        button.disabled = True
        viewClass = None
        get_user = interaction.user.id
        if self.clicks < 2:
            viewClass = self
        else:
            viewClass = ConfirmorDispute()
        await interaction.response.edit_message(content = "<@{}> Loses".format(get_user),view=viewClass)
        


class ConfirmorDispute(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)        
        self.clicks = 0      
    
    #button for confirm, could erase battle query from here
    @nextcord.ui.button(label= "CONFIRM", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "confirm01")
    async def confirm_button(self, button, interaction):
        self.clicks +=1
        get_user = interaction.user.id
        if self.clicks == 2:
            button.disabled = True
            delete_query = {}
            for player in mongodb.battle_collection.find({}, {"p1": 1, "p2": 1}):
                if player["p1"] == get_user:
                    delete_query = {"p1": get_user}
                else:
                    delete_query = {"p2": get_user}
            mongodb.battle_collection.delete_one(delete_query)
            await interaction.response.edit_message(content = "data sent, goodbye", view =MatchComplete())

   #button for dispute
    @nextcord.ui.button(label= "CANCEL", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "dispute01")
    async def dispute_button(self, button, interaction):
        get_user = interaction.user.id
        button.disabled = True
        delete_query = {}
        for player in mongodb.battle_collection.find({}, {"p1": 1, "p2": 1}):
            if player["p1"] == get_user:
                delete_query = {"p1": get_user}
            else:
                delete_query = {"p2": get_user}
        mongodb.battle_collection.delete_one(delete_query)
        await interaction.response.edit_message(content = "<@{}> Uhoh, your dispute will be followed up on".format(get_user), view =self ) 

class MatchComplete(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label= "FINISHED", disabled=True, emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.primary, custom_id= "confirm01")
    async def confirm_button(self, button, interaction):
        await interaction.send_message("match complete")
