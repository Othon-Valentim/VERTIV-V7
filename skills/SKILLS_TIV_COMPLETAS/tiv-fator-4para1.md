---
name: "tiv-fator-4para1"
description: "Formalizacao do principio metodologico Fator 4 para 1 da TIV. Valida que demanda deve ser no minimo 4x maior que oferta (com validacao P9) ou 10x (sem validacao). Define decisao GO/HOLD/NO-GO fundamentada em relacao Demanda:Oferta."
---

# SKILL: Fator 4:1 (Demanda vs Oferta)

## 1. OBJETIVO E CONTEXTO

### 1.1. PropÃ³sito
Formalizar e aplicar o **princÃ­pio metodolÃ³gico central da TIV**: a relaÃ§Ã£o Demanda:Oferta (D:O) deve ser **â‰¥ 4:1** (com validaÃ§Ã£o P9) ou **â‰¥ 10:1** (sem validaÃ§Ã£o) para garantir absorÃ§Ã£o segura do empreendimento imobiliÃ¡rio.

### 1.2. Problema Resolvido
Empreendimentos imobiliÃ¡rios frequentemente falham por:
- SuperestimaÃ§Ã£o de demanda (viÃ©s otimista)
- SubestimaÃ§Ã£o de concorrÃªncia
- LanÃ§amento em mercados saturados (D:O < 4:1)
- AusÃªncia de margem de seguranÃ§a
- AbsorÃ§Ã£o lenta â†’ ROE baixo â†’ inviabilidade

### 1.3. Fundamento MetodolÃ³gico

**CitaÃ§Ã£o-chave KB CORE v5.0:**
> "A demanda validada deve ser no mÃ­nimo 4 vezes maior que a oferta. Sem validaÃ§Ã£o de mercado (Passo 9), a margem de seguranÃ§a exigida aumenta para 10:1."

**Por que 4:1?**
1. **ProteÃ§Ã£o contra otimismo:** Nem toda demanda se converte em venda
2. **Margem de seguranÃ§a:** AbsorÃ§Ã£o funciona mesmo em cenÃ¡rio pessimista
3. **Velocidade garantida:** ROE alto vem de giro rÃ¡pido (Fator 4:1 permite isso)
4. **ValidaÃ§Ã£o empÃ­rica:** Dezenas de projetos reais confirmam a proporÃ§Ã£o

**Por que 10:1 sem validaÃ§Ã£o?**
1. **Risco muito maior:** Premissas nÃ£o testadas em campo (P9)
2. **CompensaÃ§Ã£o:** Margem extremamente conservadora
3. **Disciplina:** Obriga fazer P9 quando margem fica apertada (4:1 < D:O < 10:1)

### 1.4. Base MetodolÃ³gica
- **KB CORE v5.0:** Passo 8 (AbsorÃ§Ã£o) + Passo 9 (ValidaÃ§Ã£o)
- **PrincÃ­pios:** Conservadorismo Inteligente + Velocidade > Margem
- **ROE:** Alta rotaÃ§Ã£o (Fator 4:1) gera ROE superior a projetos com margem apertada

---

## 2. QUANDO ACIONAR

### 2.1. Triggers ObrigatÃ³rios
- [ ] **SEMPRE** apÃ³s completar P6 (Demanda) + P7 (Oferta)
- [ ] **ANTES** de iniciar P8 (AbsorÃ§Ã£o)
- [ ] Como **gate de decisÃ£o** fazer/nÃ£o fazer P9
- [ ] Como **validaÃ§Ã£o final** antes de P10 (FCD)

### 2.2. Triggers Recomendados
- [ ] Ao avaliar viabilidade preliminar de projeto
- [ ] Quando stakeholders questionarem absorÃ§Ã£o
- [ ] Para comparar mÃºltiplos produtos no mesmo terreno
- [ ] Na revisÃ£o pÃ³s-P9 (ajuste D:O com dados validados)

### 2.3. Momentos CrÃ­ticos
- **PrÃ©-Investimento:** Validar D:O antes de comprar terreno
- **PrÃ©-LanÃ§amento:** Confirmar D:O antes de lanÃ§ar produto
- **PÃ³s-Pesquisa:** Recalcular D:O com dados reais de P9

---

## 3. FRAMEWORK/METODOLOGIA

### 3.1. CÃ¡lculo da RelaÃ§Ã£o D:O

**FÃ³rmula:**
```
D:O = Demanda potencial Ã· Oferta competitiva

Onde:
- Demanda potencial = Î£ pÃºblico-alvo qualificado (P6)
  â†’ FamÃ­lias com capacidade de compra (Regra 30%)
  â†’ Dentro da Ã¡rea de influÃªncia (P3)
  â†’ Interessadas no produto (P4)

- Oferta competitiva = Î£ unidades disponÃ­veis + pipeline (P7)
  â†’ Oferta Pulverizada (disponÃ­vel agora)
  â†’ Oferta LanÃ§amentos (em comercializaÃ§Ã£o)
  â†’ Oferta TBC (pipeline prÃ³ximos 24 meses)
```

**Importante:**
- Demanda e oferta devem estar na **mesma faixa de preÃ§o** (Â±15%)
- Demanda e oferta devem ser da **mesma tipologia** (comparÃ¡vel)
- Ãrea de influÃªncia deve ser **consistente** (P3)

---

### 3.2. Matriz de DecisÃ£o

