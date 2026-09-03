#!/usr/bin/env bash
# CardioIA - Fase 1 | Gera os .zip do pacote publico (GitHub Release / Google Drive).
# Uso: bash scripts/empacotar_entrega.sh
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="entrega"
rm -rf "$OUT" && mkdir -p "$OUT"

echo ">> Parte 1 - numerico"
zip -qr "$OUT/cardioia-fase1-dados-numericos.zip" \
    dados/1-numericos -x '*/__pycache__/*'

echo ">> Parte 2 - textual"
zip -qr "$OUT/cardioia-fase1-dados-textuais.zip" \
    dados/2-textuais -x '*/__pycache__/*'

echo ">> Parte 3 - visual (120 imagens de ECG + labels)"
zip -qr "$OUT/cardioia-fase1-dados-visuais.zip" \
    dados/3-visuais/ecg_images dados/3-visuais/labels.csv \
    dados/3-visuais/amostras dados/3-visuais/LEIA-ME.md

echo ">> Pacote completo"
zip -qr "$OUT/cardioia-fase1-dados-completo.zip" \
    dados docs README.md CITACOES.md LICENSE -x '*/__pycache__/*' '*/_ptbxl_meta/*'

echo
ls -lh "$OUT"
echo
echo "Suba os .zip de $OUT/ como assets de um GitHub Release e/ou para o Google Drive."
