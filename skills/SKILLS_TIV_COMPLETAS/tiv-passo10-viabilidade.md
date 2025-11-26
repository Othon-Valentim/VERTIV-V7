---
name: "tiv-passo10-viabilidade"
version: "1.0"
description: "ProjeÃ§Ãµes financeiras defensÃ¡veis via DRE, Fluxo de Caixa e AnÃ¡lise de CenÃ¡rios para decisÃ£o Go/Hold/No-Go"
author: "Claude + Othon"
created: "2025-01-12"
updated: "2025-01-12"
tags: ["tiv", "imobiliario", "viabilidade", "financeiro", "fcd", "dre"]
priority: "CRÃTICO"
---

# SKILL: Passo 10 â€” Viabilidade Financeira, CenÃ¡rios e DecisÃ£o

## 1. Objetivo e Contexto

### PropÃ³sito
Transformar os resultados dos Passos 6â€“9 em **projeÃ§Ãµes financeiras defensÃ¡veis**, com **mÃºltiplos cenÃ¡rios** e **anÃ¡lise de sensibilidade**, para emitir uma **decisÃ£o executiva** (Go/Hold/No-Go) fundamentada em dados rastreÃ¡veis e metodologia rigorosa.

### Momento no Fluxo TIV
**Passo 10 de 10** â€” Momento final de **cristalizaÃ§Ã£o da decisÃ£o**. ApÃ³s validar demanda (P6), oferta (P7), absorÃ§Ã£o (P8) e convalidaÃ§Ã£o (P9), este passo consolida **TODOS os nÃºmeros** em um modelo financeiro que responde: **VALE A PENA?**

### PrincÃ­pio Fundamental
> **"A batalha Ã© defender VENDAS, nÃ£o custos. Custos vocÃª controla; vendas, o mercado valida."**  
> â€” Othon Valentim, TIV 4.0

**PROIBIÃ‡ÃƒO ABSOLUTA:** ProjeÃ§Ãµes sem lastro em **fontes oficiais nomeadas** (IBGE/SIDRA, CAGED, Banco Central) e sem integraÃ§Ã£o rigorosa com P6â€“P9. **"Chute" (cÃ¡lculo heurÃ­stico) Ã© inadmissÃ­vel no Passo 10.**

---

## 2. Quando Acionar

### Triggers ObrigatÃ³rios
âœ… **Passos 6, 7, 8 e 9 concluÃ­dos** com outputs documentados  
âœ… DecisÃ£o preliminar de **avanÃ§ar para anÃ¡lise financeira** (terreno passou no Garimpo e VocaÃ§Ã£o)  
âœ… Necessidade de **defender viabilidade** em comitÃª de investimento, sÃ³cios ou financiadores  

### PrÃ©-requisitos CrÃ­ticos
- **P6 (Demanda):** PreÃ§o de stand calculado, demanda pagante por faixa/H3, razÃ£o Demanda:Oferta
- **P7 (Oferta):** Oferta pulverizada, lanÃ§amentos, futura (pipeline), IVV/VSO de referÃªncia
- **P8 (AbsorÃ§Ã£o):** Velocidade de vendas por faixa e por H3 (positiva ou negativa)
- **P9 (ConvalidaÃ§Ã£o):** EvidÃªncias de intenÃ§Ã£o de compra (cliente oculto, corretores, pesquisa)

### Red Flags para NÃƒO Executar P10
ðŸš« AbsorÃ§Ã£o negativa em todos os cenÃ¡rios (< -20%)  
ðŸš« RazÃ£o Demanda:Oferta < 4:1 sem validaÃ§Ã£o robusta  
ðŸš« RestriÃ§Ãµes legais impeditivas nÃ£o resolvidas (P5)  
ðŸš« AusÃªncia de dados de mercado confiÃ¡veis (sem IBGE, sem pesquisa)  

---

## 3. Framework/Metodologia

### Estrutura de AnÃ¡lise (5 Camadas)

#### **Camada 1: Premissas MacroeconÃ´micas (O10-1)**
**Objetivo:** Parametrizar o "Brasil Real" â€” taxas, Ã­ndices e tributos que afetam o projeto.

**Componentes:**
1. **Taxas de Juros**
   - Taxa anual (a.a.) OU mensal (a.m.) â€” conversÃ£o automÃ¡tica
   - FÃ³rmula: `Taxa mensal = (1 + Taxa anual)^(1/12) - 1`
   - Exemplo: 15% a.a. = 1,17% a.m.

2. **Ãndices de CorreÃ§Ã£o**
   - INCC (obras)
   - CUB (custo unitÃ¡rio bÃ¡sico)
   - IPCA (inflaÃ§Ã£o geral)
   - IGP-M (contratos)
   - Base: sÃ©ries histÃ³ricas Ãºltimos 12-24 meses

3. **Impostos e Taxas**
   - ITBI: 2% sobre valor de escritura
   - Registro/Escritura: 1% sobre valor do imÃ³vel
   - ComissÃ£o Vendas: 4-6% sobre receita
   - Taxa AdministraÃ§Ã£o: 1-2% sobre receita
   - Impostos Operacionais: 3-5% sobre receita (depende do regime tributÃ¡rio)

4. **ParÃ¢metros EstratÃ©gicos**
   - Horizonte de projeÃ§Ã£o: 24-48 meses (tÃ­pico)
   - WACC do projeto: custo de capital ponderado (15-25% a.a.)
   - Hurdle rate: WACC + prÃªmio de risco (3-5 p.p.)

**Fontes ObrigatÃ³rias:**
- Juros: Banco Central (Selic, TR) â€” https://www.bcb.gov.br/
- INCC/CUB: FGV / Sinduscon
- IPCA/IGP-M: IBGE, FGV
- Tributos: CÃ³digo TributÃ¡rio Municipal + Federal

---

#### **Camada 2: Plano de Vendas Ã— AbsorÃ§Ã£o (O10-2)**
**Objetivo:** Transformar a **AbsorÃ§Ã£o** (P8) em **cronograma mensal de receitas**.

**LÃ³gica de DistribuiÃ§Ã£o:**

**Input Principal:** AbsorÃ§Ã£o por faixa e por H3 (output do P8)

**MÃ©todo de ProjeÃ§Ã£o:**
1. **AbsorÃ§Ã£o Positiva (> 0):**
   - Distribuir vendas em curva **linear**, **S** ou **manual**
   - Exemplo: AbsorÃ§Ã£o = 120 un/ano â†’ 10 un/mÃªs (linear)
   - Usar Fator 4:1 (conservadorismo TIV) se validaÃ§Ã£o robusta
   - Usar Fator 10:1 se SEM validaÃ§Ã£o (P9 fraco)

2. **AbsorÃ§Ã£o Negativa (< 0):**
   - CenÃ¡rio CONSERVADOR obrigatÃ³rio
   - Ajustar velocidade de vendas (-20% a -40%)
   - Considerar aumento de prazo de projeto

3. **Receita Bruta Ã— LÃ­quida:**
   - **Bruta:** PreÃ§o de stand Ã— Unidades vendidas/mÃªs
   - **LÃ­quida:** Bruta - ComissÃ£o - Impostos sobre vendas

**Exemplo PrÃ¡tico (Leopoldina-MG):**
```
Faixa 2SM-3SM: 80 unidades
AbsorÃ§Ã£o P8: +15% (positiva)
PreÃ§o stand: R$ 180.000
Plano: 24 meses (curva S)

DistribuiÃ§Ã£o:
Meses 1-6: 2 un/mÃªs (ramp-up)
Meses 7-18: 5 un/mÃªs (pico)
Meses 19-24: 3 un/mÃªs (cauda)

Receita mensal pico: 5 Ã— R$ 180k = R$ 900k bruto
Receita lÃ­quida: R$ 900k - 5% comissÃ£o - 3% impostos = R$ 828k
```

**IntegraÃ§Ã£o com P8:**
- Se P8 indica saturaÃ§Ã£o em H3 especÃ­ficos â†’ reduzir velocidade nessa sub-regiÃ£o
- Se P8 mostra demanda concentrada â†’ antecipar lanÃ§amento de fases

---

#### **Camada 3: Fluxo de Caixa e DRE (O10-3)**
**Objetivo:** Consolidar **receitas**, **custos** e **despesas** em fluxo mensal â†’ calcular **VPL, TIR, Payback**.

**Estrutura do Fluxo:**

**RECEITAS**
- Entrada (sinal): 10-30% do preÃ§o
- IntermediÃ¡rias: 20-40% durante obra
- Finais (chaves): 40-60% na entrega
- FÃ³rmula PRICE/SAC integrada (do P6)

**CUSTOS (CAPEX)**
- **Terreno:** Valor de aquisiÃ§Ã£o + ITBI + Registro
- **UrbanizaÃ§Ã£o/Obra:** 
  - CUB Ã— Ãrea construÃ­da Ã— PadrÃ£o
  - Infraestrutura (Ã¡gua, esgoto, energia, vias)
  - Paisagismo, equipamentos comunitÃ¡rios
