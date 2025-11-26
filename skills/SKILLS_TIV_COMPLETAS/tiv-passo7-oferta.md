---
name: "tiv-passo7-oferta"
version: "1.0"
description: "Mapeamento e anÃ¡lise da oferta competitiva atravÃ©s das 3 tipologias (Pulverizada, LanÃ§amentos, TBC) + cÃ¡lculo de VSO/IVV + Alinhamento de Mercado. Passo 7 da Metodologia TIV 4.0."
author: "Metodologia TIV 4.0"
created: "2025-10-31"
updated: "2025-10-31"
tags: ["tiv", "imobiliario", "oferta", "concorrencia", "vso", "ivv", "alinhamento"]
priority: "CRÃTICO (TIER 1)"
---

# SKILL: Passo 7 - AnÃ¡lise Concorrencial e Alinhamento de Mercado

## 1. OBJETIVO E CONTEXTO

### 1.1. DefiniÃ§Ã£o

O **Passo 7 da Metodologia TIV** Ã© o "Raio-X EstratÃ©gico do Mercado" que transforma coleta de dados de concorrÃªncia em **estratÃ©gia de posicionamento de produto**. Seu objetivo Ã© garantir que o empreendimento nÃ£o apenas atenda Ã  demanda mapeada (Passo 6), mas que se destaque da concorrÃªncia, maximizando o potencial de venda.

**CitaÃ§Ã£o-chave TIV:**

> *"VocÃª nÃ£o pode empreender a esmo, dirigindo a 250 km/h vendado. O Passo 7 impede que vocÃª seja surpreendido pela Oferta Futura e garante que seu produto esteja matematicamente alinhado com o desejo do comprador."*

### 1.2. PosiÃ§Ã£o na Metodologia

```
PASSO 6 (DEMANDA)
    â†“
 [Demanda potencial quantificada]
 [PreÃ§o viÃ¡vel Price/SAC]
 [PÃºblico-alvo definido]
    â†“
PASSO 7 (OFERTA) â† VOCÃŠ ESTÃ AQUI
    â†“
 [3 Tipologias de Oferta mapeadas]
 [VSO/IVV calculados]
 [Gaps de mercado identificados]
 [Alinhamento produto/desejo comprador]
    â†“
PASSO 8 (ABSORÃ‡ÃƒO)
    â†“
PASSO 9 (CONVALIDAÃ‡ÃƒO)
```

### 1.3. Outputs CrÃ­ticos

1. **MensuraÃ§Ã£o Total da Oferta** (3 tipologias)
2. **MÃ©tricas de EficiÃªncia** (VSO/IVV por bairro/tipologia)
3. **Alinhamento de Mercado** (sistema pontuaÃ§Ã£o 1/2)
4. **DecisÃ£o Go/Pivot/No-Go** fundamentada

---

## 2. QUANDO ACIONAR

### 2.1. Triggers ExplÃ­citos

- UsuÃ¡rio menciona: "oferta competitiva", "concorrÃªncia", "VSO", "velocidade de vendas"
- ReferÃªncia ao **Passo 7 TIV**
- Pergunta: "Quantos concorrentes tem na regiÃ£o?"
- SolicitaÃ§Ã£o: "Preciso saber se o mercado estÃ¡ saturado"

### 2.2. Triggers ImplÃ­citos

- Passo 6 (Demanda) foi concluÃ­do e usuÃ¡rio quer avanÃ§ar
- UsuÃ¡rio menciona preÃ§o/produto sem ter mapeado concorrÃªncia
- DÃºvida sobre "quanto posso cobrar" sem benchmark de mercado
- PreocupaÃ§Ã£o com "outros lanÃ§amentos que podem entrar"

### 2.3. PrÃ©-requisitos ObrigatÃ³rios

Antes de executar Passo 7, DEVE estar concluÃ­do:

âœ… **Passo 3:** Ãrea de influÃªncia delimitada (isÃ³cronas)  
âœ… **Passo 6:** Demanda quantificada + preÃ§o viÃ¡vel  

**Se nÃ£o estiverem completos:**

```
ALERTA: Para anÃ¡lise precisa de oferta, 
vocÃª precisa ter:

1. Ãrea de influÃªncia definida (Passo 3)
   â†’ Usar: Skill tiv-passo3-area-influencia
   
2. Demanda quantificada (Passo 6)
   â†’ Usar: Skill tiv-passo6-demanda

Deseja que eu te ajude com esses passos primeiro?
```

---

## 3. FRAMEWORK / METODOLOGIA

### 3.1. As TrÃªs Tipologias de Oferta

#### **OFERTA 1: Pulverizada**

**DefiniÃ§Ã£o:** ImÃ³veis usados, na mÃ£o de terceiros (proprietÃ¡rios individuais, imobiliÃ¡rias)

**CaracterÃ­sticas:**

- Sem padrÃ£o (preÃ§o, qualidade, prazo variam muito)
- Listados em portais (Viva Real, OLX, ZAP, Chaves na MÃ£o)
- RelevÃ¢ncia: **MÃ‰DIA** (compete indiretamente)

**Por que importa:**

> Se houver grande movimento de **investidores FPEIR** (Fases PrÃ©-Entrega, Imediata, Recente), haverÃ¡ uma **desova massiva de unidades prontas novas** que concorrerÃ£o diretamente com seu lanÃ§amento.

**Fontes:**

- Portais imobiliÃ¡rios (web scraping leve + limpeza)
- ImobiliÃ¡rias locais (tabelas)
- AnÃºncios classificados (jornais, redes sociais)

---

#### **OFERTA 2: LanÃ§amentos (Estoque PJ)**

**DefiniÃ§Ã£o:** Empreendimentos jÃ¡ lanÃ§ados, em construÃ§Ã£o ou recÃ©m-entregues, com estoque remanescente na PJ (construtora/incorporadora)

**CaracterÃ­sticas:**

- Produto novo vs novo (competiÃ§Ã£o DIRETA)
- Estoque conhecido (unidades nÃ£o vendidas)
- RelevÃ¢ncia: **ALTA** (seu concorrente direto)

**Por que importa:**

> Esta anÃ¡lise Ã© crucial para entender a **eficiÃªncia de venda** do mercado. Se concorrentes diretos tÃªm estoque alto e baixo VSO, indica saturaÃ§Ã£o.

**Fontes:**

- Sites de construtoras (tabelas de unidades disponÃ­veis)
- Stands de vendas (visita fÃ­sica)
- Corretores parceiros (tabelas assinadas)
- Cliente oculto (validaÃ§Ã£o)

---

#### **OFERTA 3: Futura (TBC - Terrenos Building Capacity)**

**DefiniÃ§Ã£o:** Projetos em tramitaÃ§Ã£o na Prefeitura (pipeline de aprovaÃ§Ã£o) ou jÃ¡ aprovados (alvarÃ¡ concedido)

**CaracterÃ­sticas:**

- NÃ£o estÃ¡ no mercado AINDA
- Pode ser lanÃ§ado a qualquer momento
- RelevÃ¢ncia: **CRÃTICA** (a mais perigosa)

**Por que Ã© a MAIS PERIGOSA:**

