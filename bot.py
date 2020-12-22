import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('NzkwNzg0MzU0NTgxNzQxNTk5.X-FpUg.9oY420NitrAJ6any9V3iUUMK0pE')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)