#!venv/Scripts/python.exe
import sqlite3
from sqlite3.dbapi2 import Error
import discord
from dotenv import load_dotenv
import mysql.connector
from discord.ext import commands
import os
from discord.ext.commands import errors
import random as ra
from datetime import datetime
import re
import asyncio
import copypasta

#region init
insulti = []

url_pattern = r'(http|https)://.*'
youtube_url = r'(http|https)://(www.youtube.com|youtu.be)/.*'
animated_emoji_pattern = r'^<a:[a-zA-Z0-9_-]+:[0-9]+>$'

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
load_dotenv()
rigenera_insulti()
bot = commands.Bot(command_prefix='$')
TOKEN = os.environ.get('TOKEN')
creator_id = os.environ.get("CREATORE")
bot.remove_command('help')
#endregion

# region Funzioni

def get_name(ctx):
    name = ctx.author.nick or ctx.author.name
    return name

async def check_admin(ctx):
    if not ctx.message.author.guild_permissions.administrator and ctx.message.author.id != int(creator_id):
        await ctx.send("Solo un admin può usare questo comando! " + genera_insulto())
        raise Error("Comando admin da persone non admin!")

async def check_creator(ctx):
    if ctx.message.author.id != int(creator_id):
        await ctx.send("Solo il creatore di questo bot può usare questo comando! " + genera_insulto())
        raise Error("Comando creatore da persone non creatore!")
    
def genera_insulto():
    return insulti[ra.randint(0, len(insulti) - 1)]

risposte_dic = {
    'hellothere': 'General Kenobi!',
    'dio': 'NON SI BESTEMMIA ' + genera_insulto().upper() + '!',
    'gigi': 'IL MIO ACERRIMO NEMICO',
    'nigga': 'Un po\' razzista ma ok',
    'negro': 'Un po\' razzista ma ok',
    'pepsiman': ['Pepsi Man!ðﾟﾍﾶ', 'https://www.player.it/wp-content/uploads/2018/12/Pepsiman-il-videogioco.jpg', 'https://youtu.be/z54MpfR3XE4'],
    'ðﾟﾍﾷ':copypasta.WINE,
    'grazie':'Prego',
    ':pepesad:':'F',
    ':(':':)))',
    ':)':':(',
    '69': 'nice',
    'flymetothemoon':'ðﾟﾚﾀðﾟﾌﾑðﾟﾌﾠ',
    'mussolini':['VIVA IL DVCE!ðﾟﾤﾚ', 'https://youtu.be/i4J4xSzpSuA'],
    ':nonni:':[':Nonni:', '^\n|', 'Epic Nonni fail'],
    'easports':copypasta.EA,
    ':love:': '<a:love:807947104164118558>',
    ':index:': '<a:index:807948759047733268>',
    ':ncry:': '<a:ncry:807989716011712532>',
    ':dance:': '<a:dance:807989758151360562>',
    ':pepelaugh:': '<a:pepelaugh:807990173282467840>',
    ':pepehype:': '<a:pepehype:807990347099537429>',
    ':pepesimp:': '<a:pepesimp:807990373167267870>',
    ':pepegacredit:': '<a:pepegacredit:807990388160987227>',
    ':ultrayaya:': '<a:ultrayaya:807990399155044373>',
    ':catjamdisco:': '<a:catjamdisco:808006353594482728>',
    ':cringepepepet:': '<a:cringepepepet:808006318359052378>',
    ':dogdance:': '<a:ultrayaya:808006262834724866>'
    }
def switch_messaggi(msg):
    for key in risposte_dic.keys():
        if msg.__contains__(key):
            return risposte_dic[key]
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
    m = await ctx.send(f'{member.mention} è stato avvertito per {reason}')
    await m.add_reaction('🕵🏻‍♂️')
    data = datetime.now().strftime(r'%Y-%d-%m %H:%M:%S')
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

@bot.command()
async def clean(ctx, arg):
    await check_admin(ctx)
    def check_member(ctx, arg):
        return ctx.author == arg
    try:
        converter = commands.MemberConverter()
        member = await converter.convert(ctx, arg)
        await ctx.channel.purge(check=lambda ctx:check_member(ctx, member))
    except errors.MemberNotFound:
        await ctx.channel.purge(limit=int(arg))
    m = await ctx.channel.send(f'Messaggi cancellati, ora pagami {ra.randint(10, 200)}$')
    await m.add_reaction('🧹')
    await asyncio.sleep(4)
    await m.delete()

@bot.command()
async def dado(ctx):
    await ctx.channel.send(f'Lanciando il dado...')
    await asyncio.sleep(2)
    await ctx.channel.send(ra.randint(1, 6))

@bot.command(aliases=['gm'])
async def gaymeter(ctx, member : discord.Member):
    perc = ra.randint(0, 100)
    BARRA = '█'
    VUOTO = '░'
    if str(member.id) == creator_id:
        perc = 0
    elif member.id == bot.user.id:
        perc = 100
    quanti = int(perc/10)
    restanti = 10-quanti
    await ctx.channel.send(f'{member.mention} è gay al {BARRA*quanti}{VUOTO*restanti} {perc}%\n')

@bot.command()
async def coin(ctx):
    num = ra.randint(1, 2)
    coin = 'testa' if num == 1 else 'croce' 
    await ctx.channel.send(f"è uscito {coin}")

#endregion

#region Sezione intercettazione messaggi

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.replace(' ', '').lower()
    messaggio = switch_messaggi(msg)
    if messaggio != 404:
        if isinstance(messaggio, list):
            for m in messaggio:
                if re.match(url_pattern, m) and not re.match(youtube_url, m):
                    e = discord.Embed()
                    e.set_image(url=m)
                    await message.channel.send(embed=e)
                else:
                    await message.channel.send(m)
        elif re.match(animated_emoji_pattern, messaggio):
            await message.delete()
            await message.channel.send(messaggio)
        else:
            await message.channel.send(messaggio)
        
    await bot.process_commands(message) # Vai alla parte comandi dopo aver controllato

#endregion

#region Error handler

@somma.error
@dividi.error
@moltiplica.error
@clean.error
async def somma_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hai messo tutti i parametri? :thinking:")

@warn.error
@mostra_infrazioni.error
@pulisci_fedina.error
@insulta.error
@kick.error
@gaymeter.error
async def membro_non_trovato(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Persona non trovata! Ma sei ' + genera_insulto() + '?')
    else:
        print(error)

@cancella_insulto_dalla_lista.error
async def cosa_non_trovata(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('L\' id deve essere un numero ' + genera_insulto().lower() + '!')

#endregion

#region help
from bonus import Help, Tris
bot.add_cog(Help(bot, risposte_dic))
bot.add_cog(Tris(bot))

#endregion

bot.run(TOKEN)
