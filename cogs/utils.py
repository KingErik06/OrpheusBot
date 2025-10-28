import discord
from discord.ext import commands
import datetime

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("🔧; Cog utulitário carregado!")

    @commands.command()
    async def ping(self, ctx):
        #Mostra a latência do bot
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓; Pong! {latency}ms.")

    @commands.command()
    async def info(self, ctx):
        #Informações sobre o OrpheusBot
        embed = discord.Embed(title="🎵 OrpheusBot", description="Bot de música e moderação inspirado na mitologia grega.", color=0x00ff00, timestamp=datetime.datetime.now())
        embed.add_field(name="Servidores", value=len(self.bot.guilds))
        embed.add_field(name="Comandos", value=len(self.bot.commands))
        embed.add_field(name="Desenvolvedor", value="KingErik06")

        await ctx.send(embed=embed)

    @commands.command()
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="🎵 Comandos do OrpheusBot",
            description="Aqui estão todos os comandos disponíveis:",
            color=0x00ff00
        )
        embed.add_field(
            name="🎶 Música",
        value="`!tocar <música>` - Toca uma música\n"
              "`!pular` - Pula a música atual\n"
              "`!parar` - Para e limpa a fila\n"
              "`!volume <1-100>` - Ajusta volume\n"
              "`!queue` - Mostra a fila",
        inline=False
        )
        embed.add_field(
            name="🔁 Loop", 
        value="`!loop` - Loop da música atual\n"
              "`!looplista` - Loop da fila inteira\n"
              "`!unloop` - Desativa todos os loops",
        inline=False
        )
        embed.add_field(
            name="🔊 Voz",
        value="`!entrar` - Entra no seu canal\n"
              "`!sair` - Sai do canal",
        inline=False
        )

        embed.set_footer(text="Use !ajuda para ver essa mensagem novamente")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utils(bot))