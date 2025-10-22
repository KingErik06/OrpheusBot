import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
    DEBUG_MODE = int(os.getenv('DEBUG_MODE', 0))

    @classmethod
    def validate(cls):
        if not cls.DISCORD_TOKEN:
            raise ValueError("🚨 DISCORD_TOKEN não encontrado!\n" "Crie um arquivo .env baseado no .env.example e adicione seu token.")
        
        if len(cls.DISCORD_TOKEN) < 10:
            raise ValueError("🚨 DISCORD_TOKEN parece inválido (muito curto)")