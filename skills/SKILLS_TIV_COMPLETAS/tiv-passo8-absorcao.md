---
name: "tiv-passo8-absorcao"
version: "1.0"
description: "Quantifica absorÃ§Ã£o mercadolÃ³gica cruzando demanda qualificada (P6) com oferta concorrente (P7), aplicando fatores de conversÃ£o conservadores para determinar velocidade de vendas e viabilidade comercial"
author: "Claude + Othon"
created: "2025-01-12"
updated: "2025-01-12"
tags: ["tiv", "imobiliario", "absorcao", "velocidade-vendas", "fator-4-1", "price-sac", "critico"]
priority: "CRÃTICO"
---

# SKILL TIV - PASSO 8: ABSORÃ‡ÃƒO DE MERCADO

## 1. OBJETIVO E CONTEXTO

### 1.1. DefiniÃ§Ã£o

O **Passo 8 - AbsorÃ§Ã£o de Mercado** Ã© o ponto de encontro entre demanda qualificada (Passo 6) e oferta concorrente (Passo 7), onde se quantifica matematicamente a **capacidade do mercado em absorver o produto** proposto.

**Pergunta Central:**
> **"A demanda Ã© maior que a oferta?"**

### 1.2. Por Que Este Passo Ã© CrÃ­tico

- **Valida viabilidade comercial** antes do investimento tÃ©cnico/financeiro
- **Evita projetos em mercados saturados** (absorÃ§Ã£o negativa = red flag)
- **Define velocidade de vendas realista** (base para FCD do Passo 10)
- **Calibra preÃ§o e mix de produtos** de acordo com capacidade real do mercado
- **Gera gates de decisÃ£o objetivos** (Go/Hold/No-Go)

### 1.3. PosiÃ§Ã£o na Metodologia TIV

```
PASSO 6 â†’ Demanda Qualificada + PreÃ§o ViÃ¡vel (Price/SAC)
         â†“
PASSO 7 â†’ Oferta Total (Pulverizada + LanÃ§amentos + TBC)
         â†“
PASSO 8 â†’ ABSORÃ‡ÃƒO (Demanda Ã· Fator - Oferta) â† VOCÃŠ ESTÃ AQUI
         â†“
PASSO 9 â†’ ConvalidaÃ§Ã£o (Validar premissas com pesquisa)
         â†“
PASSO 10 â†’ FCD (Viabilidade financeira final)
```

---

## 2. QUANDO ACIONAR

### 2.1. Triggers ObrigatÃ³rios

âœ… **Acione IMEDIATAMENTE quando:**
- UsuÃ¡rio mencionar "absorÃ§Ã£o", "velocidade de vendas", "capacidade do mercado"
- Passos 6 (Demanda) E 7 (Oferta) estiverem concluÃ­dos
- Perguntar "quantas unidades o mercado absorve?"
- Questionar sobre "Fator 4:1" ou "Fator 10:1"
- Solicitar "cÃ¡lculo de absorÃ§Ã£o por faixa de preÃ§o"
- Pedir "anÃ¡lise de saturaÃ§Ã£o de mercado"
- Mencionar "Demanda vs Oferta"

### 2.2. PrÃ©-Requisitos ObrigatÃ³rios

**ANTES de executar Passo 8, confirme:**

- [ ] **Passo 6 concluÃ­do:** Demanda pagante quantificada + PreÃ§o Price/SAC
- [ ] **Passo 7 concluÃ­do:** Oferta Total (pulverizada + lanÃ§amentos + TBC)
- [ ] **DefiniÃ§Ã£o de Fator:** 4:1 (com validaÃ§Ã£o) OU 10:1 (sem validaÃ§Ã£o)
- [ ] **SegmentaÃ§Ã£o clara:** Por faixa de preÃ§o E/OU subÃ¡rea H3

---

## 3. FRAMEWORK METODOLÃ“GICO

### 3.1. Conceito de AbsorÃ§Ã£o

**AbsorÃ§Ã£o** Ã© o **excedente (ou dÃ©ficit) de demanda** apÃ³s considerar:
1. **Demanda potencial** (populaÃ§Ã£o com capacidade de compra)
2. **Fator de conversÃ£o** (% que de fato se tornarÃ¡ comprador)
3. **Oferta concorrente** (unidades competindo pelo mesmo pÃºblico)

**FÃ³rmula-nÃºcleo:**
```
AbsorÃ§Ã£o = (Demanda Bruta Ã· Fator de ConversÃ£o) - Oferta Total
```

**InterpretaÃ§Ã£o:**
- **Positivo (+):** Janela de oportunidade (demanda > oferta)
- **Negativo (-):** SaturaÃ§Ã£o (oferta > demanda)
- **Zero (0):** EquilÃ­brio (mercado no limite)

### 3.2. Dois Pilares de Demanda

A anÃ¡lise de absorÃ§Ã£o deve considerar **dois cenÃ¡rios distintos** de demanda:

#### **PILAR 1: DÃ©ficit ImobiliÃ¡rio (Demanda Fim)**
**Perfil:**
- FamÃ­lias que **moram de aluguel** ou em **domicÃ­lio cedido**
- **Necessidade imediata** por moradia prÃ³pria
- **Menor sensibilidade a preÃ§o** (urgÃªncia > preÃ§o)

**CaracterÃ­sticas:**
- Volume menor, mas demanda **mais qualificada**
- **ConversÃ£o mais rÃ¡pida** (prazo â‰¤12 meses)
- **Base do cÃ¡lculo conservador**

#### **PILAR 2: Demanda PLUS (DÃ©ficit + Upgrade + Investimento)**
**Perfil:**
- **DÃ©ficit ImobiliÃ¡rio** (pilar 1)
- **+ FamÃ­lias com domicÃ­lio prÃ³prio quitado** buscando:
  - Upgrade (melhor localizaÃ§Ã£o/padrÃ£o)
  - Investimento patrimonial
  - DiversificaÃ§Ã£o de portfÃ³lio

**CaracterÃ­sticas:**
- Volume maior (geralmente 2-3x o dÃ©ficit)
- **ConversÃ£o mais lenta** (prazo atÃ© 24 meses)
- **Maior sensibilidade a preÃ§o e atributos**

### 3.3. Fatores de AbsorÃ§Ã£o (ConversÃ£o)

O **Fator de AbsorÃ§Ã£o** Ã© a taxa de conversÃ£o entre demanda potencial e vendas efetivas.

| Fator | ConversÃ£o | CenÃ¡rio de Uso | Quando Aplicar |
|:-----:|:---------:|:---------------|:---------------|
| **10:1** | **10%** | **SEM validaÃ§Ã£o** de intenÃ§Ã£o de compra | Estudos quantitativos puros (IBGE/FGV). Para cada 10 potenciais compradores com perfil, apenas 1 compra. **PadrÃ£o inicial conservador.** |
| **4:1** | **25%** | **COM validaÃ§Ã£o** de intenÃ§Ã£o de compra | Pesquisa primÃ¡ria comprova desejo de aquisiÃ§Ã£o. Para cada 4 pessoas que declaram interesse, 1 compra. **PadrÃ£o TIV pÃ³s-validaÃ§Ã£o (Passo 9).** |
| **3:1** | **33%** | **AvanÃ§ado:** Cadastros qualificados + produto Ãºnico | LanÃ§adores renomados com CRM robusto. Produto diferenciado, localizaÃ§Ã£o privilegiada. **Exige histÃ³rico comprovado.** |
| **2:1** | **50%** | **Excepcional:** Escassez extrema | MonopÃ³lio geogrÃ¡fico, demanda reprimida. **Raramente aplicÃ¡vel, alto risco.** |

**âš ï¸ REGRA TIV INVIOLÃVEL:**
- **Default: 10:1** (sem pesquisa validada)
- **ApÃ³s Passo 9: 4:1** (com pesquisa validando intenÃ§Ã£o)
- **Nunca assumir 4:1 sem evidÃªncia robusta** (superestima absorÃ§Ã£o)

