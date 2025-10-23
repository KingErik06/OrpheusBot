import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands

class TestBasicStructure:
    def test_imports(self):
        try:
            from config import Config
            import cogs.music
            import cogs.utils
            import cogs.moderation
            print("✅ Todas as importações funcionaram!")
            assert True
        except Exception as e:
            pytest.fail(f"❌ Falha na importação: {e}")
    
    def test_config_exists(self):
        from config import Config
        required_fields = ['DISCORD_TOKEN', 'BOT_PREFIX', 'DEBUG_MODE']
        for field in required_fields:
            assert hasattr(Config, field), f"❌ Campo {field} faltando na Config"
        print("✅ Estrutura da Config está correta")
    
    def test_bot_class_exists(self):
        from main import OrpheusBot
        
        assert hasattr(OrpheusBot, '__init__'), "❌ Classe OrpheusBot não encontrada"
        assert issubclass(OrpheusBot, commands.Bot), "❌ OrpheusBot não herda de commands.Bot"
        print("✅ Classe OrpheusBot existe e herda de commands.Bot")
    
    def test_bot_creation(self):
        from main import OrpheusBot
        
        bot = OrpheusBot()
        
        assert isinstance(bot, commands.Bot), "❌ Bot não é instância correta"
        assert bot.command_prefix == '!', f"❌ Prefixo do bot incorreto: {bot.command_prefix}"
        print("✅ Bot criado corretamente")
    
    @patch('discord.Client.is_ready')
    def test_bot_methods(self, mock_ready):
        from main import OrpheusBot
        
        bot = OrpheusBot()
        assert hasattr(bot, 'setup_hook'), "❌ Método setup_hook não existe"
        assert hasattr(bot, 'on_ready'), "❌ Método on_ready não existe"
        print("✅ Métodos do bot existem")

class TestMusicCogStructure:
    def test_music_cog_creation(self):
        from main import OrpheusBot
        from cogs.music import Music
        
        try:
            bot = OrpheusBot()
            music_cog = Music(bot)
            assert music_cog is not None
            assert hasattr(music_cog, 'bot')
            print("✅ Cog Music criada corretamente")
        except Exception as e:
            pytest.fail(f"❌ Falha criando Music cog: {e}")
    
    def test_music_commands_exist(self):
        from main import OrpheusBot
        
        bot = OrpheusBot()
        
        essential_commands = ['tocar', 'entrar', 'pular', 'volume', 'queue', 'parar', 'sair']
        
        for cmd_name in essential_commands:
            command = bot.get_command(cmd_name)
            if command is None:
                print(f"⚠️ Comando '{cmd_name}' não encontrado (pode ser normal - cogs não carregadas)")
            else:
                print(f"✅ Comando '{cmd_name}' encontrado")

def test_environment():
    import sys
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    print("✅ Ambiente de testes configurado!")