- **Projetos e AprovaÃ§Ãµes:** 2-5% do CAPEX
- **ContingÃªncia:** 5-10% do CAPEX total

**DESPESAS (OPEX)**
- Marketing e Vendas: 2-4% da receita
- AdministraÃ§Ã£o: 1-2% da receita
- JurÃ­dico e Cartorial: 1-2% da receita
- Financeiras: Juros sobre capital de giro

**IMPOSTOS**
- ISS (obras): 2-5%
- PIS/COFINS: 3,65% (lucro presumido) ou 9,25% (lucro real)
- IRPJ/CSLL: 4,8% (presumido) ou 34% sobre lucro (real)

**Indicadores de Retorno:**
1. **VPL (Valor Presente LÃ­quido):**
   - FÃ³rmula: `VPL = Î£ [FC_t / (1+WACC)^t]`
   - DecisÃ£o: VPL > 0 â†’ viÃ¡vel
   - Sensibilidade: VPL prÃ³ximo de zero exige ajustes

2. **TIR (Taxa Interna de Retorno):**
   - Taxa que zera o VPL
   - DecisÃ£o: TIR > Hurdle Rate â†’ viÃ¡vel
   - TÃ­pico: TIR > 18-22% a.a. para projetos imobiliÃ¡rios

3. **ROE (Return on Equity):**
   - **Indicador prioritÃ¡rio TIV**
   - FÃ³rmula: `ROE = Lucro LÃ­quido / PatrimÃ´nio LÃ­quido`
   - DecisÃ£o: ROE > 25% â†’ excelente | ROE < 15% â†’ revisar

4. **Payback:**
   - Tempo para recuperar investimento inicial
   - DecisÃ£o: Payback < 50% do prazo total â†’ bom
   - Exemplo: Projeto de 36 meses â†’ Payback ideal < 18 meses

**Exemplo de DRE Mensal (MÃªs 12):**
```
RECEITAS
  Vendas (5 un Ã— R$ 180k)          R$ 900.000
  (-) ComissÃ£o (5%)                R$ (45.000)
  (-) Impostos s/ Vendas (3%)      R$ (27.000)
  = Receita LÃ­quida                R$ 828.000

CUSTOS
  Obra (CUB Ã— mÂ²)                  R$ (350.000)
  Infraestrutura                   R$ (80.000)
  Projetos                         R$ (15.000)
  = Custo Total                    R$ (445.000)

DESPESAS
  Marketing                        R$ (18.000)
  AdministraÃ§Ã£o                    R$ (9.000)
  JurÃ­dico                         R$ (5.000)
  = Despesas Totais                R$ (32.000)

LUCRO OPERACIONAL                  R$ 351.000

(-) Impostos sobre Lucro (15%)     R$ (52.650)

= LUCRO LÃQUIDO                    R$ 298.350
```

---

#### **Camada 4: CenÃ¡rios MÃºltiplos**
**Objetivo:** Testar **robustez** do projeto sob diferentes condiÃ§Ãµes de mercado.

**CenÃ¡rios ObrigatÃ³rios (MÃ­nimo 3):**

**1. CENÃRIO BASE (Realista)**
- AbsorÃ§Ã£o: conforme P8 (sem ajustes)
- PreÃ§o: preÃ§o de stand do P6
- Velocidade: 100% da projeÃ§Ã£o
- Juros: taxa atual
- Resultado esperado: **VPL > 0, TIR > Hurdle**

**2. CENÃRIO CONSERVADOR (Stress)**
- AbsorÃ§Ã£o: -20% da velocidade
- PreÃ§o: -5% (pressÃ£o competitiva)
- Velocidade: 80% da projeÃ§Ã£o
- Juros: +2 p.p.
- Prazo: +6 meses
- Resultado esperado: **VPL â‰¥ 0 (mÃ­nimo)**

**3. CENÃRIO OTIMISTA (Blue Sky)**
- AbsorÃ§Ã£o: +20% da velocidade
- PreÃ§o: +5% (demanda aquecida)
- Velocidade: 120% da projeÃ§Ã£o
- Juros: -1 p.p.
- Prazo: -3 meses
- Resultado esperado: **VPL >> 0, TIR > 25%**

**AnÃ¡lise de CenÃ¡rios:**
```
MÃ©trica         BASE      CONSERV    OTIMISTA
VPL (R$ mi)     2,5       0,8        4,2
TIR (% a.a.)    22%       16%        28%
ROE (%)         28%       18%        38%
Payback (m)     18        24         14
```

**DecisÃ£o por CenÃ¡rios:**
- **Go:** VPL > 0 em BASE + CONSERVADOR
- **Hold:** VPL > 0 sÃ³ em BASE; ajustar preÃ§o/mix/praÃ§a
- **No-Go:** VPL < 0 em BASE e CONSERVADOR

---

#### **Camada 5: Sensibilidade 2Ã—2 (O10-4)**
**Objetivo:** Identificar **variÃ¡veis crÃ­ticas** que mais impactam o resultado.

**Matriz de Sensibilidade (PreÃ§o Ã— Velocidade):**

**VariaÃ§Ã£o de PreÃ§o:** -10%, -5%, 0%, +5%, +10%  
**VariaÃ§Ã£o de Velocidade:** -40%, -20%, 0%, +20%, +40%

**Exemplo de Matriz (VPL em R$ milhÃµes):**

```
Velocidade â†“ PreÃ§o â†’  | -10%  | -5%   | BASE  | +5%   | +10%
-40%                  | (1,2) | (0,5) |  0,2  |  0,9  |  1,6
-20%                  | (0,3) |  0,5  |  1,3  |  2,1  |  2,9
BASE (0%)             |  0,8  |  1,7  |  2,5  |  3,4  |  4,2
+20%                  |  1,9  |  2,9  |  3,8  |  4,7  |  5,6
+40%                  |  3,1  |  4,1  |  5,1  |  6,1  |  7,1
```

**Insights da Matriz:**
- **Ãrea Verde:** VPL > 0 â†’ zona de viabilidade
- **Ãrea Vermelha:** VPL < 0 â†’ zona de risco
- **Ponto CrÃ­tico:** Onde VPL = 0
- **Elasticidade:** Velocidade afeta mais que preÃ§o (em geral)

**Alavancas de Ajuste:**
- Se sensÃ­vel a **preÃ§o** â†’ revisar P6, reposicionar produto
- Se sensÃ­vel a **velocidade** â†’ reforÃ§ar marketing, ajustar absorÃ§Ã£o (P8)
- Se sensÃ­vel a **prazo** â†’ otimizar cronograma de obra
- Se sensÃ­vel a **juros** â†’ buscar funding mais barato

---

## 4. Inputs NecessÃ¡rios

### Inputs ObrigatÃ³rios (De Outros Passos)

**Do Passo 6 (Demanda):**
- âœ… PreÃ§o de stand mÃ¡ximo por faixa de renda
- âœ… Demanda pagante por faixa e por H3
- âœ… ParÃ¢metros de financiamento (entrada, prazo, taxa)
- âœ… RazÃ£o Demanda:Oferta (4:1 ou 10:1)

**Do Passo 7 (Oferta):**
- âœ… Oferta pulverizada (estoque atual)
- âœ… Oferta de lanÃ§amentos (Ãºltimos 12-24 meses)
- âœ… Oferta futura (pipeline, projetos aprovados)
- âœ… IVV (Ãndice de Velocidade de Vendas) e VSO de referÃªncia

**Do Passo 8 (AbsorÃ§Ã£o):**
- âœ… Taxa de absorÃ§Ã£o por faixa de renda
- âœ… Taxa de absorÃ§Ã£o por H3 (sub-regiÃ£o)
- âœ… Sinal da absorÃ§Ã£o (positivo/negativo)
- âœ… Magnitude da absorÃ§Ã£o (%, unidades/mÃªs)

**Do Passo 9 (ConvalidaÃ§Ã£o):**
- âœ… EvidÃªncias de intenÃ§Ã£o de compra (cliente oculto, pesquisa)
- âœ… Score de confianÃ§a da demanda (0-100)
- âœ… Ajuste do Fator 4:1 ou 10:1 conforme validaÃ§Ã£o

### Dados Externos ObrigatÃ³rios (Fontes Oficiais)

**Demografia e Economia (IBGE/SIDRA):**
- PopulaÃ§Ã£o residente estimada (Tabela 6579)
- TGCA (Taxa GeomÃ©trica de Crescimento Anual) â€” calculada
- PIB segmentado (Tabela 5938)
- NÃºmero de domicÃ­lios e renda mÃ©dia (Tabela 3562 - Censo 2010)

**Mercado de Trabalho (CAGED/MTE):**
- Emprego e desemprego municipal
- EvoluÃ§Ã£o de vÃ­nculos formais (Ãºltimos 12-24 meses)
- Perfil salarial (faixas de renda)

