#Importações:
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("⚖️; Cog de Moderação Carregado!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def limpar(self, ctx, amount: int = 5):
        if amount > 100:
            await ctx.send("❌; Não posso limpar mais de 100 mensagens!")
            return
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹; {len(deleted) - 1} mensagens limpas!", delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def aviso(self, ctx, member: discord.Member, *, reason="Não especificado!"):
        #Dá um aviso ao usuário
        await ctx.send(f"⚠️; {member.mention} foi avisado. Motivo: {reason}.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))