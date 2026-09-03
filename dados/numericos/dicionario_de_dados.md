# Dicionário de Dados — `cardioia_heart_disease.csv`

Dataset tabular da **Parte 1 (Dados Numéricos / IoT clínico)** do projeto CardioIA.
Cada linha representa **um paciente** avaliado para doença arterial coronariana.
Arquivo gerado por [`preparar_dados_numericos.py`](preparar_dados_numericos.py) a partir
dos dados brutos da UCI (pasta [`brutos/`](brutos/)).

- **Linhas:** 920
- **Colunas:** 25
- **Codificação:** UTF-8, separador `,`, decimal `.`
- **Valores ausentes:** célula vazia (o script converte `?` e "zeros clínicos impossíveis" em ausência)

---

## 1. Identificação e origem

| Coluna | Tipo | Descrição |
|---|---|---|
| `id_paciente` | texto | Identificador sintético (`CLE-0001`, `HUN-0002`, …). Não é dado real de paciente. |
| `origem` | categórico | Instituição de coleta: `cleveland`, `hungarian`, `switzerland`, `va`. **Relevante para análise de viés** (ver `docs/governanca-dados-e-vies.md`). |

## 2. Variáveis clínicas (preditores)

| Coluna | Unidade / valores | Descrição | Relevância clínica |
|---|---|---|---|
| `age` | anos | Idade | Risco cardiovascular cresce de forma quase monotônica com a idade. |
| `sex` | `1` = masculino, `0` = feminino | Sexo biológico registrado | Homens têm evento coronariano ~10 anos mais cedo; risadas de base diferem por sexo. |
| `sexo` | texto | Versão legível de `sex` | Facilita EDA e relatórios. |
| `cp` | `1..4` | Tipo de dor torácica (código) | Sintoma-chave da triagem. |
| `tipo_dor_peito` | texto | `angina_tipica`, `angina_atipica`, `dor_nao_anginosa`, `assintomatico` | Angina típica eleva muito a probabilidade pré-teste de doença coronariana. |
| `trestbps` | mm Hg | Pressão arterial sistólica em repouso (admissão) | Hipertensão é fator de risco maior e modificável. |
| `chol` | mg/dL | Colesterol sérico total | Dislipidemia; valor `0` no dado bruto = "não medido" → convertido em ausente. |
| `fbs` | `1` = > 120 mg/dL, `0` = ≤ 120 | Glicemia de jejum elevada | Marcador de diabetes/pré-diabetes. |
| `glicemia_jejum_alta` | texto | Versão legível de `fbs` (`sim`/`nao`) | — |
| `restecg` | `0..2` | ECG de repouso (código) | Liga a Parte 1 (tabular) à Parte 3 (imagens de ECG). |
| `ecg_repouso` | texto | `normal`, `anormalidade_st_t`, `hipertrofia_ventricular_esq` | Alteração de ST-T e HVE indicam dano/estresse miocárdico. |
| `thalach` | bpm | Frequência cardíaca máxima atingida no teste de esforço | Baixa FC máx. associa-se a pior prognóstico. |
| `exang` | `1` = sim, `0` = não | Angina induzida por esforço | Forte indício de isquemia. |
| `angina_por_esforco` | texto | Versão legível de `exang` | — |
| `oldpeak` | mm | Infra/supradesnível de ST induzido por esforço (relativo ao repouso) | Quanto maior, maior a chance de isquemia significativa. |
| `slope` | `1..3` | Inclinação do segmento ST no pico do esforço (código) | ST descendente/plano = mais suspeito. |
| `inclinacao_st` | texto | `ascendente`, `plano`, `descendente` | — |
| `ca` | `0..3` | Nº de vasos principais corados na fluoroscopia | Proxy direto de carga aterosclerótica. Alta taxa de ausência. |
| `thal` | `3`,`6`,`7` | Cintilografia com tálio (código) | Defeito fixo = infarto prévio; reversível = isquemia. |
| `cintilografia_talio` | texto | `normal`, `defeito_fixo`, `defeito_reversivel` | — |
| `faixa_etaria` | categórico | `<40`, `40-49`, `50-59`, `60-69`, `70+` | Facilita análise de subgrupos e de viés etário. |

## 3. Variáveis-alvo (target)

| Coluna | Valores | Descrição |
|---|---|---|
| `diagnostico_num` | `0..4` | Diagnóstico angiográfico original da UCI: `0` = sem estenose relevante; `1..4` = nº de vasos com > 50% de obstrução. Útil para tarefas **multiclasse / ordinais**. |
| `doenca_cardiaca` | `0` / `1` | Alvo **binário** derivado (`diagnostico_num > 0`). Convenção padrão na literatura para esse dataset. |

---

## Notas de preparação (decisões documentadas)

1. **`chol == 0` e `trestbps == 0` → ausente.** Colesterol ou pressão iguais a zero são
   fisiologicamente impossíveis; na base da Suíça representam "não coletado".
2. **Nenhuma imputação foi aplicada.** A ausência é mantida explícita para que cada
   grupo, nas próximas fases, escolha a estratégia (imputação, modelos que toleram
   ausência, exclusão de variável).
3. **Colunas legíveis** (`sexo`, `tipo_dor_peito`, …) são redundantes com os códigos
   numéricos — servem para EDA, dashboards e para uso do próprio dataset como corpus
   textual tabular em NLP.
4. **Sem dados pessoais.** Idade, sexo e medidas clínicas não identificam indivíduos;
   os identificadores são sintéticos.

## Fonte

Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1989). *Heart Disease*.
UCI Machine Learning Repository. <https://doi.org/10.24432/C52P4X> — licença **CC BY 4.0**.
Coleta original: Cleveland Clinic Foundation (EUA), Hungarian Institute of Cardiology
(Budapeste), University Hospitals de Zurique e Basileia (Suíça) e V.A. Medical Center,
Long Beach (EUA), 1988.
