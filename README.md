<div align="center">

# 🎵 Orpheus Bot

**"Como Orfeu encantava até as pedras com sua lira, eu trago harmonia e ordem para seu servidor Discord."**

[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3+-blue.svg)](https://discordpy.readthedocs.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-cyan.svg)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-14%20passed-purple.svg)](https://github.com/KingErik06/OrpheusBot)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/KingErik06/OrpheusBot/actions/workflows/ci.yml/badge.svg)](https://github.com/LingErik06/OrpheusBot/actions)

*Música de alta qualidade, filas inteligentes e controles avançados - tudo em português!*

</div>

## ✨ Características

### 🎶 Sistema de Música Divino
- **Qualidade de Estúdio**: Áudio crystal-clear com FFmpeg
- **Busca Inteligente**: Funciona com URLs ou nomes de músicas
- **Sistema de Loops**: Loop individual e loop de fila
- **Filas Inteligentes**: Gestão avançada com embeds visuais 
- **Controle de Volume**: Ajuste dinâmico em tempo real

### ⚡ Tecnologia de Ponta
- **Containerizado**: Docker completo para qualquer ambiente
- **Testado Rigorosamente**: 14 testes unitários garantindo qualidade
- **Arquitetura Modular**: Cogs para fácil expansão
- **Performance Otimizada**: Async/await para máxima eficiência

### 🎨 Embeds Profissionais com Dados do YouTube
- **Thumbnails Automáticas**: Imagens das músicas
- **Informações Completas**: Título, canal, duração, visualizações  
- **Design Temático**: Cores do YouTube com identidade visual
- **Links Clicáveis**: Acesso rápido ao vídeo original
- **Layout Responsivo**: Campos organizados e informativos

### 🎮 Experiência do Usuário
- **Comandos em Português**: Interface nativa para usuários BR
- **Embeds Visuais**: Interface rica e informativa
- **Resposta Rápida**: Comandos otimizados para velocidade
- **Tratemento de Erros**: Feedback claro e útil

### ⚖️ Moderação Sábia
- Sistema de avisos automáticos
- Ferramentas anti-spam e anti-raid
- Logs detalhados de moderação
- Auto-moderação inteligente

### 🛡️ Sistema de Punições Automáticas
- 3 Avisos = Mute automático
- 5 Avisos = Ban automático
- Remoção automática de punições quando avisos diminuem
- Embeds profissionais com status em tempo real

## 🚀 Começando Rápido

### Pré-requisitos
- **Docker** e **Docker Compose** ([Instalar](https://docs.docker.com/get-docker/))
- **Discord Bot Token** ([Criar](https://discord.com/developers/applications))

### ⚡ Instalação em 2 Minutos
1. **Clone o repositório**
```bash
git clone https://github.com/KingErik06/OrpheusBot.git
cd OrpheusBot
```

2. **Configure o Ambiente**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com seu token do Discord:
# DISCORD_TOKEN=seu_token_aqui
```

3. **Execute com Docker**
```bash
docker compose up -d
```

**Pronto! Seu bot está rodando!**

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

### ⚖️ Moderação Avançada
- `!limpar [número]` - Limpa mensagens
- `!aviso @usuário [motivo]` - Avisa um usuário com sistema progressivo
- `!avisos @usuário` - Mostra histórico de avisos
- `!removeraviso @usuário ID` - Remove aviso específico

### 🔧 Utilitários
- `!ping` - Mostra a latência
- `!info` - Informações do bot
- `!ajuda` - Mostra todos os comandos

## 🏗️ Estrutura
```
OrpheusBot/
├── docker-compose.yml
├── Dockerfile
├── tests
├── cogs/
│   ├── music.py
│   ├── moderation.py
│   └── utils.py
├── config.py
├── requirements.txt
└── main.py
```

## Executando os Testes
```bash
# Com Docker (recomendado)
docker compose run --rm bot pytest tests/ -v

# Localmente 
pip install -r requirements.txt
pytest tests/ -v
```

## 📄 Licença

MIT License

## Author 

**Erik** - [KingErik06](https://github.com/KingErik06)

*Desenvolvido com 💙 e um toque de mitologia grega*