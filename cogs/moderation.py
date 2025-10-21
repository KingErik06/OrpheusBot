#Importações:
import discord
import datetime
import json
import os
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings_file = "warnings.json"
        self.load_warnings()
        print("⚖️; Cog de Moderação Carregado!")

    def load_warnings(self):
        if os.path.exists(self.warnings_file):
            with open(self.warnings_file, 'r', encoding='utf-8') as f:
                self.warnings = json.load(f)
        else:
            self.warnings = {}

    def save_warnings(self):
        with open(self.warnings_file, 'w', encoding='utf-8') as f:
            json.dump(self.warnings, f, indent=4, ensure_ascii=False)

    async def get_mute_role(self, guild):
    #Procura por cargo de mute existente
        for role in guild.roles:
            if role.name.lower() in ["mutado", "muted", "silenciado"]:
                return role
        
        #Se não existe, cria um novo
        try:
            mute_role = await guild.create_role(
                name="Mutado",
                color=discord.Color.dark_gray(),
                reason="Cargo para sistema de mute automático"
            )
            
            #Configura permissões em todos os canais
            for channel in guild.channels:
                if isinstance(channel, (discord.TextChannel, discord.Thread)):
                    await channel.set_permissions(
                        mute_role, 
                        send_messages=False,
                        add_reactions=False,
                        create_public_threads=False,
                        create_private_threads=False,
                        send_messages_in_threads=False
                    )
                elif isinstance(channel, discord.VoiceChannel):
                    await channel.set_permissions(
                        mute_role,
                        speak=False,
                        stream=False
                    )
            
            #Move o cargo para uma posição adequada 
            try:
                positions = {}
                for role in guild.roles:
                    if role.name == "@everyone":
                        positions[role] = 0
                    elif role == mute_role:
                        positions[role] = 1
                    else:
                        positions[role] = role.position
                await guild.edit_role_positions(positions)
            except:
                pass  
            return mute_role
            
        except discord.Forbidden:
            return None  
        except discord.HTTPException:
            return None 

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
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in self.warnings:
            self.warnings[guild_id] = {}

        if user_id not in self.warnings[guild_id]:
            self.warnings[guild_id][user_id] = []

        current_warnings = len(self.warnings[guild_id][user_id])

        new_warning = {
            "id": current_warnings + 1,
            "moderador": str(ctx.author.id), 
            "motivo": reason, 
            "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
        self.warnings[guild_id][user_id].append(new_warning)
        current_warnings += 1
        self.save_warnings()
        
        punishment_applied = None
    
        if current_warnings >= 5:  #BAN AUTOMÁTICO
            try:
                await member.ban(reason=f"Ban automático - {current_warnings} avisos acumulados")
                punishment_applied = "🔨 **BANIMENTO AUTOMÁTICO**"
            except discord.Forbidden:
                punishment_applied = "❌ Não foi possível aplicar ban (sem permissões)"
                
        elif current_warnings >= 3:  #MUTE AUTOMÁTICO
            try:
                mute_role = await self.get_mute_role(ctx.guild)
                await member.add_roles(mute_role, reason=f"Mute automático - {current_warnings} avisos")
                punishment_applied = "🔇 **MUTE AUTOMÁTICO**"
            except discord.Forbidden:
                punishment_applied = "❌ Não foi possível aplicar mute (sem permissões)"
        
        embed = discord.Embed(
            title="⚠️ Aviso Aplicado",
            color=0xFFA500,
            timestamp=datetime.datetime.now()
        )
        
        #Informações básicas
        embed.add_field(name="👤 Usuário", value=f"{member.mention} (`{member.id}`)", inline=False)
        embed.add_field(name="🛡️ Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Motivo", value=reason, inline=False)
        
        #Sistema progressivo
        embed.add_field(
            name="📊 Status de Avisos", 
            value=f"**Total atual:** {current_warnings} aviso(s)", 
            inline=True
        )
        
        #Informação da punição aplicada
        if punishment_applied:
            embed.add_field(
                name="🚨 Punição Aplicada", 
                value=punishment_applied, 
                inline=False
            )
            #Muda a cor para vermelho se houve punição
            embed.color = 0xFF0000
        else:
            #Calcular avisos restantes
            if current_warnings < 3:
                warnings_until_mute = 3 - current_warnings
                embed.add_field(
                    name="🔇 Próxima punição", 
                    value=f"Mute em **{warnings_until_mute}** aviso(s)", 
                    inline=True
                )
            elif current_warnings < 5:
                warnings_until_ban = 5 - current_warnings
                embed.add_field(
                    name="🔨 Próxima punição", 
                    value=f"Ban em **{warnings_until_ban}** aviso(s)", 
                    inline=True
                )
        
        embed.set_footer(text="Sistema de moderação Orpheus Bot")
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def avisos(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author
        
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        #Verificar se existem avisos
        if (guild_id not in self.warnings or 
            user_id not in self.warnings[guild_id] or 
            not self.warnings[guild_id][user_id]):
            
            embed = discord.Embed(
                title="📭 Sem Avisos",
                description=f"{member.mention} não possui avisos registrados.",
                color=0x00FF00
            )
            await ctx.send(embed=embed)
            return
        
        warnings = self.warnings[guild_id][user_id]
        
        #Criar embed
        embed = discord.Embed(
            title=f"📋 Avisos de {member.display_name}",
            description=f"Total de **{len(warnings)}** aviso(s)",
            color=0xFFA500,
            timestamp=datetime.datetime.now()
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        #Adicionar avisos (máximo 10 para não ficar muito longo)
        for warning in warnings[-10:]: 
            try:
                moderator = await self.bot.fetch_user(int(warning['moderador']))
                mod_name = moderator.display_name
            except:
                mod_name = "Moderador não encontrado"
            
            embed.add_field(
                name=f"⚠️ Aviso #{warning['id']}",
                value=(
                    f"**Motivo:** {warning['motivo']}\n"
                    f"**Por:** {mod_name}\n"
                    f"**Data:** {warning['data']}"
                ),
                inline=False
            )
        
        #Adicionar informações de punição atual
        current_warnings = len(warnings)
        if current_warnings >= 5:
            status = "🔨 **BANIDO**"
            embed.color = 0xFF0000
        elif current_warnings >= 3:
            status = "🔇 **MUTADO**"
            embed.color = 0xFF0000
        else:
            status = "✅ Ativo"
        
        embed.add_field(
            name="📊 Status Atual",
            value=status,
            inline=True
        )
        
        embed.set_footer(text=f"Use !removeraviso {member.id} <ID> para remover um aviso")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def removeraviso(self, ctx, member: discord.Member, warning_id: int):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        #Verificar se existem avisos
        if (guild_id not in self.warnings or 
            user_id not in self.warnings[guild_id] or 
            not self.warnings[guild_id][user_id]):
            
            embed = discord.Embed(
                title="❌ Erro",
                description=f"{member.mention} não possui avisos para remover.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        warnings = self.warnings[guild_id][user_id]
        
        #Procurar o aviso pelo ID
        warning_to_remove = None
        for warning in warnings:
            if warning['id'] == warning_id:
                warning_to_remove = warning
                break
        
        if not warning_to_remove:
            embed = discord.Embed(
                title="❌ Aviso Não Encontrado",
                description=f"Aviso **#{warning_id}** não encontrado para {member.mention}.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        #Remover o aviso
        warnings.remove(warning_to_remove)
        
        for i, warning in enumerate(warnings, 1):
            warning['id'] = i

        self.save_warnings()
        
        #Embed de sucesso
        embed = discord.Embed(
            title="✅ Aviso Removido",
            color=0x00FF00,
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="👤 Usuário", value=member.mention, inline=True)
        embed.add_field(name="🔢 Aviso Removido", value=f"#{warning_id}", inline=True)
        embed.add_field(name="📝 Motivo Original", value=warning_to_remove['motivo'], inline=False)
        embed.add_field(name="📊 Avisos Restantes", value=f"**{len(warnings)}**", inline=True)
        
        #Verificar se precisa remover punição automática
        current_warnings = len(warnings)
        punishment_removed = None
        
        if current_warnings < 3:
            mute_role = await self.get_mute_role(ctx.guild)
            if mute_role and mute_role in member.roles:
                try:
                    await member.remove_roles(mute_role, reason="Remoção automática de mute - avisos abaixo do limite")
                    punishment_removed = "🔊 Mute removido automaticamente"
                except discord.Forbidden:
                    punishment_removed = "⚠️ Mute deveria ser removido, mas sem permissões"
        
        if punishment_removed:
            embed.add_field(name="🔄 Ajuste Automático", value=punishment_removed, inline=False)
        
        embed.set_footer(text=f"Removido por {ctx.author.display_name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))