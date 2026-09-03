# Corpus Textual — Fontes, Licenças e Uso em NLP

Corpus da **Parte 2 (Dados Textuais / NLP)** do projeto CardioIA.
Todos os arquivos são texto puro UTF-8, gerados/atualizáveis por
[`preparar_textos.py`](preparar_textos.py). Cada `.txt` começa com um bloco
`METADADOS` delimitado por linhas de `=`; o corpo para análise vem após o marcador
`TEXTO`.

## Arquivos

| # | Arquivo | Idioma | ~Palavras | Tipo | Fonte | Licença |
|---|---|---|---|---|---|---|
| 01 | `01_opas_oms_doencas_cardiovasculares_pt.txt` | PT-BR | ~1.7 mil | Folha informativa de saúde pública | OPAS/OMS — *Doenças cardiovasculares* | Conteúdo informativo público OPAS/OMS; uso acadêmico com atribuição |
| 02 | `02_scielo_abc_prevalencia_doencas_cardiacas_pt.txt` | PT-BR | ~2.7 mil | Artigo científico (acesso aberto) | Evora PRB, Nather JC, Rodrigues AJ. *Arq. Bras. Cardiol.* 2014;102(1):9-16 | **CC BY-NC 3.0** |
| 03 | `03_gutenberg_lettsomian_lectures_diseases_heart_en.txt` | EN | ~21 mil | Obra médica histórica (semiologia cardiovascular) | J. Mitchell Bruce, *Lettsomian Lectures on Diseases … of the Heart and Arteries* (1901) — Project Gutenberg #43780 | Domínio público |
| 04 | `04_gutenberg_arteriosclerosis_and_hypertension_en.txt` | EN | ~68 mil | Obra médica histórica (aterosclerose e hipertensão) | Louis M. Warfield, *Arteriosclerosis and Hypertension* (1912) — Project Gutenberg #37675 | Domínio público |

Links:
- OPAS/OMS: <https://www.paho.org/pt/topicos/doencas-cardiovasculares>
- SciELO: <https://www.scielo.br/j/abc/a/qtHhhVW66VdKkFS8kQGBtTS/?lang=pt> — DOI `10.5935/abc.20140001`
- Gutenberg #43780: <https://www.gutenberg.org/ebooks/43780>
- Gutenberg #37675: <https://www.gutenberg.org/ebooks/37675>

> O mínimo exigido pela atividade são **2 textos**. Foram incluídos **4**, cobrindo
> dois idiomas (PT/EN) e três registros de linguagem — divulgação em saúde pública,
> artigo científico e literatura médica histórica — para permitir estudos comparativos
> de NLP já nesta fase.

## Por que este corpus é adequado para NLP aplicada à saúde

O objetivo desta fase **não é treinar modelos**, e sim reunir matéria-prima com
diversidade linguística suficiente para as fases seguintes. As análises previstas:

### 1. Extração de sintomas e entidades clínicas (NER)
Os textos 01 e 03 são densos em descrição sintomática — *"dor ou desconforto no centro
do peito"*, *"dor … nos braços, ombro esquerdo, … mandíbula ou costas"*, *"falta de
ar"*, *"suor frio"*, *"palpitação"*, *"síncope"*. Permitem construir e avaliar um
extrator de sinais/sintomas (dicionário + regras, depois modelo), insumo direto para o
**sistema de triagem digital da Fase 2**.

### 2. Classificação de tópicos / especialidade
O texto 02 organiza explicitamente a cardiologia em grupos (coronariopatia,
valvopatia, cardiopatia congênita, cardiomiopatia, arritmia, insuficiência cardíaca,
fatores de risco). É um rótulo pronto para tarefas de **classificação temática** de
documentos e de mensagens de pacientes.

### 3. Análise de sentimento / carga emocional e legibilidade
Contrastar a linguagem tranquilizadora e preventiva da OPAS (01) com o tom clínico e
prognóstico das obras históricas (03, 04) serve para calibrar **análise de sentimento
em contexto clínico** e métricas de legibilidade — relevante para o **assistente
virtual empático da Fase 5**, que precisa comunicar risco sem alarmar.

### 4. Normalização terminológica e evolução da linguagem médica
Comparar termos de 1901/1912 (*"tobacco heart"*, *"soldier's heart"*, *"arterio-capillary
fibrosis"*) com a terminologia atual (OPAS/SciELO) exercita **mapeamento para
vocabulários controlados** (CID-10, SNOMED CT, DeCS/MeSH) — base de qualquer pipeline
sério de NLP clínico.

### 5. Recuperação de informação / RAG
O corpus é pequeno e curado o suficiente para servir de base de conhecimento em um
**chatbot com RAG** (Fase 5), testando *chunking*, *embeddings* multilíngues e citação
de fonte.

## Por que essas análises importam para IA em saúde

- **Dados clínicos reais são majoritariamente texto livre** (evoluções, laudos,
  anamnese). Sem NLP, a maior parte da informação assistencial fica inacessível a
  modelos.
- **Triagem e priorização** dependem de transformar queixa em linguagem natural em
  variáveis estruturadas — exatamente a ponte entre a Parte 2 e a Parte 1.
- **Segurança do paciente:** extração incorreta de negação (*"nega dor torácica"*) ou
  de temporalidade muda a conduta. Ter um corpus para testar esses casos desde já
  reduz risco lá na frente.

## Governança

- Nenhum texto contém dados de pacientes identificáveis.
- A licença de cada item está registrada acima e no cabeçalho de cada `.txt`.
- O texto 02 é **CC BY-NC**: uso **não comercial**. Aceitável para projeto acadêmico;
  registrado aqui para não ser esquecido em um eventual uso comercial futuro.
- Ver `document/governanca-dados-e-vies.md` para a discussão completa (idioma, época,
  viés de fonte).
