import discord
import os
from pip 

client = discord.Client()
TOKEN = os.getenv('TOKEN')
print(TOKEN)
print(os.getenv('ciao'))
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        print(f"Bot is being used in {guild.name} (id:{guild.id})")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('hello there'):
        await message.channel.send('General Kenobi!')
client.run(TOKEN)
