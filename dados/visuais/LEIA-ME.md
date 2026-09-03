# Dados Visuais — Imagens de ECG (Visão Computacional)

Conjunto da **Parte 3 (Dados Visuais / VC)** do projeto CardioIA.

- **120 imagens** de eletrocardiograma de **12 derivações** (`ecg_images/*.png`)
- **Formato:** PNG, ~1.320 × 800 px, traçado clínico padrão (25 mm/s, 10 mm/mV) sobre grade "papel de ECG"
- **Rótulos:** [`labels.csv`](labels.csv) — uma linha por imagem
- **Amostras** para visualização rápida: [`amostras/`](amostras/) (2 por classe)
- **Reprodução:** [`gerar_imagens_ecg.py`](gerar_imagens_ecg.py)

## Origem

Imagens **renderizadas a partir de sinais reais** da base **PTB-XL** (21.799 registros de 18.869 pacientes,
Physikalisch-Technische Bundesanstalt, Alemanha), distribuída pelo PhysioNet sob
licença **Creative Commons Attribution 4.0 (CC BY 4.0)**.

> São dados **reais** (não simulados): cada imagem corresponde a um ECG de 10 segundos
> de um paciente real, com laudo elaborado por cardiologista. O que o script faz é
> apenas **plotar** o sinal digital no formato visual em que um médico o lê.

Wagner et al. (2020), *PTB-XL, a large publicly available electrocardiography dataset*,
Scientific Data 7:154. <https://physionet.org/content/ptb-xl/>

## Composição (amostragem balanceada e reprodutível, `seed=42`)

| Superclasse | Rótulo `labels.csv` | Imagens | O que representa |
|---|---|---|---|
| ECG normal | `NORM` | 24 | Sem anormalidade diagnóstica |
| Infarto do miocárdio | `MI` | 24 | Ondas Q patológicas, perda de progressão de R |
| Alteração de ST/T | `STTC` | 24 | Infra/supradesnível de ST, inversão de T (isquemia, sobrecarga) |
| Distúrbio de condução | `CD` | 24 | Bloqueios de ramo, bloqueios fasciculares, WPW |
| Hipertrofia | `HYP` | 24 | Sobrecarga de câmaras (critérios de voltagem) |
| **Total** | | **120** | |

Balanceamento adicional: **60 exames masculinos / 60 femininos**; idades de 2 a 89
anos (média ≈ 62), distribuídas dentro de cada classe. Somente registros com **laudo
validado por cardiologista** e **uma única superclasse dominante** foram usados, para
que o rótulo da imagem seja limpo.

> O mínimo exigido pela atividade são **100 imagens de um tipo de exame**. Foram
> entregues **120 ECGs**, já **rotulados por achado diagnóstico** — prontos para
> classificação supervisionada, não apenas para inspeção visual.

## Colunas de `labels.csv`

| Coluna | Descrição |
|---|---|
| `arquivo` | Caminho relativo da imagem (`ecg_images/ECG_00001_NORM.png`) |
| `ecg_id` | Identificador do registro na PTB-XL |
| `superclasse` / `superclasse_pt` | Rótulo diagnóstico (código e em português) |
| `scp_codes` | Códigos SCP-ECG originais com grau de certeza (0–100) |
| `idade` | Idade do paciente (anos) |
| `sexo` | `M` / `F` |
| `eixo_cardiaco` | Eixo elétrico quando informado (`LAD`, `RAD`, `MID`, …) |
| `laudo_ptbxl` | Laudo textual original (alemão/inglês) — ponte com a Parte 2 (NLP) |

## Como essas imagens serão analisadas por Visão Computacional

| Técnica de VC | Aplicação neste conjunto | Para que serve no CardioIA |
|---|---|---|
| **Pré-processamento / detecção de bordas** (Canny, Sobel, limiarização) | Isolar o traçado preto da grade rosa; segmentar cada uma das 12 derivações | Digitalizar ECGs em papel — muitos serviços do SUS ainda arquivam ECG impresso |
| **Detecção de padrões / picos** | Localizar complexos QRS, medir intervalo RR, estimar frequência cardíaca e ritmo direto da imagem | Alimentar o monitoramento contínuo (Fase 3) e a previsão de crises (Fase 6) |
| **Classificação supervisionada (CNN)** | Treinar `imagem → {NORM, MI, STTC, CD, HYP}` usando `labels.csv` | Núcleo do **diagnóstico assistido por imagem (Fase 4)** |
| **Reconhecimento de anomalias** | Sinalizar supradesnível de ST (candidato a IAM), QRS alargado (bloqueio), baixa voltagem | Triagem automática e priorização de fila |
| **Grad-CAM / mapas de saliência** | Mostrar em qual derivação e trecho o modelo "olhou" | **Explicabilidade** — exigência ética para apoio a decisão clínica |
| **Aumento de dados** (ruído, deriva de linha de base, rotação leve) | Simular ECGs de menor qualidade | Robustez a aparelhos e condições reais de captura |

### Por que isso importa para IA em saúde

- O ECG é o exame cardiológico **mais disponível, barato e rápido** — e altamente
  padronizado, o que o torna ideal para visão computacional.
- Interpretação de ECG exige treino; em muitas unidades **não há cardiologista de
  plantão**. Um classificador confiável funciona como **segunda opinião** e como
  **ordenador de fila** (quem precisa ser visto primeiro).
- Erros têm custo assimétrico: **não** identificar um infarto é muito pior do que um
  falso alarme. Ter rótulos por classe desde já permite otimizar sensibilidade e medir
  esse trade-off.

## Limitações e viés (resumo — ver `docs/governanca-dados-e-vies.md`)

- **População alemã**, equipamento e prática dos anos 1989–1996: a distribuição de
  achados e a "aparência" do traçado podem não representar a população brasileira.
- **HYP** é a classe mais rara na PTB-XL; aqui foi forçada a 24 por balanceamento, mas
  com menos diversidade de casos subjacentes.
- Laudo original em **alemão/inglês** — atenção ao usar `laudo_ptbxl` em NLP em
  português.
- Rótulo em **nível de superclasse**: dentro de `CD`, por exemplo, convivem BRE, BRD e
  WPW, que são muito diferentes entre si.