**Registro Civil:**
- Casamentos, divÃ³rcios, separaÃ§Ãµes
- Nascidos vivos, Ã³bitos
- Movimento social que afeta formaÃ§Ã£o de domicÃ­lios

**Pendularidade (IBGE):**
- Pessoas que estudam em outro municÃ­pio (Tabela 3599)
- Pessoas que trabalham em outro municÃ­pio (Tabela 1615)
- Pessoas que retornam diariamente (Tabela 3422)

**Ãndices EconÃ´micos (Bancos de Dados):**
- Selic, TR (Banco Central)
- INCC, CUB (FGV, Sinduscon)
- IPCA, IGP-M (IBGE, FGV)

**Rastreabilidade:** Todas as fontes devem ser registradas em **O10-5_FontesOficiais.csv** com:
- Nome da fonte
- Sistema/tabela especÃ­fica
- Link direto
- Data-base (YYYY-MM)
- Uso no modelo
- ObservaÃ§Ãµes

---

## 5. Processo de AnÃ¡lise (Passo a Passo)

### FASE 1: PreparaÃ§Ã£o de Premissas (1-2 horas)

**Passo 1.1: Coletar Dados Macro**
- [ ] Acessar Banco Central â†’ taxa Selic atual
- [ ] Acessar FGV â†’ INCC Ãºltimos 12 meses
- [ ] Acessar Sinduscon â†’ CUB regional
- [ ] Documentar em O10-1_Premissas_Brasil

**Passo 1.2: Definir ParÃ¢metros do Projeto**
- [ ] Horizonte de projeÃ§Ã£o (24-48 meses)
- [ ] WACC: estimar custo de capital prÃ³prio + terceiros
- [ ] Hurdle rate: WACC + prÃªmio de risco
- [ ] Impostos: verificar regime tributÃ¡rio (presumido/real)

**Passo 1.3: Validar IntegraÃ§Ã£o P6-P9**
- [ ] Confirmar preÃ§o de stand (P6)
- [ ] Confirmar oferta total (P7)
- [ ] Confirmar absorÃ§Ã£o por faixa/H3 (P8)
- [ ] Confirmar score de convalidaÃ§Ã£o (P9)

**Checkpoint 1:** âœ… Todas as premissas coletadas e documentadas? â†’ AvanÃ§ar para Fase 2

---

### FASE 2: Montagem do Plano de Vendas (2-3 horas)

**Passo 2.1: Distribuir AbsorÃ§Ã£o em Meses**
- [ ] Escolher curva de vendas (linear/S/manual)
- [ ] Aplicar Fator 4:1 (com validaÃ§Ã£o) ou 10:1 (sem)
- [ ] Distribuir unidades vendidas por mÃªs
- [ ] Calcular receita bruta mensal

**Exemplo de AplicaÃ§Ã£o:**
```
Input P8: AbsorÃ§Ã£o = +12% (positiva), 100 unidades, faixa 2-3SM
ValidaÃ§Ã£o P9: Score = 75 (bom) â†’ Fator 4:1

CÃ¡lculo:
Demanda bruta: 100 un Ã— 4 = 400 un potenciais
AbsorÃ§Ã£o ajustada: 100 un / 24 meses = 4,2 un/mÃªs (linear)
Curva S escolhida:
  Meses 1-6: 2 un/mÃªs
  Meses 7-18: 6 un/mÃªs
  Meses 19-24: 3 un/mÃªs
```

**Passo 2.2: Calcular Receita LÃ­quida**
- [ ] Aplicar comissÃ£o de vendas (4-6%)
- [ ] Descontar impostos sobre receita (3-5%)
- [ ] Gerar coluna "Receita LÃ­quida Mensal"

**Passo 2.3: Distribuir Receitas por Tipo**
- [ ] Entrada (10-30% no mÃªs da venda)
- [ ] IntermediÃ¡rias (durante obra)
- [ ] Finais (na entrega)

**Checkpoint 2:** âœ… Plano de vendas completo e reconciliado com P8? â†’ AvanÃ§ar para Fase 3

---

### FASE 3: ConstruÃ§Ã£o do Fluxo de Caixa (3-5 horas)

**Passo 3.1: Mapear CAPEX (Investimentos)**
```
ITEM                    VALOR (R$)      TIMING
Terreno                 2.500.000       MÃªs 0
ITBI (2%)                  50.000       MÃªs 0
Registro                   25.000       MÃªs 0
Projetos                  150.000       Meses 0-6
AprovaÃ§Ãµes                 80.000       Meses 3-9
Obra (CUB Ã— mÂ²)         8.000.000       Meses 6-30
Infraestrutura          1.200.000       Meses 6-24
Paisagismo                300.000       Meses 24-30
ContingÃªncia (5%)         500.000       Reserve
-------------------------------------------
TOTAL CAPEX            12.805.000
```

**Passo 3.2: Mapear OPEX (Despesas Operacionais)**
```
ITEM                         % RECEITA    MENSAL (R$)
Marketing e Vendas           3%           VariÃ¡vel
AdministraÃ§Ã£o                1,5%         VariÃ¡vel
JurÃ­dico/Cartorial           1%           VariÃ¡vel
Impostos Operacionais        3%           VariÃ¡vel
```

**Passo 3.3: Montar Fluxo Mensal**
- [ ] Linha 1: Receitas (entrada + intermediÃ¡rias + finais)
- [ ] Linha 2: CAPEX (desembolsos por milestone)
- [ ] Linha 3: OPEX (% sobre receita)
- [ ] Linha 4: Impostos (ISS, PIS/COFINS, IR/CS)
- [ ] **Linha 5: SALDO MENSAL = Receita - CAPEX - OPEX - Impostos**
- [ ] **Linha 6: SALDO ACUMULADO**

**Passo 3.4: Calcular Indicadores**
```python
# PseudocÃ³digo para cÃ¡lculo de VPL
VPL = 0
for mes in range(0, 48):
    FC_mes = Saldo_Mensal[mes]
    VPL += FC_mes / (1 + WACC_mensal) ** mes

# TIR: taxa que zera o VPL (usar solver/funÃ§Ã£o financeira)
TIR = SOLVER(VPL = 0)

# Payback: primeiro mÃªs onde Saldo_Acumulado > 0
Payback = MIN(mes onde Saldo_Acumulado[mes] >= 0)
```

**Checkpoint 3:** âœ… Fluxo completo, VPL e TIR calculados? â†’ AvanÃ§ar para Fase 4

---

### FASE 4: AnÃ¡lise de CenÃ¡rios (2-3 horas)

**Passo 4.1: Rodar CenÃ¡rio BASE**
- [ ] Usar premissas originais (P6-P9)
- [ ] Registrar: VPL_base, TIR_base, ROE_base, Payback_base

**Passo 4.2: Rodar CenÃ¡rio CONSERVADOR**
- [ ] Ajustar: PreÃ§o -5%, Velocidade -20%, Juros +2pp
- [ ] Registrar: VPL_cons, TIR_cons, ROE_cons, Payback_cons

**Passo 4.3: Rodar CenÃ¡rio OTIMISTA**
- [ ] Ajustar: PreÃ§o +5%, Velocidade +20%, Juros -1pp
- [ ] Registrar: VPL_otim, TIR_otim, ROE_otim, Payback_otim

**Passo 4.4: Comparar Resultados**
```
DecisÃ£o:
  Se VPL_cons > 0 E TIR_base > Hurdle â†’ GO (forte)
  Se VPL_base > 0 E VPL_cons â‰ˆ 0 â†’ HOLD/AJUSTAR
  Se VPL_base < 0 â†’ NO-GO (revisar premissas ou abortar)
```

**Checkpoint 4:** âœ… 3 cenÃ¡rios rodados e comparados? â†’ AvanÃ§ar para Fase 5

---

### FASE 5: Sensibilidade e Riscos (1-2 horas)

**Passo 5.1: Montar Matriz 2Ã—2**
- [ ] Variar PreÃ§o: -10%, -5%, 0%, +5%, +10%
- [ ] Variar Velocidade: -40%, -20%, 0%, +20%, +40%
- [ ] Calcular VPL para cada combinaÃ§Ã£o (25 cenÃ¡rios)
- [ ] Plotar matriz de calor (verde/amarelo/vermelho)

**Passo 5.2: Identificar Alavancas CrÃ­ticas**
- [ ] Qual variÃ¡vel tem maior impacto no VPL?
- [ ] PreÃ§o ou Velocidade Ã© mais sensÃ­vel?
- [ ] Em que ponto o VPL vira negativo?

**Passo 5.3: Mapear Riscos CrÃ­ticos**

**Risco 1: JurÃ­dico/Legal**
- DescriÃ§Ã£o: Atraso em aprovaÃ§Ãµes, embargo de obra
- Probabilidade: Baixa/MÃ©dia/Alta
- Impacto: +3-6 meses de prazo
- MitigaÃ§Ã£o: Buffer de contingÃªncia 10%, relacionamento com prefeitura

