---
name: "tiv-passo2-dinamica-economica"
version: "2.0"
description: "AnÃ¡lise da dinÃ¢mica econÃ´mica local atravÃ©s do Framework P2i-Lead ampliado. Mede forÃ§a de consumo e qualidade do ciclo econÃ´mico para balizar vocaÃ§Ã£o, demanda e absorÃ§Ã£o. Passo 2 da Metodologia TIV 4.0."
author: "Metodologia TIV 4.0 + Othon Valentim"
created: "2025-11-12"
updated: "2025-11-12"
tags: ["tiv", "imobiliario", "dinamica-economica", "p2i-lead", "ciclo-mercado"]
priority: "CRÃTICO"
kbcore_version: "4.0"
dependencies: ["tiv-garimpo"]
feeds_into: ["tiv-passo3-area-influencia", "tiv-passo4-vocacao", "tiv-passo6-demanda", "tiv-passo8-absorcao", "tiv-fcd"]
---

# SKILL: AnÃ¡lise da DinÃ¢mica EconÃ´mica (Passo 2 TIV)

## 1. Objetivo e Contexto

### FunÃ§Ã£o na Metodologia TIV

Esta Skill executa o **PASSO 2** dos 10 Passos TIV: AnÃ¡lise da DinÃ¢mica EconÃ´mica Local.

**PosiÃ§Ã£o na sequÃªncia TIV:**
```
PASSO 1: Garimpo Inicial âœ…
PASSO 2: DinÃ¢mica EconÃ´mica â­ (ESTA SKILL)
PASSO 3: Ãrea de InfluÃªncia â†’
PASSO 4: VocaÃ§Ã£o ImobiliÃ¡ria â†’
PASSO 5: Legal e RestriÃ§Ãµes â†’
PASSO 6: Demanda â†’
PASSO 7: Oferta â†’
PASSO 8: AbsorÃ§Ã£o â†’
PASSO 9: ConvalidaÃ§Ã£o â†’
PASSO 10: FCD (Viabilidade) â†’
```

### Por Que Este Passo Ã‰ CrÃ­tico

> **"Quanto mais diversificada [a dinÃ¢mica econÃ´mica] for, mais blindada ela serÃ¡ com relaÃ§Ã£o a risco"**  
> â€” Metodologia TIV 4.0

A dinÃ¢mica econÃ´mica determina:
- âœ… **Capacidade de pagamento** da populaÃ§Ã£o (renda formal relevante?)
- âœ… **Sustentabilidade da demanda** (economia aquecida ou retraindo?)
- âœ… **Velocidade de absorÃ§Ã£o** (famÃ­lias formando ou desfazendo?)
- âœ… **Risco de liquidez** (dependÃªncia de poucos empregadores)
- âœ… **Timing estratÃ©gico** (comprar agora ou esperar?)

**PrincÃ­pio TIV:**
```
Terreno excelente + DinÃ¢mica fraca = PREJUÃZO
Terreno mediano + DinÃ¢mica forte = LUCRO
```

### Perguntas-Guia (Frame de Leitura)

Este Passo 2 responde 4 perguntas crÃ­ticas:

1. **Economia aquecida?** (admissÃµes > demissÃµes; aberturas > fechamentos)
2. **Renda formal relevante?** (% emprego formal 25-59 anos)
3. **Arranjos familiares consolidando?** (casamentos vs divÃ³rcios)
4. **Renda mÃ©dia + Gini** sustentam o preÃ§o-alvo do produto?

---

## 2. Quando Acionar Esta Skill

### Triggers ExplÃ­citos
- "Como estÃ¡ a economia de [municÃ­pio]?"
- "Qual a dinÃ¢mica econÃ´mica da regiÃ£o?"
- "A cidade estÃ¡ crescendo ou retraindo?"
- "O mercado estÃ¡ aquecido?"
- "Qual o perfil de renda da populaÃ§Ã£o?"

### Triggers ImplÃ­citos
- UsuÃ¡rio quer avaliar viabilidade de terreno
- Necessidade de entender timing de mercado
- DÃºvida sobre capacidade de absorÃ§Ã£o local
- AvaliaÃ§Ã£o de risco de investimento

### PrÃ©-Requisitos
âœ… **tiv-garimpo** concluÃ­do (terreno identificado)
âœ… MunicÃ­pio/regiÃ£o definido
âœ… Tipo de produto preliminarmente pensado

### Momento no Fluxo TIV
**PosiÃ§Ã£o:** Passo 2 de 10  
**Criticidade:** ðŸ”´ CRÃTICO - Sem isso, demanda Ã© "chute"  
**DuraÃ§Ã£o:** 4-8 horas de coleta + anÃ¡lise

---

## 3. Framework: P2i-Lead Expandido

### VisÃ£o Geral

**P2i-Lead = PopulaÃ§Ã£o Ã— PirÃ¢mide Ã— Infraestrutura Ã— IndÃºstria + Leading Indicators**

Este framework analisa **16 variÃ¡veis estruturais** organizadas em 4 pilares, complementadas por **indicadores preditivos (leading)** que antecipam mudanÃ§as no ciclo.

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚             FRAMEWORK P2i-LEAD (16 VAR)             â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ POPULAÃ‡ÃƒO (P1) â†’ Tamanho, crescimento, densidade    â”‚
â”‚ PIRÃ‚MIDE (P2)  â†’ Renda, Gini, emprego formal        â”‚
â”‚ INFRAEST. (I1) â†’ Mobilidade, equipamentos, serviÃ§os â”‚
â”‚ INDÃšSTRIA (I2) â†’ DiversificaÃ§Ã£o, setores, empregos  â”‚
â”‚ LEADING (L)    â†’ Indicadores preditivos (PIT/CAGED) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

### 3.1. POPULAÃ‡ÃƒO (P1) - 4 VariÃ¡veis

#### VariÃ¡vel 1: Tamanho Total
- **O que Ã©:** PopulaÃ§Ã£o total do municÃ­pio
- **Fonte:** IBGE (Censo + estimativas anuais)
- **AnÃ¡lise:**
  - < 20.000 hab: Micromercado, demanda limitada
  - 20.000-50.000: Pequeno porte, nichos especÃ­ficos
  - 50.000-100.000: MÃ©dio porte, viÃ¡vel loteamentos
  - \> 100.000: Grande porte, mÃºltiplos produtos

#### VariÃ¡vel 2: Taxa de Crescimento Populacional (TGCA)
- **O que Ã©:** Taxa GeomÃ©trica de Crescimento Anual (2010-2024)
- **Fonte:** IBGE Cidades
- **AnÃ¡lise:**
  - **Negativa ou 0%:** âš ï¸ Red flag - PopulaÃ§Ã£o estagnada/declinante
  - **0-1% a.a.:** Crescimento vegetativo baixo
  - **1-2% a.a.:** Crescimento saudÃ¡vel âœ…
  - **> 2% a.a.:** ExpansÃ£o acelerada (oportunidade)

#### VariÃ¡vel 3: Densidade DemogrÃ¡fica
- **O que Ã©:** PopulaÃ§Ã£o Ã· Ãrea territorial (hab/kmÂ²)
- **Fonte:** IBGE
- **AnÃ¡lise:**
  - Baixa densidade: ExpansÃ£o horizontal viÃ¡vel
  - Alta densidade: PressÃ£o para verticalizaÃ§Ã£o

#### VariÃ¡vel 4: Saldo MigratÃ³rio
- **O que Ã©:** Entrada menos saÃ­da de pessoas
- **Fonte:** Censo IBGE, dados municipais
- **AnÃ¡lise:**
  - **Positivo:** AtraÃ§Ã£o de pessoas (oportunidade econÃ´mica)
  - **Negativo:** âš ï¸ Fuga (alerta de crise)

---

### 3.2. PIRÃ‚MIDE (P2) - 4 VariÃ¡veis

#### VariÃ¡vel 5: DistribuiÃ§Ã£o de Renda (Gini)
- **O que Ã©:** Ãndice de concentraÃ§Ã£o de renda (0 = igualitÃ¡ria; 1 = concentrada)
- **Fonte:** Atlas Brasil, IBGE
- **AnÃ¡lise:**
  - **< 0,45:** Renda bem distribuÃ­da âœ…
  - **0,45-0,55:** ConcentraÃ§Ã£o moderada
  - **> 0,55:** Alta concentraÃ§Ã£o âš ï¸ (demanda concentrada em poucos)

