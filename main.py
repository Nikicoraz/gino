﻿#!venv/Scripts/python.exe
import time
import discord
from discord import permissions
from discord import webhook
from discord import channel
from discord.ext.commands.core import check
from dotenv import load_dotenv
import mysql.connector
from mysql.connector.locales.eng import client_error
from mysql.connector.plugins import mysql_native_password
from discord.ext import commands
import os
from discord.ext.commands import errors
import random as ra
from datetime import datetime
import re
import asyncio
import copypasta
import opencv
from Network import get_html
from threading import Thread
from strings import get_string
from strings import reload_lang
import yt_dlp
import queue
from timer.timer import Timer

#region init
insulti = []
langs = {}

url_pattern = r'(http|https)://.*'
youtube_url = r'(http|https)://(www.youtube.com|youtu.be)/.*'
emoji_patterns = r'^<a:[a-zA-Z0-9_-]+:[0-9]+>$'

load_dotenv()
DATABASE_HOST = os.environ.get('DB_HOST')
DATABASE_PASSWORD = os.environ.get('DB_PASS')
DATABASE_PORT  = os.environ.get('DB_PORT') or 3306
bot = commands.Bot(command_prefix='$', intents=discord.Intents().all())
TOKEN = os.environ.get('TOKEN')
creator_id = os.environ.get("CREATORE")
bot.remove_command('help')

#endregion

# region Funzioni



def use_database(command, fetch=False, commit=False):
    _ = None
    conn = mysql.connector.connect(
    host=DATABASE_HOST,
    user='discord',
    password=DATABASE_PASSWORD,
    database='discord',
    port=DATABASE_PORT,
    charset="utf8mb4",
    collation="utf8mb4_general_ci",
    )

    c = conn.cursor()
    c.execute(command)
    if fetch:
        _ = c.fetchall()
    if commit:
        conn.commit()
    conn.close()
    return _


def rigenera_insulti():
    global insulti
    _ = use_database('SELECT * FROM insulti', fetch=True)
    for i in _:
        insulti.append(i[1])
    del _
rigenera_insulti()

def get_name(ctx):
    name = ctx.author.nick or ctx.author.name
    return name

async def check_admin(ctx):
    if not ctx.message.author.guild_permissions.administrator and ctx.message.author.id != int(creator_id):
        await ctx.send(get_string(ctx, 'admin_error') + genera_insulto())
        raise Exception("Comando admin da persone non admin!")

async def check_creator(ctx):
    if ctx.message.author.id != int(creator_id):
        await ctx.send(get_string(ctx, 'creator_error') + genera_insulto())
        raise Exception("Comando creatore da persone non creatore!")

async def send_webhook(ctx, message, user, avatar):
    wbhk = [x for x in await ctx.channel.webhooks()]
    if ctx.channel.name not in set([x.name for x in set(wbhk)]):
        whk = await ctx.channel.create_webhook(name=ctx.channel.name)
    else:
        whk = [x for x in set(wbhk)][0]
    await whk.send(content=message, username=user, avatar_url=avatar)
        
    
def genera_insulto():
    return insulti[ra.randint(0, len(insulti) - 1)]

risposte_dic = {
    'hellothere': 'General Kenobi!',
    'gigi': ('func','msgg = "IL MIO ACERRIMO NEMICO"'),
    'nigga': 'Un po\' razzista ma ok',
    'negro': 'Un po\' razzista ma ok',
    'pepsiman': ['Pepsi Man!🍾', 'https://www.player.it/wp-content/uploads/2018/12/Pepsiman-il-videogioco.jpg', 'https://youtu.be/z54MpfR3XE4'],
    'grazie':'Prego',
    'flymetothemoon':'🚀🌑🌠',
    'mussolini':['VIVA IL DVCE!✋', 'https://youtu.be/i4J4xSzpSuA'],
    ':nonni:':[':Nonni:', '^\n|', 'Epic Nonni fail'],
    'rasputin':['https://youtu.be/WhPvJOnHotE', copypasta.RASPUTIN, copypasta.RASPUTIN2],
    '🍷':copypasta.WINE,
    'easports':copypasta.EA,
    'obama':copypasta.OBAMA,
    'ahegao':copypasta.AHEGAO,
    'bitcoin':copypasta.BITCOIN,
    'bruh':copypasta.BRUH,
    'ciao':'https://tenor.com/view/culo-jodete-fuck-you-drunk-gif-10066511',
    'tasse':'Io le tasse non le pago!',

    # Emoji

    '🔫': '<:pistola:821669164107825174>',

    # Emoji Animate

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
    ':dogdance:': '<a:ultrayaya:808006262834724866>',
    ':frogroll:': '<a:frogroll:820979762977439744>',
    ':frogspeed:': '<a:frogspeed:835822136731762749>',
    ':frograinbow:': '<a:frograinbow:835822233740902412>',
    ':flushedwiggle:': '<a:flushedwiggle:836159484111486976>',
    ':pepehey:':'<a:pepehey:836159681915256842>',
    ':catmad:':'<a:catmad:836159843751690281>'

    }
