# VERTIV V7.0 - Guia do Usuario

O VERTIV V7.0 e um Tribunal Agentico de Risco Imobiliario. O operador envia um Data Room em ZIP, acompanha a ingestao, revisa evidencias e decide se confirma a Sentenca de Capital.

## 1. Acesso

1. Acesse a aplicacao.
2. Entre com sua conta Supabase/Auth.
3. Abra o painel de upload ou auditoria conforme seu perfil operacional.

## 2. Fluxo Principal

```text
ZIP Data Room -> IA extrai -> Diamond Core/Polars calcula -> GoldenEvaluator compara -> Sentenca de Capital
```

### 2.1 Preparar o Data Room

Crie um arquivo `.zip` com documentos do ativo. Inclua apenas arquivos necessarios para analise, como:

- matricula, escritura ou documentos equivalentes;
- estudo de massa ou premissas de area;
- orcamento, custo ou premissas de construcao;
- tabela comercial ou premissas de venda;
- documentos ambientais, legais e restricoes conhecidas.

### 2.2 Enviar o ZIP

1. Abra o fluxo de upload do Data Room.
2. Selecione um arquivo `.zip`.
3. Opcionalmente informe um UUID de calibracao legado quando a analise deve ser comparada a uma simulacao historica.
4. Envie o arquivo.

O sistema grava o ZIP no bucket privado `data-rooms` e cria uma ingestao com status `UPLOADING`.

### 2.3 Acompanhar a Ingestao

Estados comuns:

| Estado | O que significa |
| --- | --- |
| `UPLOADING` | Upload aceito e aguardando processamento |
| `INGESTING` | Worker processando documentos |
| `AUTONOMOUS_SENTENCED` | Sentenca automatica disponivel |
| `PENDING_HUMAN_AUDIT` | Auditoria humana solicitada |
| `MANUAL_ASSISTED` | Caso exige apoio humano antes do fechamento |
| `KILLED` | Risco bloqueante identificado |
| `FAILED` | Falha tecnica ou de extracao |

## 3. Ler a Sentenca

A tela de auditoria apresenta:

- Sentenca de Capital.
- Numeros Diamond Core/Polars.
- Evidencias extraidas pela IA.
- Kill reasons, quando houver.
- Comparacao GoldenEvaluator, quando houver calibracao.
- Metadados de auditoria e confirmacao.

A IA extrai evidencias. A decisao financeira vem do Diamond Core.

## 4. Acoes Humanas

### Solicitar auditoria manual

Use quando a sentenca automatica precisa de revisao humana. A acao muda o status para `PENDING_HUMAN_AUDIT` quando aplicavel e registra evento auditavel.

### Confirmar sentenca

Use quando a sentenca esta revisada e aceita. A confirmacao registra usuario, horario, notas e evento de auditoria.

Nao confirme sentencas em estados `KILLED`, `FAILED`, `UPLOADING` ou `INGESTING`.

## 5. Dry Run Local

Para demonstracao controlada, use:

```bash
USE_MOCK=1
```

Servicos esperados:

| Servico | Porta |
| --- | ---: |
| Frontend | 3002 |
| Backend | 8000 |
| Worker | 8001 |

## 6. WebMCP

WebMCP e experimental em V7.0. Ele so deve aparecer quando as flags estiverem ativas:

```bash
WEBMCP_ENABLED=true
NEXT_PUBLIC_WEBMCP_ENABLED=true
```

Com as flags desligadas, o fluxo de Data Room continua funcionando normalmente.

## 7. Legado/Compatibilidade

O fluxo manual antigo e referencias V6 podem existir como legado de calibracao, testes historicos ou rotas de compatibilidade. Para operacao V7.0, use o fluxo de Data Room ZIP e a tela de auditoria/sentenca.
