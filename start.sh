#!/bin/bash

# Inicializar la cuenta (usará las variables de entorno DCI_LOGIN_EMAIL, etc.)
echo "Inicializando cuenta del bot..."
python bot_deltachat.py init

# Bucle infinito para mantener el bot vivo
while true; do
    echo "Iniciando servicio del bot..."
    python -u bot_deltachat.py serve
    echo "Bot terminó inesperadamente. Reiniciando en 5 segundos..."
    sleep 5
done