> **ESTUDO DE CASO "JOIA RARA" (fictÃ­cio):**
> 
> - Empreendedor investe massivamente em campanha de marketing (panela de pressÃ£o)
> - Promove novo bairro planejado "Joia Rara"
> - Concorrente descobre movimento de mercado
> - Concorrente JÃ tinha projeto similar APROVADO na Prefeitura
> - Em UMA sexta-feira, concorrente lanÃ§a e vende TUDO
> - Empreendedor original leva quase 2 ANOS para vender
> - **Motivo:** Demanda de intenÃ§Ã£o de compra foi CONSUMIDA

**Fontes:**

- Prefeitura Municipal:
    - **Pipeline:** Processos em anÃ¡lise
    - **Aprovados:** AlvarÃ¡s concedidos
- Lei de TransparÃªncia (dados pÃºblicos)
- Habeas Data (se Prefeitura recusar acesso)

**CRÃTICO:**

```
âš ï¸ ALERTA LEGAL: 
Tudo que tramita na Prefeitura deve ser pÃºblico 
(Lei de Acesso Ã  InformaÃ§Ã£o). 

LGPD protege CPF/Nome, mas vocÃª TEM DIREITO a:
- Tipo de empreendimento
- LocalizaÃ§Ã£o (lote, quadra, bairro)
- NÃºmero de unidades
- Fase do processo
- Data de protocolo/aprovaÃ§Ã£o

Se Prefeitura negar acesso:
â†’ Contratar advogado para Habeas Data
```

---

### 3.2. Metodologia TBC (Tira a Bunda da Cadeira)

**Problema:** Dados de mercado sÃ£o "sujos" e concorrentes podem ocultar informaÃ§Ãµes

**SoluÃ§Ã£o:** Aplicar **3 filtros sucessivos de validaÃ§Ã£o**

#### **Filtro 1: Corretores da RegiÃ£o**

- Corretores tÃªm acesso Ã s tabelas reais
- RelaÃ§Ã£o de confianÃ§a facilita informaÃ§Ã£o
- **LimitaÃ§Ã£o:** Podem ter viÃ©s (proteger parceiros)

#### **Filtro 2: Cliente Oculto**

- Pesquisador finge ser investidor/comprador
- Valida tabelas obtidas no Filtro 1
- Identifica unidades "reservadas fantasma" (inflam VSO)

#### **Filtro 3: Telefone por Amostragem**

- Terceira validaÃ§Ã£o por contato telefÃ´nico direto
- Confirma disponibilidade real
- Valida preÃ§os e condiÃ§Ãµes comerciais

**FrequÃªncia de AtualizaÃ§Ã£o:**

```
PRIMEIRA VEZ: Trabalho hercÃºleo (baseline)
DEPOIS: AtualizaÃ§Ã£o a cada 6 MESES
EXTRAORDINÃRIA: Se houver:
  - Novo alvarÃ¡ (Oferta Futura)
  - Pico de anÃºncios (Oferta Pulverizada)
  - LanÃ§amento grande concorrente
```

---

### 3.3. MÃ©tricas de EficiÃªncia

#### **3.3.1. VSO (Vendas Sobre Oferta)**

**FÃ³rmula:**

```
VSO = Unidades Vendidas (Ãºltimos 12m) Ã· Oferta Atual
```

**InterpretaÃ§Ã£o:**

| VSO           | Significado                       | AÃ§Ã£o Recomendada                       |
| ------------- | --------------------------------- | -------------------------------------- |
| VSO > 1,0     | Mercado aquecido (demanda > oferta) | âœ… FavorÃ¡vel para lanÃ§amento          |
| VSO 0,5-1,0   | Mercado equilibrado               | âš ï¸ Posicionamento correto Ã© crÃ­tico   |
| VSO < 0,5     | Mercado saturado (oferta > demanda) | âŒ Alto risco de estoque parado       |

**âš ï¸ ALERTA TIV:**

> VSO Ã© indicador **atrasado** (lagging). Ãštil para contexto, mas NÃƒO para projetar futuro. Para projeÃ§Ã£o, usar intenÃ§Ã£o de compra validada (Passo 9).

---

#### **3.3.2. IVV (Ãndice de Velocidade de Venda)**

**DefiniÃ§Ã£o:** Velocidade mÃ©dia de venda por regiÃ£o e tipologia

**CÃ¡lculo:**

```
IVV = Unidades Vendidas (perÃ­odo) Ã· Meses do PerÃ­odo
```

**Exemplo:**

```
PerÃ­odo: Jan-Dez 2024 (12 meses)
Bairro: Saco dos LimÃµes (FlorianÃ³polis)
Tipologia: 1 quarto
Vendas: 200 unidades

IVV = 200 un Ã· 12 meses = 16,67 un/mÃªs
```

**Uso com Mediana:**

```
IVV de Mercado: Mediana = 1,46

ClassificaÃ§Ã£o por Bairro:
- Agronomica: IVV 8,57% > Mediana âœ… (acima)
- Centro: IVV 1,40% = Mediana âš ï¸ (igual)
- Itacorubi: IVV 1,33% < Mediana âŒ (abaixo)
```

**DecisÃ£o:**

- **Acima da mediana:** Bairro atrativo, produto competitivo
- **Igual Ã  mediana:** Mercado equilibrado, nÃ£o Ã© diferencial
- **Abaixo da mediana:** SaturaÃ§Ã£o ou produto mal posicionado

---

### 3.4. Alinhamento de Mercado (Sistema 1/2)

**Objetivo:** Quantificar quÃ£o alinhado o produto estÃ¡ com o **desejo de pagar** do comprador

#### **Sistema de PontuaÃ§Ã£o**

Para cada atributo do produto (lazer, vagas, sustentabilidade, etc.), fazer 2 perguntas:

**P1: VocÃª acha importante?**

- âœ… Sim
- âŒ NÃ£o

**P2: VocÃª pagaria a mais para ter isso?**

- âœ… Sim
- âŒ NÃ£o

**PontuaÃ§Ã£o:**

| Resposta                                          | PontuaÃ§Ã£o | Significado                          |
| ------------------------------------------------- | --------- | ------------------------------------ |
| Importante, mas **NÃƒO pagaria a mais**           | **1**     | Commodity (item esperado)            |
| Importante e **PAGARIA A MAIS** para ter          | **2**     | Diferencial (valor agregado "foda") |
| NÃ£o importante                                    | **0**     | Irrelevante (nÃ£o investir)           |

**Exemplo de AplicaÃ§Ã£o:**

```
ATRIBUTOS TESTADOS:

1. Quadra Poliesportiva
   - Importante: SIM
   - Pagaria a mais: NÃƒO
   â†’ PontuaÃ§Ã£o: 1 (commodity)

2. EspaÃ§o Pet
   - Importante: SIM
   - Pagaria a mais: SIM
   â†’ PontuaÃ§Ã£o: 2 (diferencial)

3. Sustentabilidade
   - Importante: SIM
   - Pagaria a mais: SIM
   â†’ PontuaÃ§Ã£o: 2 (diferencial)

4. Sala de Cinema
   - Importante: NÃƒO
   - Pagaria a mais: NÃƒO
   â†’ PontuaÃ§Ã£o: 0 (irrelevante)

TOTAL PRODUTO A: 1+2+2+0 = 5 pontos
```

**ComparaÃ§Ã£o Competitiva:**

```
CONCORRENTES MAPEADOS:

Passarela Park Prime:  12 pontos (mais alinhado)
TrÃªs Meia Zero:         8 pontos
Vivet:                  8 pontos
Rioja Residence:        7 pontos
Three Tower:            5 pontos (menos alinhado)

DECISÃƒO:
â†’ Estudar Passarela Park Prime
â†’ Identificar atributos "foda" (score 2)
â†’ Potencializar no projeto arquitetÃ´nico
```

