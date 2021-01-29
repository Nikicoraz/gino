#!venv/Scripts/python.exe
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='$')
client = discord.Client()
TOKEN = os.getenv('TOKEN')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    for guild in bot.guilds:
        print(f"Bot is being used in {guild.name} (id:{guild.id})")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.event
async def on_message(message):
    msg = message.content.lower()
    if msg.__contains__('hello there'):
        await message.channel.send('General Kenobi!')




bot.run(TOKEN)
client.run(TOKEN)