#### VariÃ¡vel 6: Renda MÃ©dia & Renda Mediana
- **O que Ã©:** Renda domiciliar mensal mÃ©dia e mediana
- **Fonte:** IBGE, Prospecta/RAIS
- **AnÃ¡lise:**
  - Renda mÃ©dia R$ 4.000: Produto atÃ© ~R$ 250-300k (regra 30%)
  - Renda mediana < mÃ©dia: ConcentraÃ§Ã£o no topo (atenÃ§Ã£o Gini)

#### VariÃ¡vel 7: Emprego Formal 25-59 anos
- **O que Ã©:** Emprego formal 25-59 / PopulaÃ§Ã£o 25-59
- **Fonte:** RAIS/MTE/P2i, IBGE
- **AnÃ¡lise (CRÃTICO):**
  - **â‰¥ 55%:** SaudÃ¡vel âœ… (mÃ©dia Brasil)
  - **30-54%:** Zona de atenÃ§Ã£o
  - **< 30%:** âš ï¸ Red flag - Renda informal dominante
  - **> 100%:** PopulaÃ§Ã£o flutuante (trabalhadores nÃ£o residentes)

> **"Emprego formal 25-59 / Pop 25-59 Ã© proxy de capacidade de pagamento"**

#### VariÃ¡vel 8: Renda Per Capita
- **O que Ã©:** PIB Ã· PopulaÃ§Ã£o total
- **Fonte:** IBGE Cidades
- **AnÃ¡lise:**
  - Comparar com municÃ­pios pares
  - Cruzar com distribuiÃ§Ã£o (Gini)

---

### 3.3. INFRAESTRUTURA (I1) - 4 VariÃ¡veis

#### VariÃ¡vel 9: Mobilidade
- **O que Ã©:** Qualidade rodovias, transporte pÃºblico, conectividade regional
- **Fonte:** ObservaÃ§Ã£o, dados prefeitura
- **AnÃ¡lise:**
  - Acesso facilitado: Amplia Ã¡rea de influÃªncia
  - Isolamento: Restringe mercado

#### VariÃ¡vel 10: Equipamentos Urbanos
- **O que Ã©:** Hospitais, escolas, shopping, universidades
- **Fonte:** Prefeitura, observaÃ§Ã£o
- **AnÃ¡lise:**
  - Equipamentos consolidados: AtraÃ§Ã£o de moradores
  - CarÃªncia: LimitaÃ§Ã£o de vocaÃ§Ã£o residencial

#### VariÃ¡vel 11: ServiÃ§os BÃ¡sicos
- **O que Ã©:** % atendimento Ã¡gua, esgoto, energia, coleta lixo
- **Fonte:** SNIS, IBGE Cidades
- **AnÃ¡lise:**
  - Cobertura > 90%: Infraestrutura madura âœ…
  - Cobertura < 70%: âš ï¸ LimitaÃ§Ã£o para produtos premium

#### VariÃ¡vel 12: Conectividade
- **O que Ã©:** Internet banda larga, telefonia
- **Fonte:** Anatel, operadoras
- **AnÃ¡lise:**
  - Boa conectividade: Atrai trabalho remoto, famÃ­lias jovens
  - DeficiÃªncia: Limita pÃºblico-alvo

---

### 3.4. INDÃšSTRIA/EMPREGO (I2) - 4 VariÃ¡veis

#### VariÃ¡vel 13: DiversificaÃ§Ã£o EconÃ´mica
- **O que Ã©:** DistribuiÃ§Ã£o PIB por setores (agro, indÃºstria, comÃ©rcio, serviÃ§os)
- **Fonte:** IBGE PIB MunicÃ­pios
- **AnÃ¡lise CRÃTICA:**
  - **Diversificado (4 setores > 15% cada):** âœ… Blindagem anti-risco
  - **Monocultura (1 setor > 70%):** ðŸ”´ CRÃTICO - Risco sistÃªmico
  
> **"Monocultura > 70% em 1 setor = NÃƒO INVESTIR"**

#### VariÃ¡vel 14: Principais Empregadores (Top 10)
- **O que Ã©:** Listagem das 10 maiores empresas empregadoras
- **Fonte:** Prefeitura, associaÃ§Ã£o comercial, RAIS
- **AnÃ¡lise:**
  - **1 empresa > 40% empregos:** ðŸ”´ DependÃªncia crÃ­tica
  - **Top 3 > 60%:** âš ï¸ ConcentraÃ§Ã£o alta
  - **DistribuÃ­do uniformemente:** âœ… ResiliÃªncia

#### VariÃ¡vel 15: Setores Dominantes
- **O que Ã©:** Principais CNAEs por nÃºmero de empregos
- **Fonte:** RAIS/CAGED
- **AnÃ¡lise:**
  - Identificar vulnerabilidades setoriais
  - Exemplo: Turismo sazonal, mineraÃ§Ã£o cÃ­clica

#### VariÃ¡vel 16: DependÃªncias CrÃ­ticas
- **O que Ã©:** IdentificaÃ§Ã£o de pontos Ãºnicos de falha
- **Fonte:** AnÃ¡lise qualitativa
- **Exemplos:**
  - Cidade com 1 usina de aÃ§Ãºcar = risco safra
  - Polo industrial dependente de commodity = risco preÃ§o

---

### 3.5. LEADING INDICATORS (L) - Indicadores Preditivos

**FunÃ§Ã£o:** Antecipar mudanÃ§as no ciclo (6-12 meses Ã  frente)

#### L1: PIT/CAGED (Empregabilidade em Tempo Real)
- **O que Ã©:** Saldo mensal admissÃµes - demissÃµes
- **Fonte:** Painel de Impacto do Trabalho (PIT/CAGED)
- **AnÃ¡lise:**
  - **Saldo positivo 12-24m:** Economia aquecendo âœ…
  - **Saldo negativo persistente:** âš ï¸ RecessÃ£o iniciando
  - **Setores em expansÃ£o:** Oportunidade segmentada

**Como usar:**
- SÃ©ries mensais de 12-24 meses
- Identificar inflexÃµes (viradas de ciclo)
- Cruzar com aberturas/fechamentos de empresas

#### L2: Abertura vs Fechamento de Empresas
- **O que Ã©:** Saldo CNPJs ativos mensalmente
- **Fonte:** Receita Federal, CNPJ
- **AnÃ¡lise:**
  - **Aberturas > Fechamentos:** Empreendedorismo ativo
  - **Fechamentos > Aberturas:** âš ï¸ Liquidez em queda

#### L3: AlvarÃ¡s de ConstruÃ§Ã£o
- **O que Ã©:** NÃºmero de alvarÃ¡s residenciais emitidos
- **Fonte:** Prefeitura Municipal
- **AnÃ¡lise:**
  - Crescimento de alvarÃ¡s: Mercado aquecendo
  - Queda acentuada: Resfriamento futuro

#### L4: Casamentos vs DivÃ³rcios
- **O que Ã©:** ProporÃ§Ã£o casamentos/divÃ³rcios por mil habitantes
- **Fonte:** IBGE, cartÃ³rios
- **AnÃ¡lise:**
  - **Casamentos crescendo:** FormaÃ§Ã£o de lares âœ…
  - **DivÃ³rcios crescendo:** Rotatividade (pode ser oportunidade)
  - **Ambos caindo:** âš ï¸ EstagnaÃ§Ã£o social

---

### 3.6. INDICADORES COMPLEMENTARES

#### Frota Veicular
- **O que Ã©:** VeÃ­culos/domicÃ­lio e % motocicletas
- **Fonte:** DETRAN, IBGE
- **AnÃ¡lise:**
  - **> 1,5 veÃ­c/dom:** Classe mÃ©dia consolidada
  - **< 1,0 veÃ­c/dom:** Perfil popular
  - **Motos > 30-35%:** âš ï¸ ViÃ©s popular (baixo teto de preÃ§o)

#### Endividamento
- **O que Ã©:** NÃ­vel e prazo de endividamento das famÃ­lias
- **Fonte:** Banco Central, Serasa
- **AnÃ¡lise:**
  - Endividamento curto prazo (< 12m): Risco maior inadimplÃªncia
  - Endividamento longo prazo: Ciclo de consumo (24m+)

---

## 4. Inputs NecessÃ¡rios

### Dados ObrigatÃ³rios

**IdentificaÃ§Ã£o do MunicÃ­pio:**
- [ ] Nome do municÃ­pio
- [ ] Estado (UF)
- [ ] RegiÃ£o de referÃªncia (se houver)
- [ ] MunicÃ­pios pares para comparaÃ§Ã£o

