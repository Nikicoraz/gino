from discord.ext import commands
import discord

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