| RelaÃ§Ã£o D:O | ValidaÃ§Ã£o P9 | DecisÃ£o | AÃ§Ã£o Recomendada |
|-------------|--------------|---------|------------------|
| **â‰¥ 10:1** | NÃ£o | ðŸŸ¢ GO | Pode prosseguir sem P9 (margem confortÃ¡vel) |
| **â‰¥ 10:1** | Sim | ðŸŸ¢ GO+ | SeguranÃ§a mÃ¡xima (validado + folga) |
| **4:1 a 10:1** | NÃ£o | ðŸŸ¡ HOLD | **P9 OBRIGATÃ“RIO** (margem apertada) |
| **4:1 a 10:1** | Sim | ðŸŸ¢ GO | Prosseguir (validado + margem mÃ­nima) |
| **2:1 a 4:1** | NÃ£o | ðŸ”´ NO-GO | Margem insuficiente (risco alto) |
| **2:1 a 4:1** | Sim | ðŸ”´ NO-GO | InviÃ¡vel mesmo validado (saturaÃ§Ã£o) |
| **< 2:1** | Qualquer | ðŸ”´ NO-GO | Mercado super-saturado (inviÃ¡vel) |

**Legenda:**
- ðŸŸ¢ **GO:** Prosseguir para P8 (AbsorÃ§Ã£o) e P10 (FCD)
- ðŸŸ¡ **HOLD:** Pausar, executar P9 (ValidaÃ§Ã£o) obrigatoriamente
- ðŸ”´ **NO-GO:** Reprovar projeto (mercado saturado)

---

### 3.3. Ajustes por CenÃ¡rio

#### CenÃ¡rio OTIMISTA
**CondiÃ§Ãµes:**
- Mercado aquecido (ciclo ExpansÃ£o)
- Produto diferenciado (inovaÃ§Ã£o)
- LocalizaÃ§Ã£o premium (centralidade alta)
- HistÃ³rico de absorÃ§Ã£o rÃ¡pida

**Ajuste:**
- Fator pode relaxar para **3:1** (com P9 validado)
- **ATENÃ‡ÃƒO:** Aumenta risco, exige validaÃ§Ã£o rigorosa

---

#### CenÃ¡rio PESSIMISTA
**CondiÃ§Ãµes:**
- Mercado retraÃ­do (ciclo DesaceleraÃ§Ã£o/RecessÃ£o)
- Produto genÃ©rico (commodity)
- LocalizaÃ§Ã£o perifÃ©rica
- ConcorrÃªncia acirrada (VSO > 24 meses)

**Ajuste:**
- Fator aumenta para **6:1** (mesmo com P9)
- Conservadorismo extremo obrigatÃ³rio

---

#### CenÃ¡rio BASE (PadrÃ£o TIV)
**CondiÃ§Ãµes normais de mercado:**
- Fator **4:1** (com P9)
- Fator **10:1** (sem P9)

---

### 3.4. CÃ¡lculo de AbsorÃ§Ã£o Segura

**FÃ³rmula:**
```
AbsorÃ§Ã£o segura (un/mÃªs) = Demanda validada Ã· Prazo comercializaÃ§Ã£o

Margem de seguranÃ§a = [(D:O) - 4] Ã· 4 Ã— 100%
```

**Exemplos:**

| D:O | Margem SeguranÃ§a | ClassificaÃ§Ã£o |
|-----|------------------|---------------|
| 12:1 | (12-4)/4 = 200% | Excelente |
| 8:1 | (8-4)/4 = 100% | Ã“timo |
| 6:1 | (6-4)/4 = 50% | Bom |
| 4:1 | (4-4)/4 = 0% | MÃ­nimo aceitÃ¡vel |
| 3:1 | (3-4)/4 = -25% | Insuficiente |
| 2:1 | (2-4)/4 = -50% | CrÃ­tico |

**InterpretaÃ§Ã£o:**
- Margem â‰¥ 100%: Projeto resiliente (absorve imprevistos)
- Margem 50-99%: Projeto seguro (com P9 validado)
- Margem 0-49%: Projeto no limite (exige P9 + monitoramento)
- Margem negativa: Projeto inviÃ¡vel (reprovar)

---

### 3.5. Handshake com Fator 4:1 e Velocidade (P8)

**RelaÃ§Ã£o D:O â†’ Velocidade de Vendas:**

```
Velocidade real (un/mÃªs) = (Demanda validada Ã· D:O) Ã· Prazo

Exemplo:
- Demanda: 400 famÃ­lias
- Oferta: 100 unidades
- D:O = 4:1
- Prazo: 48 meses

Velocidade teÃ³rica = 100 un Ã· 48 meses = 2.08 un/mÃªs
Velocidade ajustada (Fator 4:1) = 2.08 Ã· 4 = 0.52 un/mÃªs âŒ

CORREÃ‡ÃƒO:
Velocidade conservadora = 100 un Ã· 48 meses = 2.08 un/mÃªs
Com Fator 4:1 aplicado na demanda â†’ absorÃ§Ã£o segura
```

**ATENÃ‡ÃƒO:** Fator 4:1 Ã© sobre **relaÃ§Ã£o D:O**, nÃ£o sobre **velocidade**.

---

## 4. INPUTS NECESSÃRIOS

### 4.1. Do Passo 6 (Demanda)

**ObrigatÃ³rios:**
- [ ] Demanda potencial por faixa de renda
- [ ] Demanda qualificada (capacidade de compra via Regra 30%)
- [ ] Funil de 5 filtros aplicado
- [ ] Ãrea de influÃªncia delimitada (P3)
- [ ] PreÃ§o de venda estimado

**Opcionais (se P9 executado):**
- [ ] Demanda validada (pesquisa de campo)
- [ ] Leads L1 (quentes) quantificados
- [ ] Taxa de conversÃ£o L1â†’Venda

---

### 4.2. Do Passo 7 (Oferta)