**Dados DemogrÃ¡ficos:**
- [ ] PopulaÃ§Ã£o total (Ãºltimo censo + estimativa atual)
- [ ] TGCA 2010-2024
- [ ] Densidade demogrÃ¡fica (hab/kmÂ²)
- [ ] PirÃ¢mide etÃ¡ria (% por faixa: 0-14, 15-24, 25-44, 45-59, 60+)

**Dados EconÃ´micos:**
- [ ] PIB total e per capita
- [ ] PIB por setor (agro, indÃºstria, comÃ©rcio, serviÃ§os)
- [ ] Renda mÃ©dia domiciliar
- [ ] Ãndice de Gini
- [ ] Emprego formal 25-59 / PopulaÃ§Ã£o 25-59

**Dados de Mercado:**
- [ ] Top 10 empregadores (nomes + nÂº empregos)
- [ ] CAGED/PIT Ãºltimos 12-24 meses
- [ ] Aberturas/fechamentos empresas Ãºltimos 12 meses
- [ ] AlvarÃ¡s construÃ§Ã£o residencial Ãºltimos 12-24 meses

**Dados Sociais:**
- [ ] Casamentos anuais (Ãºltimos 4-5 anos)
- [ ] DivÃ³rcios anuais (Ãºltimos 4-5 anos)
- [ ] Frota veicular (total + % motos)

### Fontes de Dados Recomendadas

**Federais (Gratuitas):**
- IBGE Cidades: https://cidades.ibge.gov.br/
- Atlas Brasil: http://atlasbrasil.org.br/
- CAGED/PIT: https://www.gov.br/trabalho-e-emprego/
- Banco Central: https://www.bcb.gov.br/

**Municipais:**
- Prefeitura (Secretaria de Planejamento)
- AssociaÃ§Ã£o Comercial/Industrial
- SINDUSCON local

**Plataformas Especializadas:**
- Prospecta/RAIS/MTE/P2i (dados consolidados)

---

## 5. Processo de AnÃ¡lise (Passo a Passo)

### ETAPA 1: Coleta e ValidaÃ§Ã£o de Dados (2-3h)

**1.1. Buscar dados obrigatÃ³rios nas fontes oficiais**
- Priorizar dados mais recentes (< 2 anos)
- Anotar data de coleta e fonte

**1.2. Validar completude**
- Verificar se hÃ¡ todas as 16 variÃ¡veis P2i
- Identificar lacunas (documentar)

**1.3. Organizar em planilha estruturada**
- Template fornecido na seÃ§Ã£o 10

---

### ETAPA 2: CÃ¡lculo do Score P2i (1-2h)

**2.1. Atribuir scores (0-10) para cada pilar:**

**POPULAÃ‡ÃƒO (0-10):**
- Tamanho: >100k = 10 | 50-100k = 7 | 20-50k = 4 | <20k = 2
- TGCA: >2% = 10 | 1-2% = 7 | 0-1% = 4 | <0% = 0
- Densidade: Avaliar contexto regional
- MigraÃ§Ã£o: Positiva = +2 | Negativa = -2

**PIRÃ‚MIDE (0-10):**
- Gini: <0,45 = 10 | 0,45-0,55 = 6 | >0,55 = 3
- Emprego formal 25-59: â‰¥55% = 10 | 30-54% = 6 | <30% = 2
- Renda mÃ©dia: Comparar com pares (ranking)
- Renda per capita: Idem

**INFRAESTRUTURA (0-10):**
- Cada item (mobilidade, equipamentos, serviÃ§os, conectividade): 0-2,5
- Soma total

**INDÃšSTRIA (0-10):**
- DiversificaÃ§Ã£o: 4 setores > 15% = 10 | Monocultura = 0
- Top 10 distribuÃ­do = 10 | 1 empresa > 40% = 2
- DependÃªncias crÃ­ticas: Nenhuma = +3 | MÃºltiplas = -3

**SCORE TOTAL P2i: [XX]/40**

---

### ETAPA 3: AnÃ¡lise de Leading Indicators (1h)

**3.1. Coletar sÃ©ries temporais (12-24 meses):**
- PIT/CAGED mensal
- Aberturas/fechamentos empresas
- AlvarÃ¡s construÃ§Ã£o
- Casamentos/divÃ³rcios anuais

**3.2. Identificar tendÃªncias:**
- â†—ï¸ Crescendo | â†’ EstÃ¡vel | â†˜ï¸ Declinando

**3.3. Classificar momentum:**
```
POSITIVO: â‰¥3 indicadores â†—ï¸
NEUTRO: Indicadores mistos
NEGATIVO: â‰¥3 indicadores â†˜ï¸
```

---

### ETAPA 4: IdentificaÃ§Ã£o da Fase do Ciclo (30min)

**Cruzamento: Score P2i Ã— Leading Ã— ObservaÃ§Ã£o**

| Score P2i | Leading   | Fase do Ciclo  | RecomendaÃ§Ã£o TIV        |
|-----------|-----------|----------------|-------------------------|
| > 28/40   | POSITIVO  | EXPANSÃƒO       | âœ… CONSTRUIR/VENDER     |
| > 28/40   | NEUTRO    | MATURIDADE     | âš ï¸ CAUTELA              |
| > 28/40   | NEGATIVO  | SATURAÃ‡ÃƒO      | ðŸ”´ NÃƒO COMPRAR          |
| 20-28/40  | POSITIVO  | RECUPERAÃ‡ÃƒO    | âœ… COMPRAR TERRENO      |
| 20-28/40  | NEUTRO    | ESTÃVEL        | âš ï¸ ANALISAR NICHO       |
| 20-28/40  | NEGATIVO  | DESACELERAÃ‡ÃƒO  | âš ï¸ ESPERAR              |
| < 20/40   | POSITIVO  | INÃCIO CICLO   | âš ï¸ RISCO ALTO           |
| < 20/40   | NEUTRO    | ESTAGNADO      | ðŸ”´ NÃƒO INVESTIR         |
| < 20/40   | NEGATIVO  | RECESSÃƒO       | ðŸ”´ CRÃTICO - NÃƒO ENTRAR |

**DescriÃ§Ã£o das Fases:**
- **RECUPERAÃ‡ÃƒO:** Emprego crescendo, oferta baixa â†’ COMPRAR
- **EXPANSÃƒO:** Emprego alto, oferta crescendo â†’ CONSTRUIR/VENDER
- **SATURAÃ‡ÃƒO:** Emprego desacelerando, oferta alta â†’ CAUTELA
- **RECESSÃƒO:** Emprego caindo, oferta estagnada â†’ NÃƒO COMPRAR

---

### ETAPA 5: AnÃ¡lise de Riscos (1h)

**5.1. Identificar Red Flags:**

**Red Flags CRÃTICOS (STOP imediato):**
- ðŸ”´ Monocultura > 70% em 1 setor
- ðŸ”´ 1 empregador > 40% dos empregos
- ðŸ”´ PopulaÃ§Ã£o declinando 3+ anos consecutivos
- ðŸ”´ Emprego formal < 30% (25-59 anos)
- ðŸ”´ Saldo migratÃ³rio negativo persistente
- ðŸ”´ CAGED negativo 12+ meses consecutivos

**Red Flags de ATENÃ‡ÃƒO:**
- âš ï¸ Gini > 0,55 (concentraÃ§Ã£o alta)
- âš ï¸ Top 3 empresas > 60% empregos
- âš ï¸ Motos > 35% da frota
- âš ï¸ Infraestrutura bÃ¡sica < 80%
- âš ï¸ AlvarÃ¡s caindo 2+ anos consecutivos

**5.2. Avaliar Liquidez:**
- Risco de distratos em ciclos de queda
- Guerra de preÃ§os entre incorporadores
- "Trocas" oportunÃ­sticas (especulaÃ§Ã£o)

**5.3. Endividamento:**
- Curto prazo (< 12m): Risco inadimplÃªncia maior
- Longo prazo (24m+): Alinhado ao ciclo de consumo

---

### ETAPA 6: SÃ­ntese Executiva (30min)

**Gerar resumo estruturado conforme template (seÃ§Ã£o 10)**

---

## 6. Outputs Esperados

