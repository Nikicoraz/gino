import discord
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
TOKEN = os.getenv('TOKEN')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        print(f"Bot is being used in {guild.name} (id:{guild.id})")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()
    if msg.__contains__('hello there'):
        await message.channel.send('General Kenobi!')
    elif msg.startswith('n/'):
        if msg.__contains__('gigi'):
            await message.author.create_dm()
            await message.author.dm_channel.send("GIGI IL MIO ACERRIMO NEMICO")
client.run(TOKEN)
