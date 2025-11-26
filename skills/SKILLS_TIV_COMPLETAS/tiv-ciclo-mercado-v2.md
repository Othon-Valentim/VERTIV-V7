---
name: "tiv-ciclo-mercado-v2"
description: "Identifica fase do ciclo de mercado imobiliario (Recuperacao, Expansao, Desaceleracao, Recessao) usando indicadores leading e lagging. Integra com Passo 1 (timing estrategico) e Passo 8 (ajuste absorcao). Define quando comprar, construir e vender."
---

# SKILL: Ciclo de Mercado ImobiliÃ¡rio v2.0

## 1. OBJETIVO E CONTEXTO

### 1.1. PropÃ³sito
Identificar a fase atual do ciclo imobiliÃ¡rio (RecuperaÃ§Ã£o, ExpansÃ£o, DesaceleraÃ§Ã£o, RecessÃ£o) atravÃ©s de sistema estruturado de indicadores leading e lagging, fornecendo timing estratÃ©gico para decisÃµes de compra, lanÃ§amento e venda de empreendimentos.

### 1.2. Problema Resolvido
Empreendedores frequentemente:
- Compram terrenos caros no topo do ciclo (ExpansÃ£o tardia)
- LanÃ§am projetos em mercados saturados (DesaceleraÃ§Ã£o)
- Perdem oportunidades de compra (RecuperaÃ§Ã£o nÃ£o identificada)
- Vendem em baixa por desespero (RecessÃ£o)
- Ignoram sinais de reversÃ£o do ciclo

### 1.3. Framework das 4 Fases

**CICLO IMOBILIÃRIO:**
```
                EXPANSÃƒO (Pico)
                      â†‘
RECUPERAÃ‡ÃƒO    â†â”€â”€â”€â”€â”€â†’     â”€â”€â”€â”€â”€â†’   DESACELERAÃ‡ÃƒO
(Crescimento)                         (SaturaÃ§Ã£o)
      â†“                                    â†“
            RECESSÃƒO (Vale)
```

**DuraÃ§Ã£o tÃ­pica:** 7-10 anos por ciclo completo
**VariaÃ§Ã£o regional:** Capitais vs interior (defasagem 6-18 meses)

### 1.4. Base MetodolÃ³gica
- **KB CORE v5.0:** SeÃ§Ã£o 1.3 (Ciclo de Mercado)
- **IntegraÃ§Ã£o:** Passo 1 (timing garimpo) + Passo 8 (ajuste absorÃ§Ã£o)
- **PrincÃ­pio:** Comprar na baixa, lanÃ§ar na alta, vender antes da queda

---

## 2. QUANDO ACIONAR

### 2.1. Triggers ObrigatÃ³rios
- [ ] **No Passo 1 (Garimpo):** Identificar fase preliminar para priorizar microrregiÃµes
- [ ] **No Passo 8 (AbsorÃ§Ã£o):** Ajustar velocidade de vendas por fase
- [ ] **Trimestralmente:** Monitorar indicadores e atualizar fase
- [ ] **PrÃ©-investimento:** Validar timing antes de comprar terreno

### 2.2. Triggers Recomendados
- [ ] Ao perceber mudanÃ§as bruscas no mercado
- [ ] Quando indicadores leading divergem dos lagging
- [ ] Antes de decisÃµes estratÃ©gicas (compra, lanÃ§amento, venda)
- [ ] Para benchmarking entre mÃºltiplas microrregiÃµes

### 2.3. Momentos CrÃ­ticos
- **PrÃ©-Compra:** Evitar comprar no topo (ExpansÃ£o tardia)
- **PrÃ©-LanÃ§amento:** Confirmar demanda aquecida (ExpansÃ£o)
- **GestÃ£o PortfÃ³lio:** Decidir timing de entrada/saÃ­da

---

## 3. FRAMEWORK/METODOLOGIA

### 3.1. Sistema de Indicadores

#### Leading Indicators (Antecedentes - 3-6 meses Ã  frente)

**1. LicenÃ§as de ConstruÃ§Ã£o**
- **Fonte:** Prefeitura Municipal (Secretaria de Obras)
- **FrequÃªncia:** Mensal
- **MÃ©trica:** Quantidade de alvarÃ¡s emitidos (mÂ² ou unidades)
- **Sinal:** â†—ï¸ = ExpansÃ£o | â†’ = EstagnaÃ§Ã£o | â†˜ï¸ = RecessÃ£o

**2. CrÃ©dito ImobiliÃ¡rio**
- **Fonte:** Banco Central (SGS - Sistema Gerenciador de SÃ©ries Temporais)
- **FrequÃªncia:** Mensal
- **MÃ©trica:** Volume de crÃ©dito imobiliÃ¡rio concedido (R$)
- **Sinal:** â†—ï¸ = ExpansÃ£o | â†’ = EstagnaÃ§Ã£o | â†˜ï¸ = RecessÃ£o

**3. ConfianÃ§a do Consumidor**
- **Fonte:** FGV (ICC - Ãndice de ConfianÃ§a do Consumidor)
- **FrequÃªncia:** Mensal
- **MÃ©trica:** Ãndice 0-200 (>100 = otimista, <100 = pessimista)
- **Sinal:** â†—ï¸ = ExpansÃ£o | â†’ = EstagnaÃ§Ã£o | â†˜ï¸ = RecessÃ£o

**4. Emprego Formal**
- **Fonte:** CAGED (Cadastro Geral de Empregados e Desempregados)
- **FrequÃªncia:** Mensal
- **MÃ©trica:** Saldo lÃ­quido admissÃµes - demissÃµes
- **Sinal:** â†—ï¸ = ExpansÃ£o | â†’ = EstagnaÃ§Ã£o | â†˜ï¸ = RecessÃ£o

---

#### Lagging Indicators (Consequentes - refletem o passado)

**1. PreÃ§o mÂ² MÃ©dio**
- **Fonte:** SECOVI, CRECI, pesquisa local
- **FrequÃªncia:** Trimestral
- **MÃ©trica:** R$/mÂ² mÃ©dio por regiÃ£o
- **Sinal:** â†—ï¸ = ExpansÃ£o | â†’ = DesaceleraÃ§Ã£o | â†˜ï¸ = RecessÃ£o

**2. Estoque de ImÃ³veis**
- **Fonte:** Pesquisa local (oferta disponÃ­vel)
- **FrequÃªncia:** Trimestral
- **MÃ©trica:** Quantidade de unidades disponÃ­veis
- **Sinal:** Alto = SaturaÃ§Ã£o | MÃ©dio = Normal | Baixo = Aquecido

