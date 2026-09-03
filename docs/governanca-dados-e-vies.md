# Governança de Dados e Viés — CardioIA Fase 1

> Esta fase constrói a **base de dados** do CardioIA. Governança e viés não são um
> apêndice: são critério de qualidade da base. Um dado enviesado ou sem rastreabilidade
> contamina todas as 7 fases seguintes.

---

## 1. Princípios de governança adotados nesta fase

| Princípio | Como foi aplicado no repositório |
|---|---|
| **Proveniência / rastreabilidade** | Toda fonte tem URL, DOI/ID, ano e licença registrados (`dados/*/`). Os dados brutos ficam versionados em `dados/numericos/brutos/`. |
| **Reprodutibilidade** | Os três conjuntos são regeneráveis por script (`preparar_dados_numericos.py`, `preparar_textos.py`, `gerar_imagens_ecg.py`). Nada foi editado à mão. |
| **Licenciamento explícito** | UCI Heart Disease e PTB-XL são **CC BY 4.0**; textos são domínio público, exceto o artigo SciELO (**CC BY-NC 3.0** — uso não comercial). Registrado em `CITACOES.md` e nos LEIA-ME. |
| **Minimização e anonimização** | Nenhum dado identifica pacientes. Identificadores são sintéticos; idades > 89 da PTB-XL (anonimizadas como "300") foram removidas da amostra. |
| **Transparência de transformações** | Cada decisão de limpeza (ex.: `colesterol = 0` → ausente) está documentada no dicionário de dados e comentada no código. |
| **Sem imputação silenciosa** | Valores ausentes são mantidos explícitos, para que a estratégia de tratamento seja uma decisão consciente das próximas fases. |
| **Adequação à LGPD** | Dados são públicos, anonimizados e de finalidade acadêmica declarada. Se o CardioIA usar dados de pacientes reais no futuro, será necessário base legal, consentimento e DPIA. |

---

## 2. Viés no dataset numérico (UCI Heart Disease)

Números extraídos de `dados/numericos/analise_exploratoria.md`.

### 2.1. Viés de seleção por instituição
| Base | Pacientes | % com doença | Idade média |
|---|---|---|---|
| Cleveland (EUA) | 303 | 45,9% | 54,4 |
| Hungria | 294 | 36,1% | 47,8 |
| Suíça | 123 | **93,5%** | 55,3 |
| V.A. Long Beach (EUA) | 200 | 74,5% | 59,4 |

A base da Suíça é composta quase só de doentes (hospital de referência terciária). Um
modelo treinado no conjunto todo **aprende a instituição junto com a doença**. Se a
coluna `origem` vazar para o modelo, ele "acerta" pelo motivo errado.
**Mitigação:** validação estratificada por `origem`; nunca usar `origem` como preditor;
reportar métricas por base.

### 2.2. Viés de sexo
- **78,9% dos pacientes são homens**; mulheres são 21,1%.
- Prevalência de doença: **63,2% (homens)** vs **25,8% (mulheres)** — parte é
  epidemiologia real, parte é viés de encaminhamento (a angina "atípica" feminina é
  historicamente subvalorizada).
- Risco de IA: menos dados femininos → modelo menos sensível em mulheres →
  **subdiagnóstico** exatamente no grupo já subdiagnosticado na prática.
**Mitigação:** avaliar sensibilidade/recall separadamente por sexo; considerar
reponderação; não aceitar acurácia global como métrica única.

### 2.3. Viés de dados ausentes (não aleatório)
| Coluna | % ausente |
|---|---|
| `ca` (vasos na fluoroscopia) | 66,4% |
| `thal` (cintilografia) | 52,8% |
| `slope` | 33,6% |
| `chol` | 22,0% |

A ausência **depende da instituição** (Hungria e Suíça quase não têm cateterismo/
cintilografia). Descartar linhas com ausência = descartar quase toda a Europa e manter
o perfil de Cleveland. Imputar pela média mistura populações diferentes.
**Mitigação:** tratar ausência como informação; modelos que a toleram nativamente;
análise de sensibilidade com e sem as colunas mais faltantes.

### 2.4. Viés histórico e de contexto
Dados de **1988**, critérios diagnósticos e limiares (colesterol, PA) da época,
sistemas de saúde dos EUA/Europa. **Não** representam a população brasileira, o SUS,
nem a prática de 2026.
**Mitigação:** usar como base de prototipagem; planejar coleta de dados locais
(DATASUS, hospitais parceiros) nas próximas fases.