**ObrigatÃ³rios:**
- [ ] Oferta Pulverizada (unidades disponÃ­veis)
- [ ] Oferta LanÃ§amentos (em comercializaÃ§Ã£o)
- [ ] Oferta TBC/Pipeline (prÃ³ximos 24 meses)
- [ ] VSO (Velocidade Sobre Oferta) calculado
- [ ] PreÃ§o mÃ©dio concorrÃªncia

**Opcionais:**
- [ ] SaturaÃ§Ã£o identificada (VSO > 24 meses)
- [ ] Posicionamento competitivo

---

### 4.3. Do Passo 9 (se aplicÃ¡vel)

**ObrigatÃ³rios (se P9 executado):**
- [ ] Pesquisa quantitativa realizada (n â‰¥ 100)
- [ ] Leads segmentados (L1, L2, L3)
- [ ] Taxa de conversÃ£o validada
- [ ] AbsorÃ§Ã£o projetada ajustada

---

## 5. PROCESSO DE ANÃLISE

### 5.1. Checklist de ExecuÃ§Ã£o (Passo a Passo)

**Etapa 1: Coletar Inputs**
- [ ] Abrir relatÃ³rio P6 (Demanda)
- [ ] Abrir relatÃ³rio P7 (Oferta)
- [ ] Verificar se P9 foi executado (sim/nÃ£o)
- [ ] Confirmar consistÃªncia de faixa de preÃ§o
- [ ] Confirmar consistÃªncia de Ã¡rea de influÃªncia

**Tempo estimado:** 15 minutos

---

**Etapa 2: Calcular D:O**
- [ ] Aplicar fÃ³rmula: D:O = Demanda Ã· Oferta
- [ ] Usar demanda validada (se P9) ou potencial (sem P9)
- [ ] Incluir oferta completa (Pulverizada + LanÃ§amentos + TBC)
- [ ] Documentar cÃ¡lculo com rastreabilidade

**Tempo estimado:** 10 minutos

---

**Etapa 3: Verificar ValidaÃ§Ã£o**
- [ ] P9 foi executado? (sim/nÃ£o)
- [ ] Se sim: usar relaÃ§Ã£o 4:1 (padrÃ£o)
- [ ] Se nÃ£o: usar relaÃ§Ã£o 10:1 (conservadora)
- [ ] Identificar cenÃ¡rio (base/otimista/pessimista)

**Tempo estimado:** 5 minutos

---

**Etapa 4: Consultar Matriz de DecisÃ£o**
- [ ] Localizar D:O calculado na matriz
- [ ] Identificar decisÃ£o (GO/HOLD/NO-GO)
- [ ] Verificar se P9 Ã© obrigatÃ³rio
- [ ] Anotar recomendaÃ§Ã£o

**Tempo estimado:** 5 minutos

---

**Etapa 5: Calcular Margem de SeguranÃ§a**
- [ ] Aplicar fÃ³rmula: [(D:O) - 4] Ã· 4 Ã— 100%
- [ ] Classificar margem (Excelente/Ã“timo/Bom/MÃ­nimo/Insuficiente)
- [ ] Documentar resultado

**Tempo estimado:** 5 minutos

---

**Etapa 6: Gerar RecomendaÃ§Ã£o**
- [ ] Consolidar decisÃ£o (GO/HOLD/NO-GO)
- [ ] Fundamentar com dados (D:O, margem, validaÃ§Ã£o)
- [ ] Listar alertas crÃ­ticos (se aplicÃ¡vel)
- [ ] Definir prÃ³ximos passos

**Tempo estimado:** 10 minutos

---

**Etapa 7: Documentar e Entregar**
- [ ] Preencher template de output (YAML)
- [ ] Gerar semÃ¡foro visual (emoji)
- [ ] Incluir recomendaÃ§Ã£o estruturada
- [ ] Entregar para P8 (se GO) ou revisar (se HOLD/NO-GO)

**Tempo estimado:** 10 minutos

**Tempo total:** 60 minutos

---

## 6. OUTPUTS ESPERADOS

### 6.1. CÃ¡lculo de D:O (YAML)

```yaml
relacao_demanda_oferta:
  # INPUTS
  demanda_potencial: 450 # famÃ­lias (P6)
  demanda_validada: 420 # famÃ­lias (P9, se aplicÃ¡vel)
  oferta_pulverizada: 30 # unidades
  oferta_lancamentos: 50 # unidades
  oferta_tbc: 20 # unidades (pipeline 24m)
  oferta_total: 100 # unidades
  
  # CÃLCULO
  ratio_DO: 4.2 # (420 Ã· 100)
  validacao_P9: sim # pesquisa realizada?
  
  # DECISÃƒO
  decisao: GO # GO/HOLD/NO-GO
  margem_seguranca: 5% # [(4.2-4)/4 Ã— 100]
  
  # CLASSIFICAÃ‡ÃƒO
  semaforo: "ðŸŸ¢ VERDE" # GO
  confianca: alta # alta/mÃ©dia/baixa
  
  # FUNDAMENTO
  justificativa: "D:O de 4.2:1 com validacao P9 atende criterio minimo 4:1. Margem de seguranca apertada (5%), mas suficiente para GO. AbsorÃ§Ã£o deve ser monitorada de perto."
```

---

### 6.2. SemÃ¡foro de DecisÃ£o

```
ðŸŸ¢ VERDE (D:O â‰¥ 10:1 sem P9 OU D:O â‰¥ 4:1 com P9)
   â””â”€ GO - Prosseguir para P8 (AbsorÃ§Ã£o)

ðŸŸ¡ AMARELO (4:1 â‰¤ D:O < 10:1 sem P9)
   â””â”€ HOLD - Executar P9 (ValidaÃ§Ã£o) OBRIGATÃ“RIO

ðŸ”´ VERMELHO (D:O < 4:1)
   â””â”€ NO-GO - Mercado saturado, reprovar projeto
```