**Limite de Risco:**
```
IDEAL:     RazÃ£o D:O â‰¥ 4:1 (com validaÃ§Ã£o) ou â‰¥ 10:1 (sem validaÃ§Ã£o)
ATENÃ‡ÃƒO:   RazÃ£o D:O entre 3:1 e 4:1 (exige justificativa)
PERIGOSO:  RazÃ£o D:O < 3:1 (NO-GO ou REVISAR produto)
```

### 3.4. PreÃ§o MÃ¡ximo SuportÃ¡vel (do Passo 6)

A anÃ¡lise de absorÃ§Ã£o **depende do preÃ§o definido** no Passo 6, calculado via:

#### **MÃ©todo: CÃ¡lculo ao ContrÃ¡rio (Atingir Meta)**

**INPUTS (Passo 6):**
1. **Renda Bruta Familiar** por classe (A1 a C2)
2. **Capacidade de Endividamento:**
   - **Vertical:** 30% da renda
   - **Loteamento:** 12-26% (varia por classe)
3. **Plano de Pagamento:**
   - Entrada (%)
   - Prazo financiamento (meses)
   - Taxa de juros (% a.m.)

**PROCESSAMENTO:**
```
Parcela MÃ¡xima = Renda Bruta Ã— % Endividamento
       â†“ (cÃ¡lculo inverso Price ou SAC)
Valor FinanciÃ¡vel (VP)
       â†“
PreÃ§o MÃ¡ximo = VP Ã· (1 - % Entrada)
```

**OUTPUTS (alimentam Passo 8):**
- **PreÃ§o mÃ¡ximo absorvÃ­vel (Price):** Parcelas fixas, VGV maior
- **PreÃ§o mÃ¡ximo absorvÃ­vel (SAC):** Parcelas decrescentes, juros menores
- **Faixa de preÃ§o por classe:** Para segmentar absorÃ§Ã£o

**Exemplo:**
```
CLASSE B2: Renda R$ 6.000
Endividamento vertical: 30%
Parcela mÃ¡xima: R$ 1.800

PRICE (420 meses, 10% a.a., entrada 40%):
VP financiÃ¡vel: R$ 205.000
PreÃ§o mÃ¡ximo: R$ 205.000 Ã· 0,60 = R$ 342.000

SAC (mesmas condiÃ§Ãµes):
PreÃ§o mÃ¡ximo: R$ 298.000 (juros menores, mas prestaÃ§Ã£o inicial maior)

â†’ AbsorÃ§Ã£o B2 considera faixa R$ 298k - R$ 342k
```

---

## 4. INPUTS NECESSÃRIOS

### 4.1. Do Passo 6 (Demanda)

**Arquivo esperado:** `O6-5_Resumo_Executivo_P6.md`

**Dados obrigatÃ³rios:**
- [ ] **Demanda pagante total** (nÂº de famÃ­lias por faixa/classe)
- [ ] **PreÃ§o de stand validado** (Price E SAC por faixa)
- [ ] **SegmentaÃ§Ã£o geogrÃ¡fica** (demanda por subÃ¡rea H3, se aplicÃ¡vel)
- [ ] **PÃºblico-alvo detalhado** (4 dimensÃµes: demogrÃ¡fico, socioeconÃ´mico, geogrÃ¡fico, comportamental)
- [ ] **% IntenÃ§Ã£o de compra** (se houver pesquisa prÃ©via)

**Exemplo de dados:**
```csv
classe,renda_media,domicilios,preco_price,preco_sac,percentual_intencao
A1,R$ 25000,4041,R$ 1413752,R$ 1210000,8%
A2,R$ 18000,4277,R$ 655342,R$ 580000,12%
B1,R$ 11000,9158,R$ 387147,R$ 342000,18%
B2,R$ 6000,10340,R$ 211662,R$ 187000,25%
C1,R$ 3500,8729,R$ 170996,R$ 151000,20%
C2,R$ 2200,3689,R$ 128368,R$ 113000,15%
```

### 4.2. Do Passo 7 (Oferta)

**Arquivo esperado:** `O7-X_Resumo_Oferta.md`

**Dados obrigatÃ³rios:**
- [ ] **Oferta Pulverizada** (unidades usadas, baixa relevÃ¢ncia)
- [ ] **Oferta LanÃ§amentos** (unidades novas competindo diretamente) â­ CRÃTICO
- [ ] **Oferta TBC** (Building Capacity - pipeline aprovado/em anÃ¡lise)
- [ ] **Oferta Total por faixa de preÃ§o** (soma das 3 tipologias)
- [ ] **VSO mÃ©dio do mercado** (Velocidade SaÃ­da Oferta, unidades/mÃªs)

**Exemplo de dados:**
```csv
tipologia,faixa_preco,unidades,vso_medio
Pulverizada,R$ 300-400k,856,0.8
LanÃ§amentos,R$ 300-400k,425,3.2
TBC (futura),R$ 300-400k,180,--
TOTAL,R$ 300-400k,1461,--
```

### 4.3. DefiniÃ§Ãµes do Projeto

**Produto proposto:**
- [ ] Quantidade de unidades (total e por fase)
- [ ] Tipologia (horizontal/vertical, metragem, padrÃ£o)
- [ ] PreÃ§o-alvo (unitÃ¡rio e VGV)
- [ ] Faseamento (se houver)

**Fator de conversÃ£o:**
- [ ] **10:1** (default sem validaÃ§Ã£o) OU
- [ ] **4:1** (se Passo 9 jÃ¡ validou intenÃ§Ã£o) OU
- [ ] **Outro** (justificar com histÃ³rico comprovado)

---

## 5. PROCESSO DE ANÃLISE

### 5.1. Passo a Passo Operacional

#### **ETAPA 1: PreparaÃ§Ã£o dos Dados**

1. **Importar demanda do Passo 6:**
   ```python
   # Dados por classe/faixa
   demanda = {
       'B2': {'domicilios': 10340, 'preco_price': 211662, 'preco_sac': 187000},
       'C1': {'domicilios': 8729, 'preco_price': 170996, 'preco_sac': 151000}
   }
   ```

2. **Importar oferta do Passo 7:**
   ```python
   oferta_total = {
       'R$ 180k-220k': 259,  # Compete com B2
       'R$ 150k-180k': 67    # Compete com C1
   }
   ```

3. **Definir cenÃ¡rios de demanda:**
   - **DÃ©ficit:** Apenas famÃ­lias sem imÃ³vel prÃ³prio
   - **PLUS:** DÃ©ficit + proprietÃ¡rios buscando upgrade

4. **Definir fator de conversÃ£o:**
   - Sem pesquisa: **10:1**
   - Com validaÃ§Ã£o (Passo 9): **4:1**

#### **ETAPA 2: CÃ¡lculo de AbsorÃ§Ã£o por Faixa**

**FÃ³rmula aplicada:**
```
Para cada faixa de preÃ§o:

AbsorÃ§Ã£o = (Demanda Bruta Ã· Fator) - Oferta Total

Onde:
- Demanda Bruta = nÂº domicÃ­lios com capacidade de compra na faixa
- Fator = 10 (sem validaÃ§Ã£o) ou 4 (com validaÃ§Ã£o)
- Oferta Total = LanÃ§amentos + TBC (ignorar pulverizada)
```

**Exemplo prÃ¡tico (Faixa B2, Fator 10:1, DÃ©ficit):**
```
Demanda Bruta: 10.340 domicÃ­lios
Fator: 10
Oferta Total: 259 unidades

CÃ¡lculo:
Demanda Ajustada = 10.340 Ã· 10 = 1.034 unidades
AbsorÃ§Ã£o = 1.034 - 259 = +775 unidades

INTERPRETAÃ‡ÃƒO: âœ… Janela de oportunidade (absorÃ§Ã£o positiva)
```

**Exemplo prÃ¡tico (Faixa A1, Fator 10:1, DÃ©ficit):**
```
Demanda Bruta: 4.041 domicÃ­lios
Fator: 10
Oferta Total: 5.715 unidades

CÃ¡lculo:
Demanda Ajustada = 4.041 Ã· 10 = 404 unidades
AbsorÃ§Ã£o = 404 - 5.715 = -5.311 unidades

INTERPRETAÃ‡ÃƒO: âŒ SaturaÃ§Ã£o severa (mercado alto padrÃ£o travado)
```