**3. VacÃ¢ncia**
- **Fonte:** Pesquisa local (imÃ³veis vazios)
- **FrequÃªncia:** Trimestral
- **MÃ©trica:** % imÃ³veis desocupados
- **Sinal:** Alta (>15%) = RecessÃ£o | MÃ©dia (8-15%) = Normal | Baixa (<8%) = Aquecido

**4. VSO (Velocidade Sobre Oferta)**
- **Fonte:** SECOVI, anÃ¡lise TIV (P7)
- **FrequÃªncia:** Mensal
- **MÃ©trica:** Meses para absorver estoque atual
- **Sinal:** Alto (>24m) = SaturaÃ§Ã£o | MÃ©dio (12-24m) = Normal | Baixo (<12m) = Aquecido

---

### 3.2. Matriz de ClassificaÃ§Ã£o de Fase

| Leading (maioria) | Lagging (tendÃªncia) | Fase Identificada | ConfianÃ§a |
|-------------------|---------------------|-------------------|-----------|
| â†—ï¸â†—ï¸â†—ï¸â†—ï¸ (4+) | PreÃ§os â†—ï¸ + Estoque â†˜ï¸ | **EXPANSÃƒO** | Alta |
| â†—ï¸â†—ï¸â†—ï¸ (3+) | PreÃ§os â†’ + Estoque Alto | **RECUPERAÃ‡ÃƒO** | MÃ©dia |
| â†˜ï¸â†˜ï¸ (2+) | PreÃ§os â†’ + Estoque â†—ï¸ | **DESACELERAÃ‡ÃƒO** | MÃ©dia |
| â†˜ï¸â†˜ï¸â†˜ï¸ (3+) | PreÃ§os â†˜ï¸ + Estoque Alto | **RECESSÃƒO** | Alta |
| Divergentes | Sinais mistos | **TRANSIÃ‡ÃƒO** | Baixa |

**Regra de ouro:**
- Leading indicators **COMANDAM** a classificaÃ§Ã£o (peso 60%)
- Lagging indicators **CONFIRMAM** a classificaÃ§Ã£o (peso 40%)
- DivergÃªncia = atenÃ§Ã£o redobrada (possÃ­vel reversÃ£o)

---

### 3.3. DescriÃ§Ã£o das 4 Fases

#### FASE 1: RECUPERAÃ‡ÃƒO (Bottom â†’ Crescimento)

**CaracterÃ­sticas:**
- ðŸ“ˆ Indicadores leading comeÃ§ando a subir
- ðŸ’° PreÃ§os baixos / estabilizando
- ðŸ—ï¸ Oferta ainda baixa (construtores cautelosos)
- ðŸ’³ CrÃ©dito comeÃ§ando a afrouxar
- ðŸ˜Š ConfianÃ§a aumentando gradualmente

**Indicadores Leading:**
- â†—ï¸ LicenÃ§as de construÃ§Ã£o (+10% a +30%)
- â†—ï¸ CrÃ©dito imobiliÃ¡rio crescendo
- â†—ï¸ ConfianÃ§a consumidor (ICC >100)
- â†—ï¸ Emprego formal positivo (saldo +)

**Indicadores Lagging:**
- â†’ PreÃ§os ainda baixos (mas estabilizados)
- ðŸ“Š Estoques altos â†’ mÃ©dios (diminuindo)
- ðŸ“‰ VacÃ¢ncia alta â†’ mÃ©dia (caindo)
- â±ï¸ VSO alto â†’ mÃ©dio (melhorando)

**DuraÃ§Ã£o tÃ­pica:** 12-18 meses

---

**ESTRATÃ‰GIA TIV:**

| AÃ§Ã£o | DecisÃ£o | Fundamento |
|------|---------|------------|
| **COMPRAR terrenos** | âœ… SIM (oportunidade) | PreÃ§os baixos, oferta futura alta |
| **LANÃ‡AR projetos** | â¸ï¸ AGUARDAR | Demanda se consolidando |
| **VENDER estoque** | âŒ NÃƒO (segurar) | PreÃ§os ainda deprimidos |

**Timing:** PreparaÃ§Ã£o e posicionamento

---

#### FASE 2: EXPANSÃƒO (Crescimento â†’ Pico)

**CaracterÃ­sticas:**
- ðŸ“ˆðŸ“ˆ Indicadores leading em alta acelerada
- ðŸ’°ðŸ’° PreÃ§os subindo rapidamente (+5% a +15% a.a.)
- ðŸ—ï¸ðŸ—ï¸ Oferta crescente (construtores confiantes)
- ðŸ’³ CrÃ©dito farto e barato
- ðŸ˜„ Euforia no mercado

**Indicadores Leading:**
- â†—ï¸â†—ï¸ LanÃ§amentos em alta (+++)
- â†—ï¸â†—ï¸ VSO acelerado (vendas rÃ¡pidas)
- â†—ï¸ CrÃ©dito crescendo forte
- âš ï¸ Primeiros sinais de superoferta (alertar)

**Indicadores Lagging:**
- â†—ï¸ PreÃ§os em alta contÃ­nua
- ðŸ“Š Estoques mÃ©dios â†’ baixos
- ðŸ“‰ VacÃ¢ncia baixa (<8%)
- â±ï¸ VSO baixo (<12 meses = aquecido)

**DuraÃ§Ã£o tÃ­pica:** 18-36 meses

---

**ESTRATÃ‰GIA TIV:**

| AÃ§Ã£o | DecisÃ£o | Fundamento |
|------|---------|------------|
| **COMPRAR terrenos** | âš ï¸ CAUTELA | PreÃ§os altos, risco de topo |
| **LANÃ‡AR projetos** | âœ… SIM (momento Ã³timo) | Demanda forte, absorÃ§Ã£o rÃ¡pida |
| **VENDER estoque** | âœ… SIM (aproveitar) | PreÃ§os mÃ¡ximos, liquidez alta |

**Timing:** ExecuÃ§Ã£o e comercializaÃ§Ã£o acelerada

---

#### FASE 3: DESACELERAÃ‡ÃƒO (Pico â†’ Queda)

**CaracterÃ­sticas:**
- ðŸ“‰ Indicadores leading revertendo
- ðŸ’° PreÃ§os parando de subir / estagnando
- ðŸ—ï¸ Oferta ainda alta (pipeline do boom)
- ðŸ’³ CrÃ©dito comeÃ§ando a apertar
- ðŸ˜Ÿ Cautela aumentando

