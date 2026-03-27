# Deploy VERTIV V7 Frontend na Vercel

## Pré-requisitos
- Node.js 18+ instalado
- Conta Vercel (team: Palmáceas' projects)
- Repo GitHub: github.com/Othon-Valentim/vertiv-platform.git
- Backend rodando em: https://api.vertiv.tech

---

## OPÇÃO A: Deploy via Dashboard (Recomendado para primeira vez)

### Passo 1 — Commit das alterações
```bash
cd C:\Users\Jussara Thomaz\Documents\VERTIV_V6_GLOBAL
git add apps/frontend/next.config.js
git commit -m "fix: remove standalone output for Vercel compatibility"
git push origin master
```

### Passo 2 — Criar projeto na Vercel
1. Acesse https://vercel.com/new
2. Clique em **"Import Git Repository"**
3. Selecione o repositório `vertiv-platform`
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
| `NEXT_PUBLIC_API_URL` | `https://api.vertiv.tech` |
| `NEXT_PUBLIC_SUPABASE_URL` | `https://nutilcpmpapjowqmxoqf.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dGlsY3BtcGFwam93cW14b3FmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5NDg1OTksImV4cCI6MjA4MTUyNDU5OX0.VhvEhOJOLc_Xkf2BvMQs4IbqcJtnmSEXPNfMwvuPXgY` |
| `NEXT_PUBLIC_DOMAIN` | `vertiv.tech` |

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
cd C:\Users\Jussara Thomaz\Documents\VERTIV_V6_GLOBAL
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
- **Which scope?** → Palmáceas' projects
- **Link to existing project?** → N (criar novo)
- **Project name?** → vertiv-frontend
- **In which directory is your code located?** → ./ (já está em apps/frontend)

### Passo 5 — Configurar variáveis de ambiente
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Cole: https://api.vertiv.tech

vercel env add NEXT_PUBLIC_SUPABASE_URL production
# Cole: https://nutilcpmpapjowqmxoqf.supabase.co

vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY production
# Cole: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dGlsY3BtcGFwam93cW14b3FmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5NDg1OTksImV4cCI6MjA4MTUyNDU5OX0.VhvEhOJOLc_Xkf2BvMQs4IbqcJtnmSEXPNfMwvuPXgY

vercel env add NEXT_PUBLIC_DOMAIN production
# Cole: vertiv.tech
```

### Passo 6 — Redeploy com variáveis
```bash
vercel --prod
```

---

## Configurar Domínio app.vertiv.tech

### Na Vercel:
```bash
vercel domains add app.vertiv.tech
```
Ou no Dashboard: Settings → Domains → Add → `app.vertiv.tech`

### No seu DNS (registrador do domínio):
Adicione um registro CNAME:
```
Tipo: CNAME
Nome: app
Valor: cname.vercel-dns.com
TTL: 300
```

Se quiser `vertiv.tech` (apex/raiz) também na Vercel:
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
    "https://vertiv.tech",
    "https://app.vertiv.tech",
    "https://www.vertiv.tech",
    "https://vertiv-frontend-*.vercel.app",  # preview deploys
    "http://localhost:3000",  # dev local
]
```

---

## Teste E2E: Upload de ZIP

Após o deploy estar live:

1. Acesse `https://app.vertiv.tech` (ou a URL temporária da Vercel)
2. Faça login
3. Vá para Dashboard → Upload
4. Faça upload de um arquivo ZIP de teste
5. Confirme que o pipeline de simulação inicia
6. Verifique no Network tab do DevTools que as chamadas vão para `api.vertiv.tech`

### Teste rápido via curl:
```bash
# Testar se o frontend responde
curl -I https://app.vertiv.tech

# Testar se o backend responde
curl https://api.vertiv.tech/health

# Testar CORS
curl -H "Origin: https://app.vertiv.tech" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     https://api.vertiv.tech/api/v1/simulations/upload
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