**Risco 2: Demanda AquÃ©m do Projetado**
- DescriÃ§Ã£o: Velocidade de vendas < 80% do previsto
- Probabilidade: MÃ©dia (se P9 fraco)
- Impacto: VPL cai 30-50%
- MitigaÃ§Ã£o: ReforÃ§o de marketing, ajuste de preÃ§o/mix

**Risco 3: Oferta Futura (Pipeline)**
- DescriÃ§Ã£o: Concorrentes lanÃ§am 200+ unidades na mesma faixa
- Probabilidade: MÃ©dia/Alta (verificar P7)
- Impacto: PressÃ£o de preÃ§o -5 a -10%
- MitigaÃ§Ã£o: Monitoramento mensal, flexibilidade de lanÃ§amento

**Risco 4: CrÃ©dito/Financiamento**
- DescriÃ§Ã£o: RestriÃ§Ã£o de crÃ©dito imobiliÃ¡rio (juros sobem, renda cai)
- Probabilidade: MÃ©dia (depende de macro)
- Impacto: Demanda cai 20-40%
- MitigaÃ§Ã£o: Oferecer financiamento direto, parcerias com bancos

**Risco 5: ExecuÃ§Ã£o/Obra**
- DescriÃ§Ã£o: Atraso de obra, estouro de custo
- Probabilidade: MÃ©dia
- Impacto: +10-15% de CAPEX
- MitigaÃ§Ã£o: ContingÃªncia 10%, fornecedores de confianÃ§a

**Checkpoint 5:** âœ… Matriz de sensibilidade gerada e riscos mapeados? â†’ AvanÃ§ar para Fase 6

---

### FASE 6: Resumo Executivo e DecisÃ£o (1 hora)

**Passo 6.1: Consolidar KPIs**
```
INDICADORES FINANCEIROS (CenÃ¡rio Base)
VPL:            R$ 2,5 milhÃµes
TIR:            22% a.a.
ROE:            28%
Payback:        18 meses
Margem LÃ­quida: 18%

CENÃRIOS COMPARATIVOS
              BASE    CONSERV   OTIMISTA
VPL (R$ mi)   2,5     0,8       4,2
TIR (%)       22%     16%       28%
```

**Passo 6.2: Emitir DecisÃ£o**

**DECISÃƒO: GO / HOLD / NO-GO**

**Justificativa (3 bullets):**
1. VPL positivo em BASE e CONSERVADOR (R$ 2,5mi e R$ 0,8mi)
2. TIR de 22% supera Hurdle de 18% com margem confortÃ¡vel
3. AbsorÃ§Ã£o validada no P9 (Score 75), razÃ£o Demanda:Oferta de 4,5:1

**Premissas CrÃ­ticas:**
- Velocidade de vendas: 4,2 un/mÃªs (base)
- PreÃ§o de stand: R$ 180.000
- AbsorÃ§Ã£o P8: +12% (positiva)
- WACC: 18% a.a.

**Riscos Monitorados:**
- Oferta futura: 180 unidades em pipeline (P7)
- CrÃ©dito: taxa Selic em 11,75% (monitorar mensalmente)

**PrÃ³ximos Passos:**
1. Aprovar inÃ­cio de projetos executivos (1-2 meses)
2. Fechar parceria com banco para crÃ©dito (2 meses)
3. Iniciar campanha de prÃ©-lanÃ§amento (cliente oculto ativo)

**Checkpoint 6:** âœ… Resumo Executivo completo? â†’ **PASSO 10 CONCLUÃDO**

---

## 6. Outputs Esperados

### EntregÃ¡veis ObrigatÃ³rios (Templates)

**O10-1_Premissas_Brasil.xlsx**
- Aba 1: README (instruÃ§Ãµes)
- Aba 2: Juros (taxa a.a./a.m., conversÃ£o automÃ¡tica)
- Aba 3: Ãndices (INCC, CUB, IPCA, IGP-M por mÃªs)
- Aba 4: Impostos (ITBI, Registro, ComissÃ£o, etc.)
- Aba 5: ParÃ¢metros (Horizonte, WACC, Hurdle)

**O10-2_PlanodeVendas_Absorcao.xlsx**
- Coluna A: MÃªs (1 a 48)
- Coluna B: Unidades vendidas
- Coluna C: Receita bruta (preÃ§o Ã— unidades)
- Coluna D: ComissÃ£o (%)
- Coluna E: Impostos s/ vendas (%)
- Coluna F: Receita lÃ­quida
- Coluna G: AbsorÃ§Ã£o P8 (referÃªncia)

**O10-3_FluxoDRE_Retornos.xlsx**
- SeÃ§Ã£o 1: RECEITAS (entrada, intermediÃ¡ria, final)
- SeÃ§Ã£o 2: CAPEX (terreno, obra, projetos)
- SeÃ§Ã£o 3: OPEX (marketing, admin, jurÃ­dico)
- SeÃ§Ã£o 4: IMPOSTOS (ISS, PIS/COFINS, IR/CS)
- SeÃ§Ã£o 5: FLUXO (Saldo mensal, Saldo acumulado)
- SeÃ§Ã£o 6: RETORNOS (VPL, TIR, ROE, Payback)

**O10-4_Sensibilidade_2x2.xlsx**
- Matriz: PreÃ§o Ã— Velocidade (25 cÃ©lulas)
- Valores: VPL em cada cenÃ¡rio
- FormataÃ§Ã£o condicional: verde/amarelo/vermelho
- GrÃ¡fico de superfÃ­cie (opcional)

**O10-5_FontesOficiais.csv**
- Colunas: fonte; sistema_tabela; link; data_base; uso_no_modelo; observacoes
- Exemplo de linha:
```
IBGE;Tabela 6579;https://sidra.ibge.gov.br/tabela/6579;2024-12;PopulaÃ§Ã£o residente para cÃ¡lculo de domicÃ­lios;Dados atualizados anualmente
```

**O10-6_Resumo_Executivo_P10.md**
- 1 pÃ¡gina mÃ¡xima
- SeÃ§Ãµes: Veredito, Premissas, CenÃ¡rios, Sensibilidade, Riscos, PrÃ³ximos Passos
- Formato: Markdown para fÃ¡cil conversÃ£o (PDF, DOCX)

---

## 7. Alertas e ValidaÃ§Ãµes

### âš ï¸ Red Flags CrÃ­ticos (STOP IMEDIATO)

ðŸ”´ **VPL negativo em BASE e CONSERVADOR**
- AÃ§Ã£o: Revisar preÃ§o (P6), absorÃ§Ã£o (P8) ou CAPEX
- Se nÃ£o resolver: **NO-GO**

ðŸ”´ **TIR < Hurdle Rate em BASE**
- AÃ§Ã£o: Buscar reduÃ§Ã£o de CAPEX ou aumento de preÃ§o
- Se inviÃ¡vel: **NO-GO**

ðŸ”´ **Payback > 75% do prazo total**
- AÃ§Ã£o: Revisar cronograma de vendas e desembolsos
- Risco: Projeto fica "travado" em caixa negativo por muito tempo

ðŸ”´ **AbsorÃ§Ã£o negativa em todos os cenÃ¡rios (P8)**
- AÃ§Ã£o: **PARAR** â€” mercado nÃ£o valida o produto
- Retornar ao P4 (VocaÃ§Ã£o) ou abortar terreno

ðŸ”´ **RazÃ£o Demanda:Oferta < 4:1 sem validaÃ§Ã£o robusta**
- AÃ§Ã£o: ObrigatÃ³rio usar Fator 10:1 (muito conservador)
- Se ainda inviÃ¡vel: **NO-GO**

### âš ï¸ Yellow Flags (AtenÃ§Ã£o e Ajustes)

ðŸŸ¡ **VPL positivo apenas em BASE (negativo em CONSERVADOR)**
- AÃ§Ã£o: **HOLD** â€” projeto frÃ¡gil, ajustar premissas
- Revisar: mix de produto, praÃ§a, preÃ§o, timing de lanÃ§amento

ðŸŸ¡ **TIR entre Hurdle e Hurdle+3pp**
- AÃ§Ã£o: Margem apertada, buscar otimizaÃ§Ãµes
- Revisar: custo de obra, comissÃ£o, timing de caixa

ðŸŸ¡ **Sensibilidade alta a VELOCIDADE (> 50% de variaÃ§Ã£o no VPL)**
- AÃ§Ã£o: ReforÃ§ar validaÃ§Ã£o de demanda (P9)
- MitigaÃ§Ã£o: Campanha de marketing agressiva, corretor parceiro

ðŸŸ¡ **Sensibilidade alta a PREÃ‡O (> 40% de variaÃ§Ã£o no VPL)**
- AÃ§Ã£o: Produto pode estar mal posicionado
- Revisar: padrÃ£o construtivo, localizaÃ§Ã£o, diferenciaÃ§Ã£o

ðŸŸ¡ **Oferta futura > 150% da demanda anual (P7)**
- AÃ§Ã£o: Pipeline saturarÃ¡ mercado
- MitigaÃ§Ã£o: Antecipar lanÃ§amento, diferenciar produto, flexibilizar preÃ§o

