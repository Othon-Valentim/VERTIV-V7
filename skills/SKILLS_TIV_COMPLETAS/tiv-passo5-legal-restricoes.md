---
name: "tiv-passo5-legal-restricoes"
version: "1.0"
description: "Determina potencial construtivo/loteÃ¡vel via Estudo de Massa sob regras municipais e NBR, validando viabilidade jurÃ­dico-urbanÃ­stica antes do projeto arquitetÃ´nico"
author: "Claude + Othon"
created: "2025-11-12"
updated: "2025-11-12"
tags: ["tiv", "imobiliario", "legal", "urbanistico", "estudo-massa", "leopoldina-mg"]
priority: "CRÃTICO"
---

# SKILL: TIV Passo 5 - AnÃ¡lise Legal Ã— RestriÃ§Ãµes UrbanÃ­sticas

## 1. OBJETIVO E CONTEXTO

### 1.1 FunÃ§Ã£o na Metodologia TIV

Esta Skill executa o **Passo 5 da Metodologia TIV 4.0**: determinaÃ§Ã£o do **potencial construtivo/loteÃ¡vel** atravÃ©s de **Estudo de Massa** sob regras municipais e normas tÃ©cnicas, **ANTES** de qualquer "arte" de projeto.

**PosiÃ§Ã£o na sequÃªncia TIV:**
```
PASSO 1: Garimpo (triagem rÃ¡pida)
PASSO 2: DinÃ¢mica EconÃ´mica (P2i-Lead)
PASSO 3: Ãrea de InfluÃªncia (isÃ³cronas)
PASSO 4: VocaÃ§Ã£o ImobiliÃ¡ria (3 Pilares)
         â†“
â†’ PASSO 5: LEGAL Ã— RESTRIÃ‡Ã•ES â† [VOCÃŠ ESTÃ AQUI]
         â†“
PASSO 6: Demanda (quantificaÃ§Ã£o)
PASSO 7: Oferta (concorrÃªncia)
PASSO 8: AbsorÃ§Ã£o (velocidade)
PASSO 9: ValidaÃ§Ã£o (premissas)
PASSO 10: FCD (viabilidade final)
```

### 1.2 O Que Esta Skill Faz

**Objetivo Central (KB CORE v4.0):**
> "Determinar o **potencial construtivo/loteÃ¡vel** do imÃ³vel por meio de **Estudo de Massa** sob as **regras municipais** (Plano Diretor, LUOS, CÃ³digo de Obras, Posturas) e **normas tÃ©cnicas aplicÃ¡veis (ABNT/NBR)**, **antes** de qualquer "arte" de projeto."

**O Passo 5 traduz:**
- **"O que pode"** (limites normativos) 
- Em **"quanto cabe"** (Ã¡rea/volumetria mÃ­nima viÃ¡vel)
- Deixando a concepÃ§Ã£o arquitetÃ´nica para **apÃ³s o fit de mercado**

**MissÃ£o do Arquiteto neste passo:**
> "A missÃ£o do arquiteto Ã© **maximizar o potencial construtivo do negÃ³cio**, levando em conta todas as regras dispostas na legislaÃ§Ã£o de ocupaÃ§Ã£o do solo das prefeituras."
> *Apostila TIV - Passo 5, p.58*

### 1.3 Por Que Este Passo Ã© CrÃ­tico

**PrincÃ­pio TIV:**
> "RestriÃ§Ãµes legais SÃƒO FATOS, nÃ£o negociÃ¡veis. Identificar cedo evita trabalho perdido."

**Sem validaÃ§Ã£o legal:**
- âŒ Produto tecnicamente inviÃ¡vel (zoneamento veda)
- âŒ APP compromete 60%+ da Ã¡rea (descoberto tarde)
- âŒ LitÃ­gio dominial paralisa projeto por anos
- âŒ Infraestrutura ausente = custo 3x estimado

**ValidaÃ§Ã£o legal BEM executada:**
- âœ… Potencial construtivo real conhecido
- âœ… RestriÃ§Ãµes identificadas e mitigadas
- âœ… Cronograma de aprovaÃ§Ãµes realista
- âœ… Custos de conformidade no budget

---

## 2. QUANDO ACIONAR ESTA SKILL

### 2.1 Triggers ExplÃ­citos

**Comandos diretos:**
- "FaÃ§a a anÃ¡lise legal do terreno"
- "Qual o potencial construtivo deste imÃ³vel?"
- "Preciso do Estudo de Massa"
- "Quais restriÃ§Ãµes urbanÃ­sticas aplicam?"
- "Validar viabilidade jurÃ­dico-urbanÃ­stica"
- "Execute o Passo 5 TIV"

**Perguntas tÃ©cnicas:**
- "Posso construir [X] nesta Ã¡rea?"
- "Quantos lotes cabem neste terreno?"
- "Qual o CA e TO desta zona?"
- "HÃ¡ APP neste imÃ³vel?"

### 2.2 Triggers ImplÃ­citos

- UsuÃ¡rio tem terreno definido e quer validar viabilidade
- **Passo 4 (VocaÃ§Ã£o) concluÃ­do** â†’ tipo de produto jÃ¡ definido
- DÃºvida sobre zoneamento ou restriÃ§Ãµes ambientais
- PreparaÃ§Ã£o para estudo de viabilidade completo

### 2.3 PrÃ©-requisitos OBRIGATÃ“RIOS

**Dados mÃ­nimos para acionar:**
- âœ… LocalizaÃ§Ã£o precisa (endereÃ§o OU coordenadas GPS)
- âœ… Ãrea total do terreno (mÂ²)
- âœ… Tipo de produto pretendido (loteamento/incorporaÃ§Ã£o/comercial)

**Dados DESEJÃVEIS (nÃ£o impeditivos):**
- MatrÃ­cula atualizada (< 90 dias)
- Levantamento topogrÃ¡fico
- Fotos do terreno

---

## 3. FRAMEWORK METODOLÃ“GICO: ESTUDO DE MASSA

### 3.1 Nota de IntegraÃ§Ã£o com Passo 4 (Fronteira Clara)

**Regra de Ouro TIV:**
> "**Passo 4 define 'o quÃª'** (tipologia, padrÃ£o, faixa de preÃ§o). **Passo 5 comprova 'quanto cabe'** (Estudo de Massa + Mapa de RestriÃ§Ãµes). A 'arte' sÃ³ apÃ³s o fit final."

**DivisÃ£o de responsabilidades:**
- **Passo 4 (VocaÃ§Ã£o):** AnÃ¡lise estratÃ©gica â†’ produto candidato (horizontal/vertical, econÃ´mico/mÃ©dio/alto)
- **Passo 5 (Legal):** AnÃ¡lise tÃ©cnico-legal â†’ potencial construtivo viÃ¡vel sob normas
- **Anteprojeto:** Apenas APÃ“S validaÃ§Ã£o Passo 5 + fit de mercado (Passo 6)

**ERRO COMUM:**
âŒ Partir para "arte" arquitetÃ´nica sem Estudo de Massa
âœ… CORRETO: Estudo de Massa â†’ Fit de Mercado â†’ Arte

### 3.2 As 7 Etapas do Estudo de Massa

#### ETAPA 1: Coleta de Dados do Terreno

**Inputs necessÃ¡rios:**

**Dados BÃ¡sicos:**
- EndereÃ§o completo (rua, nÂº, bairro, CEP)
- Coordenadas GPS (lat/long) - usar Google Maps
- Ãrea total (mÂ²) - conforme matrÃ­cula
- Testada (metros lineares de frente)
- Topografia (plano/aclive/declive/acidentado)

**Dados Dominiais:**
- NÃºmero da matrÃ­cula (CartÃ³rio RI)
- Data da matrÃ­cula (< 90 dias = atualizada)
- ProprietÃ¡rio titular
- Ã”nus/gravames (hipoteca, penhora, servidÃ£o)

**Contexto:**
- Uso pretendido (residencial/comercial/misto/industrial)
- Tipo produto (loteamento/incorporaÃ§Ã£o/casa isolada)
- Prazo (urgente/normal/longo)

**Fontes:**
- MatrÃ­cula atualizada (CartÃ³rio)
- Google Maps/Earth (coordenadas, topografia visual)
- Vistoria in loco (fotos, mediÃ§Ãµes)
- Prefeitura (consulta prÃ©via)