### Output 1: Scorecard de DinÃ¢mica EconÃ´mica

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚     SCORECARD DINÃ‚MICA ECONÃ”MICA - [MunicÃ­pio]       â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Indicador               â”‚ Valor  â”‚ Faixa  â”‚ Status   â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Emprego formal 25-59    â”‚ ___%   â”‚ â‰¥55% âœ…â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´  â”‚
â”‚ TGCA PopulaÃ§Ã£o          â”‚ __%a.a.â”‚ >1% âœ… â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´  â”‚
â”‚ TGCA Renda (proxy)      â”‚ __%a.a.â”‚ >0% âœ… â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´  â”‚
â”‚ Renda MÃ©dia + Gini      â”‚ R$__ / _â”‚ <0,55âœ…â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´  â”‚
â”‚ PIB & DiversificaÃ§Ã£o    â”‚ R$__ / _â”‚ >4 setâœ…â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´  â”‚
â”‚ Casamentos (%pop/mil)   â”‚ __%    â”‚ >0,8%âœ…â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´  â”‚
â”‚ PIT/CAGED 12-24m        â”‚ __     â”‚ >0 âœ…  â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´  â”‚
â”‚ Frota/% motos           â”‚ __ / __â”‚ >1,5<35âœ…â”‚ ðŸŸ¢ðŸŸ¡ðŸ”´â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ SCORE P2i: [XX]/40                                   â”‚
â”‚ LEADING: [POSITIVO/NEUTRO/NEGATIVO]                  â”‚
â”‚ FASE CICLO: [RECUPERAÃ‡ÃƒO/EXPANSÃƒO/SATURAÃ‡ÃƒO/RECESSÃƒO]â”‚
â”‚ DECISÃƒO TIV: [âœ… COMPRAR | âš ï¸ CAUTELA | ðŸ”´ NÃƒO]     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Output 2: Resumo Executivo

```markdown
## DINÃ‚MICA ECONÃ”MICA - SUMÃRIO EXECUTIVO

**MunicÃ­pio:** [Nome/UF]  
**Data AnÃ¡lise:** [DD/MM/AAAA]  
**Score P2i:** [XX]/40  
**Fase do Ciclo:** [Fase]

### Principais ConclusÃµes

**ForÃ§a de Consumo:**
- Emprego formal 25-59: __% [interpretaÃ§Ã£o]
- Renda mÃ©dia: R$ __ + Gini __ [interpretaÃ§Ã£o]
- Capacidade compra (30% renda): R$ __ [produto viÃ¡vel atÃ©]

**Qualidade do Ciclo:**
- DireÃ§Ã£o: [Acelerando/EstÃ¡vel/Desacelerando]
- Leading indicators: [POSITIVO/NEUTRO/NEGATIVO]
- CAGED 12m: __ (admissÃµes - demissÃµes)

**Riscos Identificados:**
- Liquidez: [anÃ¡lise]
- EspeculaÃ§Ã£o: [anÃ¡lise]
- Endividamento: [anÃ¡lise]
- DependÃªncias crÃ­ticas: [lista]

**ImplicaÃ§Ãµes para TIV:**
- **Passo 3 (AAI):** [raio esperado da Ã¡rea de influÃªncia]
- **Passo 4 (VocaÃ§Ã£o):** [horizontal/vertical/misto]
- **Passo 6 (Demanda):** [faixas de renda prioritÃ¡rias]
- **Passo 7 (Oferta):** [saturaÃ§Ã£o esperada]
- **Passo 8 (AbsorÃ§Ã£o):** [ajuste no Fator 4:1]
- **Passo 9 (ConvalidaÃ§Ã£o):** [pontos crÃ­ticos para validar]

### DecisÃ£o

**Ambiente:** [FAVORÃVEL | NEUTRO | DESFAVORÃVEL]  
**RecomendaÃ§Ã£o TIV:** [âœ… COMPRAR | âš ï¸ CAUTELA | ðŸ”´ NÃƒO INVESTIR]  
**Justificativa:** [2-3 sentenÃ§as]
```

### Output 3: SÃ©rie PIT/CAGED (12-24 meses)

Planilha CSV com:
- MÃªs/Ano
- AdmissÃµes
- DemissÃµes
- Saldo
- Por setor (AdministraÃ§Ã£o, AgropecuÃ¡ria, ComÃ©rcio, IndÃºstria, ServiÃ§os)

### Output 4: Tabela Comparativa com Pares

```csv
municipio;pop_2022;tgca_pop;renda_media;gini;pib_total;dens_empresas;emp_formal_25-59;casamentos_pop;divorcios_pop;veic_dom;motos_pct
[MunicÃ­pio-alvo];___;___;___;___;___;___;___;___;___;___;___
[MunicÃ­pio-par-1];___;___;___;___;___;___;___;___;___;___;___
[MunicÃ­pio-par-2];___;___;___;___;___;___;___;___;___;___;___
```

---

## 7. Alertas e ValidaÃ§Ãµes

### Checklist de ValidaÃ§Ã£o (Antes de Finalizar)

- [ ] **PopulaÃ§Ã£o:** Dados sÃ£o os mais recentes (< 2 anos)?
- [ ] **Emprego formal 25-59:** CÃ¡lculo validado (emp_formal Ã· pop_25-59)?
- [ ] **Leading:** SÃ©ries temporais coletadas (12-24 meses)?
- [ ] **Fase ciclo:** IdentificaÃ§Ã£o cruzou Score + Leading + Contexto?
- [ ] **Red flags:** Todos os crÃ­ticos foram checados?
- [ ] **DiversificaÃ§Ã£o:** PIB setorial analisado (nÃ£o sÃ³ PIB total)?
- [ ] **Top empregadores:** Lista atualizada e verificada?
- [ ] **Fontes:** Todas citadas com data de acesso?
- [ ] **ComparaÃ§Ã£o:** MunicÃ­pios pares adequados (porte/regiÃ£o)?
- [ ] **PopulaÃ§Ã£o flutuante:** Se emp_formal > 100%, foi analisado?

### Erros Comuns a Evitar

âŒ **Foto estÃ¡tica sem sÃ©rie temporal**
- Erro: Usar apenas dados pontuais (ex: populaÃ§Ã£o 2022)
- Correto: Analisar TGCA (sÃ©rie 2010-2024) para identificar tendÃªncia

âŒ **Misturar mÃ©dia sem olhar Gini**
- Erro: "Renda mÃ©dia R$ 5.000, entÃ£o mercado tem poder de compra"
- Correto: Checar Gini. Se > 0,55, renda concentrada no topo (ilusÃ£o)

âŒ **NÃ£o considerar PIT/CAGED**
- Erro: Usar apenas dados do censo (defasados 2+ anos)
- Correto: PIT/CAGED Ã© leading indicator (antecipa virada de ciclo)

âŒ **Ignorar populaÃ§Ã£o flutuante**
- Erro: Ver emprego formal > 100% e considerar "erro"
- Correto: Indica trabalhadores nÃ£o-residentes (validar perfil/salÃ¡rios)

âŒ **Desprezar endividamento/prazo**
- Erro: "InadimplÃªncia alta, mercado ruim"
- Correto: Checar SE Ã© curto prazo (< 12m = problema) ou longo (ciclo normal)

---

## 8. IntegraÃ§Ã£o com Outras Skills TIV

### Esta Skill Alimenta:

**tiv-passo3-area-influencia:**
- Score P2i baixo â†’ Ãrea de influÃªncia menor (mercado limitado)
- Leading positivo â†’ Pode expandir polÃ­gono de busca

**tiv-passo4-vocacao:**
- Renda mÃ©dia + Gini â†’ Define teto de preÃ§o por vocaÃ§Ã£o
- DiversificaÃ§Ã£o alta â†’ Produtos mistos viÃ¡veis
- Monocultura â†’ Cautela com vocaÃ§Ãµes dependentes

**tiv-passo6-demanda:**
- Emprego formal 25-59 â†’ Quantifica demanda elegÃ­vel
- TGCA + PirÃ¢mide â†’ ProjeÃ§Ã£o demanda futura
- Casamentos â†’ Velocidade formaÃ§Ã£o novos lares

**tiv-passo8-absorcao:**
- Fase do ciclo â†’ Ajusta Fator 4:1
  - RecuperaÃ§Ã£o: Manter 4:1
  - ExpansÃ£o: Pode usar 3:1 (otimista)
  - SaturaÃ§Ã£o/RecessÃ£o: Aumentar para 5:1 ou 6:1 (conservador)