---

### 6.3. RecomendaÃ§Ã£o Estruturada (Template)

```markdown
# ANÃLISE FATOR 4:1

## RELAÃ‡ÃƒO DEMANDA:OFERTA
**D:O:** [valor]:1

## VALIDAÃ‡ÃƒO P9
**Status:** [Sim/NÃ£o]
**Leads L1:** [quantidade] (se aplicÃ¡vel)
**Taxa conversÃ£o:** [%] (se aplicÃ¡vel)

## DECISÃƒO
**SemÃ¡foro:** [ðŸŸ¢/ðŸŸ¡/ðŸ”´]
**DecisÃ£o:** [GO/HOLD/NO-GO]

## FUNDAMENTO
**Demanda:**
- Potencial: [X] famÃ­lias/unidades
- Validada: [Y] famÃ­lias (se P9)
- Fonte: [P6 + P9]

**Oferta:**
- Pulverizada: [A] unidades
- LanÃ§amentos: [B] unidades
- TBC (pipeline): [C] unidades
- Total: [D] unidades
- Fonte: [P7]

**CÃ¡lculo:**
- Ratio: [demanda] Ã· [oferta] = [Z]:1
- Margem seguranÃ§a: [(Z-4)/4 Ã— 100]% = [W]%

## RECOMENDAÃ‡ÃƒO
[Texto objetivo com prÃ³ximos passos]

Exemplo:
"Com D:O de 6:1 e validaÃ§Ã£o P9 realizada, o projeto estÃ¡ aprovado (GO). A margem de seguranÃ§a de 50% permite absorÃ§Ã£o segura mesmo em cenÃ¡rio pessimista. Prosseguir para P8 (AbsorÃ§Ã£o) usando velocidade conservadora de 2.5 un/mÃªs."

## ALERTAS
[Lista de riscos ou observaÃ§Ãµes, se aplicÃ¡vel]

Exemplos:
- âš ï¸ Margem apertada (5%): monitorar absorÃ§Ã£o de perto
- âš ï¸ VSO concorrÃªncia alto (22 meses): mercado desacelerando
- âœ… Nenhum alerta crÃ­tico identificado
```

---

## 7. ALERTAS E VALIDAÃ‡Ã•ES

### 7.1. Red Flags CrÃ­ticos

| SituaÃ§Ã£o | D:O | Criticidade | DecisÃ£o | AÃ§Ã£o |
|----------|-----|-------------|---------|------|
| Super-saturaÃ§Ã£o | < 2:1 | ðŸ”´ CRÃTICA | NO-GO imediato | Abandonar projeto |
| SaturaÃ§Ã£o alta | 2:1 - 3:99:1 | ðŸ”´ CRÃTICA | NO-GO | Reprovar (mesmo com P9) |
| Margem apertada | 4:1 - 5:99:1 | ðŸŸ¡ ALTA | HOLD â†’ P9 | P9 obrigatÃ³rio |
| Zona segura | 6:1 - 9:99:1 | ðŸŸ¢ MÃ‰DIA | GO (com P9) | Prosseguir com validaÃ§Ã£o |
| Zona confortÃ¡vel | â‰¥ 10:1 | ðŸŸ¢ BAIXA | GO (sem P9) | Prosseguir sem necessidade de validar |

---

### 7.2. ValidaÃ§Ãµes ObrigatÃ³rias

**Antes de calcular D:O:**
- [ ] Demanda Ã© **PAGANTE** (nÃ£o apenas interessados)?
  - âŒ "500 pessoas curtiram no Instagram" â†’ NÃƒO Ã© demanda
  - âœ… "450 famÃ­lias com renda â‰¥ R$ 8k" â†’ SIM Ã© demanda

- [ ] Oferta inclui **PIPELINE (TBC)**?
  - âŒ Considerar apenas oferta jÃ¡ lanÃ§ada â†’ subestima concorrÃªncia
  - âœ… Incluir projetos em aprovaÃ§Ã£o (prÃ³ximos 24m) â†’ realista

- [ ] CÃ¡lculo usa **mesma faixa de preÃ§o** (Â±15%)?
  - âŒ Comparar apartamento R$ 300k com casa R$ 600k â†’ erro
  - âœ… Comparar produtos na faixa R$ 280k-320k â†’ correto

- [ ] Ãrea de influÃªncia Ã© **consistente** (P3)?
  - âŒ Demanda em raio 20km, oferta em raio 5km â†’ inconsistente
  - âœ… Ambos no polÃ­gono 15min (isÃ³crona) â†’ consistente

- [ ] Tipologias sÃ£o **comparÃ¡veis**?
  - âŒ Comparar loteamento com apartamento â†’ erro
  - âœ… Comparar casa tÃ©rrea com casa sobrado â†’ comparÃ¡vel

---

### 7.3. Chutes Caros Comuns (Anti-Patterns)

| Chute Caro | Problema | CorreÃ§Ã£o TIV |
|------------|----------|--------------|
| "Vou vender 5 un/mÃªs porque quero" | Sem base em D:O | Calcular D:O primeiro, depois absorÃ§Ã£o |
| "Demanda Ã© infinita (cidade grande)" | Demanda nÃ£o segmentada | Aplicar funil 5 filtros (P6) |
| "ConcorrÃªncia nÃ£o importa" | Ignorar oferta | Mapear 3 Ofertas (P7) + TBC |
| "Vou lanÃ§ar sem pesquisa" | D:O entre 4:1-10:1 sem P9 | HOLD â†’ fazer P9 obrigatÃ³rio |
| "D:O de 2:1 estÃ¡ bom" | Abaixo do mÃ­nimo | NO-GO imediato (saturaÃ§Ã£o) |

