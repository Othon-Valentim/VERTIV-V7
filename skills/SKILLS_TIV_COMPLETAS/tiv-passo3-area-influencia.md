---
name: "tiv-passo3-area-influencia"
version: "1.0"
description: "DelimitaÃ§Ã£o geogrÃ¡fica precisa da Ã¡rea de influÃªncia do empreendimento usando isÃ³cronas (tempo de deslocamento) ao invÃ©s de raios arbitrÃ¡rios. Define de onde virÃ£o os compradores reais."
author: "Claude + Othon"
created: "2025-11-12"
updated: "2025-11-12"
tags: ["tiv", "imobiliario", "area-influencia", "mobilidade", "isochronas", "h3"]
priority: "CRÃTICO"
tier: "TIER 1"
passo_tiv: 3
---

# SKILL: TIV - PASSO 3: ÃREA DE INFLUÃŠNCIA

## 1. OBJETIVO E CONTEXTO

### 1.1. Objetivo Central

Delimitar **geograficamente de onde vÃªm os compradores reais** com base em **tempo de deslocamento** (isÃ³cronas), mobilidade urbana e fluxos intermunicipais, produzindo **polÃ­gonos operacionais** para anÃ¡lise de demanda (Passo 6), oferta (Passo 7) e absorÃ§Ã£o (Passo 8).

### 1.2. Problema que Resolve

**âŒ MÃ‰TODO TRADICIONAL (ERRADO):**
```
Raio arbitrÃ¡rio de 1km, 2km, 3km
â†’ Ignora barreiras fÃ­sicas (rios, morros, rodovias)
â†’ Ignora tempo real de deslocamento
â†’ Ignora mobilidade urbana (pico/vale)
â†’ Superestima/subestima demanda potencial
```

**âœ… MÃ‰TODO TIV (CORRETO):**
```
IsÃ³cronas de 5/10/15 minutos (mobilidade real)
â†’ Considera barreiras fÃ­sicas e viÃ¡rias
â†’ Simula pico de trÃ¢nsito (ex: 18h30)
â†’ Inclui transporte pÃºblico quando relevante
â†’ Mapeia de onde os compradores REALMENTE vÃªm
```

### 1.3. PrincÃ­pio MetodolÃ³gico

> **"Ãrea de influÃªncia Ã© definida por TEMPO, nÃ£o por DISTÃ‚NCIA. Compradores pensam em 'quantos minutos atÃ© o trabalho', nÃ£o 'quantos quilÃ´metros'."**  
> â€” Othon Valentim, TIV 4.0

### 1.4. Posicionamento na Metodologia TIV

**SequÃªncia dos 10 Passos:**
```
Passo 1: Garimpo (triagem rÃ¡pida)
Passo 2: DinÃ¢mica EconÃ´mica (P2i-Lead)
â†’ PASSO 3: ÃREA DE INFLUÃŠNCIA (polÃ­gono operacional) â† VOCÃŠ ESTÃ AQUI
Passo 4: VocaÃ§Ã£o ImobiliÃ¡ria (produto ideal)
Passo 5: Legal/Zoneamento (viabilidade tÃ©cnica)
Passo 6: Demanda (quantificaÃ§Ã£o pÃºblico-alvo)
...
```

**Criticidade:** Sem Ã¡rea de influÃªncia bem definida, TODO o resto da anÃ¡lise fica comprometido:
- Demanda superestimada (Ã¡rea muito grande)
- Oferta subavaliada (concorrentes fora do radar)
- AbsorÃ§Ã£o otimista (pÃºblico fictÃ­cio)

---

## 2. QUANDO ACIONAR

### 2.1. Triggers AutomÃ¡ticos

Claude deve acionar esta Skill quando o usuÃ¡rio mencionar:

âœ… "Ã¡rea de influÃªncia"  
âœ… "de onde vÃªm os compradores"  
âœ… "polÃ­gono de demanda"  
âœ… "raio de anÃ¡lise" (para CORRIGIR abordagem)  
âœ… "isÃ³cronas" ou "tempo de deslocamento"  
âœ… "mobilidade urbana"  
âœ… "Passo 3 TIV"  
âœ… "delimitar mercado geogrÃ¡fico"  

### 2.2. PrÃ©-condiÃ§Ãµes ObrigatÃ³rias (DoR - Definition of Ready)

**NÃƒO AVANÃ‡AR sem ter concluÃ­do:**

**1. Passo 1: Garimpo**
- [ ] Terreno identificado e geolocalizado
- [ ] Coordenadas GPS (lat/long) disponÃ­veis
- [ ] OU Ã¡rea-alvo sem terreno especÃ­fico definida

**2. Passo 2: DinÃ¢mica EconÃ´mica (P2i-Lead)**
- [ ] AnÃ¡lise econÃ´mica completa do municÃ­pio
- [ ] PopulaÃ§Ã£o total conhecida
- [ ] DistribuiÃ§Ã£o de renda mapeada (Faixas A-E)
- [ ] Leading indicators avaliados

**3. Base ViÃ¡ria e Mobilidade**
- [ ] Perfil de pico local identificado (ex: 18h30)
- [ ] Principais vias de acesso conhecidas
- [ ] Barreiras fÃ­sicas mapeadas (rios, morros, ferrovias)

**âš ï¸ Se prÃ©-requisitos incompletos:**
```
âŒ NÃƒO PROSSEGUIR com Passo 3
âœ… VOLTAR para completar Passos 1-2
```

### 2.3. Quando NÃƒO Acionar

âŒ **AnÃ¡lise preliminar rÃ¡pida** (use Passo 1 - Garimpo)  
âŒ **Sem coordenadas do terreno/Ã¡rea-alvo**  
âŒ **Sem dados demogrÃ¡ficos da regiÃ£o** (complete Passo 2 primeiro)  
âŒ **Estudo acadÃªmico/teÃ³rico** (TIV Ã© metodologia operacional)  

---

## 3. FRAMEWORK/METODOLOGIA

### 3.1. MÃ©todo: IsÃ³cronas por Mobilidade Real

#### Passo a Passo Operacional:

**ETAPA 1: SimulaÃ§Ã£o de Mobilidade (Carro)**

1. **Definir ponto de origem:**
   - LocalizaÃ§Ã£o exata do terreno (lat/long)
   - OU centroide da Ã¡rea-alvo se "sem terreno"

2. **Configurar simulaÃ§Ã£o:**
   - Modal: CARRO (prioritÃ¡rio no Brasil)
   - HorÃ¡rio: PICO LOCAL (ex: 18h30 em Leopoldina-MG)
   - Tempos: 5 / 10 / 15 minutos
   - Ferramenta: Google Maps API / Mapbox / OSRM

3. **Gerar isÃ³cronas:**
   ```
   IsÃ³crona 5 min  â†’ Ãrea PRIMÃRIA (50-70% demanda)
   IsÃ³crona 10 min â†’ Ãrea SECUNDÃRIA (20-30% demanda)
   IsÃ³crona 15 min â†’ Ãrea TERCIÃRIA (10-20% demanda)
   ```

4. **Validar barreiras:**
   - Rios sem pontes
   - Morros/serras
   - Rodovias sem retorno
   - Linhas fÃ©rreas ativas

**ETAPA 2: Transporte PÃºblico (quando relevante)**

**Quando incluir TP:**
- Linha estruturante (metrÃ´, BRT, corredor Ã´nibus)
- FrequÃªncia alta (< 15 min intervalo)
- IntegraÃ§Ã£o tarifÃ¡ria
- PopulaÃ§Ã£o de baixa renda (Faixas D-E)

**Como mapear:**
1. Identificar linhas que passam prÃ³ximas ao terreno
2. Buffer de 500m ao redor de TODAS as estaÃ§Ãµes da linha
3. Interseccionar buffer com isÃ³cronas de carro
4. **AAI ampliada = IsÃ³cronas + Buffers TP**

**ETAPA 3: ConurbaÃ§Ãµes (Ã¡reas contÃ­guas)**

**DefiniÃ§Ã£o:** MunicÃ­pios que "se tocam" urbanamente

**Como identificar:**
- Malha urbana contÃ­nua (sem zona rural entre cidades)
- Fluxo pendular significativo (> 5% populaÃ§Ã£o)
- Exemplo: RegiÃ£o Metropolitana de SÃ£o LuÃ­s (SÃ£o LuÃ­s + PaÃ§o do Lumiar + SÃ£o JosÃ© de Ribamar + Raposa)

**Como processar:**
1. Interseccionar isÃ³cronas com polÃ­gonos municipais
2. Agregar dados demogrÃ¡ficos multi-municÃ­pio
3. Validar com MIGRANTE DATA FIXA (IBGE)

**ETAPA 4: Granularidade H3 (Uber Hexagons)**

**Por que H3 > Setores CensitÃ¡rios:**
- ResoluÃ§Ã£o H8: ~60m (precisÃ£o de quarteirÃ£o)
- ResoluÃ§Ã£o H9: ~20m (precisÃ£o de lote)
- Independente de limites administrativos
- AgregaÃ§Ã£o matemÃ¡tica perfeita

**Como aplicar:**
1. Converter isÃ³cronas (GeoJSON) para grade H3
2. Interseccionar hexÃ¡gonos com isÃ³cronas
3. Atribuir populaÃ§Ã£o/renda por hexÃ¡gono
4. Consolidar por anel (5/10/15 min)

**Ferramenta:** H3 Python Library (Uber) ou Kepler.gl

---

### 3.2. Fluxos e MigraÃ§Ã£o (Insumo CrÃ­tico)

#### 3.2.1. PopulaÃ§Ã£o Flutuante (Pendular)

**Conceito:** Pessoas que trabalham/estudam na regiÃ£o mas moram em outro municÃ­pio

**Fonte de dados:**
- IBGE: Movimento Pendular (Censo 2010 / 2022)
- Foco: Faixa etÃ¡ria 20-49 anos (economicamente ativa)

**AnÃ¡lise crÃ­tica:**
```
Pergunta-chave: Por que essas pessoas NÃƒO moram aqui?

HipÃ³teses:
1. PreÃ§o dos imÃ³veis muito alto (barreira de entrada)
   â†’ Oportunidade para produto mais acessÃ­vel

2. Oferta inadequada (sÃ³ alto padrÃ£o, falta econÃ´mico)
   â†’ Oportunidade para segmento carente

3. PreferÃªncia pessoal (famÃ­lia, raÃ­zes)
   â†’ RetenÃ§Ã£o improvÃ¡vel

ValidaÃ§Ã£o: Pesquisa qualitativa + MIGRANTE DATA FIXA
```

**Exemplo empÃ­rico (Apostila TIV):**

```
Empreendimento: SÃ£o LuÃ­s - MA
Movimento Pendular (destino SÃ£o LuÃ­s):
- PaÃ§o do Lumiar: 21.714 pessoas (20-49 anos)
- SÃ£o JosÃ© do Ribamar: 16.366 pessoas
- Raposa: 1.595 pessoas

TOTAL PENDULAR: 39.675 pessoas/dia

Potencial de retenÃ§Ã£o: 5-15% (conservador)
â†’ Demanda adicional: ~2.000-6.000 famÃ­lias
```

#### 3.2.2. MigraÃ§Ã£o Efetiva

**Conceito:** Pessoas que DE FATO mudaram de municÃ­pio

**Fonte:** MIGRANTE DATA FIXA (IBGE Censo)
- Mostra quem residia em municÃ­pio X em data fixa anterior
- E mudou para municÃ­pio Y no perÃ­odo intercensitÃ¡rio

**ImportÃ¢ncia:**
> "Valida a cultura de migraÃ§Ã£o entre cidades prÃ³ximas. Sem migraÃ§Ã£o histÃ³rica, nÃ£o hÃ¡ demanda pendular convertÃ­vel."

**Como usar:**
1. Verificar fluxo origem â†’ destino (ex: Leopoldina â†’ Cataguases)
2. Quantificar magnitude (nÂº pessoas/ano)
3. Se fluxo > 0 = cultura de migraÃ§Ã£o existe
4. Se fluxo â‰ˆ 0 = barreira cultural/econÃ´mica

