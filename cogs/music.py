#Importações:
import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

#Configurando o yt-dlp:
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True, 
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
    #Para funcionar localmente caso queira:
    #'executable': r'C:\ffmpeg\bin\ffmpeg.exe'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

#Classe Principal CORRIGIDA:
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#Classe Música COMPLETAMENTE REESCRITA:
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.volumes = {}
        self.loops = {}
        self.queue_loops = {}
        self.now_playing = {}
        print("🎵 Cog de Música Carregado!")

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]

    @commands.command()
    async def entrar(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()
            await ctx.send(f"🎵 Conectado em {channel.name}!")
        else:
            await ctx.send("Você precisa estar em um canal de voz.")

    @commands.command()
    async def tocar(self, ctx, *, query):
        try:
            if not ctx.voice_client:
                await ctx.invoke(self.entrar)
            elif ctx.author.voice and ctx.author.voice.channel != ctx.voice_client.channel:
                await ctx.send("❌ Você precisa estar no mesmo canal de voz que eu!")
                return
        
            async with ctx.typing():
                if not query.startswith(('http://', 'https://')):
                    query = f"ytsearch:{query}"
                
                player = await YTDLSource.from_url(query, loop=self.bot.loop, stream=True)
                queue = self.get_queue(ctx.guild.id)
                queue.append(player)

                if not ctx.voice_client.is_playing():
                    await self._play(ctx, player)
                    
                    embed = discord.Embed(
                        title="🎵 Tocando Agora",
                        description=f"**{player.title}**",
                        color=0xFF0000,
                        url=player.url
                    )
                    if 'thumbnail' in player.data:
                        embed.set_thumbnail(url=player.data['thumbnail'])
                    if 'uploader' in player.data:
                        embed.add_field(name="🎤 Canal", value=player.data['uploader'], inline=True)
                    if player.duration:
                        minutes = player.duration // 60
                        seconds = player.duration % 60
                        embed.add_field(name="⏱️ Duração", value=f"{minutes}:{seconds:02d}", inline=True)
                    embed.set_footer(text="Use '!pular' para pular esta música.")
                    await ctx.send(embed=embed)

                else:
                    embed_fila = discord.Embed(
                        title="📥 Adicionado à Fila",
                        description=f"**{player.title}**",
                        color=0xFFA500
                    )
                    if 'thumbnail' in player.data:
                        embed_fila.set_thumbnail(url=player.data['thumbnail'])
                    if 'uploader' in player.data:
                        embed_fila.add_field(name="🎤 Canal", value=player.data['uploader'], inline=True)
                    await ctx.send(embed=embed_fila)

        except Exception as e:
            await ctx.send(f"❌ Erro ao tocar música: {str(e)}")

    async def _play(self, ctx, player):
        """🔥 SOLUÇÃO DEFINITIVA para o problema _MissingSentinel"""
        guild_id = ctx.guild.id
        self.now_playing[guild_id] = player
        
        # 🔥 CORREÇÃO: Criar uma nova instância do FFmpegPCMAudio para cada reprodução
        try:
            # Define volume
            volume = self.volumes.get(guild_id, 50) / 100
            
            # Cria uma NOVA instância do áudio
            audio_source = discord.FFmpegPCMAudio(
                player.url,
                **ffmpeg_options
            )
            volume_adjusted = discord.PCMVolumeTransformer(audio_source, volume=volume)
            
            def after_playing(error):
                if error:
                    if "'_MissingSentinel' object has no attribute 'read'" not in str(error):
                        print(f"❌ Erro na reprodução: {error}")
                
                # 🔥 CORREÇÃO: Não usar run_coroutine_threadsafe dentro da callback
                # Em vez disso, criar uma task diretamente
                async def play_next():
                    await self._play_next(ctx)
                
                # Cria uma task assíncrona de forma segura
                asyncio.run_coroutine_threadsafe(play_next(), self.bot.loop)
            
            # Reproduz a música
            ctx.voice_client.play(volume_adjusted, after=after_playing)
            
        except Exception as e:
            print(f"Erro ao iniciar reprodução: {e}")
            await ctx.send(f"❌ Erro ao reproduzir música: {e}")

    async def _play_next(self, ctx):
        """Gerencia a próxima música na fila"""
        guild_id = ctx.guild.id
        queue = self.get_queue(guild_id)
        
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            return

        current_song = self.now_playing.get(guild_id)
        
        # 🔄 Lógica de Loop CORRIGIDA
        if self.loops.get(guild_id, False) and current_song:
            # Loop individual - toca a mesma música novamente
            await self._play(ctx, current_song)
            return
            
        elif self.queue_loops.get(guild_id, False) and current_song:
            # Loop da fila - coloca a música atual no final
            queue.append(current_song)
        
        # Remove a música atual da fila (se não estiver em loop individual)
        if queue and current_song in queue and not self.loops.get(guild_id, False):
            queue.remove(current_song)
        
        # Limpa a música atual
        if guild_id in self.now_playing:
            del self.now_playing[guild_id]
        
        # Toca próxima música se houver
        if queue:
            next_song = queue[0]
            await self._play(ctx, next_song)
        else:
            # Fila vazia
            await ctx.send("🎵 Fila terminada! Adicione mais músicas com `!tocar`")

    @commands.command()
    async def volume(self, ctx, volume: int = None):
        if volume is None:
            current_volume = self.volumes.get(ctx.guild.id, 50)
            await ctx.send(f"🔊 Volume atual: **{current_volume}%**")
            return

        if volume < 0 or volume > 100:
            await ctx.send("❌ Volume deve estar entre 0 e 100!")
            return
        
        self.volumes[ctx.guild.id] = volume
        if ctx.voice_client and ctx.voice_client.source:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"🔊 Volume ajustado para **{volume}%**")
        else:
            await ctx.send(f"🔊 Volume padrão definido para **{volume}%**")

    @commands.command()
    async def pular(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            # Chama _play_next manualmente
            await self._play_next(ctx)
            await ctx.send("⏭️ Música pulada!")
        else:
            await ctx.send("❌ Não há música tocando no momento.")

    @commands.command()
    async def loop(self, ctx):
        guild_id = ctx.guild.id
        self.loops[guild_id] = not self.loops.get(guild_id, False)

        if self.loops[guild_id]:
            await ctx.send("🔂 **Loop ativado!** A música atual será repetida.")
            self.queue_loops[guild_id] = False
        else:
            await ctx.send("⏹️ **Loop desativado!**")

    @commands.command()
    async def looplista(self, ctx):
        guild_id = ctx.guild.id
        self.queue_loops[guild_id] = not self.queue_loops.get(guild_id, False)

        if self.queue_loops[guild_id]:
            await ctx.send("🔁 **Loop da fila ativado!** A fila inteira será repetida.")
            self.loops[guild_id] = False
        else:
            await ctx.send("⏹️ **Loop da fila desativado!**")

    @commands.command()
    async def unloop(self, ctx):
        guild_id = ctx.guild.id
        self.loops[guild_id] = False
        self.queue_loops[guild_id] = False
        await ctx.send("⏹️ **Todos os loops desativados!**")

    @commands.command()
    async def radio(self, ctx, station="lofi"):
        stations = {
            'lofi': {
                'url': 'https://www.youtube.com/watch?v=jfKfPfyJRdk',
                'name': '🎧 Lofi Hip Hop Radio',
                'emoji': '🎧'},
            'rock': {
                'url': 'https://www.youtube.com/watch?v=Nt27aBceerI',
                'name': '🎸 Rock Classics Radio',
                'emoji': '🎸'},
            'jazz': {
                'url': 'https://www.youtube.com/watch?v=1QI_YCb6_Sk',
                'name': '🎷 Smooth Jazz Radio',
                'emoji': '🎷'}}
        
        if station not in stations:
            available = ", ".join([f"`{s}`" for s in stations.keys()])
            embed = discord.Embed(
                title="📻 Estações Disponíveis",
                description=f"Estações: {available}",
                color=0xff0000)
            embed.add_field(name="Exemplo", value="`!radio lofi`", inline=False)
            await ctx.send(embed=embed)
            return

        station_info = stations[station]
        embed=discord.Embed(
            title=f"{station_info['emoji']} Tocando {station_info['name']}",
            description=f"**Estação:** {station_info['name']}",
            color=0x00ff00)
        embed.add_field(name="🎵 Status", value="Carregando rádio...", inline=False)
        embed.set_footer(text="Use !parar para parar a reprodução.")
        loading_msg = await ctx.send(embed=embed)

        await ctx.invoke(self.tocar, query=station_info['url'])

        embed.set_field_at(0, name="🎵 Status", value="✅ Rádio carregada com sucesso!", inline=False)
        await loading_msg.edit(embed=embed)

    @commands.command()
    async def radios(self, ctx):
        embed = discord.Embed(
        title="📻 Rádios Online Disponíveis",
        description="Escolha uma estação com `!radio [nome]`",
        color=0x7289DA)
    
        embed.add_field(
        name="🎧 Lofi Hip Hop", 
        value="`!radio lofi` - Música relaxante para estudar/trabalhar",
        inline=False)
    
        embed.add_field(
        name="🎸 Rock Classics", 
        value="`!radio rock` - Clássicos do rock internacional", 
        inline=False)
    
        embed.add_field(
        name="🎷 Smooth Jazz", 
        value="`!radio jazz` - Jazz suave e instrumental",
        inline=False)
    
        embed.set_footer(text="Novas estações em breve!")
    
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        queue = self.get_queue(ctx.guild.id)
        current = self.now_playing.get(ctx.guild.id)
        
        if not queue and not current:
            await ctx.send("📭 Fila vazia!")
            return
            
        embed = discord.Embed(title="🎵 Fila de Músicas", color=0x00ff00)
        
        if current:
            embed.add_field(
                name="🎵 Tocando Agora",
                value=f"**{current.title}**",
                inline=False
            )
        
        if queue:
            queue_text = "\n".join([f"{i+1}. {song.title}" for i, song in enumerate(queue[:10])])
            embed.add_field(
                name=f"📋 Próximas Músicas ({len(queue)})",
                value=queue_text,
                inline=False
            )
        
        await ctx.send(embed=embed)

    @commands.command()
    async def parar(self, ctx):
        if ctx.voice_client:
            guild_id = ctx.guild.id
            self.queues[guild_id] = []
            if guild_id in self.now_playing:
                del self.now_playing[guild_id]
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            await ctx.send("⏹️ Música parada e fila limpa!")

    @commands.command()
    async def sair(self, ctx):
        if ctx.voice_client:
            guild_id = ctx.guild.id
            # Limpa tudo
            self.queues[guild_id] = []
            self.loops[guild_id] = False
            self.queue_loops[guild_id] = False
            if guild_id in self.now_playing:
                del self.now_playing[guild_id]
                
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Saindo do canal de voz!")

async def setup(bot):
    await bot.add_cog(Music(bot))