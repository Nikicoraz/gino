#!venv/Scripts/python.exe
import sqlite3
from sqlite3.dbapi2 import Error
import discord
from discord.ext import commands
import os
from discord.ext.commands.core import check
from dotenv import load_dotenv
import random as ra
from datetime import datetime
import re

#region init
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
bot.remove_command('help')
#endregion

# region Funzioni

def get_name(ctx):
    name = ctx.author.nick or ctx.author.name
    return name

async def check_admin(ctx):
    if ctx.message.author.id != int(creator_id):
        await ctx.send("Solo il creatore di questo bot può usare questo comando! " + genera_insulto())
        raise Error("Comando admin da persone non admin!")
    
def genera_insulto():
    return insulti[ra.randint(0, len(insulti) - 1)]

def switch_messaggi(msg):
    dic = {
        'hello there': 'General Kenobi!',
        'dio': 'NON SI BESTEMMIA ' + genera_insulto().upper() + '!',
        'gigi': 'IL MIO ACERRIMO NEMICO',
        'nigga': 'Un po\' razzista ma ok'
        }

    for key in dic.keys():
        if msg.__contains__(key):
            return dic[key]
    return 404 

#endregion

#region Sezione comandi bot

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    for guild in bot.guilds:
        print(f"Bot is being used in {guild.name} (id:{guild.id})")

@bot.command()
async def test(ctx, *, arg):
    await check_admin(ctx)
    await ctx.send(f'{get_name(ctx)} sent {arg}')

@bot.command(aliases=['i'])
async def insulta(ctx, *, member: discord.Member):
    await ctx.send(f'{member.mention} è un {genera_insulto().lower()}\n\n> Messaggio cordialmente inviato da {get_name(ctx)}')

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

@bot.command(aliases=['mi'])
async def mostra_infrazioni(ctx, *, member: discord.Member):
    conn = sqlite3.connect('generale.db')
    c = conn.cursor()
    c.execute(f'SELECT reason, date FROM fedina WHERE user_id = {member.id}')
    infrazioni = c.fetchall()
    conn.close()
    for i, infrazione in enumerate(infrazioni, 1):
        await ctx.send(f'> infrazione {i}: `{infrazione[0]}` in data `{infrazione[1]}`')
    if len(infrazioni) == 0:
        await ctx.send(f"{member.mention} non ha mai fatto un'infrazione")

@bot.command(aliases=['pf'])
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

@bot.command(aliases=['ai'])
async def aggiungi_insulto(ctx, *, arg):
    pattern = r'[a-zA-Z0-9 ]+'
    if not re.match(pattern, arg):
        await ctx.send('Formato messaggio non supportato :(')
        return
    conn = sqlite3.connect('generale.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO insulti VALUES ('{arg}')")
    conn.commit()
    conn.close()
    await ctx.send("Insulto aggiunto!")

@bot.command()
async def visualizza_lista_insulti(ctx):
    check_admin(ctx)
    conn = sqlite3.connect('generale.db')
    c = conn.cursor()
    c.execute('SELECT *, oid FROM insulti')
    for i in c.fetchall():
        await ctx.send('> ' + i)
    conn.close()

#endregion

#region Sezione intercettazione messaggi

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()
    messaggio = switch_messaggi(msg)
    if messaggio != 404:
        await message.channel.send(messaggio)

    await bot.process_commands(message) # Vai alla parte comandi dopo aver controllato

#endregion

#region Error handler

@somma.error
@dividi.error
@moltiplica.error
async def somma_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Non hai messo 2 numeri!!!")

@warn.error
@mostra_infrazioni.error
@pulisci_fedina.error
@insulta.error
async def membro_non_trovato(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Persona non trovata! Ma sei ' + genera_insulto() + '?')

#endregion

#region help

@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='Help', description='ciao, usa $help <comando> per avere piu\' informazioni!')
    em.add_field(name='Admin', value='warn, pulisci_fedina(pf)')
    em.add_field(name='Casual', value='aggiungi_insulto(ai), mostra_infrazioni(mi), insulta(i)')
    em.add_field(name='Matematica', value='somma, dividi, moltiplica')
    await ctx.send(embed = em)

@help.command()
async def warn(ctx):
    em = discord.Embed(title='Warn', description='Aggiunge una infrazione sulla fedina di una persona', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$warn <persona> [ragione]')
    await ctx.send(embed=em)

@help.command(aliases=['pf'])
async def pulisci_fedina(ctx):
    em = discord.Embed(title='Pulisci Fedina', description='Pulisce la fedina penale di una persona', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$pulisci_fedina <persona>')
    em.add_field(name='alias', value='$pf')
    await ctx.send(embed=em)

@help.command(aliases=['mi'])
async def mostra_infrazioni(ctx):
    em = discord.Embed(title='Mostra Infrazioni', description='Mostra le infrazioni penali di una persona', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$mostra_infrazioni <persona>')
    em.add_field(name='alias', value='$mi')
    await ctx.send(embed=em)

@help.command(aliases=['ai'])
async def aggiungi_insulto(ctx):
    em = discord.Embed(title='Aggiungi Insulto', description='In caso hai un insulto simpatico da aggiungere al database', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$aggiungi_insulto [insulto]')
    em.add_field(name='alias', value='$ai')
    await ctx.send(embed=em)

@help.command(aliases=['i'])
async def insulta(ctx):
    em = discord.Embed(title='Insulta', description='Insulta una persona', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$insulta <persona>')
    em.add_field(name='alias', value='$i')
    await ctx.send(embed=em)

#endregion

bot.run(TOKEN)