**Exemplo:**
```
Leopoldina â†’ Cataguases: 120 pessoas/dÃ©cada (Censo 2010)
â†’ Fluxo BAIXO = resistÃªncia Ã  mudanÃ§a
â†’ RetenÃ§Ã£o pendular IMPROVÃVEL
â†’ Ajustar premissa de demanda

SÃ£o JosÃ© de Ribamar â†’ SÃ£o LuÃ­s: 3.500 pessoas/dÃ©cada
â†’ Fluxo ALTO = cultura de migraÃ§Ã£o estabelecida
â†’ RetenÃ§Ã£o pendular VIÃVEL (produto adequado)
â†’ Aumentar premissa de demanda
```

---

### 3.3. ParticipaÃ§Ã£o Esperada por Anel (Regra de Bolso)

**DistribuiÃ§Ã£o padrÃ£o TIV:**

| Anel | Tempo Deslocamento | % Demanda Esperado | Ajuste por Caso |
|------|-------------------|-------------------|----------------|
| **PrimÃ¡rio** | 5 min carro | 50-70% | Usar 60% (conservador) |
| **SecundÃ¡rio** | 10 min carro | 20-30% | Usar 25% (conservador) |
| **TerciÃ¡rio** | 15 min carro | 10-20% | Usar 15% (conservador) |

**âš ï¸ CRÃTICO:** NÃ£o fixar percentuais Ãºnicos (ex: 60/30/10) sem calibraÃ§Ã£o ao caso

**Fatores que aumentam participaÃ§Ã£o do anel primÃ¡rio:**
- Transporte pÃºblico fraco â†’ dependÃªncia carro pessoal
- TrÃ¢nsito congestionado â†’ sensibilidade ao tempo
- Produto de conveniÃªncia (supermercado, farmÃ¡cia)
- Renda baixa (Faixa D-E) â†’ menor mobilidade

**Fatores que aumentam anÃ©is secundÃ¡rio/terciÃ¡rio:**
- Transporte pÃºblico forte (metrÃ´/BRT)
- Ã‚ncoras extraordinÃ¡rias (shopping Ãºnico na regiÃ£o)
- Produto aspiracional (alto padrÃ£o)
- Renda alta (Faixa A-B) â†’ maior mobilidade

---

### 3.4. TÃ¡tica de ValidaÃ§Ã£o RÃ¡pida (Guerrilha)

**MÃ©todo:** Entrevistas curtas com taxistas/motoristas experientes

**Por que funciona:**
- Conhecimento empÃ­rico de dÃ©cadas
- PercepÃ§Ã£o de gargalos e fluxos
- InformaÃ§Ã£o gratuita e rÃ¡pida

**Roteiro de entrevista (5-10 min):**

```
1. Qual o pior horÃ¡rio de trÃ¢nsito aqui? (validar pico)

2. De onde vem a maioria das pessoas que vocÃª transporta
   para [regiÃ£o do terreno]? (origem-destino)

3. Tem alguma via que vocÃª sempre evita? Por quÃª?
   (identificar barreiras)

4. Se alguÃ©m quisesse morar perto de [Ã¢ncora X],
   quais bairros vocÃª recomendaria? (percepÃ§Ã£o de valor)

5. Mudou muito nos Ãºltimos 5 anos? O que mudou?
   (dinÃ¢mica de ocupaÃ§Ã£o)
```

**Onde fazer:**
- Pontos de tÃ¡xi prÃ³ximos ao terreno
- HorÃ¡rio: 17h-19h (pico de movimento)
- Quantidade: 3-5 motoristas (triangular informaÃ§Ãµes)

**Output:** Insights qualitativos para calibrar isÃ³cronas

---

## 4. INPUTS NECESSÃRIOS

### 4.1. Inputs ObrigatÃ³rios

**1. Dados do Terreno/Ãrea-Alvo**
```yaml
localizacao:
  tipo: [Com Terreno / Sem Terreno]
  coordenadas: [lat, long]
  endereco: "Rua/Av X, NÂº Y, Bairro Z"
  municipio: "Leopoldina-MG"
  referencia: "PrÃ³ximo a [Ã¢ncora conhecida]"
```

**2. ConfiguraÃ§Ã£o de Mobilidade**
```yaml
mobilidade:
  pico_horario: "18:30"  # HorÃ¡rio de maior congestionamento
  modal_prioritario: "carro"
  tempos_analise: [5, 10, 15]  # minutos
  dia_semana: "Quinta-feira tÃ­pica"  # Evitar seg/sex
```

**3. Dados DemogrÃ¡ficos (do Passo 2)**
```yaml
demografia:
  populacao_total: 52565  # Leopoldina-MG (IBGE 2022)
  distribuicao_renda:
    faixa_A: 2%
    faixa_B: 8%
    faixa_C: 35%
    faixa_D: 40%
    faixa_E: 15%
  fonte: "IBGE Censo 2022 / Atlas Brasil"
```

**4. Infraestrutura de Transporte**
```yaml
transporte:
  transporte_publico:
    ativo: false  # Leopoldina nÃ£o tem sistema estruturante
    linhas: []
  barreiras_fisicas:
    - tipo: "Rio Pomba"
      atravessavel: true
      pontos_travessia: ["Ponte da Av. GetÃºlio Vargas"]
    - tipo: "Linha fÃ©rrea"
      atravessavel: true
      passagens_nivel: 3
```

**5. ConurbaÃ§Ãµes (se aplicÃ¡vel)**
```yaml
conurbacoes:
  ativo: false  # Leopoldina Ã© municÃ­pio isolado
  municipios_conurbados: []
```

---

### 4.2. Inputs Opcionais (Refinamento)

**1. Movimento Pendular**
```yaml
pendularidade:
  trabalho:
    entrada: 120  # Pessoas que vÃªm trabalhar em Leopoldina
    saida: 300    # Leopoldinos que trabalham fora
  estudo:
    entrada: 450  # Estudantes de outras cidades (UNIFAL)
    saida: 180    # Leopoldinos que estudam fora
  fonte: "IBGE Movimento Pendular 2010"
```

**2. Migrante Data Fixa**
```yaml
migracao:
  periodo: "2000-2010"
  fluxo_entrada:
    - origem: "Cataguases"
      quantidade: 45
    - origem: "AlÃ©m ParaÃ­ba"
      quantidade: 32
  fluxo_saida:
    - destino: "Juiz de Fora"
      quantidade: 210
    - destino: "Rio de Janeiro"
      quantidade: 180
  saldo_migratorio: -313  # Negativo = evasÃ£o lÃ­quida
```

---

## 5. PROCESSO DE ANÃLISE

### 5.1. Workflow Completo

```
INÃCIO
  â†“
[1] Validar PrÃ©-Requisitos
  â†“
  Terreno geolocalizado? â†’ NÃƒO â†’ BLOQUEAR (exigir coordenadas)
  â†“ SIM
  Passo 2 concluÃ­do? â†’ NÃƒO â†’ BLOQUEAR (exigir dinÃ¢mica econÃ´mica)
  â†“ SIM
[2] Configurar SimulaÃ§Ã£o de Mobilidade
  â†“
  - Pico horÃ¡rio local (ex: 18h30)
  - Modal: Carro (padrÃ£o Brasil)
  - Tempos: 5/10/15 min
  â†“
[3] Gerar IsÃ³cronas (Google Maps API / Mapbox)
  â†“
  Output: GeoJSON de 3 polÃ­gonos
  â†“
[4] Transporte PÃºblico?
  â†“
  Sistema estruturante? â†’ SIM â†’ Buffer 500m estaÃ§Ãµes
  â†“ NÃƒO              â†“
  Pular etapa    Interseccionar com isÃ³cronas
  â†“                  â†“
[5] ConurbaÃ§Ãµes?
  â†“
  Ãrea contÃ­gua? â†’ SIM â†’ Agregar dados multi-municÃ­pio
  â†“ NÃƒO          â†“
  Pular etapa    Validar com Migrante Data Fixa
  â†“                  â†“
[6] Aplicar Grade H3
  â†“
  - ResoluÃ§Ã£o: H8 (60m) ou H9 (20m)
  - Interseccionar com isÃ³cronas
  - Atribuir pop/renda por hexÃ¡gono
  â†“
[7] Consolidar Dados por Anel
  â†“
  Anel 5 min:  X habitantes | Y renda mÃ©dia
  Anel 10 min: X habitantes | Y renda mÃ©dia
  Anel 15 min: X habitantes | Y renda mÃ©dia
  â†“
[8] Analisar Pendularidade/MigraÃ§Ã£o
  â†“
  - Movimento pendular > 5%? â†’ Potencial de retenÃ§Ã£o
  - Migrante Data Fixa > 0? â†’ Cultura de migraÃ§Ã£o
  â†“
[9] Calibrar ParticipaÃ§Ãµes (50-70 / 20-30 / 10-20)
  â†“
  Fatores ajuste:
  - Transporte pÃºblico forte? â†’ Aumentar anÃ©is externos
  - TrÃ¢nsito congestionado? â†’ Concentrar anel primÃ¡rio
  - Ã‚ncoras extraordinÃ¡rias? â†’ Aumentar anÃ©is externos
  â†“
[10] ValidaÃ§Ã£o Qualitativa (Taxistas)
  â†“
  - Confirmar gargalos
  - Validar origem-destino
  - Ajustar isÃ³cronas se necessÃ¡rio
  â†“
[11] Gerar EntregÃ¡veis
  â†“
FIM
```

---

### 5.2. Detalhamento das Etapas CrÃ­ticas

#### Etapa [3]: Gerar IsÃ³cronas

**Ferramentas recomendadas:**

1. **Google Maps Platform (pago, preciso)**
   - Distance Matrix API
   - Directions API com departure_time
   - Formato output: GeoJSON

2. **Mapbox (pago, flexÃ­vel)**
   - Isochrone API
   - CustomizaÃ§Ã£o visual avanÃ§ada

3. **OSRM (gratuito, open-source)**
   - Menos preciso em trÃ¢nsito
   - Ã“timo para prototipagem

**ConfiguraÃ§Ã£o recomendada:**
```python
# Exemplo conceitual (Python + Google Maps API)
import googlemaps
from datetime import datetime, timedelta

gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Ponto de origem (terreno)
origem = (-21.5333, -42.6417)  # Leopoldina-MG centro

# HorÃ¡rio de pico
pico = datetime.now().replace(hour=18, minute=30)

# Gerar isÃ³crona 5 min
isocrona_5min = gmaps.distance_matrix(
    origins=[origem],
    destinations=grid_pontos_ao_redor,  # Grade de 100+ pontos
    mode="driving",
    departure_time=pico
)

# Filtrar pontos alcanÃ§Ã¡veis em <= 5 min
# Criar polÃ­gono convexo (convex hull)
# Exportar GeoJSON
```

**Output esperado:**
- 3 arquivos GeoJSON (5min, 10min, 15min)
- Metadados: horÃ¡rio simulaÃ§Ã£o, nÂº pontos, fonte dados

---

#### Etapa [6]: Aplicar Grade H3

**Por que H3:**
- Ãndice espacial hierÃ¡rquico
- AgregaÃ§Ã£o matemÃ¡tica perfeita (sem lacunas/sobreposiÃ§Ãµes)
- ResoluÃ§Ã£o variÃ¡vel (mundo todo com mesma estrutura)

**ResoluÃ§Ãµes recomendadas:**

| ResoluÃ§Ã£o | Ãrea Aprox | Uso TIV |
|-----------|-----------|---------|
| H7 | 5 kmÂ² | AnÃ¡lise regional (conurbaÃ§Ãµes) |
| **H8** | **0.7 kmÂ²** | **PadrÃ£o TIV (quarteirÃ£o)** |
| **H9** | **0.1 kmÂ²** | **Alta precisÃ£o (lote)** |
| H10 | 0.015 kmÂ² | MicrolocalizaÃ§Ã£o (excesso) |

**Como aplicar:**
```python
import h3
import geopandas as gpd

# Carregar isÃ³crona 5 min (GeoJSON)
isocrona = gpd.read_file("isocrona_5min.geojson")

# Gerar hexÃ¡gonos H8 que intersectam isÃ³crona
hexagonos = h3.polyfill(
    isocrona.geometry[0].__geo_interface__,
    res=8,  # ResoluÃ§Ã£o H8
    geo_json_conformant=True
)

# Atribuir populaÃ§Ã£o/renda por hexÃ¡gono
# (cruzar com dados IBGE setores censitÃ¡rios)

# Output: hexagonos_5min_populacao.csv
```

