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
    'source_address': '0.0.0.0'
}

ffmpeg_options = {'options': '-vn'}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

#Classe Principal:
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
#Classe Música:
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        print("🎵 Cod de Música Carregado!")

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]
    
    @commands.command()
    async def entrar(self, ctx):
        #Entra no canal de voz
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"🎵 Conectado em {channel.name}!")
        else:
            await ctx.send("Você precisa estar em um canal de voz.")

    @commands.command()
    async def tocar(self, ctx, *, query):
        #Toca uma música do YouTube
        try:
            #Ele entra no canal de voz se não estiver conectado
            if not ctx.voice_client:
                await ctx.invoke(self.entrar)
        
            async with ctx.typing():
                player = await YTDLSource.from_url(query, loop=self.bot.loop, stream=True)

                #Adiciona à fila
                queue = self.get_queue(ctx.guild.id)
                queue.append(player)

                #Se não estava tocando nada, começa a tocar
                if not ctx.voice_client.is_playing():
                    self.proxima(ctx, queue)
                    #Criar um embed profissional:
                    embed = discord.Embed(
                        title="🎵 Tocando Agora",
                        description=f"**{player.title}**",
                        color=0xFF0000, #Vermelho YouTube
                        url=player.url
                    )
                    #Adiciona a thumbnail:
                    if 'thumbnail' in player.data:
                        embed.set_thumbnail(url=player.data['thumbnail'])
                    #Adiciona o uploader:
                    if 'uploader' in player.data:
                        embed.add_field(name="🎤 Canal", value=player.data['uploader'], inline=True)
                    #Adiciona a duração:
                    if 'duration' in player.data:
                        duration = player.data['duration']
                        minutes = duration // 60
                        seconds = duration % 60
                        embed.add_field(name="⏱️ Duração", value=f"{minutes}:{seconds:02d}", inline=True)
                    #Adiciona as visualizações:
                    if 'view_count' in player.data:
                        views = player.data['view_count']
                        embed.add_field(name="👀 Visualizações", value=f"{views:,}", inline=True)
                    #Adiciona botão de pular:
                    embed.set_footer(text="Use '!pular' para pular esta música.")
                    await ctx.send(embed=embed)

                else:
                    embed_fila = discord.Embed(
                        title="📥 Adicionado à Fila",
                        description=f"**{player.title}**",
                        color=0xFFA500 #laranja
                    )
                    #Adiciona a thumbnail
                    if 'thumbnail' in player.data:
                        embed_fila.set_thumbnail(url=player.data['thumbnail'])
                    #Adiciona o uploader
                    if 'uploader' in player.data:
                        embed_fila.add_field(name="🎤 Canal", value=player.data['uploader'], inline=True)
                    await ctx.send(embed=embed_fila)

        except Exception as e:
            await ctx.send(f"Erro ao tocar música: {str(e)}.")
    
    def proxima(self, ctx, queue):
        #Verifica se há músicas na fila
        if queue:
            player = queue.pop(0)

            def after_playing(error):
                if error:
                    print(f"❌ Erro na reprodução: {error}")
                if queue:
                    self.proxima(ctx, queue)
            ctx.voice_client.play(player, after=after_playing)


    @commands.command()
    async def pular(self, ctx):
        #Pula a música atual
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Música Pulada.")
        else:
            await ctx.send("Não há música tocando.")


    @commands.command()
    async def queue(self, ctx):
        #Mostra a fila de músicas
        queue = self.get_queue(ctx.guild.id)
        if queue:
            queue_list = "\n".join([f"{i+1}. {song.title}" for i, song in enumerate(queue[:10])])
            await ctx.send(f"**Fila:**\n{queue_list}")
        else:
            await ctx.send("Fila vazia!")


    @commands.command()
    async def parar(self, ctx):
        #Para a música e limpa a fila
        if ctx.voice_client:
            self.queues[ctx.guild.id] = []
            ctx.voice_client.stop()
            await ctx.send("Música parada e fila limpa!")

    
    @commands.command()
    async def sair(self, ctx):
        #Sai do canal de voz
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Saindo do canal de voz!")


async def setup(bot):
    await bot.add_cog(Music(bot))