**AÃ§Ã£o:** Reprovar premissa e exigir cÃ¡lculo conforme metodologia TIV.

---

### 7.4. CenÃ¡rios Especiais

**Caso 1: D:O > 10:1 mas VSO concorrÃªncia > 24 meses**
- **SituaÃ§Ã£o:** Demanda alta, mas oferta nÃ£o absorve
- **Alerta:** Problema pode nÃ£o ser D:O, mas qualidade da oferta
- **AÃ§Ã£o:** Investigar por que concorrÃªncia nÃ£o vende (preÃ§o? localizaÃ§Ã£o? produto?)

**Caso 2: D:O = 4:1 mas pesquisa P9 reprova premissa**
- **SituaÃ§Ã£o:** CÃ¡lculo matemÃ¡tico OK, mas campo invalida
- **Alerta:** Demanda teÃ³rica â‰  demanda real
- **AÃ§Ã£o:** Recalcular D:O com demanda validada (P9) e reavaliar

**Caso 3: D:O < 4:1 mas produto Ã© inovador/Ãºnico**
- **SituaÃ§Ã£o:** SaturaÃ§Ã£o, mas sem concorrÃªncia direta
- **Alerta:** Oceano azul (sem comparÃ¡veis)
- **AÃ§Ã£o:** P9 obrigatÃ³rio + ajuste para Fator 3:1 (exceÃ§Ã£o, com P9)

---

## 8. INTEGRAÃ‡ÃƒO COM OUTRAS SKILLS

### 8.1. DependÃªncias (Inputs)

**Upstream (alimentam Fator 4:1):**

```mermaid
graph LR
    P3[P3 Ãrea InfluÃªncia] --> P6[P6 Demanda]
    P4[P4 VocaÃ§Ã£o] --> P6
    P6 --> F41[Fator 4:1]
    P7[P7 Oferta] --> F41
    P9[P9 ValidaÃ§Ã£o] -.opcional.-> F41
```

**Handshakes crÃ­ticos:**
- **P3â†’P6:** Ãrea de influÃªncia delimita onde buscar demanda
- **P4â†’P6:** VocaÃ§Ã£o define qual produto buscar
- **P6+P7â†’Fator 4:1:** CÃ¡lculo da relaÃ§Ã£o D:O
- **P9â†’Fator 4:1:** ValidaÃ§Ã£o ajusta demanda (se executado)

---

### 8.2. Alimenta (Outputs)

**Downstream (recebem output do Fator 4:1):**

```mermaid
graph LR
    F41[Fator 4:1] --> P8[P8 AbsorÃ§Ã£o]
    F41 --> P9[P9 ValidaÃ§Ã£o]
    F41 --> P10[P10 FCD]
    F41 --> VAL[Validador]
```

**Handshakes crÃ­ticos:**
- **Fator 4:1â†’P8:** DecisÃ£o GO/HOLD/NO-GO trava absorÃ§Ã£o
- **Fator 4:1â†’P9:** Se HOLD, obriga executar P9
- **Fator 4:1â†’P10:** Premissa crÃ­tica do FCD (absorÃ§Ã£o segura)
- **Fator 4:1â†’Validador:** Checklist valida se D:O â‰¥ 4:1

---

### 8.3. IntegraÃ§Ã£o com tiv-passo8-absorcao

**Fator 4:1 alimenta P8 com:**
- DecisÃ£o GO/HOLD/NO-GO
- Margem de seguranÃ§a (%)
- Necessidade ou nÃ£o de P9

**P8 usa Fator 4:1 para:**
- Calcular velocidade de vendas segura
- Projetar cronograma realista
- Aplicar conservadorismo (se margem apertada)

**Exemplo de handshake:**
```yaml
# Output Fator 4:1
fator_41:
  ratio_DO: 6.5:1
  decisao: GO
  margem_seguranca: 62.5%
  validacao_P9: sim

# Input para P8 (AbsorÃ§Ã£o)
absorcao:
  premissa_validada: sim # (Fator 4:1 = GO)
  margem_seguranca: 62.5% # (buffer para imprevistos)
  velocidade_conservadora: 2.5 un/mÃªs # (com folga)
  prazo_total: 48 meses # (realista)
```

---

### 8.4. IntegraÃ§Ã£o com tiv-passo9-convalidacao

**Fator 4:1 decide se P9 Ã© obrigatÃ³rio:**
- D:O â‰¥ 10:1 â†’ P9 opcional (mas recomendado)
- 4:1 â‰¤ D:O < 10:1 â†’ P9 **OBRIGATÃ“RIO**
- D:O < 4:1 â†’ P9 nÃ£o resolve (NO-GO direto)

**P9 valida premissas e ajusta D:O:**
- Demanda potencial (P6) â†’ Demanda validada (P9)
- Recalcular D:O com dados reais
- Confirmar ou reprovar projeto

**Fluxo:**
```
P6 (Demanda) + P7 (Oferta) â†’ Fator 4:1 (D:O inicial)
â†“
Se 4:1 â‰¤ D:O < 10:1 â†’ HOLD â†’ Executar P9
â†“
P9 valida â†’ Recalcular Fator 4:1 (D:O ajustado)
â†“
Se D:O ajustado â‰¥ 4:1 â†’ GO para P8
Se D:O ajustado < 4:1 â†’ NO-GO
```