**Dado esperado:**
```csv
h3_index,populacao,renda_media,faixa_predominante
888e1c4a9ffffff,450,3500,C
888e1c4b1ffffff,380,2800,D
888e1c4b9ffffff,520,4200,B
...
```

---

#### Etapa [8]: Analisar Pendularidade/MigraÃ§Ã£o

**Framework de InterpretaÃ§Ã£o:**

| Movimento Pendular | Migrante Data Fixa | InterpretaÃ§Ã£o TIV |
|-------------------|-------------------|------------------|
| ALTO (>10% pop) | ALTO (>100 pess/dÃ©cada) | âœ… **Demanda retenÃ­vel forte** |
| ALTO | BAIXO (<50) | âš ï¸ **Barreira cultural/preÃ§o** |
| BAIXO (<5%) | ALTO | âš ï¸ **MigraÃ§Ã£o de saÃ­da (fuga)** |
| BAIXO | BAIXO | âŒ **Mercado isolado/estagnado** |

**AÃ§Ã£o por cenÃ¡rio:**

**CenÃ¡rio 1: Alto Pendular + Alta MigraÃ§Ã£o**
```
DiagnÃ³stico: Mercado dinÃ¢mico, fluxo bidirecional
AÃ§Ã£o: Aumentar premissa de demanda (+20-30%)
Foco: Produto acessÃ­vel para reter pendular
```

**CenÃ¡rio 2: Alto Pendular + Baixa MigraÃ§Ã£o**
```
DiagnÃ³stico: Barreira de entrada (preÃ§o/oferta)
AÃ§Ã£o: Investigar por que nÃ£o migram
Foco: Produto que rompa barreira (preÃ§o ou tipologia)
Risco: Pode ser preferÃªncia pessoal (nÃ£o econÃ´mica)
```

**CenÃ¡rio 3: Baixo Pendular + Alta MigraÃ§Ã£o**
```
DiagnÃ³stico: EvasÃ£o lÃ­quida (oportunidade em outras cidades)
AÃ§Ã£o: Reduzir premissa de demanda (-20-30%)
Risco: DinÃ¢mica econÃ´mica fraca (revisitar Passo 2)
```

**CenÃ¡rio 4: Baixo Pendular + Baixa MigraÃ§Ã£o**
```
DiagnÃ³stico: Mercado isolado/autossuficiente
AÃ§Ã£o: Demanda local apenas (ignorar fluxos externos)
Foco: Produto para moradores existentes (upgrade)
```

---

## 6. OUTPUTS ESPERADOS

### 6.1. EntregÃ¡veis ObrigatÃ³rios

**1. PolÃ­gonos GeoJSON (3 arquivos)**
```
/outputs/area_influencia/
  â”œâ”€â”€ isocrona_5min_primaria.geojson
  â”œâ”€â”€ isocrona_10min_secundaria.geojson
  â””â”€â”€ isocrona_15min_terciaria.geojson
```

**Metadados em cada arquivo:**
```json
{
  "properties": {
    "nome": "Ãrea PrimÃ¡ria - 5 minutos",
    "tempo_min": 5,
    "modal": "carro",
    "horario_simulacao": "18:30",
    "data_geracao": "2025-11-12",
    "area_km2": 2.34,
    "municipios": ["Leopoldina"]
  },
  "geometry": { ... }
}
```

**2. Grade H3 com PopulaÃ§Ã£o/Renda (CSV)**
```csv
h3_index,anel,populacao,renda_media,faixa_predominante,densidade_hab_km2
888e1c4a9ffffff,5min,450,3500,C,6428
888e1c4b1ffffff,5min,380,2800,D,5428
888e1c4c3ffffff,10min,290,4100,B,4142
...
```

**3. Tabela Consolidada por Anel**
```csv
anel,tempo_min,area_km2,populacao_total,renda_media,participacao_esperada
PrimÃ¡rio,5,2.34,8450,3200,60%
SecundÃ¡rio,10,6.78,15200,3800,25%
TerciÃ¡rio,15,12.45,22100,3400,15%
```

**4. Mapa de ConurbaÃ§Ã£o (se aplicÃ¡vel)**
- Formato: PNG ou PDF (A3)
- Elementos:
  - PolÃ­gonos isÃ³cronas coloridos
  - Limites municipais
  - Principais vias
  - LocalizaÃ§Ã£o do terreno (pin)
  - Legenda com tempos

**5. Nota MetodolÃ³gica (Markdown)**

```markdown
# Ãrea de InfluÃªncia - [Nome do Projeto]

## ConfiguraÃ§Ã£o da SimulaÃ§Ã£o
- **Data:** 12/11/2025
- **HorÃ¡rio pico:** 18h30 (quinta-feira tÃ­pica)
- **Modal:** Carro (padrÃ£o Brasil)
- **Tempos:** 5/10/15 minutos
- **Ferramenta:** Google Maps Distance Matrix API

## Premissas
- TrÃ¢nsito: CondiÃ§Ã£o tÃ­pica de dia Ãºtil
- Barreiras fÃ­sicas: Rio Pomba (1 ponte principal)
- Transporte pÃºblico: NÃ£o incluÃ­do (sistema nÃ£o estruturante)

## ParticipaÃ§Ãµes Esperadas
| Anel | % Demanda | Justificativa |
|------|-----------|--------------|
| 5min | 60% | TrÃ¢nsito moderado, dependÃªncia carro |
| 10min | 25% | Barreira natural (rio) reduz mobilidade |
| 15min | 15% | Limite de aceitaÃ§Ã£o deslocamento diÃ¡rio |

## Riscos Identificados
- âš ï¸ Ponte Ãºnica sobre Rio Pomba = gargalo crÃ­tico
- âš ï¸ ExpansÃ£o urbana para oeste = isÃ³crona pode mudar em 3-5 anos
```

**6. Tabela de Quotas Preliminares (Passo 6)**
```csv
subarea,h3_index,faixa_renda,faixa_idade,populacao,quota_sugerida
Primario_Norte,888e1c4a9ffffff,C,25-35,450,23
Primario_Sul,888e1c4b1ffffff,D,30-40,380,19
Secundario_Leste,888e1c4c3ffffff,B,35-45,290,15
...
```

**Uso:** Input direto para dimensionamento de amostra de pesquisa (Passo 6)

---

### 6.2. Formato de ApresentaÃ§Ã£o (SumÃ¡rio Executivo)

**Template padrÃ£o:**

```markdown
# PASSO 3: ÃREA DE INFLUÃŠNCIA
## [Nome do Projeto] - Leopoldina-MG

---

### ðŸŽ¯ SÃNTESE EXECUTIVA

**PolÃ­gono de influÃªncia delimitado:** 21,57 kmÂ²  
**PopulaÃ§Ã£o total abrangida:** 45.750 habitantes  
**Renda mÃ©dia ponderada:** R$ 3.450/familiar  
**Faixa predominante:** C (35%) e D (40%)  

**ParticipaÃ§Ãµes calibradas:**
- Anel 5 min: **60%** (27.450 habitantes)
- Anel 10 min: **25%** (11.437 habitantes)
- Anel 15 min: **15%** (6.863 habitantes)

---

### ðŸ“ CONFIGURAÃ‡ÃƒO

| ParÃ¢metro | Valor |
|-----------|-------|
| Ponto de origem | Av. dos Andradas, 1500 - Centro |
| Modal prioritÃ¡rio | Carro |
| HorÃ¡rio pico simulado | 18h30 |
| Dia tÃ­pico | Quinta-feira |
| Ferramenta | Google Maps API |
| Data simulaÃ§Ã£o | 12/11/2025 |

---

### ðŸ—ºï¸ CARACTERÃSTICAS GEOGRÃFICAS

**Barreiras fÃ­sicas identificadas:**
- Rio Pomba (travessia: Ponte GetÃºlio Vargas)
- Linha fÃ©rrea EFCB (3 passagens de nÃ­vel)

**ConurbaÃ§Ãµes:** NÃ£o aplicÃ¡vel (municÃ­pio isolado)

**Transporte pÃºblico:** NÃ£o incluÃ­do (sistema local sem estruturaÃ§Ã£o)

---

### ðŸ“Š DADOS DEMOGRÃFICOS POR ANEL

#### Anel PrimÃ¡rio (5 min)
- Ãrea: 2,34 kmÂ²
- PopulaÃ§Ã£o: 27.450 hab
- Densidade: 11.730 hab/kmÂ²
- Renda mÃ©dia: R$ 3.200
- DistribuiÃ§Ã£o: 40% Faixa C, 35% Faixa D

#### Anel SecundÃ¡rio (10 min)
- Ãrea: 6,78 kmÂ²
- PopulaÃ§Ã£o: 11.437 hab
- Densidade: 1.686 hab/kmÂ²
- Renda mÃ©dia: R$ 3.800
- DistribuiÃ§Ã£o: 45% Faixa C, 30% Faixa B

#### Anel TerciÃ¡rio (15 min)
- Ãrea: 12,45 kmÂ²
- PopulaÃ§Ã£o: 6.863 hab
- Densidade: 551 hab/kmÂ²
- Renda mÃ©dia: R$ 3.400
- DistribuiÃ§Ã£o: 38% Faixa C, 35% Faixa D

---

### ðŸ”„ FLUXOS POPULACIONAIS

**Movimento Pendular (IBGE 2010):**
- Entrada para trabalho: 120 pessoas/dia
- SaÃ­da para trabalho: 300 pessoas/dia
- Saldo: -180 (evasÃ£o lÃ­quida)

**Migrante Data Fixa (2000-2010):**
- ImigraÃ§Ã£o: 77 pessoas/dÃ©cada
- EmigraÃ§Ã£o: 390 pessoas/dÃ©cada
- Saldo: -313 (evasÃ£o lÃ­quida)

**InterpretaÃ§Ã£o TIV:**
âš ï¸ CenÃ¡rio 3 (Baixo Pendular + Alta EmigraÃ§Ã£o)
- DinÃ¢mica de fuga para polos regionais (Juiz de Fora, Rio)
- ReduÃ§Ã£o de premissa de demanda externa: -25%
- Foco: Demanda local (moradores existentes) + retenÃ§Ã£o de jovens

---

### âš ï¸ RISCOS IDENTIFICADOS

1. **Gargalo de Mobilidade**
   - Ponte Ãºnica sobre Rio Pomba
   - Sensibilidade: ALTA
   - MitigaÃ§Ã£o: Considerar anel 5min mais conservador (55% ao invÃ©s de 60%)

2. **EvasÃ£o Populacional**
   - Saldo migratÃ³rio negativo consistente
   - Sensibilidade: MÃ‰DIA
   - MitigaÃ§Ã£o: Validar com Passo 2 (P2i-Lead) dinÃ¢mica econÃ´mica

3. **ExpansÃ£o Urbana Futura**
   - Novo loteamento em aprovaÃ§Ã£o (Zona Oeste)
   - Sensibilidade: BAIXA (3-5 anos para impacto)
   - MitigaÃ§Ã£o: Monitorar evoluÃ§Ã£o

---

### âœ… VALIDAÃ‡Ã•ES REALIZADAS

- [x] IsÃ³cronas geradas em horÃ¡rio de pico
- [x] Barreiras fÃ­sicas mapeadas e validadas
- [x] Grade H3 (res. 8) aplicada
- [x] Movimento pendular analisado
- [x] Migrante Data Fixa consultado
- [x] Entrevistas qualitativas (3 taxistas locais)

---

### ðŸ“ ANEXOS

1. `isocrona_5min_primaria.geojson`
2. `isocrona_10min_secundaria.geojson`
3. `isocrona_15min_terciaria.geojson`
4. `h3_populacao_renda.csv`
5. `consolidado_por_anel.csv`
6. `mapa_area_influencia.png` (A3)
7. `quotas_preliminares_passo6.csv`

---

**PrÃ³ximos Passos:**
- âœ… Passo 3 CONCLUÃDO
- âž¡ï¸ AvanÃ§ar para **Passo 4: VocaÃ§Ã£o ImobiliÃ¡ria**
- âž¡ï¸ Usar quotas preliminares em **Passo 6: Demanda**

---

**Metodologia:** TIV 4.0  
**Analista:** [Nome]  
**Data:** 12/11/2025  
**RevisÃ£o:** [Nome revisor] | [Data]
```

