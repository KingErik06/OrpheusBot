#Importações:
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

#Carregar variáveis de ambiente do arquivo .env:
load_dotenv()

#Definição do bot:
class OrpheusBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all(), help_command=None)
        print("🎵 OrpheusBot Inicializado!")

    
    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            #Verifica se é arquivo python e não começa com __
            if os.path.isfile(os.path.join('./cogs', filename)) and filename.endswith('.py') and not filename.startswith('__'):
                await self.load_extension(f"cogs.{filename[:-3]}")
        print("🎵 Todos os cogs carregados.")


    async def on_ready(self):
        print(f"🎵 {self.user} está online!")
        print(f"🎵 Conectado em {len(self.guilds)} servidores.")
        print(f"🎵 {len(self.commands)} comandos carregados.")


#Inicialização do bot:
async def main():
    bot = OrpheusBot()
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())