### âœ… Green Flags (Sinais Positivos)

âœ… **VPL > 0 em BASE, CONSERVADOR e OTIMISTA**
- ConclusÃ£o: Projeto robusto, **GO STRONG**

âœ… **TIR > Hurdle + 5pp**
- ConclusÃ£o: Margem confortÃ¡vel, risco diluÃ­do

âœ… **ROE > 25%**
- ConclusÃ£o: Gera riqueza real (nÃ£o sÃ³ lucro absoluto)

âœ… **Payback < 50% do prazo**
- ConclusÃ£o: RecuperaÃ§Ã£o rÃ¡pida de capital

âœ… **AbsorÃ§Ã£o positiva (> 0) validada no P9**
- ConclusÃ£o: Demanda confirmada, mercado receptivo

---

## 8. IntegraÃ§Ã£o com Outras Skills

### DependÃªncias (Inputs de Outros Passos)

**P6 (Demanda):** tiv-passo6-demanda
- Output usado: PreÃ§o de stand, demanda pagante, parÃ¢metros de financiamento
- Se P6 nÃ£o executado: **IMPOSSÃVEL** rodar P10 corretamente

**P7 (Oferta):** tiv-passo7-oferta
- Output usado: Oferta total (pulverizada + lanÃ§amentos + futura), IVV/VSO
- Se P7 nÃ£o executado: Risco de ignorar pressÃ£o competitiva

**P8 (AbsorÃ§Ã£o):** tiv-absorcao
- Output usado: Taxa de absorÃ§Ã£o por faixa e H3, sinal positivo/negativo
- Se P8 nÃ£o executado: Plano de vendas serÃ¡ **CHUTE** (inaceitÃ¡vel)

**P9 (ConvalidaÃ§Ã£o):** tiv-passo9-convalidacao
- Output usado: Score de confianÃ§a, ajuste de Fator 4:1 ou 10:1
- Se P9 nÃ£o executado: Usar Fator 10:1 por padrÃ£o (conservadorismo mÃ¡ximo)

### Consumidores (Skills que Usam P10)

**PITH (RelatÃ³rio Final):** tiv-pith
- Usa: Resumo Executivo P10, KPIs financeiros, decisÃ£o Go/Hold/No-Go
- IntegraÃ§Ã£o: P10 Ã© a **Ãºltima seÃ§Ã£o tÃ©cnica** do PITH antes da conclusÃ£o

**Validador:** tiv-validador
- Usa: Checklist de premissas, rastreabilidade de fontes
- IntegraÃ§Ã£o: Valida se P10 foi executado com rigor metodolÃ³gico

**FCD (anÃ¡lise complementar):** tiv-fcd
- Usa: Mesmo fluxo de caixa do P10, mas com foco em estruturaÃ§Ã£o financeira
- IntegraÃ§Ã£o: P10 = viabilidade; FCD = otimizaÃ§Ã£o de funding e estrutura

---

## 9. Exemplos PrÃ¡ticos

### Caso Real: Loteamento Residencial em Leopoldina-MG

**Contexto:**
- Terreno: 22 hectares, zona rural com potencial de parcelamento
- VocaÃ§Ã£o (P4): Loteamento popular (faixa 2-3 SM)
- Produto: 180 lotes de 200-250mÂ²
- PraÃ§a: Leopoldina-MG e regiÃ£o (AlÃ©m ParaÃ­ba, Cataguases)

**Inputs dos Passos Anteriores:**

**P6 (Demanda):**
- PreÃ§o de stand: R$ 55.000/lote (calculado via PRICE reverso)
- Demanda pagante: 720 famÃ­lias (razÃ£o 4:1)
- Renda-alvo: 2-3 SM (R$ 2.600 - R$ 3.900)

**P7 (Oferta):**
- Oferta pulverizada: 45 lotes
- LanÃ§amentos (12m): 90 lotes
- Oferta futura (pipeline): 120 lotes
- IVV: 3,5 meses (bom)

**P8 (AbsorÃ§Ã£o):**
- Taxa: +18% (positiva)
- Velocidade: 8 lotes/mÃªs (calculado)

**P9 (ConvalidaÃ§Ã£o):**
- Cliente oculto: 12 interessados em 3 dias
- Score: 80 (validaÃ§Ã£o forte)
- Fator: 4:1 (aprovado)

---

**EXECUÃ‡ÃƒO DO PASSO 10:**

**Premissas (O10-1):**
```
Taxa Selic: 11,75% a.a. â†’ 0,93% a.m.
INCC (12m): 4,2% acumulado
CUB MG (R$/mÂ²): R$ 1.850
WACC: 18% a.a. (1,39% a.m.)
Hurdle: 21% a.a.
```

**Plano de Vendas (O10-2):**
```
Curva S â€” 24 meses
Meses 1-4:   4 lotes/mÃªs  Ã— R$ 55k = R$ 220k/mÃªs
Meses 5-16: 10 lotes/mÃªs  Ã— R$ 55k = R$ 550k/mÃªs
Meses 17-24: 6 lotes/mÃªs  Ã— R$ 55k = R$ 330k/mÃªs
Total: 180 lotes vendidos

Receita bruta total: R$ 9.900.000
Receita lÃ­quida (apÃ³s comissÃ£o 5% + impostos 3%): R$ 9.108.000
```

**Fluxo de Caixa (O10-3):**
```
CAPEX:
  Terreno:                R$ 1.500.000
  ITBI + Registro:        R$    45.000
  Projetos/AprovaÃ§Ãµes:    R$   150.000
  Infraestrutura:         R$ 2.800.000
  ContingÃªncia (10%):     R$   450.000
  TOTAL CAPEX:            R$ 4.945.000

OPEX (% da receita):
  Marketing:              R$   300.000 (3%)
  AdministraÃ§Ã£o:          R$   150.000 (1,5%)
  JurÃ­dico:               R$   100.000 (1%)
  TOTAL OPEX:             R$   550.000

Impostos sobre lucro:     R$   650.000 (15% presumido)

LUCRO LÃQUIDO:            R$ 2.963.000
```

**Indicadores:**
```
VPL (WACC 18%):           R$ 1.850.000
TIR:                      24,5% a.a.
ROE:                      32%
Payback:                  14 meses
Margem LÃ­quida:           30%
```

**CenÃ¡rios:**
```
MÃ©trica       BASE     CONSERV   OTIMISTA
VPL (R$ mi)   1,85     0,65      3,10
TIR (%)       24,5%    19,2%     29,8%
ROE (%)       32%      22%       42%
Payback (m)   14       19        11
```

**Sensibilidade 2Ã—2 (VPL em R$ milhÃµes):**
```
Vel â†“ PreÃ§o â†’  -10%    -5%     BASE    +5%     +10%
-40%           (0,3)   0,2     0,7     1,2     1,7
-20%            0,6    1,1     1,6     2,1     2,6
BASE            1,2    1,7     2,2     2,7     3,2
+20%            1,8    2,3     2,8     3,3     3,8
+40%            2,4    2,9     3,4     3,9     4,4
```

**AnÃ¡lise:**
- âœ… VPL positivo em todos os 3 cenÃ¡rios
- âœ… TIR > Hurdle (24,5% vs 21%)
- âœ… ROE > 25% (indica criaÃ§Ã£o de riqueza)
- âœ… Payback em 14 meses (58% do prazo) â€” bom
- âš ï¸ SensÃ­vel a velocidade: -20% de vendas â†’ VPL cai 40%

**Riscos Mapeados:**
1. **Pipeline de 120 lotes** (P7) â†’ MitigaÃ§Ã£o: LanÃ§ar em 6 meses, diferenciar infraestrutura
2. **CrÃ©dito imobiliÃ¡rio** â†’ MitigaÃ§Ã£o: Oferecer parcelamento direto (entrada + 48Ã—)
3. **Pendularidade alta** (P2) â†’ Oportunidade: PÃºblico trabalha em outras cidades, valoriza acesso

**DECISÃƒO: GO (FORTE)**

**Justificativa:**
1. VPL robusto mesmo em cenÃ¡rio conservador (R$ 650k)
2. AbsorÃ§Ã£o validada (+18%) com convalidaÃ§Ã£o forte (Score 80)
3. Margem de seguranÃ§a: TIR 3,5pp acima do Hurdle

**PrÃ³ximos Passos:**
1. Aprovar aquisiÃ§Ã£o do terreno (30 dias)
2. Iniciar projetos de infraestrutura (60 dias)
3. LanÃ§ar campanha de prÃ©-venda (cliente oculto ativo)
4. Fechar parceria com construtora regional (90 dias)

---

### Caso 2: IncorporaÃ§Ã£o Vertical em Leopoldina (Contraste)

**Contexto:**
- EdifÃ­cio 8 andares, 32 apartamentos (4 por andar)
- VocaÃ§Ã£o (P4): Classe mÃ©dia (faixa 4-6 SM)
- Produto: 2 quartos, 55mÂ², padrÃ£o normal
- PraÃ§a: Centro de Leopoldina