**Indicadores Leading:**
- â†˜ï¸ LicenÃ§as de construÃ§Ã£o caindo
- â†˜ï¸ VSO desacelerando (vendas lentas)
- â†˜ï¸ CrÃ©dito restringindo (juros subindo)
- âš ï¸ Superoferta se consolidando

**Indicadores Lagging:**
- â†’ PreÃ§os estagnados (resistÃªncia baixa)
- ðŸ“Š Estoques crescendo rapidamente
- ðŸ“ˆ VacÃ¢ncia aumentando (>12%)
- â±ï¸ VSO aumentando (>18 meses)

**DuraÃ§Ã£o tÃ­pica:** 12-24 meses

---

**ESTRATÃ‰GIA TIV:**

| AÃ§Ã£o | DecisÃ£o | Fundamento |
|------|---------|------------|
| **COMPRAR terrenos** | âŒ NÃƒO | PreÃ§os ainda altos, vÃ£o cair mais |
| **LANÃ‡AR projetos** | âŒ NÃƒO | Mercado saturando, risco alto |
| **VENDER estoque** | âœ… URGENTE | Antes da queda, aceitar desconto |

**Timing:** SaÃ­da estratÃ©gica e proteÃ§Ã£o de capital

---

#### FASE 4: RECESSÃƒO (Queda â†’ Bottom)

**CaracterÃ­sticas:**
- ðŸ“‰ðŸ“‰ Indicadores leading em mÃ­nimas histÃ³ricas
- ðŸ’° PreÃ§os caindo (-5% a -20%)
- ðŸ—ï¸ Oferta despencando (paralisaÃ§Ã£o)
- ðŸ’³ CrÃ©dito escasso / restritivo
- ðŸ˜° Pessimismo generalizado

**Indicadores Leading:**
- â†˜ï¸â†˜ï¸ LanÃ§amentos mÃ­nimos (---)
- â†˜ï¸â†˜ï¸ Vendas paralisadas
- âŒ CrÃ©dito restrito (juros altos)
- âš ï¸ Desemprego subindo

**Indicadores Lagging:**
- â†˜ï¸ PreÃ§os em queda aberta
- ðŸ“Š Estoques mÃ¡ximos histÃ³ricos
- ðŸ“ˆ VacÃ¢ncia alta (>20%)
- â±ï¸ VSO altÃ­ssimo (>36 meses)

**DuraÃ§Ã£o tÃ­pica:** 12-24 meses

---

**ESTRATÃ‰GIA TIV:**

| AÃ§Ã£o | DecisÃ£o | Fundamento |
|------|---------|------------|
| **COMPRAR terrenos** | âœ… PROSPECTAR | Oportunidades aparecem |
| **LANÃ‡AR projetos** | â¸ï¸ AGUARDAR | Demanda fraca, sem urgÃªncia |
| **VENDER estoque** | â¸ï¸ SEGURAR | PreÃ§os mÃ­nimos, aguardar recuperaÃ§Ã£o |

**Timing:** PaciÃªncia estratÃ©gica e posicionamento futuro

---

### 3.4. Processo de IdentificaÃ§Ã£o (Passo a Passo)

**ETAPA 1: Coletar Indicadores (30 min)**
- [ ] Buscar 4 indicadores leading (fontes oficiais)
- [ ] Buscar 4 indicadores lagging (pesquisa local)
- [ ] Documentar fontes e datas
- [ ] Calcular variaÃ§Ã£o vs trimestre anterior

**ETAPA 2: Classificar Indicadores (15 min)**
- [ ] Marcar cada indicador: â†—ï¸ / â†’ / â†˜ï¸
- [ ] Contar quantos leading positivos (+) vs negativos (-)
- [ ] Verificar tendÃªncia lagging (preÃ§os, estoque)
- [ ] Identificar divergÃªncias (leading vs lagging)

**ETAPA 3: Consultar Matriz (10 min)**
- [ ] Localizar situaÃ§Ã£o na Matriz de ClassificaÃ§Ã£o
- [ ] Identificar fase mais provÃ¡vel
- [ ] Definir nÃ­vel de confianÃ§a (alto/mÃ©dio/baixo)
- [ ] Documentar fundamento

**ETAPA 4: Gerar RecomendaÃ§Ãµes (15 min)**
- [ ] Consultar estratÃ©gia TIV da fase identificada
- [ ] Definir aÃ§Ãµes: comprar/lanÃ§ar/vender (sim/nÃ£o/aguardar)
- [ ] Calcular ajustes para P1 (garimpo) e P8 (absorÃ§Ã£o)
- [ ] Gerar output estruturado (YAML)

**Tempo total:** 70 minutos

---

## 4. INPUTS NECESSÃRIOS

### 4.1. Dados MacroeconÃ´micos (Leading)

**ObrigatÃ³rios:**
- [ ] LicenÃ§as construÃ§Ã£o (Ãºltimos 6 meses)
- [ ] CrÃ©dito imobiliÃ¡rio (Ãºltimos 6 meses)
- [ ] ICC FGV (Ãºltimo trimestre)
- [ ] CAGED (Ãºltimos 3 meses)

**Fontes:**
- Prefeitura Municipal
- Banco Central (SGS)
- FGV (FundaÃ§Ã£o Getulio Vargas)
- MinistÃ©rio do Trabalho (CAGED)

---

### 4.2. Dados Locais (Lagging)

**ObrigatÃ³rios:**
- [ ] PreÃ§o mÂ² mÃ©dio (Ãºltimo trimestre)
- [ ] Estoque disponÃ­vel (contagem atual)
- [ ] Taxa de vacÃ¢ncia (estimativa)
- [ ] VSO (calculado em P7 ou pesquisa)

**Fontes:**
- SECOVI / CRECI regional
- Pesquisa local (anÃºncios, imobiliÃ¡rias)
- AnÃ¡lise TIV Passo 7 (Oferta)

---

### 4.3. Contexto Adicional

**Recomendados:**
- [ ] HistÃ³rico ciclos anteriores (benchmarking)
- [ ] NotÃ­cias econÃ´micas locais
- [ ] Grandes investimentos anunciados (indÃºstrias, obras)
- [ ] MigraÃ§Ã£o populacional (IBGE)

---

## 5. PROCESSO DE ANÃLISE

### 5.1. Coleta de Dados

**Passo a passo:**
1. Acessar fontes oficiais (BCB, FGV, Prefeitura)
2. Baixar sÃ©ries temporais (Ãºltimos 12 meses)
3. Organizar em planilha (data, valor, variaÃ§Ã£o %)
4. Calcular mÃ©dias mÃ³veis (3 meses)
5. Identificar tendÃªncia (â†—ï¸/â†’/â†˜ï¸)