**tiv-fcd:**
- Score P2i baixo â†’ Aumenta TMA (taxa de desconto)
- Red flags crÃ­ticos â†’ Penalizar cenÃ¡rio-base ou inviabilizar

### Esta Skill Ã‰ Alimentada Por:

**tiv-garimpo:**
- Terreno identificado â†’ MunicÃ­pio definido â†’ Iniciar P2i-Lead

---

## 9. Exemplos PrÃ¡ticos

### Exemplo 1: Leopoldina-MG (ReferÃªncia)

**CONTEXTO:**
- MunicÃ­pio: Leopoldina-MG
- PopulaÃ§Ã£o: 52.565 hab (IBGE 2022)
- Terreno: 22 ha rurais (potencial loteamento)

**INPUTS COLETADOS:**

**POPULAÃ‡ÃƒO (P1):**
- Tamanho: 52.565 hab â†’ Score: **7/10** (mÃ©dio porte)
- TGCA 2010-2022: +1,1% a.a. â†’ Score: **7/10** (crescimento saudÃ¡vel)
- Densidade: 118 hab/kmÂ² â†’ Score: **6/10** (baixa/mÃ©dia)
- MigraÃ§Ã£o: Dados nÃ£o disponÃ­veis â†’ Score: **5/10** (neutro)
**Subtotal POPULAÃ‡ÃƒO: 25/40**

**PIRÃ‚MIDE (P2):**
- Renda mÃ©dia: R$ 4.200 â†’ Score: **6/10**
- Gini: 0,48 â†’ Score: **7/10** (concentraÃ§Ã£o moderada)
- Emprego formal 25-59: 42% â†’ Score: **6/10** (abaixo mÃ©dia Brasil 55%)
- Renda per capita: R$ 28.567 â†’ Score: **6/10**
**Subtotal PIRÃ‚MIDE: 25/40**

**INFRAESTRUTURA (I1):**
- Mobilidade: BR-267 (boa), transporte local limitado â†’ **6/10**
- Equipamentos: Hospital regional, escolas pÃºblicas/privadas â†’ **7/10**
- ServiÃ§os bÃ¡sicos: Ãgua 92%, esgoto 78%, energia 98% â†’ **7/10**
- Conectividade: Fibra Ã³ptica disponÃ­vel â†’ **7/10**
**Subtotal INFRAESTRUTURA: 27/40**

**INDÃšSTRIA (I2):**
- DiversificaÃ§Ã£o: ComÃ©rcio 35%, ServiÃ§os 32%, IndÃºstria 20%, Agro 13% â†’ **9/10** âœ…
- Top 10 empregadores: Prefeitura (12%), hospital (8%), comÃ©rcio distribuÃ­do â†’ **8/10**
- Setores: Sem dependÃªncia crÃ­tica â†’ **8/10**
- DependÃªncias: Nenhuma identificada â†’ **9/10**
**Subtotal INDÃšSTRIA: 34/40**

**SCORE TOTAL P2i: 27,75/40** â‰ˆ **28/40**

**LEADING INDICATORS:**
- PIT/CAGED 12m: +150 empregos (saldo positivo) â†’ âœ…
- Aberturas empresas: +12% vs ano anterior â†’ âœ…
- AlvarÃ¡s construÃ§Ã£o: +8 (crescimento modesto) â†’ â†’
- Casamentos: 0,95% pop/mil (estÃ¡vel) â†’ â†’
**Leading: POSITIVO** (3 de 4 crescendo)

**FASE DO CICLO:**
- Score 28/40 + Leading POSITIVO = **RECUPERAÃ‡ÃƒO** âœ…
- InterpretaÃ§Ã£o: Economia saindo de perÃ­odo fraco, momento ideal para COMPRAR terreno

**RISCOS IDENTIFICADOS:**
- âš ï¸ Emprego formal 42% (abaixo mÃ©dia Brasil) â†’ Atentar para informalidade
- âš ï¸ Renda mÃ©dia R$ 4.200 â†’ Teto de preÃ§o produto ~R$ 280-320k
- âœ… Sem monocultura (diversificaÃ§Ã£o 9/10)
- âœ… Sem dependÃªncia crÃ­tica de empregadores

**DECISÃƒO TIV:**
```
Ambiente: FAVORÃVEL (Score 28/40, leading positivo)
RecomendaÃ§Ã£o: âœ… COMPRAR TERRENO AGORA
Timing: Ã“timo (recuperaÃ§Ã£o = preÃ§o terreno ainda baixo)
Cautelas: 
- Produto atÃ© R$ 300k (regra 30% renda)
- AbsorÃ§Ã£o conservadora (Fator 4:1 padrÃ£o)
```

---

### Exemplo 2: MunicÃ­pio com Monocultura (RED FLAG)

**CONTEXTO:**
- MunicÃ­pio: [AnÃ´nimo]-MG
- PopulaÃ§Ã£o: 28.000 hab
- Economia: Usina de aÃ§Ãºcar dominante

**INPUTS:**

**POPULAÃ‡ÃƒO:** 21/40 (pequeno porte, crescimento baixo)

**INDÃšSTRIA:**
- DiversificaÃ§Ã£o: Agro 78% (usina), ComÃ©rcio 15%, ServiÃ§os 7% â†’ **1/10** ðŸ”´
- Top 10: Usina = 65% dos empregos formais â†’ **0/10** ðŸ”´
- DependÃªncias: 1 empresa crÃ­tica â†’ **0/10** ðŸ”´
**Subtotal INDÃšSTRIA: 1/40** ðŸ”´

**SCORE TOTAL P2i: 14/40** ðŸ”´

**LEADING:**
- CAGED: -80 empregos (usina demitindo entressafra) â†’ ðŸ”´
- AlvarÃ¡s: 2 nos Ãºltimos 12m (-70% vs ano anterior) â†’ ðŸ”´
**Leading: NEGATIVO**

**FASE DO CICLO:** RECESSÃƒO ðŸ”´

**DECISÃƒO TIV:**
```
Ambiente: DESFAVORÃVEL (monocultura crÃ­tica)
RecomendaÃ§Ã£o: ðŸ”´ NÃƒO INVESTIR
Red Flags:
- Monocultura > 70% (78% agro)
- 1 empresa > 40% empregos (65% usina)
- Leading negativo (demissÃµes + alvarÃ¡s caindo)
Justificativa: Risco sistÃªmico. Crise na usina = colapso mercado.
```

---

### Exemplo 3: MunicÃ­pio em ExpansÃ£o (Grande Porte)

**CONTEXTO:**
- MunicÃ­pio: [Exemplo]-SP
- PopulaÃ§Ã£o: 180.000 hab (+2,3% a.a.)
- Novos investimentos: Shopping + hospital privado + indÃºstria automotiva

**SCORE P2i: 34/40** âœ… (excelente)

**LEADING:**
- CAGED: +650 empregos/mÃªs (mÃ©dia 12m) â†’ âœ…âœ…
- AlvarÃ¡s: +45% vs ano anterior â†’ âœ…âœ…
- Novos lanÃ§amentos imobiliÃ¡rios: 8 (vs 3 ano anterior) â†’ âœ…
**Leading: MUITO POSITIVO**

**FASE DO CICLO:** EXPANSÃƒO âœ…

**DECISÃƒO TIV:**
```
Ambiente: MUITO FAVORÃVEL
RecomendaÃ§Ã£o: âœ… CONSTRUIR E VENDER (nÃ£o comprar terreno agora)
Timing: Pico do ciclo - preÃ§o terreno alto, mas absorÃ§Ã£o rÃ¡pida
Cautelas:
- Atentar para saturaÃ§Ã£o futura (jÃ¡ hÃ¡ 8 lanÃ§amentos)
- Velocidade pode compensar margem menor
```

---

## 10. Templates Prontos (Copiar e Colar)

### Template 1: Frontmatter.yml (Metadados da AnÃ¡lise)

```yaml
passo: 2
versao: "2025-11-12_v2.0"
municipio: "[Nome]"
estado: "[UF]"
populacao_2024: [nÃºmero]
fontes:
  - IBGE_Cidades
  - RAIS_MTE_P2I
  - CAGED_PIT
  - Atlas_Brasil
  - Prefeitura_Municipal
pares_comparacao:
  - "[Cidade A]"
  - "[Cidade B]"
  - "[Cidade C]"
janela_series_meses: 24
data_analise: "2025-11-12"
analista: "[Nome]"
outputs:
  - scorecard_dinamica.md
  - serie_pit_caged.csv
  - comparativo_pares.csv
  - resumo_executivo_p2.md
```

