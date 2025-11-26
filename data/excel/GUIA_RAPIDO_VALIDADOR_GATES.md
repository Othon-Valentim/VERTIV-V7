# 📊 GUIA RÁPIDO - VALIDADOR_GATES_TIV_v5.xlsx

## ⚡ Instalação (30 segundos)

1. Baixe o arquivo `VALIDADOR_GATES_TIV_v5.xlsx`
2. Abra no Excel 2016+ (recomendado) ou Google Sheets
3. Habilite edição se solicitado
4. ✅ Pronto!

---

## 🗂️ ESTRUTURA DA PLANILHA

### 6 Abas Disponíveis

| Aba | Função | Ordem de Preenchimento |
|-----|--------|------------------------|
| **DASHBOARD** | Painel consolidado com decisão final | ⬅️ Preencher por ÚLTIMO |
| **DETALHAMENTO_P1** | Score de Atratividade (0-100) | 1️⃣ Primeiro |
| **DETALHAMENTO_P8** | Fator 4:1 (Absorção) | 2️⃣ Segundo |
| **DETALHAMENTO_P9** | Validação de Premissas (Desvios) | 3️⃣ Terceiro |
| **DETALHAMENTO_P10** | ROE e Viabilidade Financeira | 4️⃣ Quarto |
| **HISTORICO** | Registro de projetos analisados | 📝 Após conclusão |

---

## 🎯 COMO USAR

### Passo 1: Preencher Cabeçalho (DASHBOARD)

1. Vá para aba **DASHBOARD**
2. Preencha células amarelas:
   - **B3**: Nome do Projeto
   - **B4**: Data da Análise
   - **B5**: Nome do Analista
   - **E3**: Cidade/Região
   - **E4**: Tipologia (Loteamento, Incorporação, etc.)

### Passo 2: Preencher Gate P1 (DETALHAMENTO_P1)

1. Vá para aba **DETALHAMENTO_P1**
2. **CICLO (0-25 pts)**: Selecione fase e pontos base
   - Recuperação: 22 pts
   - Expansão: 25 pts
   - Desaceleração: 10 pts
   - Recessão: 5 pts
3. **P2i-LEAD (0-50 pts)**: Preencha scores 0-10 para cada pilar
4. **VETORES (0-25 pts)**: Avalie atração/repulsão
5. **Score Total**: Calculado automaticamente (0-100)

### Passo 3: Preencher Gate P8 (DETALHAMENTO_P8)

1. Vá para aba **DETALHAMENTO_P8**
2. Preencha **DEMANDA**:
   - Demanda Potencial (famílias do P6)
3. Preencha **OFERTA**:
   - Pulverizada, Lançamentos, TBC (do P7)
4. **Fator 4:1**: Calculado automaticamente

### Passo 4: Preencher Gate P9 (DETALHAMENTO_P9)

1. Vá para aba **DETALHAMENTO_P9**
2. Para cada premissa:
   - Coluna B: Valor **Projetado** (P1-P8)
   - Coluna C: Valor **Validado** (pesquisa P9)
3. **Desvio Médio**: Calculado automaticamente

### Passo 5: Preencher Gate P10 (DETALHAMENTO_P10)

1. Vá para aba **DETALHAMENTO_P10**
2. Preencha indicadores para 3 cenários:
   - VPL, TIR, ROE, Payback, Exposição
3. **ROE BASE**: Métrica principal de decisão

### Passo 6: Verificar Decisão Final (DASHBOARD)

1. Volte para aba **DASHBOARD**
2. Verifique:
   - Status de cada Gate (✅/🟡/🔴)
   - **DECISÃO FINAL**: GO / GO com ressalvas / NO-GO
3. Documente alertas e ressalvas

---

## 🚦 THRESHOLDS DOS GATES

### Gate P1 - Score de Atratividade
| Score | Status | Decisão |
|-------|--------|---------|
| ≥70 | ✅ PASS | GO |
| 40-69 | 🟡 HOLD | CAUTELA |
| <40 | 🔴 STOP | NO-GO |

### Gate P5 - Impeditivos Legais
| Impeditivos | Status | Decisão |
|-------------|--------|---------|
| 0 | ✅ PASS | GO |
| >0 | 🔴 STOP | NO-GO |

### Gate P8 - Fator 4:1
| Fator | Status | Decisão |
|-------|--------|---------|
| ≥1.0 | ✅ PASS | GO |
| 0.95-0.99 | 🟡 PASS* | GO (ressalva) |
| <0.95 | 🔴 FAIL | NO-GO |

### Gate P9 - Desvio Médio
| Desvio | Status | Decisão |
|--------|--------|---------|
| ≤10% | ✅ PASS | GO |
| 10-15% | 🟡 AJUSTAR | Ajustar P4 |
| >15% | 🔴 REABRIR | Reabrir P4 |

### Gate P10 - ROE (Base)
| ROE | Status | Decisão |
|-----|--------|---------|
| ≥18% | ✅ PASS | GO |
| 12-17% | 🟡 HOLD | HOLD |
| <12% | 🔴 NO-GO | NO-GO |

---

## 💾 APÓS CONCLUSÃO

1. **Salvar** planilha com nome do projeto:
   ```
   VALIDADOR_[NomeProjeto]_[Data].xlsx
   ```

2. **Registrar no Histórico**:
   - Vá para aba **HISTORICO**
   - Adicione linha com dados do projeto

3. **Exportar Dashboard** como PDF para relatório

---

## ⚠️ IMPORTANTE

### Células Amarelas = INPUTS
- São as únicas células que você deve editar
- Valores em azul = inputs manuais

### Células Brancas = FÓRMULAS
- NÃO edite células com fórmulas
- Valores são calculados automaticamente

### Ordem Obrigatória
- P1 → P8 → P9 → P10 → Dashboard
- Não pule etapas!

---

## 🆘 TROUBLESHOOTING

### Problema: Fórmulas mostram #REF!
**Solução**: Verifique se não deletou células referenciadas

### Problema: Status não atualiza
**Solução**: Pressione F9 para recalcular (Excel)

### Problema: Caracteres estranhos (emojis)
**Solução**: Use Excel 2016+ ou Google Sheets

---

## 📞 REFERÊNCIAS

- **Especificação Completa**: `VALIDADOR_GATES_TIV_v5_SPEC.md`
- **Metodologia TIV**: `KB_CORE_v5_0_2_CONSOLIDADO_FINAL.md`
- **Gates Numéricos**: `GATES_NUMERICOS_TIV_v5_0_1.md`

---

**Versão**: 5.0  
**Data**: 26/11/2025  
**Autor**: Claude + Othon Valentim  

✅ **PLANILHA PRONTA PARA USO!**
