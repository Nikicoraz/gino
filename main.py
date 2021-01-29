#!venv/Scripts/python.exe
import sqlite3
from discord.ext import commands
import os
from dotenv import load_dotenv
import random as ra

conn =  sqlite3.connect('insulti.db')
c = conn.cursor()
c.execute('SELECT *, oid FROM insulti')
_ = c.fetchall()
conn.close()
insulti = []
for i in _:
    insulti.append(i[0])
del _
print(insulti)
load_dotenv()
bot = commands.Bot(command_prefix='$')
TOKEN = os.getenv('TOKEN')

# Sezione comandi bot

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    for guild in bot.guilds:
        print(f"Bot is being used in {guild.name} (id:{guild.id})")

@bot.command()
async def test(ctx, *, arg):
    name = ctx.author.nick or ctx.author.name
    await ctx.send(f'{name} sent {arg}')


@bot.command()
async def somma(ctx, a : float, b : float):
    await ctx.send(f'{insulti[ra.randint(0, len(insulti))]}, non sai neanche fare {a} + {b} = {a + b}')

@bot.command()
async def dividi(ctx, a : float, b : float):
    await ctx.send(f'{insulti[ra.randint(0, len(insulti))]}, non sai neanche fare {a} / {b} = {a / b}')

@bot.command()
async def moltiplica(ctx, a : float, b : float):
    await ctx.send(f'{insulti[ra.randint(0, len(insulti))]}, non sai neanche fare {a} * {b} = {a * b}')



# Sezione intercettazione messaggi



@bot.event
async def on_message(message):
    msg = message.content.lower()
    if msg.__contains__('hello there'):
        await message.channel.send('General Kenobi!')

    await bot.process_commands(message) # Vai alla parte comandi dopo aver controllato


# Error handler
@somma.error
@dividi.error
@moltiplica.error
async def somma_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Non hai messo 2 numeri!!!")

bot.run(TOKEN)