---

### Template 2: Scorecard_Dinamica.md

```markdown
# SCORECARD â€“ PASSO 2: DINÃ‚MICA ECONÃ”MICA

**MunicÃ­pio:** [Nome/UF]  
**Data:** [DD/MM/AAAA]  
**Score P2i:** [XX]/40  
**Fase:** [RecuperaÃ§Ã£o/ExpansÃ£o/SaturaÃ§Ã£o/RecessÃ£o]  
**Leading:** [POSITIVO/NEUTRO/NEGATIVO]

---

## INDICADORES-CHAVE

| Indicador | MÃ©trica | Valor | Faixa ReferÃªncia | Status |
|-----------|---------|------:|------------------|:------:|
| **Emprego formal 25â€“59** | emp_formal/pop_25â€“59 | __% | â‰¥55% ok / <30% alerta | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **TGCA PopulaÃ§Ã£o** | % a.a. (2010â€“2024) | __% | >1% saudÃ¡vel | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **TGCA Renda (proxy)** | % a.a. estimado | __% | >0% positivo | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **Renda MÃ©dia** | R$ mensal | R$ __ | vs pares | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **Ãndice Gini** | 0-1 | __ | <0,55 ok | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **PIB Total** | R$ bilhÃµes | R$ __ | contexto regional | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **DiversificaÃ§Ã£o** | nÂº setores >15% | __ | â‰¥4 ideal | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **Casamentos** | % pop/mil | __% | >0,8% ok | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **DivÃ³rcios** | % pop/mil | __% | contexto | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **PIT/CAGED 12m** | saldo empregos | __ | >0 aquecido | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **AlvarÃ¡s 12m** | nÂº residenciais | __ | tendÃªncia | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **Frota/domicÃ­lio** | veÃ­c/dom | __ | >1,5 saudÃ¡vel | ðŸŸ¢ðŸŸ¡ðŸ”´ |
| **% Motocicletas** | % frota | __% | <35% ok | ðŸŸ¢ðŸŸ¡ðŸ”´ |

---

## SÃNTESE

**Pontos Fortes:**
- [listar]

**Pontos Fracos:**
- [listar]

**Red Flags:**
- [listar se houver]

**RecomendaÃ§Ã£o:**
[âœ… COMPRAR | âš ï¸ CAUTELA | ðŸ”´ NÃƒO INVESTIR]
```

---

### Template 3: Comparativo_Pares.csv

```csv
municipio;pop_2022;tgca_pop_2010-2022;renda_media;gini;pib_total_mi;dens_empresas;emp_formal_25-59_pct;casamentos_pct_pop;divorcios_pct_pop;veic_dom;motocicletas_pct_frota
[MunicÃ­pio-alvo];;;;;;;;;;
[Par-1];;;;;;;;;;
[Par-2];;;;;;;;;;
[Par-3];;;;;;;;;;
```

---

### Template 4: Resumo_Executivo.md (Completo)