#### **ETAPA 3: AnÃ¡lise por SubÃ¡rea H3 (se aplicÃ¡vel)**

Se o Passo 6 segmentou demanda por H3 (hexÃ¡gonos geogrÃ¡ficos):

```python
# Exemplo: absorÃ§Ã£o por subÃ¡rea
absorÃ§Ã£o_h3 = []

for h3_id in subareas:
    demanda_h3 = demanda_por_h3[h3_id]
    oferta_h3 = oferta_por_h3.get(h3_id, 0)  # Se nÃ£o houver oferta, = 0
    
    abs_h3 = (demanda_h3 / fator) - oferta_h3
    
    status = 'positivo' if abs_h3 > 0 else 'negativo' if abs_h3 < 0 else 'neutro'
    
    absorÃ§Ã£o_h3.append({
        'h3_id': h3_id,
        'demanda_ajustada': demanda_h3 / fator,
        'oferta': oferta_h3,
        'absorÃ§Ã£o': abs_h3,
        'status': status
    })
```

**Output esperado:**
```csv
h3_id,h3_nome,demanda_ajustada,oferta,absorcao,status
89a8a0644ffffff,Centro,125,42,+83,positivo
89a8a0645ffffff,Zona Sul,98,156,-58,negativo
89a8a0646ffffff,Zona Norte,142,0,+142,positivo
```

#### **ETAPA 4: CenÃ¡rios (Baseline, Conservador, Otimista)**

Para **cada faixa/subÃ¡rea**, rodar 3 cenÃ¡rios:

| CenÃ¡rio | Demanda | Sistema PreÃ§o | Fator | Oferta |
|:--------|:--------|:--------------|:------|:-------|
| **Baseline** | DÃ©ficit | Price | 10:1 | LanÃ§amentos + TBC |
| **Conservador** | DÃ©ficit | SAC | 10:1 | LanÃ§amentos + TBC + 20% pipeline |
| **Otimista** | PLUS | Price | 4:1 (se validado) | LanÃ§amentos apenas |

**Exemplo de tabela de cenÃ¡rios:**
```csv
cenario,faixa,demanda_tipo,sistema,fator,oferta,absorcao,status
Baseline,B2,Defici,Price,10,259,+775,positivo
Conservador,B2,Deficit,SAC,10,311,-77,negativo
Otimista,B2,PLUS,Price,4,259,+7821,positivo
```

#### **ETAPA 5: Velocidade de Vendas Projetada**

Com absorÃ§Ã£o positiva, estimar **unidades/mÃªs**:

**MÃ©todo 1: RazÃ£o Demanda:Oferta**
```
Se AbsorÃ§Ã£o = +775 unidades (B2)
Produto proposto = 180 unidades
Prazo total do projeto = 24 meses

Velocidade projetada = 180 Ã· 24 = 7,5 un/mÃªs

VALIDAÃ‡ÃƒO:
RazÃ£o D:O = (10.340 Ã· 10) Ã· 180 = 5,7:1
Status: âœ… Acima de 4:1 (seguro com validaÃ§Ã£o)
```

**MÃ©todo 2: Benchmarking com VSO**
```
VSO mÃ©dio mercado (Passo 7) = 3,2 un/mÃªs
Ajuste conservador TIV = 80% do VSO

Velocidade conservadora = 3,2 Ã— 0,80 = 2,6 un/mÃªs
Prazo venda = 180 Ã· 2,6 = 69 meses âš ï¸ (muito longo)

DECISÃƒO: Reduzir lote inicial ou acelerar marketing
```

**MÃ©todo 3: Curva de AbsorÃ§Ã£o (rampa + pico + desaceleraÃ§Ã£o)**
```
Fase 1 (meses 1-6):   Rampa    â†’ 3 un/mÃªs Ã— 6 = 18 un
Fase 2 (meses 7-18):  Pico     â†’ 8 un/mÃªs Ã— 12 = 96 un
Fase 3 (meses 19-24): Desacel  â†’ 4 un/mÃªs Ã— 6 = 24 un
                                          TOTAL: 138 un (de 180)

Saldo 42 unidades â†’ ajustar preÃ§o ou mudar estratÃ©gia
```

---

## 6. OUTPUTS ESPERADOS

### 6.1. Estrutura de EntregÃ¡veis

O Passo 8 deve gerar **5 arquivos principais**:

#### **O8-1_Absorcao_por_faixa.csv**
**Template:**
```csv
cenario,demanda_tipo,classe,faixa_preco,capacidade_end,domicilios,preco_maximo,entrada_pct,prazo_meses,oferta_total,fator,demanda_ajustada,absorcao,status,razao_d_o
Baseline,Deficit,B2,R$ 180-220k,30%,10340,211662,40%,420,259,10,1034,+775,positivo,5.74
Baseline,Deficit,C1,R$ 150-180k,30%,8729,170996,30%,360,67,10,873,+806,positivo,13.03
Conservador,Deficit,B2,R$ 180-220k,30%,10340,187000,40%,420,311,10,1034,-77,negativo,3.32
Otimista,PLUS,B2,R$ 180-220k,30%,32387,211662,40%,420,259,4,8097,+7838,positivo,31.24
```

**Colunas obrigatÃ³rias:**
- cenario, demanda_tipo, classe, faixa_preco
- domicilios, preco_maximo (Price ou SAC)
- oferta_total, fator, demanda_ajustada
- **absorcao** (valor chave), status (positivo/negativo/neutro)
- razao_d_o (Demanda:Oferta)

#### **O8-2_Absorcao_por_subarea_H3.csv**
**Template (se houver segmentaÃ§Ã£o H3):**
```csv
cenario,h3_id,h3_nome,latitude,longitude,demanda_ajustada,oferta,absorcao,status,produto_recomendado
Baseline,89a8a0644ffffff,Centro,-21.5321,-42.6432,125,42,+83,positivo,Vertical mÃ©dio
Baseline,89a8a0645ffffff,Zona Sul,-21.5498,-42.6201,98,156,-58,negativo,Evitar
Baseline,89a8a0646ffffff,Zona Norte,-21.5187,-42.6589,142,0,+142,positivo,Loteamento popular
```

**Uso:** Mapear geograficamente onde hÃ¡ oportunidade vs saturaÃ§Ã£o.

#### **O8-3_Simulador_Absorcao.xlsx**
**Excel com 2 abas:**

**Aba 1: CenÃ¡rios**
- Inputs: demanda, fator, oferta (editÃ¡veis)
- FÃ³rmulas: demanda_ajustada, absorÃ§Ã£o, razÃ£o D:O
- SemÃ¡foro: verde (positivo), amarelo (neutro), vermelho (negativo)

**Aba 2: Resumo**
- Conta positivos/negativos por cenÃ¡rio
- Identifica gates (â‰¥ 4:1 ou < 3:1)
- RecomendaÃ§Ã£o final (GO/HOLD/NO-GO)

**Exemplo de layout:**
```
[Aba CenÃ¡rios]
CenÃ¡rio | Faixa | Demanda | Fator | Oferta | Abs. Ajust | AbsorÃ§Ã£o | Status | Gate
--------|-------|---------|-------|--------|------------|----------|--------|------
Base    | B2    | 10340   | 10    | 259    | 1034       | +775     | âœ…     | 5.7:1
Base    | C1    | 8729    | 10    | 67     | 873        | +806     | âœ…     | 13:1
Conserv | B2    | 10340   | 10    | 311    | 1034       | -77      | âŒ     | 3.3:1

[Aba Resumo]
CenÃ¡rio      | Positivos | Negativos | Gate â‰¥4:1 | DecisÃ£o
-------------|-----------|-----------|-----------|----------
Baseline     | 4/6       | 2/6       | 67%       | GO
Conservador  | 2/6       | 4/6       | 33%       | HOLD
Otimista     | 6/6       | 0/6       | 100%      | GO
```

#### **O8-4_Mapa_Absorcao_H3.qgz**
**Projeto QGIS (se houver H3):**