def switch_messaggi(msg):
    # Piccola funzione molto utile
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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))

@bot.command()
async def test(ctx : discord.Message):
    pass

@bot.command(aliases=['p', 'probability'])
async def probabilita(ctx, *, arg):
    import random
    await ctx.send(arg + get_string(ctx, 'probabilita') + str(random.randint(0, 100)) + '%')

@bot.command(aliases=['i'])
async def insulta(ctx, *, member: discord.Member):
    # Prende un insulto dalla lista scaricata precedentemente dal database
    await ctx.send(f'{member.mention} è un {genera_insulto().lower()}\n\n> -Messaggio cordialmente inviato da *{get_name(ctx)}*')

@bot.command()
async def warn(ctx, member: discord.Member, *, reason='no reason'):
    await check_admin(ctx)
    m = await ctx.send(f'{member.mention}' + get_string(ctx, 'warn') + f'{reason}')
    await ctx.message.add_reaction('<:pepefedora:822422976796295198>')
    data = datetime.now().strftime(r'%Y-%m-%d %H:%M:%S') # Formattazione ora
    reason = reason.replace("'", "")
    use_database(f"INSERT INTO fedina VALUES ({member.id}, '{reason}', '{data}')", commit=True)

@bot.command(aliases=['mi', 'show_infractions'])
async def mostra_infrazioni(ctx, *, member: discord.Member = None):
    msg = ''
    if not member:
        member = ctx.author
    infrazioni = use_database(f'SELECT reason, date FROM fedina WHERE user_id = {member.id}', True)
    for i, infrazione in enumerate(infrazioni, 1):
        msg += f'> {get_string(ctx, "infrazione")} {i}: `{infrazione[0]}` {get_string(ctx, "in_data")} `{infrazione[1]}`\n'
    if len(infrazioni) == 0:
        await ctx.send(f"{member.mention} {get_string(ctx, 'mai_infra')}")
    await ctx.send(msg)

@bot.command(aliases=['pf', 'clean_infractions'])
async def pulisci_fedina(ctx, *, member: discord.Member):
    await check_creator(ctx)
    use_database(f"DELETE FROM fedina WHERE user_id = {member.id}", commit=True)
    await ctx.send(f'{get_string(ctx, "fed_pen_di")} {member.mention} {get_string(ctx, "pulita_con_succ")}')

@bot.command(aliases=['sum'])
async def somma(ctx, a : float, b : float):
    await ctx.send(f'{genera_insulto()}, non sai neanche fare {a} + {b} = {a + b}')

@bot.command(aliases=['divide'])
async def dividi(ctx, a : float, b : float):
    await ctx.send(f'{genera_insulto()}, non sai neanche fare {a} / {b} = {a / b}')

@bot.command(aliases=['multiply'])
async def moltiplica(ctx, a : float, b : float):
    await ctx.send(f'{genera_insulto()}, non sai neanche fare {a} * {b} = {a * b}')

@bot.command()
async def visualizza_lista_insulti(ctx):
    await check_creator(ctx)
    _ = use_database('SELECT * FROM insulti', True)
    insulti = ''
    for i in _:
        insulti += '> ' + str(i[1]) + ' id:' + str(i[0]) + '\n'
    em = discord.Embed(title='Lista insulti', description=insulti)
    await ctx.send(embed=em)

@bot.command()
async def cancella_insulto_dalla_lista(ctx, num):
    await check_creator(ctx)
    use_database('DELETE FROM insulti WHERE id = ' + num, commit=True)
    await ctx.send('Insulto id: ' + num + ' cancellato se esiste')
    rigenera_insulti()