---

### 3.5. Fatores de AbsorÃ§Ã£o (ConexÃ£o Financeira)

**Objetivo:** Determinar pressÃ£o de vendas atravÃ©s da relaÃ§Ã£o Demanda:Oferta

| CenÃ¡rio       | RelaÃ§Ã£o (Demanda:Oferta) | DescriÃ§Ã£o                                                           |
| ------------- | ------------------------ | ------------------------------------------------------------------- |
| **Potencial** | **10:1**                 | Fase inicial, anÃ¡lise de potencial de compra (Renda + DomicÃ­lio)   |
| **HistÃ³rico** | **4:1**                  | HistÃ³rico TIV: para cada 4 que dizem que compram, 1 compra          |
| **Qualificado** | **3:1**                | MÃ­nimo ideal para pressÃ£o de vendas (cadastros qualificÃ¡veis)      |
| **Perigoso**  | **< 3:1**                | MUITO PERIGOSO para saÃºde do lanÃ§amento                             |

**Exemplo de CÃ¡lculo:**

```
DEMANDA (Passo 6):
Demanda Potencial: 1.200 famÃ­lias
IntenÃ§Ã£o de Compra: 35%
Demanda Real: 1.200 Ã— 35% = 420 famÃ­lias

OFERTA (Passo 7):
Oferta Pulverizada: 150 un
LanÃ§amentos: 92 un
Oferta Futura: 80 un (pipeline)
TOTAL OFERTA: 322 un

RAZÃƒO: 420 Ã· 322 = 1,30:1

DECISÃƒO: âŒ ABAIXO de 3:1 â†’ PERIGOSO
         Mercado saturado, risco alto
```

---

## 4. INPUTS NECESSÃRIOS

### 4.1. Do Passo 3 (Ãrea de InfluÃªncia)

- [ ] PolÃ­gono de influÃªncia (shapefile ou KML)
- [ ] IsÃ³cronas (10/20/30 min)
- [ ] Bairros/subÃ¡reas abrangidos
- [ ] PopulaÃ§Ã£o por subÃ¡rea

### 4.2. Do Passo 6 (Demanda)

- [ ] Demanda potencial quantificada (nÂº famÃ­lias)
- [ ] PreÃ§o viÃ¡vel Price/SAC
- [ ] Perfil pÃºblico-alvo (4 dimensÃµes)
- [ ] Percentual de intenÃ§Ã£o de compra

### 4.3. Dados PrimÃ¡rios (Coleta Oferta)

**Oferta Pulverizada:**

- [ ] AnÃºncios em portais (Viva Real, OLX, ZAP)
- [ ] Data da coleta
- [ ] Link do anÃºncio

**LanÃ§amentos:**

- [ ] Nome do empreendimento
- [ ] Estoque remanescente (unidades)
- [ ] Tipologia (dorms, vagas, mÂ²)
- [ ] PreÃ§o e preÃ§o/mÂ²
- [ ] PadrÃ£o (econÃ´mico/mÃ©dio/alto)
- [ ] EvidÃªncia (tabela, print, cliente oculto)

**Oferta Futura:**

- [ ] NÂº do processo na Prefeitura
- [ ] Fase (em anÃ¡lise / aprovado)
- [ ] Data de protocolo
- [ ] Prazo previsto
- [ ] Tipologia e nÃºmero de unidades

---

## 5. PROCESSO DE ANÃLISE

### ETAPA 1: Coleta da Oferta Pulverizada

**MÃ©todo:** Web scraping leve + limpeza manual

```
AÃ‡Ã•ES:
1. Definir raio de busca (Ã¡rea de influÃªncia)
2. Coletar anÃºncios em portais
3. Deduplicar por endereÃ§o/empreendimento
4. Remover "reservado" sem lastro (inflaÃ§Ã£o artificial)
5. Consolidar preÃ§o/mÂ² por tipologia
6. Preencher template O7-1_oferta_pulverizada.csv
```

**Template CSV:**

```csv
id_anuncio;portal;link;data_coleta;endereco;bairro;cidade;uf;tipologia;dorms;vagas;metragem_m2;preco_total;preco_m2;status;contato;fonte;observacoes
```

**Exemplo de Linha:**

```csv
VR12345;VivaReal;https://...;2024-10-31;Rua ABC 123;Centro;Leopoldina;MG;Apartamento;2;1;65;280000;4307.69;Disponivel;31999999999;Portal;Proximo ao comercio
```

---

### ETAPA 2: Coleta de LanÃ§amentos (Estoque PJ)

**MÃ©todo:** TBC + 3 Filtros de ValidaÃ§Ã£o

```
AÃ‡Ã•ES:
1. Listar empreendimentos em construÃ§Ã£o (raio 2-5 km)
2. Coletar dados com corretores (Filtro 1)
3. Validar com cliente oculto (Filtro 2)
4. Confirmar por telefone (Filtro 3)
5. Registrar evidÃªncias (tabela, print, gravaÃ§Ã£o)
6. Preencher O7-2_lancamentos_estoque.csv
```

**Estrutura CSV:**

```csv
empreendimento;construtora;estoque_remanescente;dorms;vagas;metragem_m2;preco_total;preco_m2;padrao;fase_obra;data_lancamento;evidencia;observacoes
```

**Exemplo de Linha:**

```csv
Residencial Horizonte;Construtora XYZ;15;2;1;68;320000;4705.88;Medio;60%;2023-05;Tabela_assinada.pdf;Unidades sul ainda disponiveis
```

---

### ETAPA 3: Coleta da Oferta Futura (Prefeitura)

**MÃ©todo:** Protocolo formal na Prefeitura

```
AÃ‡Ã•ES:
1. Protocolar pedido de acesso (LAI)
2. Solicitar:
   - Processos em anÃ¡lise (pipeline)
   - AlvarÃ¡s concedidos (Ãºltimos 24 meses)
   - LocalizaÃ§Ã£o, tipologia, unidades
3. Se negado: Habeas Data via advogado
4. Registrar processos em O7-3_oferta_futura_prefeitura.csv
5. Mapear em QGIS (pontos/polÃ­gonos)
```

**Template CSV:**

```csv
processo;fase;tipologia;unidades;logradouro;bairro;cidade;uf;latitude;longitude;area_m2;alvara;fase_dt;prazo_previsto;status;observacoes
```

**Exemplo de Linha:**

```csv
2024/0123;Aprovado;Loteamento;45;Rua Nova Esperanca;Rural;Leopoldina;MG;-21.531;-42.645;22000;456/2024;2024-09-15;2025-12;Ativo;Projeto aprovado aguardando licenca ambiental
```

**Mapa QGIS:**

```
LAYERS:
1. Ãrea de InfluÃªncia (polÃ­gono)
2. Oferta Futura - Pipeline (pontos vermelhos)
3. Oferta Futura - Aprovados (pontos amarelos)
4. Seu Terreno (ponto verde)

SIMBOLOGIA:
- Tamanho proporcional ao nÂº de unidades
- TransparÃªncia por fase (anÃ¡lise vs aprovado)
```

---

### ETAPA 4: CÃ¡lculo IVV/VSO

**MÃ©todo:** AnÃ¡lise por bairro/tipologia