**Camadas:**
1. **HexÃ¡gonos H3** com simbologia:
   - Verde: absorÃ§Ã£o positiva (>+50 un)
   - Amarelo: equilÃ­brio (-50 a +50 un)
   - Vermelho: saturaÃ§Ã£o (<-50 un)

2. **RÃ³tulos:** `h3_nome â€” absorÃ§Ã£o`
   - Exemplo: "Centro â€” +83"

3. **Tabela de atributos:** Vincular O8-2_Absorcao_por_subarea_H3.csv

4. **Layout A3:** (opcional)
   - Legenda
   - Tabela resumo por cenÃ¡rio
   - Escala e norte

#### **O8-5_Resumo_Executivo_P8.md**
**RelatÃ³rio executivo de 1-2 pÃ¡ginas:**

**Estrutura obrigatÃ³ria:**
```markdown
# RESUMO EXECUTIVO - PASSO 8 (ABSORÃ‡ÃƒO)

## 1. IDENTIFICAÃ‡ÃƒO
- Projeto: [nome]
- MunicÃ­pio: [cidade-UF]
- Data: [dd/mm/aaaa]
- ResponsÃ¡vel: [nome]

## 2. RESULTADO PRINCIPAL
**AbsorÃ§Ã£o Status:**
- Baseline: [positivo/negativo] â€” [valor]
- Conservador: [positivo/negativo] â€” [valor]
- Otimista: [positivo/negativo] â€” [valor]

**Gate Check:**
- RazÃ£o Demanda:Oferta: [X:1]
- Status Gate: âœ… â‰¥4:1 | âš ï¸ 3-4:1 | âŒ <3:1

## 3. PREMISSAS UTILIZADAS
- Demanda: [DÃ©ficit/PLUS] â€” [nÂº domicÃ­lios]
- PreÃ§o: [Price/SAC] â€” R$ [valor]
- Fator: [10:1 ou 4:1] â€” [com/sem validaÃ§Ã£o]
- Oferta: [nÂº unidades] (LanÃ§amentos + TBC)

## 4. ANÃLISE POR FAIXA
| Faixa | Demanda Ajust | Oferta | AbsorÃ§Ã£o | Status |
|-------|---------------|--------|----------|--------|
| A1    | 404           | 5.715  | -5.311   | âŒ     |
| B2    | 1.034         | 259    | +775     | âœ…     |
| C1    | 873           | 67     | +806     | âœ…     |

## 5. VELOCIDADE PROJETADA
- Unidades/mÃªs (projeÃ§Ã£o): [valor] un/mÃªs
- VSO mercado (benchmark): [valor] un/mÃªs
- Prazo venda estimado: [valor] meses

## 6. GATES DE DECISÃƒO
**GO se:**
- [ ] AbsorÃ§Ã£o â‰¥ 0 em â‰¥2 cenÃ¡rios
- [ ] RazÃ£o D:O â‰¥ 4:1 (validado) ou â‰¥10:1 (nÃ£o validado)

**HOLD/AJUSTAR se:**
- [ ] AbsorÃ§Ã£o levemente negativa (>-10% oferta)
- [ ] RazÃ£o D:O entre 3:1 e 4:1 (limite)
â†’ Ajustar: preÃ§o, mix ou praÃ§a

**NO-GO se:**
- [ ] AbsorÃ§Ã£o â‰ª 0 em todos cenÃ¡rios
- [ ] RazÃ£o D:O < 3:1 (perigoso)

## 7. RISCOS IDENTIFICADOS
1. [DescriÃ§Ã£o do risco 1]
2. [DescriÃ§Ã£o do risco 2]
3. [DescriÃ§Ã£o do risco 3]

## 8. RECOMENDAÃ‡Ã•ES ESTRATÃ‰GICAS
- **PreÃ§o:** [manter/ajustar para R$ X]
- **Mix:** [manter/priorizar faixa Y]
- **PraÃ§a:** [focar subÃ¡rea H3 Z]
- **PromoÃ§Ã£o:** [timing de lanÃ§amento T]

## 9. DECISÃƒO FINAL
[  ] GO â€” AbsorÃ§Ã£o positiva, gates aprovados
[  ] HOLD â€” Ajustes necessÃ¡rios antes de prosseguir
[  ] NO-GO â€” Mercado saturado, inviÃ¡vel comercialmente

## 10. PRÃ“XIMOS PASSOS
â†’ Passo 9: Validar premissas com pesquisa primÃ¡ria
â†’ Passo 10: FCD com velocidade validada

---
**Anexos:**
- O8-1_Absorcao_por_faixa.csv
- O8-2_Absorcao_por_subarea_H3.csv
- O8-3_Simulador_Absorcao.xlsx
- O8-4_Mapa_Absorcao_H3.qgz

**Metadados:**
- VersÃ£o TIV: 4.0
- Autor: [nome]
- Revisado: [nome] em [data]
```

---

## 7. ALERTAS E VALIDAÃ‡Ã•ES

### 7.1. Red Flags CrÃ­ticos

âŒ **NUNCA faÃ§a:**
1. **Aplicar Fator 4:1 sem validaÃ§Ã£o** (superestima absorÃ§Ã£o)
   - Sem pesquisa primÃ¡ria = obrigatÃ³rio 10:1
   
2. **Ignorar Oferta TBC (Building Capacity)**
   - Terrenos com potencial construtivo = concorrÃªncia futura
   
3. **Misturar faixas de preÃ§o distintas** na mesma conta
   - B2 (R$ 200k) vs A2 (R$ 600k) = pÃºblicos diferentes
   
4. **Considerar Oferta Pulverizada como concorrente direto**
   - Usados competem fracamente com novos
   
5. **Assumir absorÃ§Ã£o linear** (unidades/mÃªs constante)
   - Curva real: rampa â†’ pico â†’ desaceleraÃ§Ã£o
   
6. **Usar Price quando pÃºblico exige SAC**
   - Classes C1/C2: sensibilidade a juros > VGV
   
7. **Desconsiderar cenÃ¡rios** (fazer apenas Baseline)
   - Conservador testa robustez do projeto

### 7.2. ValidaÃ§Ãµes ObrigatÃ³rias (DoD)

**ANTES de considerar Passo 8 CONCLUÃDO:**

#### **Dados de Entrada (4 itens)**
- [ ] Demanda Passo 6 importada (domicÃ­lios + preÃ§o Price/SAC)
- [ ] Oferta Passo 7 importada (lanÃ§amentos + TBC por faixa)
- [ ] Fator de conversÃ£o definido (10:1 default, 4:1 se validado)
- [ ] Produto proposto especificado (unidades, tipologia, preÃ§o)

#### **CenÃ¡rios Rodados (3 itens)**
- [ ] Baseline: DÃ©ficit + Price + Fator 10:1
- [ ] Conservador: DÃ©ficit + SAC + Oferta aumentada
- [ ] Otimista: PLUS + Price + Fator 4:1 (se validado)

#### **CÃ¡lculos Executados (5 itens)**
- [ ] AbsorÃ§Ã£o por faixa calculada (â‰¥3 faixas)
- [ ] AbsorÃ§Ã£o por H3 calculada (se aplicÃ¡vel)
- [ ] RazÃ£o Demanda:Oferta verificada (â‰¥4:1 ideal)
- [ ] Velocidade projetada estimada (unidades/mÃªs)
- [ ] Gates de decisÃ£o avaliados (GO/HOLD/NO-GO)

#### **Outputs Gerados (5 itens)**
- [ ] O8-1_Absorcao_por_faixa.csv criado
- [ ] O8-2_Absorcao_por_subarea_H3.csv criado (se H3)
- [ ] O8-3_Simulador_Absorcao.xlsx criado
- [ ] O8-4_Mapa_Absorcao_H3.qgz criado (se H3)
- [ ] O8-5_Resumo_Executivo_P8.md criado

#### **AnÃ¡lise CrÃ­tica (4 itens)**
- [ ] Sinal de absorÃ§Ã£o interpretado (positivo/negativo)
- [ ] Magnitude de absorÃ§Ã£o analisada (>+50 un = robusto)
- [ ] Riscos de saturaÃ§Ã£o identificados (se negativo)
- [ ] Ajustes recomendados (preÃ§o, mix, praÃ§a, timing)

