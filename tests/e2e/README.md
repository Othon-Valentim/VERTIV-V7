# VERTIV V7 E2E Tests

## Papel da Suíte

Os testes Playwright agora ficam separados em dois grupos:

- **Gate V7**: valida o fluxo de fechamento do produto atual: upload de ZIP Data Room, abertura da tela de auditoria, sentença, solicitação de auditoria manual, revisão humana e confirmação idempotente.
- **Legado**: preserva specs históricos do wizard/V6 para compatibilidade e investigação, mas eles não bloqueiam o fechamento V7.

O gate oficial de release é:

```bash
npm run test:v7
```

Esse comando roda backend, worker e o spec E2E V7 mockado. Para o E2E, o frontend precisa estar ativo em `http://localhost:3000`.

## Pré-requisitos

- Node.js 18+
- npm 9+
- Dependências instaladas com `npm install`
- Navegadores Playwright instalados com `npm run playwright:install`
- Frontend local ativo para `test:v7:e2e`: `npm run dev:frontend`

## Comandos V7

```bash
# Gate completo de fechamento V7
npm run test:v7

# Apenas backend V7
npm run test:v7:backend

# Apenas worker V7
npm run test:v7:worker

# Apenas E2E V7
npm run test:v7:e2e

# Alias de verificação final
npm run verify:v7
```

## Comandos Gerais e Legados

```bash
# Todos os specs Playwright, incluindo legado
npm run test:e2e

# Somente specs legados, excluindo os marcados com @v7
npm run test:e2e:legacy

# Modo interativo
npm run test:e2e:ui

# Browser visível
npm run test:e2e:headed

# Debug
npm run test:e2e:debug

# Relatório HTML
npm run test:e2e:report
```

## Estrutura

```text
tests/e2e/
  v7_upload_audit_mock.spec.ts        # Gate V7 mockado e determinístico
  test_*.spec.ts                      # Specs legados do wizard/V6
  customer_journey_demo.spec.ts       # Jornada histórica legada
  debug_login.spec.ts                 # Debug legado de autenticação
  reports/                            # Relatórios Playwright gerados
  test-results/                       # Artefatos de execução
```

## Variáveis

| Variável | Default | Uso |
| --- | --- | --- |
| `BASE_URL` | `http://localhost:3000` | URL do frontend para navegação Playwright |
| `API_URL` | `http://localhost:8000` | URL esperada do backend em specs legados |
| `CI` | `false` | Ativa retries e modo headless em CI |

## Critério de Gate V7

O fechamento V7 considera verde quando:

- `npm run test:v7:backend` passa.
- `npm run test:v7:worker` passa.
- `npm run test:v7:e2e` passa com o frontend rodando.
- Falhas em specs legados não aparecem no `test:v7`.

Os specs legados não foram apagados porque ainda documentam fluxos históricos e podem ajudar em regressões futuras, mas o produto V7 não depende deles para aceite.
