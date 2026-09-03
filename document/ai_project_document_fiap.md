<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="30%" height="30%">

# AI Project Document — Módulo 1 — FIAP

## CardioIA — A Nova Era da Cardiologia Inteligente

#### Guilherme Yamada Dantas — RM rm568506

---

## Sumário

[1. Introdução](#c1)
[2. Visão Geral do Projeto](#c2)
[3. Desenvolvimento do Projeto](#c3)
[4. Resultados e Avaliações](#c4)
[5. Conclusões e Trabalhos Futuros](#c5)
[6. Referências](#c6)
[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

A IA aplicada à saúde é um dos segmentos de maior crescimento do setor, com atuação
**internacional** e forte presença em cardiologia — a área médica com maior volume de
dados estruturados e sinais padronizados (ECG, pressão, frequência cardíaca). As
atividades típicas incluem triagem e priorização de atendimento, diagnóstico assistido
por imagem e sinal, monitoramento contínuo por dispositivos vestíveis, assistentes
conversacionais para acompanhamento e modelos preditivos de eventos agudos. As doenças
cardiovasculares são a **principal causa de morte no mundo** (~17,9 milhões de óbitos/
ano, 31% do total, segundo a OPAS/OMS), o que torna ganhos marginais de sensibilidade
diagnóstica altamente relevantes em termos de vidas.

### 1.1.2. Descrição da Solução Desenvolvida

O **CardioIA** é uma plataforma acadêmica que simula o ecossistema de uma cardiologia
moderna, integrando dados clínicos, ML, Visão Computacional, IoT e agentes
inteligentes ao longo de 7 fases. **Esta entrega (Fase 1)** corresponde à camada de
**dados**: a coleta, organização, documentação e análise crítica das três bases que
alimentarão todos os módulos seguintes — dados numéricos de pacientes, corpus textual
de saúde cardiovascular e imagens de ECG rotuladas — com governança e tratamento de
viés como critérios de qualidade.

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

**Objetivo geral:** preparar a fundação de dados do CardioIA.

**Objetivos específicos da Fase 1:**
1. Obter um dataset numérico clínico real (≥ 100 pacientes) com variáveis de risco
   cardiovascular, documentado e com alvo definido.
2. Reunir um corpus textual (≥ 2 textos) sobre doença cardiovascular, com fontes e
   licenças rastreáveis e proposta de uso em NLP.
3. Reunir um conjunto de imagens (≥ 100) de um exame cardiológico, com proposta de uso
   em Visão Computacional — e, como diferencial, rotuladas por achado.
4. Documentar proveniência, decisões de limpeza, reprodutibilidade e vieses.

## 2.2. Público-Alvo

- **Direto (fases seguintes):** o próprio grupo/aluno, que consumirá estes dados em
  notebooks de ML, NLP e VC.
- **Final (visão do produto):** cardiologistas e equipes de triagem (apoio à decisão),
  gestores de unidades de saúde (priorização de fila) e pacientes cardíacos em
  acompanhamento remoto.

## 2.3. Metodologia

Método **PBL (Project Based Learning)** da FIAP, com abordagem de engenharia de dados:

1. **Descoberta de fontes** — busca em repositórios públicos (UCI, PhysioNet), bases
   científicas (SciELO), órgãos de saúde (OPAS/OMS) e acervos de domínio público
   (Project Gutenberg).
2. **Ingestão reprodutível** — um script Python por tipo de dado, versionado, que
   baixa e transforma os dados brutos.
3. **Limpeza documentada** — cada decisão registrada em dicionário de dados e
   comentários de código.
4. **Análise exploratória** — estatísticas descritivas automáticas e leitura crítica
   dos desbalanços.
5. **Governança** — licenciamento, anonimização, checklist de viés.

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

| Categoria | Ferramentas |
|---|---|
| Linguagem | Python 3.12 |
| Manipulação de dados | pandas, numpy |
| Sinais e imagem | wfdb (leitura PTB-XL), scipy (filtros), matplotlib (render do ECG) |
| Coleta | curl, urllib |
| Versionamento | Git / GitHub, GitHub Releases (distribuição do pacote) |
| Documentação | Markdown |

## 3.2. Modelagem e Algoritmos

Nesta fase **não há treinamento de modelos** — o produto é a base de dados. As
estruturas foram desenhadas para as tarefas de IA das próximas fases:

- **Numérico:** alvo binário (`doenca_cardiaca`) e ordinal (`diagnostico_num`) →
  classificação supervisionada (Fase 2).
- **Textual:** corpus multilíngue e multi-registro → NER de sintomas, classificação de
  tópicos, RAG (Fases 2 e 5).
- **Visual:** 120 ECGs rotulados em 5 superclasses → CNN de classificação e
  reconhecimento de anomalias (Fase 4).

## 3.3. Treinamento e Teste

Não aplicável nesta fase. Foram produzidos **artefatos de avaliação de dados**:
`dados/numericos/analise_exploratoria.md` (distribuições, ausência, prevalência por
subgrupo) e `dados/visuais/labels.csv` (rótulos e metadados por imagem), que serão a
base para as divisões treino/validação/teste estratificadas nas próximas fases.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

| Meta | Mínimo | Entregue |
|---|---|---|
| Dataset numérico | 100 linhas | **920 pacientes**, 25 colunas, real, com EDA |
| Textos | 2 | **4 textos**, 2 idiomas, ~93 mil palavras |
| Imagens | 100 | **120 ECGs** de 12 derivações, rotulados, balanceados |
| Governança/viés | citar conceitos | documento dedicado + checklist + EDA de subgrupos |

Principais achados analíticos: forte **viés de seleção institucional** (Suíça 93,5% de
doentes), **viés de sexo** (79% homens; recall potencialmente menor em mulheres) e
**ausência não aleatória** em variáveis de cateterismo (`ca` 66%, `thal` 53%).

## 4.2. Feedback dos Usuários

Não aplicável nesta fase (sem interface com usuário final). O "usuário" desta entrega é
a própria equipe nas fases seguintes; o feedback esperado é a facilidade de carregar os
dados em Colab/Jupyter — por isso o notebook `notebooks/00_carregar_dados.ipynb` e os scripts de ingestão.

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

A Fase 1 atingiu todos os objetivos: três bases reais, acima do mínimo, rastreáveis,
reprodutíveis e com viés documentado.

**Pontos fortes:** dados reais nas três frentes; rótulos prontos em numérico e visual;
governança tratada como requisito, não como texto de conclusão.

**Pontos a melhorar / plano de ação:**
1. **Representatividade local** — incorporar dados brasileiros (DATASUS, diretrizes
   SBC, hospitais parceiros) na Fase 2.
2. **Corpus PT** — aumentar a proporção de textos em português e incluir linguagem
   leiga (voz do paciente) para a Fase 5.
3. **Granularidade dos rótulos de imagem** — descer de superclasse para diagnóstico
   específico quando o volume permitir.
4. **Cartão de modelo e auditoria de fairness** — assim que houver o primeiro modelo.

# <a name="c6"></a>6. Referências

- Janosi, A., Steinbrunn, W., Pfisterer, M., Detrano, R. (1989). *Heart Disease*. UCI
  Machine Learning Repository. https://doi.org/10.24432/C52P4X
- Wagner, P. et al. (2020). *PTB-XL, a large publicly available electrocardiography
  dataset*. Scientific Data 7:154. https://doi.org/10.1038/s41597-020-0495-6
- Goldberger, A. et al. (2000). *PhysioBank, PhysioToolkit, and PhysioNet*.
  Circulation 101(23):e215–e220.
- Evora, P. R. B., Nather, J. C., Rodrigues, A. J. (2014). *Prevalência das Doenças
  Cardíacas Ilustrada em 60 Anos dos Arquivos Brasileiros de Cardiologia*. Arq. Bras.
  Cardiol. 102(1):9-16. https://doi.org/10.5935/abc.20140001
- OPAS/OMS. *Doenças cardiovasculares*. https://www.paho.org/pt/topicos/doencas-cardiovasculares
- Bruce, J. M. (1901). *The Lettsomian Lectures on Diseases and Disorders of the Heart
  and Arteries*. Project Gutenberg #43780.
- Warfield, L. M. (1912). *Arteriosclerosis and Hypertension*. Project Gutenberg #37675.

# <a name="c7"></a>Anexos

- **Anexo A** — `dados/numericos/dicionario_de_dados.md`: dicionário completo do dataset numérico.
- **Anexo B** — `dados/numericos/analise_exploratoria.md`: EDA automática.
- **Anexo C** — `assets/textos/FONTES_E_LICENCAS.md`: fontes, licenças e plano de uso em NLP.
- **Anexo D** — `dados/visuais/LEIA-ME.md` e `labels.csv`: descrição e rótulos das imagens.
- **Anexo E** — `document/governanca-dados-e-vies.md`: análise de governança e viés.