#### **Rastreabilidade (3 itens)**
- [ ] Premissas documentadas (taxa, prazo, entrada)
- [ ] Fontes registradas (Passos 6-7, data-base)
- [ ] Changelog atualizado (versÃ£o, autor, data)

**TOTAL: 24 validaÃ§Ãµes obrigatÃ³rias**

### 7.3. Erros Comuns a Evitar

**ERRO 1: Confundir demanda potencial com demanda ajustada**
```
âŒ ERRADO:
Demanda = 10.000 domicÃ­lios
AbsorÃ§Ã£o = 10.000 - 300 = +9.700 âœ… (irreal)

âœ… CORRETO:
Demanda = 10.000 domicÃ­lios
Fator 10:1 â†’ Demanda Ajustada = 1.000
AbsorÃ§Ã£o = 1.000 - 300 = +700 âœ… (realista)
```

**ERRO 2: NÃ£o segmentar por faixa de preÃ§o**
```
âŒ ERRADO:
Demanda Total = 30.000 domicÃ­lios (todas classes)
Oferta Total = 6.000 unidades (todas faixas)
AbsorÃ§Ã£o = 3.000 - 6.000 = -3.000 âŒ

Problema: Classe C (R$ 150k) nÃ£o compete com Classe A (R$ 800k)

âœ… CORRETO:
Analisar por faixa:
- R$ 150-200k: AbsorÃ§Ã£o = +800
- R$ 300-400k: AbsorÃ§Ã£o = +150
- R$ 600-800k: AbsorÃ§Ã£o = -200
```

**ERRO 3: Ignorar oferta futura (TBC)**
```
âŒ ERRADO:
Oferta = 300 (apenas lanÃ§amentos atuais)

âœ… CORRETO:
Oferta = 300 (lanÃ§amentos) + 150 (TBC aprovados) = 450
```

**ERRO 4: Assumir velocidade constante**
```
âŒ ERRADO:
Velocidade = 5 un/mÃªs Ã— 24 meses = 120 un

âœ… CORRETO:
Meses 1-6:  3 un/mÃªs (rampa)
Meses 7-18: 8 un/mÃªs (pico)
Meses 19-24: 4 un/mÃªs (desaceleraÃ§Ã£o)
Total: 18 + 96 + 24 = 138 un (mais realista)
```

---

## 8. INTEGRAÃ‡ÃƒO COM OUTRAS SKILLS

### 8.1. Skills Fornecedoras (Inputs)

#### **tiv-passo6-demanda**
**O que consome:**
- Demanda pagante quantificada (domicÃ­lios por faixa/H3)
- PreÃ§o mÃ¡ximo absorvÃ­vel (Price E SAC)
- SegmentaÃ§Ã£o 4D (demogrÃ¡fico, socioeconÃ´mico, geogrÃ¡fico, comportamental)
- % IntenÃ§Ã£o de compra (se houver pesquisa prÃ©via)

**Como usar:**
```
PASSO 6 fornece:
Classe B2: 10.340 domicÃ­lios
PreÃ§o Price: R$ 211.662
PreÃ§o SAC: R$ 187.000

PASSO 8 usa:
â†’ Baseline: PreÃ§o Price + Fator 10:1
â†’ Conservador: PreÃ§o SAC + Fator 10:1
â†’ Validar: RazÃ£o D:O para aprovar produto
```

#### **tiv-passo7-oferta**
**O que consome:**
- Oferta Total por faixa (LanÃ§amentos + TBC)
- VSO mÃ©dio do mercado (velocidade histÃ³rica)
- Gaps de mercado identificados
- Concorrentes diretos (produto, preÃ§o, localizaÃ§Ã£o)

**Como usar:**
```
PASSO 7 fornece:
Faixa R$ 180-220k: 259 unidades (oferta total)
VSO mÃ©dio: 3,2 un/mÃªs

PASSO 8 usa:
â†’ Oferta Total como denominador de absorÃ§Ã£o
â†’ VSO como benchmark de velocidade
â†’ Identificar faixas saturadas (Abs. negativa)
```

#### **tiv-passo5-legal-restricoes**
**O que consome:**
- Capacidade construtiva validada (CA, TO, gabarito)
- RestriÃ§Ãµes que afetam produto (metragem, vagas, Ã¡reas non aedificandi)

**Como usar:**
- Produto proposto deve respeitar limites legais
- Se restriÃ§Ã£o reduzir unidades, recalcular absorÃ§Ã£o

### 8.2. Skills Consumidoras (Outputs)

#### **tiv-passo9-convalidacao**
**O que fornece:**
- AbsorÃ§Ã£o preliminar (Fator 10:1) â†’ Passo 9 valida com pesquisa
- Premissas a serem testadas (% intenÃ§Ã£o, sensibilidade preÃ§o)
- Base para dimensionar amostra de pesquisa

**Como usa:**
```
PASSO 8 indica:
AbsorÃ§Ã£o B2 = +775 (Fator 10:1)
RazÃ£o D:O = 5,7:1

PASSO 9 valida:
Pesquisa primÃ¡ria comprova:
- % IntenÃ§Ã£o real: 28% (vs 10% assumido)
- Gate 4:1: 5,7 â†’ 14,3 (2,5x melhor!)
â†’ AbsorÃ§Ã£o passa para Fator 4:1 (mais robusta)
```

#### **tiv-passo10-fcd**
**O que fornece:**
- Velocidade de vendas (unidades/mÃªs) â†’ input cronograma FCD
- AbsorÃ§Ã£o positiva = GO/HOLD/NO-GO comercial
- PreÃ§o validado (Price ou SAC) â†’ input VGV

**Como usa:**
```
PASSO 8 confirma:
Velocidade: 6,5 un/mÃªs (curva realista)
Prazo venda: 28 meses (180 un Ã· 6,5)

PASSO 10 usa:
â†’ Modelar receita mÃªs a mÃªs (cronograma vendas)
â†’ Calcular ROE considerando velocidade real
â†’ DecisÃ£o GO/NO-GO fundamentada em absorÃ§Ã£o
```

#### **tiv-pith (RelatÃ³rio Final)**
**O que fornece:**
- SeÃ§Ã£o "AbsorÃ§Ã£o de Mercado" com gates validados
- ComprovaÃ§Ã£o de viabilidade comercial (nÃ£o sÃ³ financeira)
- GrÃ¡ficos de absorÃ§Ã£o por faixa/H3

**Como usa:**
- Apresentar para investidores/bancos/sÃ³cios
- Defender viabilidade com dados de mercado
- Justificar preÃ§o e mix de produtos

---

## 9. EXEMPLOS DE USO

### 9.1. Caso Real: Loteamento Popular - Leopoldina-MG

**CONTEXTO:**
- Terreno: 22.000 mÂ² (ZEU - Zona de ExpansÃ£o Urbana)
- Produto proposto: 35 lotes de 250 mÂ² cada
- PreÃ§o-alvo: R$ 140.000/lote
- MunicÃ­pio: Leopoldina-MG (52.000 habitantes)

**DADOS DO PASSO 6 (Demanda):**
```
Classe C1 (Faixa R$ 130-170k):
- DomicÃ­lios Ã¡rea de influÃªncia: 8.729
- PreÃ§o mÃ¡ximo Price: R$ 170.996
- PreÃ§o mÃ¡ximo SAC: R$ 151.000
- % IntenÃ§Ã£o estimada: 18%
```

**DADOS DO PASSO 7 (Oferta):**
```
Oferta Faixa R$ 130-170k:
- Pulverizada: 0 (lotes populares escassos)
- LanÃ§amentos: 0 (nenhum concorrente direto)
- TBC (futura): 0 (zoneamento restritivo)
TOTAL: 0 unidades
```

**PASSO 8 - ANÃLISE DE ABSORÃ‡ÃƒO:**

