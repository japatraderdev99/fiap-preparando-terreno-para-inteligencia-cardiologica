# Analise Exploratoria - Dataset Numerico CardioIA

> Arquivo gerado automaticamente por `preparar_dados_numericos.py`. Nao editar a mao.

- **Total de pacientes:** 920
- **Com doenca cardiaca (`doenca_cardiaca=1`):** 509 (55.3%) | **sem:** 411 (44.7%)
- **Colunas:** 25

## Distribuicao por base de origem

| origem | pacientes | % com doenca | idade media |
|---|---|---|---|
| cleveland | 303 | 45.9% | 54.4 |
| hungarian | 294 | 36.1% | 47.8 |
| switzerland | 123 | 93.5% | 55.3 |
| va | 200 | 74.5% | 59.4 |

## Distribuicao por sexo

| sexo | pacientes | % da base | % com doenca |
|---|---|---|---|
| feminino | 194 | 21.1% | 25.8% |
| masculino | 726 | 78.9% | 63.2% |

## Variaveis numericas (apos limpeza)

| variavel | n | media | dp | min | max | % ausente |
|---|---|---|---|---|---|---|
| age | 920 | 53.5 | 9.4 | 28.0 | 77.0 | 0.0% |
| trestbps | 860 | 132.3 | 18.5 | 80.0 | 200.0 | 6.5% |
| chol | 718 | 246.8 | 58.5 | 85.0 | 603.0 | 22.0% |
| thalach | 865 | 137.5 | 25.9 | 60.0 | 202.0 | 6.0% |
| oldpeak | 858 | 0.9 | 1.1 | -2.6 | 6.2 | 6.7% |

## Valores ausentes por coluna

| coluna | % ausente |
|---|---|
| ca | 66.4% |
| cintilografia_talio | 52.8% |
| thal | 52.8% |
| slope | 33.6% |
| inclinacao_st | 33.6% |
| chol | 22.0% |
| glicemia_jejum_alta | 9.8% |
| fbs | 9.8% |
| oldpeak | 6.7% |
| trestbps | 6.5% |
| thalach | 6.0% |
| exang | 6.0% |
| angina_por_esforco | 6.0% |
| restecg | 0.2% |
| ecg_repouso | 0.2% |

## Faixa etaria x prevalencia de doenca

| faixa | pacientes | % com doenca |
|---|---|---|
| <40 | 93 | 34.4% |
| 40-49 | 224 | 41.5% |
| 50-59 | 382 | 58.4% |
| 60-69 | 197 | 73.6% |
| 70+ | 24 | 66.7% |
