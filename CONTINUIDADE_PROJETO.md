# VERTIV v6.0 - Documentacao de Continuidade

## Status Atual do Projeto

**Data:** 17/12/2025
**Plataforma:** https://vertiv.tech
**API:** https://api.vertiv.tech

---

## 1. INFRAESTRUTURA IMPLEMENTADA

### 1.1 Google Cloud Platform
- **Projeto:** vertiv-prod-v1
- **Regiao:** us-central1
- **Servicos:**
  - Cloud Run: vertiv-frontend, vertiv-backend
  - Cloud Build: CI/CD automatizado
  - Container Registry: gcr.io/vertiv-prod-v1/

### 1.2 Cloudflare
- **Dominio:** vertiv.tech
- **DNS:** Configurado com proxy
- **Worker:** Proxy para Cloud Run (vertiv-proxy)
- **SSL:** Full (strict)

### 1.3 Supabase
- **Projeto:** nutilcpmpapjowqmxoqf
- **URL:** https://nutilcpmpapjowqmxoqf.supabase.co
- **Anon Key:** eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dGlsY3BtcGFwam93cW14b3FmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5NDg1OTksImV4cCI6MjA4MTUyNDU5OX0.VhvEhOJOLc_Xkf2BvMQs4IbqcJtnmSEXPNfMwvuPXgY

### 1.4 Tabelas Supabase Criadas
```sql
-- Tabela de analises TIV (JA CRIADA)
CREATE TABLE analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  data JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS habilitado com politicas para cada usuario ver apenas suas analises
```

---

## 2. ESTRUTURA DO PROJETO

```
VERTIV_V6_GLOBAL/
├── apps/
│   ├── frontend/          # Next.js 14 App Router
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── page.tsx              # Landing page
│   │   │   │   ├── layout.tsx            # Root layout com AuthProvider
│   │   │   │   ├── auth/
│   │   │   │   │   ├── login/page.tsx    # Pagina de login
│   │   │   │   │   └── register/page.tsx # Pagina de registro
│   │   │   │   ├── wizard/page.tsx       # TIV Wizard (10 passos)
│   │   │   │   └── dashboard/
│   │   │   │       ├── portfolio/        # Gestao de portfolio
│   │   │   │       ├── real-options/     # Opcoes reais
│   │   │   │       └── tribunal/         # Tribunal de deals
│   │   │   ├── components/
│   │   │   │   ├── wizard/steps/         # Componentes dos 10 passos
│   │   │   │   │   ├── p1-garimpo.tsx
│   │   │   │   │   ├── p2-economic.tsx
│   │   │   │   │   ├── p4-vocation.tsx
│   │   │   │   │   ├── p5-legal.tsx
│   │   │   │   │   ├── p6-p9-market.tsx
│   │   │   │   │   └── p10-financial.tsx
│   │   │   │   ├── ProtectedRoute.tsx
│   │   │   │   └── UserMenu.tsx
│   │   │   ├── contexts/
│   │   │   │   └── AuthContext.tsx       # Contexto de autenticacao
│   │   │   └── lib/
│   │   │       ├── supabase.ts           # Cliente Supabase
│   │   │       └── analyses.ts           # Servico de persistencia
│   │   └── package.json                  # @supabase/supabase-js: 2.33.2
│   │
│   └── backend/           # FastAPI Python
│       ├── main.py
│       ├── routers/
│       │   ├── bcb.py                    # Indicadores BCB
│       │   ├── p2_economic.py            # Dinamica economica
│       │   └── simulation.py             # Simulacoes
│       └── requirements.txt
│
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── frontend.cloudbuild.yaml
│   └── backend.cloudbuild.yaml
│
└── packages/
    └── shared/            # Tipos compartilhados
```

---

## 3. FUNCIONALIDADES IMPLEMENTADAS

### 3.1 Autenticacao (Supabase Auth)
- [x] Login com email/senha
- [x] Registro com confirmacao por email
- [x] Logout
- [x] Contexto de autenticacao (AuthContext)
- [x] Componente UserMenu
- [x] Redirect URLs configuradas (vertiv.tech)
- [x] Email templates personalizados (VERTIV)

### 3.2 TIV Wizard - 10 Passos
- [x] P1: Garimpo & Ciclo - Screening inicial
- [x] P2: Dinamica Economica - Indicadores BCB ao vivo
- [ ] P3: Area de Influencia - PLACEHOLDER (precisa Mapbox/Google Maps)
- [x] P4: Vocacao & Produto - Matriz 3 pilares
- [x] P5: Legal & Restricoes - Gate binario
- [x] P6: Demanda Qualificada - Funil 5 estagios
- [x] P7: Oferta & Mercado - Benchmark concorrencia
- [x] P8: Absorcao (VSO) - Projecao velocidade vendas
- [x] P9: Convalidacao 4:1 - Gate estrategico
- [x] P10: Modelagem Financeira - DCF + Opcoes Reais

### 3.3 Persistencia de Dados
- [x] Tabela analyses no Supabase
- [x] Servico analysesService (lib/analyses.ts)
- [x] Botoes Salvar/Abrir/Nova Analise no Wizard
- [x] Auto-save com indicador de status
- [x] Lista de analises salvas
- [x] Excluir analises

