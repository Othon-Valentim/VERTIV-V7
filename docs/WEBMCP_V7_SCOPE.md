# WebMCP V7.0 Scope

## Decisao

WebMCP fica em modo experimental controlado no VERTIV V7.0. Ele nao participa
do fluxo principal de produto, nao e requisito para demonstracao e nao pode
bloquear o gate `npm run test:v7`.

## Flags

Backend:

```env
WEBMCP_ENABLED=false
```

Frontend:

```env
NEXT_PUBLIC_WEBMCP_ENABLED=false
```

Ambas ficam `false` por padrao. Para testes controlados, as duas precisam ser
ativadas de forma explicita no ambiente correspondente.

## Comportamento Esperado

Com `WEBMCP_ENABLED=false`:

- `/api/v7/webmcp/schemas` nao e registrado;
- `/api/v7/webmcp/schemas/{tool_name}` nao e registrado;
- `/api/v7/openapi/schemas` nao e registrado;
- `/health` retorna `webmcp_enabled: false`.

Com `NEXT_PUBLIC_WEBMCP_ENABLED=false`:

- `useWebMCP` retorna estado inativo;
- nenhuma chamada ao catalogo e feita;
- navegadores sem `navigator.modelContext` funcionam normalmente.

## Ferramentas Publicadas

O catalogo V7.0 publica apenas:

- `simulate_what_if`;
- `highlight_pdf_evidence`.

As ferramentas abaixo existem como desenho interno, mas nao sao publicadas em
V7.0:

- `approve_capital_sentence`;
- `register_kill_reason`;
- `override_legal_flag`.

Motivo: elas alteram estado ou podem induzir decisao operacional. Para entrarem
em V7.1, precisam de endpoint real, autorizacao, auditoria, idempotencia,
confirmacao humana e teste E2E.

## Riscos

- A especificacao de browser ainda e experimental.
- `navigator.modelContext` nao existe nos navegadores usuais.
- Ferramentas de mutacao exigem modelo de autorizacao e auditoria mais forte.
- Prometer WebMCP como produto principal criaria escopo falso para V7.0.

## Criterio para V7.1

WebMCP so deve sair de experimental quando:

- houver pelo menos uma UI usando `useWebMCP` em fluxo real;
- o catalogo tiver cobertura de teste por ferramenta;
- ferramentas de mutacao tiverem confirmacao humana obrigatoria;
- as rotas continuarem autenticadas e rate-limited;
- o runbook incluir operacao, rollback e diagnostico.