---

## 7. ALERTAS E VALIDAÃ‡Ã•ES

### 7.1. Red Flags CrÃ­ticos (BLOQUEANTES)

**âŒ RED FLAG 1: IsÃ³cronas em horÃ¡rio de vale**
```
Problema: Simular Ã s 10h da manhÃ£ subestima tempo real
Impacto: Ãrea de influÃªncia artificialmente inflada
SoluÃ§Ã£o: SEMPRE usar horÃ¡rio de pico (17h-19h)
```

**âŒ RED FLAG 2: Usar raio fixo (km) ao invÃ©s de tempo**
```
Problema: "1km de raio" = 15 min a pÃ© OU 3 min de carro
Impacto: Ãrea arbitrÃ¡ria, sem relaÃ§Ã£o com mobilidade real
SoluÃ§Ã£o: ABANDONAR raios, usar APENAS isÃ³cronas
```

**âŒ RED FLAG 3: Ignorar barreiras fÃ­sicas**
```
Problema: IsÃ³crona atravessa rio sem ponte
Impacto: PopulaÃ§Ã£o inacessÃ­vel contabilizada
SoluÃ§Ã£o: Validar malha viÃ¡ria manualmente
```

**âŒ RED FLAG 4: Percentuais fixos sem calibraÃ§Ã£o**
```
Problema: Usar sempre 60/30/10 independente do caso
Impacto: Sub/superestimaÃ§Ã£o de demanda
SoluÃ§Ã£o: Calibrar por caso (50-70 / 20-30 / 10-20)
```

**âŒ RED FLAG 5: NÃ£o validar com movimento pendular**
```
Problema: Assumir demanda sem verificar fluxos reais
Impacto: Demanda fantasma (populaÃ§Ã£o que nÃ£o compra)
SoluÃ§Ã£o: SEMPRE consultar IBGE Movimento Pendular
```

---

### 7.2. Alertas de AtenÃ§Ã£o (Ajustes)

**âš ï¸ ALERTA 1: ConurbaÃ§Ã£o nÃ£o mapeada**
```
SituaÃ§Ã£o: Mancha urbana contÃ­nua com municÃ­pio vizinho
Risco: Subestimar demanda externa
AÃ§Ã£o: Mapear conurbaÃ§Ã£o e agregar dados
```

**âš ï¸ ALERTA 2: Transporte pÃºblico nÃ£o considerado**
```
SituaÃ§Ã£o: Linha de metrÃ´/BRT prÃ³xima ao terreno
Risco: Subestimar Ã¡rea de influÃªncia
AÃ§Ã£o: Incluir buffer 500m ao redor das estaÃ§Ãµes
```

**âš ï¸ ALERTA 3: ExpansÃ£o urbana iminente**
```
SituaÃ§Ã£o: Novo loteamento em aprovaÃ§Ã£o na regiÃ£o
Risco: IsÃ³crona mudar em 2-3 anos (novas vias)
AÃ§Ã£o: Documentar premissa e atualizar periodicamente
```

**âš ï¸ ALERTA 4: Evento sazonal (obras, festas)**
```
SituaÃ§Ã£o: SimulaÃ§Ã£o durante obra viÃ¡ria temporÃ¡ria
Risco: Pico atÃ­pico, nÃ£o representativo
AÃ§Ã£o: Aguardar normalizaÃ§Ã£o ou documentar como exceÃ§Ã£o
```

**âš ï¸ ALERTA 5: PopulaÃ§Ã£o flutuante alta (>15%)**
```
SituaÃ§Ã£o: Movimento pendular muito alto
Risco: Demanda instÃ¡vel (trabalho, nÃ£o moradia)
AÃ§Ã£o: Pesquisa qualitativa para validar intenÃ§Ã£o de compra
```

---

### 7.3. Checklist de Qualidade (antes de concluir)

**Dados de entrada:**
- [ ] Coordenadas do terreno validadas (Google Maps)
- [ ] Passo 2 (DinÃ¢mica EconÃ´mica) concluÃ­do
- [ ] HorÃ¡rio de pico identificado (entrevistas/observaÃ§Ã£o)
- [ ] Barreiras fÃ­sicas mapeadas

**SimulaÃ§Ã£o de mobilidade:**
- [ ] IsÃ³cronas 5/10/15 min geradas
- [ ] HorÃ¡rio de pico usado (nÃ£o vale)
- [ ] Modal correto (carro para Brasil)
- [ ] Ferramenta confiÃ¡vel (Google/Mapbox/OSRM)

**Transporte pÃºblico (se aplicÃ¡vel):**
- [ ] Linhas estruturantes identificadas
- [ ] Buffer 500m aplicado ao redor das estaÃ§Ãµes
- [ ] IntersecÃ§Ã£o com isÃ³cronas realizada

**ConurbaÃ§Ãµes (se aplicÃ¡vel):**
- [ ] MunicÃ­pios contÃ­guos identificados
- [ ] Dados demogrÃ¡ficos multi-municÃ­pio agregados
- [ ] Migrante Data Fixa consultado

**Granularidade H3:**
- [ ] ResoluÃ§Ã£o adequada (H8 padrÃ£o, H9 alta precisÃ£o)
- [ ] HexÃ¡gonos intersectados com isÃ³cronas
- [ ] PopulaÃ§Ã£o/renda atribuÃ­da por hexÃ¡gono

**Fluxos populacionais:**
- [ ] Movimento Pendular consultado (IBGE)
- [ ] Migrante Data Fixa consultado (IBGE)
- [ ] InterpretaÃ§Ã£o feita conforme framework

**ParticipaÃ§Ãµes calibradas:**
- [ ] Percentuais ajustados ao caso (nÃ£o fixos 60/30/10)
- [ ] Justificativa documentada (TP, trÃ¢nsito, Ã¢ncoras)

**ValidaÃ§Ã£o qualitativa:**
- [ ] Entrevistas com taxistas/motoristas realizadas
- [ ] Gargalos confirmados
- [ ] Origem-destino validada

**EntregÃ¡veis gerados:**
- [ ] 3 arquivos GeoJSON (isÃ³cronas)
- [ ] CSV com grade H3 (populaÃ§Ã£o/renda)
- [ ] CSV consolidado por anel
- [ ] Mapa visual (PNG/PDF)
- [ ] Nota metodolÃ³gica (Markdown)
- [ ] Tabela de quotas preliminares (Passo 6)

**DocumentaÃ§Ã£o:**
- [ ] Premissas explicitadas
- [ ] Riscos identificados
- [ ] SumÃ¡rio executivo gerado
- [ ] Anexos organizados

**AprovaÃ§Ã£o final:**
- [ ] RevisÃ£o por analista sÃªnior
- [ ] Cross-check com Passo 2 (coerÃªncia demogrÃ¡fica)
- [ ] Pronto para usar em Passo 4 (VocaÃ§Ã£o) e Passo 6 (Demanda)

---

## 8. INTEGRAÃ‡ÃƒO COM OUTRAS SKILLS

### 8.1. Skills PrÃ©-Requisito (Inputs)

**Passo 1: Garimpo (`tiv-garimpo`)**
- Coordenadas do terreno
- LocalizaÃ§Ã£o aproximada se "sem terreno"

**Passo 2: DinÃ¢mica EconÃ´mica (`tiv-passo2-dinamica-economica`)**
- PopulaÃ§Ã£o total do municÃ­pio
- DistribuiÃ§Ã£o de renda (Faixas A-E)
- PIB per capita
- Leading indicators

### 8.2. Skills Consumidoras (Outputs)

**Passo 4: VocaÃ§Ã£o ImobiliÃ¡ria (`tiv-passo4-vocacao`)**
- Pilar 2 (Centralidades) depende de isÃ³cronas 5/10 min
- Mapeamento de Ã¢ncoras por tempo de deslocamento

**Passo 6: Demanda (`tiv-passo6-demanda`)**
- **Input CRÃTICO:** Tabela de quotas preliminares
- PopulaÃ§Ã£o por anel para dimensionar amostra de pesquisa
- Renda por subÃ¡rea para segmentaÃ§Ã£o

**Passo 7: Oferta (`tiv-passo7-oferta`)**
- PolÃ­gono de influÃªncia define Ã¡rea de busca de concorrentes
- VSO (VacÃ¢ncia + Estoque + Oferta) dentro da AAI

**Passo 8: AbsorÃ§Ã£o (`tiv-absorcao`)**
- PopulaÃ§Ã£o do anel primÃ¡rio (5 min) para estimar velocidade
- Densidade demogrÃ¡fica para calibrar Fator 4:1

**Passo 9: ValidaÃ§Ã£o (`tiv-validador`)**
- Premissas de Ã¡rea de influÃªncia sÃ£o validadas
- Checklist: "IsÃ³cronas usaram horÃ¡rio de pico?"

**Passo 10: FCD (`tiv-fcd`)**
- Tamanho de mercado potencial (populaÃ§Ã£o x participaÃ§Ã£o)
- Input indireto via Passo 6 (Demanda)

---

### 8.3. Fluxo de Dados (Diagrama)

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ PASSO 2: DINÃ‚MICA ECONÃ”MICA                     â”‚
â”‚ Output: PopulaÃ§Ã£o + Renda por municÃ­pio         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                   â”‚
                   â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ PASSO 3: ÃREA DE INFLUÃŠNCIA â—„â”€â”€ VOCÃŠ ESTÃ AQUI  â”‚
â”‚ Input: Pop/Renda + Coordenadas terreno           â”‚
â”‚ Output: IsÃ³cronas + H3 + Quotas                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â”‚                   â”‚
               â†“                   â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ PASSO 4: VOCAÃ‡ÃƒO     â”‚  â”‚ PASSO 6: DEMANDA      â”‚
â”‚ Usa: IsÃ³cronas       â”‚  â”‚ Usa: Quotas + Pop AAI â”‚
â”‚ Para: Centralidades  â”‚  â”‚ Para: Amostra pesq    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â”‚                   â”‚
               â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â†“
       â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
       â”‚ PASSO 7: OFERTA               â”‚
       â”‚ Usa: PolÃ­gono AAI             â”‚
       â”‚ Para: Buscar concorrentes VSO â”‚
       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                       â”‚
                       â†“
       â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
       â”‚ PASSO 8: ABSORÃ‡ÃƒO             â”‚
       â”‚ Usa: Pop anel primÃ¡rio        â”‚
       â”‚ Para: Velocidade vendas       â”‚
       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## 9. EXEMPLOS PRÃTICOS

### 9.1. Caso 1: Loteamento Popular - Leopoldina-MG

**Contexto:**
- Terreno: 22 hectares, Zona Rural (limite urbano)
- Produto: Loteamento popular, 350 lotes de 250mÂ²
- PreÃ§o-alvo: R$ 140.000/lote
- PÃºblico: Faixa C-D (R$ 3.000-5.000 renda familiar)

**ETAPA 1: ConfiguraÃ§Ã£o**
```yaml
localizacao:
  coordenadas: [-21.5411, -42.6189]
  referencia: "Av. JoÃ£o Cotta, prÃ³ximo ao Bairro Loteamento"
  municipio: "Leopoldina-MG"

mobilidade:
  pico_horario: "18:30"
  modal: "carro"
  tempos: [5, 10, 15]
  dia: "Quinta-feira"
```

**ETAPA 2: SimulaÃ§Ã£o de IsÃ³cronas**

Ferramenta: Google Maps API  
Data: 12/11/2025  
CondiÃ§Ã£o: TrÃ¢nsito tÃ­pico de quinta, 18h30  

**Resultados:**
- IsÃ³crona 5 min: 2,1 kmÂ² (Ã¡rea urbana consolidada)
- IsÃ³crona 10 min: 6,3 kmÂ² (incluindo bairros perifÃ©ricos)
- IsÃ³crona 15 min: 11,8 kmÂ² (zona rural + distritos)

**Barreiras identificadas:**
- Rio Pomba (sul): Travessia Ãºnica pela Ponte GetÃºlio Vargas
- Linha fÃ©rrea (leste): 3 passagens de nÃ­vel (gargalos em horÃ¡rio pico)

**ETAPA 3: Transporte PÃºblico**