---

#### ETAPA 2: IdentificaÃ§Ã£o da Zona UrbanÃ­stica

**Objetivo:** Determinar em qual zona do Plano Diretor/LUOS o terreno estÃ¡ inserido.

**Para Leopoldina-MG:**

**9 Zonas Urbanas (LC 09/2006 + LC 14/2009):**

| Sigla | Nome | CaracterÃ­stica |
|-------|------|----------------|
| **ZPH** | Zona PreservaÃ§Ã£o PatrimÃ´nio HistÃ³rico | Centro histÃ³rico, bens tombados |
| **ZAR** | Zona Adensamento Restrito | Baixa densidade, controle rÃ­gido |
| **ZCA** | Zona Controle Adensamento | Densidade controlada |
| **ZEIS** | Zona Especial Interesse Social | HabitaÃ§Ã£o popular |
| **ZAE** | Zona Atividades EconÃ´micas | ComÃ©rcio, serviÃ§os, indÃºstria |
| **ZAV** | Zona Ãreas Verdes | Parques, lazer |
| **ZOC** | Zona Controle OcupaÃ§Ã£o | OcupaÃ§Ã£o controlada |
| **ZVC** | Zona ExpansÃ£o VerticalizaÃ§Ã£o Controlada | ExpansÃ£o com gabarito limitado |
| **ZEU** | Zona ExpansÃ£o Urbana | ExpansÃ£o futura |

**+ Zona Especial:**
- **ZUE (LC 63/2020):** Zona UrbanizaÃ§Ã£o EspecÃ­fica para condomÃ­nios de lotes

**Como identificar:**
1. **Consulta PrÃ©via Formal** Ã  Secretaria de Obras (MAIS CONFIÃVEL)
2. Mapa de Macrozoneamento (PDF oficial - requer interpretaÃ§Ã£o visual)
3. InferÃªncia por endereÃ§o + bairro (conhecimento local)

âš ï¸ **ALERTA LEOPOLDINA:** Mapa de zoneamento NÃƒO estÃ¡ georreferenciado. Consulta formal Ã  Prefeitura Ã© RECOMENDADA.

---

#### ETAPA 3: ExtraÃ§Ã£o dos ParÃ¢metros UrbanÃ­sticos

**Objetivo:** Obter coeficientes e limites construtivos aplicÃ¡veis Ã  zona.

**ParÃ¢metros a extrair:**

**1. Taxa de OcupaÃ§Ã£o (TO):**
- DefiniÃ§Ã£o: % mÃ¡xima do lote que pode ser coberta pela edificaÃ§Ã£o
- FÃ³rmula: `Ãrea Ocupada = Ãrea Terreno Ã— (TO/100)`
- Fonte: LUOS vigente

**2. Coeficiente de Aproveitamento (CA):**
- CA BÃ¡sico: aproveitamento sem contrapartida
- CA MÃ¡ximo: com outorga onerosa
- FÃ³rmula: `Ãrea ConstruÃ­da Total = Ãrea Terreno Ã— CA`
- Fonte: LUOS vigente

**3. Gabarito:**
- Altura mÃ¡xima em pavimentos OU metros
- Exemplo ZC: 8 pavimentos mÃ¡ximo
- Fonte: CÃ³digo de Obras (Lei 263/1957) + LUOS

**4. Recuos ObrigatÃ³rios:**
- Frontal: distÃ¢ncia mÃ­nima da testada
- Laterais: distÃ¢ncia das divisas laterais
- Fundos: distÃ¢ncia da divisa de fundos
- **Exemplo (CÃ³digo Obras 1957):** Residencial = 3m frontal obrigatÃ³rio

**5. Lote MÃ­nimo (para parcelamento):**
- **CÃ³digo Obras 1957 (Leopoldina):**
  - Residencial urbano: **360mÂ²**, testada **12m**
  - Comercial urbano: **200mÂ²**, testada **8m**
  - Industrial suburbano: **600mÂ²**, testada **15m**
- **ZUE (LC 63/2020):** Lote mÃ­n **500mÂ²**, testada **12m**

**6. Usos Permitidos:**
- Residencial (unifamiliar/multifamiliar)
- Comercial (local/geral/especializado)
- Industrial (leve/mÃ©dia/pesada)
- Misto

**7. Vagas de Estacionamento:**
- Quantidade mÃ­nima por mÂ² ou unidade
- Fonte: LUOS (tabela especÃ­fica)

**STATUS LEOPOLDINA (nov/2025):**
- LUOS vigente: 2007 (18 anos, defasada)
- Nova LUOS: PLC 01/2024 em tramitaÃ§Ã£o
- **RECOMENDAÃ‡ÃƒO:** Consultar AMBAS

**Como obter:**
1. Consulta PrÃ©via Formal (MAIS CONFIÃVEL)
2. Download LUOS vigente (portal CÃ¢mara Municipal)
3. Download Projeto LUOS 01/2024 (acompanhar tramitaÃ§Ã£o)
4. Consultar CÃ³digo de Obras (Lei 263/1957)

---

#### ETAPA 4: IdentificaÃ§Ã£o de RestriÃ§Ãµes

**Objetivo:** Mapear Ã¡reas nÃ£o edificÃ¡veis e condicionantes.

**A. RestriÃ§Ãµes Ambientais**

**APP (Ãreas de PreservaÃ§Ã£o Permanente):**
- **Lei Municipal 4.842/2024** + Lei Federal 12.651/2012
- Faixas marginais cursos d'Ã¡gua: **10m e 7,5m** (conforme enquadramento)
- Nascentes: raio 50m
- Topos de morro, encostas > 45Â°
- VegetaÃ§Ã£o nativa (consulta IEF-MG necessÃ¡ria)

**Licenciamento Ambiental:**
- **Lei 15.190/2025** (Lei Geral Licenciamento Ambiental)
- Empreendimentos > 100 unidades: LP + LI + LO obrigatÃ³rias
- Prazos: LP atÃ© 90 dias, LI atÃ© 120 dias, LO atÃ© 60 dias

**B. RestriÃ§Ãµes UrbanÃ­sticas**

**Faixas NÃ£o EdificÃ¡veis:**
- Rodovias: conforme DER-MG / DNIT
- Ferrovias: Lei Federal 10.233/2001
- Linhas transmissÃ£o: conforme concessionÃ¡ria
- Adutoras/dutos: conforme saneamento

**PatrimÃ´nio HistÃ³rico:**
- **Bens tombados Leopoldina:** Escola Botelho Reis, Prefeitura, estaÃ§Ãµes ferroviÃ¡rias
- Entorno bens tombados: restriÃ§Ãµes nÃ£o padronizadas (consultar IPHAN/IEPHA)
- Decretos: 1435/1999, 1752-1754/2000

**C. RestriÃ§Ãµes GeotÃ©cnicas**

- Topografia ingreme (> 30%): custos elevados, riscos geolÃ³gicos
- Ãreas inundÃ¡veis: consultar mapas oficiais
- Solos problemÃ¡ticos: requer sondagem

**D. SituaÃ§Ã£o Dominial**

- MatrÃ­cula atualizada (< 90 dias)
- ConfrontaÃ§Ãµes conferidas
- ServidÃµes registradas
- Ã”nus reais (hipoteca, penhora)
- Regularidade fundiÃ¡ria

---

#### ETAPA 5: CÃ¡lculo do Potencial Construtivo

**Objetivo:** Quantificar Ã¡rea edificÃ¡vel mÃ¡xima respeitando parÃ¢metros legais.

**5.1 CÃ¡lculo Ãrea LÃ­quida EdificÃ¡vel**

```
Ãrea LÃ­quida = Ãrea Total - Î£ RestriÃ§Ãµes

Onde:
- Ãrea Total = conforme matrÃ­cula (mÂ²)
- RestriÃ§Ãµes = APP + Faixas nÃ£o edificÃ¡veis + Recuos + Outras
```

**Exemplo:**
```
Terreno: 10.000 mÂ²
APP cÃ³rrego (10m Ã— 100m margem): -1.000 mÂ²
Faixa rodovia (15m Ã— 80m): -1.200 mÂ²
Ãrea LÃ­quida = 10.000 - 1.000 - 1.200 = 7.800 mÂ²
```