**CENÃRIO 1: Baseline (DÃ©ficit, Price, Fator 10:1)**
```
Demanda Bruta: 8.729 domicÃ­lios
Fator: 10:1 (sem validaÃ§Ã£o)
Demanda Ajustada: 8.729 Ã· 10 = 873 unidades
Oferta Total: 0
AbsorÃ§Ã£o: 873 - 0 = +873 unidades

RazÃ£o D:O: 873 Ã· 35 = 24,9:1 ðŸŽ¯ MUITO ACIMA do mÃ­nimo 10:1

INTERPRETAÃ‡ÃƒO: âœ…âœ…âœ… 
- Demanda ROBUSTA para o produto
- Zero concorrÃªncia direta
- Capacidade de absorver 873 lotes (proposto: 35)
- Janela de oportunidade EXCEPCIONAL
```

**CENÃRIO 2: Conservador (DÃ©ficit, SAC, Fator 10:1)**
```
Demanda Bruta: 8.729 (mesma)
PreÃ§o SAC: R$ 151.000 (mais acessÃ­vel que Price)
Fator: 10:1
Oferta: 0 (conservador nÃ£o muda isso)
AbsorÃ§Ã£o: 873 - 0 = +873

RazÃ£o D:O: 24,9:1 (mantÃ©m)

INTERPRETAÃ‡ÃƒO: âœ…âœ…
- Mesmo cenÃ¡rio conservador Ã© VIÃVEL
- SAC facilita compra (juros menores)
- Margem de seguranÃ§a ALTA
```

**CENÃRIO 3: Otimista (PLUS, Price, Fator 10:1)**
```
Demanda PLUS: 8.729 (DÃ©ficit) + 12.500 (upgrade) = 21.229
Fator: 10:1 (mantÃ©m conservadorismo)
Demanda Ajustada: 21.229 Ã· 10 = 2.123 unidades
AbsorÃ§Ã£o: 2.123 - 0 = +2.123

RazÃ£o D:O: 2.123 Ã· 35 = 60,7:1 ðŸš€

INTERPRETAÃ‡ÃƒO: âœ…âœ…âœ…
- Demanda PLUS quase 3x maior que DÃ©ficit
- Produto pode servir investidores tambÃ©m
- Possibilidade de FASES (35 + 35 + 35...)
```

**VELOCIDADE PROJETADA:**
```
MÃ©todo 1 (RazÃ£o D:O):
Demanda Ajustada / Produto = 873 / 35 = 24,9x
Prazo conservador = 24 meses
Velocidade = 35 Ã· 24 = 1,5 lotes/mÃªs

MÃ©todo 2 (Benchmark mercado):
VSO Leopoldina (loteamentos) = 0,8 lotes/mÃªs (histÃ³rico baixo)
Ajuste TIV (conservador) = 0,8 Ã— 1,2 = 1,0 lote/mÃªs
Prazo = 35 Ã· 1,0 = 35 meses

DECISÃƒO: Usar 1,2 lotes/mÃªs (mÃ©dia entre mÃ©todos)
â†’ Prazo venda: ~29 meses (2,4 anos)
```

**GATES DE DECISÃƒO:**
```
âœ… AbsorÃ§Ã£o positiva: +873 (todos cenÃ¡rios)
âœ… RazÃ£o D:O: 24,9:1 (muito acima de 10:1)
âœ… Zero concorrÃªncia direta
âœ… PreÃ§o dentro da capacidade C1
âœ… Velocidade projetada: 1,2 lotes/mÃªs (realista)

DECISÃƒO FINAL: ðŸŸ¢ GO
```

**RECOMENDAÃ‡Ã•ES ESTRATÃ‰GICAS:**
```
1. PREÃ‡O: Manter R$ 140k (dentro da faixa)
   - Considerar R$ 135k para acelerar (ainda lucrativo)

2. MIX: 100% lotes 250mÂ² (padrÃ£o classe C1)
   - Considerar 20% de lotes 300mÂ² (teste C2)

3. PRAÃ‡A: Focar bairros DÃ©ficit (sem casa prÃ³pria)
   - Marketing: "Saia do aluguel, realize o sonho"

4. PROMOÃ‡ÃƒO: LanÃ§amento em 2 fases (35 + 35)
   - Fase 1: Criar escassez ("Ãºltimos lotes")
   - Fase 2: ApÃ³s 12-18 meses (novo pÃºblico)

5. TIMING: LanÃ§ar em 90 dias (apÃ³s Passos 9-10)
   - Mercado aquecido, janela curta
```

---

### 9.2. Caso Real: Vertical MÃ©dio PadrÃ£o - Centro de Leopoldina

**CONTEXTO:**
- Terreno: 1.200 mÂ² (Av. Andradas, zona central)
- Produto proposto: 24 apartamentos 2 dorm (70mÂ²)
- PreÃ§o-alvo: R$ 420.000/unidade
- MunicÃ­pio: Leopoldina-MG

**DADOS DO PASSO 6:**
```
Classe B1 (Faixa R$ 350-450k):
- DomicÃ­lios: 9.158
- PreÃ§o mÃ¡ximo Price: R$ 387.147
- PreÃ§o mÃ¡ximo SAC: R$ 342.000
- % IntenÃ§Ã£o: 22%

ALERTA: PreÃ§o-alvo (R$ 420k) > Capacidade B1 (R$ 387k)
â†’ Produto direcionado para CLASSE A2
```

**DADOS DO PASSO 7:**
```
Oferta Vertical Centro (R$ 350-500k):
- Pulverizada: 89 (usados, baixa relevÃ¢ncia)
- LanÃ§amentos: 36 (2 empreendimentos diretos)
- TBC: 48 (1 terreno aprovado, construÃ§Ã£o em 18m)
TOTAL: 84 unidades (36 + 48, ignora pulverizada)
```

**PASSO 8 - ANÃLISE:**

**CENÃRIO 1: Baseline (Classe A2, Price, Fator 10:1)**
```
Classe A2 (ajustada para preÃ§o R$ 420k):
DomicÃ­lios: 4.277
PreÃ§o mÃ¡ximo Price: R$ 655.342 âœ… (suporta R$ 420k)
Fator: 10:1
Demanda Ajustada: 4.277 Ã· 10 = 428 unidades
Oferta: 84

AbsorÃ§Ã£o: 428 - 84 = +344 unidades

RazÃ£o D:O: 428 Ã· 24 = 17,8:1 ðŸŽ¯

INTERPRETAÃ‡ÃƒO: âœ…âœ…
- AbsorÃ§Ã£o POSITIVA e ROBUSTA
- RazÃ£o 17,8:1 >> 10:1 (mÃ­nimo)
- Classe A2 suporta preÃ§o R$ 420k
- ConcorrÃªncia moderada (84 un)
```

**CENÃRIO 2: Conservador (A2, SAC, Oferta +20%)**
```
Demanda: 4.277 (mesma)
PreÃ§o SAC: R$ 580.000 (ainda suporta R$ 420k)
Oferta conservadora: 84 Ã— 1,2 = 101 unidades
AbsorÃ§Ã£o: 428 - 101 = +327

RazÃ£o D:O: 428 Ã· 24 = 17,8:1 (mantÃ©m)

INTERPRETAÃ‡ÃƒO: âœ…
- Mesmo cenÃ¡rio conservador = VIÃVEL
- AbsorÃ§Ã£o levemente menor (+327 vs +344)
- Gate 17,8:1 ainda robusto
```

**CENÃRIO 3: Produto Reposicionado (B1, SAC, PreÃ§o R$ 342k)**
```
Se ajustar preÃ§o para R$ 342k (limite SAC Classe B1):

Demanda B1: 9.158
Fator: 10:1
Demanda Ajustada: 916 unidades
Oferta: 84 (mesma faixa)
AbsorÃ§Ã£o: 916 - 84 = +832

RazÃ£o D:O: 916 Ã· 24 = 38,2:1 ðŸš€

INTERPRETAÃ‡ÃƒO: âœ…âœ…âœ…
- AbsorÃ§Ã£o MUITO SUPERIOR (+832 vs +344)
- Base de compradores 2x maior (B1 > A2)
- Trade-off: VGV menor (R$ 342k vs R$ 420k)
- DECISÃƒO: Modelar ambos no FCD (Passo 10)
```

