#!/bin/bash
while true; do
    echo "Iniciando bot..."
    python -u bot_deltachat.py serve
    echo "Bot terminó inesperadamente. Reiniciando en 5 segundos..."
    sleep 5
done