```
AÃ‡Ã•ES:
1. Consolidar vendas Ãºltimos 12 meses (fontes mÃºltiplas)
2. Calcular VSO por empreendimento
3. Calcular IVV por bairro/tipologia
4. Determinar mediana de mercado
5. Classificar cada subÃ¡rea vs mediana
6. Preencher O7-4_ivv_vso_dashboard.csv
```

**Template CSV:**

```csv
periodo_inicio;periodo_fim;bairro_subarea;tipologia;ivv;vso;vendas;estoque_medio;preco_m2_mediana;fonte;observacoes
```

**Exemplo de Linha:**

```csv
2023-11-01;2024-10-31;Centro;2 dorms;1.85;0.78;24;30;5200;SECOVI;Mercado equilibrado
```

**Benchmark:**

```
MEDIANA DE MERCADO: 1,46

CLASSIFICAÃ‡ÃƒO:
- Agronomica (8,57%): âœ… Acima (4x mediana)
- Centro (1,40%): âš ï¸ Igual
- Itacorubi (1,33%): âŒ Abaixo
```

---

### ETAPA 5: Alinhamento de Mercado

**MÃ©todo:** Pesquisa rÃ¡pida + sistema 1/2

```
AÃ‡Ã•ES:
1. Definir â‰¤12 atributos relevantes para produto
2. Rodar pesquisa rÃ¡pida (pode ser em paralelo ao Passo 9)
3. Perguntar:
   - Ã‰ importante? (sim/nÃ£o)
   - Pagaria a mais? (sim/nÃ£o)
4. Pontuar: 0 (irrelevante), 1 (commodity), 2 (foda)
5. Comparar com concorrentes
6. Preencher O7-5_alinhamento_mercado.csv
```

**Template CSV:**

```csv
entidade;atributo;classe_atributo(1_essencial|2_diferencial);importante(sim_nao);pagaria_mais(sim_nao);score(0-2);observacoes
```

**Exemplo de Linha:**

```csv
Residencial Horizonte;Espaco Pet;2_diferencial;sim;sim;2;Atributo valorizado por familias
Residencial Horizonte;Academia;1_essencial;sim;nao;1;Esperado em empreendimentos medio padrao
```

**Score Consolidado:**

```
CONCORRENTES:

1. Passarela Park Prime: 12 pontos
   Atributos "foda" (score 2):
   - Quadra Poliesportiva
   - EspaÃ§o Pet
   - Sustentabilidade
   - Varanda no apartamento
   - Academia
   - Vagas de Garagem

2. TrÃªs Meia Zero: 8 pontos
3. Vivet: 8 pontos
4. Rioja Residence: 7 pontos
5. Three Tower: 5 pontos

DECISÃƒO:
â†’ Nosso produto deve ter â‰¥12 pontos para competir
â†’ Priorizar atributos score 2 no projeto arquitetÃ´nico
â†’ NÃ£o gastar com atributos score 0 ou 1
```

---

### ETAPA 6: Gates de DecisÃ£o

**Gate 1: RazÃ£o Demanda:Oferta**

```
CRITÃ‰RIO: Demanda Ã· Oferta â‰¥ 3:1

SE < 3:1 â†’ âŒ MERCADO SATURADO
SE 3-4:1 â†’ âš ï¸ EQUILIBRADO (posicionamento crÃ­tico)
SE 4-10:1 â†’ âœ… FAVORÃVEL
SE > 10:1 â†’ âœ… DEMANDA REPRIMIDA
```

**Gate 2: IVV vs Mediana**

```
CRITÃ‰RIO: IVV â‰¥ Mediana de Mercado

SE < Mediana â†’ âŒ BAIRRO SATURADO
SE = Mediana â†’ âš ï¸ MERCADO EQUILIBRADO
SE > Mediana â†’ âœ… BAIRRO AQUECIDO
```

**Gate 3: VSO Concorrentes**

```
CRITÃ‰RIO: VSO Concorrentes â‰¥ 0,5

SE < 0,5 â†’ âŒ CONCORRENTES COM ESTOQUE PARADO
SE 0,5-1,0 â†’ âš ï¸ VENDAS EQUILIBRADAS
SE > 1,0 â†’ âœ… MERCADO AQUECIDO
```

**Gate 4: Risco Oferta Futura**

```
CRITÃ‰RIO: Oferta Futura (aprovados) < 50% do seu produto

SE > 100% â†’ âŒ ALTO RISCO CANIBALIZAÃ‡ÃƒO
SE 50-100% â†’ âš ï¸ MÃ‰DIO RISCO (monitorar)
SE < 50% â†’ âœ… RISCO CONTROLADO
```

**DecisÃ£o Consolidada:**

```
MATRIZ DE DECISÃƒO:

Gate 1  Gate 2  Gate 3  Gate 4  â†’ DecisÃ£o
  âœ…      âœ…      âœ…      âœ…   â†’ GO (viÃ¡vel)
  âš ï¸      âœ…      âœ…      âœ…   â†’ GO com atenÃ§Ã£o
  âŒ      âœ…      âš ï¸      âœ…   â†’ PIVOT (ajustar)
  âŒ      âŒ      âŒ      âš ï¸   â†’ NO-GO (inviÃ¡vel)
```

---

## 6. OUTPUTS ESPERADOS

### 6.1. Outputs ObrigatÃ³rios (7 arquivos)

**1. O7-1_oferta_pulverizada.csv**

- Portal, link, endereÃ§o, tipologia, mÂ², preÃ§o, preÃ§o/mÂ², status
- Fonte validada (data coleta)

**2. O7-2_lancamentos_estoque.csv**

- Empreendimento, estoque, dorms, vagas, mÂ², preÃ§o, preÃ§o/mÂ²
- PadrÃ£o, evidÃªncia (tabela, cliente oculto)

**3. O7-3_oferta_futura_prefeitura.csv**

- Processo, fase (anÃ¡lise/aprovado), tipologia, unidades
- LocalizaÃ§Ã£o (lat/long), prazos, observaÃ§Ãµes

**4. O7-4_ivv_vso_dashboard.csv**

- PerÃ­odo, bairro/subÃ¡rea, tipologia, IVV, VSO
- Mediana de mercado (para benchmark)

**5. O7-5_alinhamento_mercado.csv**

- Atributo, "importante" (sim/nÃ£o), "pagaria a mais" (sim/nÃ£o)
- Score (1/2) por concorrente/produto

**6. Mapa Oferta Futura (QGIS/KML)**

- Pontos/polÃ­gonos dos processos
- Simbologia por fase (pipeline/aprovado)
- Layer Ã¡rea de influÃªncia

**7. Resumo Executivo P7 (1 pÃ¡gina)**

- PressÃ£o competitiva (Demanda:Oferta)
- Risco de canibalizaÃ§Ã£o (Oferta Futura)
- RecomendaÃ§Ã£o de preÃ§o/mix vs Passo 6
- DecisÃ£o Go/Pivot/No-Go

---

### 6.2. Template Resumo Executivo