@bot.command(aliases=['ai'])
async def aggiungi_insulto(ctx, *, arg):
    pattern = r'[a-zA-Z0-9 ]+'
    if not re.match(pattern, arg):
        await ctx.send('Formato insulto non supportato :(, sono accettate solo lettere e numeri')
        return
    use_database(f"INSERT INTO insulti VALUES (null, '{arg}')", commit=True)
    await ctx.send("Insulto aggiunto!")
    rigenera_insulti()

@bot.command()
async def kick(ctx, member : discord.Member, *, reason='no reason'):
    await check_admin(ctx)
    if not ctx.message.author.guild_permissions.kick_members:
        await ctx.channel.send(f'{get_string(ctx, "kick_error")} ' + genera_insulto())
        return
    elif member.guild_permissions.administrator:
        await ctx.channel.send(f'{get_string(ctx, "kick_amm")}')
        return
    else:
        await member.kick(reason=reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason='no reason'):
    await check_admin(ctx)
    if not ctx.message.author.guild_permissions.ban_members:
        await ctx.channel.send(f'{get_string(ctx, "ban_error")} ' + genera_insulto())
        return
    elif member.guild_permissions.administrator:
        await ctx.channel.send(get_string(ctx, "ban_amm"))
        return
    else:
        await member.ban(reason=reason)

@bot.command()
async def clean(ctx, arg):
    await check_admin(ctx)
    def check_member(ctx, arg):
        return ctx.author == arg
    try: 
        # Se si vuole cancellare oltre 5000 messaggi no
        if int(arg) > 5000:
            if ctx.message.author.id != int(creator_id):
                await ctx.channel.send(get_string(ctx, 'canc_errore'))
                return
    except:
        try:
            # Se e' un membro cancella messaggi suoi
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, arg)
            await ctx.channel.purge(check=lambda ctx:check_member(ctx, member))
        except errors.MemberNotFound:
            # Altrimenti cancella il numero indicato
            await ctx.channel.purge(limit=int(arg))
    m = await ctx.channel.send(f'{get_string(ctx, "costo")} {ra.randint(10, 200)}$')
    await m.add_reaction('🧹')
    await asyncio.sleep(4)
    await m.delete()

@bot.command(aliases=['dice'])
async def dado(ctx):
    await ctx.channel.send(get_string(ctx, 'dado'))
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
    await ctx.channel.send(f'{member.mention} {get_string(ctx, "gay")} {BARRA*quanti}{VUOTO*restanti} {perc}%\n')

@bot.command()
async def furrymeter(ctx, member : discord.Member):
    perc = ra.randint(0, 100)
    BARRA = '█'
    VUOTO = '░'
    if str(member.id) == creator_id:
        perc = 0
    quanti = int(perc/10)
    restanti = 10-quanti
    await ctx.channel.send(f'{member.mention} {get_string(ctx, "furry")} {BARRA*quanti}{VUOTO*restanti} {perc}%:cat:\n')

@bot.command()
async def coin(ctx):
    num = ra.randint(1, 2)
    coin = get_string(ctx, 'testa') if num == 1 else get_string(ctx, 'croce') 
    await ctx.channel.send(f"{get_string(ctx, 'uscito')}{coin}")