---

## 3. Viés no conjunto de imagens (PTB-XL)

- **População alemã**, coleta 1989–1996, aparelhos Schiller AG. Morfologia do traçado,
  prevalência de achados e até o "ruído" são específicos desse contexto.
- **Classe `HYP` é rara** na base original; ao forçar 24 exemplos por classe,
  ganhamos balanceamento mas reduzimos a diversidade de casos de hipertrofia.
- **Rótulo em superclasse:** `CD` reúne bloqueios de ramo, fasciculares e WPW —
  entidades com aparência e significado clínico distintos. Modelos treinados só na
  superclasse terão explicabilidade limitada.
- **Laudo textual em alemão/inglês:** viés de idioma se `laudo_ptbxl` for usado direto
  em NLP em português.
- **Viés de digitalização:** nossas imagens são plotagens limpas de sinal digital.
  ECG real digitalizado de papel tem sombra, dobras, rotação. Modelos treinados só no
  "limpo" degradam no mundo real → necessidade de *data augmentation*.

---

## 4. Viés no corpus textual

| Eixo | Viés | Efeito potencial | Mitigação nas próximas fases |
|---|---|---|---|
| **Idioma** | 2 de 4 textos em inglês | Vocabulário clínico PT sub-representado | Priorizar fontes PT (SciELO, BVS, diretrizes SBC, DATASUS) |
| **Época** | 2 textos de 1901–1912 | Termos obsoletos (*"tobacco heart"*), condutas superadas | Usar como corpus de contraste, não como fonte de verdade clínica |
| **Registro** | Divulgação (OPAS) vs acadêmico (SciELO) vs histórico | Estilos muito diferentes | Bom para robustez; ruim se um único estilo for assumido como padrão |
| **Autoria** | Fontes institucionais e médicas | Ausência da "voz do paciente" (fóruns, redes) | Coletar linguagem leiga para o chatbot da Fase 5 |
| **Escopo geográfico** | OMS global, autores brasileiros e britânicos | Pouca especificidade regional | Complementar com epidemiologia local |

---

## 5. Riscos de IA em cardiologia e como esta base os endereça

| Risco | Origem no dado | O que já fizemos | O que fica para as próximas fases |
|---|---|---|---|
| **Subdiagnóstico em subgrupos** | Sexo, idade, instituição desbalanceados | Medimos e documentamos os desbalanços; balanceamos as imagens por sexo e classe | Métricas por subgrupo obrigatórias; *fairness constraints* |
| **Automação enviesada ("o modelo aprende o hospital")** | `origem` correlacionada ao alvo | Proibimos `origem` como preditor; recomendamos validação estratificada | Testes de vazamento; auditoria de features |
| **Falsa confiança / caixa-preta** | — | Escolhemos ECG (exame explicável) e mantivemos rótulos interpretáveis | Grad-CAM, cartões de modelo, revisão médica |
| **Erro com custo assimétrico** (perder um IAM) | Prevalência e rótulos | Rótulos por classe permitem otimizar sensibilidade | Definir limiares com cardiologista; priorizar recall de `MI`/`STTC` |
| **Perda de privacidade** | Dados de saúde | Só dados públicos, anonimizados, licenciados | DPIA e base legal antes de qualquer dado real de paciente |
| **Deriva de dados** (*data drift*) | Bases de 1988–1996 | Documentada a defasagem temporal/geográfica | Monitoramento de distribuição; recoleta periódica |

---

## 6. Checklist de governança — status da Fase 1

- [x] Toda fonte tem licença identificada e compatível com uso acadêmico
- [x] Dados brutos versionados e transformações 100% reprodutíveis por script
- [x] Nenhum dado pessoal identificável no repositório
- [x] Desbalanços de sexo, idade e instituição medidos e documentados
- [x] Valores ausentes preservados e explicados (sem imputação silenciosa)
- [x] Riscos de viés mapeados com mitigação proposta para as fases seguintes
- [ ] Dados representativos da população-alvo (Brasil/SUS) — **pendente, Fase 2+**
- [ ] Cartão de modelo e auditoria de fairness — **pendente, quando houver modelo**