**Inputs P6-P9:**
- PreÃ§o stand: R$ 280.000 (P6)
- AbsorÃ§Ã£o: **-8%** (negativa) â€” saturaÃ§Ã£o na faixa 4-6 SM (P8)
- ConvalidaÃ§Ã£o: Score 45 (fraco) â€” poucos interessados (P9)
- Oferta futura: 150 unidades em pipeline (P7)

**EXECUÃ‡ÃƒO DO PASSO 10:**

**Plano de Vendas:**
```
AbsorÃ§Ã£o negativa â†’ Usar cenÃ¡rio CONSERVADOR desde o inÃ­cio
Velocidade: 1 un/mÃªs (muito lenta)
Prazo: 32 meses (ao invÃ©s de 24)
```

**Fluxo de Caixa:**
```
CAPEX: R$ 6.500.000
Receita lÃ­quida: R$ 8.200.000
OPEX + Impostos: R$ 1.200.000
LUCRO LÃQUIDO: R$ 500.000 (margem de 6% â€” muito baixa)
```

**Indicadores:**
```
VPL (WACC 18%):    R$ (150.000) â€” NEGATIVO
TIR:               14,5% â€” ABAIXO DO HURDLE (21%)
ROE:               8% â€” INSUFICIENTE
Payback:           28 meses (88% do prazo) â€” RUIM
```

**CenÃ¡rios:**
```
MÃ©trica       BASE     CONSERV   OTIMISTA
VPL (R$ mi)   (0,15)   (0,80)    0,30
TIR (%)       14,5%    9,2%      18,8%
ROE (%)       8%       2%        14%
```

**AnÃ¡lise:**
- ðŸ”´ VPL negativo em BASE e CONSERVADOR
- ðŸ”´ TIR abaixo do Hurdle em todos os cenÃ¡rios
- ðŸ”´ ROE < 15% (nÃ£o gera riqueza)
- ðŸ”´ AbsorÃ§Ã£o negativa validada (P8 + P9 fracos)

**DECISÃƒO: NO-GO**

**Justificativa:**
1. Mercado saturado (oferta futura de 150 un)
2. AbsorÃ§Ã£o negativa nÃ£o reversÃ­vel sem mudanÃ§a radical de produto
3. Viabilidade financeira inviÃ¡vel mesmo em cenÃ¡rio otimista

**Alternativas Exploradas:**
- âŒ Reduzir preÃ§o 10% â†’ VPL continua negativo
- âŒ Mudar para faixa 2-3 SM â†’ Produto inadequado (vertical nÃ£o se sustenta)
- âŒ Adiar lanÃ§amento 12 meses â†’ Pipeline aumenta ainda mais

**RecomendaÃ§Ã£o Final:**
**ABORTAR TERRENO** ou **MUDAR COMPLETAMENTE A VOCAÃ‡ÃƒO** (voltar ao P4)
- OpÃ§Ã£o: Revisar como loteamento horizontal (faixa 2-3 SM)
- OpÃ§Ã£o: Vender terreno e buscar outra oportunidade

---

## 10. Checklist de Qualidade

### âœ… PrÃ©-ExecuÃ§Ã£o (Antes de ComeÃ§ar)

- [ ] Passos 6, 7, 8 e 9 foram concluÃ­dos e documentados?
- [ ] Outputs de P6-P9 estÃ£o acessÃ­veis e validados?
- [ ] Fontes de dados oficiais foram identificadas (IBGE, CAGED, Banco Central)?
- [ ] Templates O10-1 a O10-6 estÃ£o prontos para preenchimento?
- [ ] ParÃ¢metros bÃ¡sicos foram definidos (WACC, Hurdle, horizonte)?

### âœ… Durante a ExecuÃ§Ã£o (Cada Fase)

**Premissas (Fase 1):**
- [ ] Taxas de juros coletadas de fonte oficial (Banco Central)?
- [ ] Ãndices (INCC, CUB, IPCA) dos Ãºltimos 12 meses documentados?
- [ ] Impostos municipais e federais verificados (regime tributÃ¡rio)?
- [ ] WACC calculado considerando custo de capital prÃ³prio + terceiros?
- [ ] Todas as fontes registradas em O10-5_FontesOficiais.csv?

**Plano de Vendas (Fase 2):**
- [ ] AbsorÃ§Ã£o do P8 foi aplicada corretamente (sinal e magnitude)?
- [ ] Fator 4:1 ou 10:1 escolhido conforme validaÃ§Ã£o do P9?
- [ ] Curva de vendas (linear/S) Ã© realista para o mercado local?
- [ ] Receita lÃ­quida descontou comissÃ£o (4-6%) e impostos (3-5%)?
- [ ] Plano de vendas reconcilia com meta de unidades totais?

**Fluxo de Caixa (Fase 3):**
- [ ] CAPEX inclui: terreno, ITBI, projetos, obra, infraestrutura, contingÃªncia?
- [ ] ContingÃªncia de 5-10% foi incluÃ­da?
- [ ] OPEX estÃ¡ vinculado a % da receita (nÃ£o valores fixos)?
- [ ] Impostos sobre lucro foram calculados conforme regime tributÃ¡rio?
- [ ] Saldo mensal e acumulado foram calculados corretamente?
- [ ] VPL foi calculado usando WACC correto (mensal ou anual)?
- [ ] TIR foi verificada (taxa que zera o VPL)?
- [ ] Payback foi identificado (primeiro mÃªs de saldo acumulado > 0)?

**CenÃ¡rios (Fase 4):**
- [ ] CenÃ¡rio BASE usa premissas originais (P6-P9)?
- [ ] CenÃ¡rio CONSERVADOR aplica stress (-20% velocidade, -5% preÃ§o, +2pp juros)?
- [ ] CenÃ¡rio OTIMISTA Ã© realista (nÃ£o "wishful thinking")?
- [ ] Os 3 cenÃ¡rios foram comparados lado a lado?
- [ ] DecisÃ£o preliminar (Go/Hold/No-Go) foi tomada com base nos cenÃ¡rios?

**Sensibilidade (Fase 5):**
- [ ] Matriz 2Ã—2 foi gerada (PreÃ§o Ã— Velocidade)?
- [ ] VariaÃ§Ãµes sÃ£o suficientes para testar extremos (-40% a +40%)?
- [ ] VPL foi calculado para cada cÃ©lula da matriz (25 cenÃ¡rios)?
- [ ] Alavancas crÃ­ticas foram identificadas (preÃ§o, velocidade, prazo, juros)?
- [ ] Riscos foram mapeados (jurÃ­dico, demanda, oferta futura, crÃ©dito, execuÃ§Ã£o)?
- [ ] Cada risco tem mitigaÃ§Ã£o proposta?

**Resumo Executivo (Fase 6):**
- [ ] DecisÃ£o final estÃ¡ clara (Go/Hold/No-Go)?
- [ ] Justificativa tem 3 bullets objetivos?
- [ ] KPIs principais estÃ£o destacados (VPL, TIR, ROE, Payback)?
- [ ] Premissas crÃ­ticas foram listadas?
- [ ] Riscos monitorados foram elencados?
- [ ] PrÃ³ximos passos sÃ£o acionÃ¡veis e tÃªm prazo?

### âœ… PÃ³s-ExecuÃ§Ã£o (EntregÃ¡veis Finais)

- [ ] O10-1_Premissas_Brasil.xlsx estÃ¡ completo e versionado?
- [ ] O10-2_PlanodeVendas_Absorcao.xlsx reconcilia com P8?
- [ ] O10-3_FluxoDRE_Retornos.xlsx tem VPL/TIR/ROE/Payback calculados?
- [ ] O10-4_Sensibilidade_2x2.xlsx tem matriz completa e formatada?
- [ ] O10-5_FontesOficiais.csv registra TODAS as fontes usadas?
- [ ] O10-6_Resumo_Executivo_P10.md estÃ¡ em 1 pÃ¡gina e Ã© claro?
- [ ] Todos os arquivos estÃ£o salvos em pasta organizada (Projeto_X/Passo10/)?
- [ ] VersÃ£o foi registrada (v1.0, v1.1, etc.)?

### âœ… ValidaÃ§Ã£o Final (CritÃ©rios de AceitaÃ§Ã£o)

**MetodolÃ³gico:**
- [ ] ProibiÃ§Ã£o de "chute" foi respeitada (fontes oficiais usadas)?
- [ ] IntegraÃ§Ã£o P6-P9 foi rigorosa (sem desconexÃ£o de dados)?
- [ ] Premissas sÃ£o defensÃ¡veis em comitÃª de investimento?

**Financeiro:**
- [ ] VPL foi calculado corretamente (sem erros de fÃ³rmula)?
- [ ] TIR Ã© realista (nÃ£o estÃ¡ absurdamente alta/baixa)?
- [ ] ROE > 15% em cenÃ¡rio BASE (se nÃ£o, foi justificado)?
- [ ] Payback < 75% do prazo total (se nÃ£o, foi sinalizado)?