**VELOCIDADE PROJETADA:**
```
Classe A2 (R$ 420k):
VSO mercado vertical centro = 2,8 un/mÃªs
Ajuste TIV = 2,8 Ã— 0,85 = 2,4 un/mÃªs
Prazo = 24 Ã· 2,4 = 10 meses âœ…

Classe B1 (R$ 342k):
Demanda maior â†’ acelera
ProjeÃ§Ã£o: 3,5 un/mÃªs
Prazo = 24 Ã· 3,5 = 7 meses âœ…

CONCLUSÃƒO: Ambos viÃ¡veis, B1 mais rÃ¡pido
```

**GATES:**
```
CenÃ¡rio A2 (R$ 420k):
âœ… AbsorÃ§Ã£o: +344
âœ… RazÃ£o D:O: 17,8:1
âœ… Velocidade: 2,4 un/mÃªs (10 meses)
âœ… VGV: R$ 10,08 milhÃµes

CenÃ¡rio B1 (R$ 342k):
âœ… AbsorÃ§Ã£o: +832
âœ… RazÃ£o D:O: 38,2:1
âœ… Velocidade: 3,5 un/mÃªs (7 meses)
âš ï¸ VGV: R$ 8,21 milhÃµes (-18% vs A2)

DECISÃƒO: Ambos aprovados, definir no FCD
```

**RECOMENDAÃ‡Ã•ES:**
```
1. Modelar AMBOS cenÃ¡rios no Passo 10 (FCD)
   - A2: Maior VGV, pÃºblico menor
   - B1: Menor VGV, giro mais rÃ¡pido

2. Considerar MIX:
   - 16 aptos R$ 420k (A2) + 8 aptos R$ 342k (B1)
   - Diversifica risco, maximiza absorÃ§Ã£o

3. Timing: LanÃ§ar em 120 dias
   - ConcorrÃªncia moderada, janela de 12-18 meses
   - 2 TBC futuros exigem velocidade

4. EstratÃ©gia: PreÃ§o dinÃ¢mico
   - Fase 1 (1-6m): R$ 420k (teste A2)
   - Fase 2 (7-12m): Ajustar para R$ 380k se necessÃ¡rio
```

---

### 9.3. Caso Negativo: Alto PadrÃ£o em Mercado Saturado

**CONTEXTO:**
- Terreno: 3.500 mÂ² (bairro perifÃ©rico)
- Produto proposto: 18 casas alto padrÃ£o (180mÂ²)
- PreÃ§o-alvo: R$ 850.000/unidade
- MunicÃ­pio: Leopoldina-MG

**DADOS DO PASSO 6:**
```
Classe A1 (Faixa R$ 800k+):
- DomicÃ­lios: 4.041
- PreÃ§o mÃ¡ximo Price: R$ 1.413.752 âœ…
- LocalizaÃ§Ã£o desejada: Centro/bairros nobres âš ï¸
```

**DADOS DO PASSO 7:**
```
Oferta Alto PadrÃ£o (R$ 800k+):
- Pulverizada: 428 (casas usadas)
- LanÃ§amentos: 0
- TBC: 72 (2 condomÃ­nios aprovados, localizaÃ§Ã£o CENTRO)
TOTAL: 72 unidades (ignora pulverizada)
```

**PASSO 8 - ANÃLISE:**

**CENÃRIO Baseline:**
```
Demanda: 4.041
Fator: 10:1
Demanda Ajustada: 404 unidades
Oferta: 72

AbsorÃ§Ã£o: 404 - 72 = +332 âœ…

RazÃ£o D:O: 404 Ã· 18 = 22,4:1 âœ…

INTERPRETAÃ‡ÃƒO INICIAL: âœ… AbsorÃ§Ã£o positiva
```

**âš ï¸ MAS ATENÃ‡ÃƒO: AnÃ¡lise Qualitativa CrÃ­tica**

**PROBLEMA 1: LocalizaÃ§Ã£o Desalinhada**
```
Classe A1 prioriza:
- Centro (46% preferÃªncia)
- Bairros nobres (32%)
- Periferia (apenas 8%) âŒ

Terreno proposto: Periferia
â†’ Desconto demanda: 404 Ã— 0,08 = 32 unidades (real)

RECÃLCULO:
AbsorÃ§Ã£o Real = 32 - 72 = -40 âŒ SATURAÃ‡ÃƒO
```

**PROBLEMA 2: TBC em LocalizaÃ§Ã£o Privilegiada**
```
ConcorrÃªncia futura:
- 2 condomÃ­nios no CENTRO (preferÃªncia A1)
- LanÃ§amento em 6-12 meses
- PreÃ§o similar: R$ 800-900k

â†’ Produto proposto compete em DESVANTAGEM
```

**GATES:**
```
âŒ AbsorÃ§Ã£o real: -40 (apÃ³s ajuste localizaÃ§Ã£o)
âŒ LocalizaÃ§Ã£o desalinhada com preferÃªncia A1
âŒ ConcorrÃªncia em localizaÃ§Ã£o superior
âš ï¸ Classe A1: volume pequeno (4.041 domicÃ­lios)
âš ï¸ VSO alto padrÃ£o Leopoldina: 0,3 un/mÃªs (mercado lento)

DECISÃƒO: ðŸ”´ NO-GO ou PIVOT
```

**RECOMENDAÃ‡Ã•ES:**
```
OPÃ‡ÃƒO 1: NO-GO
- NÃ£o construir alto padrÃ£o neste terreno
- Revender terreno ou buscar outro uso

OPÃ‡ÃƒO 2: PIVOT DE PRODUTO
- Reduzir padrÃ£o: R$ 420k (Classe A2/B1)
- Aumentar unidades: 40 casas 100mÂ²
- Demanda A2: 4.277 domicÃ­lios
- AbsorÃ§Ã£o: (4.277 Ã· 10) - 84 = +344 âœ…

OPÃ‡ÃƒO 3: PIVOT DE MERCADO
- Buscar terreno NO CENTRO
- Manter produto alto padrÃ£o
- Competir de igual para igual

DECISÃƒO: Priorizar OPÃ‡ÃƒO 2 (pivot produto)
```

---

## 10. CHECKLIST DE QUALIDADE

### 10.1. Definition of Done (DoD)

**ANTES de considerar Passo 8 CONCLUÃDO, validar:**

#### **PRÃ‰-CONDIÃ‡Ã•ES (4 itens)**
- [ ] Passo 6 concluÃ­do (demanda + preÃ§o Price/SAC)
- [ ] Passo 7 concluÃ­do (oferta total por faixa)
- [ ] Produto proposto definido (unidades, tipologia, preÃ§o)
- [ ] Fator de conversÃ£o definido (10:1 ou 4:1 com justificativa)

#### **CENÃRIOS PROCESSADOS (3 itens)**
- [ ] Baseline rodado (DÃ©ficit, Price, Fator 10:1)
- [ ] Conservador rodado (DÃ©ficit, SAC, Oferta +20%)
- [ ] Otimista rodado (PLUS, Price, Fator ajustado)

#### **CÃLCULOS EXECUTADOS (6 itens)**
- [ ] AbsorÃ§Ã£o por faixa calculada (â‰¥2 faixas)
- [ ] AbsorÃ§Ã£o por H3 calculada (se aplicÃ¡vel)
- [ ] RazÃ£o Demanda:Oferta verificada
- [ ] Sinal de absorÃ§Ã£o interpretado (+/-/0)
- [ ] Magnitude de absorÃ§Ã£o analisada
- [ ] Velocidade de vendas estimada (un/mÃªs)

#### **GATES AVALIADOS (3 itens)**
- [ ] Gate 4:1 (ou 10:1) verificado
- [ ] AbsorÃ§Ã£o â‰¥ 0 em â‰¥2 cenÃ¡rios (GO) OU
- [ ] AbsorÃ§Ã£o < 0 (HOLD/NO-GO) com ajustes recomendados

#### **OUTPUTS GERADOS (5 itens)**
- [ ] O8-1_Absorcao_por_faixa.csv criado
- [ ] O8-2_Absorcao_por_subarea_H3.csv criado (se H3)
- [ ] O8-3_Simulador_Absorcao.xlsx criado
- [ ] O8-4_Mapa_Absorcao_H3.qgz criado (se H3)
- [ ] O8-5_Resumo_Executivo_P8.md criado

