# VERTIV V7.0 - Manual Operacional

**Identidade:** Tribunal Agentico de Risco Imobiliario
**Operacao padrao:** Data Room ZIP, extracao por IA, calculo Diamond Core/Polars, calibracao GoldenEvaluator e Sentenca de Capital auditavel.

## 1. Posicionamento

VERTIV V7.0 nao e uma calculadora manual. Ele e um fluxo de decisao para risco imobiliario no qual documentos viram evidencias, evidencias viram premissas estruturadas e o Diamond Core calcula a sentenca.

## 2. Preparacao Operacional

Antes de operar:

- confirme que o backend esta em `http://localhost:8000`;
- confirme que o frontend esta em `http://localhost:3002`;
- confirme que o worker esta ativo;
- confirme que o bucket Supabase `data-rooms` existe e e privado;
- use `USE_MOCK=1` para dry run local.

## 3. Procedimento de Analise

1. Receba o Data Room do ativo em ZIP.
2. Envie o ZIP pelo frontend.
3. Aguarde a ingestao sair de `UPLOADING`/`INGESTING`.
4. Abra a tela de auditoria.
5. Revise evidencias da IA e premissas extraidas.
6. Revise calculos Diamond Core/Polars.
7. Revise comparacao GoldenEvaluator quando houver `legacy_simulation_id`.
8. Solicite auditoria manual ou confirme a Sentenca de Capital.

## 4. Criterios de Decisao

### Sentenca automatica

Uma ingestao em `AUTONOMOUS_SENTENCED` possui calculos suficientes para revisao operacional. O operador ainda deve conferir evidencias e premissas antes de confirmar.

### Auditoria humana

Use `REQUEST_MANUAL_AUDIT` quando:

- a extracao da IA deixou duvidas;
- documentos criticos parecem ausentes;
- as premissas financeiras precisam de revisao;
- a calibracao GoldenEvaluator diverge de forma relevante.

### Estados terminais bloqueados

`KILLED` e `FAILED` nao devem ser confirmados. O operador deve analisar `kill_reasons`, erro registrado ou solicitar novo Data Room quando necessario.

## 5. Responsabilidade do Diamond Core

O Diamond Core e responsavel por calculo financeiro, risco, opcoes reais e metricas. A IA nao decide NPV, IRR, payback ou viabilidade; ela apenas extrai e normaliza insumos.

## 6. Auditoria

Toda acao humana relevante deve manter:

- usuario;
- data/hora;
- status anterior;
- status atual;
- notas ou motivo;
- chave de idempotencia quando fornecida.

## 7. WebMCP

WebMCP e experimental em V7.0 e fica desligado por padrao. Use somente em ambiente controlado e com as flags `WEBMCP_ENABLED` e `NEXT_PUBLIC_WEBMCP_ENABLED`.

## 8. Legado/Compatibilidade

O material V6 e o fluxo manual anterior permanecem como historico de calibracao e compatibilidade. Eles nao definem a operacao padrao V7.0.