---

### 8.5. IntegraÃ§Ã£o com tiv-validador

**Validador checa Fator 4:1:**
- [ ] D:O foi calculado?
- [ ] D:O â‰¥ 4:1 (com P9) ou â‰¥ 10:1 (sem P9)?
- [ ] Se 4:1 â‰¤ D:O < 10:1, P9 foi executado?
- [ ] Margem de seguranÃ§a documentada?
- [ ] DecisÃ£o GO/HOLD/NO-GO fundamentada?

**Criticidade:**
- D:O nÃ£o calculado â†’ **CRÃTICO** (gap P7)
- D:O < 4:1 sem alerta â†’ **CRÃTICO** (reprovar estudo)
- D:O entre 4:1-10:1 sem P9 â†’ **ALTO** (P9 obrigatÃ³rio)

---

## 9. EXEMPLOS PRÃTICOS

### 9.1. EXEMPLO 1: GO DIRETO (D:O = 12:1)

**Contexto:**
- **Projeto:** Loteamento Jardim Primavera
- **LocalizaÃ§Ã£o:** Leopoldina-MG
- **Produto:** 100 lotes residenciais (300-400mÂ²)
- **PreÃ§o mÃ©dio:** R$ 120.000/lote
- **Data:** Janeiro/2025

---

**Inputs:**

**Demanda (P6):**
- PopulaÃ§Ã£o Ã¡rea influÃªncia: 45.000 habitantes (polÃ­gono 15 min)
- FamÃ­lias totais: 12.500 (3,6 hab/famÃ­lia)
- Renda â‰¥ R$ 4.000: 3.200 famÃ­lias (25,6%)
- Capacidade de compra (30%): 1.200 famÃ­lias qualificadas
- **Demanda potencial: 1.200 famÃ­lias**
- **ValidaÃ§Ã£o P9: NÃƒO executada**

**Oferta (P7):**
- Oferta Pulverizada: 20 lotes (em venda individual)
- Oferta LanÃ§amentos: 50 lotes (Loteamento Bela Vista)
- Oferta TBC: 30 lotes (projeto em aprovaÃ§Ã£o)
- **Oferta total: 100 lotes**
- VSO mÃ©dio: 12 meses (saudÃ¡vel)

---

**CÃ¡lculo:**
```yaml
relacao_demanda_oferta:
  demanda_potencial: 1200 # famÃ­lias (P6)
  demanda_validada: null # P9 nÃ£o executado
  oferta_total: 100 # lotes
  
  ratio_DO: 12.0 # (1.200 Ã· 100)
  validacao_P9: nao
  
  decisao: GO
  margem_seguranca: 200% # [(12-4)/4 Ã— 100]
  
  semaforo: "ðŸŸ¢ VERDE"
  confianca: alta
```

**Margem de seguranÃ§a:**
```
Margem = (12 - 4) Ã· 4 Ã— 100% = 200%
```

**InterpretaÃ§Ã£o:**
- D:O de **12:1** estÃ¡ **ACIMA** do limiar 10:1 (sem P9)
- Margem de seguranÃ§a de **200%** Ã© **excelente**
- Projeto pode absorver atÃ© 67% de erro na demanda e ainda ter D:O â‰¥ 4:1

---

**DecisÃ£o:**
```
ðŸŸ¢ GO DIRETO (sem necessidade de P9)

FUNDAMENTO:
- RelaÃ§Ã£o D:O de 12:1 supera critÃ©rio mÃ­nimo de 10:1 para projetos sem validaÃ§Ã£o P9
- Margem de seguranÃ§a de 200% garante absorÃ§Ã£o mesmo em cenÃ¡rio pessimista
- VSO concorrÃªncia saudÃ¡vel (12 meses) nÃ£o indica saturaÃ§Ã£o
- Pode prosseguir para P8 (AbsorÃ§Ã£o) diretamente

OBSERVAÃ‡ÃƒO:
- P9 Ã© opcional, mas recomendado para refinar premissas
- Se executar P9, poderÃ¡ otimizar preÃ§o e cronograma
```

---

**PrÃ³ximos Passos:**
1. âœ… Prosseguir para P8 (AbsorÃ§Ã£o)
2. âœ… Calcular velocidade conservadora (~2 lotes/mÃªs)
3. âœ… Projetar cronograma de 48 meses
4. âšª P9 opcional (mas recomendado para otimizaÃ§Ã£o)

---

### 9.2. EXEMPLO 2: HOLD - P9 OBRIGATÃ“RIO (D:O = 5:1)

**Contexto:**
- **Projeto:** Residencial Vista Verde
- **LocalizaÃ§Ã£o:** Cataguases-MG
- **Produto:** 50 apartamentos (2 quartos, 60mÂ²)
- **PreÃ§o mÃ©dio:** R$ 280.000/unidade
- **Data:** MarÃ§o/2025

---

**Inputs:**

**Demanda (P6):**
- PopulaÃ§Ã£o Ã¡rea influÃªncia: 35.000 habitantes (polÃ­gono 15 min)
- FamÃ­lias totais: 9.700
- Renda â‰¥ R$ 8.000: 650 famÃ­lias (6,7%)
- Capacidade de compra (30%): 250 famÃ­lias qualificadas
- **Demanda potencial: 250 famÃ­lias**
- **ValidaÃ§Ã£o P9: NÃƒO executada**

**Oferta (P7):**
- Oferta Pulverizada: 10 apartamentos (revenda)
- Oferta LanÃ§amentos: 30 apartamentos (EdifÃ­cio ParaÃ­so)
- Oferta TBC: 10 apartamentos (projeto em anÃ¡lise)
- **Oferta total: 50 unidades**
- VSO mÃ©dio: 18 meses (moderado)