**5.2 CÃ¡lculo Ãrea Ocupada (ProjeÃ§Ã£o)**

```
Ãrea Ocupada = Ãrea LÃ­quida Ã— (TO / 100)
```

**Exemplo:**
```
Ãrea LÃ­quida: 7.800 mÂ²
TO permitido: 60%
Ãrea Ocupada = 7.800 Ã— 0,60 = 4.680 mÂ²
```

**5.3 CÃ¡lculo Ãrea Total ConstruÃ­da**

```
Ãrea Total ConstruÃ­da = Ãrea LÃ­quida Ã— CA
```

**Exemplo:**
```
Ãrea LÃ­quida: 7.800 mÂ²
CA permitido: 2,0
Ãrea Total = 7.800 Ã— 2,0 = 15.600 mÂ²
```

**5.4 NÃºmero de Pavimentos**

```
NÂº Pavimentos = min(
    Ãrea Total ConstruÃ­da / Ãrea Ocupada,
    Gabarito MÃ¡ximo
)
```

**Exemplo:**
```
Ãrea Total: 15.600 mÂ²
Ãrea Ocupada: 4.680 mÂ²
Gabarito: 8 pavimentos

CÃ¡lculo: 15.600 / 4.680 = 3,33 pavimentos
Limitado por gabarito: min(3,33, 8) = 3 pavimentos
```

**5.5 Para Loteamentos:**

```
NÂº Lotes = (Ãrea LoteÃ¡vel / Lote MÃ©dio)

Onde:
- Ãrea LoteÃ¡vel = Ãrea LÃ­quida Ã— (1 - % Ãreas PÃºblicas)
- % Ãreas PÃºblicas = arruamento + Ã¡reas verdes (tipicamente 30-35%)
- Lote MÃ©dio â‰¥ Lote MÃ­nimo Legal
```

**Exemplo:**
```
Ãrea LÃ­quida: 50.000 mÂ²
Ãreas pÃºblicas: 35%
Ãrea LoteÃ¡vel: 50.000 Ã— 0,65 = 32.500 mÂ²
Lote MÃ©dio: 250 mÂ²
NÂº Lotes = 32.500 / 250 = 130 lotes
```

---

#### ETAPA 6: ElaboraÃ§Ã£o do Mapa de RestriÃ§Ãµes

**Objetivo:** Visualizar espacialmente as restriÃ§Ãµes identificadas.

