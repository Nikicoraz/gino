#!venv/Scripts/python.exe
import sqlite3
from sqlite3.dbapi2 import Error
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random as ra
from datetime import datetime

conn =  sqlite3.connect('generale.db')
c = conn.cursor()
c.execute('SELECT *, oid FROM insulti')
_ = c.fetchall()
conn.close()
insulti = []
for i in _:
    insulti.append(i[0])
del _
load_dotenv()
bot = commands.Bot(command_prefix='$')
TOKEN = os.getenv('TOKEN')
creator_id = os.getenv("CREATORE")
# Funzioni

async def check_admin(ctx):
    if ctx.message.author.id != int(creator_id):
        await ctx.send("Solo il creatore di questo bot può usare questo comando! " + genera_insulto())
        raise Error("Comando admin da persone non admin!")
    
def genera_insulto():
    return insulti[ra.randint(0, len(insulti))]


# Sezione comandi bot

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    for guild in bot.guilds:
        print(f"Bot is being used in {guild.name} (id:{guild.id})")

@bot.command()
async def test(ctx, *, arg):
    await check_admin(ctx)
    name = ctx.author.nick or ctx.author.name
    await ctx.send(f'{name} sent {arg}')

@bot.command()
async def warn(ctx, member: discord.Member, *, reason='no reason'):
    
    await check_admin(ctx)
    await ctx.send(f'{member.mention} è stato avvertito per {reason}')
    data = datetime.now().strftime('%D %H:%M:%S')
    conn = sqlite3.connect('generale.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO fedina VALUES ({member.id}, '{reason}', '{data}')")
    conn.commit()
    conn.close()

@bot.command()
async def mostra_infrazioni(ctx, *, member: discord.Member):
    await check_admin(ctx)
    conn = sqlite3.connect('generale.db')
    c = conn.cursor()
    c.execute(f'SELECT reason, date FROM fedina WHERE user_id = {member.id}')
    infrazioni = c.fetchall()
    conn.close()
    for i, infrazione in enumerate(infrazioni, 1):
        await ctx.send(f'> infrazione {i}: `{infrazione[0]}` in data `{infrazione[1]}`')

@bot.command()
async def pulisci_fedina(ctx, *, member: discord.Member):
    await check_admin(ctx)
    conn = sqlite3.connect('generale.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM fedina WHERE user_id = {member.id}")
    conn.commit()
    conn.close()
    await ctx.send(f'Fedina penale di {member.mention} pulita con successo!')

@bot.command()
async def somma(ctx, a : float, b : float):
    await ctx.send(f'{genera_insulto()}, non sai neanche fare {a} + {b} = {a + b}')

@bot.command()
async def dividi(ctx, a : float, b : float):
    await ctx.send(f'{genera_insulto()}, non sai neanche fare {a} / {b} = {a / b}')

@bot.command()
async def moltiplica(ctx, a : float, b : float):
    await ctx.send(f'{genera_insulto()}, non sai neanche fare {a} * {b} = {a * b}')

@bot.command()
async def aggiungi_insulto(ctx, *, arg):
    #TODO regex per controllare il pattern
    conn = sqlite3.connect('generale.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO insulti VALUES ('{arg}')")
    conn.commit()
    conn.close()
    await ctx.send("Insulto aggiunto!")

# Sezione intercettazione messaggi

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

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

@warn.error
@mostra_infrazioni.error
@pulisci_fedina.error
async def membro_non_trovato(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Persona non trovata! Ma sei ' + genera_insulto() + '?')

bot.run(TOKEN)