```markdown
# RESUMO EXECUTIVO - PASSO 7: OFERTA

**Projeto:** [Nome do Empreendimento]  
**MunicÃ­pio:** [Cidade-UF]  
**Data:** [DD/MM/AAAA]

---

## 1. SÃNTESE

**RazÃ£o Demanda:Oferta:** [X:1]  
**IVV vs Mediana:** [Valor] vs [Mediana] â†’ [Acima/Igual/Abaixo]  
**VSO MÃ©dio Concorrentes:** [Valor]  
**Risco Oferta Futura:** [Baixo/MÃ©dio/Alto]  
**DecisÃ£o:** [GO / PIVOT / NO-GO]

---

## 2. TRÃŠS OFERTAS CONSOLIDADAS

### Oferta Pulverizada
- **Total:** [XXX] unidades
- **Faixa preÃ§o/mÂ²:** R$ [MIN] - R$ [MAX]
- **Tipologia predominante:** [X] dorms
- **RelevÃ¢ncia:** [Baixa/MÃ©dia/Alta]

### LanÃ§amentos (Estoque PJ)
- **Total:** [XX] unidades em [Y] empreendimentos
- **VSO mÃ©dio:** [Valor]
- **Empreendimentos mapeados:**
  1. [Nome] - [Estoque] un - R$ [PreÃ§o/mÂ²]
  2. [Nome] - [Estoque] un - R$ [PreÃ§o/mÂ²]
  3. [Nome] - [Estoque] un - R$ [PreÃ§o/mÂ²]

### Oferta Futura (TBC)
- **Pipeline (em anÃ¡lise):** [XX] unidades
- **Aprovados (alvarÃ¡):** [XX] unidades
- **Total:** [XXX] unidades
- **Prazo entrada mercado:** [X] meses

---

## 3. MÃ‰TRICAS DE EFICIÃŠNCIA

### IVV por Bairro (vs Mediana = [Valor])

| Bairro       | IVV   | ClassificaÃ§Ã£o |
|--------------|-------|---------------|
| [Bairro 1]   | [Val] | âœ… Acima      |
| [Bairro 2]   | [Val] | âš ï¸ Igual     |
| [Bairro 3]   | [Val] | âŒ Abaixo    |

### VSO Concorrentes

| Empreendimento | VSO   | Status          |
|----------------|-------|-----------------|
| [Nome 1]       | [Val] | âœ… SaudÃ¡vel    |
| [Nome 2]       | [Val] | âš ï¸ Equilibrado |
| [Nome 3]       | [Val] | âŒ Estoque Alto|

---

## 4. ALINHAMENTO DE MERCADO

**Concorrente mais alinhado:** [Nome] - [XX] pontos

**Atributos "foda" (score 2) identificados:**
1. [Atributo 1]
2. [Atributo 2]
3. [Atributo 3]

**RecomendaÃ§Ã£o arquitetÃ´nica:**
â†’ Priorizar [atributos] no projeto
â†’ Evitar investir em [atributos score 0/1]

---

## 5. GATES DE DECISÃƒO

| Gate                   | Resultado | Status |
|------------------------|-----------|--------|
| Demanda:Oferta         | [X:1]     | [âœ…âš ï¸âŒ]|
| IVV vs Mediana         | [Val]     | [âœ…âš ï¸âŒ]|
| VSO Concorrentes       | [Val]     | [âœ…âš ï¸âŒ]|
| Risco Oferta Futura    | [%]       | [âœ…âš ï¸âŒ]|

**DecisÃ£o Consolidada:** [GO / PIVOT / NO-GO]

---

## 6. RECOMENDAÃ‡Ã•ES

### PreÃ§o
[Ajustar preÃ§o para R$ X/mÂ² baseado em...]

### Produto
[Priorizar tipologia X dorms porque...]

### Timing
[LanÃ§ar em X meses para evitar Oferta Futura...]

### Posicionamento
[Diferenciar em atributos X, Y, Z...]

---

**PrÃ³ximo Passo:** PASSO 8 - AbsorÃ§Ã£o (Velocidade de Vendas)
```

---

## 7. ALERTAS E VALIDAÃ‡Ã•ES

### 7.1. Red Flags CrÃ­ticos

âŒ **Usar somente anÃºncios online sem validaÃ§Ã£o**

```
PROBLEMA: 
Oferta Pulverizada pode ter anÃºncios duplicados, 
unidades "reservadas fantasma" ou preÃ§os irreais.

SOLUÃ‡ÃƒO: 
Aplicar 3 filtros TBC obrigatoriamente.
```

âŒ **Ignorar Oferta Futura (prefeitura)**

```
PROBLEMA: 
Concorrente pode lanÃ§ar projeto aprovado e consumir 
demanda de intenÃ§Ã£o de compra (Caso Joia Rara).

SOLUÃ‡ÃƒO: 
Protocolar pedido na Prefeitura SEMPRE.
Se negar acesso, Habeas Data via advogado.
```

âŒ **Calcular IVV/VSO sem benchmark de mediana**

```
PROBLEMA: 
NÃ£o saber se IVV 2,5% Ã© bom ou ruim sem contexto.

SOLUÃ‡ÃƒO: 
Calcular mediana de mercado para classificaÃ§Ã£o.
```

âŒ **Montar atributos "foda" sem medir "pagaria a mais"**

```
PROBLEMA: 
Investir em atributos que pÃºblico acha importante, 
mas nÃ£o pagaria a mais (commodity).

SOLUÃ‡ÃƒO: 
Usar sistema 1/2 para identificar verdadeiros diferenciais.
```

---

### 7.2. Checklist de ValidaÃ§Ã£o

**Antes de considerar Passo 7 CONCLUÃDO:**

#### Coleta de Dados (6 itens)

- [ ] **As 3 ofertas** consolidadas (Pulverizada, LanÃ§amentos, Futura)
- [ ] **3 filtros TBC** aplicados (corretores, cliente oculto, telefone)
- [ ] **Oferta Futura** mapeada com evidÃªncia documental
- [ ] Dados deduplicados e limpos
- [ ] Templates CSV preenchidos
- [ ] Mapa QGIS gerado

#### MÃ©tricas (4 itens)

- [ ] **IVV/VSO** calculados por tipologia
- [ ] **Mediana de mercado** definida
- [ ] ConcorrÃªncia comparada Ã  mediana
- [ ] Velocidade histÃ³rica documentada

#### Alinhamento (3 itens)

- [ ] **Tabela 1/2** aplicada (â‰¤12 atributos)
- [ ] Score consolidado por concorrente
- [ ] Atributos "foda" identificados

#### Gates (4 itens)

- [ ] **Gate 1:** RazÃ£o Demanda:Oferta calculada
- [ ] **Gate 2:** IVV vs Mediana avaliado
- [ ] **Gate 3:** VSO concorrentes analisado
- [ ] **Gate 4:** Risco Oferta Futura mensurado

#### IntegraÃ§Ã£o (4 items)

- [ ] Comparado ao **PreÃ§o de stand** (Passo 6)
- [ ] Gaps de mercado identificados
- [ ] Posicionamento competitivo definido
- [ ] Insumos enviados ao **Passo 8** (AbsorÃ§Ã£o)

**TOTAL: 21 validaÃ§Ãµes**

---

## 8. INTEGRAÃ‡ÃƒO COM OUTRAS SKILLS

### 8.1. Skills PrÃ©-requisito (Inputs)

#### **tiv-passo3-area-influencia**

**Consome:**

- PolÃ­gono de influÃªncia (shapefile/KML)
- IsÃ³cronas (10/20/30 min)
- Bairros abrangidos
- PopulaÃ§Ã£o por subÃ¡rea

**Uso no Passo 7:**

- Definir raio de busca para oferta
- Filtrar concorrentes dentro da Ã¡rea relevante
- Estratificar IVV/VSO por subÃ¡rea

---

#### **tiv-passo6-demanda**

