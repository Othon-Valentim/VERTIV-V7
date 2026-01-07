# MCP Servers Documentation - VERTIV v6.0

**Gerado em:** 2025-12-24
**Status:** Production Ready
**Ambiente:** Claude Desktop + Claude Code CLI

---

## Visao Geral

O projeto VERTIV v6.0 utiliza o Model Context Protocol (MCP) para estender as capacidades do Claude com ferramentas especializadas.

---

## Servidores MCP Configurados

### 1. Filesystem Server
| Propriedade | Valor |
|-------------|-------|
| **Package** | `@modelcontextprotocol/server-filesystem` |
| **Funcao** | Acesso seguro ao sistema de arquivos do projeto |
| **Diretorio** | `C:\Users\Jussara Thomaz\Documents\VERTIV_V6_GLOBAL` |
| **Status** | ONLINE |

**Capacidades:**
- Leitura de arquivos do projeto
- Listagem de diretorios
- Busca de arquivos por padrao
- Acesso restrito ao diretorio configurado

---

### 2. Memory Server (Knowledge Graph)
| Propriedade | Valor |
|-------------|-------|
| **Package** | `@modelcontextprotocol/server-memory` |
| **Funcao** | Memoria persistente entre sessoes |
| **Status** | ONLINE |

**Capacidades:**
- Armazenamento de entidades e relacoes
- Grafo de conhecimento persistente
- Contexto entre conversas
- Recuperacao de informacoes salvas

---

### 3. Sequential Thinking Server
| Propriedade | Valor |
|-------------|-------|
| **Package** | `@modelcontextprotocol/server-sequential-thinking` |
| **Funcao** | Raciocinio estruturado e planejamento |
| **Status** | ONLINE |

**Capacidades:**
- Decomposicao de problemas complexos
- Planejamento passo-a-passo
- Analise estruturada
- Tomada de decisao guiada

---

### 4. Puppeteer Server
| Propriedade | Valor |
|-------------|-------|
| **Package** | `puppeteer-mcp-server` |
| **Funcao** | Automacao de navegador headless |
| **Status** | CONFIGURADO |

**Capacidades:**
- Navegacao web automatizada
- Screenshots de paginas
- Extracao de dados de websites
- Testes de interface

---

### 5. Playwright Server
| Propriedade | Valor |
|-------------|-------|
| **Package** | `@anthropic/claude-code-mcp-server-playwright` |
| **Funcao** | Testes E2E e automacao avancada |
| **Status** | CONFIGURADO |

**Capacidades:**
- Testes cross-browser
- Automacao de formularios
- Captura de screenshots/videos
- Testes de acessibilidade

---

## Arquivo de Configuracao

**Localizacao:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Jussara Thomaz\\Documents\\VERTIV_V6_GLOBAL"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "puppeteer-mcp-server"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/claude-code-mcp-server-playwright"]
    }
  }
}
```

---

## Verificacao de Saude

Para verificar se os servidores estao funcionando:

```powershell
# Filesystem
npx -y @modelcontextprotocol/server-filesystem "C:\seu\diretorio"

# Memory
npx -y @modelcontextprotocol/server-memory

# Sequential Thinking
npx -y @modelcontextprotocol/server-sequential-thinking
```

---

## Troubleshooting

### Servidor nao inicia
1. Verifique se o Node.js esta instalado (v18+)
2. Execute `npm cache clean --force`
3. Reinstale o pacote: `npx -y <package-name>`

### JSON invalido
1. Valide o JSON: `node -e "JSON.parse(require('fs').readFileSync('config.json'))"`
2. Verifique virgulas e chaves

### Servidor nao aparece no Claude Desktop
1. Feche completamente o Claude Desktop
2. Verifique o arquivo de config em `%APPDATA%\Claude\`
3. Reinicie o Claude Desktop

---

## Dependencias

| Dependencia | Versao Minima |
|-------------|---------------|
| Node.js | v18.0.0+ |
| npm | v8.0.0+ |
| npx | v8.0.0+ |

---

## Changelog

### 2025-12-24
- Configuracao inicial dos 5 servidores MCP
- Validacao e health check realizado
- Documentacao gerada automaticamente

---

**Gerado por:** AGENTE 5 - MCPDocumentationGenerator
**Projeto:** VERTIV v6.0 - GLOBAL EDITION
