#!/bin/bash

DATA=$(date +"%Y%m%d_%H%M%S")

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

DOCS="$BASE_DIR/documentos"
BACKUPS="$BASE_DIR/backups"
LOG="$BASE_DIR/logs/backup.log"

mkdir -p "$BACKUPS"

ARQUIVO="backup_$DATA.tar.gz"

tar -czf "$BACKUPS/$ARQUIVO" "$DOCS"

openssl enc -aes-256-cbc \
-salt \
-in "$BACKUPS/$ARQUIVO" \
-out "$BACKUPS/$ARQUIVO.enc" \
-pass pass:123456

rm "$BACKUPS/$ARQUIVO"

TAMANHO=$(du -h "$BACKUPS/$ARQUIVO.enc" | cut -f1)

echo "[$(date)] BACKUP OK | Arquivo: $ARQUIVO.enc | Tamanho: $TAMANHO" >> "$LOG"

python3 "$BASE_DIR/backup/reg_backup.py"