```markdown
# PASSO 2: ANÃLISE DA DINÃ‚MICA ECONÃ”MICA

**MunicÃ­pio:** [Nome/UF]  
**Data da AnÃ¡lise:** [DD/MM/AAAA]  
**Analista:** [Nome]  
**Produto-Alvo:** [Loteamento/IncorporaÃ§Ã£o/Misto]

---

## SUMÃRIO EXECUTIVO (TL;DR)

**Score P2i:** [XX]/40  
**Fase do Ciclo:** [Fase]  
**Leading Indicators:** [POSITIVO/NEUTRO/NEGATIVO]  
**DecisÃ£o TIV:** [âœ… COMPRAR | âš ï¸ CAUTELA | ðŸ”´ NÃƒO INVESTIR]

**Principais ConclusÃµes:**
- [ConclusÃ£o 1]
- [ConclusÃ£o 2]
- [ConclusÃ£o 3]

---

## 1. CONTEXTO E METODOLOGIA

**Objetivo:**
Medir forÃ§a de consumo e qualidade do ciclo econÃ´mico local para balizar vocaÃ§Ã£o (Passo 4), desenho da AAI (Passo 3) e hipÃ³teses de demanda/oferta/absorÃ§Ã£o (Passos 6-7-8).

**Framework Aplicado:**
P2i-Lead (16 variÃ¡veis: PopulaÃ§Ã£o, PirÃ¢mide, Infraestrutura, IndÃºstria + Leading Indicators)

**Fontes de Dados:**
- IBGE Cidades (populaÃ§Ã£o, PIB, infraestrutura)
- RAIS/MTE/P2i (emprego formal, setores)
- CAGED/PIT (empregabilidade tempo real)
- Atlas Brasil (renda, Gini, IDH)
- Prefeitura Municipal (alvarÃ¡s, projetos)
- [outras fontes especÃ­ficas]

---

## 2. SCORE P2i DETALHADO

### 2.1. POPULAÃ‡ÃƒO (/10)

| VariÃ¡vel | Valor | Score | Justificativa |
|----------|------:|------:|---------------|
| Tamanho total | [N] hab | [X]/10 | [explicaÃ§Ã£o] |
| TGCA 2010-2024 | [X]% a.a. | [X]/10 | [explicaÃ§Ã£o] |
| Densidade demogrÃ¡fica | [X] hab/kmÂ² | [X]/10 | [explicaÃ§Ã£o] |
| Saldo migratÃ³rio | [+/-X] | [X]/10 | [explicaÃ§Ã£o] |
| **SUBTOTAL POPULAÃ‡ÃƒO** | | **[XX]/10** | |

**AnÃ¡lise:**
[2-3 parÃ¡grafos interpretando os dados]

---

### 2.2. PIRÃ‚MIDE (/10)

| VariÃ¡vel | Valor | Score | Justificativa |
|----------|------:|------:|---------------|
| Renda mÃ©dia | R$ [X] | [X]/10 | [explicaÃ§Ã£o] |
| Ãndice de Gini | [X] | [X]/10 | [explicaÃ§Ã£o] |
| Emprego formal 25-59 | [X]% | [X]/10 | [explicaÃ§Ã£o] |
| Renda per capita | R$ [X] | [X]/10 | [explicaÃ§Ã£o] |
| **SUBTOTAL PIRÃ‚MIDE** | | **[XX]/10** | |

**AnÃ¡lise:**
[2-3 parÃ¡grafos interpretando os dados]

**Capacidade de Compra (Regra 30%):**
- Renda mÃ©dia R$ [X] Ã— 30% = R$ [Y] mensal
- Produto viÃ¡vel atÃ© ~R$ [Z] (financiamento tÃ­pico)

---

### 2.3. INFRAESTRUTURA (/10)

| VariÃ¡vel | AvaliaÃ§Ã£o | Score | Justificativa |
|----------|-----------|------:|---------------|
| Mobilidade | [descriÃ§Ã£o] | [X]/10 | [explicaÃ§Ã£o] |
| Equipamentos urbanos | [descriÃ§Ã£o] | [X]/10 | [explicaÃ§Ã£o] |
| ServiÃ§os bÃ¡sicos | [descriÃ§Ã£o] | [X]/10 | [explicaÃ§Ã£o] |
| Conectividade | [descriÃ§Ã£o] | [X]/10 | [explicaÃ§Ã£o] |
| **SUBTOTAL INFRAESTRUTURA** | | **[XX]/10** | |

**AnÃ¡lise:**
[2-3 parÃ¡grafos interpretando os dados]

---

### 2.4. INDÃšSTRIA/EMPREGO (/10)

| VariÃ¡vel | AvaliaÃ§Ã£o | Score | Justificativa |
|----------|-----------|------:|---------------|
| DiversificaÃ§Ã£o setorial | [setores] | [X]/10 | [explicaÃ§Ã£o] |
| Top 10 empregadores | [concentraÃ§Ã£o] | [X]/10 | [explicaÃ§Ã£o] |
| Setores dominantes | [CNAEs] | [X]/10 | [explicaÃ§Ã£o] |
| DependÃªncias crÃ­ticas | [anÃ¡lise] | [X]/10 | [explicaÃ§Ã£o] |
| **SUBTOTAL INDÃšSTRIA** | | **[XX]/10** | |

**AnÃ¡lise:**
[2-3 parÃ¡grafos interpretando os dados]

**Top 10 Empregadores:**
1. [Nome] - [N] empregos ([X]% do total)
2. [Nome] - [N] empregos ([X]% do total)
[...]

---

### 2.5. SCORE TOTAL P2i

```
POPULAÃ‡ÃƒO:      [XX]/10
PIRÃ‚MIDE:       [XX]/10
INFRAESTRUTURA: [XX]/10
INDÃšSTRIA:      [XX]/10
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
TOTAL P2i:      [XX]/40
```

**InterpretaÃ§Ã£o Geral:**
- **> 28/40:** Base sÃ³lida âœ…
- **20-28/40:** IntermediÃ¡rio (avaliar leading)
- **< 20/40:** Fragilidades estruturais âš ï¸

[ParÃ¡grafo interpretativo]

---

## 3. LEADING INDICATORS

### 3.1. PIT/CAGED (Empregabilidade)

**SÃ©rie 12-24 meses:**

| MÃªs/Ano | AdmissÃµes | DemissÃµes | Saldo | TendÃªncia |
|---------|----------:|----------:|------:|:---------:|
| [MÃªs/Ano] | [N] | [N] | [+/-N] | â†—ï¸â†’â†˜ï¸ |
[...]

**AnÃ¡lise:**
[Interpretar tendÃªncia: aquecimento, estabilidade ou resfriamento]

**Por Setor (Ãºltimos 12m):**
- AdministraÃ§Ã£o: [saldo]
- AgropecuÃ¡ria: [saldo]
- ComÃ©rcio: [saldo]
- IndÃºstria: [saldo]
- ServiÃ§os: [saldo]

---

### 3.2. Abertura vs Fechamento de Empresas

**SÃ©rie 12 meses:**

| MÃªs/Ano | Aberturas | Fechamentos | Saldo | IEM* |
|---------|----------:|------------:|------:|-----:|
| [MÃªs/Ano] | [N] | [N] | [+/-N] | [X]% |
[...]

*IEM = Ãndice de EficÃ¡cia do Mercado (aberturas Ã· fechamentos)

**AnÃ¡lise:**
[Interpretar: empreendedorismo ativo, liquidez, setores]

---

### 3.3. AlvarÃ¡s de ConstruÃ§Ã£o Residencial

**SÃ©rie 12-24 meses:**

| Ano | AlvarÃ¡s Emitidos | VariaÃ§Ã£o vs Anterior |
|-----|------------------:|---------------------:|
| [Ano] | [N] | - |
| [Ano] | [N] | [+/-X]% |
[...]

**AnÃ¡lise:**
[Interpretar: aquecimento, resfriamento, comparar com CAGED]

---

### 3.4. Casamentos e DivÃ³rcios

**SÃ©rie 4-5 anos:**

| Ano | Casamentos | % Pop | DivÃ³rcios | % Pop | RazÃ£o Cas/Div |
|-----|------------:|------:|----------:|------:|--------------:|
| [Ano] | [N] | [X]% | [N] | [X]% | [X]:1 |
[...]

**AnÃ¡lise:**
[Interpretar: formaÃ§Ã£o/dissoluÃ§Ã£o lares, impacto demanda]

---

### 3.5. SÃ­ntese Leading Indicators

| Indicador | TendÃªncia | Peso | ContribuiÃ§Ã£o |
|-----------|:---------:|:----:|:------------:|
| CAGED 12m | â†—ï¸â†’â†˜ï¸ | 35% | POSITIVO/NEUTRO/NEGATIVO |
| Aberturas empresas | â†—ï¸â†’â†˜ï¸ | 25% | POSITIVO/NEUTRO/NEGATIVO |
| AlvarÃ¡s construÃ§Ã£o | â†—ï¸â†’â†˜ï¸ | 25% | POSITIVO/NEUTRO/NEGATIVO |
| Casamentos | â†—ï¸â†’â†˜ï¸ | 15% | POSITIVO/NEUTRO/NEGATIVO |

**LEADING GERAL:** [POSITIVO / NEUTRO / NEGATIVO]

---

## 4. IDENTIFICAÃ‡ÃƒO DA FASE DO CICLO

**Cruzamento: Score P2i [XX]/40 + Leading [STATUS]**

**Matriz de DecisÃ£o:**

| Score P2i | Leading | Fase Identificada |
|-----------|---------|-------------------|
| [faixa] | [status] | **[FASE]** |

**DescriÃ§Ã£o da Fase [FASE]:**
[Explicar caracterÃ­sticas da fase: emprego, oferta, preÃ§os, timing ideal]

**HistÃ³rico Visual do Ciclo:**
```
[GrÃ¡fico ou descriÃ§Ã£o temporal mostrando evoluÃ§Ã£o Ãºltimos 3-5 anos]
Exemplo:
2020: RecessÃ£o (COVID)
2021-2022: RecuperaÃ§Ã£o (retomada)
2023-2024: ExpansÃ£o (aquecimento)
2025: [Fase atual identificada]
```

---

## 5. ANÃLISE DE RISCOS

### 5.1. Red Flags Identificados

**RED FLAGS CRÃTICOS (STOP):**
- [ ] Monocultura > 70%
- [ ] 1 empregador > 40%
- [ ] PopulaÃ§Ã£o declinando 3+ anos
- [ ] Emprego formal < 30%
- [ ] MigraÃ§Ã£o negativa persistente
- [ ] CAGED negativo 12+ meses

[Para cada flag identificado, detalhar:]
- **Flag:** [descriÃ§Ã£o]
- **Severidade:** CRÃTICO/ALTO/MÃ‰DIO
- **Impacto:** [explicaÃ§Ã£o]
- **MitigaÃ§Ã£o possÃ­vel:** [se houver]

---

**RED FLAGS DE ATENÃ‡ÃƒO:**
- [ ] Gini > 0,55
- [ ] Top 3 empresas > 60%
- [ ] Motos > 35% frota
- [ ] Infraestrutura < 80%
- [ ] AlvarÃ¡s declinando 2+ anos

[Idem]

---

### 5.2. Riscos de Liquidez e EspeculaÃ§Ã£o

**Liquidez:**
[Analisar risco de distratos em ciclos de queda, guerra de preÃ§os]

**EspeculaÃ§Ã£o:**
[Identificar sinais de "trocas" oportunÃ­sticas, compradores recorrentes]

**Endividamento:**
[Analisar nÃ­vel e prazo: curto vs longo prazo]

---

### 5.3. PopulaÃ§Ã£o Flutuante

**Emprego formal 25-59 / Pop 25-59 = [X]%**

[Se > 100%:]
- HÃ¡ populaÃ§Ã£o flutuante (trabalhadores nÃ£o residentes)
- **Perfil:** [qualificaÃ§Ã£o, salÃ¡rios, setores]
- **Mobilidade:** [origem, meio de transporte]
- **TendÃªncia:** [aluguel â†’ compra? migraÃ§Ã£o definitiva?]
- **Impacto demanda:** [positivo/neutro/negativo]

---

## 6. IMPLICAÃ‡Ã•ES PARA OS PRÃ“XIMOS PASSOS TIV

### Passo 3: Ãrea de InfluÃªncia
- **Raio sugerido:** [X] km ou [Y] minutos (isÃ³crona)
- **Justificativa:** [baseado em renda mÃ©dia, mobilidade, densidade]

### Passo 4: VocaÃ§Ã£o ImobiliÃ¡ria
- **VocaÃ§Ãµes prioritÃ¡rias:** [Horizontal/Vertical/Misto]
- **Justificativa:** [baseado em renda, demanda, diversificaÃ§Ã£o]

### Passo 5: Legal e RestriÃ§Ãµes
- **AtenÃ§Ã£o especial:** [zoneamento, potencial construtivo]

### Passo 6: Demanda
- **Faixas de renda prioritÃ¡rias:** R$ [X] a R$ [Y]
- **Perfil esperado:** [idade, familiar, emprego]
- **Capacidade compra (30% renda):** AtÃ© R$ [Z]

### Passo 7: Oferta
- **SaturaÃ§Ã£o esperada:** [baixa/mÃ©dia/alta]
- **Tipologias concorrentes:** [loteamento/edifÃ­cio/casa]

### Passo 8: AbsorÃ§Ã£o
- **Fator sugerido:** [4:1 padrÃ£o | ajustado para X:1]
- **Justificativa:** [baseado em fase do ciclo]

### Passo 9: ConvalidaÃ§Ã£o
- **Pontos crÃ­ticos para validar:**
  1. [Premissa a validar]
  2. [Premissa a validar]
  3. [Premissa a validar]

### Passo 10: FCD
- **Taxa desconto (TMA):** [ajuste baseado em score e riscos]
- **CenÃ¡rios:** [base/otimista/pessimista recomendados]

---

## 7. CONCLUSÃƒO E RECOMENDAÃ‡ÃƒO

### SÃ­ntese Final

**ForÃ§a de Consumo:**
[ParÃ¡grafo resumindo capacidade de pagamento, renda, emprego]

**Qualidade do Ciclo:**
[ParÃ¡grafo resumindo fase, tendÃªncia, leading indicators]

**Riscos:**
[ParÃ¡grafo resumindo red flags, dependÃªncias, vulnerabilidades]

---

### DECISÃƒO TIV

```
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘  AMBIENTE: [FAVORÃVEL / NEUTRO / DESFAVORÃVEL]  â•‘
â•‘  RECOMENDAÃ‡ÃƒO: [âœ… COMPRAR | âš ï¸ CAUTELA | ðŸ”´ NÃƒO] â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
```

**Justificativa:**
[2-3 parÃ¡grafos fundamentando a decisÃ£o com base em:
- Score P2i
- Leading indicators
- Fase do ciclo
- Red flags (ou ausÃªncia deles)
- Oportunidade de timing]

**Condicionantes (se houver):**
1. [CondiÃ§Ã£o 1]
2. [CondiÃ§Ã£o 2]

---

## 8. PRÃ“XIMOS PASSOS

**Imediatos:**
- [ ] Iniciar Passo 3 (Ãrea de InfluÃªncia)
- [ ] Coletar dados complementares: [especificar]
- [ ] Validar in loco: [pontos especÃ­ficos]

**RevalidaÃ§Ãµes:**
- [ ] Atualizar CAGED a cada trimestre
- [ ] Monitorar alvarÃ¡s mensalmente
- [ ] Revisar score P2i anualmente

---

## 9. ANEXOS

### Anexo A: Fontes de Dados (Completo)

| Fonte | URL | Data Acesso | Dados ExtraÃ­dos |
|-------|-----|-------------|-----------------|
| IBGE Cidades | [link] | [DD/MM/AAAA] | [lista] |
| Atlas Brasil | [link] | [DD/MM/AAAA] | [lista] |
| CAGED/PIT | [link] | [DD/MM/AAAA] | [lista] |
[...]

### Anexo B: Planilhas Auxiliares

- `scorecard_dinamica.xlsx` - Scores detalhados P2i
- `serie_pit_caged.csv` - Dados mensais emprego
- `comparativo_pares.csv` - Benchmarking municÃ­pios
- `leading_indicators.xlsx` - SÃ©ries temporais completas

### Anexo C: Imagens e Mapas

- Mapa de localizaÃ§Ã£o regional
- GrÃ¡fico evoluÃ§Ã£o CAGED 24m
- PirÃ¢mide etÃ¡ria municÃ­pio
- [outras visualizaÃ§Ãµes relevantes]

---

**âš ï¸ DISCLAIMER:**

Esta anÃ¡lise Ã© baseada em dados pÃºblicos e informaÃ§Ãµes fornecidas atÃ© [data]. Recomenda-se:
1. ValidaÃ§Ã£o in loco dos principais indicadores
2. Consulta a fontes locais (prefeitura, associaÃ§Ã£o comercial, imobiliÃ¡rias)
3. RevisÃ£o periÃ³dica (trimestral para leading, anual para P2i)
4. AnÃ¡lise de sensibilidade para variÃ¡veis crÃ­ticas

A decisÃ£o final de investimento deve considerar este Passo 2 em conjunto com todos os demais Passos da Metodologia TIV 4.0.

---

**Elaborado por:** [Nome]  
**Revisado por:** [Nome]  
**Data:** [DD/MM/AAAA]  
**VersÃ£o:** 2.0
```