**Consome:**

- Demanda potencial calculada
- PreÃ§o viÃ¡vel Price/SAC
- Perfil pÃºblico-alvo
- Percentual de intenÃ§Ã£o de compra

**Uso no Passo 7:**

- **Calcular razÃ£o Demanda:Oferta** (Gate 1)
- Benchmark preÃ§o (seu produto vs concorrentes)
- Validar se perfil pÃºblico-alvo tem oferta compatÃ­vel

**Exemplo Cruzamento:**

```
PASSO 6 (Demanda):
Demanda: 420 famÃ­lias
PreÃ§o viÃ¡vel: R$ 320.000 (R$ 4.700/mÂ²)
Tipologia: 2 dorms, 1 vaga, 68mÂ²

PASSO 7 (Oferta):
Oferta Total: 322 unidades
PreÃ§o mÃ©dio concorrentes: R$ 4.850/mÂ²
Tipologia predominante: 2 dorms, 1 vaga, 65-70mÂ²

RAZÃƒO: 420 Ã· 322 = 1,30:1 âŒ ABAIXO de 3:1

CONCLUSÃƒO: 
- Mercado saturado
- PreÃ§o competitivo (R$ 4.700 vs R$ 4.850)
- Produto alinhado (tipologia similar)
- DECISÃƒO: PIVOT (aguardar absorÃ§Ã£o ou diferenciar)
```

---

### 8.2. Skills Consumidoras (Outputs)

#### **tiv-passo8-absorcao**

**Fornece:**

- Oferta total consolidada (3 tipologias)
- VSO histÃ³rico (velocidade passada)
- IVV por bairro (velocidade regional)
- PressÃ£o competitiva (Demanda:Oferta)

**Uso no Passo 8:**

- Benchmark velocidade (VSO histÃ³rico vs projeÃ§Ã£o)
- Ajustar Fator 4:1 se mercado aquecido/saturado
- Cronograma de absorÃ§Ã£o fundamentado

---

#### **tiv-passo9-convalidacao**

**Fornece:**

- Concorrentes mapeados (nomes, produtos, preÃ§os)
- Atributos "foda" identificados (score 2)
- Gaps de mercado (oportunidades)

**Uso no Passo 9:**

- Validar concorrentes na pesquisa primÃ¡ria
- Testar atributos score 2 com amostra
- Confirmar gaps de mercado (demanda nÃ£o atendida)

---

#### **tiv-passo10-fcd**

**Fornece:**

- PreÃ§o competitivo (benchmark concorrentes)
- Velocidade esperada (IVV/VSO)
- Risco de canibalizaÃ§Ã£o (Oferta Futura)

**Uso no Passo 10:**

- ProjeÃ§Ã£o de receitas (VGV) com preÃ§o validado
- Cronograma de vendas (absorÃ§Ã£o realista)
- CenÃ¡rios (base/conservador) com pressÃ£o competitiva

---

#### **tiv-pith**

**Fornece:**

- SeÃ§Ã£o "AnÃ¡lise Competitiva" (2-3 pÃ¡ginas)
- Mapa concorrÃªncia
- Tabela VSO/IVV
- Posicionamento estratÃ©gico

---

## 9. EXEMPLOS PRÃTICOS

### EXEMPLO 1: Loteamento EconÃ´mico - Leopoldina-MG

**Contexto:**

- Terreno: 22.000 mÂ², ZEU
- Produto: 35 lotes 250mÂ², R$ 120-150k
- PÃºblico: Faixa C-D (R$ 3.000-5.000)
- Demanda (Passo 6): 180 famÃ­lias

---

**COLETA DE OFERTA:**

**Oferta Pulverizada:**

```
Portal: OLX + Viva Real
Filtro: Leopoldina + Lote + R$ 100-200k
Resultado: 12 anÃºncios
Deduplicados: 8 lotes Ãºnicos
MÃ©dia preÃ§o/mÂ²: R$ 480
```

**LanÃ§amentos:**

```
Empreendimento: Jardim das Flores
Incorporadora: Construtora Local XYZ
Estoque: 8 lotes (de 40 originais)
Tipologia: 300mÂ², R$ 135.000 (R$ 450/mÂ²)
VSO: 32 vendidos em 18 meses = 1,78 un/mÃªs
Fase: 80% vendido
EvidÃªncia: Tabela assinada + cliente oculto
```

**Oferta Futura:**

```
Processo: 2024/0089
Fase: EM ANÃLISE (pipeline)
Tipologia: Loteamento 50 lotes
LocalizaÃ§Ã£o: Zona Rural (3 km do nosso terreno)
Prazo previsto: AprovaÃ§Ã£o em 6 meses
Status: Aguardando licenÃ§a ambiental
```

---

**MÃ‰TRICAS:**

**IVV:**

```
Leopoldina - Loteamentos:
Ãšltimos 12m: 65 lotes vendidos
IVV = 65 Ã· 12 = 5,42 un/mÃªs

Mediana de mercado: 4,0 un/mÃªs
ClassificaÃ§Ã£o: âœ… ACIMA (Leopoldina aquecida)
```

**VSO:**

```
Jardim das Flores: 32 vendidos Ã· 40 total = 0,80
Mercado equilibrado (prÃ³ximo de 1,0)
```

**RazÃ£o Demanda:Oferta:**

```
DEMANDA: 180 famÃ­lias
OFERTA: 
  Pulverizada: 8 lotes
  LanÃ§amentos: 8 lotes (Jardim das Flores)
  Futura: 50 lotes (pipeline)
  TOTAL: 66 lotes

RAZÃƒO: 180 Ã· 66 = 2,73:1

âŒ ABAIXO de 3:1 (perigoso)
âš ï¸ Risco mÃ©dio se Oferta Futura entrar
```

---

**ALINHAMENTO DE MERCADO:**

```
ATRIBUTOS TESTADOS (pesquisa rÃ¡pida, n=50):

1. Infraestrutura bÃ¡sica (Ã¡gua, luz, esgoto)
   - Importante: 100% SIM
   - Pagaria a mais: 80% SIM
   â†’ Score: 2 (diferencial CRÃTICO)

2. Asfalto
   - Importante: 90% SIM
   - Pagaria a mais: 40% NÃƒO
   â†’ Score: 1 (commodity)

3. Ãrea de lazer comum
   - Importante: 60% SIM
   - Pagaria a mais: 20% NÃƒO
   â†’ Score: 1 (commodity)

4. Portaria 24h
   - Importante: 40% SIM
   - Pagaria a mais: 10% NÃƒO
   â†’ Score: 0 (irrelevante para pÃºblico C-D)

CONCLUSÃƒO:
â†’ Priorizar infraestrutura 100% (Ã¡gua, luz, esgoto)
â†’ Asfalto Ã© esperado (nÃ£o diferencial)
â†’ NÃ£o investir em portaria (custo x benefÃ­cio ruim)
```

---

**GATES DE DECISÃƒO:**

```
Gate 1: Demanda:Oferta = 2,73:1 âŒ (< 3:1)
Gate 2: IVV = 5,42 vs Mediana 4,0 âœ… (acima)
Gate 3: VSO Jardim = 0,80 âœ… (saudÃ¡vel)
Gate 4: Oferta Futura = 50 lotes (142% do nosso) âŒ

DECISÃƒO: PIVOT (com atenÃ§Ã£o)
```

---

**RECOMENDAÃ‡ÃƒO:**

