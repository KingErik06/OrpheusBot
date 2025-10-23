#!/bin/bash

echo "🎵 Iniciando Orpheus Bot..."
echo "🔧 Verificando configurações..."

if [ -z "$DISCORD_TOKEN" ]; then
    echo "DISCORD_TOKEN não encontrado!"
    echo "Certifique-se de:"
    echo "  1. Configurar DISCORD_TOKEN no arquivo .env"
    echo "  2. Usar env_file no docker-compose.yml"
    exit 1
fi

echo "✅ Configurações verificadas"
echo "🚀 Iniciando bot..."

exec python -m orpheus_bot