**Decisional:**
- [ ] DecisÃ£o Go/Hold/No-Go tem base sÃ³lida?
- [ ] Riscos crÃ­ticos foram endereÃ§ados?
- [ ] PrÃ³ximos passos sÃ£o claros e tÃªm responsÃ¡veis?

**Rastreabilidade:**
- [ ] Todas as fontes estÃ£o documentadas (O10-5)?
- [ ] VersÃµes de arquivos estÃ£o controladas?
- [ ] Modelo financeiro pode ser auditado por terceiros?

---

## 11. Erros Comuns e Como Evitar

### âŒ Erro 1: Usar "Chute" em Premissas
**Sintoma:** Taxas ou Ã­ndices estimados "de cabeÃ§a", sem fonte oficial.  
**ConsequÃªncia:** ProjeÃ§Ãµes inverificÃ¡veis, comitÃª de investimento rejeita.  
**SoluÃ§Ã£o:** Sempre coletar de fontes nomeadas (Banco Central, IBGE, FGV).

### âŒ Erro 2: Ignorar Fator 4:1 ou 10:1
**Sintoma:** Usar absorÃ§Ã£o direta do P8 sem ajuste conservador.  
**ConsequÃªncia:** Plano de vendas otimista demais, frustraÃ§Ã£o de expectativas.  
**SoluÃ§Ã£o:** Aplicar Fator 4:1 (com validaÃ§Ã£o P9) ou 10:1 (sem validaÃ§Ã£o).

### âŒ Erro 3: Misturar Faixas de Renda na AbsorÃ§Ã£o
**Sintoma:** Calcular absorÃ§Ã£o mÃ©dia entre faixas 2-3SM e 4-6SM.  
**ConsequÃªncia:** Velocidade de vendas irreal (uma faixa pode estar saturada).  
**SoluÃ§Ã£o:** Separar absorÃ§Ã£o por faixa de renda e por H3 (sub-regiÃ£o).

### âŒ Erro 4: Esquecer Oferta Futura (Pipeline)
**Sintoma:** Analisar sÃ³ oferta atual (pulverizada + lanÃ§amentos).  
**ConsequÃªncia:** Ignorar concorrentes que lanÃ§arÃ£o em 6-12 meses.  
**SoluÃ§Ã£o:** Incluir pipeline do P7 na anÃ¡lise de pressÃ£o competitiva.

### âŒ Erro 5: Curva de Vendas Desconectada da AbsorÃ§Ã£o
**Sintoma:** Projetar 10 un/mÃªs quando P8 indica 4 un/mÃªs.  
**ConsequÃªncia:** Modelo financeiro fictÃ­cio, VPL irreal.  
**SoluÃ§Ã£o:** Curva de vendas DEVE derivar da absorÃ§Ã£o P8 (com Fator aplicado).

### âŒ Erro 6: VPL Positivo Mas ROE Baixo (<15%)
**Sintoma:** Projeto "viÃ¡vel" no papel, mas nÃ£o gera riqueza real.  
**ConsequÃªncia:** Lucro absoluto existe, mas retorno sobre capital Ã© insuficiente.  
**SoluÃ§Ã£o:** Priorizar ROE como mÃ©trica de decisÃ£o (nÃ£o sÃ³ VPL).

### âŒ Erro 7: CenÃ¡rio Otimista Muito Otimista
**Sintoma:** CenÃ¡rio otimista com +50% de velocidade e +20% de preÃ§o.  
**ConsequÃªncia:** Distorce anÃ¡lise, cria expectativas irreais.  
**SoluÃ§Ã£o:** Limitar otimismo a +20% velocidade e +5% preÃ§o (mÃ¡ximo).

### âŒ Erro 8: NÃ£o Mapear Riscos
**Sintoma:** Focar sÃ³ em nÃºmeros, ignorar riscos qualitativos.  
**ConsequÃªncia:** Surpresas negativas nÃ£o previstas (embargo, crÃ©dito, concorrÃªncia).  
**SoluÃ§Ã£o:** Sempre mapear 5 riscos crÃ­ticos + mitigaÃ§Ãµes.

### âŒ Erro 9: Resumo Executivo Extenso (>2 pÃ¡ginas)
**Sintoma:** Resumo de 5-10 pÃ¡ginas, cheio de detalhes tÃ©cnicos.  
**ConsequÃªncia:** Decisores nÃ£o leem, perdem interesse.  
**SoluÃ§Ã£o:** 1 pÃ¡gina mÃ¡xima â€” KPIs, decisÃ£o, 3 bullets de justificativa.

### âŒ Erro 10: NÃ£o Versionar Arquivos
**Sintoma:** Sobrescrever O10-3 sem manter versÃ£o anterior.  
**ConsequÃªncia:** Perda de histÃ³rico, impossibilidade de auditoria.  
**SoluÃ§Ã£o:** Usar versionamento (v1.0, v1.1) e datas (YYYY-MM-DD).

---

## 12. Notas de IntegraÃ§Ã£o e GovernanÃ§a

### SequÃªncia ObrigatÃ³ria (P6 â†’ P7 â†’ P8 â†’ P9 â†’ P10)

**Nunca pular passos.** P10 depende CRITICAMENTE de P6-P9:

```
P6 (Demanda) â†’ PreÃ§o de stand, demanda pagante
       â†“
P7 (Oferta) â†’ Oferta total, IVV/VSO, pressÃ£o competitiva
       â†“
P8 (AbsorÃ§Ã£o) â†’ Velocidade de vendas por faixa/H3
       â†“
P9 (ConvalidaÃ§Ã£o) â†’ ValidaÃ§Ã£o de intenÃ§Ã£o, ajuste de Fator
       â†“
P10 (Viabilidade) â†’ ProjeÃ§Ãµes, cenÃ¡rios, decisÃ£o
```

**ExceÃ§Ã£o:** Se P8/P9 nÃ£o foram executados, tratar P10 como **hipÃ³tese preliminar**:
- Usar Fator 10:1 (mÃ¡ximo conservadorismo)
- Sinalizar claramente que decisÃ£o Ã© CONDICIONAL
- Obrigar execuÃ§Ã£o de P8/P9 antes de Go definitivo

---

### Rastreabilidade e Auditoria

**PrincÃ­pio:** Cada nÃºmero do P10 deve ter **origem rastreÃ¡vel**.

**Fontes ObrigatÃ³rias (O10-5):**
```csv
fonte;sistema_tabela;link;data_base;uso_no_modelo;observacoes
IBGE;Tabela 6579;https://sidra.ibge.gov.br/tabela/6579;2024-12;PopulaÃ§Ã£o residente;Dados atualizados anualmente
IBGE;Tabela 5938;https://sidra.ibge.gov.br/tabela/5938;2024-12;PIB municipal;Base para renda per capita
IBGE;Tabela 3562;https://sidra.ibge.gov.br/tabela/3562;2010;DomicÃ­lios e renda;Censo 2010 (prÃ³ximo em 2030)
CAGED;Sistema CAGED;https://bi.mte.gov.br/bgcaged/;2024-11;Emprego formal;Atualizado mensalmente
Banco Central;SGS Sistema Gerenciador de SÃ©ries;https://www3.bcb.gov.br/sgspub/;2025-01;Taxa Selic;Base para WACC
FGV;IBRE;https://portalibre.fgv.br/;2024-12;INCC;Ãndice para correÃ§Ã£o de obra
```

**Versionamento:**
```
Projeto_Leopoldina_Loteamento/
  Passo10/
    v1.0_2025-01-12/
      O10-1_Premissas_Brasil_v1.0.xlsx
      O10-2_PlanodeVendas_v1.0.xlsx
      ...
    v1.1_2025-01-20/  (apÃ³s ajuste de preÃ§o)
      O10-1_Premissas_Brasil_v1.1.xlsx
      ...
```

---

### ComunicaÃ§Ã£o com Stakeholders

**Para ComitÃª de Investimento:**
- Enviar O10-6_Resumo_Executivo_P10.md (1 pÃ¡gina)
- Apresentar matriz de sensibilidade (visual)
- Destacar: VPL, TIR, ROE, Payback
- Tempo de apresentaÃ§Ã£o: 10-15 minutos

**Para SÃ³cios/Investidores:**
- Foco em **ROE** (retorno sobre capital)
- Comparar com alternativas (CDB, Tesouro, outros projetos)
- Mostrar cenÃ¡rio CONSERVADOR (nÃ£o sÃ³ BASE)
- Tempo: 5-10 minutos

**Para Equipe TÃ©cnica:**
- Disponibilizar O10-3_FluxoDRE_Retornos.xlsx completo
- Explicar premissas (O10-1)
- Discutir riscos e mitigaÃ§Ãµes
- Tempo: 30-60 minutos (workshop)

---

### AtualizaÃ§Ã£o e RevisÃ£o

