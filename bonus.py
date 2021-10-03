from discord.ext import commands
import discord
import re
from timer.timer import Timer
from threading import Thread
import asyncio
from strings import get_string

numbers = r'[1-9]'
animated_emoji_pattern = r'^<a:[a-zA-Z0-9_-]+:[0-9]+>$'


class Help(commands.Cog):
    def __init__(self, bot, dizionario_emoji):
        self.bot = bot
        self.dic = dizionario_emoji
        
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title='Help', description=get_string(ctx, 'help'))
        em.add_field(name=get_string(ctx, 'creatore'), value='pulisci_fedina(pf), cancella_insulto_dalla_lista, visualizza_lista_insulti')
        em.add_field(name='Admin', value=get_string(ctx, 'v_admin'))
        em.add_field(name='Casual', value=get_string(ctx, 'v_casual'))
        em.add_field(name=get_string(ctx, 'music'), value='play, stop, pause, resume, join, disconnect')
        em.add_field(name=get_string(ctx, 'immagini'), value=get_string(ctx, 'v_immagini'))
        em.add_field(name=get_string(ctx, 'matematica'), value=get_string(ctx, 'v_matematica'))
        await ctx.send(embed = em)

    @help.command()
    async def warn(self, ctx):
        em = discord.Embed(title='Warn', description=get_string(ctx, 'warn_d'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_warn'))
        await ctx.send(embed=em)

    @help.command(aliases=['pf'])
    async def pulisci_fedina(self, ctx):
        em = discord.Embed(title='Pulisci Fedina', description='Pulisce la fedina penale di una persona', color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value='$pulisci_fedina <persona>')
        em.add_field(name='alias', value='$pf')
        await ctx.send(embed=em)

    @help.command(aliases=['mi', 'show_infractions'])
    async def mostra_infrazioni(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'mostr_infr'), description=get_string(ctx, 'd_mostr_infr'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_mostr_infr'))
        em.add_field(name='alias', value='$mi')
        await ctx.send(embed=em)

    @help.command(aliases=['i'])
    async def insulta(self, ctx):
        em = discord.Embed(title='Insulta', description='Insulta una persona', color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value='$insulta <persona>')
        em.add_field(name='alias', value='$i')
        await ctx.send(embed=em)

    @help.command()
    async def visualizza_lista_insulti(self, ctx):
        em = discord.Embed(title='Visualizza lista insulti', description='Visualizza la lista degli insulti', color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value='$visualizza_lista_insulti')
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['p', 'probability'])
    async def probabilita(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'prob'), description=get_string(ctx, 'd_prob'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_prob'))
        em.add_field(name='alias', value='$p')
        await ctx.send(embed=em)

    @help.command(aliases=['ai'])
    async def aggiungi_insulto(self, ctx):
        em = discord.Embed(title='Aggiungi Insulto', description='In caso hai un insulto simpatico da aggiungere al database', color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value='$aggiungi_insulto [insulto]')
        em.add_field(name='alias', value='$ai')
        await ctx.send(embed=em)

    @help.command()
    async def cancella_insulto_dalla_lista(self, ctx):
        em = discord.Embed(title='Cancella insulto dalla lista', description='Cancella un insulto dal database, comando lungo apposta per essere certi di quello che si fa', color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value='$cancella_insulto_dalla_lista [id]')
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def kick(self, ctx):
        em = discord.Embed(title='Kick', description=get_string(ctx, 'd_kick'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_kick'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def ban(self, ctx):
        em = discord.Embed(title='ban', description=get_string(ctx, 'd_ban'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_ban'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def clean(self, ctx):
        em = discord.Embed(title='clean', description=get_string(ctx, 'd_clean'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_clean'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['dice'])
    async def dado(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'dado_n'), description=get_string(ctx, 'd_dado'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_dado'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def tris(self, ctx):
        em = discord.Embed(title='tris', description=get_string(ctx, 'd_tris'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_tris'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['gm'])
    async def gaymeter(self, ctx):
        em = discord.Embed(title='gaymeter', description=get_string(ctx, 'd_gm'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_gm'))
        em.add_field(name='alias', value='gm')
        await ctx.send(embed=em)

    @help.command()
    async def furrymeter(self, ctx):
        em = discord.Embed(title='furrymeter', description=get_string(ctx, 'd_fm'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_fm'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def coin(self, ctx):
        em = discord.Embed(title='coin', description=get_string(ctx, 'd_coin'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value='$coin')
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['animated_emojis'])
    async def emoji_animate(self, ctx):
        emoji = []
        for k, v in self.dic.items():
            if isinstance(v, str) and re.match(animated_emoji_pattern, v):
                emoji.append(k)
        em = discord.Embed(title=get_string(ctx, 'em_an'), description=get_string(ctx, 'd_em_an'))
        em.add_field(name='Lista', value=emoji)
        await ctx.send(embed=em)

    @help.command(aliases=['gray', 'grey'])
    async def grigio(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'grigio'), description=get_string(ctx, 'd_grigio'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_grigio'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['lines'])
    async def linee(self, ctx):
        em = discord.Embed(title='linee', description=get_string(ctx, 'd_linee'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_linee'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def buff(self, ctx):
        em = discord.Embed(title='buff', description=get_string(ctx, 'd_buff'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_buff'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['pirate'])
    async def pirata(self, ctx):
        em = discord.Embed(title='pirata', description='Arrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr', color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_pirate'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['inspire'])
    async def ispira(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'ispira'), description=get_string(ctx, 'd_ispira'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_ispira'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)
   
    @help.command(aliases=['credits'])
    async def crediti(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'crediti'), description=get_string(ctx, 'd_credits'), color = ctx.message.author.color)
        await ctx.send(embed=em)
    
    @help.command(aliases=['mc'])
    async def morracinese(self, ctx):
        em = discord.Embed(title='morra cinese', description='Sfida il bot a morra cinese!', color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value='$morracinese [scelta]')
        em.add_field(name='alias', value='mc')
        await ctx.send(embed=em)

    @help.command()
    async def avatar(self, ctx):
        em = discord.Embed(title='avatar', description=get_string(ctx, 'd_avatar'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_avatar'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command(aliases=['burn'])
    async def brucia(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'brucia'), description=get_string(ctx, 'd_brucia'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_brucia'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def mute(self, ctx):
        em = discord.Embed(title='mute', description=get_string(ctx, 'd_mute'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_mute'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def unmute(self, ctx):
        em = discord.Embed(title='unmute', description=get_string(ctx, 'd_unmute'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_unmute'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)

    @help.command()
    async def choose(self, ctx):
        em = discord.Embed(title='choose', description=get_string(ctx, 'd_choose'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_choose'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)
    
    @help.command(aliases=['impersonate'])
    async def impersona(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'impersona'), description=get_string(ctx, 'd_impersona'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_impersona'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
        await ctx.send(embed=em)
    
    @help.command(aliases=['vm', 'sm', 'show_muted'])
    async def visualizza_mutati(self, ctx):
        em = discord.Embed(title=get_string(ctx, 'visualizza_mutati'), description=get_string(ctx, 'd_v_mutati'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_v_mutati'))
        em.add_field(name='alias', value='vm, sm')
        await ctx.send(embed=em)

    @help.command()
    async def join(self, ctx):
        em = discord.Embed(title='join', description=get_string(ctx, 'd_join'), color = ctx.message.author.color)
        em.add_field(name=get_string(ctx, 'sintassi'), value=get_string(ctx, 'v_v_mutati'))
        em.add_field(name='alias', value=get_string(ctx, 'nessuno'))
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
                await ctx.channel.send(get_string(ctx, 'pareggio'))
                self.end_game()
            elif check != False:
                winner = self.initializer if check == 'x' else self.guest
                await ctx.channel.send(get_string(ctx, 'vincitore_e') + winner.mention)
                self.end_game()

    @commands.command()
    async def tris(self, ctx, member : discord.Member):
        # Inizio
        react = ['✅', '❌']
        # Devo sistemarla in qualche modo xDDD
        if self.running == True:
            await ctx.channel.send(get_string(ctx, 'partita_in_corso'))
            return
        if ctx.author == member:
            await ctx.channel.send(get_string(ctx, 'solo'))
            return
        if member.bot:
            await ctx.channel.send(get_string(ctx, 'gioco_con_bot'))
            return
        msg = await ctx.channel.send(f"{member.mention} {get_string(ctx, 'sfida')}")
        self.running = True
        # Aggiungi reazioni ad un messaggio per fare la sfida
        for r in react:
            await msg.add_reaction(r)

        def check_react(reaction, user):
            # Controllo cosa mette l'utente
            if user != member or reaction.message.id != msg.id or not str(reaction.emoji) in react:
                return False
            return True
        try:
            res, user = await self.bot.wait_for('reaction_add', check=check_react, timeout=15)
        except asyncio.TimeoutError:
            await ctx.channel.send(f'{member.mention} {get_string(ctx, "timeout")}')
            self.running = False
            return

        # In caso accetta
        if react[0] in str(res.emoji):
            await ctx.channel.send(f'{member.mention} {get_string(ctx, "accept")}')
        # Se rifiuta
        elif react[1] in str(res.emoji):
            await ctx.channel.send(f'{member.mention} {get_string(ctx, "decline")}')
            self.running = False
            return

        # Numeri per far vedere come si gioca
        num_tris_board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        await ctx.channel.send('Iniziando sessione di tris...')
        if member == self.bot.user:
            await ctx.send.channel('Non puoi sfidare il bot!')
            return
        # Disegno tavola iniziale
        await self.DrawBoard(ctx, num_tris_board)
        await ctx.channel.send(get_string(ctx, 'reg_tris'))
        self.tris = True
        self.initializer = ctx.author
        self.guest = member
        loop = asyncio.get_event_loop()
        # Inizio timer della morte
        self.timeout_timer.call_at_end(lambda:(self.timeout(ctx, loop)))
        t = Thread(target=self.timeout_timer.start)
        t.start()
    
    def timeout(self, ctx, loop):
        loop.create_task(ctx.channel.send(get_string(ctx, 'timeout60')))
        self.end_game()

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # Controllo se persona ha i diritti di giocare
        if not self.tris or ctx.author == self.bot.user or (ctx.author != self.initializer and ctx.author != self.guest):
            return
        else:
            # Controllo se ha scritto un numero
            num = re.search(numbers, ctx.content)
            # Controllo di chi e' il turno
            if self.turn % 2 == 0 and ctx.author != self.initializer:
                await ctx.channel.send(get_string(ctx, 'turno_di') + self.initializer.mention + '!')
                return
            if self.turn % 2 == 1 and ctx.author != self.guest:
                await ctx.channel.send(get_string(ctx, 'turno_di') + self.guest.mention + '!')
                return
            if num == None:
                await ctx.channel.send(get_string(ctx, 'number_19'))
                return
            num = int(num.group()) - 1
            # Controllo se casella gia' occupata
            if self.tris_board[num] != ' ':
                await ctx.channel.send(get_string(ctx, 'occupato'))
                await self.DrawBoard(ctx, self.tris_board)
                return
            self.tris_board[num] = 'x' if self.turn % 2 == 0 else 'o'
            # Aumento turno
            self.turn += 1
            if self.lastBoard != None:
                await self.lastBoard.delete()
                await ctx.delete()
            # Disegno tavola
            await self.DrawBoard(ctx, self.tris_board)
            # Reset timer della morte
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
        # Reset allo stato iniziale
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
            await ctx.send(get_string(ctx, 'da_solo'))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(get_string(ctx, 'immaginary'))