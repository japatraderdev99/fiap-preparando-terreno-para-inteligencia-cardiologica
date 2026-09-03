"""
CardioIA - Fase 1 | Parte 1 (Dados numericos / IoT clinico)
Pipeline reproduzivel: dados BRUTOS da UCI -> dataset LIMPO e documentado.

Entrada  : dados/numericos/brutos/processed.{cleveland,hungarian,switzerland,va}.data
Saida    : dados/numericos/cardioia_heart_disease.csv   (dataset final, 1 linha = 1 paciente)
           dados/numericos/analise_exploratoria.md       (resumo estatistico auto-gerado)

Fonte
-----
Janosi, Steinbrunn, Pfisterer, Detrano (1988). "Heart Disease".
UCI Machine Learning Repository. https://doi.org/10.24432/C52P4X  (licenca CC BY 4.0)
Bases: Cleveland Clinic Foundation, Hungarian Institute of Cardiology (Budapeste),
University Hospital (Zurique/Basileia, Suica) e V.A. Medical Center (Long Beach, EUA).

Uso
---
    python preparar_dados_numericos.py
"""
from __future__ import annotations

import textwrap
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
BRUTOS = AQUI / "brutos"
SAIDA_CSV = AQUI / "cardioia_heart_disease.csv"
SAIDA_EDA = AQUI / "analise_exploratoria.md"

COLUNAS = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
           "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]

ARQUIVOS = {
    "cleveland": "processed.cleveland.data",
    "hungarian": "processed.hungarian.data",
    "switzerland": "processed.switzerland.data",
    "va": "processed.va.data",
}

MAP_SEXO = {0: "feminino", 1: "masculino"}
MAP_CP = {1: "angina_tipica", 2: "angina_atipica", 3: "dor_nao_anginosa", 4: "assintomatico"}
MAP_RESTECG = {0: "normal", 1: "anormalidade_st_t", 2: "hipertrofia_ventricular_esq"}
MAP_SLOPE = {1: "ascendente", 2: "plano", 3: "descendente"}
MAP_THAL = {3: "normal", 6: "defeito_fixo", 7: "defeito_reversivel"}
MAP_BOOL = {0: "nao", 1: "sim"}


def carrega() -> pd.DataFrame:
    partes = []
    for origem, nome in ARQUIVOS.items():
        df = pd.read_csv(BRUTOS / nome, header=None, names=COLUNAS, na_values="?")
        df.insert(0, "origem", origem)
        partes.append(df)
    return pd.concat(partes, ignore_index=True)


