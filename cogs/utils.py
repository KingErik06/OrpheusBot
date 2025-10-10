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

async def setup(bot):
    await bot.add_cog(Utils(bot))