#### **ANÃLISE CRÃTICA (4 itens)**
- [ ] Riscos identificados (saturaÃ§Ã£o, timing, concorrÃªncia)
- [ ] Ajustes recomendados (preÃ§o, mix, praÃ§a, promoÃ§Ã£o)
- [ ] IntegraÃ§Ã£o validada (outputs alimentam Passo 9-10)
- [ ] DecisÃ£o final documentada (GO/HOLD/NO-GO)

#### **RASTREABILIDADE (3 itens)**
- [ ] Premissas documentadas (taxa, prazo, entrada, fator)
- [ ] Fontes registradas (Passos 6-7, data-base)
- [ ] Changelog atualizado (versÃ£o, autor, data, modificaÃ§Ãµes)

**TOTAL: 28 validaÃ§Ãµes obrigatÃ³rias**

---

## 11. PRÃ“XIMOS PASSOS

### 11.1. ApÃ³s Concluir Passo 8

**Fluxo sequencial:**

```
PASSO 8 (AbsorÃ§Ã£o) âœ… CONCLUÃDO
         â†“
PASSO 9 (ConvalidaÃ§Ã£o)
- Validar premissas com pesquisa primÃ¡ria
- Comprovar Gate 4:1 com intenÃ§Ã£o real
- Testar elasticidade preÃ§o (P50, P80)
- Classificar leads (L1/L2/L3)
- TRAVAR premissas para FCD
         â†“
PASSO 10 (FCD - Fluxo de Caixa Descontado)
- Input: Velocidade validada (Passo 8+9)
- Input: PreÃ§o-alvo validado (Passo 9)
- Input: Cronograma vendas (curva absorÃ§Ã£o)
- Processar: ROE, TIR, VPL, Payback
- Output: GO/NO-GO FINAL
         â†“
PITH (RelatÃ³rio Executivo)
- Compilar todos os passos
- Apresentar para stakeholders
- DecisÃ£o fundamentada
```

### 11.2. Handshake P8 â†’ P9

**PACOTE OBRIGATÃ“RIO para Passo 9:**

```
1. O8-5_Resumo_Executivo_P8.md
   â†’ AbsorÃ§Ã£o preliminar (Fator 10:1)
   â†’ Premissas a validar

2. O8-1_Absorcao_por_faixa.csv
   â†’ SegmentaÃ§Ã£o para definir quotas de pesquisa

3. Gates Preliminares
   â†’ RazÃ£o D:O atual (base para Gate 4:1)
   â†’ Faixas prioritÃ¡rias (onde focar pesquisa)

4. Perguntas CrÃ­ticas
   â†’ IntenÃ§Ã£o de compra real (validar 10% â†’ 25%)
   â†’ Sensibilidade preÃ§o (P50, P80)
   â†’ Timing (horizonte 0-24 meses)
   â†’ ObjeÃ§Ãµes principais
```

### 11.3. Handshake P8 â†’ P10

**PACOTE OBRIGATÃ“RIO para FCD:**

```
1. Velocidade Validada
   â†’ Unidades/mÃªs (curva rampa-pico-desaceleraÃ§Ã£o)
   â†’ Prazo total de vendas
   â†’ CenÃ¡rios (base/conservador/otimista)

2. PreÃ§o Validado
   â†’ Price ou SAC (decisÃ£o estratÃ©gica)
   â†’ Faixa de preÃ§o por fase
   â†’ Elasticidade testada (P9)

3. Mix Definido
   â†’ Tipologias por fase
   â†’ Quantidade de unidades
   â†’ Faseamento fÃ­sico

4. Premissas Travadas
   â†’ Taxa de juros (% a.m.)
   â†’ Prazo financiamento (meses)
   â†’ Entrada (%)
   â†’ Fator de absorÃ§Ã£o (4:1 validado)
```

---

## 12. PRINCÃPIOS FINAIS

### 12.1. Lembre-se Sempre

**1. FATOR 10:1 Ã‰ O DEFAULT**
```
Sem pesquisa primÃ¡ria = OBRIGATÃ“RIO 10:1
Aplicar 4:1 sem validaÃ§Ã£o = ERRO GRAVE
Superestima absorÃ§Ã£o e gera prejuÃ­zo
```

**2. ABSORÃ‡ÃƒO POSITIVA â‰  GO AUTOMÃTICO**
```
Analisar TAMBÃ‰M:
- Magnitude (+10 un vs +1.000 un)
- RazÃ£o D:O (â‰¥4:1 ideal)
- Contexto qualitativo (localizaÃ§Ã£o, timing, concorrÃªncia)
```

**3. OFERTA TBC NÃƒO PODE SER IGNORADA**
```
Terrenos aprovados = concorrÃªncia FUTURA
Incluir no cÃ¡lculo conservador
Pipeline pode saturar mercado em 12-18 meses
```

**4. CENÃRIOS SÃƒO OBRIGATÃ“RIOS**
```
Nunca fazer apenas Baseline
Conservador testa robustez
Otimista testa teto de mercado
```

**5. PRICE vs SAC = DECISÃƒO ESTRATÃ‰GICA**
```
Price: Maximiza VGV (parcelas fixas)
SAC: Facilita venda (juros menores)
Classes C1/C2: SAC preferÃ­vel
Classes A1/A2: Price aceitÃ¡vel
```

**6. VELOCIDADE REALISTA > VELOCIDADE OTIMISTA**
```
Curva real: rampa â†’ pico â†’ desaceleraÃ§Ã£o
NÃ£o assumir vendas lineares
Conservadorismo protege fluxo de caixa
```

**7. SATURAÃ‡ÃƒO = RED FLAG CRÃTICO**
```
AbsorÃ§Ã£o < 0 = NO-GO ou PIVOT
Mercado nÃ£o comporta mais unidades
Revisar: preÃ§o, produto, praÃ§a ou timing
```

### 12.2. CitaÃ§Ãµes-Guia TIV

> **"A demanda Ã© maior que a oferta?"**  
> â€• Pergunta central do Passo 8

> **"AbsorÃ§Ã£o positiva com RazÃ£o D:O â‰¥4:1 Ã© o gate comercial"**  
> â€• PadrÃ£o TIV validado em dezenas de projetos

> **"Fator 4:1 sem validaÃ§Ã£o Ã© chute caro"**  
> â€• Conservadorismo metodolÃ³gico inviolÃ¡vel

> **"Oferta futura (TBC) compete tanto quanto oferta atual"**  
> â€• Pipeline nÃ£o pode ser ignorado

> **"Velocidade de vendas define viabilidade financeira"**  
> â€• Input crÃ­tico para FCD (Passo 10)

> **"AbsorÃ§Ã£o mede capacidade, nÃ£o certeza"**  
> â€• Passo 9 valida premissas com mercado real

> **"Price maximiza VGV, SAC minimiza resistÃªncia"**  
> â€• DecisÃ£o estratÃ©gica baseada em pÃºblico-alvo

---

## 13. CHANGELOG

| VersÃ£o | Data | Autor | ModificaÃ§Ãµes |
|:------:|:----:|:------|:-------------|
| 1.0 | 2025-01-12 | Claude + Othon | CriaÃ§Ã£o da Skill Passo 8 - AbsorÃ§Ã£o de Mercado. Framework completo com 2 Pilares (DÃ©ficit + PLUS), Fatores 10:1/4:1, mÃ©todo Price/SAC, 3 cenÃ¡rios obrigatÃ³rios, 5 outputs estruturados, 3 casos de uso (2 GO, 1 NO-GO), 28 validaÃ§Ãµes DoD, integraÃ§Ã£o P6-P7-P9-P10 |

---

**Esta Skill Ã© parte integrante da Metodologia TIV 4.0 - TÃ©cnica Inteligente de Viabilidade**

*VersÃ£o: 1.0 | Data: 12/01/2025 | Autor: Claude + Othon | MunicÃ­pio de ReferÃªncia: Leopoldina-MG*