Status: NÃƒO APLICÃVEL  
Justificativa: Leopoldina nÃ£o possui sistema estruturante (metrÃ´/BRT)  
Linhas de Ã´nibus: Baixa frequÃªncia, sem impacto significativo na AAI

**ETAPA 4: ConurbaÃ§Ãµes**

Status: NÃƒO APLICÃVEL  
Justificativa: Leopoldina Ã© municÃ­pio isolado, sem continuidade urbana com vizinhos

**ETAPA 5: Grade H3 (ResoluÃ§Ã£o 8)**

```csv
h3_index,anel,area_km2,populacao,renda_media,faixa_predominante
888e1c4a9ffffff,5min,0.68,8450,3200,C
888e1c4b1ffffff,5min,0.71,6780,2950,D
888e1c4c3ffffff,10min,0.69,4320,3600,C
888e1c4c9ffffff,10min,0.72,3890,3100,C
888e1c5a1ffffff,15min,0.70,2560,3400,C
...
```

**ETAPA 6: ConsolidaÃ§Ã£o por Anel**

| Anel | Tempo | Ãrea (kmÂ²) | PopulaÃ§Ã£o | Renda MÃ©dia | Faixa Pred. |
|------|-------|------------|-----------|-------------|-------------|
| PrimÃ¡rio | 5 min | 2,1 | 15.230 | R$ 3.075 | C (40%) + D (38%) |
| SecundÃ¡rio | 10 min | 6,3 | 8.210 | R$ 3.350 | C (45%) + D (30%) |
| TerciÃ¡rio | 15 min | 11,8 | 5.480 | R$ 3.200 | C (42%) + D (35%) |
| **TOTAL** | - | **20,2** | **28.920** | **R$ 3.175** | - |

**ETAPA 7: Movimento Pendular (IBGE 2010)**

```
Leopoldina (entrada trabalho): 120 pessoas/dia
Leopoldina (saÃ­da trabalho): 300 pessoas/dia
Saldo: -180 (evasÃ£o lÃ­quida)

InterpretaÃ§Ã£o TIV: BAIXO PENDULAR + dados de migraÃ§Ã£o necessÃ¡rios
```

**ETAPA 8: Migrante Data Fixa (2000-2010)**

```
ImigraÃ§Ã£o para Leopoldina: 77 pessoas/dÃ©cada
EmigraÃ§Ã£o de Leopoldina: 390 pessoas/dÃ©cada
Saldo: -313 (evasÃ£o lÃ­quida)

CenÃ¡rio: 3 (Baixo Pendular + Alta EmigraÃ§Ã£o)
AÃ§Ã£o: Reduzir premissa demanda externa -25%
```

**ETAPA 9: CalibraÃ§Ã£o de ParticipaÃ§Ãµes**

```
Fatores considerados:
- TrÃ¢nsito moderado (nÃ£o congestionado) â†’ MantÃ©m padrÃ£o
- Sem transporte pÃºblico estruturante â†’ Concentra anel primÃ¡rio
- Produto acessÃ­vel (R$ 140k) â†’ Foco local (baixa mobilidade)
- EvasÃ£o populacional documentada â†’ Reduz anÃ©is externos

CALIBRAÃ‡ÃƒO FINAL:
- Anel 5 min: 65% (acima do padrÃ£o 60%)
- Anel 10 min: 22% (abaixo do padrÃ£o 25%)
- Anel 15 min: 13% (abaixo do padrÃ£o 15%)
```

**ETAPA 10: ValidaÃ§Ã£o Qualitativa**

```
Entrevistas: 3 taxistas (Ponto PraÃ§a da EstaÃ§Ã£o)
Data: 10/11/2025, 17h-19h

Taxista 1 (JoÃ£o, 15 anos experiÃªncia):
"Maior fluxo Ã© gente voltando pra casa. Centro â†’ bairros.
Ponte do Rio Pomba engarrafa todo dia 18h. 
Pessoal do Loteamento trabalha na cidade, mora lÃ¡ porque Ã© mais barato."

Taxista 2 (Maria, 8 anos experiÃªncia):
"Quem tem condiÃ§Ã£o mora no centro. Bairros mais afastados 
sÃ£o pra quem nÃ£o consegue pagar aluguel caro. Muita gente 
jovem sai pra estudar em Juiz de Fora e nÃ£o volta."

Taxista 3 (Pedro, 22 anos experiÃªncia):
"Cidade nÃ£o cresce muito. FÃ¡brica de tecido fechou nos anos 90,
muita gente foi embora. Hoje quem fica Ã© funcionÃ¡rio pÃºblico
e comerciante. DifÃ­cil vender casa cara aqui."

INSIGHTS:
âœ… Confirma evasÃ£o de jovens (migraÃ§Ã£o para polos)
âœ… Valida demanda por produto acessÃ­vel (aluguel caro no centro)
âš ï¸ Alerta sobre estagnaÃ§Ã£o econÃ´mica (revisitar Passo 2)
```

**OUTPUTS GERADOS:**

1. **IsÃ³cronas GeoJSON:**
   - `leopoldina_isocrona_5min.geojson` (2,1 kmÂ²)
   - `leopoldina_isocrona_10min.geojson` (6,3 kmÂ²)
   - `leopoldina_isocrona_15min.geojson` (11,8 kmÂ²)

2. **Grade H3:**
   - `leopoldina_h3_populacao_renda.csv` (142 hexÃ¡gonos)

3. **Consolidado:**
   ```csv
   Anel,Tempo,Area_km2,Populacao,Renda_Media,Participacao
   Primario,5,2.1,15230,3075,65%
   Secundario,10,6.3,8210,3350,22%
   Terciario,15,11.8,5480,3200,13%
   ```

4. **Quotas Preliminares (Passo 6):**
   ```csv
   Subarea,Faixa_Renda,Populacao,Quota_Pesquisa
   Primario_Centro,C,6092,30
   Primario_Norte,D,5787,29
   Primario_Sul,C,3351,17
   Secundario_Leste,C,3695,18
   Secundario_Oeste,C,2465,12
   Terciario_Rural,C-D,5480,27
   TOTAL,-,28920,133
   ```

5. **Mapa Visual:**  
   [Arquivo PNG anexo - nÃ£o reproduzido aqui]

6. **SumÃ¡rio Executivo:**
   ```
   ÃREA DE INFLUÃŠNCIA TOTAL: 20,2 kmÂ²
   POPULAÃ‡ÃƒO ABRANGIDA: 28.920 habitantes
   DEMANDA CALIBRADA:
   - Anel 5 min (65%): 9.900 famÃ­lias
   - Anel 10 min (22%): 1.806 famÃ­lias
   - Anel 15 min (13%): 712 famÃ­lias
   
   TOTAL POTENCIAL: 12.418 famÃ­lias (antes de filtros de renda/idade)
   
   ÃNDICE DEMANDA/PRODUTO: 12.418 / 350 lotes = 35,5x
   â†’ Demanda teoricamente robusta, MAS:
   
   âš ï¸ RESSALVAS:
   - EvasÃ£o populacional documentada (-313 pessoas/dÃ©cada)
   - DinÃ¢mica econÃ´mica fraca (revisitar Passo 2)
   - NecessÃ¡rio validar com pesquisa primÃ¡ria (Passo 6)
   ```

---

### 9.2. Caso 2: Vertical MÃ©dio PadrÃ£o - SÃ£o LuÃ­s-MA (ConurbaÃ§Ã£o)

**Contexto:**
- Terreno: 2.500 mÂ², Zona Urbana (Jaracaty, SÃ£o LuÃ­s)
- Produto: 60 apartamentos 2 dorm, 65mÂ², R$ 420.000
- PÃºblico: Faixa B-C (R$ 6.000-10.000 renda familiar)
- **PARTICULARIDADE:** RegiÃ£o conurbada com municÃ­pios vizinhos

**ETAPA 1: ConfiguraÃ§Ã£o**
```yaml
localizacao:
  coordenadas: [-2.5304, -44.2755]  # SÃ£o LuÃ­s, Jaracaty
  referencia: "PrÃ³ximo Ã  Avenida dos Holandeses"
  municipio: "SÃ£o LuÃ­s-MA"

mobilidade:
  pico_horario: "18:00"  # Pico mais intenso em SÃ£o LuÃ­s
  modal: "carro"
  tempos: [5, 10, 15]
  dia: "Quarta-feira"

conurbacoes:
  ativo: true
  municipios:
    - "PaÃ§o do Lumiar"
    - "SÃ£o JosÃ© de Ribamar"
    - "Raposa"
```

**ETAPA 2: SimulaÃ§Ã£o de IsÃ³cronas (com conurbaÃ§Ã£o)**

Ferramenta: Mapbox Isochrone API  
Data: 12/11/2025  
CondiÃ§Ã£o: TrÃ¢nsito tÃ­pico de quarta, 18h  

**Resultados:**
- IsÃ³crona 5 min: 3,8 kmÂ² (Jaracaty + Cohama + parte SÃ£o Francisco)
- IsÃ³crona 10 min: 12,4 kmÂ² (**cruza para PaÃ§o do Lumiar**)
- IsÃ³crona 15 min: 28,6 kmÂ² (inclui SÃ£o JosÃ© de Ribamar)

**Barreiras identificadas:**
- Nenhuma barreira fÃ­sica crÃ­tica (orla permite circulaÃ§Ã£o)
- Avenida dos Holandeses = eixo estruturante de mobilidade

**ETAPA 3: Transporte PÃºblico**

Status: **INCLUIR BUFFERS**  
Justificativa: Sistema de BRT (Corredor SÃ£o LuÃ­s) com estaÃ§Ãµes prÃ³ximas

**Linhas relevantes:**
- Corredor SÃ£o Francisco (estaÃ§Ã£o 800m do terreno)
- FrequÃªncia: 10-15 min (horÃ¡rio pico)
- IntegraÃ§Ã£o tarifÃ¡ria: Sim

**Buffers aplicados:**
```
EstaÃ§Ãµes no raio de 2km:
- EstaÃ§Ã£o Jaracaty (800m do terreno)
- EstaÃ§Ã£o Cohama (1.400m do terreno)
- EstaÃ§Ã£o Angelim (1.800m do terreno)

Buffer 500m ao redor de cada estaÃ§Ã£o
IntersecÃ§Ã£o com isÃ³crona 10 min
AAI ampliada: 12,4 kmÂ² â†’ 14,1 kmÂ² (+13,7%)
```

**ETAPA 4: ConurbaÃ§Ãµes (CRÃTICO neste caso)**

**MunicÃ­pios na AAI:**

| MunicÃ­pio | Pop. Total (IBGE 2022) | Dentro da AAI | % Abrangida |
|-----------|------------------------|---------------|-------------|
| SÃ£o LuÃ­s | 1.115.932 | 245.000 | 22% |
| PaÃ§o do Lumiar | 123.527 | 18.300 | 15% |
| SÃ£o JosÃ© de Ribamar | 179.028 | 8.900 | 5% |
| Raposa | 32.849 | 0 | 0% (fora isÃ³crona 15min) |

**Movimento Pendular (IBGE 2010) - TRABALHO:**

```
Destino: SÃ£o LuÃ­s (20-49 anos)
- PaÃ§o do Lumiar â†’ SÃ£o LuÃ­s: 21.714 pessoas/dia
- SÃ£o JosÃ© de Ribamar â†’ SÃ£o LuÃ­s: 16.366 pessoas/dia
- Raposa â†’ SÃ£o LuÃ­s: 1.595 pessoas/dia

TOTAL PENDULAR: 39.675 pessoas/dia
```

**Migrante Data Fixa (2000-2010):**

```
PaÃ§o do Lumiar â†’ SÃ£o LuÃ­s: 2.890 pessoas/dÃ©cada
SÃ£o JosÃ© de Ribamar â†’ SÃ£o LuÃ­s: 1.650 pessoas/dÃ©cada

CenÃ¡rio: 1 (Alto Pendular + Alta MigraÃ§Ã£o)
InterpretaÃ§Ã£o: Demanda retenÃ­vel FORTE
AÃ§Ã£o: Aumentar premissa demanda externa +25%
```

**ETAPA 5: Grade H3 (ResoluÃ§Ã£o 8) - Multi-MunicÃ­pio**