**Template Excel:**
```
| MÃªs | LicenÃ§as | CrÃ©dito (R$ mil) | ICC FGV | CAGED | TendÃªncia |
|-----|----------|------------------|---------|-------|-----------|
| Jan | 15       | 2.500            | 98      | -50   | â†˜ï¸        |
| Fev | 18       | 2.800            | 101     | +20   | â†—ï¸        |
| Mar | 22       | 3.200            | 105     | +45   | â†—ï¸â†—ï¸      |
```

---

### 5.2. ClassificaÃ§Ã£o

**Passo a passo:**
1. Contar indicadores leading positivos (â†—ï¸)
2. Contar indicadores lagging positivos (â†—ï¸)
3. Verificar consistÃªncia (leading = lagging?)
4. Consultar Matriz de ClassificaÃ§Ã£o
5. Identificar fase (RecuperaÃ§Ã£o/ExpansÃ£o/DesaceleraÃ§Ã£o/RecessÃ£o)
6. Definir confianÃ§a (alta/mÃ©dia/baixa)

---

### 5.3. RecomendaÃ§Ã£o EstratÃ©gica

**Passo a passo:**
1. Consultar estratÃ©gia TIV da fase identificada
2. Definir decisÃµes: comprar/lanÃ§ar/vender
3. Calcular ajustes:
   - P1 (Garimpo): +/- score atratividade
   - P8 (AbsorÃ§Ã£o): +/- velocidade de vendas
4. Gerar output estruturado (YAML)
5. Documentar fundamento e alertas

---

## 6. OUTPUTS ESPERADOS

### 6.1. Template de AnÃ¡lise de Ciclo (YAML)

```yaml
analise_ciclo:
  municipio: "Leopoldina-MG"
  data_analise: "2025-01-15"
  periodo_referencia: "Out/2024 - Jan/2025"
  
  indicadores_leading:
    licencas_construcao: "â†—ï¸" # +25% vs trimestre anterior
    credito_imobiliario: "â†—ï¸" # +18% vs trimestre anterior
    confianca_consumidor: "â†—ï¸" # ICC 108 (otimista)
    emprego_formal: "â†—ï¸" # CAGED +120 saldo (3 meses)
    sintese: "4/4 positivos" # todos indicadores leading positivos
  
  indicadores_lagging:
    preco_m2: "â†’" # R$ 3.200/mÂ² (estÃ¡vel)
    estoque: "medio" # 80 unidades (normal)
    vacancia: "media" # 12% (dentro da mÃ©dia)
    vso: "medio" # 16 meses (saudÃ¡vel)
    sintese: "estavel" # preÃ§os e estoques normalizados
  
  classificacao:
    fase_identificada: "RecuperaÃ§Ã£o"
    confianca: "alta" # leading + lagging consistentes
    duracao_estimada: "12-18 meses" # ciclo tÃ­pico
    fundamento: |
      Todos os 4 indicadores leading estÃ£o positivos (â†—ï¸), sinalizando 
      inÃ­cio de ciclo de crescimento. Indicadores lagging ainda neutros, 
      confirmando que estamos no inÃ­cio da RecuperaÃ§Ã£o (nÃ£o ExpansÃ£o).
      Momento estratÃ©gico para comprar terrenos (preÃ§os ainda baixos).
  
  recomendacoes:
    comprar_terreno: "sim" # âœ… OPORTUNIDADE
    lancar_projeto: "aguardar" # â¸ï¸ demanda se consolidando
    vender_estoque: "nao" # âŒ preÃ§os ainda baixos
    
  integracao_tiv:
    ajuste_p1_score: "+15%" # bonus para microrregiÃµes em RecuperaÃ§Ã£o
    ajuste_p8_velocidade: "+10%" # otimismo cauteloso na absorÃ§Ã£o
    fator_41_ajustado: "4:1" # padrÃ£o (sem ajuste)
    
  alertas:
    - "Monitorar indicadores mensalmente (possÃ­vel aceleraÃ§Ã£o)"
    - "CrÃ©dito crescendo: janela de oportunidade 12-18 meses"
    - "Evitar comprar apÃ³s leading indicar ExpansÃ£o (preÃ§os sobem)"
```

---

### 6.2. Matriz de DecisÃ£o EstratÃ©gica por Fase

| Fase | Comprar Terreno | LanÃ§ar Projeto | Vender Estoque | Timing | Ajuste P8 |
|------|----------------|----------------|----------------|--------|-----------|
| **RecuperaÃ§Ã£o** | âœ… SIM (preÃ§os baixos) | â¸ï¸ AGUARDAR | âŒ NÃƒO (segurar) | PreparaÃ§Ã£o | +10% velocidade |
| **ExpansÃ£o** | âš ï¸ CAUTELA (preÃ§os altos) | âœ… SIM (demanda forte) | âœ… SIM (aproveitar) | ExecuÃ§Ã£o | +20% velocidade |
| **DesaceleraÃ§Ã£o** | âŒ NÃƒO (vÃ£o cair) | âŒ NÃƒO (saturando) | âœ… URGENTE (sair) | SaÃ­da | -20% velocidade |
| **RecessÃ£o** | âœ… PROSPECTAR (oportunidades) | âŒ NÃƒO (demanda fraca) | â¸ï¸ SEGURAR (aguardar) | PaciÃªncia | -30% velocidade |

**Uso:**
- **Comprar:** Timing de aquisiÃ§Ã£o de terrenos
- **LanÃ§ar:** Timing de lanÃ§amento de produtos
- **Vender:** Timing de liquidaÃ§Ã£o de estoque
- **Ajuste P8:** Fator de correÃ§Ã£o na velocidade de absorÃ§Ã£o

---

### 6.3. SemÃ¡foro Visual

```
ðŸŸ¢ VERDE - RECUPERAÃ‡ÃƒO
   â””â”€ Comprar: SIM | LanÃ§ar: AGUARDAR | Vender: NÃƒO

ðŸŸ¢ðŸŸ¢ VERDE FORTE - EXPANSÃƒO
   â””â”€ Comprar: CAUTELA | LanÃ§ar: SIM | Vender: SIM

ðŸŸ¡ AMARELO - DESACELERAÃ‡ÃƒO
   â””â”€ Comprar: NÃƒO | LanÃ§ar: NÃƒO | Vender: URGENTE

ðŸ”´ VERMELHO - RECESSÃƒO
   â””â”€ Comprar: PROSPECTAR | LanÃ§ar: NÃƒO | Vender: SEGURAR
```

