# VERTIV v6.1.0 - Guia do Usuario

## Bem-vindo ao VERTIV!

O VERTIV e uma plataforma de analise de viabilidade imobiliaria que utiliza metodologia T.I.V. (Tese de Investimento Vertical) para avaliar oportunidades de investimento em empreendimentos imobiliarios.

**Acesso:** https://vertiv.tech

---

## 1. Primeiros Passos

### 1.1 Criar Conta

1. Acesse https://vertiv.tech
2. Clique em **"Entrar"** no canto superior direito
3. Clique em **"Criar conta"**
4. Preencha seu email e senha
5. Verifique seu email e clique no link de confirmacao
6. Pronto! Voce ja pode fazer login

### 1.2 Fazer Login

1. Acesse https://vertiv.tech
2. Clique em **"Entrar"**
3. Digite seu email e senha
4. Clique em **"Entrar"**

---

## 2. Tela Inicial

Apos o login, voce vera duas opcoes principais:

| Opcao | Descricao |
|-------|-----------|
| **TIV Wizard** | Metodologia completa em 10 passos para analise de viabilidade |
| **Real Options** | Calculadora de opcoes reais (Black-Scholes) para terrenos |

---

## 3. TIV Wizard - Analise Completa

O TIV Wizard guia voce pelos 10 passos da metodologia de investimento vertical:

### Passo 1: P1 Garimpo & Ciclo
- **Objetivo:** Screening inicial da oportunidade
- **Entrada:** Localizacao, area do terreno, preco pedido
- **Saida:** Score de atratividade (0-100) e fase do ciclo de mercado

### Passo 2: P2 Dinamica Economica
- **Objetivo:** Avaliar indicadores macroeconomicos
- **Dados ao vivo:** Taxa Selic, IPCA, INCC do Banco Central
- **Saida:** Score de favorabilidade economica

### Passo 3: P3 Area de Influencia
- **Objetivo:** Mapear area de influencia do empreendimento
- **Entrada:** Coordenadas ou endereco
- **Saida:** Isocronas e dados demograficos

### Passo 4: P4 Vocacao & Produto
- **Objetivo:** Definir o melhor uso do terreno
- **Analise:** Zoneamento, centralidade, densidade
- **Saida:** Recomendacao de tipologia (Residencial, Comercial, Misto)

### Passo 5: P5 Legal & Restricoes
- **Objetivo:** Verificar impedimentos legais
- **Checklist:** APP, Tombamento, Servidoes, Contaminacao
- **Saida:** GO/NO-GO (Gate Binario)

### Passo 6: P6 Demanda Qualificada
- **Objetivo:** Quantificar demanda potencial
- **Funil:** Populacao → Familias → Renda compativel → Demanda efetiva
- **Saida:** Numero de unidades absorviveis

### Passo 7: P7 Oferta & Mercado
- **Objetivo:** Analisar concorrencia
- **Dados:** Lancamentos ativos, estoque, preco medio/m2
- **Saida:** Benchmark de mercado

### Passo 8: P8 Absorcao (VSO)
- **Objetivo:** Projetar velocidade de vendas
- **Calculo:** Velocidade Sobre Oferta mensal
- **Saida:** Meses para vender o empreendimento

### Passo 9: P9 Convalidacao 4:1
- **Objetivo:** Validar equilibrio demanda/oferta
- **Regra:** Demanda deve ser 4x maior que oferta
- **Saida:** GO/NO-GO estrategico

### Passo 10: P10 Modelagem Financeira
- **Objetivo:** Calcular viabilidade financeira
- **Metricas:**
  - NPV (Valor Presente Liquido)
  - IRR (Taxa Interna de Retorno)
  - ROE (Retorno sobre Patrimonio)
  - Payback (Meses para recuperar investimento)
  - Exposicao Maxima (Capital necessario)
- **Bonus:** Valor de Opcoes Reais (Black-Scholes)

---

## 4. Salvar e Gerenciar Analises

### 4.1 Salvar Analise
- No wizard, clique em **"Salvar"** a qualquer momento
- De um nome para sua analise
- A analise fica vinculada a sua conta

### 4.2 Abrir Analise Existente
- Clique em **"Minhas Analises"**
- Selecione a analise desejada
- Continue de onde parou

### 4.3 Nova Analise
- Clique em **"Nova Analise"** para comecar do zero

---

## 5. Dashboard Real Options

A calculadora de Opcoes Reais permite avaliar o valor de "esperar" antes de desenvolver um terreno.

### Parametros de Entrada:
| Campo | Descricao | Exemplo |
|-------|-----------|---------|
| Valor Atual do Terreno | Quanto o terreno vale hoje | R$ 10.000.000 |
| Custo de Desenvolvimento | Investimento total necessario | R$ 60.000.000 |
| Tempo ate Aprovacao | Anos ate obter licencas | 2 anos |
| Volatilidade | Incerteza do mercado (%) | 20% |
| Taxa Livre de Risco | Selic atual | 13.75% |

### Resultado:
- **Valor da Opcao:** Quanto vale a opcionalidade de esperar
- **Cone de Incerteza:** Visualizacao grafica dos cenarios

---

## 6. Portfolio (Gestao de Projetos)

Acesse `/dashboard/portfolio` para ver todos os seus projetos:

- **Lista de Projetos:** Todas as analises salvas
- **Status:** Pendente, Em analise, Concluido
- **Metricas:** NPV, IRR, ROE de cada projeto
- **Filtros:** Ordene por data, nome ou performance

---

## 7. Exportar Relatorios

### Deal Memo (PDF)
1. Abra a analise desejada
2. Clique em **"Exportar PDF"**
3. Um relatorio profissional sera gerado
4. Use para apresentar ao Comite de Investimentos

---

## 8. Dicas de Uso

### Para Analises Rapidas:
- Use o P1 Garimpo para filtrar oportunidades rapidamente
- Score > 75 = Prosseguir com analise completa
- Score < 50 = Descartar oportunidade

### Para Analises Completas:
- Preencha todos os 10 passos
- Use dados reais de mercado
- Compare com benchmarks da regiao

### Para Decisoes de Timing:
- Use Real Options para terrenos em estoque
- Se o valor da opcao > 10% do terreno, considere esperar

---

## 9. Suporte

**Problemas tecnicos:** Contate o administrador do sistema

**Duvidas metodologicas:** Consulte o WHITE_PAPER.md

**API para integracao:** Consulte API_CONTRACT.md

---

## 10. Glossario

| Termo | Significado |
|-------|-------------|
| **TIV** | Tese de Investimento Vertical |
| **NPV** | Net Present Value (Valor Presente Liquido) |
| **IRR** | Internal Rate of Return (Taxa Interna de Retorno) |
| **ROE** | Return on Equity (Retorno sobre Patrimonio) |
| **VSO** | Velocidade Sobre Oferta |
| **CA** | Coeficiente de Aproveitamento |
| **IT-11** | Instrucao Tecnica 11 (Bombeiros - MG) |
| **Real Options** | Opcoes Reais (teoria financeira) |

---

**VERTIV v6.1.0-SINGULARITY**
*"Nao prevemos o futuro. Estruturamos o presente para lucrar com a volatilidade do futuro."*