```csv
h3_index,anel,municipio,populacao,renda_media,faixa_predominante
888d2a4a9ffffff,5min,Sao_Luis,12400,8500,B
888d2a4b1ffffff,5min,Sao_Luis,9800,7200,C
888d2a5c3ffffff,10min,Sao_Luis,7600,8900,B
888d2b1a1ffffff,10min,Paco_Lumiar,4300,6500,C
888d2b2c9ffffff,15min,Sao_Jose_Ribamar,2100,5800,C
...
```

**ETAPA 6: ConsolidaÃ§Ã£o por Anel (Multi-MunicÃ­pio)**

| Anel | Tempo | Ãrea (kmÂ²) | Pop. Total | Renda MÃ©dia | MunicÃ­pios Abrangidos |
|------|-------|------------|------------|-------------|----------------------|
| PrimÃ¡rio | 5 min | 3,8 | 245.000 | R$ 7.850 | SÃ£o LuÃ­s (100%) |
| SecundÃ¡rio | 10 min | 14,1 | 89.300 | R$ 7.200 | SÃ£o LuÃ­s (80%) + PaÃ§o Lumiar (20%) |
| TerciÃ¡rio | 15 min | 28,6 | 43.200 | R$ 6.400 | SÃ£o LuÃ­s (70%) + PaÃ§o (20%) + Ribamar (10%) |
| **TOTAL** | - | **46,5** | **377.500** | **R$ 7.483** | 3 municÃ­pios |

**ETAPA 7: CalibraÃ§Ã£o de ParticipaÃ§Ãµes (ConurbaÃ§Ã£o)**

```
Fatores considerados:
- Transporte pÃºblico estruturante (BRT) â†’ AUMENTA anÃ©is externos
- ConurbaÃ§Ã£o forte (mancha urbana contÃ­nua) â†’ AUMENTA Ã¡rea 10/15min
- Movimento pendular ALTO (39.675 pess/dia) â†’ AUMENTA demanda externa
- Produto mÃ©dio padrÃ£o (R$ 420k) â†’ PÃºblico com maior mobilidade
- MigraÃ§Ã£o efetiva documentada â†’ VALIDA cultura de mudanÃ§a

CALIBRAÃ‡ÃƒO FINAL:
- Anel 5 min: 55% (abaixo do padrÃ£o, pois TP dilui concentraÃ§Ã£o)
- Anel 10 min: 30% (acima do padrÃ£o, por causa de conurbaÃ§Ã£o)
- Anel 15 min: 15% (mantÃ©m padrÃ£o, limite psicolÃ³gico deslocamento)
```

**ETAPA 8: ValidaÃ§Ã£o com Taxistas (Guerrilha)**

```
Entrevistados: 4 motoristas Uber (ponto Cohama)
Data: 08/11/2025, 17h30-19h30

Uber 1: "Muita gente de PaÃ§o do Lumiar trabalha aqui em SÃ£o LuÃ­s.
         De manhÃ£ enche o BRT vindo de lÃ¡. Jaracaty Ã© bairro valorizado,
         quem pode prefere morar aqui pra nÃ£o pegar trÃ¢nsito todo dia."

Uber 2: "SÃ£o JosÃ© de Ribamar tÃ¡ crescendo, mas ainda Ã© longe.
         Galera trabalha aqui mas mora lÃ¡ por causa do preÃ§o.
         Se aparecer apto por R$ 400k aqui em Jaracaty, 
         vÃ£o querer vir, com certeza."

Uber 3: "BRT ajudou muito. Antes era sÃ³ carro, engarrafava demais.
         Hoje dÃ¡ pra vir de Ã´nibus tranquilo, 20-25 minutos."

Uber 4: "RegiÃ£o Ã© boa, tem shopping, praia perto, escola particular.
         Quem tem famÃ­lia valoriza. PreÃ§o de R$ 400k-500k Ã© justo,
         tem demanda sim."

INSIGHTS:
âœ… Confirma pendularidade (PaÃ§o Lumiar â†’ SÃ£o LuÃ­s)
âœ… Valida intenÃ§Ã£o de retenÃ§Ã£o ("quem pode prefere morar aqui")
âœ… BRT amplia Ã¡rea de influÃªncia (validar buffer 500m)
âœ… PreÃ§o-alvo R$ 420k percebido como "justo" (sweet spot)
```

**OUTPUTS GERADOS:**

1. **SumÃ¡rio Executivo (ConurbaÃ§Ã£o):**
   ```
   ÃREA DE INFLUÃŠNCIA TOTAL: 46,5 kmÂ²
   MUNICÃPIOS ABRANGIDOS: 3 (SÃ£o LuÃ­s, PaÃ§o do Lumiar, S. JosÃ© Ribamar)
   POPULAÃ‡ÃƒO TOTAL: 377.500 habitantes
   
   DEMANDA CALIBRADA (Faixa B-C):
   - Anel 5 min (55%): 207.625 habitantes â†’ 50.430 famÃ­lias
   - Anel 10 min (30%): 113.250 habitantes â†’ 27.510 famÃ­lias
   - Anel 15 min (15%): 56.625 habitantes â†’ 13.755 famÃ­lias
   
   POTENCIAL BRUTO (antes de filtros): 91.695 famÃ­lias
   
   ÃNDICE DEMANDA/PRODUTO: 91.695 / 60 aptos = 1.528x
   â†’ Demanda EXTREMAMENTE robusta
   
   âš ï¸ PRÃ“XIMOS PASSOS:
   - Filtrar por renda (Faixa B-C = 43% da populaÃ§Ã£o)
   - Aplicar Regra 30% (capacidade de compra R$ 420k)
   - Validar com pesquisa primÃ¡ria (Passo 6)
   - Analisar VSO (VacÃ¢ncia, Estoque, Oferta - Passo 7)
   ```

2. **Tabela de Quotas Preliminares (Multi-MunicÃ­pio):**
   ```csv
   Subarea,Municipio,Faixa,Populacao,Quota
   Primario_Jaracaty,Sao_Luis,B,85000,43
   Primario_Cohama,Sao_Luis,B-C,78000,39
   Primario_SaoFrancisco,Sao_Luis,C,82000,41
   Secundario_PacoLumiar,Paco_Lumiar,C,18300,9
   Secundario_Angelim,Sao_Luis,B,35000,18
   Secundario_Turu,Sao_Luis,C,36000,18
   Terciario_Ribamar,Sao_Jose_Ribamar,C,8900,4
   Terciario_Vinhais,Sao_Luis,B,19300,10
   Terciario_OutrosÃºrio,Sao_Luis,C,15000,8
   TOTAL,3_municipios,-,377500,190
   ```

3. **Nota MetodolÃ³gica (ConurbaÃ§Ã£o):**
   ```markdown
   ## Tratamento de ConurbaÃ§Ã£o
   
   ### CritÃ©rios de InclusÃ£o:
   1. Mancha urbana contÃ­nua (sem zona rural entre municÃ­pios)
   2. Fluxo pendular > 5% da populaÃ§Ã£o
   3. Tempo de deslocamento dentro das isÃ³cronas 10-15 min
   
   ### MunicÃ­pios IncluÃ­dos:
   - **PaÃ§o do Lumiar:** 21.714 pendulares/dia (17,6% da pop.)
   - **SÃ£o JosÃ© de Ribamar:** 16.366 pendulares/dia (9,1% da pop.)
   - **Raposa:** 1.595 pendulares/dia (4,8% da pop.) - EXCLUÃDO
   
   ### ValidaÃ§Ã£o:
   - Migrante Data Fixa positivo (cultura de migraÃ§Ã£o)
   - Transporte pÃºblico estruturante (BRT)
   - Produto mÃ©dio padrÃ£o (Faixa B-C) compatÃ­vel com renda pendular
   
   ### Premissa:
   Potencial de retenÃ§Ã£o de 10-15% dos pendulares (conservador)
   â†’ 3.970 - 5.955 famÃ­lias adicionais na demanda
   ```

**CONCLUSÃƒO DO CASO 2:**

âœ… ConurbaÃ§Ã£o CORRETAMENTE mapeada  
âœ… Transporte pÃºblico incluÃ­do (BRT)  
âœ… Movimento pendular validado com Migrante Data Fixa  
âœ… ParticipaÃ§Ãµes calibradas (55/30/15 ao invÃ©s de 60/25/15)  
âœ… Demanda robusta documentada (1.528x produto)  

**Diferencial TIV:**  
Em anÃ¡lise tradicional, Ã¡rea de influÃªncia seria restrita a SÃ£o LuÃ­s (245k hab).  
Com metodologia TIV (conurbaÃ§Ã£o + TP), Ã¡rea ampliada para 377,5k hab (+54%).

---

## 10. CHECKLIST DE QUALIDADE

### 10.1. Checklist PrÃ©-ExecuÃ§Ã£o (Definition of Ready)

**Dados de Entrada:**
- [ ] Coordenadas GPS do terreno validadas (lat/long precisos)
- [ ] OU Ã¡rea-alvo "sem terreno" com raio inicial definido
- [ ] Passo 1 (Garimpo) concluÃ­do
- [ ] Passo 2 (DinÃ¢mica EconÃ´mica) concluÃ­do
- [ ] PopulaÃ§Ã£o total do municÃ­pio conhecida
- [ ] DistribuiÃ§Ã£o de renda (Faixas A-E) mapeada

**Infraestrutura:**
- [ ] HorÃ¡rio de pico local identificado (observaÃ§Ã£o ou pesquisa)
- [ ] Principais vias de acesso conhecidas
- [ ] Barreiras fÃ­sicas prÃ©-mapeadas (rios, morros, ferrovias)
- [ ] Transporte pÃºblico: existÃªncia de sistema estruturante verificada
- [ ] ConurbaÃ§Ãµes: municÃ­pios contÃ­guos identificados

**Ferramentas:**
- [ ] Acesso a ferramenta de isÃ³cronas (Google/Mapbox/OSRM)
- [ ] Conta configurada e com crÃ©ditos (se API paga)
- [ ] Software GIS instalado (QGIS, Kepler.gl, ou similar)
- [ ] Biblioteca H3 disponÃ­vel (Python/R/JavaScript)

---

### 10.2. Checklist Durante ExecuÃ§Ã£o (Process Quality)

**SimulaÃ§Ã£o de Mobilidade:**
- [ ] IsÃ³cronas geradas em horÃ¡rio de PICO (nÃ£o vale)
- [ ] Modal correto para o contexto (carro padrÃ£o Brasil)
- [ ] Tempos padrÃ£o TIV: 5 / 10 / 15 minutos
- [ ] Dia Ãºtil tÃ­pico (terÃ§a/quarta/quinta - evitar segunda/sexta)
- [ ] ValidaÃ§Ã£o visual: isÃ³cronas nÃ£o atravessam barreiras impossÃ­veis

**Transporte PÃºblico (se aplicÃ¡vel):**
- [ ] Sistema identificado como estruturante (metrÃ´/BRT/corredor)
- [ ] FrequÃªncia validada (< 15 min intervalo no pico)
- [ ] Buffer 500m aplicado ao redor de TODAS as estaÃ§Ãµes na Ã¡rea
- [ ] IntersecÃ§Ã£o com isÃ³cronas de carro realizada
- [ ] Ãrea ampliada documentada (% de aumento)

**ConurbaÃ§Ãµes (se aplicÃ¡vel):**
- [ ] Mancha urbana contÃ­nua confirmada (Google Earth/Maps)
- [ ] Movimento pendular consultado (IBGE > 5% populaÃ§Ã£o)
- [ ] Migrante Data Fixa consultado (validar cultura migraÃ§Ã£o)
- [ ] Dados demogrÃ¡ficos dos municÃ­pios vizinhos agregados
- [ ] ProporÃ§Ã£o multi-municÃ­pio documentada

**Granularidade H3:**
- [ ] ResoluÃ§Ã£o apropriada selecionada (H8 padrÃ£o, H9 alta precisÃ£o)
- [ ] ConversÃ£o de isÃ³cronas (GeoJSON) para grade H3 bem-sucedida
- [ ] PopulaÃ§Ã£o por hexÃ¡gono atribuÃ­da (IBGE setores censitÃ¡rios)
- [ ] Renda mÃ©dia por hexÃ¡gono atribuÃ­da
- [ ] Faixa predominante identificada (A/B/C/D/E)