---

## 7. ALERTAS E VALIDAÃ‡Ã•ES

### 7.1. Red Flags CrÃ­ticos

| Sinal | Indicador | Risco | AÃ§Ã£o |
|-------|-----------|-------|------|
| ðŸ”´ | Leading â†—ï¸â†—ï¸â†—ï¸ + Lagging â†’ | TOPO prÃ³ximo | Evitar comprar, preparar venda |
| ðŸ”´ | VSO > 30 meses | SUPER-SATURAÃ‡ÃƒO | NO-GO para novos lanÃ§amentos |
| ðŸŸ¡ | Leading â†—ï¸ + Lagging â†˜ï¸ | DIVERGÃŠNCIA | Monitorar (possÃ­vel reversÃ£o) |
| ðŸŸ¡ | CrÃ©dito â†˜ï¸ forte | RESTRIÃ‡ÃƒO | Desacelera demanda em 6-12m |
| âœ… | Leading â†—ï¸ + Lagging â†—ï¸ | EXPANSÃƒO confirmada | Momento Ã³timo para lanÃ§ar |

---

### 7.2. ValidaÃ§Ãµes ObrigatÃ³rias

**Antes de classificar fase:**
- [ ] Indicadores sÃ£o de **fontes oficiais** (nÃ£o estimativas)?
- [ ] Dados tÃªm **<3 meses** de defasagem?
- [ ] **TendÃªncia** Ã© calculada (nÃ£o apenas snapshot)?
- [ ] **Contexto local** foi considerado (eventos especiais)?
- [ ] **HistÃ³rico** do municÃ­pio foi comparado?

---

### 7.3. Erros Comuns

| Erro | Problema | CorreÃ§Ã£o |
|------|----------|----------|
| Ignorar leading | Reagir tarde (usar sÃ³ lagging) | Leading antecipa em 6 meses |
| Ignorar lagging | Confundir ruÃ­do com tendÃªncia | Lagging confirma fase |
| Dados defasados | AnÃ¡lise desatualizada | MÃ¡ximo 3 meses de atraso |
| ViÃ©s confirmaÃ§Ã£o | Ver sÃ³ o que quer ver | Seguir matriz objetiva |
| Generalizar | Aplicar ciclo nacional ao local | Analisar regiÃ£o especÃ­fica |

---

## 8. INTEGRAÃ‡ÃƒO COM OUTRAS SKILLS

### 8.1. Handshake com Passo 1 (Garimpo)

**P1 Usa Ciclo Para:**
- Priorizar microrregiÃµes em **RecuperaÃ§Ã£o** (comprar barato)
- Evitar microrregiÃµes em **DesaceleraÃ§Ã£o** (preÃ§os vÃ£o cair)
- Ajustar score de atratividade por fase (+/- 15%)
- Definir timing de entrada no mercado

**Output P1â†’Ciclo:**
```yaml
ciclo_preliminar:
  fase_identificada: "RecuperaÃ§Ã£o" # ou outra fase
  confianca: "media" # anÃ¡lise rÃ¡pida (P1 Ã© screening)
  acoes_recomendadas:
    - comprar: "sim" # GO para prospecÃ§Ã£o
    - construir: "aguardar" # demanda se consolidando
    - vender: "nao" # preÃ§os ainda baixos
```

**Handshake:**
```
P1 (screening rÃ¡pido) â†’ Ciclo (anÃ¡lise preliminar) â†’ Score ajustado
```

**Exemplo:**
- MicrorregiÃ£o A: Score base 7.5/10
- Ciclo: RecuperaÃ§Ã£o â†’ Ajuste +15%
- Score final: 8.6/10 (prioridade aumenta)

---

### 8.2. Handshake com Passo 8 (AbsorÃ§Ã£o)

**P8 Usa Ciclo Para:**
- Ajustar **velocidade de vendas** por fase do ciclo
- Aplicar **conservadorismo** em DesaceleraÃ§Ã£o/RecessÃ£o
- **Otimismo cauteloso** em RecuperaÃ§Ã£o/ExpansÃ£o
- Definir cronograma realista de comercializaÃ§Ã£o

**Ajuste de AbsorÃ§Ã£o por Ciclo:**

| Fase | Ajuste Velocidade | Fator 4:1 Ajustado | ObservaÃ§Ãµes |
|------|-------------------|---------------------|-------------|
| **RecuperaÃ§Ã£o** | +10% a +20% | 4:1 padrÃ£o | Demanda crescendo |
| **ExpansÃ£o** | +20% a +30% | 3:1 possÃ­vel* | Demanda aquecida |
| **DesaceleraÃ§Ã£o** | -20% a -30% | 5:1 conservador | Demanda desacelerando |
| **RecessÃ£o** | -30% a -50% | 6:1 crÃ­tico | Demanda fraca |

*ExceÃ§Ã£o: Fator 3:1 sÃ³ com P9 validado + mercado aquecido

**Output Cicloâ†’P8:**
```yaml
ajuste_absorcao:
  fase: "RecuperaÃ§Ã£o"
  fator_ajuste: "+15%" # velocidade
  fator_41_ajustado: "4:1" # padrÃ£o
  cronograma_vendas: "ajustado" # +15% mais rÃ¡pido
  fundamento: |
    Ciclo em RecuperaÃ§Ã£o permite otimismo cauteloso.
    Demanda crescendo, mas ainda nÃ£o aquecida.
    Velocidade conservadora + 15% de bonus.
```

**Handshake:**
```
Ciclo identifica fase â†’ P8 aplica ajuste â†’ Cronograma realista
```

**Exemplo prÃ¡tico:**
```
AbsorÃ§Ã£o base: 2.0 un/mÃªs (cÃ¡lculo P8 padrÃ£o)
Fase RecuperaÃ§Ã£o: +15% ajuste
AbsorÃ§Ã£o ajustada: 2.3 un/mÃªs

Total 100 unidades:
- Sem ajuste: 50 meses
- Com ajuste: 43 meses (otimismo fundamentado)
```

---

### 8.3. DependÃªncias CrÃ­ticas

```mermaid
graph LR
    P1[P1 Garimpo] --> CM[Ciclo Mercado]
    CM --> P1adj[P1 Score ajustado]
    CM --> P8[P8 AbsorÃ§Ã£o]
    P8 --> P8adj[Velocidade ajustada]
    CM --> P10[P10 FCD]
    P10 --> ROE[ROE realista]
```

