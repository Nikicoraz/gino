#!venv/Scripts/python.exe
import discord
from discord import permissions
from discord import webhook
from discord.ext.commands.core import check
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
import opencv
from Network import get_html
from threading import Thread
from strings import get_string
from strings import reload_lang

#region init
insulti = []
langs = {}

url_pattern = r'(http|https)://.*'
youtube_url = r'(http|https)://(www.youtube.com|youtu.be)/.*'
animated_emoji_pattern = r'^<a:[a-zA-Z0-9_-]+:[0-9]+>$'

load_dotenv()
DATABASE_PASSWORD = os.environ.get('DB_PASS')
bot = commands.Bot(command_prefix='$')
TOKEN = os.environ.get('TOKEN')
creator_id = os.environ.get("CREATORE")
bot.remove_command('help')



#endregion

# region Funzioni



def use_database(command, fetch=False, commit=False):
    _ = None
    conn = mysql.connector.connect(
    host='freedb.tech',
    user='freedbtech_Nikicoraz',
    password=DATABASE_PASSWORD,
    database='freedbtech_generale')
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
    
def genera_insulto():
    return insulti[ra.randint(0, len(insulti) - 1)]

risposte_dic = {
    'hellothere': 'General Kenobi!',
    'gigi': ('func','msgg = "IL MIO ACERRIMO NEMICO"'),
    'nigga': 'Un po\' razzista ma ok',
    'negro': 'Un po\' razzista ma ok',
    'pepsiman': ['Pepsi Man!🍾', 'https://www.player.it/wp-content/uploads/2018/12/Pepsiman-il-videogioco.jpg', 'https://youtu.be/z54MpfR3XE4'],
    'grazie':'Prego',
    'uwu': 'OwO',
    'owo':'UwU',
    ':pepesad:':'F',
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
    '🔫': '<:pistola:821669164107825174>'
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
async def test(ctx : discord.Message):
    pass

@bot.command(aliases=['p', 'probability'])
async def probabilita(ctx, *, arg):
    import random
    await ctx.send(arg + get_string(ctx, 'probabilita') + str(random.randint(0, 100)) + '%')

@bot.command(aliases=['i'])
async def insulta(ctx, *, member: discord.Member):
    await ctx.send(f'{member.mention} è un {genera_insulto().lower()}\n\n> -Messaggio cordialmente inviato da *{get_name(ctx)}*')

@bot.command()
async def warn(ctx, member: discord.Member, *, reason='no reason'):
    await check_admin(ctx)
    m = await ctx.send(f'{member.mention}' + get_string(ctx, 'warn') + f'{reason}')
    await ctx.message.add_reaction('<:pepefedora:822422976796295198>')
    data = datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')
    reason = reason.replace("'", "")
    use_database(f"INSERT INTO fedina VALUES ({member.id}, '{reason}', '{data}')", commit=True)

@bot.command(aliases=['mi', 'show_infractions'])
async def mostra_infrazioni(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.author
    infrazioni = use_database(f'SELECT reason, date FROM fedina WHERE user_id = {member.id}', True)
    for i, infrazione in enumerate(infrazioni, 1):
        await ctx.send(f'> {get_string(ctx, "infrazione")} {i}: `{infrazione[0]}` {get_string(ctx, "in_data")} `{infrazione[1]}`')
    if len(infrazioni) == 0:
        await ctx.send(f"{member.mention} {get_string(ctx, 'mai_infra')}")

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
        if int(arg) > 5000:
            if ctx.message.author.id != int(creator_id):
                await ctx.channel.send(get_string(ctx, 'canc_errore'))
                return
    except:
        try:
            converter = commands.MemberConverter()
            member = await converter.convert(ctx, arg)
            await ctx.channel.purge(check=lambda ctx:check_member(ctx, member))
        except errors.MemberNotFound:
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

@bot.command(aliases=['gm'])
async def furrymeter(ctx, member : discord.Member):
    perc = ra.randint(0, 100)
    BARRA = '█'
    VUOTO = '░'
    if str(member.id) == creator_id:
        perc = 0
    quanti = int(perc/10)
    restanti = 10-quanti
    await ctx.channel.send(f'{member.mention} {get_string(ctx, "furry:")} {BARRA*quanti}{VUOTO*restanti} {perc}%:cat:\n')

@bot.command()
async def coin(ctx):
    num = ra.randint(1, 2)
    coin = get_string(ctx, 'testa') if num == 1 else get_string(ctx, 'croce') 
    await ctx.channel.send(f"{get_string(ctx, 'uscito')}{coin}")

@bot.command()
async def modify_role(ctx, member : discord.Member, role_input : discord.Role, add_remove : bool):
    await check_creator(ctx)
    if add_remove:
        await member.add_roles(role_input)
    else:
        await member.remove_roles(role_input)
    await ctx.message.delete()

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
    html = get_html('https://inspirobot.me/api?generate=true')
    em = discord.Embed()
    em.set_image(url=html)
    await ctx.channel.send(get_string(ctx, 'motivante'), embed=em)

@bot.command(aliases=['mc'])
async def morracinese(ctx, *,scelta : str = ...):
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

@bot.command()
async def avatar(ctx, member : discord.Member):
    em = discord.Embed(title=f'Avatar di {member.display_name}', description=f'''{get_string(ctx, 'scaricalo')} [64]({str(member.avatar_url).replace("?size=1024", "?size=64")})
     | [128]({str(member.avatar_url).replace("?size=1024", "?size=128")})
     | [256]({str(member.avatar_url).replace("?size=1024", "?size=256")})
     | [512]({str(member.avatar_url).replace("?size=1024", "?size=512")}) 
     | [1024]({str(member.avatar_url)}) 
     | [2048]({str(member.avatar_url).replace("?size=1024", "?size=2048")}) 
     | [4096]({str(member.avatar_url).replace("?size=1024", "?size=4096")})'''.replace('\n', ""))
    em.set_image(url=str(member.avatar_url))
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
    use_database(f"INSERT INTO silenziati VALUES ('{member.id}')", commit=True)
    await ctx.channel.send(f'{member.display_name} {get_string(ctx, "silenziato")}')

@bot.command()
async def unmute(ctx, member : discord.Member):
    global silenziati
    if member.id not in set(silenziati):
        await ctx.channel.send(f'{member.display_name} {get_string(ctx, "no_silenziato")}')
        return
    await check_admin(ctx)
    ROLE_NAME = 'Silenziato'
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    del silenziati[silenziati.index(member.id)]
    use_database(f"DELETE FROM silenziati WHERE user_id = '{member.id}'", commit=True)
    if role:
        await member.remove_roles(role)
        if len(silenziati) == 0:
            await role.delete()
    await ctx.channel.send(f'{member.display_name} {get_string(ctx, "ricordato_parlare")}')

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
    if len(lista_scelte) <= 1 or all(x.strip() == lista_scelte[0] for x in lista_scelte):
        await ctx.channel.send(f'{get_string(ctx, "no_scelta")} <:pepesad:806184708655808543>')
        return
    num = ra.randint(0, len(lista_scelte) - 1)
    await ctx.channel.send(lista_scelte[num])

@bot.command(aliases=['impersonate'])
async def impersona(ctx, member: discord.Member, *, message):
    await ctx.message.delete()
    webhook = await ctx.channel.create_webhook(name='IDKWNTPH')
    await webhook.send(content=message, username=member.display_name, avatar_url=member.avatar_url)
    await webhook.delete()

@bot.command()
async def lang(ctx : discord.Message, language : str):
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
    else:
        await ctx.channel.send(get_string(ctx, 'no_ling'))
    

#endregion

#region Sezione intercettazione messaggi

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user or message.webhook_id:
        return
    
    # Per quelli silenziati
    if message.author.id in set(silenziati) and str(message.author.id) != creator_id:
        await message.delete()
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
        elif messaggio[0] == 'func':
            loc = {}
            exec(messaggio[1], globals(), loc)
            if loc['msgg'].__contains__('NON SI BESTEMMIA') or loc['msgg'].__contains__('IL MIO ACERRIMO NEMICO') and message.channel.guild.id == 829765996771803157:
                return
            await message.channel.send(loc['msgg'])
        elif messaggio[0] == 'embed':
            loc = {}
            exec(messaggio[1], globals(), loc)
            await message.channel.send(embed=loc['msgg'])
        elif re.match(animated_emoji_pattern, messaggio):
            author = message.author
            await message.delete()
            webhook = await message.channel.create_webhook(name='IDKWNTPH')
            await webhook.send(content=messaggio, username=author.display_name, avatar_url=author.avatar_url)
            await webhook.delete()
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
bot.add_cog(Help(bot, risposte_dic))
bot.add_cog(Tris(bot))

#endregion

bot.run(TOKEN)