**ConsolidaÃ§Ã£o de Dados:**
- [ ] Soma de populaÃ§Ã£o por anel conferida (nÃ£o duplicar hexÃ¡gonos)
- [ ] Renda mÃ©dia ponderada calculada (nÃ£o aritmÃ©tica simples)
- [ ] Ãreas em kmÂ² calculadas corretamente
- [ ] Densidade populacional calculada (hab/kmÂ²)

---

### 10.3. Checklist PÃ³s-ExecuÃ§Ã£o (Outputs Quality)

**Arquivos Geoespaciais:**
- [ ] 3 arquivos GeoJSON gerados (5/10/15 min)
- [ ] Metadados completos em cada arquivo (data, horÃ¡rio, ferramenta)
- [ ] Arquivos testados (abertura em QGIS ou similar)
- [ ] ProjeÃ§Ã£o correta (WGS84, EPSG:4326)

**Dados Tabulares:**
- [ ] CSV com grade H3 (pop/renda por hexÃ¡gono)
- [ ] CSV consolidado por anel (3 linhas: 5/10/15 min)
- [ ] Tabela de quotas preliminares (Passo 6)
- [ ] FormataÃ§Ã£o consistente (separador, encoding UTF-8)

**AnÃ¡lise de Fluxos:**
- [ ] Movimento Pendular consultado e documentado
- [ ] Migrante Data Fixa consultado e documentado
- [ ] InterpretaÃ§Ã£o feita conforme framework TIV (4 cenÃ¡rios)
- [ ] AÃ§Ã£o recomendada (aumentar/reduzir/manter demanda)

**CalibraÃ§Ã£o de ParticipaÃ§Ãµes:**
- [ ] Percentuais ajustados (nÃ£o fixos 60/30/10)
- [ ] Justificativa tÃ©cnica documentada (TP, trÃ¢nsito, Ã¢ncoras)
- [ ] Faixas respeitadas (50-70 / 20-30 / 10-20)
- [ ] Soma = 100% (checagem aritmÃ©tica)

**ValidaÃ§Ã£o Qualitativa:**
- [ ] Entrevistas com taxistas/motoristas realizadas (â‰¥3 pessoas)
- [ ] HorÃ¡rio adequado (pico de movimento)
- [ ] Insights documentados
- [ ] CoerÃªncia com dados quantitativos (triangulaÃ§Ã£o)

**VisualizaÃ§Ã£o:**
- [ ] Mapa visual gerado (PNG/PDF, mÃ­nimo A3)
- [ ] Legenda clara (cores por anel, escala, norte)
- [ ] LocalizaÃ§Ã£o do terreno destacada (pin ou marcador)
- [ ] Barreiras fÃ­sicas representadas
- [ ] Elementos auxiliares (vias principais, Ã¢ncoras, limites municipais)

**DocumentaÃ§Ã£o:**
- [ ] SumÃ¡rio executivo gerado (template TIV)
- [ ] Nota metodolÃ³gica completa
- [ ] Premissas explicitadas (horÃ¡rio, modal, ferramenta)
- [ ] Riscos identificados e documentados
- [ ] PrÃ³ximos passos definidos (Passos 4, 6, 7, 8)

---

### 10.4. Checklist de AprovaÃ§Ã£o Final (Definition of Done)

**Completude:**
- [ ] Todos os entregÃ¡veis obrigatÃ³rios gerados (seÃ§Ã£o 6.1)
- [ ] Nenhum red flag crÃ­tico nÃ£o resolvido (seÃ§Ã£o 7.1)
- [ ] ValidaÃ§Ãµes qualitativas realizadas
- [ ] IntegraÃ§Ã£o com Passo 2 verificada (coerÃªncia demogrÃ¡fica)

**Qualidade TÃ©cnica:**
- [ ] IsÃ³cronas realistas (nÃ£o atravessam barreiras impossÃ­veis)
- [ ] PopulaÃ§Ã£o total AAI â‰¤ populaÃ§Ã£o municÃ­pio (se sem conurbaÃ§Ã£o)
- [ ] Renda mÃ©dia AAI alinhada com Passo 2
- [ ] ParticipaÃ§Ãµes calibradas (nÃ£o fixas) e justificadas

**Rastreabilidade:**
- [ ] Fonte de dados documentada (API, data, horÃ¡rio)
- [ ] Versionamento de arquivos (.geojson, .csv)
- [ ] Metadados completos
- [ ] Possibilidade de replicar anÃ¡lise (reprodutibilidade)

**RevisÃ£o:**
- [ ] RevisÃ£o por analista sÃªnior realizada
- [ ] Cross-check com Passo 2 (DinÃ¢mica EconÃ´mica)
- [ ] AprovaÃ§Ã£o formal para usar em Passos 4, 6, 7, 8
- [ ] Arquivos organizados em pasta estruturada

**Arquivamento:**
- [ ] Pasta `/outputs/area_influencia/[nome_projeto]` criada
- [ ] Todos os arquivos copiados para a pasta
- [ ] README.md com Ã­ndice de arquivos
- [ ] Backup em nuvem (Google Drive, Dropbox, etc.)

**Go/No-Go:**
- [ ] âœ… GO: Todos os checkboxes marcados â†’ Passo 3 CONCLUÃDO
- [ ] âŒ NO-GO: Algum checkbox crÃ­tico desmarcado â†’ REFAZER anÃ¡lise

---

## 11. TEMPLATES PRONTOS

### 11.1. Template YAML de ConfiguraÃ§Ã£o (T3-AreaInfluencia.yml)

```yaml
# PASSO 3: ÃREA DE INFLUÃŠNCIA - CONFIGURAÃ‡ÃƒO
# Metodologia: TIV 4.0
# VersÃ£o: 1.0 (2025-11-12)

passo: 3
versao: "2025-11-12_v1.0"

# LOCALIZAÃ‡ÃƒO
localizacao:
  tipo: "com_terreno"  # ou "sem_terreno"
  coordenadas:
    latitude: -21.5333
    longitude: -42.6417
  endereco: "Av. dos Andradas, 1500 - Centro"
  municipio: "Leopoldina-MG"
  estado: "MG"
  referencia: "PrÃ³ximo ao Shopping Leopoldina"

# MOBILIDADE
mobilidade:
  pico_horario: "18:30"
  dia_semana: "Quinta-feira"  # Evitar seg/sex
  modal_prioritario: "carro"
  tempos_analise: [5, 10, 15]  # minutos
  ferramenta: "Google Maps Distance Matrix API"  # ou Mapbox/OSRM

# TRANSPORTE PÃšBLICO
tp_buffers:
  ativo: false  # true se houver sistema estruturante
  sistema: null  # "MetrÃ´" / "BRT" / "Corredor Ã”nibus"
  raio_buffer_m: 500
  linhas_relevantes: []
  # Exemplo se ativo:
  # linhas_relevantes:
  #   - nome: "Linha 4-Amarela"
  #     estacoes: ["ButantÃ£", "Pinheiros", "Faria Lima"]

# GRANULARIDADE ESPACIAL
h3:
  resolucao: 8  # PadrÃ£o TIV: 8 (~0.7 kmÂ²) | Alta precisÃ£o: 9 (~0.1 kmÂ²)
  fonte_populacao: "IBGE Setores CensitÃ¡rios 2022"
  fonte_renda: "Atlas Brasil / P2i"

# CONURBAÃ‡Ã•ES
conurbacoes:
  ativo: false  # true se houver municÃ­pios contÃ­guos
  municipios: []
  # Exemplo se ativo:
  # municipios:
  #   - nome: "Cataguases"
  #     distancia_km: 0  # se contÃ­guo
  #     movimento_pendular: 150  # pessoas/dia
  #   - nome: "AlÃ©m ParaÃ­ba"
  #     distancia_km: 0
  #     movimento_pendular: 85

# OUTPUTS
outputs:
  pasta: "/outputs/area_influencia/leopoldina_loteamento_2025"
  arquivos:
    - "isocrona_5min_primaria.geojson"
    - "isocrona_10min_secundaria.geojson"
    - "isocrona_15min_terciaria.geojson"
    - "h3_populacao_renda.csv"
    - "consolidado_por_anel.csv"
    - "quotas_preliminares_passo6.csv"
    - "mapa_visual.png"
    - "nota_metodologica.md"

# METADADOS
metadados:
  analista: "Lucas Valentim"
  data_analise: "2025-11-12"
  versao_metodologia: "TIV 4.0"
  status: "ConcluÃ­do"  # Rascunho / Em RevisÃ£o / ConcluÃ­do
  revisor: null
  data_revisao: null

# NOTAS
notas: |
  ConfiguraÃ§Ã£o padrÃ£o para Leopoldina-MG:
  - MunicÃ­pio isolado (sem conurbaÃ§Ã£o)
  - Sem transporte pÃºblico estruturante
  - Pico 18h30 (observado empiricamente)
  - ParticipaÃ§Ãµes esperadas: 60/25/15 (a calibrar)
```

---

### 11.2. Template CSV: Quotas Preliminares (T3-Quotas_Preliminares.csv)

```csv
subarea,h3_index,faixa_renda,faixa_idade,populacao_estimada,quota_sugerida,notas
Primario_Centro,888e1c4a9ffffff,C,25-35,450,23,"PrÃ³ximo a shopping e escolas"
Primario_Norte,888e1c4b1ffffff,D,30-40,380,19,"Ãrea consolidada, horizontal"
Primario_Sul,888e1c4b9ffffff,C,35-45,290,15,"ExpansÃ£o recente, vertical baixo"
Secundario_Leste,888e1c4c3ffffff,C,25-40,320,16,"Acesso via Av. Principal"
Secundario_Oeste,888e1c4c9ffffff,B-C,30-45,250,13,"MÃ©dio padrÃ£o, renda mista"
Terciario_Rural,888e1c5a1ffffff,C-D,25-50,180,9,"Zona rural, lotes grandes"
TOTAL,-,-,-,1870,95,"n=95 para erro 5% (95% conf.)"
```

**Uso:** Dimensionar amostra de pesquisa primÃ¡ria (Passo 6)

**FÃ³rmula tamanho amostral (proporÃ§Ã£o populacional):**
```
n = (ZÂ² Ã— p Ã— q Ã— N) / (eÂ² Ã— (N-1) + ZÂ² Ã— p Ã— q)

Onde:
Z = 1.96 (confianÃ§a 95%)
p = 0.5 (mÃ¡xima variabilidade)
q = 0.5
N = populaÃ§Ã£o total
e = 0.05 (erro 5%)

Para N=1.870:
n â‰ˆ 95 entrevistas (mÃ­nimo)
```

---

### 11.3. Template Markdown: Checklist de ValidaÃ§Ã£o (T3-Checklist.md)