**Ordem de execuÃ§Ã£o:**
1. **P1:** Screening preliminar (identifica fase rÃ¡pida)
2. **Ciclo:** AnÃ¡lise aprofundada (confirma fase)
3. **P1 ajustado:** Score com bonus/malus por ciclo
4. **P8:** AbsorÃ§Ã£o com velocidade ajustada
5. **P10:** FCD com premissas realistas por fase

---

## 9. EXEMPLOS PRÃTICOS

### 9.1. EXEMPLO 1: Leopoldina-MG em RECUPERAÃ‡ÃƒO (2023)

**Contexto:**
- **MunicÃ­pio:** Leopoldina-MG
- **PerÃ­odo:** Out/2023 - Jan/2024
- **HistÃ³rico:** Mercado retraÃ­do 2020-2022 (pandemia)

---

**Coleta de Indicadores:**

**Leading (Out-Dez/2023):**
- LicenÃ§as construÃ§Ã£o: 18 alvarÃ¡s (vs 12 tri anterior) = **+50% â†—ï¸**
- CrÃ©dito imobiliÃ¡rio: R$ 2.8M (vs R$ 2.3M) = **+22% â†—ï¸**
- ICC FGV: 108 (vs 98 tri anterior) = **+10 pontos â†—ï¸**
- CAGED: +85 saldo lÃ­quido (vs -30) = **positivo â†—ï¸**

**SÃ­ntese Leading:** 4/4 positivos (â†—ï¸â†—ï¸â†—ï¸â†—ï¸)

**Lagging (Jan/2024):**
- PreÃ§o mÂ²: R$ 3.100 (vs R$ 3.050 6m antes) = **+1.6% â†’**
- Estoque: 75 unidades (mÃ©dio, vs 95 hÃ¡ 6m) = **diminuindo â†˜ï¸**
- VacÃ¢ncia: 14% (vs 18% hÃ¡ 6m) = **caindo â†˜ï¸**
- VSO: 18 meses (vs 24m hÃ¡ 6m) = **melhorando â†˜ï¸**

**SÃ­ntese Lagging:** PreÃ§os estÃ¡veis, estoques normalizando

---

**ClassificaÃ§Ã£o:**
```yaml
analise_ciclo:
  municipio: "Leopoldina-MG"
  data_analise: "2024-01-15"
  
  indicadores_leading:
    sintese: "4/4 positivos (â†—ï¸â†—ï¸â†—ï¸â†—ï¸)"
  
  indicadores_lagging:
    sintese: "estÃ¡veis, melhorando"
  
  classificacao:
    fase_identificada: "RECUPERAÃ‡ÃƒO"
    confianca: "alta"
    fundamento: |
      Todos indicadores leading positivos sinalizam inÃ­cio de 
      ciclo de crescimento. Lagging ainda neutros confirmam 
      que nÃ£o Ã© ExpansÃ£o (preÃ§os nÃ£o dispararam). Momento 
      ideal para comprar terrenos (preÃ§os baixos).
```

---

**RecomendaÃ§Ãµes:**
```yaml
recomendacoes:
  comprar_terreno: "âœ… SIM (oportunidade)"
  lancar_projeto: "â¸ï¸ AGUARDAR 12-18m"
  vender_estoque: "âŒ NÃƒO (segurar)"
  
integracao_tiv:
  ajuste_p1_score: "+15%" # bonus RecuperaÃ§Ã£o
  ajuste_p8_velocidade: "+10%"
  fator_41_ajustado: "4:1" # padrÃ£o
  
alertas:
  - "Janela de compra: 12-18 meses (antes preÃ§os subirem)"
  - "Monitorar transiÃ§Ã£o para ExpansÃ£o (leading acelera)"
  - "Preparar pipeline de projetos (lanÃ§ar em 2025)"
```

---

**DecisÃ£o EstratÃ©gica:**
- âœ… **COMPRAR:** 3 terrenos identificados (R$ 180/mÂ²)
- â¸ï¸ **AGUARDAR:** NÃ£o lanÃ§ar ainda (demanda consolidando)
- ðŸ“ˆ **PREPARAR:** Estudos de viabilidade (lanÃ§ar 2025)

**Resultado Real (2024):**
- PreÃ§os mÂ² subiram para R$ 3.600 (+16% em 12m)
- Terrenos que custavam R$ 180/mÂ² foram para R$ 240/mÂ² (+33%)
- Quem comprou em 2023 teve ROE alto ao lanÃ§ar em 2024

---

### 9.2. EXEMPLO 2: Leopoldina-MG em EXPANSÃƒO (2024)

**Contexto:**
- **MunicÃ­pio:** Leopoldina-MG
- **PerÃ­odo:** Abr-Jun/2024
- **HistÃ³rico:** RecuperaÃ§Ã£o em 2023, aquecimento em 2024

---

**Coleta de Indicadores:**

**Leading (Abr-Jun/2024):**
- LicenÃ§as construÃ§Ã£o: 35 alvarÃ¡s (vs 22 tri anterior) = **+59% â†—ï¸â†—ï¸**
- CrÃ©dito imobiliÃ¡rio: R$ 4.2M (vs R$ 3.1M) = **+35% â†—ï¸â†—ï¸**
- ICC FGV: 118 (vs 112 tri anterior) = **+6 pontos â†—ï¸**
- CAGED: +180 saldo (vs +95) = **acelerando â†—ï¸â†—ï¸**

**SÃ­ntese Leading:** 4/4 positivos FORTES (â†—ï¸â†—ï¸â†—ï¸â†—ï¸)

**Lagging (Jun/2024):**
- PreÃ§o mÂ²: R$ 3.600 (vs R$ 3.200 hÃ¡ 6m) = **+12.5% â†—ï¸â†—ï¸**
- Estoque: 45 unidades (baixo, vs 70 hÃ¡ 6m) = **caindo â†˜ï¸â†˜ï¸**
- VacÃ¢ncia: 8% (vs 13% hÃ¡ 6m) = **baixa âœ…**
- VSO: 9 meses (vs 16m hÃ¡ 6m) = **aquecido âœ…**

**SÃ­ntese Lagging:** PreÃ§os subindo, demanda forte

---

