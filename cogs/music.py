#Importações:
import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Cog de música carregado.")

    
    @commands.command()
    async def tocar(self, ctx, *, query):
        #Toca uma música do YouTube
        await ctx.send("🎵; Buscando: **{query}**")

    @commands.command()
    async def pular(self, ctx):
        #Pula a música do YouTube
        await ctx.send("🎵; Música Pulada.")

    @commands.command()
    async def fila(self, ctx):
        #Adiciona músicas a fila
        await ctx.send("🎵; Fila de músicas: (em desenvolvimento)")


async def setup(bot):
    await bot.add_cog(Music(bot))