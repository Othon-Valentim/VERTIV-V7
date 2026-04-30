# Deploy VERTIV V7 Frontend na Vercel

## Pré-requisitos
- Node.js 18+ instalado
- Conta Vercel
- Repo GitHub: <REPO_URL>
- Backend rodando em: <API_BASE_URL>

---

## OPÇÃO A: Deploy via Dashboard (Recomendado para primeira vez)

### Passo 1 — Commit das alterações
```bash
cd <PROJECT_ROOT>
git add apps/frontend/next.config.js
git commit -m "fix: remove standalone output for Vercel compatibility"
git push origin master
```

### Passo 2 — Criar projeto na Vercel
1. Acesse https://vercel.com/new
2. Clique em **"Import Git Repository"**
3. Selecione o repositório `<REPO_NAME>`
4. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** `apps/frontend` ← IMPORTANTE!
   - **Build Command:** `npm run build` (padrão)
   - **Output Directory:** (deixe vazio, padrão do Next.js)
   - **Install Command:** `npm install`

### Passo 3 — Variáveis de Ambiente
Na seção "Environment Variables" antes de clicar Deploy, adicione:

| Variável | Valor |
|---|---|
| `NEXT_PUBLIC_API_URL` | `<API_BASE_URL>` |
| `NEXT_PUBLIC_SUPABASE_URL` | `<NEXT_PUBLIC_SUPABASE_URL>` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `<NEXT_PUBLIC_SUPABASE_ANON_KEY>` |
| `NEXT_PUBLIC_DOMAIN` | `<NEXT_PUBLIC_DOMAIN>` |

> Use apenas placeholders neste arquivo. Valores reais devem ser configurados em Vercel Environment Variables ou em arquivos `.env` locais e nunca commitados.

### Passo 4 — Deploy!
Clique **"Deploy"** e aguarde o build completar (~2-3 min).

---

## OPÇÃO B: Deploy via CLI

### Passo 1 — Instalar Vercel CLI
```bash
npm install -g vercel
```

### Passo 2 — Login
```bash
vercel login
```

### Passo 3 — Commit e push primeiro
```bash
cd <PROJECT_ROOT>
git add apps/frontend/next.config.js
git commit -m "fix: remove standalone output for Vercel compatibility"
git push origin master
```

### Passo 4 — Deploy do frontend
```bash
cd apps/frontend
vercel --yes
```

Quando perguntar:
- **Set up and deploy?** → Y
- **Which scope?** → <VERCEL_ORG_ID>
- **Link to existing project?** → N (criar novo)
- **Project name?** → vertiv-frontend
- **In which directory is your code located?** → ./ (já está em apps/frontend)

### Passo 5 — Configurar variáveis de ambiente
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Cole: <API_BASE_URL>

vercel env add NEXT_PUBLIC_SUPABASE_URL production
# Cole: <NEXT_PUBLIC_SUPABASE_URL>

vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY production
# Cole: <NEXT_PUBLIC_SUPABASE_ANON_KEY>

vercel env add NEXT_PUBLIC_DOMAIN production
# Cole: <NEXT_PUBLIC_DOMAIN>
```

### Passo 6 — Redeploy com variáveis
```bash
vercel --prod
```

---

## Configurar Domínio app.<NEXT_PUBLIC_DOMAIN>

### Na Vercel:
```bash
vercel domains add app.<NEXT_PUBLIC_DOMAIN>
```
Ou no Dashboard: Settings → Domains → Add → `app.<NEXT_PUBLIC_DOMAIN>`

### No seu DNS (registrador do domínio):
Adicione um registro CNAME:
```
Tipo: CNAME
Nome: app
Valor: cname.vercel-dns.com
TTL: 300
```

Se quiser `<NEXT_PUBLIC_DOMAIN>` (apex/raiz) também na Vercel:
```
Tipo: A
Nome: @
Valor: 76.76.21.21
TTL: 300
```

---

## Verificação CORS no Backend

Confirme que o backend aceita requests de ambos os domínios.
No backend FastAPI, verifique o `allow_origins`:

```python
origins = [
    "https://<NEXT_PUBLIC_DOMAIN>",
    "https://app.<NEXT_PUBLIC_DOMAIN>",
    "https://www.<NEXT_PUBLIC_DOMAIN>",
    "https://<VERCEL_PREVIEW_DOMAIN>",  # preview deploys
    "http://localhost:3000",  # dev local
]
```

---

## Teste E2E: Upload de ZIP

Após o deploy estar live:

1. Acesse `https://app.<NEXT_PUBLIC_DOMAIN>` (ou a URL temporária da Vercel)
2. Faça login
3. Vá para Dashboard → Upload
4. Faça upload de um arquivo ZIP de teste
5. Confirme que o pipeline de simulação inicia
6. Verifique no Network tab do DevTools que as chamadas vão para `<API_BASE_URL>`

### Teste rápido via curl:
```bash
# Testar se o frontend responde
curl -I https://app.<NEXT_PUBLIC_DOMAIN>

# Testar se o backend responde
curl <API_BASE_URL>/health

# Testar CORS
curl -H "Origin: https://app.<NEXT_PUBLIC_DOMAIN>" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     <API_BASE_URL>/api/v1/simulations/upload
```

---

## Troubleshooting

### Build falha com "Could not generate types"
Normal — o prebuild tenta acessar `localhost:8000` que não existe na Vercel.
O script já tem fallback (`|| echo 'Warning...'`). Sem impacto.

### 404 em rotas dinâmicas
Next.js na Vercel lida automaticamente. Não precisa de rewrites extras.

### CORS errors no console
Verificar que `app.vertiv.tech` está na lista `allow_origins` do backend.

### Variáveis de ambiente não funcionam
Variáveis `NEXT_PUBLIC_*` são embutidas no build. Após alterar, é necessário **redeploy**:
```bash
vercel --prod
```