```
POSICIONAMENTO:
- Diferenciar em INFRAESTRUTURA (score 2)
- Garantir 100% Ã¡gua, luz, esgoto ANTES do lanÃ§amento
- PreÃ§o competitivo: R$ 120-135k (abaixo Jardim)
- LanÃ§ar ANTES de Oferta Futura (6 meses janela)

TIMING:
- Acelerar aprovaÃ§Ã£o (3 meses)
- LanÃ§amento em 4-5 meses (antes do concorrente)
- Se perder janela, AGUARDAR absorÃ§Ã£o de ambos

DECISÃƒO FINAL: GO com atenÃ§Ã£o (timing crÃ­tico)
```

---

### EXEMPLO 2: Vertical MÃ©dio PadrÃ£o - Leopoldina-MG

**Contexto:**

- Terreno: 1.200 mÂ², Av. Tiradentes (centro)
- Produto: 16 aptos 2 dorms, R$ 420.000
- PÃºblico: Faixa B-C (R$ 6.000-8.000)
- Demanda (Passo 6): 220 famÃ­lias

---

**COLETA DE OFERTA:**

**Oferta Pulverizada:**

```
Portal: Viva Real
Filtro: Leopoldina + 2 dorms + R$ 350-500k
Resultado: 3 anÃºncios (usados)
MÃ©dia preÃ§o/mÂ²: R$ 6.200
RelevÃ¢ncia: Baixa (competiÃ§Ã£o indireta)
```

**LanÃ§amentos:**

```
NENHUM empreendimento vertical em Leopoldina
Ãšltimo lanÃ§amento: 2019 (5 anos atrÃ¡s)

ReferÃªncia regional (Cataguases, 30 km):
Empreendimento: Residencial Cataguases
Estoque: 4 aptos (de 20 originais)
Tipologia: 2 dorms, 1 vaga, 70mÂ²
PreÃ§o: R$ 380.000 (R$ 5.428/mÂ²)
VSO: 16 vendidos em 24 meses = 0,67 un/mÃªs
```

**Oferta Futura:**

```
Prefeitura Leopoldina:
NENHUM processo de vertical em anÃ¡lise
NENHUM alvarÃ¡ concedido (Ãºltimos 36 meses)

GAP IDENTIFICADO: âœ…
Sem oferta vertical nova em Leopoldina!
```

---

**MÃ‰TRICAS:**

**IVV:**

```
Leopoldina - Vertical:
NÃ£o hÃ¡ IVV (sem lanÃ§amentos recentes)

ReferÃªncia Cataguases:
IVV = 16 Ã· 24 = 0,67 un/mÃªs
Mediana regional: 1,2 un/mÃªs
ClassificaÃ§Ã£o: âŒ ABAIXO (mercado devagar)
```

**RazÃ£o Demanda:Oferta:**

```
DEMANDA: 220 famÃ­lias
OFERTA: 
  Pulverizada: 3 usados (irrelevante)
  LanÃ§amentos: 0
  Futura: 0
  TOTAL: ~0 (GAP!)

RAZÃƒO: 220 Ã· 3 = 73:1

âœ… MUITO ACIMA de 10:1 (demanda reprimida!)
```

---

**ALINHAMENTO DE MERCADO:**

```
(NÃ£o hÃ¡ concorrentes diretos para comparar)

ATRIBUTOS ESSENCIAIS (pesquisa, n=60):

1. Varanda gourmet
   - Importante: 85% SIM
   - Pagaria a mais: 70% SIM
   â†’ Score: 2 (diferencial FORTE)

2. 2 vagas de garagem
   - Importante: 90% SIM
   - Pagaria a mais: 60% SIM
   â†’ Score: 2 (diferencial)

3. Elevador
   - Importante: 95% SIM
   - Pagaria a mais: 30% NÃƒO
   â†’ Score: 1 (commodity obrigatÃ³rio)

4. Piscina
   - Importante: 50% SIM
   - Pagaria a mais: 15% NÃƒO
   â†’ Score: 0 (irrelevante)

CONCLUSÃƒO:
â†’ Priorizar varanda gourmet (diferencial forte)
â†’ 2 vagas Ã© essencial (pÃºblico B-C tem 2 carros)
â†’ Elevador esperado (nÃ£o diferencial)
â†’ NÃ£o fazer piscina (custo x benefÃ­cio ruim)
```

---

**GATES DE DECISÃƒO:**

```
Gate 1: Demanda:Oferta = 73:1 âœ… (demanda reprimida)
Gate 2: IVV = N/A (sem referÃªncia local) âš ï¸
Gate 3: VSO = 0 (sem concorrentes) âœ…
Gate 4: Oferta Futura = 0 âœ… (sem risco)

DECISÃƒO: GO (oportunidade clara!)
```

---

**RECOMENDAÃ‡ÃƒO:**

```
POSICIONAMENTO:
- PIONEIRISMO: Primeiro vertical em Leopoldina em 5 anos
- Produto diferenciado: varanda gourmet + 2 vagas
- PreÃ§o premium: R$ 420k (R$ 6.000/mÂ²) justificado
- Marketing: "Ãšnico no centro com 2 vagas"

RISCO:
- Sem referÃªncia local de VSO (mercado nÃ£o testado)
- MitigaÃ§Ã£o: Fase 1 (8 aptos) + Fase 2 (8 aptos)
- Testar mercado antes de construir tudo

TIMING:
- LanÃ§ar EM OBRAS (30% construÃ­do)
- Garantir 50% vendido antes de finalizar

DECISÃƒO FINAL: GO (oportunidade rara)
```

---

### EXEMPLO 3: Loteamento Alto PadrÃ£o - NO-GO

**Contexto:**

- Terreno: 50.000 mÂ², Zona Rural
- Produto: 80 lotes 600mÂ², R$ 350-450k
- PÃºblico: Faixa A-B (R$ 15.000+)
- Demanda (Passo 6): 45 famÃ­lias

---

**COLETA DE OFERTA:**

**LanÃ§amentos:**

```
Empreendimento 1: CondomÃ­nio Vale Verde
Estoque: 35 lotes (de 60 originais)
Prazo lanÃ§amento: 3 anos
VSO: 25 vendidos em 36 meses = 0,69 un/mÃªs
Status: âŒ ESTOQUE ALTO

Empreendimento 2: Residencial Bosque
Estoque: 18 lotes (de 40 originais)
Prazo lanÃ§amento: 2 anos
VSO: 22 vendidos em 24 meses = 0,92 un/mÃªs
Status: âš ï¸ LENTO

TOTAL ESTOQUE: 53 lotes parados
```

**Oferta Futura:**

```
Processo: 2024/0045
Fase: APROVADO (alvarÃ¡ concedido)
Tipologia: 100 lotes alto padrÃ£o
LocalizaÃ§Ã£o: Mesmo bairro (2 km)
Prazo lanÃ§amento: 3-6 meses
Status: âŒ ALTO RISCO
```

---

**RAZÃƒO DEMANDA:OFERTA:**

```
DEMANDA: 45 famÃ­lias
OFERTA: 
  LanÃ§amentos: 53 lotes
  Futura: 100 lotes
  TOTAL: 153 lotes

RAZÃƒO: 45 Ã· 153 = 0,29:1

âŒ MUITO ABAIXO de 3:1 (MERCADO SATURADO)
```

---

**GATES:**