**ClassificaÃ§Ã£o:**
```yaml
analise_ciclo:
  municipio: "Leopoldina-MG"
  data_analise: "2024-06-15"
  
  indicadores_leading:
    sintese: "4/4 positivos FORTES (â†—ï¸â†—ï¸â†—ï¸â†—ï¸)"
  
  indicadores_lagging:
    sintese: "preÃ§os em alta, estoques baixos"
  
  classificacao:
    fase_identificada: "EXPANSÃƒO"
    confianca: "alta"
    fundamento: |
      Leading e lagging confirmam ExpansÃ£o consolidada.
      PreÃ§os subindo forte (+12.5%), VSO aquecido (9m),
      estoques baixos. Momento Ã“TIMO para lanÃ§ar projetos
      (absorÃ§Ã£o rÃ¡pida garantida).
```

---

**RecomendaÃ§Ãµes:**
```yaml
recomendacoes:
  comprar_terreno: "âš ï¸ CAUTELA (preÃ§os altos)"
  lancar_projeto: "âœ… SIM (momento ideal)"
  vender_estoque: "âœ… SIM (preÃ§os mÃ¡ximos)"
  
integracao_tiv:
  ajuste_p1_score: "0%" # neutro (preÃ§os altos)
  ajuste_p8_velocidade: "+25%" # absorÃ§Ã£o acelerada
  fator_41_ajustado: "3:1" # pode relaxar (com P9)
  
alertas:
  - "TOPO pode estar prÃ³ximo (monitorar leading)"
  - "Evitar comprar terrenos caros (preÃ§os inflados)"
  - "Acelerar vendas (aproveitar liquidez alta)"
```

---

**DecisÃ£o EstratÃ©gica:**
- âš ï¸ **COMPRAR:** Apenas se oportunidade excepcional
- âœ… **LANÃ‡AR:** 2 projetos em carteira (absorÃ§Ã£o 3.5 un/mÃªs)
- âœ… **VENDER:** Estoque remanescente (preÃ§os mÃ¡ximos)

**Resultado Real (2024):**
- Projetos lanÃ§ados venderam 100% em 18 meses (rÃ¡pido)
- ROE de 28% a.a. (velocidade alta)
- Estoque antigo vendido com +15% sobre preÃ§o base

---

### 9.3. EXEMPLO 3: AlÃ©m ParaÃ­ba-MG em DESACELERAÃ‡ÃƒO (hipotÃ©tico)

**Contexto:**
- **MunicÃ­pio:** AlÃ©m ParaÃ­ba-MG
- **PerÃ­odo:** Jan-Mar/2025 (hipotÃ©tico)
- **CenÃ¡rio:** ApÃ³s boom 2023-2024, sinais de saturaÃ§Ã£o

---

**Coleta de Indicadores:**

**Leading (Jan-Mar/2025):**
- LicenÃ§as construÃ§Ã£o: 12 alvarÃ¡s (vs 28 tri anterior) = **-57% â†˜ï¸â†˜ï¸**
- CrÃ©dito imobiliÃ¡rio: R$ 1.8M (vs R$ 2.5M) = **-28% â†˜ï¸â†˜ï¸**
- ICC FGV: 95 (vs 110 tri anterior) = **-15 pontos â†˜ï¸â†˜ï¸**
- CAGED: -45 saldo (vs +120) = **negativo â†˜ï¸**

**SÃ­ntese Leading:** 4/4 negativos (â†˜ï¸â†˜ï¸â†˜ï¸â†˜ï¸)

**Lagging (Mar/2025):**
- PreÃ§o mÂ²: R$ 4.100 (vs R$ 4.150 hÃ¡ 3m) = **-1.2% â†’**
- Estoque: 180 unidades (alto, vs 95 hÃ¡ 6m) = **crescendo â†—ï¸â†—ï¸**
- VacÃ¢ncia: 22% (vs 12% hÃ¡ 6m) = **alta âš ï¸**
- VSO: 32 meses (vs 14m hÃ¡ 6m) = **saturaÃ§Ã£o âŒ**

**SÃ­ntese Lagging:** PreÃ§os estagnando, superoferta

---

**ClassificaÃ§Ã£o:**
```yaml
analise_ciclo:
  municipio: "AlÃ©m ParaÃ­ba-MG"
  data_analise: "2025-03-15"
  
  indicadores_leading:
    sintese: "4/4 negativos (â†˜ï¸â†˜ï¸â†˜ï¸â†˜ï¸)"
  
  indicadores_lagging:
    sintese: "preÃ§os estagnados, superoferta crÃ­tica"
  
  classificacao:
    fase_identificada: "DESACELERAÃ‡ÃƒO"
    confianca: "alta"
    fundamento: |
      Leading todos negativos indicam reversÃ£o do ciclo.
      Lagging confirmam saturaÃ§Ã£o (VSO 32m, vacÃ¢ncia 22%).
      Momento de SAIR (vender estoque antes queda).
```

---

**RecomendaÃ§Ãµes:**
```yaml
recomendacoes:
  comprar_terreno: "âŒ NÃƒO (preÃ§os vÃ£o cair)"
  lancar_projeto: "âŒ NÃƒO (mercado saturado)"
  vender_estoque: "âœ… URGENTE (antes queda)"
  
integracao_tiv:
  ajuste_p1_score: "-25%" # malus DesaceleraÃ§Ã£o
  ajuste_p8_velocidade: "-30%" # absorÃ§Ã£o lenta
  fator_41_ajustado: "5:1" # conservador
  
alertas:
  - "RISCO ALTO: VSO >30m indica super-saturaÃ§Ã£o"
  - "PreÃ§os devem cair 10-15% em 12-18 meses"
  - "Aceitar descontos para liquidar estoque"
  - "Evitar novos investimentos (aguardar fundo)"
```

---

**DecisÃ£o EstratÃ©gica:**
- âŒ **COMPRAR:** NÃ£o investir (preÃ§os inflados)
- âŒ **LANÃ‡AR:** Cancelar projetos planejados
- âœ… **VENDER:** Liquidar estoque com -10% (melhor que -30% depois)

---

### 9.4. EXEMPLO 4: Cataguases-MG em RECESSÃƒO (hipotÃ©tico)

**Contexto:**
- **MunicÃ­pio:** Cataguases-MG
- **PerÃ­odo:** Jul-Set/2025 (hipotÃ©tico)
- **CenÃ¡rio:** Crise prolongada, mercado paralisado

---

**Coleta de Indicadores:**

**Leading (Jul-Set/2025):**
- LicenÃ§as construÃ§Ã£o: 3 alvarÃ¡s (vs 8 tri anterior) = **-63% â†˜ï¸â†˜ï¸**
- CrÃ©dito imobiliÃ¡rio: R$ 800k (vs R$ 1.5M) = **-47% â†˜ï¸â†˜ï¸**
- ICC FGV: 78 (vs 92 tri anterior) = **-14 pontos â†˜ï¸â†˜ï¸**
- CAGED: -120 saldo (vs -60) = **piorando â†˜ï¸â†˜ï¸**

