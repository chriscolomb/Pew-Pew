import nextcord
from nextcord import message
from nextcord import guild
from nextcord.channel import TextChannel
import mongodb
import UpdateELO
from battle import Battle
from nextcord import Guild


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
        user_id = self.p1.id
        print(user_id)
        # to fix https://stackoverflow.com/questions/64221377/discord-py-rewrite-get-member-function-returning-none-for-all-users-except-bot
        thread_name = Guild.fetch_member(user_id)        
        battle_thread = await nextcord.TextChannel.create_thread(interaction.channel,name ="{}".format(thread_name), message = interaction.message, auto_archive_duration= 60, reason = None)
        await battle_thread.send(content = "let the fight begin", view = WinorLose(self.p1, self.p2)) 
        #await interaction.response.edit_message(content = "let the fight begin", 
        #view = WinorLose(self.p1, self.p2))
        #await nextcord.Thread.send(interaction.channel,content = "let the fight begin", 
        #view = WinorLose(self.p1, self.p2))
        
                
    
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
    async def handle_win_or_lose(self, button: nextcord.ui.Button, interaction: nextcord.Interaction, clicker_wins):
        button.disabled = True
        viewClass = self
        get_user = interaction.user.id
        if self.clicks == 2:
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
            delete_query = {}
            for player in mongodb.battle_collection.find():
                if player["p1"] == winner.get_id():
                    delete_query = {"p1": winner.get_id()}
                else:
                    delete_query = {"p1": loser.get_id()}
            mongodb.battle_collection.delete_one(delete_query)
            await interaction.response.edit_message(content = "<@{}> Wins Against <@{}>!".format(winner.get_id(), loser.get_id()), view=MatchComplete())  
        else:
            await interaction.response.edit_message(content="let the fight begin", view=self)        

    #button for winning
    @nextcord.ui.button(label= "WIN", disabled = False, emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.green, custom_id= "Iwin01")
    async def win_button(self, button, interaction):
        self.clicks+=1 
        button.disabled = True
        await self.handle_win_or_lose(button,interaction, True)     
    
    #button for losing
    @nextcord.ui.button(label= "LOSE", emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.danger, custom_id= "Ilose01")
    async def loss_button(self, button, interaction):
        self.clicks += 1
        button.disabled = True
        await self.handle_win_or_lose(button,interaction, False)

class MatchComplete(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label= "FINISHED", disabled=True, emoji="<:Cutedragon:794999307048321044>", style= nextcord.ButtonStyle.primary, custom_id= "confirm01")
    async def confirm_button(self, interaction):
        
        await interaction.send_message("match complete")