---

## 11. Definition of Done (DoD)

Passo 2 estÃ¡ completo quando:

- [ ] **Emprego formal 25â€“59 / Pop. 25â€“59** calculado e classificado
- [ ] **TGCA** de populaÃ§Ã£o estimada (2010â€“Ãºltimo ano)
- [ ] **Renda mÃ©dia + Gini** consolidados e comparados
- [ ] **PIB, diversificaÃ§Ã£o, top empregadores** analisados
- [ ] **Casamentos/divÃ³rcios** anuais plotados (4â€“5 anos)
- [ ] **PIT/CAGED** (12â€“24m) com leitura por setor
- [ ] **Abertura/fechamento** empresas analisado
- [ ] **Frota e % motos** avaliados
- [ ] **Score P2i** calculado ([XX]/40)
- [ ] **Leading indicators** classificados (POSITIVO/NEUTRO/NEGATIVO)
- [ ] **Fase do ciclo** identificada com justificativa
- [ ] **Red flags** checados (CRÃTICOS + ATENÃ‡ÃƒO)
- [ ] **RelatÃ³rio executivo** gerado com recomendaÃ§Ã£o clara
- [ ] **Fontes citadas** com links e datas
- [ ] **IntegraÃ§Ã£o Passo 3-10** explicitada (implicaÃ§Ãµes)

---

## 12. Versionamento e ManutenÃ§Ã£o

### HistÃ³rico de VersÃµes

**v2.0 (2025-11-12):**
- âœ… Framework P2i-Lead expandido (16 variÃ¡veis detalhadas)
- âœ… Leading indicators formalizados (PIT/CAGED, aberturas empresas, alvarÃ¡s, casamentos)
- âœ… Templates completos prontos para uso
- âœ… 3 exemplos prÃ¡ticos (Leopoldina-MG, monocultura, expansÃ£o)
- âœ… IntegraÃ§Ã£o detalhada com Skills TIV 3-10
- âœ… Checklist de validaÃ§Ã£o expandido

**v1.0 (2025-10-30):**
- Primeira versÃ£o operacional
- Framework P2i bÃ¡sico

### PrÃ³ximas Melhorias (Backlog)

- [ ] Dashboard visual automÃ¡tico (grÃ¡ficos P2i)
- [ ] API integraÃ§Ã£o direta IBGE/CAGED
- [ ] Alertas automÃ¡ticos (red flags via scraping)
- [ ] Benchmarking automÃ¡tico (municÃ­pios pares IA)
- [ ] SÃ©ries histÃ³ricas completas (10+ anos)

---

## 13. ReferÃªncias MetodolÃ³gicas

### CitaÃ§Ãµes-Chave TIV 4.0

> **"Quanto mais diversificada [a dinÃ¢mica econÃ´mica] for, mais blindada ela serÃ¡ com relaÃ§Ã£o a risco"**

> **"Emprego formal 25-59 / Pop. 25-59 Ã© proxy de capacidade de pagamento; mÃ©dia Brasil â‰ˆ 55%; < 30% Ã© zona de risco"**

> **"Se Emprego formal 25-59 / Pop 25-59 > 100%, hÃ¡ populaÃ§Ã£o flutuante (empregados que nÃ£o residem)"**

> **"TGCA populacional e de renda â€“ direÃ§Ã£o e velocidade do ciclo; observar aceleraÃ§Ã£o/desaceleraÃ§Ã£o"**

> **"Renda mÃ©dia + Ãndice de Gini â€“ poder de compra e concentraÃ§Ã£o (0 = dispersa; 1 = concentrada)"**

> **"Monocultura > 70% em 1 setor = NÃƒO INVESTIR (risco sistÃªmico)"**

> **"Leading indicators > Lagging indicators para antecipar mudanÃ§as de ciclo"**

### Base Conceitual

- **Framework P2i-Lead:** Desenvolvimento prÃ³prio Metodologia TIV 4.0
- **Regra 30% Renda:** Capacidade compra baseada em comprometimento mÃ¡ximo
- **Fator 4:1:** Conservadorismo TIV aplicado Ã  velocidade de vendas
- **AnÃ¡lise de Ciclos:** AdaptaÃ§Ã£o de modelos macroeconÃ´micos para micro-regiÃµes

---

**FIM DA SKILL `tiv-passo2-dinamica-economica` v2.0**

**Metodologia:** TIV 4.0 - Framework P2i-Lead (16 variÃ¡veis)  
**Autor:** Othon Valentim + Metodologia TIV  
**ManutenÃ§Ã£o:** RevisÃ£o trimestral (leading) + anual (P2i)  
**Suporte:** IntegraÃ§Ã£o total com Skills TIV Passo 1-10
