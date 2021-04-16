from discord.ext import commands
import discord
import re
from timer.timer import Timer
from threading import Thread
import asyncio

from discord.ext.commands.core import check

numbers = r'[1-9]'
animated_emoji_pattern = r'^<a:[a-zA-Z0-9_-]+:[0-9]+>$'

class Help(commands.Cog):
    def __init__(self, bot, dizionario_emoji):
        self.bot = bot
        self.dic = dizionario_emoji
        
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title='Help', description='ciao, usa $help <comando> per avere piu\' informazioni!')
        em.add_field(name='Creatore', value='pulisci_fedina(pf), cancella_insulto_dalla_lista, visualizza_lista_insulti')
        em.add_field(name='Admin', value='warn, kick, ban, clean, mute, unmute')
        em.add_field(name='Casual', value='''aggiungi_insulto(ai), mostra_infrazioni(mi), insulta(i),
         probabilita(p), dado, tris, coin, gaymeter(gm), emoji_animate, ispira,
         crediti, morracinese(mc), choose, impersona''')
        em.add_field(name='Immagini', value='avatar, grigio, linee, buff, pirata, brucia')
        em.add_field(name='Matematica', value='somma, dividi, moltiplica')
        await ctx.send(embed = em)

    @help.command()
    async def warn(self, ctx):
        em = discord.Embed(title='Warn', description='Aggiunge una infrazione sulla fedina di una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$warn <persona> [ragione]')
        await ctx.send(embed=em)

    @help.command(aliases=['pf'])
    async def pulisci_fedina(self, ctx):
        em = discord.Embed(title='Pulisci Fedina', description='Pulisce la fedina penale di una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$pulisci_fedina <persona>')
        em.add_field(name='alias', value='$pf')
        await ctx.send(embed=em)

    @help.command(aliases=['mi'])
    async def mostra_infrazioni(self, ctx):
        em = discord.Embed(title='Mostra Infrazioni', description='Mostra le infrazioni penali di una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$mostra_infrazioni <persona>')
        em.add_field(name='alias', value='$mi')
        await ctx.send(embed=em)

    @help.command(aliases=['i'])
    async def insulta(self, ctx):
        em = discord.Embed(title='Insulta', description='Insulta una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$insulta <persona>')
        em.add_field(name='alias', value='$i')
        await ctx.send(embed=em)

    @help.command()
    async def visualizza_lista_insulti(self, ctx):
        em = discord.Embed(title='Visualizza lista insulti', description='Visualizza la lista degli insulti', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$visualizza_lista_insulti')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command(aliases=['p'])
    async def probabilita(self, ctx):
        em = discord.Embed(title='Probabilita', description='Probabilità che succeda una cosa', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$probabilita [cosa che deve accadere]')
        em.add_field(name='alias', value='$p')
        await ctx.send(embed=em)

    @help.command(aliases=['ai'])
    async def aggiungi_insulto(self, ctx):
        em = discord.Embed(title='Aggiungi Insulto', description='In caso hai un insulto simpatico da aggiungere al database', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$aggiungi_insulto [insulto]')
        em.add_field(name='alias', value='$ai')
        await ctx.send(embed=em)

    @help.command()
    async def cancella_insulto_dalla_lista(self, ctx):
        em = discord.Embed(title='Cancella insulto dalla lista', description='Cancella un insulto dal database, comando lungo apposta per essere certi di quello che si fa', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$cancella_insulto_dalla_lista [id]')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def kick(self, ctx):
        em = discord.Embed(title='Kick', description='Caccia una persona dal server', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$kick <persona> [motivo]')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def ban(self, ctx):
        em = discord.Embed(title='ban', description='Banna una persona dal server', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$ban <persona> [motivo]')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def clean(self, ctx):
        em = discord.Embed(title='clean', description='Pulisce la chat', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$clean {persona o numero di messaggi}')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def dado(self, ctx):
        em = discord.Embed(title='dado', description='Lancia un dado e sceglie un numero tra 1 e 6', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$dado')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def tris(self, ctx):
        em = discord.Embed(title='tris', description='Comincia una partita a tris', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$tris <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command(aliases=['gm'])
    async def gaymeter(self, ctx):
        em = discord.Embed(title='gaymeter', description='Indica quanto è gay una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$gaymeter <persona>')
        em.add_field(name='alias', value='gm')
        await ctx.send(embed=em)

    @help.command()
    async def coin(self, ctx):
        em = discord.Embed(title='coin', description='Lancia una monetina', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$coin')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def emoji_animate(self, ctx):
        emoji = []
        for k, v in self.dic.items():
            if isinstance(v, str) and re.match(animated_emoji_pattern, v):
                emoji.append(k)
        em = discord.Embed(title='Emoji Animate', description='Lista della emoji animate')
        em.add_field(name='Lista', value=emoji)
        await ctx.send(embed=em)

    @help.command()
    async def grigio(self, ctx):
        em = discord.Embed(title='grigio', description='Visualizza una immagine profilo in una scala di grigi', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$grigio <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def linee(self, ctx):
        em = discord.Embed(title='linee', description='Visualizza le linee di una immagine profilo', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$linee <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def buff(self, ctx):
        em = discord.Embed(title='buff', description='Fatti diventare un figo muscoloso', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$buff <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def pirata(self, ctx):
        em = discord.Embed(title='pirata', description='Arrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$pirata <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def ispira(self, ctx):
        em = discord.Embed(title='ispira', description='Manda una immagine motivante dal sito https://inspirobot.me', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$ispira')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)
   
    @help.command()
    async def crediti(self, ctx):
        em = discord.Embed(title='Crediti', description='Creato da Nikicoraz\n[Github](https://github.com/Nikicoraz/gino)', color = ctx.message.author.color)
        await ctx.send(embed=em)
    
    @help.command(aliases=['mc'])
    async def morracinese(self, ctx):
        em = discord.Embed(title='morra cinese', description='Sfida il bot a morra cinese!', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$morracinese [scelta]')
        em.add_field(name='alias', value='mc')
        await ctx.send(embed=em)

    @help.command()
    async def avatar(self, ctx):
        em = discord.Embed(title='avatar', description='Scarica l\'avatar di una persona nel server!', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$avatar')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def brucia(self, ctx):
        em = discord.Embed(title='brucia', description='Brucia una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$brucia <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def mute(self, ctx):
        em = discord.Embed(title='mute', description='Togli il diritto di parola ad una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$mute <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def unmute(self, ctx):
        em = discord.Embed(title='unmute', description='Ridai tristemente il diritto di parola ad una persona', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$unmute <persona>')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)

    @help.command()
    async def choose(self, ctx):
        em = discord.Embed(title='choose', description='Scegli tra alcune opzioni', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$choose [opzioni separate da ","]')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)
    
    @help.command()
    async def impersona(self, ctx):
        em = discord.Embed(title='impersona', description='Fai finta di essere qualcun altro', color = ctx.message.author.color)
        em.add_field(name='**Sintassi**', value='$impersona <persona> [messaggio]')
        em.add_field(name='alias', value='Nessuno')
        await ctx.send(embed=em)
    
    
    


class Tris(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tris = False
        self.tris_board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.turn = 0
        self.initializer = None
        self.guest = None
        self.running = False
        self.timeout_timer = Timer(60)
        self.lastBoard = None
    
    async def DrawBoard(self, ctx, tris_board):
            self.lastBoard = await ctx.channel.send("""`+---+---+---+
| %c | %c | %c |
+---+---+---+
| %c | %c | %c |
+---+---+---+
| %c | %c | %c |
+---+---+---+`""" % (tris_board[0], tris_board[1], tris_board[2], tris_board[3], tris_board[4], tris_board[5], tris_board[6], tris_board[7], tris_board[8]))
            check = self.check_board()
            if check == 404:
                await ctx.channel.send('Pareggio!')
                self.end_game()
            elif check != False:
                winner = self.initializer if check == 'x' else self.guest
                await ctx.channel.send("Il vincitore è " + winner.mention)
                self.end_game()

    @commands.command()
    async def tris(self, ctx, member : discord.Member):
        react = ['✅', '❌']
        if self.running == True:
            await ctx.channel.send('Una partita è già in corso!')
            return
        if ctx.author == member:
            await ctx.channel.send('Non pensavo fossi così triste')
            return
        if member.bot:
            await ctx.channel.send('Vuoi giocare con un bot? :thinking:')
            return
        msg = await ctx.channel.send(f"{member.mention} accetti la sfida?")
        self.running = True
        for r in react:
            await msg.add_reaction(r)
        def check_react(reaction, user):
            if user != member or reaction.message.id != msg.id or not str(reaction.emoji) in react:
                return False
            return True
        try:
            res, user = await self.bot.wait_for('reaction_add', check=check_react, timeout=15)
        except asyncio.TimeoutError:
            await ctx.channel.send(f'{member.mention} non ha risposto in tempo')
            self.running = False
            return

        if react[0] in str(res.emoji):
            await ctx.channel.send(f'{member.mention} ha accettato la sfida!')
        elif react[1] in str(res.emoji):
            await ctx.channel.send(f'{member.mention} è un codardo e ha rifiutato la sfida!')
            self.running = False
            return

        num_tris_board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        await ctx.channel.send('Iniziando sessione di tris...')
        if member == self.bot.user:
            await ctx.send.channel('Non puoi sfidare il bot!')
            return
        await self.DrawBoard(ctx, num_tris_board)
        await ctx.channel.send('Inserisci un numero da 1 a 9 per posizionare')
        self.tris = True
        self.initializer = ctx.author
        self.guest = member
        loop = asyncio.get_event_loop()
        self.timeout_timer.call_at_end(lambda:(self.timeout(ctx, loop)))
        t = Thread(target=self.timeout_timer.start)
        t.start()
    
    def timeout(self, ctx, loop):
        loop.create_task(ctx.channel.send('Nessuna risposta da 60 secondi, mi ignorate :cry:? Addio'))
        self.end_game()

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not self.tris or ctx.author == self.bot.user or (ctx.author != self.initializer and ctx.author != self.guest):
            return
        else:
            num = re.search(numbers, ctx.content)
            if self.turn % 2 == 0 and ctx.author != self.initializer:
                await ctx.channel.send("Attualmente è il turno di " + self.initializer.mention + '!')
                return
            if self.turn % 2 == 1 and ctx.author != self.guest:
                await ctx.channel.send("Attualmente è il turno di " + self.guest.mention + '!')
                return
            if num == None:
                await ctx.channel.send('Inserisci un numero tra 1 e 9!')
                return
            num = int(num.group()) - 1
            if self.tris_board[num] != ' ':
                await ctx.channel.send("Casella già occupata!")
                await self.DrawBoard(ctx, self.tris_board)
                return
            self.tris_board[num] = 'x' if self.turn % 2 == 0 else 'o'
            self.turn += 1
            if self.lastBoard != None:
                await self.lastBoard.delete()
                await ctx.delete()
            await self.DrawBoard(ctx, self.tris_board)
            self.timeout_timer.reset()
    
    def check_board(self):
        # Orizzontale
        if self.tris_board[0] == self.tris_board[1] and self.tris_board[0] == self.tris_board[2] and self.tris_board[0] != ' ':
            return self.tris_board[0]
        if self.tris_board[3] == self.tris_board[4] and self.tris_board[3] == self.tris_board[5] and self.tris_board[3] != ' ':
            return self.tris_board[3]
        if self.tris_board[6] == self.tris_board[7] and self.tris_board[6] == self.tris_board[8] and self.tris_board[6] != ' ':
            return self.tris_board[6]
        #Verticale
        if self.tris_board[0] == self.tris_board[3] and self.tris_board[0] == self.tris_board[6] and self.tris_board[0] != ' ':
            return self.tris_board[0]
        if self.tris_board[1] == self.tris_board[4] and self.tris_board[1] == self.tris_board[7] and self.tris_board[1] != ' ':
            return self.tris_board[1]
        if self.tris_board[2] == self.tris_board[5] and self.tris_board[2] == self.tris_board[8] and self.tris_board[2] != ' ':
            return self.tris_board[2]
        #Obliquo
        if self.tris_board[0] == self.tris_board[4] and self.tris_board[0] == self.tris_board[8] and self.tris_board[0] != ' ':
            return self.tris_board[0]
        if self.tris_board[2] == self.tris_board[4] and self.tris_board[2] == self.tris_board[6] and self.tris_board[2] != ' ':
            return self.tris_board[2]
        # Tutte piene 
        if not ' ' in self.tris_board:
            return 404
        return False

    def end_game(self):
        self.tris = False
        self.initializer = None
        self.guest = None
        self.tris_board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.turn = 0
        self.timeout_timer.stop()
        self.running = False
    
    @tris.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Vuoi giocare da solo? :thinking:")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Non conosco il tuo amico immaginario :neutral_face:")