**Camadas do Mapa:**
- ðŸ”´ APP (cursos d'Ã¡gua, nascentes, encostas)
- ðŸŸ  Faixas nÃ£o edificÃ¡veis (rodovias, ferrovias, linhas)
- ðŸŸ¡ ServidÃµes (passagem, dutos)
- ðŸŸ¢ Ãrea edificÃ¡vel lÃ­quida
- ðŸ”µ Recuos obrigatÃ³rios
- âšª PatrimÃ´nio histÃ³rico (raio influÃªncia)

**Ferramentas:**
- Google My Maps (camadas KML)
- QGIS (SIG open source)
- Desenho CAD simplificado

**Formato de SaÃ­da:**
- Arquivo .geojson ou .shp (georreferenciado)
- Imagem .png ou .jpg (para relatÃ³rio)
- Legenda clara e escala grÃ¡fica

---

#### ETAPA 7: ConsolidaÃ§Ã£o do Parecer TÃ©cnico

**Objetivo:** Sintetizar anÃ¡lise em documento decisÃ³rio de 1-2 pÃ¡ginas.

**Estrutura do Parecer:**

**1. IdentificaÃ§Ã£o**
- EndereÃ§o do imÃ³vel
- Ãrea total (mÂ²)
- MatrÃ­cula (nÂº e data)
- Produto pretendido

**2. ParÃ¢metros Legais Aplicados**
- Zona urbanÃ­stica identificada
- TO, CA, gabarito, recuos (com citaÃ§Ã£o da fonte legal)
- Lote mÃ­nimo (se loteamento)

**3. RestriÃ§Ãµes Identificadas**
- APP: Ã¡rea (mÂ²) e % do terreno
- Faixas nÃ£o edificÃ¡veis: Ã¡rea (mÂ²)
- Outras restriÃ§Ãµes relevantes

**4. Potencial Construtivo Calculado**
- Ãrea lÃ­quida edificÃ¡vel (mÂ²)
- Ãrea ocupada mÃ¡xima (mÂ²)
- Ãrea total construÃ­da mÃ¡xima (mÂ²)
- NÂº unidades/lotes estimado

**5. Status de Viabilidade**
- âœ… **VIÃVEL:** sem impedimentos, restriÃ§Ãµes dentro do aceitÃ¡vel
- âš ï¸ **VIÃVEL COM RESTRIÃ‡Ã•ES:** condicionantes identificadas, custos adicionais
- âŒ **INVIÃVEL:** impedimentos tÃ©cnicos ou legais insuperÃ¡veis

**6. CondiÃ§Ãµes e Ressalvas**
- Exemplo: "ViÃ¡vel **se** recuo frontal 5m; cota soleira +0,50m; compensaÃ§Ã£o APP"

**7. Custos Adicionais Estimados**
- Infraestrutura ausente
- CompensaÃ§Ãµes ambientais
- RegularizaÃ§Ãµes necessÃ¡rias

**8. Cronograma de Licenciamento**
- LP (LicenÃ§a PrÃ©via): prazo estimado
- LI (LicenÃ§a InstalaÃ§Ã£o): prazo estimado
- LO (LicenÃ§a OperaÃ§Ã£o): prazo estimado

**9. Anexos**
- MatrÃ­cula atualizada
- Mapa de RestriÃ§Ãµes
- LegislaÃ§Ã£o consultada
- Fotos do terreno

---

## 4. INPUTS NECESSÃRIOS

### 4.1 Dados ObrigatÃ³rios

- **LocalizaÃ§Ã£o:** EndereÃ§o completo OU coordenadas GPS
- **Ãrea total:** mÂ² conforme matrÃ­cula
- **Produto pretendido:** Loteamento/IncorporaÃ§Ã£o/Comercial/Industrial
- **Zona urbanÃ­stica:** Identificada ou a identificar
- **RestriÃ§Ãµes visÃ­veis:** APP, rodovias, topografia crÃ­tica

### 4.2 Dados DesejÃ¡veis

- **MatrÃ­cula atualizada** (< 90 dias)
- **Levantamento topogrÃ¡fico** (curvas de nÃ­vel)
- **Fotos do terreno** (mÃ­nimo 8, 360Â°)
- **Consulta prÃ©via Prefeitura** (protocolo)
- **Sondagem geotÃ©cnica** (se terreno > 5.000mÂ²)

### 4.3 Fontes de Dados

**LegislaÃ§Ã£o Municipal (Leopoldina-MG):**
- LC 09/2006 - Plano Diretor Participativo
- LC 14/2009 - AlteraÃ§Ã£o Mapa Plano Diretor
- Lei 263/1957 - CÃ³digo de Obras
- Lei 4.842/2024 - APPs Urbanas
- LC 63/2020 - Zona UrbanizaÃ§Ã£o EspecÃ­fica
- PLC 01/2024 - Nova LUOS (em tramitaÃ§Ã£o)

**LegislaÃ§Ã£o Federal:**
- Lei 12.651/2012 - CÃ³digo Florestal
- Lei 15.190/2025 - Licenciamento Ambiental
- Lei 6.766/1979 - Parcelamento Solo Urbano
- Lei 4.591/1964 - IncorporaÃ§Ãµes ImobiliÃ¡rias
- Lei 10.257/2001 - Estatuto da Cidade

**Normas TÃ©cnicas (ABNT):**
- NBR 12.721 - AvaliaÃ§Ã£o de Custos
- NBR 12.271 - Ãreas Privativas (Quadro II)
- NBR 9050 - Acessibilidade
- NBR 14.653 - AvaliaÃ§Ã£o de Bens

**Ã“rgÃ£os Consultados:**
- Prefeitura Leopoldina (Secretaria Obras)
- CartÃ³rio Registro de ImÃ³veis
- IEF-MG (vegetaÃ§Ã£o nativa)
- SEMAD (licenciamento ambiental)
- COPASA (Ã¡gua/esgoto)
- CEMIG (energia elÃ©trica)

---

## 5. PROCESSO DE ANÃLISE (PASSO A PASSO)

### 5.1 Checklist de ExecuÃ§Ã£o

**FASE 1: PreparaÃ§Ã£o**
- [ ] Receber inputs do usuÃ¡rio (localizaÃ§Ã£o, Ã¡rea, produto)
- [ ] Confirmar Passo 4 (VocaÃ§Ã£o) concluÃ­do
- [ ] Definir escopo: anÃ¡lise rÃ¡pida (Garimpo) ou completa (Viabilidade)

**FASE 2: Dados JurÃ­dico-Dominiais**
- [ ] Obter matrÃ­cula atualizada (< 90 dias)
- [ ] Verificar titularidade, Ã´nus, gravames
- [ ] Confirmar confrontaÃ§Ãµes e medidas
- [ ] Identificar servidÃµes registradas

**FASE 3: Zoneamento e ParÃ¢metros**
- [ ] Identificar zona urbanÃ­stica (ZPH/ZAR/ZCA/ZEIS/ZAE/ZAV/ZOC/ZVC/ZEU/ZUE)
- [ ] Extrair TO, CA, gabarito, recuos
- [ ] Confirmar usos permitidos
- [ ] Verificar vagas de estacionamento
- [ ] Consultar legislaÃ§Ã£o vigente + em tramitaÃ§Ã£o

**FASE 4: RestriÃ§Ãµes Ambientais**
- [ ] Mapear APPs (cursos d'Ã¡gua, nascentes, encostas)
- [ ] Verificar vegetaÃ§Ã£o nativa (consulta IEF-MG)
- [ ] Identificar Ã¡reas inundÃ¡veis
- [ ] Avaliar declividade/topografia
- [ ] Definir necessidade licenciamento ambiental

**FASE 5: RestriÃ§Ãµes UrbanÃ­sticas**
- [ ] Mapear faixas nÃ£o edificÃ¡veis (rodovias, ferrovias, linhas)
- [ ] Identificar servidÃµes nÃ£o registradas
- [ ] Verificar entorno bens tombados
- [ ] Avaliar infraestrutura disponÃ­vel

**FASE 6: CÃ¡lculos TÃ©cnicos**
- [ ] Calcular Ã¡rea lÃ­quida edificÃ¡vel
- [ ] Calcular Ã¡rea ocupada (TO)
- [ ] Calcular Ã¡rea total construÃ­da (CA)
- [ ] Determinar nÂº pavimentos (gabarito)
- [ ] Estimar nÂº unidades/lotes

**FASE 7: Mapa de RestriÃ§Ãµes**
- [ ] Elaborar mapa com todas as camadas
- [ ] Georreferenciar arquivo (.geojson/.shp)
- [ ] Gerar imagem para relatÃ³rio

**FASE 8: Parecer TÃ©cnico**
- [ ] Consolidar anÃ¡lise em documento 1-2 pÃ¡ginas
- [ ] Definir status: ViÃ¡vel / ViÃ¡vel com RestriÃ§Ãµes / InviÃ¡vel
- [ ] Listar condiÃ§Ãµes e ressalvas
- [ ] Estimar custos adicionais
- [ ] Projetar cronograma licenciamento

**FASE 9: ValidaÃ§Ã£o Interna**
- [ ] Aplicar testes lÃ³gicos (Ã¡rea lÃ­quida > 0, TO respeitado, etc.)
- [ ] Conferir citaÃ§Ãµes legais (leis, artigos, datas)
- [ ] Verificar consistÃªncia com Passo 4 (produto viÃ¡vel?)
- [ ] Revisar red flags identificados

**FASE 10: Entrega e Handoff**
- [ ] Compartilhar Parecer com usuÃ¡rio
- [ ] Destacar decisÃ£o Go/Conditional/Stop
- [ ] Indicar prÃ³ximos passos (Passo 6 ou iteraÃ§Ã£o Passo 4)
- [ ] Arquivar documentaÃ§Ã£o (matrÃ­cula, mapa, legislaÃ§Ã£o)

---

## 6. OUTPUTS ESPERADOS

### 6.1 Estudo de Massa (Quadros de Ãreas)

**Formato Tabela:**

```markdown
| ParÃ¢metro | Valor | Unidade | Fonte Legal |
|-----------|-------|---------|-------------|
| **Ãrea Total** | 10.000 | mÂ² | MatrÃ­cula nÂº XXXX |
| **Zona UrbanÃ­stica** | ZEU | - | LC 09/2006 |
| **TO Permitido** | 60 | % | LUOS 2007 |
| **CA Permitido** | 1,5 | - | LUOS 2007 |
| **Gabarito MÃ¡ximo** | 3 | pavimentos | CÃ³digo Obras 263/1957 |
| **Recuos** | 5m frontal, 3m laterais | m | LUOS 2007 |
| **RestriÃ§Ãµes APP** | 1.500 | mÂ² | Lei 12.651/2012 |
| **Faixas NÃ£o Edif.** | 800 | mÂ² | DNIT |
| **Ãrea LÃ­quida** | 7.700 | mÂ² | Calculado |
| **Ãrea Ocupada MÃ¡x** | 4.620 | mÂ² | Ãrea LÃ­quida Ã— TO |
| **Ãrea Total Const.** | 11.550 | mÂ² | Ãrea LÃ­quida Ã— CA |
| **NÂº Pavimentos** | 2,5 â‰ˆ 3 | - | Ãrea Total / Ocupada |
| **NÂº Lotes Estimado** | 30 | unidades | Lote mÃ©dio 250mÂ² |
```

### 6.2 Mapa de RestriÃ§Ãµes

**Elementos obrigatÃ³rios:**
- PerÃ­metro do terreno
- APPs identificadas (cor vermelha)
- Faixas nÃ£o edificÃ¡veis (cor laranja)
- Ãrea edificÃ¡vel lÃ­quida (cor verde)
- Recuos obrigatÃ³rios (tracejado)
- Legenda clara
- Escala grÃ¡fica
- Norte geogrÃ¡fico

**Formatos:**
- Arquivo georreferenciado (.geojson ou .shp)
- Imagem para relatÃ³rio (.png ou .jpg, mÃ­n. 1920Ã—1080)
- Link Google My Maps (quando aplicÃ¡vel)

### 6.3 Parecer de Viabilidade JurÃ­dico-UrbanÃ­stica

**Estrutura (1-2 pÃ¡ginas):**

```markdown
# PARECER DE VIABILIDADE JURÃDICO-URBANÃSTICA

## 1. IDENTIFICAÃ‡ÃƒO
- **ImÃ³vel:** [EndereÃ§o completo]
- **Ãrea Total:** [X.XXX] mÂ²
- **MatrÃ­cula:** nÂº [XXXXX], CartÃ³rio [X]Âº RI Leopoldina-MG
- **Produto Pretendido:** [Loteamento/IncorporaÃ§Ã£o/Comercial]
- **Data AnÃ¡lise:** [DD/MM/AAAA]

## 2. ENQUADRAMENTO LEGAL
- **Zona UrbanÃ­stica:** [ZEU / ZAR / ZCA / etc.]
- **Base Legal:** LC 09/2006, Art. [X]
- **TO Permitido:** [60]%
- **CA Permitido:** [1,5]
- **Gabarito:** [3] pavimentos ou [9] metros
- **Recuos:** Frontal [5]m, Laterais [3]m, Fundos [3]m

## 3. RESTRIÃ‡Ã•ES IDENTIFICADAS
- **APP (Lei 12.651/2012):** [1.500] mÂ² ([15]% do terreno)
- **Faixas NÃ£o EdificÃ¡veis:** [800] mÂ² (rodovia BR-XXX)
- **Topografia:** Plana (0-3% declividade)
- **VegetaÃ§Ã£o:** Pasto degradado (sem restriÃ§Ã£o)

## 4. POTENCIAL CONSTRUTIVO
- **Ãrea LÃ­quida EdificÃ¡vel:** [7.700] mÂ²
- **Ãrea Ocupada MÃ¡xima:** [4.620] mÂ²
- **Ãrea Total ConstruÃ­da:** [11.550] mÂ²
- **NÂº Pavimentos:** [3] pavimentos
- **NÂº Unidades/Lotes:** [30] lotes de 250mÂ² (mÃ©dia)

## 5. STATUS DE VIABILIDADE
âœ… **VIÃVEL COM RESTRIÃ‡Ã•ES**

**CondiÃ§Ãµes:**
- Respeitar faixa APP 10m (cÃ³rrego norte)
- Recuo frontal mÃ­nimo 5m
- Licenciamento ambiental (LP+LI+LO) necessÃ¡rio
- CompensaÃ§Ã£o APP: plantio 500 mudas nativas

## 6. CUSTOS ADICIONAIS ESTIMADOS
- Infraestrutura Ã¡gua/esgoto: R$ 150.000
- Licenciamento ambiental: R$ 30.000
- CompensaÃ§Ã£o APP (plantio): R$ 20.000
- **TOTAL:** R$ 200.000 (2% VGV estimado)

## 7. CRONOGRAMA LICENCIAMENTO
- Consulta PrÃ©via: 30 dias
- LP (LicenÃ§a PrÃ©via): 90 dias
- LI (LicenÃ§a InstalaÃ§Ã£o): 120 dias
- Obras: 18 meses
- LO (LicenÃ§a OperaÃ§Ã£o): 60 dias
- **TOTAL:** 24 meses atÃ© comercializaÃ§Ã£o

## 8. PRÃ“XIMOS PASSOS
â†’ **Passo 6 (Demanda):** Validar mercado para 30 lotes
â†’ Protocolar consulta prÃ©via Prefeitura
â†’ Contratar levantamento topogrÃ¡fico completo

## 9. ANEXOS
- A: MatrÃ­cula atualizada
- B: Mapa de RestriÃ§Ãµes
- C: LegislaÃ§Ã£o consultada (PDFs)
- D: Fotos do terreno (8 unidades)

---
**ResponsÃ¡vel TÃ©cnico:** [Nome]
**CREA/CAU:** [Registro]
**Data:** [DD/MM/AAAA]
```

### 6.4 Tabela de LegislaÃ§Ã£o Consultada

```markdown
| Diploma Legal | Assunto | Artigos AplicÃ¡veis | Data Consulta |
|---------------|---------|-------------------|---------------|
| LC 09/2006 | Plano Diretor | Arts. 15-20 | 12/11/2025 |
| Lei 263/1957 | CÃ³digo de Obras | Arts. 45-52 | 12/11/2025 |
| Lei 4.842/2024 | APPs Urbanas | Arts. 1Âº-5Âº | 12/11/2025 |
| Lei 12.651/2012 | CÃ³digo Florestal | Arts. 4Âº, 6Âº | 12/11/2025 |
| Lei 15.190/2025 | Licenciamento Ambiental | Arts. 10-15 | 12/11/2025 |
```

---

## 7. ALERTAS E VALIDAÃ‡Ã•ES

### 7.1 Red Flags por NÃ­vel de Criticidade

#### NÃVEL 1: IMPEDITIVOS (STOP) ðŸ›‘

**Zoneamento:**
- âŒ Uso pretendido VETADO pela LUOS
- âŒ Potencial construtivo ZERO apÃ³s restriÃ§Ãµes
- âŒ Gabarito insuficiente para viabilizar produto vertical

**Ambiental:**
- âŒ APP compromete > 60% da Ã¡rea edificÃ¡vel
- âŒ VegetaÃ§Ã£o nativa estÃ¡gio avanÃ§ado (corte proibido)
- âŒ Ãrea de risco geolÃ³gico alto (deslizamento iminente)

**Dominial:**
- âŒ LitÃ­gio de propriedade em curso
- âŒ Penhora judicial sem soluÃ§Ã£o prÃ³xima
- âŒ ConfrontaÃ§Ãµes conflitantes com sobreposiÃ§Ã£o

**Infraestrutura:**
- âŒ Ãgua e esgoto ausentes + inviÃ¡vel estender
- âŒ Acesso impossÃ­vel (terreno encravado)

**AÃ‡ÃƒO:** **DESCARTAR** terreno. NÃƒO prosseguir anÃ¡lise.

---

#### NÃVEL 2: RISCO ALTO (CONDITIONAL) âš ï¸

**Legal:**
- âš ï¸ LegislaÃ§Ã£o em transiÃ§Ã£o (nova LUOS tramitando)
- âš ï¸ Hipoteca sem anuÃªncia prÃ©via banco
- âš ï¸ MatrÃ­cula desatualizada (> 1 ano)

**Ambiental:**
- âš ï¸ APP compromete 30-60% da Ã¡rea
- âš ï¸ VegetaÃ§Ã£o nativa estÃ¡gio mÃ©dio (autorizaÃ§Ã£o complexa)
- âš ï¸ Topografia Ã­ngreme (custos +100-200%)

**Financeiro:**
- âš ï¸ Custos adicionais > 15% VGV
- âš ï¸ Prazo licenciamento > 12 meses

**AÃ‡ÃƒO:** **APROFUNDAR** anÃ¡lise. Mitigar riscos. Considerar desconto no preÃ§o terreno.

---

#### NÃVEL 3: RISCO MODERADO (MONITORAR) âš¡

**Legal:**
- âš¡ Ã”nus reais existentes mas solucionÃ¡veis
- âš¡ DocumentaÃ§Ã£o complementar necessÃ¡ria
- âš¡ Entorno bem tombado (restriÃ§Ãµes nÃ£o claras)

**Ambiental:**
- âš¡ APP compromete < 30% da Ã¡rea
- âš¡ VegetaÃ§Ã£o nativa estÃ¡gio inicial (autorizaÃ§Ã£o simples)
- âš¡ Topografia moderada (custos +30-50%)

**Financeiro:**
- âš¡ Custos adicionais 5-15% VGV
- âš¡ Prazo licenciamento 6-12 meses

**AÃ‡ÃƒO:** **PROSSEGUIR** com anÃ¡lise. Incluir custos no budget. Monitorar prazos.

---

### 7.2 Testes de ValidaÃ§Ã£o LÃ³gica

**Aplicar automaticamente antes de concluir Passo 5:**

```python
# Teste 1: Ãrea edificÃ¡vel nÃ£o pode ser negativa
assert Area_Liquida >= 0, "ERRO: RestriÃ§Ãµes excedem Ã¡rea total"

# Teste 2: Potencial construtivo deve respeitar TO
assert (Area_Ocupada / Area_Liquida) <= (TO / 100), "ERRO: TO excedido"

# Teste 3: Ãrea construÃ­da deve respeitar CA
assert (Area_Total_Const / Area_Liquida) <= CA, "ERRO: CA excedido"

# Teste 4: NÂº pavimentos nÃ£o pode exceder gabarito
assert NÂº_Pavimentos <= Gabarito, "ERRO: Gabarito excedido"

# Teste 5: Lote mÃ©dio nÃ£o pode ser menor que mÃ­nimo legal
assert Lote_Medio >= Lote_Minimo_Legal, "ERRO: Lote abaixo do mÃ­nimo"

# Teste 6: Se restriÃ§Ãµes > 60%, sinalizar RISCO ALTO
if (Area_Restrita / Area_Total) > 0.6:
    print("âš ï¸ ALERTA: RestriÃ§Ãµes comprometem > 60% da Ã¡rea")

# Teste 7: MatrÃ­cula deve estar atualizada
assert Dias_Desde_Matricula <= 90, "âš ï¸ ALERTA: MatrÃ­cula desatualizada"
```

**Se QUALQUER teste falhar:**
â†’ Revisar cÃ¡lculos
â†’ Revalidar parÃ¢metros
â†’ Consultar especialista

---

### 7.3 Checklist de DocumentaÃ§Ã£o

**ANTES de Concluir Passo 5:**

**Dados Completos:**
- [ ] Terreno localizado precisamente (GPS ou endereÃ§o)
- [ ] Ãrea total confirmada (mÂ²)
- [ ] Zona urbanÃ­stica identificada (formal ou inferida)
- [ ] ParÃ¢metros TO, CA, gabarito, recuos obtidos
- [ ] RestriÃ§Ãµes ambientais verificadas (APP, vegetaÃ§Ã£o, topografia)
- [ ] SituaÃ§Ã£o dominial consultada (matrÃ­cula)
- [ ] Infraestrutura disponÃ­vel checada (Ã¡gua, esgoto, energia)

**CÃ¡lculos Validados:**
- [ ] Ãrea lÃ­quida edificÃ¡vel calculada
- [ ] Potencial construtivo calculado (TO, CA, gabarito)
- [ ] Recuos aplicados corretamente
- [ ] Quantidade de lotes/unidades estimada
- [ ] Custos adicionais orÃ§ados

**Red Flags Classificados:**
- [ ] Impeditivos identificados (se houver)
- [ ] Riscos altos listados (se houver)
- [ ] Riscos moderados documentados
- [ ] DecisÃ£o GO/CONDITIONAL/STOP tomada

**IntegraÃ§Ã£o TIV:**
- [ ] Outputs prontos para Passo 6 (potencial, VGV, custos)
- [ ] Necessidade de iteraÃ§Ã£o sinalizada (se aplicÃ¡vel)
- [ ] PrÃ³ximos passos especificados claramente

---

## 8. INTEGRAÃ‡ÃƒO COM OUTRAS SKILLS TIV

### 8.1 Inputs Recebidos De:

**Passo 1 (Garimpo) - tiv-garimpo:**
- LocalizaÃ§Ã£o do terreno (endereÃ§o/GPS)
- Ãrea total (mÂ²)
- Produto pretendido (loteamento/incorporaÃ§Ã£o)
- Red flags iniciais identificados

**Passo 2 (DinÃ¢mica EconÃ´mica) - tiv-passo2-dinamica-economica:**
- Contexto macroeconÃ´mico (influencia tipo produto)
- TendÃªncias de mercado (demanda residencial/comercial)

**Passo 3 (Ãrea de InfluÃªncia) - tiv-passo3-area-influencia:**
- PolÃ­gono de influÃªncia definido (isÃ³cronas)
- Demografia local (renda, populaÃ§Ã£o)
- Centralidades mapeadas

**Passo 4 (VocaÃ§Ã£o) - tiv-passo4-vocacao:**
- **PRINCIPAL INPUT:** Tipo de produto recomendado (horizontal/vertical)
- PadrÃ£o (econÃ´mico/mÃ©dio/alto)
- Faixa de preÃ§o-alvo
- PÃºblico-alvo (renda familiar)

### 8.2 Outputs Fornecidos Para:

**Passo 6 (Demanda) - tiv-passo6-demanda:**
- âœ… Potencial construtivo validado (nÂº unidades/lotes)
- âœ… Ãrea mÃ©dia das unidades (mÂ²)
- âœ… VGV preliminar (preÃ§o Ã— unidades)
- âœ… Custos adicionais (infraestrutura, licenciamento)
- âœ… Cronograma licenciamento (impacta lanÃ§amento)

**Passo 7 (Oferta) - tiv-passo7-oferta:**
- âœ… Tipo produto definido (para mapear concorrentes)
- âœ… LocalizaÃ§Ã£o precisa (raio de busca)
- âœ… PadrÃ£o produto (benchmarking)

**Passo 8 (AbsorÃ§Ã£o) - tiv-absorcao:**
- âœ… Cronograma licenciamento (impacta lanÃ§amento)
- âœ… Velocidade potencial (unidades disponÃ­veis)
- âœ… Faseamento recomendado (se loteamento grande)

**Passo 9 (ValidaÃ§Ã£o) - tiv-validador:**
- âœ… Premissas legais a validar
- âœ… Red flags a monitorar
- âœ… Fontes legais consultadas (auditoria)

**Passo 10 (FCD) - tiv-fcd:**
- âœ… Custos de conformidade legal
- âœ… Cronograma de aprovaÃ§Ãµes (fluxo de caixa)
- âœ… Ãrea vendÃ¡vel confirmada (receita)
- âœ… Red flags financeiros (contingÃªncias)

### 8.3 IteraÃ§Ã£o ObrigatÃ³ria Passo 5 â†” Passo 6

**PrincÃ­pio TIV:**
> "Potencial tÃ©cnico MÃXIMO raramente Ã© o produto IDEAL. Iterar com Demanda (Passo 6) Ã© OBRIGATÃ“RIO."

**CenÃ¡rio tÃ­pico:**

1ï¸âƒ£ **Passo 5 calcula:** 80 lotes viÃ¡veis tecnicamente
2ï¸âƒ£ **Passo 6 valida:** Demanda para 50 lotes/ano
3ï¸âƒ£ **IteraÃ§Ã£o:** Reduzir para 50 lotes (velocidade 12 meses, Fator 4:1 TIV)
4ï¸âƒ£ **Passo 5 revalida:** 50 lotes ainda respeita TO, CA, lote mÃ­n?

**Quando iterar:**
- Demanda < 50% potencial tÃ©cnico â†’ REDUZIR produto
- Produto ajustado â†’ REVALIDAR parÃ¢metros legais
- RestriÃ§Ãµes descobertas â†’ REVISAR vocaÃ§Ã£o (Passo 4)

---

## 9. EXEMPLOS PRÃTICOS (LEOPOLDINA-MG)

### 9.1 Exemplo 1: Loteamento Periurbano - GO âœ…

**Contexto:**
- **Terreno:** 50.000 mÂ²
- **LocalizaÃ§Ã£o:** Bairro Vista Alegre, Leopoldina-MG
- **Produto pretendido:** Loteamento econÃ´mico

**AnÃ¡lise:**

**Zona:** ZEU (Zona de ExpansÃ£o Urbana)

**ParÃ¢metros (LUOS 2007 inferida):**
- Lote mÃ­nimo: 250 mÂ²
- Testada mÃ­nima: 10 m
- Ãreas pÃºblicas: 35% gleba (arruamento + Ã¡reas verdes)

**RestriÃ§Ãµes:**
- **APP:** CÃ³rrego atravessa terreno (faixa 10m cada margem)
  - Comprimento margem: 200 m
  - Ãrea APP: 200m Ã— 10m Ã— 2 margens = **4.000 mÂ²** (8% terreno)
- **Topografia:** Plana (0-3% declividade)
- **VegetaÃ§Ã£o:** Pasto degradado (sem restriÃ§Ã£o)

**CÃ¡lculos:**
```
Ãrea Total:        50.000 mÂ²
Ãrea APP:          -4.000 mÂ² (8%)
Ãrea LÃ­quida:      46.000 mÂ²
Ãreas pÃºblicas:    46.000 Ã— 0,35 = -16.100 mÂ²
Ãrea LoteÃ¡vel:     29.900 mÂ²
Lote MÃ©dio:        250 mÂ²
NÂº Lotes:          29.900 Ã· 250 = 119 lotes
                   (arredondar 115-120 lotes)
```

**DecisÃ£o:** âœ… **VIÃVEL**

**Justificativa:**
- RestriÃ§Ã£o APP moderada (8% do terreno)
- Topografia favorÃ¡vel (custos normais terraplanagem)
- Potencial: **115-120 lotes econÃ´micos**
- Licenciamento: LP+LI+LO necessÃ¡rio (> 100 lotes, Lei 15.190/2025)

**CondiÃ§Ãµes:**
- Respeitar faixa APP 10m (cÃ³rrego)
- Licenciamento ambiental obrigatÃ³rio
- CompensaÃ§Ã£o: plantio 200 mudas nativas

**Custos Adicionais:**
- Infraestrutura Ã¡gua/esgoto: R$ 400.000
- Licenciamento ambiental: R$ 50.000
- CompensaÃ§Ã£o APP: R$ 30.000
- **TOTAL:** R$ 480.000 (â‰ˆ 3% VGV)

**PrÃ³ximos Passos:**
â†’ **Passo 6 (Demanda):** Validar mercado para 115 lotes
â†’ Qual a velocidade de absorÃ§Ã£o esperada?
â†’ PreÃ§o viÃ¡vel: R$ 120-150k/lote (pÃºblico C-D)?

---

### 9.2 Exemplo 2: IncorporaÃ§Ã£o Centro - GO com RestriÃ§Ãµes âš ï¸

**Contexto:**
- **Terreno:** 1.200 mÂ²
- **LocalizaÃ§Ã£o:** Av. BarÃ£o de Cotegipe (centro), Leopoldina-MG
- **Produto pretendido:** EdifÃ­cio residencial

**AnÃ¡lise:**

**Zona:** ZCA (Zona Controle de Adensamento) - inferida

**ParÃ¢metros (LUOS 2007 + CÃ³digo Obras 263/1957):**
- TO mÃ¡ximo: 70%
- CA bÃ¡sico: 2,0
- Gabarito: 8 pavimentos (CÃ³digo Obras, ZC)
- Recuos: 5m frontal, 3m laterais, 3m fundos

**RestriÃ§Ãµes:**
- **Entorno bem tombado:** Escola Botelho Reis (50m distÃ¢ncia)
  - âš ï¸ **RestriÃ§Ãµes nÃ£o padronizadas** (consulta IPHAN necessÃ¡ria)
- **Topografia:** Plana
- **Infraestrutura:** Completa (Ã¡gua, esgoto, energia)

**CÃ¡lculos:**
```
Ãrea Total:           1.200 mÂ²
Recuos:               -180 mÂ² (estimado)
Ãrea LÃ­quida:         1.020 mÂ²
TO 70%:               1.020 Ã— 0,70 = 714 mÂ² (Ã¡rea ocupada)
CA 2,0:               1.020 Ã— 2,0 = 2.040 mÂ² (Ã¡rea total construÃ­da)
NÂº Pavimentos:        2.040 Ã· 714 = 2,86 â‰ˆ 3 pavimentos
Gabarito MÃ¡x:         8 pavimentos
NÂº Pavimentos Final:  min(3, 8) = 3 pavimentos
```

**Potencial:**
- Ãrea privativa: 2.040 mÂ² Ã— 0,80 (eficiÃªncia) = **1.632 mÂ²**
- Apto mÃ©dio: 60 mÂ²
- **NÂº Aptos: 1.632 Ã· 60 = 27 apartamentos**

**DecisÃ£o:** âš ï¸ **VIÃVEL COM RESTRIÃ‡Ã•ES**

**Justificativa:**
- Zoneamento permite uso residencial vertical
- Potencial tÃ©cnico: **27 apartamentos** (3 pavimentos)
- âš ï¸ **RESTRIÃ‡ÃƒO:** Entorno bem tombado requer consulta IPHAN
  - PossÃ­vel exigÃªncia: fachada alinhada, altura limitada, materiais especÃ­ficos

**CondiÃ§Ãµes:**
- Protocolar consulta prÃ©via IPHAN (entorno Escola Botelho Reis)
- Gabarito pode ser reduzido para 2 pavimentos (18 aptos)
- Recuos frontais podem ser exigidos maiores (6-7m)
- Fachada: restriÃ§Ãµes estÃ©ticas possÃ­veis

**Custos Adicionais:**
- Consulta IPHAN: R$ 5.000
- Ajustes projeto (se exigido): R$ 15.000
- **TOTAL:** R$ 20.000 (< 1% VGV)

**Riscos:**
- ðŸ”´ **ALTO:** IPHAN pode vetar gabarito 3 pavimentos â†’ reduzir para 2 (18 aptos)
- ðŸŸ  **MODERADO:** ExigÃªncias estÃ©ticas podem encarecer obra (+10-15%)

**PrÃ³ximos Passos:**
â†’ Protocolar consulta IPHAN ANTES de avanÃ§ar
â†’ **Se IPHAN OK:** Prosseguir Passo 6 (Demanda 27 aptos)
â†’ **Se IPHAN restringe:** Iterar Passo 4 (vocaÃ§Ã£o 18 aptos viÃ¡vel?)

---

### 9.3 Exemplo 3: Comercial Rodovia - STOP âŒ

**Contexto:**
- **Terreno:** 5.000 mÂ²
- **LocalizaÃ§Ã£o:** BR-116 (Km 738), Leopoldina-MG
- **Produto pretendido:** Posto de combustÃ­vel + restaurante

**AnÃ¡lise:**

**Zona:** ZAE (Zona Atividades EconÃ´micas) - inferida

**ParÃ¢metros (LUOS 2007):**
- TO mÃ¡ximo: 60%
- CA bÃ¡sico: 1,5
- Uso comercial permitido

**RestriÃ§Ãµes:**
- **Faixa de domÃ­nio BR-116:** 40m (Lei Federal 5.917/1973 + ResoluÃ§Ãµes DNIT)
  - Ãrea nÃ£o edificÃ¡vel: 40m Ã— 150m (testada) = **6.000 mÂ²**
- âŒ **PROBLEMA:** Faixa nÃ£o edificÃ¡vel (6.000mÂ²) > Ãrea total (5.000mÂ²)
- **APP:** NÃ£o identificada
- **Topografia:** Plana

**CÃ¡lculos:**
```
Ãrea Total:              5.000 mÂ²
Faixa domÃ­nio BR-116:    -6.000 mÂ² (!)
Ãrea LÃ­quida:            -1.000 mÂ² (!!) 
                         âŒ NEGATIVO = INVIÃVEL
```

**DecisÃ£o:** âŒ **INVIÃVEL**

**Justificativa:**
- Faixa de domÃ­nio federal (40m BR-116) **EXCEDE** Ã¡rea total do terreno
- Ãrea edificÃ¡vel lÃ­quida = **ZERO**
- ImpossÃ­vel construir qualquer edificaÃ§Ã£o

**Causa Raiz:**
- Terreno estreito (testada < 40m para BR-116)
- Faixa nÃ£o edificÃ¡vel compromete 100%+ Ã¡rea

**PrÃ³ximos Passos:**
â†’ **DESCARTAR** terreno
â†’ Buscar imÃ³vel com testada > 50m (faixa 40m + 10m edificaÃ§Ã£o mÃ­nima)
â†’ Ou buscar terreno em rodovia estadual (faixa menor: 15-20m)

**LiÃ§Ãµes Aprendidas:**
- âš ï¸ Terrenos em rodovias federais: verificar faixa domÃ­nio ANTES de negociar
- âš ï¸ BR-116 = 40m faixa (Lei 5.917/1973)
- âš ï¸ Rodovias estaduais MG = 15-20m faixa (DER-MG)

---

## 10. CHECKLIST DE QUALIDADE

### 10.1 Antes de Concluir Passo 5

**Dados Completos:**
- [ ] Terreno localizado precisamente (GPS ou endereÃ§o)
- [ ] Ãrea total confirmada (mÂ²)
- [ ] Zona urbanÃ­stica identificada (formal ou inferida)
- [ ] ParÃ¢metros TO, CA, gabarito, recuos obtidos
- [ ] RestriÃ§Ãµes ambientais verificadas (APP, vegetaÃ§Ã£o, topografia)
- [ ] SituaÃ§Ã£o dominial consultada (matrÃ­cula)
- [ ] Infraestrutura disponÃ­vel checada (Ã¡gua, esgoto, energia)

**CÃ¡lculos Validados:**
- [ ] Ãrea lÃ­quida edificÃ¡vel calculada (total - restriÃ§Ãµes)
- [ ] Potencial construtivo calculado (TO, CA, gabarito)
- [ ] Recuos aplicados corretamente
- [ ] Quantidade de lotes/unidades estimada
- [ ] Custos adicionais orÃ§ados (infraestrutura, licenciamento)

**Red Flags Classificados:**
- [ ] Impeditivos identificados (se houver) â†’ STOP
- [ ] Riscos altos listados (se houver) â†’ CONDITIONAL
- [ ] Riscos moderados documentados â†’ MONITORAR
- [ ] DecisÃ£o GO/CONDITIONAL/STOP tomada

**IntegraÃ§Ã£o TIV:**
- [ ] Outputs prontos para Passo 6 (potencial, VGV, custos)
- [ ] Necessidade de iteraÃ§Ã£o sinalizada (se aplicÃ¡vel)
- [ ] PrÃ³ximos passos especificados claramente

---

### 10.2 PrincÃ­pios TIV Respeitados

**Inputs DefensÃ¡veis:**
- [ ] Toda afirmaÃ§Ã£o cita fonte legal (Lei X, Art. Y)
- [ ] ParÃ¢metros inferidos sinalizados claramente
- [ ] Lacunas de dados declaradas (sem "chutes")

**Concisos:**
- [ ] InformaÃ§Ã£o > opiniÃ£o
- [ ] Fatos citados, nÃ£o interpretaÃ§Ãµes subjetivas
- [ ] NÃºmeros com unidades (mÂ², %, R$)

**TangÃ­veis:**
- [ ] Outputs quantificados (nÂº lotes, mÂ² Ã¡rea)
- [ ] Custos em R$ (nÃ£o "alto/baixo")
- [ ] Prazos em meses (nÃ£o "rÃ¡pido/demorado")

**RastreÃ¡veis:**
- [ ] Fontes citadas (lei, artigo, consulta, data)
- [ ] CÃ¡lculos passo a passo visÃ­veis
- [ ] Premissas explÃ­citas (nÃ£o implÃ­citas)

---

### 10.3 Erros Comuns a Evitar

**âŒ NÃƒO FAÃ‡A:**
- Iniciar "arte"/anteprojeto ANTES de Estudo de Massa
- Tratar zoneamento como checagem textual (sem quadros e mapas)
- Confundir ambiental Ã— urbanÃ­stico (deixar condicionantes fora do status)
- NÃ£o versionar leis e desenhos (risco obsolescÃªncia)
- Usar parÃ¢metros desatualizados (LUOS 2007 sem checar PLC 2024)
- Desconsiderar faixas nÃ£o edificÃ¡veis (rodovias, ferrovias, linhas)
- Ignorar entorno bens tombados (restriÃ§Ãµes nÃ£o padronizadas)

**âœ… FAÃ‡A:**
- Consolidar Estudo de Massa ANTES de qualquer arte
- Mapear TODAS restriÃ§Ãµes em camadas georreferenciadas
- Citar TODAS fontes legais (lei, artigo, data)
- Versionar anÃ¡lise (data, responsÃ¡vel, legislaÃ§Ã£o consultada)
- Consultar legislaÃ§Ã£o vigente + em tramitaÃ§Ã£o
- Protocolar consultas formais (Prefeitura, IPHAN, IEF)
- Iterar com Passo 6 (tÃ©cnico Ã— mercado)

---

## REFERÃŠNCIAS E CITAÃ‡Ã•ES-CHAVE

### Fundamentos MetodolÃ³gicos

**PrincÃ­pio TIV - TÃ©cnica antes de Mercado:**
> "NÃ£o adianta ter demanda se o terreno nÃ£o comporta tecnicamente o produto. Legal Ã— RestriÃ§Ãµes Ã© filtro primÃ¡rio."
> *KB CORE v4.0, IntroduÃ§Ã£o Passo 5*

**Regra de Ouro:**
> "RestriÃ§Ãµes legais SÃƒO FATOS, nÃ£o negociÃ¡veis. Identificar cedo evita trabalho perdido."
> *KB CORE v4.0, Passo 5*

**IteraÃ§Ã£o ObrigatÃ³ria:**
> "Potencial tÃ©cnico MÃXIMO raramente Ã© o produto IDEAL. Iterar com Demanda (Passo 6) Ã© OBRIGATÃ“RIO."
> *KB CORE v4.0, IntegraÃ§Ã£o Passo 5-6*

**MissÃ£o do Arquiteto:**
> "A missÃ£o do arquiteto Ã© maximizar o potencial construtivo do negÃ³cio, levando em conta todas as regras dispostas na legislaÃ§Ã£o de ocupaÃ§Ã£o do solo das prefeituras."
> *Apostila TIV - Passo 5, p.58*

**Sequenciamento Correto:**
> "ApÃ³s definiÃ§Ã£o do produto, apontado pelo mercado, faz-se necessÃ¡rio a adequaÃ§Ã£o do projeto ao terreno, levando em consideraÃ§Ã£o as informaÃ§Ãµes do QUADRO II da NBR 12.271 (Ãreas Privativas e Reais do Empreendimento)."
> *Apostila TIV - Passo 5, p.58*

---

### Base Legal (Leopoldina-MG + Federal)

**Federal:**
- Lei 10.257/2001 - Estatuto da Cidade
- Lei 12.651/2012 - CÃ³digo Florestal (APPs)
- Lei 15.190/2025 - Lei Geral Licenciamento Ambiental
- Lei 6.766/1979 - Parcelamento Solo Urbano
- Lei 4.591/1964 - IncorporaÃ§Ãµes ImobiliÃ¡rias
- Lei 5.917/1973 - Faixa domÃ­nio rodovias federais
- Lei 10.233/2001 - Faixa domÃ­nio ferrovias

**Municipal (Leopoldina-MG):**
- LC 09/2006 - Plano Diretor Participativo
- LC 14/2009 - AlteraÃ§Ã£o Mapa Plano Diretor
- Lei 263/1957 - CÃ³digo de Obras e EdificaÃ§Ãµes
- Lei 4.698/2022 - PerÃ­metro Urbano
- Lei 4.842/2024 - Marco RegulatÃ³rio APP Urbana âœ… **RECENTE**
- LC 63/2020 - Zona UrbanizaÃ§Ã£o EspecÃ­fica
- LC 42/2015 - Parcelamento Solo Rural
- PLC 01/2024 - Nova LUOS (em tramitaÃ§Ã£o) âš ï¸

**PatrimÃ´nio HistÃ³rico:**
- Decreto 1435/1999 - Tombamento Escola Botelho Reis
- Decretos 1752-1754/2000 - Tombamentos diversos

**Normas TÃ©cnicas (ABNT):**
- NBR 12.721 - AvaliaÃ§Ã£o de Custos UnitÃ¡rios
- NBR 12.271 - Ãreas Privativas e Comuns (Quadro II)
- NBR 9050 - Acessibilidade
- NBR 14.653 - AvaliaÃ§Ã£o de Bens

---

### Ã“rgÃ£os de Consulta

**Municipal:**
- Secretaria Municipal de Obras (consultas prÃ©vias)
- Secretaria Meio Ambiente (licenciamento local)
- CartÃ³rio Registro de ImÃ³veis (matrÃ­culas)

**Estadual:**
- IEF-MG (vegetaÃ§Ã£o nativa)
- SEMAD-MG (licenciamento ambiental estadual)
- DER-MG (rodovias estaduais)

**Federal:**
- IPHAN (bens tombados federais/entorno)
- DNIT (rodovias federais)
- ANA (recursos hÃ­dricos)

**ConcessionÃ¡rias:**
- COPASA (Ã¡gua/esgoto)
- CEMIG (energia elÃ©trica)
- Operadoras telecom (fibra Ã³ptica)

---

### Metodologia de CÃ¡lculo

**Ãrea LÃ­quida EdificÃ¡vel:**
```
Ãrea LÃ­quida = Ãrea Total - Î£ RestriÃ§Ãµes
Onde RestriÃ§Ãµes = APP + Faixas nÃ£o edif. + Outras
```

**Potencial Construtivo (Vertical):**
```
Ãrea Ocupada = Ãrea LÃ­quida Ã— (TO / 100)
Ãrea Total ConstruÃ­da = Ãrea LÃ­quida Ã— CA
NÂº Pavimentos = min(Ãrea Total / Ocupada, Gabarito)
```

**Potencial LoteÃ¡vel (Horizontal):**
```
Ãrea LoteÃ¡vel = Ãrea LÃ­quida Ã— (1 - % Ãreas PÃºblicas)
NÂº Lotes = Ãrea LoteÃ¡vel / Lote MÃ©dio
Onde: Lote MÃ©dio â‰¥ Lote MÃ­nimo Legal
```

---

**FIM DA SKILL TIV PASSO 5 - ANÃLISE LEGAL Ã— RESTRIÃ‡Ã•ES URBANÃSTICAS**

---

**VersÃ£o:** 1.0  
**Data CriaÃ§Ã£o:** 12/11/2025  
**Ãšltima AtualizaÃ§Ã£o:** 12/11/2025  
**MunicÃ­pio-Foco:** Leopoldina-MG  
**Metodologia:** TIV 4.0  
**Status:** âœ… Operacional - Pronto para Uso  

---

**PrÃ³ximos Passos TIV:**
â†’ Se **VIÃVEL**: Prosseguir **Passo 6 (Demanda)**
â†’ Se **VIÃVEL COM RESTRIÃ‡Ã•ES**: Iterar **Passo 4 (VocaÃ§Ã£o)** + Passo 6
â†’ Se **INVIÃVEL**: **STOP** - Descartar terreno
