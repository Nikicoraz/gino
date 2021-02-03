from discord.ext import commands
import discord
import re

from discord.ext.commands.core import check

numbers = r'[1-9]'

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title='Help', description='ciao, usa $help <comando> per avere piu\' informazioni!')
        em.add_field(name='Creatore', value='pulisci_fedina(pf), cancella_insulto_dalla_lista, visualizza_lista_insulti')
        em.add_field(name='Admin', value='warn, kick, ban, clean')
        em.add_field(name='Casual', value='aggiungi_insulto(ai), mostra_infrazioni(mi), insulta(i), probabilita(p), dado')
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

class Tris(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tris = False
        self.tris_board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.turn = 0
        self.initializer = None
        self.guest = None
        #TODO votazione e timer
    
    async def DrawBoard(self, ctx, tris_board):
            await ctx.channel.send("""`+---+---+---+
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
        if ctx.author == member:
            await ctx.channel.send('Non pensavo fossi così triste')
            return
        if member.bot:
            await ctx.channel.send('Vuoi giocare con un bot? :thinking:')
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
            await self.DrawBoard(ctx, self.tris_board)
    
    
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
    
    @tris.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Vuoi giocare da solo? :thinking:")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Non conosco il tuo amico immaginario :neutral_face:")