def limpa(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # tipos numericos
    for c in ["age", "trestbps", "chol", "thalach", "oldpeak", "ca"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["sex", "cp", "fbs", "restecg", "exang", "slope", "thal", "num"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    # regra clinica: colesterol/pressao == 0 significa "nao medido", nao zero real
    df.loc[df["chol"] == 0, "chol"] = np.nan
    df.loc[df["trestbps"] == 0, "trestbps"] = np.nan

    # id sequencial e identificador de paciente por base
    df.insert(0, "id_paciente", [f"{o[:3].upper()}-{i:04d}"
                                 for i, o in enumerate(df["origem"], 1)])

    # alvo: original (0-4) e binario
    df["diagnostico_num"] = df["num"]
    df["doenca_cardiaca"] = (df["num"].fillna(0) > 0).astype(int)

    # colunas legiveis (para EDA / relatorios / NLP tabular)
    df["sexo"] = df["sex"].map(MAP_SEXO)
    df["tipo_dor_peito"] = df["cp"].map(MAP_CP)
    df["glicemia_jejum_alta"] = df["fbs"].map(MAP_BOOL)
    df["ecg_repouso"] = df["restecg"].map(MAP_RESTECG)
    df["angina_por_esforco"] = df["exang"].map(MAP_BOOL)
    df["inclinacao_st"] = df["slope"].map(MAP_SLOPE)
    df["cintilografia_talio"] = df["thal"].map(MAP_THAL)

    # faixa etaria (util para analise de subgrupo / vies)
    df["faixa_etaria"] = pd.cut(df["age"], [0, 40, 50, 60, 70, 120],
                                labels=["<40", "40-49", "50-59", "60-69", "70+"])

    ordem = ["id_paciente", "origem", "age", "sex", "sexo", "cp", "tipo_dor_peito",
             "trestbps", "chol", "fbs", "glicemia_jejum_alta", "restecg", "ecg_repouso",
             "thalach", "exang", "angina_por_esforco", "oldpeak", "slope", "inclinacao_st",
             "ca", "thal", "cintilografia_talio", "faixa_etaria",
             "diagnostico_num", "doenca_cardiaca"]
    return df[ordem]


def gera_eda(df: pd.DataFrame) -> str:
    n = len(df)
    pos = int(df["doenca_cardiaca"].sum())
    linhas = []
    linhas.append("# Analise Exploratoria - Dataset Numerico CardioIA\n")
    linhas.append("> Arquivo gerado automaticamente por `preparar_dados_numericos.py`. "
                  "Nao editar a mao.\n")
    linhas.append(f"- **Total de pacientes:** {n}")
    linhas.append(f"- **Com doenca cardiaca (`doenca_cardiaca=1`):** {pos} "
                  f"({pos / n:.1%}) | **sem:** {n - pos} ({1 - pos / n:.1%})")
    linhas.append(f"- **Colunas:** {df.shape[1]}\n")

    linhas.append("## Distribuicao por base de origem\n")
    linhas.append("| origem | pacientes | % com doenca | idade media |")
    linhas.append("|---|---|---|---|")
    for o, g in df.groupby("origem"):
        linhas.append(f"| {o} | {len(g)} | {g['doenca_cardiaca'].mean():.1%} | "
                      f"{g['age'].mean():.1f} |")

    linhas.append("\n## Distribuicao por sexo\n")
    linhas.append("| sexo | pacientes | % da base | % com doenca |")
    linhas.append("|---|---|---|---|")
    for s, g in df.groupby("sexo"):
        linhas.append(f"| {s} | {len(g)} | {len(g) / n:.1%} | "
                      f"{g['doenca_cardiaca'].mean():.1%} |")

    linhas.append("\n## Variaveis numericas (apos limpeza)\n")
    num = df[["age", "trestbps", "chol", "thalach", "oldpeak"]].describe().T
    num["% ausente"] = df[["age", "trestbps", "chol", "thalach", "oldpeak"]].isna().mean().values
    linhas.append("| variavel | n | media | dp | min | max | % ausente |")
    linhas.append("|---|---|---|---|---|---|---|")
    for v, r in num.iterrows():
        linhas.append(f"| {v} | {int(r['count'])} | {r['mean']:.1f} | {r['std']:.1f} | "
                      f"{r['min']:.1f} | {r['max']:.1f} | {r['% ausente']:.1%} |")

    linhas.append("\n## Valores ausentes por coluna\n")
    linhas.append("| coluna | % ausente |")
    linhas.append("|---|---|")
    for c, p in df.isna().mean().sort_values(ascending=False).items():
        if p > 0:
            linhas.append(f"| {c} | {p:.1%} |")

    linhas.append("\n## Faixa etaria x prevalencia de doenca\n")
    linhas.append("| faixa | pacientes | % com doenca |")
    linhas.append("|---|---|---|")
    for f, g in df.groupby("faixa_etaria", observed=True):
        linhas.append(f"| {f} | {len(g)} | {g['doenca_cardiaca'].mean():.1%} |")

    return "\n".join(linhas) + "\n"


def main() -> None:
    bruto = carrega()
    df = limpa(bruto)
    df.to_csv(SAIDA_CSV, index=False)
    SAIDA_EDA.write_text(gera_eda(df), encoding="utf-8")

    print(f"OK  {len(df)} linhas -> {SAIDA_CSV.name}")
    print(textwrap.indent(df.head(4).to_string(), "    "))
    print(f"OK  resumo -> {SAIDA_EDA.name}")


if __name__ == "__main__":
    main()