**Quando revisar P10:**
- âœ… MudanÃ§a de preÃ§o de stand (P6)
- âœ… Nova oferta futura identificada (P7)
- âœ… AbsorÃ§Ã£o recalculada (P8)
- âœ… ValidaÃ§Ã£o adicional (P9)
- âœ… MudanÃ§a em juros/Ã­ndices (macro)
- âœ… Ajuste de CAPEX (orÃ§amento de obra)

**FrequÃªncia de RevisÃ£o:**
- **Durante prÃ©-lanÃ§amento:** Mensal (mercado volÃ¡til)
- **ApÃ³s lanÃ§amento:** Trimestral (acompanhar realizado vs projetado)
- **Em crise/mudanÃ§a macro:** Imediata

---

## 13. GlossÃ¡rio e Termos TÃ©cnicos

**VPL (Valor Presente LÃ­quido):** Soma dos fluxos de caixa futuros descontados ao valor presente pela taxa WACC. VPL > 0 indica viabilidade.

**TIR (Taxa Interna de Retorno):** Taxa de desconto que zera o VPL. Deve ser > Hurdle Rate para aprovaÃ§Ã£o.

**ROE (Return on Equity):** Lucro LÃ­quido / PatrimÃ´nio LÃ­quido. MÃ©trica prioritÃ¡ria TIV (indica geraÃ§Ã£o de riqueza, nÃ£o sÃ³ lucro).

**WACC (Weighted Average Cost of Capital):** Custo mÃ©dio ponderado de capital (prÃ³prio + terceiros). Base para cÃ¡lculo do VPL.

**Hurdle Rate:** Taxa mÃ­nima de retorno exigida. Tipicamente WACC + prÃªmio de risco (3-5 p.p.).

**Payback:** Tempo necessÃ¡rio para recuperar o investimento inicial. Quanto menor, melhor.

**Fator 4:1 ou 10:1:** Conservadorismo TIV. Divide demanda bruta por 4 (com validaÃ§Ã£o) ou 10 (sem validaÃ§Ã£o) para absorÃ§Ã£o realista.

**CenÃ¡rio BASE:** ProjeÃ§Ã£o realista usando premissas mais provÃ¡veis (P6-P9).

**CenÃ¡rio CONSERVADOR:** Stress test com premissas pessimistas (-20% velocidade, -5% preÃ§o, +2pp juros).

**CenÃ¡rio OTIMISTA:** ProjeÃ§Ã£o otimista (mas nÃ£o irrealista) com +20% velocidade, +5% preÃ§o, -1pp juros.

**Sensibilidade 2Ã—2:** Matriz que testa impacto de variaÃ§Ãµes em 2 variÃ¡veis (tipicamente PreÃ§o Ã— Velocidade) sobre o VPL.

**CAPEX (Capital Expenditure):** Investimentos de capital (terreno, obra, projetos, infraestrutura).

**OPEX (Operational Expenditure):** Despesas operacionais (marketing, administraÃ§Ã£o, jurÃ­dico).

**DRE (Demonstrativo de Resultado do ExercÃ­cio):** RelatÃ³rio contÃ¡bil que mostra Receitas - Custos - Despesas = Lucro.

**Pipeline (Oferta Futura):** Projetos concorrentes em estÃ¡gio de aprovaÃ§Ã£o ou prÃ©-lanÃ§amento que entrarÃ£o no mercado nos prÃ³ximos 12-24 meses.

**IVV (Ãndice de Velocidade de Vendas):** Tempo mÃ©dio para vender 100% do estoque. IVV < 6 meses = mercado aquecido.

**VSO (VacÃ¢ncia, Estoque, Oferta):** Indicador de saturaÃ§Ã£o. VSO alto = mercado saturado.

---

## 14. ReferÃªncias e Fontes

### Fontes de Dados Oficiais (Acesso ObrigatÃ³rio)

**IBGE (Instituto Brasileiro de Geografia e EstatÃ­stica)**
- **Tabela 6579:** PopulaÃ§Ã£o residente estimada
- **Tabela 5938:** PIB municipal
- **Tabela 3562:** DomicÃ­lios e renda (Censo 2010)
- **Tabela 3599:** Pessoas que estudam em outro municÃ­pio
- **Tabela 1615:** Pessoas que trabalham em outro municÃ­pio
- **Tabela 3422:** Pessoas que retornam diariamente (pendularidade)
- Link: https://sidra.ibge.gov.br/

**CAGED (MinistÃ©rio do Trabalho e Emprego)**
- Emprego formal por municÃ­pio
- EvoluÃ§Ã£o de vÃ­nculos (Ãºltimos 12-24 meses)
- Link: https://bi.mte.gov.br/bgcaged/

**Banco Central do Brasil**
- Taxa Selic (juros bÃ¡sicos)
- TR (Taxa Referencial)
- SGS (Sistema Gerenciador de SÃ©ries Temporais)
- Link: https://www.bcb.gov.br/

**FGV (FundaÃ§Ã£o Getulio Vargas)**
- INCC (Ãndice Nacional de Custo da ConstruÃ§Ã£o)
- IGP-M (Ãndice Geral de PreÃ§os - Mercado)
- Link: https://portalibre.fgv.br/

**Sinduscon (Regional)**
- CUB (Custo UnitÃ¡rio BÃ¡sico) por estado/regiÃ£o
- Link: Verificar sindicato estadual

**Registro Civil (EstatÃ­sticas Vitais)**
- Casamentos, divÃ³rcios, separaÃ§Ãµes
- Nascidos vivos, Ã³bitos
- Link: https://www.ibge.gov.br/estatisticas/sociais/populacao/

---

### Bibliografia MetodolÃ³gica

**Livros e Artigos:**
- **"AnÃ¡lise de Viabilidade de Empreendimentos ImobiliÃ¡rios"** â€” Claudio Tavares de Alencar
- **"Mercado ImobiliÃ¡rio: ProduÃ§Ã£o Habitacional e AvaliaÃ§Ã£o de Empreendimentos"** â€” JoÃ£o da Rocha Lima Jr.
- **"Valuation: Como Avaliar Empresas e Escolher as Melhores AÃ§Ãµes"** â€” Alexandre Assaf Neto

**Metodologia TIV:**
- **KB CORE v4.0** â€” Othon Valentim (documento mestre interno)
- **10 Passos TIV** â€” Apostila completa (interna)
- **Skills TIV** â€” Banco de Skills operacionais (tiv-passo1 a tiv-passo10)

---

## 15. Changelog e Versionamento

**v1.0 (2025-01-12) â€” CriaÃ§Ã£o Inicial**
- Estrutura completa dos 10 passos da TIV integrada ao Passo 10
- 5 Camadas de anÃ¡lise (Premissas, Plano de Vendas, Fluxo/DRE, CenÃ¡rios, Sensibilidade)
- Templates O10-1 a O10-6 especificados
- Exemplos prÃ¡ticos: Leopoldina-MG (Go e No-Go)
- Checklist de 95+ itens de validaÃ§Ã£o
- IntegraÃ§Ã£o rigorosa com P6, P7, P8, P9
- GlossÃ¡rio e fontes oficiais listadas

---

## ðŸŽ¯ PrÃ³ximos Passos Sugeridos

ApÃ³s concluir o **Passo 10 â€” Viabilidade Financeira**, o projeto TIV estÃ¡ COMPLETO. Os prÃ³ximos passos sÃ£o:

1. **Consolidar no PITH** (Plano de InteligÃªncia de Teto Horizontal)
   - Usar Skill: tiv-pith
   - Integrar Resumo Executivo P10
   - Gerar relatÃ³rio final de 15-25 pÃ¡ginas

2. **Apresentar para ComitÃª de Investimento**
   - Usar O10-6_Resumo_Executivo_P10.md
   - Destacar: VPL, TIR, ROE, Payback
   - Mostrar cenÃ¡rios e sensibilidade

3. **Executar DecisÃ£o (Go/Hold/No-Go)**
   - **Go:** AvanÃ§ar para projetos executivos, funding, prÃ©-lanÃ§amento
   - **Hold:** Ajustar preÃ§o/mix/praÃ§a, rodar P10 novamente
   - **No-Go:** Abortar ou revisar completamente a vocaÃ§Ã£o (voltar ao P4)

4. **Monitorar Realizado vs Projetado**
   - ApÃ³s lanÃ§amento: Comparar vendas reais com projeÃ§Ã£o (P10)
   - FrequÃªncia: Mensal (primeiros 6 meses), depois trimestral
   - Ajustar premissas se desvio > 15%

---

**FIM DA SKILL TIV-PASSO10-VIABILIDADE v1.0**

---

> **"No Passo 10, nÃºmeros mentem se nÃ£o tiverem fonte. ProjeÃ§Ãµes sem lastro sÃ£o entretenimento, nÃ£o anÃ¡lise. A TIV exige rastreabilidade absoluta â€” cada premissa com origem, cada fonte citada, cada decisÃ£o fundamentada. SÃ³ assim vocÃª defende o projeto em qualquer mesa."**  
> â€” Othon Valentim, Metodologia TIV 4.0
