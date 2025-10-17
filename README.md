# 🎵 Orpheus Bot

*"Como Orfeu encantava até as pedras com sua lira, eu trago harmonia e ordem para seu servidor Discord."*

![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Stable](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

## ✨ Características

### 🎶 Música Divina
- **Reprodução Estável** - Músicas tocam completamente sem cortes
- **Sistema de Filas Avançado** - Transições suaves entre músicas
- **Loops poderosos** - Loop individual e de fila completa
- **Controles de volume** - Ajuste preciso de 0-100%
- **Busca inteligente** - Funciona com URLs ou nomes de músicas

### 🎨 Embeds Profissionais com Dados do YouTube
- **Thumbnails automáticas** - Imagens das músicas
- **Informações completas** - Título, canal, duração, visualizações  
- **Design temático** - Cores do YouTube com identidade visual
- **Links clicáveis** - Acesso rápido ao vídeo original
- **Layout responsivo** - Campos organizados e informativos

### 🔊 Sistema de Áudio Avançado
- **Qualidade de áudio** otimizada com FFmpeg
- **Streaming eficiente** sem download de arquivos
- **Sistema de filas** inteligente e estável

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
- `!volume [0-100]` - Ajusta o volume ou mostra o atual
- `!loop` - Repete a música atual infinitamente
- `!looplista` - Loop contínuo de toda a fila de músicas
- `!unloop` - Liberta das repetições eternas

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