@bot.command(aliases=['grey', 'gray'])
async def grigio(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author
    file, filename = await opencv.grey(member)
    await ctx.channel.send(file=file)
    os.remove(filename)

@bot.command(aliases=['lines'])
async def linee(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author
    file, filename = await opencv.canny(member)
    await ctx.channel.send(file=file)
    os.remove(filename)

@bot.command()
async def buff(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author
    file, filename = await opencv.rock(member)
    await ctx.channel.send(file=file)
    os.remove(filename)

@bot.command(aliases=['pirate'])
async def pirata(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author
    file, filename = await opencv.pirate(member)
    await ctx.channel.send(file=file)
    os.remove(filename)


@bot.command(aliases=['inspire'])
async def ispira(ctx):
    # Ottenimento link immagine e spedizione via embed di discord
    html = get_html('https://inspirobot.me/api?generate=true')
    em = discord.Embed()
    em.set_image(url=html)
    await ctx.channel.send(get_string(ctx, 'motivante'), embed=em)

@bot.command(aliases=['mc'])
async def morracinese(ctx, *,scelta : str = ...):
    # Controllo di ogni scelta e vincita del bot
    if scelta.strip().lower() == 'carta':
        msg = 'Ho scelto forbici, ho vinto io'
    elif scelta.strip().lower() == 'forbici' or scelta.strip().lower() == 'forbice':
        msg = 'Ho scelto sasso, ho vinto io'
    elif scelta.strip().lower() == 'sasso':
        msg = 'Ho scelto carta, ho vinto io'
    elif scelta.strip().lower() == ...:
        msg = 'Siccome non hai messo niente ho vinto io'
    else:
        msg = 'Non ho riconosciuto una opzione valida, ho vinto io'
    await ctx.channel.send(msg)

# Comando per scaricare avatar
@bot.command()
async def avatar(ctx, member : discord.Member):
    em = discord.Embed(title=f'Avatar di {member.display_name}', description=f'''{get_string(ctx, 'scaricalo')} [64]({str(member.avatar).replace("?size=1024", "?size=64")})
     | [128]({str(member.avatar).replace("?size=1024", "?size=128")})
     | [256]({str(member.avatar).replace("?size=1024", "?size=256")})
     | [512]({str(member.avatar).replace("?size=1024", "?size=512")}) 
     | [1024]({str(member.avatar)}) 
     | [2048]({str(member.avatar).replace("?size=1024", "?size=2048")}) 
     | [4096]({str(member.avatar).replace("?size=1024", "?size=4096")})'''.replace('\n', ""))
    em.set_image(url=str(member.avatar))
    await ctx.channel.send(embed=em)

silenziati = []
[silenziati.append(int(x[0])) for x in use_database('SELECT * FROM silenziati', True)]

@bot.command()
async def mute(ctx, member : discord.Member):
    global silenziati
    if member.id in set(silenziati):
        await ctx.channel.send(f'{member.display_name} {get_string(ctx, "gia_silenziato")}')
        return
    await check_admin(ctx)
    # Inserimento persona dentro lista silenziati
    Thread(target=lambda:use_database(f"INSERT INTO silenziati VALUES ('{member.id}')", commit=True)).start()
    ROLE_NAME = 'Silenziato'
    guild = ctx.guild
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    if not role:
        perms = discord.Permissions(send_messages=False, speak=False)
        role = await guild.create_role(name=ROLE_NAME, permissions=perms)
    for channel in guild.channels:
        await channel.set_permissions(role, speak=False, send_messages=False)
    await member.add_roles(role)
    silenziati.append(member.id)
    await ctx.channel.send(f'{member.display_name} {get_string(ctx, "silenziato")}')
    await ctx.message.add_reaction('<:evilpepe:837050861586087977>')

@bot.command()
async def unmute(ctx, member : discord.Member):
    global silenziati
    if member.id not in set(silenziati):                                                    # Toglimento persona dentro lista silenziati
        await ctx.channel.send(f'{member.display_name} {get_string(ctx, "no_silenziato")}')
        return
    await check_admin(ctx)
    # Togli la persona dal database
    Thread(target=lambda:use_database(f"DELETE FROM silenziati WHERE user_id = '{member.id}'", commit=True)).start()
    ROLE_NAME = 'Silenziato'
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)                               # Ottenimento ruolo
    del silenziati[silenziati.index(member.id)]
    if role:
        # Rimozione ruolo
        await member.remove_roles(role)
        if len(silenziati) == 0:
            await role.delete()
    await ctx.channel.send(f'{member.display_name} {get_string(ctx, "ricordato_parlare")}')
    await ctx.message.add_reaction('<:feelsgrugman:837051421102047242>')

@bot.command(aliases=['burn'])
async def brucia(ctx, member : discord.Member = None):
    if not member:
        member = ctx.author
    file, filename = await opencv.burn(member)
    await ctx.channel.send(file=file)
    os.remove(filename)

@bot.command(aliases=['scegli'])
async def choose(ctx, *, scelte : str = None):
    lista_scelte = scelte.split(',') if scelte != None else []
    if len(lista_scelte) <= 1 or all(x.strip() == lista_scelte[0] for x in lista_scelte):       # se le scelte sono <= 1 allora non si ha vera scelta
        await ctx.channel.send(f'{get_string(ctx, "no_scelta")} <:pepesad:806184708655808543>')
        return
    num = ra.randint(0, len(lista_scelte) - 1)
    await ctx.channel.send(lista_scelte[num])


@bot.command(aliases=['impersonate'])
async def impersona(ctx, member, *, message):
    await ctx.message.delete()
    try:
        member = await commands.MemberConverter().convert(ctx, member)   # Se esiste un membro convertilo
        nome = member.display_name                  # altrimenti usa come nome la stringa
        avatar = member.avatar                      # e come avatar il default
    except:
        nome = member
        avatar = None
    await send_webhook(ctx, message, nome, avatar)

# Comando per cambiare le lingue
@bot.command()
async def lang(ctx : discord.Message, language : str):
    # Controllo lingua selezionata e inserimento nel database dopo cancellamento
    # con un thread per mandare il messaggio prima
    if language == 'it':
        Thread(target=lambda:[
            use_database(f"DELETE FROM lang WHERE ch_id = {ctx.guild.id}", commit=True),
            use_database(f"INSERT INTO lang VALUES({ctx.guild.id}, 'it')", commit=True),
            reload_lang()]
            ).start()
        await ctx.channel.send('Lingua messa in italiano!')
    elif language == 'en':
        Thread(target=lambda:[
            use_database(f"DELETE FROM lang WHERE ch_id = {ctx.guild.id}", commit=True),
            use_database(f"INSERT INTO lang VALUES({ctx.guild.id}, 'en')", commit=True),
            reload_lang()]
            ).start()
        await ctx.channel.send('Language set to english!')
    elif language == 'OwO':
        Thread(target=lambda:[
            use_database(f"DELETE FROM lang WHERE ch_id = {ctx.guild.id}", commit=True),
            use_database(f"INSERT INTO lang VALUES({ctx.guild.id}, 'OwO')", commit=True),
            reload_lang()]
            ).start()
        await ctx.channel.send('Language set to OwO!')
    else:
        await ctx.channel.send(get_string(ctx, 'no_ling'))

@bot.command(aliases=['vm', 'sm', 'show_muted'])
async def visualizza_mutati(ctx):
    await check_admin(ctx)
    msg = ''
    if not set(silenziati):
        msg = get_string(ctx, 'ness_silenziato')
    else:
        converter = commands.MemberConverter()
        for user in set(silenziati):
            member = await converter.convert(ctx, f'<@!{user}>')
            msg += f'> {member.display_name}\n'
    await ctx.channel.send(msg)

#region Musica

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send(get_string(ctx, 'no_can_voc'))
    canale = ctx.author.voice.channel
    if ctx.voice_client is None:
        await canale.connect()
    elif ctx.voice_client:
        return
    else:
        await ctx.voice_client_move_to(canale)

@bot.command()
async def disconnect(ctx):
    for x in bot.voice_clients:
        if x.guild == ctx.guild:        
            await x.disconnect()


coda_canzoni = queue.Queue()
_skip = False
song_disconnect_timer = Timer(60)   # Time before the bot disconnects
async def play_loop(ctx, loop):
    song_disconnect_timer.call_at_end(lambda: loop.create_task(disconnect(ctx)) if coda_canzoni.empty() else None)
    song_disconnect_timer.stop()
    
    global _skip
    while not coda_canzoni.empty():
        if song_disconnect_timer.running:
            song_disconnect_timer.stop()
        if ctx.voice_client.is_playing() and not ctx.voice_client.is_paused() and not _skip:
            time.sleep(1)
        else:
            _skip = False
            await play_func(ctx, coda_canzoni.get(), loop)
            
    while ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        time.sleep(1)
    
    Thread(target=song_disconnect_timer.start).start()
    
async def play_func(ctx, url, loop : asyncio.AbstractEventLoop):
    # Opzione di FFMPEG
    FFMPEG_OPTIONS = {'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}
    # Opzione youtube_dl
    YDL_OPTIONS = {'format': 'bestaudio'}
    vc = ctx.voice_client
    vc.stop()
    
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        # Nota: la variabile url2 deve essere formats[indice audio, quindi asr] 
        
        if re.fullmatch(url_pattern, url):
            # Se e' un link allora lo fa partire cosi'
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][6]['url']
            title = info['title']
        else:
            # Altrimenti cerca su youtube la canzone
            info = ydl.extract_info(f'ytsearch:{url}', download=False)
            url2 = info['entries'][0]['formats'][6]['url']
            title = info['entries'][0]['title']
        
        # Source e' il link dell'audio estratto
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)
        
        loop.create_task(ctx.send(get_string(ctx, 'now_playing') + title))


@bot.command()
async def play(ctx, *, url):
    # Si unisce al canale
    await join(ctx)
    await ctx.send(get_string(ctx, 'now_enqueued'))
    loop = asyncio.get_event_loop()
    if coda_canzoni.empty():
        coda_canzoni.put(url)
        Thread(target=lambda: asyncio.run(play_loop(ctx, loop))).start()
    else:
        coda_canzoni.put(url)
@bot.command()
async def pause(ctx):
    # Mette in pausa la riproduzione di una canzone
    ctx.voice_client.pause()
    await ctx.send(get_string(ctx, 'pausa'))

@bot.command()
async def resume(ctx):
    # Ricomincia a riprodurrre l'audio dopo un pause
    ctx.voice_client.resume()
    await ctx.send(get_string(ctx, 'riprendi'))

@bot.command()
async def stop(ctx):
    # Smette di riprodurre l'audio
    ctx.voice_client.stop()
    
@bot.command()
async def skip(ctx):
    global _skip
    if coda_canzoni.empty():
        await stop(ctx)
    else:
        _skip = True

@bot.command()
async def clear(ctx):
    while not coda_canzoni.empty():
        coda_canzoni.get()
    await stop(ctx)
#endregion


#endregion

#region Sezione intercettazione messaggi

@bot.event
async def on_message(message: discord.Message):
    # Controlla se il messaggio e' stato inviato dal bot
    if message.author == bot.user or message.webhook_id:
        return
    
    # Per quelli silenziati
    if message.author.id in set(silenziati) and str(message.author.id) != creator_id:
        await message.delete()
        return

    msg = message.content.replace(' ', '').lower()
    messaggio = switch_messaggi(msg)
    # Se messaggio ritorna un valore
    if messaggio != 404:
        # Se e' una lista manda tutte le cose nella lista
        if isinstance(messaggio, list):
            for m in messaggio:
                # Se e' un URL manda un immagine
                if re.match(url_pattern, m) and not re.match(youtube_url, m):
                    e = discord.Embed()
                    e.set_image(url=m)
                    await message.channel.send(embed=e)
                else:
                    await message.channel.send(m)
        # Se contiene func allora esegui la funzione e scrivi il messaggio msgg
        elif messaggio[0] == 'func':
            loc = {}
            exec(messaggio[1], globals(), loc)
            if loc['msgg'].__contains__('NON SI BESTEMMIA') or loc['msgg'].__contains__('IL MIO ACERRIMO NEMICO') and message.channel.guild.id == 829765996771803157:
                return
            await message.channel.send(loc['msgg'])
        # Se contiene embed allora manda un embed del messaggio dopo aver eseguito il codice
        elif messaggio[0] == 'embed':
            loc = {}
            exec(messaggio[1], globals(), loc)
            await message.channel.send(embed=loc['msgg'])
        # Se e' una emoji allora sostituisci e manda
        elif re.match(emoji_patterns, messaggio):
            author = message.author
            try:
                await message.delete()
            except:
                pass
            await send_webhook(message, messaggio, author.display_name, author.avatar)
        # Altrimenti manda il messaggio e basta
        else:
            await message.channel.send(messaggio)
        
    await bot.process_commands(message) # Vai alla parte comandi dopo aver controllato

#endregion

#region Error handler

@somma.error
@dividi.error
@moltiplica.error
@clean.error
@lang.error
async def somma_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Hai messo tutti i parametri? :thinking:")

@warn.error
@mostra_infrazioni.error
@pulisci_fedina.error
@insulta.error
@kick.error
@gaymeter.error
@furrymeter.error
@grigio.error
@linee.error
@buff.error
@avatar.error
@pirata.error
@brucia.error
@mute.error
@unmute.error
async def membro_non_trovato(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Persona non trovata! Ma sei ' + genera_insulto() + '?')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Devi indicare una pesona su cui eseguire questo comando ' + genera_insulto() + '!')
    else:
        print(error)

@cancella_insulto_dalla_lista.error
async def cosa_non_trovata(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('L\' id deve essere un numero ' + genera_insulto().lower() + '!')

#endregion

#region help
from bonus import Help, Tris
asyncio.run(bot.add_cog(Help(bot, risposte_dic)))
asyncio.run(bot.add_cog(Tris(bot)))

#endregion

bot.run(TOKEN)