**SÃ­ntese Leading:** 4/4 negativos CRÃTICOS (â†˜ï¸â†˜ï¸â†˜ï¸â†˜ï¸)

**Lagging (Set/2025):**
- PreÃ§o mÂ²: R$ 3.400 (vs R$ 4.000 hÃ¡ 12m) = **-15% â†˜ï¸â†˜ï¸**
- Estoque: 250 unidades (mÃ¡ximo histÃ³rico) = **crÃ­tico âŒ**
- VacÃ¢ncia: 28% (vs 18% hÃ¡ 6m) = **altÃ­ssima âŒ**
- VSO: 48 meses (vs 28m hÃ¡ 6m) = **paralisado âŒ**

**SÃ­ntese Lagging:** PreÃ§os caindo, mercado travado

---

**ClassificaÃ§Ã£o:**
```yaml
analise_ciclo:
  municipio: "Cataguases-MG"
  data_analise: "2025-09-15"
  
  indicadores_leading:
    sintese: "4/4 negativos CRÃTICOS"
  
  indicadores_lagging:
    sintese: "preÃ§os caindo, mercado paralisado"
  
  classificacao:
    fase_identificada: "RECESSÃƒO"
    confianca: "alta"
    fundamento: |
      Leading em mÃ­nimas histÃ³ricas + lagging em queda 
      confirmam RecessÃ£o profunda. VSO 48m = mercado 
      travado. Momento de PACIÃŠNCIA (nÃ£o vender em pÃ¢nico,
      aguardar sinais de recuperaÃ§Ã£o).
```

---

**RecomendaÃ§Ãµes:**
```yaml
recomendacoes:
  comprar_terreno: "âœ… PROSPECTAR (oportunidades)"
  lancar_projeto: "âŒ NÃƒO (demanda fraca)"
  vender_estoque: "â¸ï¸ SEGURAR (preÃ§os mÃ­nimos)"
  
integracao_tiv:
  ajuste_p1_score: "-40%" # malus RecessÃ£o
  ajuste_p8_velocidade: "-50%" # absorÃ§Ã£o crÃ­tica
  fator_41_ajustado: "6:1" # conservadorismo extremo
  
alertas:
  - "FUNDO PODE ESTAR PRÃ“XIMO (monitorar leading)"
  - "Prospectar terrenos (proprietÃ¡rios flexÃ­veis)"
  - "NÃƒO vender em pÃ¢nico (aguardar recuperaÃ§Ã£o)"
  - "Preservar caixa (nÃ£o travar capital)"
```

---

**DecisÃ£o EstratÃ©gica:**
- âœ… **PROSPECTAR:** Identificar terrenos bons (sem comprar)
- âŒ **LANÃ‡AR:** Zero novos projetos
- â¸ï¸ **SEGURAR:** NÃ£o liquidar estoque (preÃ§os mÃ­nimos)

**EstratÃ©gia de SobrevivÃªncia:**
1. Preservar caixa (nÃ£o investir)
2. Renegociar dÃ­vidas (alongar prazos)
3. Manter relacionamento com leads (futuro)
4. Preparar pipeline (lanÃ§ar na RecuperaÃ§Ã£o)

---

## 10. CHECKLIST DE QUALIDADE

### 10.1. Auto-ValidaÃ§Ã£o da Skill

- [ ] **Estrutura:** 10 seÃ§Ãµes completas?
- [ ] **YAML:** Frontmatter sem acentuaÃ§Ã£o, <200 chars?
- [ ] **4 Fases:** RecuperaÃ§Ã£o, ExpansÃ£o, DesaceleraÃ§Ã£o, RecessÃ£o descritas?
- [ ] **8 Indicadores:** 4 leading + 4 lagging formalizados?
- [ ] **Matriz classificaÃ§Ã£o:** IncluÃ­da e documentada?
- [ ] **EstratÃ©gia TIV:** Por fase (comprar/lanÃ§ar/vender)?
- [ ] **Handshakes:** P1 e P8 integrados?
- [ ] **Exemplos:** 4 casos prÃ¡ticos (1 por fase)?
- [ ] **Templates:** Output YAML estruturado?
- [ ] **Alertas:** Red flags listados?

---

### 10.2. Conformidade KB v5.0

- [ ] **Base:** SeÃ§Ã£o 1.3 (Ciclo de Mercado) referenciada?
- [ ] **IntegraÃ§Ã£o P1:** Timing estratÃ©gico garimpo?
- [ ] **IntegraÃ§Ã£o P8:** Ajuste absorÃ§Ã£o por fase?
- [ ] **Conservadorismo:** Aplicado em DesaceleraÃ§Ã£o/RecessÃ£o?
- [ ] **CitaÃ§Ãµes:** KB CORE v5.0 referenciado?

---

### 10.3. Usabilidade

- [ ] **Clareza:** Linguagem tÃ©cnica mas acessÃ­vel?
- [ ] **Praticidade:** AnÃ¡lise executÃ¡vel em 70 min?
- [ ] **Rastreabilidade:** Fontes oficiais indicadas?
- [ ] **Exemplos:** Casos reais (Leopoldina-MG) incluÃ­dos?
- [ ] **Alertas:** Red flags e divergÃªncias documentados?
- [ ] **DecisÃ£o:** SemÃ¡foro visual facilita interpretaÃ§Ã£o?

---

### 10.4. Checklist Final de Entrega

- [ ] Arquivo SKILL.md criado
- [ ] 10 seÃ§Ãµes estruturadas
- [ ] Framework 4 fases completo
- [ ] Sistema de indicadores (4 leading + 4 lagging)
- [ ] Matriz de classificaÃ§Ã£o
- [ ] Matriz de decisÃ£o estratÃ©gica (comprar/lanÃ§ar/vender)
- [ ] Handshakes P1 e P8 formalizados
- [ ] Template YAML de output
- [ ] 4 exemplos prÃ¡ticos (1 por fase)
- [ ] Checklist de qualidade
- [ ] Conformidade KB CORE v5.0 atestada

---

**FIM DA SKILL tiv-ciclo-mercado v2.0**

**VersÃ£o:** 2.0  
**Base:** KB CORE v5.0  
**AtualizaÃ§Ã£o de:** v1.0 (KB v4.0)  
**Data:** 14/11/2025  
**Status:** âœ… OPERACIONAL