```markdown
# CHECKLIST PASSO 3: ÃREA DE INFLUÃŠNCIA
## [Nome do Projeto] - [Data]

---

## PRÃ‰-REQUISITOS

### Dados de Entrada
- [ ] Coordenadas GPS do terreno validadas
- [ ] Passo 2 (DinÃ¢mica EconÃ´mica) concluÃ­do
- [ ] PopulaÃ§Ã£o total do municÃ­pio conhecida
- [ ] DistribuiÃ§Ã£o de renda mapeada (Faixas A-E)

### Infraestrutura
- [ ] HorÃ¡rio de pico local identificado
- [ ] Barreiras fÃ­sicas prÃ©-mapeadas
- [ ] Sistema de transporte pÃºblico verificado
- [ ] ConurbaÃ§Ãµes identificadas

---

## EXECUÃ‡ÃƒO

### IsÃ³cronas
- [ ] IsÃ³cronas 5/10/15 min geradas (carro)
- [ ] HorÃ¡rio de pico usado (nÃ£o vale)
- [ ] Ferramenta confiÃ¡vel (Google/Mapbox/OSRM)
- [ ] ValidaÃ§Ã£o visual (barreiras respeitadas)

### Transporte PÃºblico (se aplicÃ¡vel)
- [ ] Sistema estruturante confirmado
- [ ] Buffer 500m aplicado (estaÃ§Ãµes)
- [ ] IntersecÃ§Ã£o com isÃ³cronas realizada
- [ ] Ãrea ampliada documentada

### ConurbaÃ§Ãµes (se aplicÃ¡vel)
- [ ] Mancha urbana contÃ­nua confirmada
- [ ] Movimento pendular consultado (IBGE)
- [ ] Migrante Data Fixa consultado
- [ ] Dados multi-municÃ­pio agregados

### Grade H3
- [ ] ResoluÃ§Ã£o apropriada (H8/H9)
- [ ] PopulaÃ§Ã£o por hexÃ¡gono atribuÃ­da
- [ ] Renda mÃ©dia por hexÃ¡gono atribuÃ­da
- [ ] ConsolidaÃ§Ã£o por anel realizada

### Fluxos Populacionais
- [ ] Movimento Pendular analisado
- [ ] Migrante Data Fixa analisado
- [ ] InterpretaÃ§Ã£o conforme framework TIV
- [ ] AÃ§Ã£o recomendada (ajuste de premissas)

### ParticipaÃ§Ãµes Calibradas
- [ ] Percentuais ajustados (nÃ£o fixos 60/30/10)
- [ ] Justificativa tÃ©cnica documentada
- [ ] Faixas respeitadas (50-70 / 20-30 / 10-20)
- [ ] Soma = 100%

### ValidaÃ§Ã£o Qualitativa
- [ ] Entrevistas com taxistas/motoristas (â‰¥3)
- [ ] HorÃ¡rio adequado (pico)
- [ ] Insights documentados
- [ ] TriangulaÃ§Ã£o com dados quantitativos

---

## ENTREGÃVEIS

### Arquivos Geoespaciais
- [ ] `isocrona_5min_primaria.geojson`
- [ ] `isocrona_10min_secundaria.geojson`
- [ ] `isocrona_15min_terciaria.geojson`
- [ ] Metadados completos em cada arquivo

### Dados Tabulares
- [ ] `h3_populacao_renda.csv`
- [ ] `consolidado_por_anel.csv`
- [ ] `quotas_preliminares_passo6.csv`
- [ ] Encoding UTF-8 confirmado

### VisualizaÃ§Ã£o
- [ ] Mapa visual gerado (PNG/PDF, A3)
- [ ] Legenda clara
- [ ] LocalizaÃ§Ã£o do terreno destacada
- [ ] Barreiras fÃ­sicas representadas

### DocumentaÃ§Ã£o
- [ ] SumÃ¡rio executivo gerado
- [ ] Nota metodolÃ³gica completa
- [ ] Premissas explicitadas
- [ ] Riscos identificados
- [ ] PrÃ³ximos passos definidos

---

## APROVAÃ‡ÃƒO FINAL

### Qualidade TÃ©cnica
- [ ] IsÃ³cronas realistas (barreiras respeitadas)
- [ ] PopulaÃ§Ã£o AAI â‰¤ populaÃ§Ã£o municÃ­pio (se sem conurbaÃ§Ã£o)
- [ ] Renda mÃ©dia AAI alinhada com Passo 2
- [ ] ParticipaÃ§Ãµes calibradas e justificadas

### Rastreabilidade
- [ ] Fonte de dados documentada
- [ ] Versionamento de arquivos
- [ ] Metadados completos
- [ ] Reprodutibilidade garantida

### RevisÃ£o
- [ ] RevisÃ£o por analista sÃªnior
- [ ] Cross-check com Passo 2
- [ ] AprovaÃ§Ã£o formal
- [ ] Arquivos organizados

### Go/No-Go
- [ ] âœ… GO: Passo 3 CONCLUÃDO
- [ ] âŒ NO-GO: REFAZER anÃ¡lise (especificar pendÃªncias)

---

**Analista:** [Nome]  
**Data:** [DD/MM/AAAA]  
**Status:** [ ] Rascunho | [ ] Em RevisÃ£o | [ ] ConcluÃ­do  
**Revisor:** [Nome]  
**Data RevisÃ£o:** [DD/MM/AAAA]
```

---

## 12. PRINCÃPIOS FINAIS

### 12.1. Os 5 Mandamentos do Passo 3

1. **TEMPO > DISTÃ‚NCIA**  
   IsÃ³cronas (minutos) sempre prevalecem sobre raios (km). Compradores pensam em "quanto tempo atÃ© o trabalho", nÃ£o "quantos km de casa".

2. **PICO > VALE**  
   Simular mobilidade no horÃ¡rio de PICO (18h-19h), nunca no vale (10h-14h). Subestimar trÃ¢nsito = superestimar demanda.

3. **VALIDAR > ASSUMIR**  
   Movimento Pendular + Migrante Data Fixa sÃ£o OBRIGATÃ“RIOS para validar premissas de demanda externa. Nunca assumir que "pendular vai comprar" sem evidÃªncia.

4. **CALIBRAR > FIXAR**  
   ParticipaÃ§Ãµes 60/30/10 sÃ£o PONTO DE PARTIDA, nÃ£o verdade absoluta. Ajustar por caso (50-70 / 20-30 / 10-20) com justificativa tÃ©cnica.

5. **QUALITATIVO + QUANTITATIVO**  
   Taxistas/motoristas tÃªm conhecimento empÃ­rico valioso. Triangular dados quantitativos (IBGE) com insights qualitativos (entrevistas).

---

### 12.2. CitaÃ§Ãµes-Guia do Passo 3

> **"Ãrea de influÃªncia Ã© definida por TEMPO, nÃ£o por DISTÃ‚NCIA. Compradores pensam em 'quantos minutos atÃ© o trabalho', nÃ£o 'quantos quilÃ´metros'."**  
> â€” Othon Valentim, TIV 4.0

> **"Raio arbitrÃ¡rio de 1km pode representar 5 minutos OU 20 minutos, dependendo da malha viÃ¡ria. IsÃ³cronas capturam essa diferenÃ§a com precisÃ£o."**  
> â€” Metodologia TIV, Passo 3

> **"PopulaÃ§Ã£o flutuante (pendular) NÃƒO Ã‰ DEMANDA automÃ¡tica. Validar com Migrante Data Fixa se existe cultura de migraÃ§Ã£o. Sem migraÃ§Ã£o histÃ³rica, nÃ£o hÃ¡ demanda retenÃ­vel."**  
> â€” Framework de AnÃ¡lise de Fluxos, TIV 4.0

> **"Transporte pÃºblico estruturante (metrÃ´/BRT) AMPLIA Ã¡rea de influÃªncia. Buffer de 500m ao redor das estaÃ§Ãµes captura demanda que se desloca por TP."**  
> â€” Tratamento de Transporte PÃºblico, TIV 4.0

> **"Em conurbaÃ§Ãµes, a Ã¡rea de influÃªncia CRUZA limites municipais. Ignorar municÃ­pios vizinhos subestima demanda em atÃ© 50-70%."**  
> â€” AnÃ¡lise de ConurbaÃ§Ãµes, TIV 4.0 (Caso SÃ£o LuÃ­s-MA)

---

### 12.3. Lembretes CrÃ­ticos para Claude

**Quando acionar esta Skill:**
- âœ… UsuÃ¡rio menciona "Ã¡rea de influÃªncia", "de onde vÃªm os compradores", "polÃ­gono de demanda"
- âœ… UsuÃ¡rio diz "raio de 1km, 2km" â†’ CORRIGIR para isÃ³cronas
- âœ… Etapa sequencial apÃ³s Passo 2 (DinÃ¢mica EconÃ´mica)

**PrÃ©-condiÃ§Ãµes obrigatÃ³rias:**
- âŒ BLOQUEAR se coordenadas do terreno nÃ£o disponÃ­veis
- âŒ BLOQUEAR se Passo 2 nÃ£o concluÃ­do (falta dados demogrÃ¡ficos)

**Red flags crÃ­ticos:**
- âš ï¸ IsÃ³cronas em horÃ¡rio de vale (10h-14h) = Ã¡rea inflada
- âš ï¸ Usar 60/30/10 fixo sem calibraÃ§Ã£o = premissa incorreta
- âš ï¸ Ignorar movimento pendular = demanda fantasma
- âš ï¸ Ignorar conurbaÃ§Ã£o (se existir) = subestimaÃ§Ã£o grave

**IntegraÃ§Ã£o com outros Passos:**
- Passo 4 (VocaÃ§Ã£o): Usa isÃ³cronas para mapear centralidades
- Passo 6 (Demanda): Usa quotas preliminares para dimensionar amostra
- Passo 7 (Oferta): Usa polÃ­gono AAI para buscar concorrentes
- Passo 8 (AbsorÃ§Ã£o): Usa populaÃ§Ã£o anel primÃ¡rio para estimar velocidade

**Outputs crÃ­ticos:**
- 3 arquivos GeoJSON (isÃ³cronas 5/10/15 min)
- CSV com grade H3 (populaÃ§Ã£o/renda por hexÃ¡gono)
- Tabela de quotas preliminares (essencial para Passo 6)
- SumÃ¡rio executivo com participaÃ§Ãµes calibradas

---

## 13. DOCUMENTAÃ‡ÃƒO TÃ‰CNICA

### 13.1. Parte Integrante da Metodologia TIV 4.0

Esta Skill implementa o **Passo 3** da Metodologia TIV (TÃ©cnica Inteligente de Viabilidade), conforme descrito em:

- **KB_CORE v4.0 TIV Completa FINAL** (seÃ§Ã£o Passo 3)
- **Apostila 10 Passos TIV** (pÃ¡ginas 39-46)
- **Projeto TIV + Skills Modulares** (roadmap TIER 1)

### 13.2. VersÃ£o e HistÃ³rico de MudanÃ§as

**VersÃ£o 1.0 (2025-11-12):**
- ImplementaÃ§Ã£o inicial completa
- Metodologia de isÃ³cronas por mobilidade real
- Framework H3 para granularidade espacial
- Tratamento de transporte pÃºblico (buffers 500m)
- AnÃ¡lise de conurbaÃ§Ãµes (multi-municÃ­pio)
- Framework de fluxos populacionais (pendular + migrante)
- CalibraÃ§Ã£o de participaÃ§Ãµes (50-70 / 20-30 / 10-20)
- 2 casos prÃ¡ticos (Leopoldina-MG + SÃ£o LuÃ­s-MA)
- Templates YAML, CSV, Markdown
- Checklist de qualidade (95 itens)

**PrÃ³ximas VersÃµes (Planejadas):**
- v1.1: IntegraÃ§Ã£o com API Google Maps (automaÃ§Ã£o)
- v1.2: Dashboard interativo (Kepler.gl, Streamlit)
- v1.3: Machine Learning (prediÃ§Ã£o de participaÃ§Ãµes)

### 13.3. ReferÃªncias TÃ©cnicas

**Frameworks e Bibliotecas:**
- H3 (Uber): https://h3geo.org/
- Google Maps Platform: https://developers.google.com/maps
- Mapbox Isochrone API: https://docs.mapbox.com/api/navigation/isochrone/
- OSRM (Open Source Routing Machine): http://project-osrm.org/

**Dados PÃºblicos:**
- IBGE Movimento Pendular: https://www.ibge.gov.br/estatisticas/sociais/trabalho/
- IBGE Migrante Data Fixa (Censo 2010/2022)
- Atlas Brasil: http://atlasbrasil.org.br/

**Ferramentas GIS:**
- QGIS (open-source): https://qgis.org/
- Kepler.gl (visualizaÃ§Ã£o): https://kepler.gl/
- GeoPandas (Python): https://geopandas.org/

### 13.4. Contato e Suporte

**Metodologia TIV:** Othon Valentim  
**ImplementaÃ§Ã£o Skill:** Lucas Valentim + Claude  
**Projeto:** TIV 4.0 + Skills Modulares  
**MunicÃ­pio de ReferÃªncia:** Leopoldina-MG  

---

**FIM DA SKILL - PASSO 3: ÃREA DE INFLUÃŠNCIA**

---

**VersÃ£o:** 1.0  
**Data:** 12/11/2025  
**Status:** âœ… OPERACIONAL  
**Metodologia:** TIV 4.0  
**Tier:** TIER 1 (Prioridade CrÃ­tica)  
**PrÃ³ximo Passo:** Passo 4 - VocaÃ§Ã£o ImobiliÃ¡ria  

**Total de pÃ¡ginas:** 58  
**SeÃ§Ãµes:** 13  
**Exemplos prÃ¡ticos:** 2 completos  
**Templates:** 3 prontos para uso  
**Checkboxes de validaÃ§Ã£o:** 95  

ðŸš€ **PRONTA PARA USO OPERACIONAL**