### 3.4 Backend API
- [x] /api/bcb/indicators - Indicadores economicos
- [x] /api/p2/municipality-data - Dados municipais
- [x] /api/simulation/* - Simulacoes financeiras

---

## 4. O QUE FALTA IMPLEMENTAR

### 4.1 Persistencia (Melhorias)
- [ ] Auto-save automatico a cada mudanca
- [ ] Indicador de "nao salvo" quando ha alteracoes
- [ ] Compartilhar analise com outros usuarios
- [ ] Duplicar analise existente
- [ ] Exportar/Importar analises (JSON)

### 4.2 Dashboard do Usuario
- [ ] Pagina /dashboard com lista de analises
- [ ] Cards com preview de cada analise
- [ ] Filtros e busca
- [ ] Ordenacao por data/nome/progresso

### 4.3 Exportacao PDF
- [ ] Gerar relatorio profissional
- [ ] Template com logo VERTIV
- [ ] Graficos e tabelas formatados
- [ ] Deal Memo automatico

### 4.4 P3 - Area de Influencia
- [ ] Integracao com Mapbox ou Google Maps
- [ ] Desenho de isocronas (5, 10, 15 min)
- [ ] Dados demograficos por area
- [ ] Heatmap de renda/populacao

### 4.5 Melhorias de UX
- [ ] Loading states em todas as acoes
- [ ] Toasts de feedback (sucesso/erro)
- [ ] Validacao de formularios
- [ ] Responsividade mobile
- [ ] Dark/Light mode toggle

### 4.6 Seguranca
- [ ] Rate limiting na API
- [ ] Validacao de inputs
- [ ] Logs de auditoria
- [ ] Backup automatico

---

## 5. COMANDOS UTEIS

### 5.1 Deploy Frontend
```bash
cd "C:\Users\Jussara Thomaz\Documents\VERTIV_V6_GLOBAL"

gcloud builds submit --config=docker/frontend.cloudbuild.yaml \
  --substitutions=_NEXT_PUBLIC_API_URL="https://api.vertiv.tech",_NEXT_PUBLIC_SUPABASE_URL="https://nutilcpmpapjowqmxoqf.supabase.co",_NEXT_PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dGlsY3BtcGFwam93cW14b3FmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5NDg1OTksImV4cCI6MjA4MTUyNDU5OX0.VhvEhOJOLc_Xkf2BvMQs4IbqcJtnmSEXPNfMwvuPXgY"

gcloud run deploy vertiv-frontend \
  --image gcr.io/vertiv-prod-v1/vertiv-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### 5.2 Deploy Backend
```bash
gcloud builds submit --config=docker/backend.cloudbuild.yaml

gcloud run deploy vertiv-backend \
  --image gcr.io/vertiv-prod-v1/vertiv-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

### 5.3 Verificar Status
```bash
gcloud run services list
gcloud run services describe vertiv-frontend --region us-central1
gcloud run services describe vertiv-backend --region us-central1
```

---

## 6. ARQUIVOS CHAVE PARA REFERENCIA

### 6.1 Autenticacao
- `apps/frontend/src/lib/supabase.ts` - Cliente Supabase
- `apps/frontend/src/contexts/AuthContext.tsx` - Provider de auth
- `apps/frontend/src/app/auth/login/page.tsx` - Pagina login
- `apps/frontend/src/app/auth/register/page.tsx` - Pagina registro

### 6.2 Persistencia
- `apps/frontend/src/lib/analyses.ts` - Servico CRUD analises
- `apps/frontend/src/app/wizard/page.tsx` - Wizard com save/load

### 6.3 Configuracao
- `apps/frontend/package.json` - Dependencias (Supabase 2.33.2)
- `docker/Dockerfile.frontend` - Build com env vars
- `docker/frontend.cloudbuild.yaml` - CI/CD config

---

## 7. PROBLEMAS CONHECIDOS E SOLUCOES

### 7.1 Supabase SDK ESM Error
**Problema:** Versoes >= 2.34.0 causam erro de ESM no build
**Solucao:** Usar versao exata 2.33.2 no package.json

### 7.2 Redirect para localhost
**Problema:** Email de confirmacao redireciona para localhost:3000
**Solucao:** Configurar Site URL no Supabase Dashboard > Authentication > URL Configuration

### 7.3 Build lento no Cloud Build
**Problema:** Build demora ~3-4 minutos
**Solucao:** Normal para projeto Next.js. Cache ajuda em builds subsequentes.

---

## 8. PROXIMOS PASSOS SUGERIDOS

1. **Testar persistencia atual** - Verificar se save/load funciona
2. **Implementar Dashboard** - Criar /dashboard com lista de analises
3. **Adicionar Toasts** - Feedback visual para acoes
4. **Exportacao PDF** - Gerar relatorios profissionais
5. **P3 Mapeamento** - Integrar API de mapas

---

## 9. CREDENCIAIS E ACESSOS

### Supabase
- Dashboard: https://supabase.com/dashboard/project/nutilcpmpapjowqmxoqf
- URL: https://nutilcpmpapjowqmxoqf.supabase.co
- Anon Key: (ver secao 1.3)

### Google Cloud
- Console: https://console.cloud.google.com/run?project=vertiv-prod-v1
- Projeto: vertiv-prod-v1

### Cloudflare
- Dashboard: https://dash.cloudflare.com
- Dominio: vertiv.tech
- Worker: vertiv-proxy

---

**Documento criado para continuidade do desenvolvimento VERTIV v6.0**
