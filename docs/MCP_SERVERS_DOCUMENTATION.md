# MCP e WebMCP no VERTIV V7

## Status V7.0

WebMCP nao e feature principal do VERTIV V7.0. Ele permanece experimental,
desligado por padrao e fora do caminho critico de ingestao, sentenca e revisao
humana.

Flags padrao:

```env
WEBMCP_ENABLED=false
NEXT_PUBLIC_WEBMCP_ENABLED=false
```

Com essas flags desligadas:

- o backend nao registra `/api/v7/webmcp/*`;
- o backend nao registra `/api/v7/openapi/schemas`;
- o frontend nao busca catalogo WebMCP;
- a ausencia de `navigator.modelContext` nao afeta a aplicacao.

## Rotas Experimentais

Quando `WEBMCP_ENABLED=true`, as rotas ficam disponiveis apenas com usuario
autenticado:

| Metodo | Rota | Finalidade |
| --- | --- | --- |
| `GET` | `/api/v7/webmcp/schemas` | Catalogo experimental de ferramentas WebMCP |
| `GET` | `/api/v7/webmcp/schemas/{tool_name}` | Schema de uma ferramenta suportada |
| `GET` | `/api/v7/openapi/schemas` | Catalogo B2B experimental |

## Ferramentas Suportadas em V7.0

Somente ferramentas com suporte real entram no catalogo:

| Ferramenta | Status | Observacao |
| --- | --- | --- |
| `simulate_what_if` | Experimental | Simulacao sem persistencia; matematica deve continuar no backend |
| `highlight_pdf_evidence` | Experimental | Foco visual em evidencia de PDF quando a UI suportar o alvo |

Ferramentas de mutacao como `approve_capital_sentence`,
`register_kill_reason` e `override_legal_flag` permanecem fora do catalogo V7.0
ate terem endpoint, persistencia, autorizacao e confirmacao humana testados.

## Relacao com MCP Local

Servidores MCP locais usados por ferramentas de desenvolvimento, como filesystem,
browser automation ou memory, sao infraestrutura de produtividade do operador e
nao fazem parte da superficie de produto V7.0.

## Verificacao

Comandos relevantes:

```bash
npm run test:v7:backend
npm run test:v7:e2e
```

O backend possui testes garantindo que as rotas WebMCP nao sao registradas por
padrao e que o catalogo nomeado nao expõe ferramentas sem suporte produtivo.