```
Gate 1: Demanda:Oferta = 0,29:1 âŒ
Gate 2: VSO Concorrentes = 0,69-0,92 âŒ (< 1,0)
Gate 3: Oferta Futura = 100 lotes (125% do nosso) âŒ
Gate 4: IVV = 0,80 vs Mediana 1,46 âŒ

DECISÃƒO: NO-GO (inviÃ¡vel)
```

---

**RECOMENDAÃ‡ÃƒO:**

```
POSICIONAMENTO:
- NÃƒO LANÃ‡AR alto padrÃ£o
- Mercado saturado (53 lotes parados)
- Oferta Futura agrava (mais 100 lotes)
- VSO baixo (< 1 un/mÃªs) indica baixa demanda

ALTERNATIVA:
1. PIVOT para produto diferente:
   - ChÃ¡caras de lazer (maior metragem)
   - Ou aguardar 2-3 anos (absorÃ§Ã£o estoque)

2. VENDER TERRENO:
   - Para construtora com portfÃ³lio
   - Ou para outro tipo de uso

DECISÃƒO FINAL: NO-GO (nÃ£o empreender agora)
```

---

## 10. CHECKLIST DE QUALIDADE

### Definition of Done (DoD) - Passo 7

**Antes de considerar Passo 7 CONCLUÃDO:**

#### Coleta de Dados (6 validaÃ§Ãµes)

- [ ] **3 ofertas** consolidadas e validadas
    - [ ] Pulverizada (portais + limpeza)
    - [ ] LanÃ§amentos (TBC + 3 filtros)
    - [ ] Futura (prefeitura + evidÃªncia)
- [ ] **DeduplicaÃ§Ã£o** realizada
- [ ] **Templates CSV** preenchidos (O7-1 a O7-5)
- [ ] **Mapa QGIS** gerado (Oferta Futura)

#### MÃ©tricas (5 validaÃ§Ãµes)

- [ ] **IVV/VSO** calculados por tipologia
- [ ] **Mediana de mercado** determinada
- [ ] ConcorrÃªncia **comparada Ã  mediana**
- [ ] **Velocidade histÃ³rica** documentada
- [ ] **Benchmark de preÃ§o/mÂ²** por bairro

#### Alinhamento (4 validaÃ§Ãµes)

- [ ] **Tabela 1/2** aplicada (â‰¤12 atributos)
- [ ] Score consolidado por concorrente
- [ ] **Atributos "foda"** (score 2) identificados
- [ ] Gap de mercado (atributos nÃ£o ofertados) mapeado

#### Gates (4 validaÃ§Ãµes)

- [ ] **Gate 1:** RazÃ£o Demanda:Oferta calculada e avaliada
- [ ] **Gate 2:** IVV vs Mediana benchmarkado
- [ ] **Gate 3:** VSO concorrentes analisado
- [ ] **Gate 4:** Risco Oferta Futura mensurado

#### IntegraÃ§Ã£o (4 validaÃ§Ãµes)

- [ ] ComparaÃ§Ã£o ao **PreÃ§o de stand** (Passo 6)
- [ ] **Gaps de mercado** identificados
- [ ] **Posicionamento competitivo** definido
- [ ] Insumos enviados ao **Passo 8** (AbsorÃ§Ã£o)

#### DocumentaÃ§Ã£o (4 validaÃ§Ãµes)

- [ ] **Resumo Executivo P7** (1 pÃ¡gina) concluÃ­do
- [ ] **7 outputs** entregues (CSVs + mapa + resumo)
- [ ] **DecisÃ£o Go/Pivot/No-Go** fundamentada
- [ ] **Premissas documentadas** (rastreabilidade)

**TOTAL: 27 validaÃ§Ãµes**

---

## PRÃ“XIMOS PASSOS

**ApÃ³s concluir Passo 7 (Oferta):**

**â†’ PASSO 8: ABSORÃ‡ÃƒO**

- Input: Demanda potencial + Oferta total
- AÃ§Ã£o: Calcular velocidade de vendas realista
- Output: Unidades/mÃªs (aplicar Fator 4:1)
- FÃ³rmula: AbsorÃ§Ã£o = (Demanda - Oferta) Ã· Prazo Ã— 0,25

**â†’ PASSO 9: CONVALIDAÃ‡ÃƒO**

- Input: Todas premissas (Passos 1-8)
- AÃ§Ã£o: Validar com pesquisa primÃ¡ria
- Output: IntenÃ§Ã£o de compra validada, Gate 4:1

**â†’ PASSO 10: FCD**

- Input: VGV validado (preÃ§o Ã— demanda Ã— absorÃ§Ã£o)
- AÃ§Ã£o: Fluxo de caixa descontado dinÃ¢mico
- Output: ROE, TIR, VPL â†’ DecisÃ£o final GO/NO-GO

---

## PRINCÃPIOS FINAIS

### Lembre-se Sempre:

**1. OFERTA â‰  ANÃšNCIOS ONLINE**

```
Aplicar 3 filtros TBC:
Corretores â†’ Cliente Oculto â†’ Telefone
```

**2. OFERTA FUTURA Ã‰ A MAIS PERIGOSA**

```
Protocolar pedido na Prefeitura SEMPRE
Se negar, Habeas Data via advogado
```

**3. VSO Ã‰ INDICADOR ATRASADO**

```
Ãštil para contexto, NÃƒO para projetar futuro
Usar intenÃ§Ã£o de compra (Passo 9) para projeÃ§Ã£o
```

**4. ALINHAMENTO > INTUIÃ‡ÃƒO**

```
Sistema 1/2 quantifica desejo de pagar
Priorizar atributos score 2 (diferencial)
NÃ£o gastar em score 0 ou 1 (commodity)
```

**5. RAZÃƒO 3:1 MÃNIMA**

```
Demanda:Oferta < 3:1 Ã© PERIGOSO
Indica saturaÃ§Ã£o ou risco alto
```

**6. MEDIANA Ã‰ O BENCHMARK**

```
IVV/VSO sem mediana nÃ£o tem contexto
Sempre comparar com mercado regional
```

### CitaÃ§Ãµes-Guia TIV:

> *"Se vocÃª nÃ£o sabe quem sÃ£o seus concorrentes, vocÃª nÃ£o conhece seu mercado. E se nÃ£o conhece seu mercado, estÃ¡ empreendendo no escuro."*

> *"A Oferta Futura Ã© a mais perigosa porque ela Ã© invisÃ­vel. Quando vocÃª a vÃª, jÃ¡ Ã© tarde demais."*

> *"O mercado nÃ£o liga para o que vocÃª acha importante. Ele sÃ³ paga mais pelo que ELE acha importante."*

> *"Dados > IntuiÃ§Ã£o. Sempre. A metodologia TBC existe porque 'achar' custa caro."*

---

## DOCUMENTAÃ‡ÃƒO TÃ‰CNICA

Este documento Ã© parte integrante da **Metodologia TIV 4.0** e deve ser usado em conjunto com:

- **KB CORE v4.0** (documento mestre)
- **Skill tiv-passo6-demanda** (prÃ©-requisito)
- **Skill tiv-passo8-absorcao** (sequÃªncia)
- **Skill tiv-passo9-convalidacao** (validaÃ§Ã£o)

**VersÃ£o:** 1.0  
**Data:** 31/10/2025  
**Status:** Operacional âœ…  
**Prioridade:** TIER 1 (CrÃ­tico)

---

**FIM DA SKILL - Passo 7 da Metodologia TIV 4.0**