---

**CÃ¡lculo:**
```yaml
relacao_demanda_oferta:
  demanda_potencial: 250 # famÃ­lias (P6)
  demanda_validada: null # P9 nÃ£o executado
  oferta_total: 50 # unidades
  
  ratio_DO: 5.0 # (250 Ã· 50)
  validacao_P9: nao
  
  decisao: HOLD
  margem_seguranca: 25% # [(5-4)/4 Ã— 100]
  
  semaforo: "ðŸŸ¡ AMARELO"
  confianca: media
```

**Margem de seguranÃ§a:**
```
Margem = (5 - 4) Ã· 4 Ã— 100% = 25%
```

**InterpretaÃ§Ã£o:**
- D:O de **5:1** estÃ¡ **ENTRE** 4:1 e 10:1 (zona amarela)
- Margem de seguranÃ§a de **25%** Ã© **apertada**
- Projeto pode absorver apenas 20% de erro na demanda (5 â†’ 4)

---

**DecisÃ£o:**
```
ðŸŸ¡ HOLD - P9 OBRIGATÃ“RIO

FUNDAMENTO:
- RelaÃ§Ã£o D:O de 5:1 estÃ¡ na zona amarela (4:1 < D:O < 10:1)
- SEM validaÃ§Ã£o P9, o critÃ©rio mÃ­nimo Ã© 10:1 (nÃ£o atendido)
- Margem apertada (25%) nÃ£o permite prosseguir sem validaÃ§Ã£o
- P9 Ã© OBRIGATÃ“RIO para confirmar premissas

RISCO:
- Se demanda real for 20% menor que estimada (200 famÃ­lias), D:O cai para 4:1
- Margem de erro muito pequena para prosseguir sem validar campo
```

---

**PrÃ³ximos Passos:**
1. â¸ï¸ **PAUSAR** (nÃ£o prosseguir para P8)
2. ðŸ”´ **EXECUTAR P9** (ValidaÃ§Ã£o em campo) **OBRIGATÃ“RIO**
3. âšª ApÃ³s P9, recalcular D:O com demanda validada
4. âšª Se D:O validado â‰¥ 4:1 â†’ GO para P8
5. âšª Se D:O validado < 4:1 â†’ NO-GO

---

**Exemplo de ajuste pÃ³s-P9:**
```yaml
# ApÃ³s executar P9
pesquisa_validacao:
  amostra: 120 respondentes
  leads_L1: 45 famÃ­lias (38% da amostra)
  taxa_conversao: 60% (histÃ³rico)
  demanda_validada: 230 famÃ­lias # (45 Ã— 5 + ajuste conservador)

# Recalcular Fator 4:1
relacao_demanda_oferta_ajustada:
  demanda_validada: 230 # famÃ­lias (P9)
  oferta_total: 50 # unidades
  ratio_DO: 4.6 # (230 Ã· 50)
  validacao_P9: sim
  
  decisao: GO # âœ… Agora aprovado
  margem_seguranca: 15% # [(4.6-4)/4 Ã— 100]
```

---

### 9.3. EXEMPLO 3: NO-GO MESMO COM P9 (D:O = 2:1)

**Contexto:**
- **Projeto:** CondomÃ­nio Residencial Alegria
- **LocalizaÃ§Ã£o:** AlÃ©m ParaÃ­ba-MG
- **Produto:** 80 casas geminadas (3 quartos)
- **PreÃ§o mÃ©dio:** R$ 420.000/unidade
- **Data:** Abril/2024

---

**Inputs:**

**Demanda (P6 + P9):**
- PopulaÃ§Ã£o Ã¡rea influÃªncia: 28.000 habitantes
- FamÃ­lias totais: 7.800
- Renda â‰¥ R$ 12.000: 280 famÃ­lias (3,6%)
- Capacidade de compra validada (P9): **160 famÃ­lias**
- **Demanda validada: 160 famÃ­lias** (P9 executado)

**Oferta (P7):**
- Oferta Pulverizada: 15 casas (revenda)
- Oferta LanÃ§amentos: 45 casas (CondomÃ­nio Sol Nascente)
- Oferta TBC: 20 casas (projeto aprovado, lanÃ§amento em 6 meses)
- **Oferta total: 80 unidades**
- VSO mÃ©dio: **26 meses** (saturaÃ§Ã£o identificada)

---

**CÃ¡lculo:**
```yaml
relacao_demanda_oferta:
  demanda_potencial: 280 # famÃ­lias (P6)
  demanda_validada: 160 # famÃ­lias (P9) âš ï¸
  oferta_total: 80 # unidades
  
  ratio_DO: 2.0 # (160 Ã· 80)
  validacao_P9: sim # âœ… Pesquisa realizada
  
  decisao: NO-GO # âŒ
  margem_seguranca: -50% # [(2-4)/4 Ã— 100]
  
  semaforo: "ðŸ”´ VERMELHO"
  confianca: alta # (validado, mas resultado negativo)
```

**Margem de seguranÃ§a:**
```
Margem = (2 - 4) Ã· 4 Ã— 100% = -50% (NEGATIVA)
```

**InterpretaÃ§Ã£o:**
- D:O de **2:1** estÃ¡ **ABAIXO** do mÃ­nimo 4:1
- Margem de seguranÃ§a **NEGATIVA** (-50%) indica saturaÃ§Ã£o crÃ­tica
- **MESMO COM P9 VALIDADO**, projeto Ã© inviÃ¡vel

---

