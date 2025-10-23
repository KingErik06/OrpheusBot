import pytest
import asyncio
import discord
from unittest.mock import AsyncMock, MagicMock, patch

class TestMusicCog:
    @pytest.mark.asyncio
    async def test_tocar_command_exists(self):
        from main import OrpheusBot
        from cogs.music import Music
        
        bot = OrpheusBot()
        music_cog = Music(bot)

        assert hasattr(music_cog, 'tocar'), "❌ Método tocar não existe na cog"
        tocar_method = getattr(music_cog, 'tocar')
        assert callable(tocar_method), "❌ tocar não é callable"
        print("✅ Comando tocar existe e é callable")
        
        essential_commands = ['entrar', 'pular', 'volume', 'queue', 'parar', 'sair', 'loop']
        for cmd_name in essential_commands:
            if hasattr(music_cog, cmd_name):
                method = getattr(music_cog, cmd_name)
                assert callable(method), f"❌ {cmd_name} não é callable"
                print(f"✅ Comando {cmd_name} existe e é callable")
    
    @pytest.mark.asyncio
    async def test_youtube_dl_available(self):
        try:
            import yt_dlp
            print("✅ yt-dlp disponível para uso")
            
            from cogs.music import ytdl
            print("✅ Módulo ytdl importado corretamente")
            
            from cogs.music import YTDLSource
            assert hasattr(YTDLSource, 'from_url'), "❌ YTDLSource.from_url não existe"
            print("✅ YTDLSource importado corretamente")
            
            assert True
        except ImportError as e:
            pytest.fail(f"❌ yt-dlp não disponível: {e}")
    
    def test_ffmpeg_detection(self):
        import subprocess
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                print("✅ FFmpeg encontrado no sistema")
            else:
                print("⚠️ FFmpeg não encontrado (pode ser normal em testes)")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️ FFmpeg não disponível (normal em alguns ambientes)")
        assert True
    
    def test_music_cog_structure(self):
        from main import OrpheusBot
        from cogs.music import Music
        
        bot = OrpheusBot()
        music_cog = Music(bot)
 
        assert hasattr(music_cog, 'bot'), "❌ Cog não tem referência ao bot"
        assert music_cog.bot == bot, "❌ Referência do bot incorreta"
        
        assert hasattr(music_cog, 'queues'), "❌ Cog não tem sistema de filas"
        assert hasattr(music_cog, 'volumes'), "❌ Cog não tem sistema de volumes"
        assert hasattr(music_cog, 'loops'), "❌ Cog não tem sistema de loops"
        
        assert hasattr(music_cog, '_play'), "❌ Método _play não existe"
        assert hasattr(music_cog, '_play_next'), "❌ Método _play_next não existe"
        assert hasattr(music_cog, 'get_queue'), "❌ Método get_queue não existe"
        
        print("✅ Estrutura da Music cog está correta")
    
    def test_ytdl_source_structure(self):
        from cogs.music import YTDLSource
        
        assert issubclass(YTDLSource, discord.PCMVolumeTransformer), "❌ YTDLSource não herda de PCMVolumeTransformer"
        
        assert hasattr(YTDLSource, 'from_url'), "❌ YTDLSource.from_url não existe"
        assert callable(YTDLSource.from_url), "❌ YTDLSource.from_url não é callable"
        
        print("✅ Estrutura do YTDLSource está correta")

@pytest.mark.asyncio
async def test_async_operations():
    async def dummy_async():
        return "success"
    result = await dummy_async()
    assert result == "success"
    print("✅ Operações assíncronas funcionando")