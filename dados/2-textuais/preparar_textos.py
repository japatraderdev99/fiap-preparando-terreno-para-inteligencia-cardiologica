"""
CardioIA - Fase 1 | Parte 2 (Dados textuais / NLP)
Baixa e normaliza o corpus textual sobre doencas cardiovasculares.

Saida: dados/2-textuais/NN_<slug>_<lang>.txt
       Cada arquivo tem um cabecalho de metadados delimitado e, em seguida,
       o corpo em texto puro (UTF-8, sem HTML), pronto para tokenizacao.

Fontes (todas de acesso publico - ver FONTES_E_LICENCAS.md):
  01  OPAS/OMS  - Folha informativa "Doencas cardiovasculares" (PT)
  02  SciELO / Arq. Bras. Cardiologia - Evora et al., 2014 (PT, CC BY-NC 3.0)
  03  Project Gutenberg #43780 - Bruce, "Lettsomian Lectures on Diseases
      ... of the Heart and Arteries", 1901 (EN, dominio publico)
  04  Project Gutenberg #37675 - Warfield, "Arteriosclerosis and
      Hypertension", 1912 (EN, dominio publico)

Uso:  python preparar_textos.py
"""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (cardioia-fase1)"


def baixa(url: str) -> str:
    r = subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, url],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(f"falha ao baixar {url}")
    return r.stdout


def desmarca(txt: str) -> str:
    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", txt, flags=re.S)
    txt = re.sub(r"<li[^>]*>", "\n- ", txt)
    txt = re.sub(r"</(p|div|h[1-6]|section|tr|br)>", "\n", txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n +", "\n", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt.strip()


def limpa_gutenberg(txt: str) -> str:
    i = txt.find("*** START")
    j = txt.find("*** END")
    if i != -1 and j != -1:
        txt = txt[txt.find("\n", i) + 1:j]
    txt = re.sub(r"<[^>]+>", "", txt)                     # eventuais tags soltas
    txt = re.sub(r"Transcriber'?s Notes?:.*?(?=\n\n[A-Z0-9])", "", txt, count=1,
                 flags=re.S | re.I)
    txt = re.sub(r"Produced by .*?\n\n", "", txt, count=1, flags=re.S)
    txt = re.sub(r"\n\s*ERRATUM\s*\n.*?\n\n", "\n\n", txt, count=1, flags=re.S | re.I)
    txt = re.sub(r"^\s*(Passages in .*|Small caps .*|Text enclosed .*)$", "", txt,
                 flags=re.M | re.I)
    # remove indice remissivo no fim (lista "termo; num de pagina")
    txt = re.split(r"\n\s*INDEX\.?\s*\n", txt)[0]
    return re.sub(r"\n{3,}", "\n\n", txt).strip()


def escreve(nome: str, meta: dict, corpo: str) -> None:
    cab = ["=" * 78, "METADADOS (nao faz parte do texto a ser analisado)", "=" * 78]
    for k, v in meta.items():
        cab.append(f"{k}: {v}")
    cab += ["=" * 78, "TEXTO", "=" * 78, ""]
    destino = AQUI / nome
    destino.write_text("\n".join(cab) + "\n" + corpo.strip() + "\n", encoding="utf-8")
    palavras = len(corpo.split())
    print(f"  {nome:<52} {palavras:>7} palavras")


def secao_scielo(raw: str) -> str:
    m = re.search(r"<article[^>]*>(.*?)</article>", raw, re.S)
    corpo = desmarca(m.group(1) if m else raw)
    # remove seções de fim que não são o corpo do artigo
    corpo = re.split(r"\n(?:Referências|Contribuição dos autores|Potencial conflito)", corpo)[0]
    return corpo.strip()


def main() -> None:
    print("Baixando e normalizando o corpus textual...\n")

    # 01 - OPAS/OMS
    raw = baixa("https://www.paho.org/pt/topicos/doencas-cardiovasculares")
    m = re.search(r"<main.*?</main>", raw, re.S)
    corpo = desmarca(m.group(0) if m else raw)
    corpo = corpo[corpo.find("As doenças cardiovasculares são um grupo"):]
    corpo = re.split(r"\n(?:Estamos comprometidos|Temas relacionados|Boletín|Mais informa"
                     r"|Documentos rela|Notícias\n|Comunicados)", corpo)[0]
    corpo = corpo.replace("HEARTS nas Américas \n", "").strip()
    escreve("01_opas_oms_doencas_cardiovasculares_pt.txt", {
        "titulo": "Doenças cardiovasculares - Folha informativa",
        "fonte": "Organização Pan-Americana da Saúde (OPAS/OMS)",
        "url": "https://www.paho.org/pt/topicos/doencas-cardiovasculares",
        "idioma": "pt-BR",
        "tipo": "folha informativa de saúde pública",
        "uso": "conteúdo informativo público da OPAS/OMS; uso acadêmico com atribuição",
    }, corpo)

    # 02 - SciELO / ABC
    raw = baixa("https://www.scielo.br/j/abc/a/qtHhhVW66VdKkFS8kQGBtTS/?format=html&lang=pt")
    escreve("02_scielo_abc_prevalencia_doencas_cardiacas_pt.txt", {
        "titulo": ("Prevalência das Doenças Cardíacas Ilustrada em 60 Anos dos "
                   "Arquivos Brasileiros de Cardiologia"),
        "autores": "Evora PRB, Nather JC, Rodrigues AJ",
        "fonte": "Arquivos Brasileiros de Cardiologia, 2014; 102(1):9-16",
        "doi": "10.5935/abc.20140001",
        "url": "https://www.scielo.br/j/abc/a/qtHhhVW66VdKkFS8kQGBtTS/?lang=pt",
        "idioma": "pt-BR",
        "tipo": "artigo científico (acesso aberto)",
        "licenca": "Creative Commons Attribution Non-Commercial 3.0 (CC BY-NC 3.0)",
    }, secao_scielo(raw))

    # 03 e 04 - Project Gutenberg
    for gid, nome, meta in [
        ("43780", "03_gutenberg_lettsomian_lectures_diseases_heart_en.txt", {
            "titulo": ("The Lettsomian Lectures on Diseases and Disorders of the "
                       "Heart and Arteries in Middle and Advanced Life [1900-1901]"),
            "autor": "J. Mitchell Bruce",
            "fonte": "Project Gutenberg eBook #43780",
            "url": "https://www.gutenberg.org/ebooks/43780",
            "idioma": "en",
            "tipo": "obra médica histórica (semiologia cardiovascular)",
            "licenca": "domínio público (Project Gutenberg License)",
        }),
        ("37675", "04_gutenberg_arteriosclerosis_and_hypertension_en.txt", {
            "titulo": "Arteriosclerosis and Hypertension, with Chapters on Blood Pressure",
            "autor": "Louis M. Warfield",
            "fonte": "Project Gutenberg eBook #37675",
            "url": "https://www.gutenberg.org/ebooks/37675",
            "idioma": "en",
            "tipo": "obra médica histórica (aterosclerose e hipertensão)",
            "licenca": "domínio público (Project Gutenberg License)",
        }),
    ]:
        raw = baixa(f"https://www.gutenberg.org/cache/epub/{gid}/pg{gid}.txt")
        escreve(nome, meta, limpa_gutenberg(raw))

    print("\nConcluido. Corpus em", AQUI)


if __name__ == "__main__":
    main()
