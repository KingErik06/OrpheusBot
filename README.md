# 🎵 Orpheus Bot

*"Como Orfeu encantava até as pedras com sua lira, eu trago harmonia e ordem para seu servidor Discord."*

![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Características

### 🎶 Música Divina
- Reprodução de alta qualidade de YouTube, Spotify e mais
- Sistema de filas e playlists
- Letras em tempo real
- Controles intuitivos de música

### ⚖️ Moderação Sábia
- Sistema de avisos automáticos
- Ferramentas anti-spam e anti-raid
- Logs detalhados de moderação
- Auto-moderação inteligente

### 🎭 Inspirado na Mitologia Grega
- Comandos com temática épica
- Design inspirado na antiguidade clássica
- Performance estável como os deuses do Olimpo

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/KingErik06/OrpheusBot.git
cd OrpheusBot

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com seu token do Discord
```
## ⚙️ Configuração

1. Crie um aplicativo em [Discord Developer Portal](https://discord.com/developers/applications)
2. Vá em "Bot" e copie o token
3. Cole no arquivo `.env`:
```env
DISCORD_TOKEN=seu_token_aqui
```
## 🎮 Comandos Principais

### 🎵 Música
- `!entrar` - Conecta ao canal de voz
- `!tocar [música/URL]` - Reproduz uma música do YouTube
- `!pular` - Pula a música atual
- `!fila` - Mostra a fila de músicas
- `!parar` - Para a música e limpa a fila
- `!sair` - Sai do canal de voz

### ⚖️ Moderação  
- `!limpar [número]` - Limpa mensagens
- `!aviso @usuário` - Avisa um usuário

### 🔧 Utilitários
- `!ping` - Mostra a latência
- `!info` - Informações do bot

## 🏗️ Estrutura
```
OrpheusBot/
├── cogs/
│   ├── music.py
│   ├── moderation.py
│   └── utils.py
├── main.py
└── requirements.txt
```
## 📄 Licença

MIT License

---

*Desenvolvido com 💙 e um toque de mitologia grega*