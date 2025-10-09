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
        super().__init__(command_prefix='!', intents=discord.Intents.all())
        print("OrpheusBot Inicializado!")

    async def on_ready(self):
        print(f"🎵 {self.user} está online!")
        print(f"🎵 Conectado em {len(self.guilds)} servidores.")


#Inicialização do bot:
if __name__ == "__main__":
    bot = OrpheusBot()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ ERROR: DISCORD_TOKEN não encontrado no .env")
    else:
        bot.run(token)