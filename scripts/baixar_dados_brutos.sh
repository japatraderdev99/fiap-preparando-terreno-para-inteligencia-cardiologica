#!/usr/bin/env bash
# CardioIA - Fase 1 | Baixa os dados BRUTOS de origem.
# Uso: bash scripts/baixar_dados_brutos.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo ">> Parte 1: UCI Heart Disease"
mkdir -p dados/numericos/brutos
tmp="$(mktemp -d)"
curl -sL "https://archive.ics.uci.edu/static/public/45/heart+disease.zip" -o "$tmp/uci.zip"
unzip -o "$tmp/uci.zip" -d "$tmp" >/dev/null
cp "$tmp"/processed.*.data "$tmp/heart-disease.names" dados/numericos/brutos/
rm -rf "$tmp"
echo "   ok -> dados/numericos/brutos/"

echo ">> Parte 3: metadados da PTB-XL (os sinais sao baixados pelo gerador de imagens)"
mkdir -p dados/visuais/_ptbxl_meta
curl -sL "https://physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv" \
     -o dados/visuais/_ptbxl_meta/ptbxl_database.csv
curl -sL "https://physionet.org/files/ptb-xl/1.0.3/scp_statements.csv" \
     -o dados/visuais/scp_statements.csv
cp dados/visuais/scp_statements.csv dados/visuais/_ptbxl_meta/
echo "   ok -> dados/visuais/_ptbxl_meta/"

echo
echo "Concluido. Agora rode os pipelines:"
echo "  python dados/numericos/preparar_dados_numericos.py"
echo "  python assets/textos/preparar_textos.py"
echo "  python dados/visuais/gerar_imagens_ecg.py --por-classe 24"
