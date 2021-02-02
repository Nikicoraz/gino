#!venv/Scripts/python.exe
import sqlite3
from sqlite3.dbapi2 import Error
import discord
from discord import role
import mysql.connector
from discord.client import _cancel_tasks
from discord.errors import DiscordServerError
from discord.ext import commands
import os
from discord.ext.commands import errors
from discord.ext.commands.core import check
from dotenv import load_dotenv
import random as ra
from datetime import datetime
import re
from time import sleep
#region init
insulti = []

def rigenera_insulti():
    global insulti
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password='bJGoz5qBPHo$#i5k',
    database='freedbtech_generale')
    c = conn.cursor()
    c.execute('SELECT * FROM insulti')
    _ = c.fetchall()
    conn.close()
    for i in _:
        insulti.append(i[1])
    del _

rigenera_insulti()
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
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send("Solo un admin può usare questo comando! " + genera_insulto())
        raise Error("Comando admin da persone non admin!")

async def check_creator(ctx):
    if ctx.message.author.id != int(creator_id):
        await ctx.send("Solo il creatore di questo bot può usare questo comando! " + genera_insulto())
        raise Error("Comando creatore da persone non creatore!")
    
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
async def test(ctx, member : discord.Member):
    await check_creator(ctx)
    

@bot.command(aliases=['p'])
async def probabilita(ctx, *, arg):
    import random
    await ctx.send(f'{arg} ha una probabilità del {random.randint(0, 100)}%')

@bot.command(aliases=['i'])
async def insulta(ctx, *, member: discord.Member):
    await ctx.send(f'{member.mention} è un {genera_insulto().lower()}\n\n> -Messaggio cordialmente inviato da *{get_name(ctx)}*')

@bot.command()
async def warn(ctx, member: discord.Member, *, reason='no reason'):
    await check_admin(ctx)
    await ctx.send(f'{member.mention} è stato avvertito per {reason}')
    data = datetime.now().strftime(r'%d-%m-%Y %H:%M:%S')
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password='bJGoz5qBPHo$#i5k',
    database='freedbtech_generale')
    c = conn.cursor()
    c.execute(f"INSERT INTO fedina VALUES ({member.id}, '{reason}', '{data}')")
    conn.commit()
    conn.close()

@bot.command(aliases=['mi'])
async def mostra_infrazioni(ctx, *, member: discord.Member):
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password='bJGoz5qBPHo$#i5k',
    database='freedbtech_generale')
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
    await check_creator(ctx)
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password='bJGoz5qBPHo$#i5k',
    database='freedbtech_generale')
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
async def visualizza_lista_insulti(ctx):
    await check_creator(ctx)
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password='bJGoz5qBPHo$#i5k',
    database='freedbtech_generale')
    c = conn.cursor()
    c.execute('SELECT * FROM insulti')
    insulti = ''
    for i in c.fetchall():
        insulti += '> ' + str(i[1]) + ' id:' + str(i[0]) + '\n'
    em = discord.Embed(title='Lista insulti', description=insulti)
    await ctx.send(embed=em)
    conn.close()

@bot.command()
async def cancella_insulto_dalla_lista(ctx, num):
    await check_creator(ctx)
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password='bJGoz5qBPHo$#i5k',
    database='freedbtech_generale')
    c = conn.cursor()
    c.execute('DELETE FROM insulti WHERE id = ' + num)
    conn.commit()
    conn.close()
    await ctx.send('Insulto id: ' + num + ' cancellato se esiste')
    rigenera_insulti()

@bot.command(aliases=['ai'])
async def aggiungi_insulto(ctx, *, arg):
    pattern = r'[a-zA-Z0-9 ]+'
    if not re.match(pattern, arg):
        await ctx.send('Formato messaggio non supportato :(')
        return
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password='bJGoz5qBPHo$#i5k',
    database='freedbtech_generale')
    c = conn.cursor()
    c.execute(f"INSERT INTO insulti VALUES (null, '{arg}')")
    conn.commit()
    conn.close()
    await ctx.send("Insulto aggiunto!")
    rigenera_insulti()

@bot.command()
async def kick(ctx, member : discord.Member, *, reason='no reason'):
    await check_admin(ctx)
    if not ctx.message.author.guild_permissions.kick_members:
        await ctx.channel.send('Non hai i permessi per kiccare le persone! ' + genera_insulto())
        return
    elif member.guild_permissions.administrator:
        await ctx.channel.send('Non si può kiccare l\'amministratore! :(')
        return
    else:
        await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason='no reason'):
    await check_admin(ctx)
    if not ctx.message.author.guild_permissions.ban_members:
        await ctx.channel.send('Non hai i permessi per bannare le persone! ' + genera_insulto())
        return
    elif member.guild_permissions.administrator:
        await ctx.channel.send('Non si può bannare l\'amministratore! :(')
        return
    else:
        await member.ban(reason=reason)

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
@kick.error
async def membro_non_trovato(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Persona non trovata! Ma sei ' + genera_insulto() + '?')

@cancella_insulto_dalla_lista.error
async def cosa_non_trovata(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('L\' id deve essere un numero ' + genera_insulto().lower() + '!')


#endregion

#region help

@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='Help', description='ciao, usa $help <comando> per avere piu\' informazioni!')
    em.add_field(name='Creatore', value='pulisci_fedina(pf), cancella_insulto_dalla_lista, visualizza_lista_insulti')
    em.add_field(name='Admin', value='warn, kick, ban')
    em.add_field(name='Casual', value='aggiungi_insulto(ai), mostra_infrazioni(mi), insulta(i), probabilita(p)')
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

@help.command(aliases=['i'])
async def insulta(ctx):
    em = discord.Embed(title='Insulta', description='Insulta una persona', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$insulta <persona>')
    em.add_field(name='alias', value='$i')
    await ctx.send(embed=em)

@help.command()
async def visualizza_lista_insulti(ctx):
    em = discord.Embed(title='Visualizza lista insulti', description='Visualizza la lista degli insulti', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$visualizza_lista_insulti')
    em.add_field(name='alias', value='Nessuno')
    await ctx.send(embed=em)

@help.command(aliases=['p'])
async def probabilita(ctx):
    em = discord.Embed(title='Probabilita', description='Probabilità che succeda una cosa', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$probabilita [cosa che deve accadere]')
    em.add_field(name='alias', value='$p')
    await ctx.send(embed=em)

@help.command(aliases=['ai'])
async def aggiungi_insulto(ctx):
    em = discord.Embed(title='Aggiungi Insulto', description='In caso hai un insulto simpatico da aggiungere al database', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$aggiungi_insulto [insulto]')
    em.add_field(name='alias', value='$ai')
    await ctx.send(embed=em)


@help.command()
async def cancella_insulto_dalla_lista(ctx):
    em = discord.Embed(title='Cancella insulto dalla lista', description='Cancella un insulto dal database, comando lungo apposta per essere certi di quello che si fa', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$cancella_insulto_dalla_lista [id]')
    em.add_field(name='alias', value='Nessuno')
    await ctx.send(embed=em)

@help.command()
async def kick(ctx):
    em = discord.Embed(title='Kick', description='Caccia una persona dal server', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$kick <persona> [motivo]')
    em.add_field(name='alias', value='Nessuno')
    await ctx.send(embed=em)

@help.command()
async def ban(ctx):
    em = discord.Embed(title='ban', description='Banna una persona dal server', color = ctx.message.author.color)
    em.add_field(name='**Sintassi**', value='$ban <persona> [motivo]')
    em.add_field(name='alias', value='Nessuno')
    await ctx.send(embed=em)

#endregion

bot.run(TOKEN)