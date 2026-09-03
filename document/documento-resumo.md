<img src="../assets/logo-fiap.png" alt="FIAP" width="30%">

# Documento Resumo — CardioIA · Fase 1: Batimentos de Dados

**Aluno:** Guilherme Yamada Dantas — **RM:** rm568506
**Curso:** Inteligência Artificial (2º ano) — **Fase 1, Capítulo 1:** *A Busca de Dados — Preparando o Terreno para a Inteligência Cardiológica*
**Repositório:** <https://github.com/japatraderdev99/fiap-preparando-terreno-para-inteligencia-cardiologica>

---

## 1. Objetivo da fase

Assumir o papel de **cientista de dados hospitalar** e levantar, organizar e
documentar as três matérias-primas que alimentarão os módulos inteligentes do
CardioIA nas próximas 6 fases:

1. **Dados numéricos** de pacientes cardíacos (base para Machine Learning e IoT);
2. **Textos** sobre saúde cardiovascular (base para NLP);
3. **Imagens** de exame cardiológico (base para Visão Computacional).

Tudo com **governança de dados e atenção a viés** desde o primeiro dado.

---

## 2. O que foi entregue

| Parte | Entregável | Quantidade | Mínimo exigido | Fonte | Tipo |
|---|---|---|---|---|---|
| 1 — Numérico | `dados/numericos/cardioia_heart_disease.csv` | **920 pacientes**, 25 colunas | 100 linhas | UCI Heart Disease (Cleveland, Hungria, Suíça, V.A.) | **Real** |
| 2 — Textual | `assets/textos/*.txt` | **4 textos**, ~93 mil palavras, PT + EN | 2 textos | OPAS/OMS, SciELO, Project Gutenberg | Real |
| 3 — Visual | `dados/visuais/ecg_images/*.png` + `labels.csv` | **120 ECGs de 12 derivações**, rotulados | 100 imagens | PTB-XL / PhysioNet | **Real** |

Todos os conjuntos são **regeneráveis por script** e têm **licença compatível**
(CC BY 4.0, domínio público; o artigo SciELO é CC BY-NC 3.0).

---

## 3. Parte 1 — Dados Numéricos (ML / IoT)

- **Base:** UCI *Heart Disease* (1988), união das 4 instituições → 920 pacientes.
- **Pipeline:** `preparar_dados_numericos.py` lê os dados brutos, corrige tipos,
  converte "zeros clínicos impossíveis" (`colesterol = 0`) em ausência, adiciona
  colunas legíveis e as variáveis-alvo (`doenca_cardiaca` binária e `diagnostico_num`
  0–4), e gera uma análise exploratória automática.
- **Variáveis mais relevantes clinicamente** (justificativa completa no README):
  `age`, `sex`, `cp` (tipo de dor torácica), `trestbps` (PA), `chol` (colesterol),
  `thalach` (FC máx.), `exang` (angina de esforço), `oldpeak` e `ca` (carga
  aterosclerótica). São fatores de risco modificáveis ou marcadores diretos de
  isquemia — o que um modelo de risco precisa enxergar.
- **Achados de viés já documentados:** 79% dos pacientes são homens; a base da Suíça
  tem 93,5% de doentes; `ca` e `thal` têm > 50% de ausência, de forma dependente da
  instituição.

## 4. Parte 2 — Dados Textuais (NLP)

- **Corpus:** folha informativa da **OPAS/OMS** (PT), artigo dos **Arquivos
  Brasileiros de Cardiologia** via SciELO (PT), e duas obras médicas históricas do
  **Project Gutenberg** (EN, 1901 e 1912).
- **Pipeline:** `preparar_textos.py` baixa e normaliza tudo para texto puro UTF-8 com
  cabeçalho de metadados padronizado.
- **Uso previsto em NLP:** extração de sintomas/entidades (NER), classificação de
  tópicos por especialidade, análise de sentimento/legibilidade para o assistente
  virtual, normalização terminológica (CID-10/DeCS) e base de conhecimento para RAG.
- **Por que importa:** a maior parte da informação clínica real é texto livre; sem
  NLP, ela não chega aos modelos.

## 5. Parte 3 — Dados Visuais (Visão Computacional)

- **Conjunto:** 120 imagens de **ECG de 12 derivações** renderizadas a partir de
  **sinais reais** da PTB-XL, no formato clínico padrão (25 mm/s, 10 mm/mV).
- **Rotuladas** por achado diagnóstico em 5 superclasses (`NORM`, `MI`, `STTC`, `CD`,
  `HYP`), **24 por classe**, **60 masculino / 60 feminino** — prontas para
  classificação supervisionada, não só inspeção visual.
- **Uso previsto em VC:** detecção de bordas/segmentação de derivações, detecção de
  complexos QRS e ritmo, CNN para `imagem → diagnóstico`, reconhecimento de anomalias
  (supradesnível de ST), Grad-CAM para explicabilidade, *data augmentation*.
- **Por que ECG:** exame cardiológico mais disponível, barato e padronizado — e nem
  toda unidade tem cardiologista para interpretá-lo.

## 6. Governança e viés (resumo)

Documento completo: [`governanca-dados-e-vies.md`](governanca-dados-e-vies.md).

- **Proveniência:** toda fonte com URL, DOI/ID, ano e licença.
- **Reprodutibilidade:** 3 scripts regeneram 100% dos dados; nada editado à mão.
- **Privacidade:** nenhum dado identifica pacientes; conforme finalidade acadêmica e LGPD.
- **Viés mapeado:** seleção por instituição, desbalanço de sexo/idade, ausência não
  aleatória, defasagem histórica e geográfica, idioma do corpus. Cada um com
  mitigação proposta para as fases seguintes.

---

## 7. Estrutura do repositório

```
assets/textos/   Parte 2 — 4 .txt + FONTES_E_LICENCAS.md + pipeline (NLP)
dados/
  numericos/     Parte 1 — CSV final + dicionário + EDA + pipeline + dados brutos
  visuais/       Parte 3 — 120 PNG + labels.csv + amostras/ + LEIA-ME.md + pipeline
document/            este resumo + governança + documento do projeto (modelo FIAP)
scripts/         download dos dados brutos + empacotamento da entrega
notebooks/       reservada para os notebooks de Colab/Jupyter das próximas fases
```

## 8. Links públicos para os dados

O conjunto completo (numérico + textual + visual) está **versionado no próprio
repositório** e também empacotado (4 `.zip`) em dois locais públicos, acessíveis sem login:

- **Google Drive** (pasta "FIAP - CardioIA - Fase 1", "qualquer pessoa com o link"):
  <https://drive.google.com/drive/folders/16FjfiQG6EJJIPeHYDrwGwO5cVUbyqvz3?usp=sharing>
- **GitHub Release `v1.0-fase1`:**
  <https://github.com/japatraderdev99/fiap-preparando-terreno-para-inteligencia-cardiologica/releases/tag/v1.0-fase1>

## 9. Conclusão

A base do CardioIA está montada: três tipos de dado, todos **reais**, **acima do
mínimo exigido**, **rotulados quando possível**, **rastreáveis**, **reprodutíveis** e
com os **vieses já identificados e documentados**. O terreno está preparado para a
Fase 2 (diagnóstico automatizado).
