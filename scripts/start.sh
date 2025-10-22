#!/bin/bash

echo "🎵 Iniciando Orpheus Bot..."
echo "🔧 Verificando configurações..."

if [ ! -f .env ]; then
    echo "Arquivo .env não encontrado!"
    echo "Certifique-se de:"
    echo "  1. Criar .env baseado no .env.example"
    echo "  2. Adicionar seu DISCORD_TOKEN"
    echo "  3. Montar como volume ou usar env_file no docker-compose"
    exit 1
fi

if [ ! -f requirements.txt ]; then
    echo "requirements.txt não encontrado!"
    exit 1
fi

echo "Configurações verificadas!"
echo "Iniciando o bot..."

exec python main.py