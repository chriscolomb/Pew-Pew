import nextcord


class AttackButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label= "approve", emoji="name: 917679403943723008", style= nextcord.ButtonStyle.primary, custom_id= "fight01")
    async def approve_button(self, button, interaction):
        interaction.response.send_message("let the fight begin")

    @nextcord.ui.button(label= "deny", emoji="name: 917679541722419232", style= nextcord.ButtonStyle.danger, custom_id= "deny01")
    async def deny_button(self, button, interaction):
        interaction.response.send_message("GG")