**DecisÃ£o:**
```
ðŸ”´ NO-GO (mercado saturado)

FUNDAMENTO:
- RelaÃ§Ã£o D:O de 2:1 estÃ¡ ABAIXO do critÃ©rio mÃ­nimo de 4:1
- MESMO com validaÃ§Ã£o P9 executada, demanda insuficiente
- Margem de seguranÃ§a negativa (-50%) indica saturaÃ§Ã£o crÃ­tica
- VSO concorrÃªncia alto (26 meses) confirma dificuldade de absorÃ§Ã£o

RISCO IDENTIFICADO:
- Oferta total (80 un) Ã© METADE da demanda validada (160 famÃ­lias)
- CenÃ¡rio: cada 2 famÃ­lias disputando 1 unidade NÃƒO Ã© suficiente
- AbsorÃ§Ã£o seria extremamente lenta (>60 meses)
- ROE projetado <10% a.a. (inviÃ¡vel)
```

---

**Por que P9 nÃ£o salvou o projeto?**
1. **Demanda validada (160) < Demanda potencial (280):** Pesquisa confirmou superestimaÃ§Ã£o
2. **Oferta TBC crÃ­tica:** 20 unidades em pipeline (25% da oferta) nÃ£o foram consideradas inicialmente
3. **VSO alto (26 meses):** Mercado jÃ¡ demonstra dificuldade de absorÃ§Ã£o
4. **Fator 4:1 nÃ£o flexÃ­vel:** Mesmo com P9, D:O < 4:1 Ã© inviÃ¡vel

---

**RecomendaÃ§Ã£o:**
```
âŒ REPROVAR PROJETO

ALTERNATIVAS:
1. Reduzir escopo: de 80 para 40 casas (D:O = 4:1)
2. Mudar produto: apartamentos menor valor (demanda maior)
3. Aguardar absorÃ§Ã£o: postergar lanÃ§amento em 18-24 meses
4. Mudar localizaÃ§Ã£o: buscar microrregiÃ£o com demanda > 320 famÃ­lias

IMPORTANTE:
- NÃƒO prosseguir para P8 (AbsorÃ§Ã£o) ou P10 (FCD)
- Documentar liÃ§Ã£o aprendida: P9 valida premissas, mas nÃ£o cria demanda
```

---

**LiÃ§Ã£o:**
> "P9 valida premissas, mas nÃ£o cria demanda. Fator 4:1 Ã© inegociÃ¡vel â€” se D:O < 4:1 (mesmo com P9), projeto Ã© inviÃ¡vel."

---

## 10. CHECKLIST DE QUALIDADE

### 10.1. Auto-ValidaÃ§Ã£o da Skill

- [ ] **Estrutura:** 10 seÃ§Ãµes completas?
- [ ] **YAML:** Frontmatter sem acentuaÃ§Ã£o, <200 chars?
- [ ] **FÃ³rmula D:O:** Claramente documentada?
- [ ] **Matriz de decisÃ£o:** 7 cenÃ¡rios cobertos?
- [ ] **SemÃ¡foro:** Emoji visual incluÃ­do?
- [ ] **Exemplos:** 3 casos prÃ¡ticos (GO, HOLD, NO-GO)?
- [ ] **IntegraÃ§Ã£o:** Handshakes P6, P7, P8, P9, P10 formalizados?
- [ ] **CitaÃ§Ã£o KB:** ReferÃªncia ao Fator 4:1 incluÃ­da?
- [ ] **Templates:** Output YAML estruturado?
- [ ] **Red flags:** Alertas crÃ­ticos listados?

---

### 10.2. Conformidade KB v5.0

- [ ] **PrincÃ­pio 4:1:** Formalizado e aplicado?
- [ ] **PrincÃ­pio 10:1:** Para casos sem P9 documentado?
- [ ] **Conservadorismo:** Margem de seguranÃ§a calculada?
- [ ] **ValidaÃ§Ã£o P9:** IntegraÃ§Ã£o formalizada?
- [ ] **ROE:** RelaÃ§Ã£o D:O â†’ Velocidade â†’ ROE explicada?
- [ ] **CitaÃ§Ãµes:** KB CORE v5.0 referenciado?

---

### 10.3. Usabilidade

- [ ] **Clareza:** Linguagem tÃ©cnica mas acessÃ­vel?
- [ ] **Praticidade:** CÃ¡lculo executÃ¡vel em <60 min?
- [ ] **Rastreabilidade:** Templates permitem auditoria?
- [ ] **Exemplos:** Casos reais (regiÃ£o Leopoldina) incluÃ­dos?
- [ ] **Alertas:** Red flags e chutes caros listados?
- [ ] **DecisÃ£o:** SemÃ¡foro visual facilita interpretaÃ§Ã£o?

---

### 10.4. Checklist Final de Entrega

- [ ] Arquivo SKILL.md criado
- [ ] 10 seÃ§Ãµes estruturadas
- [ ] FÃ³rmula D:O documentada
- [ ] Matriz de decisÃ£o completa (7 cenÃ¡rios)
- [ ] SemÃ¡foro visual (emoji) implementado
- [ ] Templates YAML de output
- [ ] 3 exemplos prÃ¡ticos documentados
- [ ] IntegraÃ§Ã£o P6â†”P7â†”P8â†”P9â†”P10 formalizada
- [ ] Checklist de validaÃ§Ãµes obrigatÃ³rias
- [ ] Conformidade KB CORE v5.0 atestada

---

**FIM DA SKILL tiv-fator-4para1**

**VersÃ£o:** 1.0  
**Base:** KB CORE v5.0  
**Tipo:** Nova (TIER 1)  
**Data:** 14/11/2025  
**Status:** âœ… OPERACIONAL
