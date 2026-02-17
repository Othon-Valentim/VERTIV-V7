# VERTIV v6.0 — Roteiro de Reunião Técnica (The Engineering Pitch)

Este roteiro foi desenhado para posicionar você como um **Product Owner Técnico** que entende do negócio e sabe o suficiente de tecnologia para tomar decisões arquiteturais, mas que respeita a especialidade do engenheiro sênior.

---

## Fase 1: Abertura e Contexto (3 Minutos)
**Objetivo:** Capturar a atenção sem entediar com detalhes irrelevantes. Vender o "Problema".

**Tática:** Comece pelo *Business Pain* (Dor do Negócio), não pelo código.

**Script:**
> "Obrigado pelo tempo. Para te dar contexto rápido:
>
> Nós estamos construindo o que eu chamo de 'Bloomberg dos Terrenos'.
>
> Hoje, incorporadoras compram terrenos de milhões baseadas em 'feeling' e planilhas de Excel quebradas. É um processo lento e cego.
>
> O **VERTIV** resolve isso automatizando a viabilidade financeira. A gente cruza dados de mercado (via scraping) com um motor financeiro pesado (Black-Scholes/Polars) pra dizer 'Compre' ou 'Não Compre' em segundos.
>
> **Meu objetivo hoje com você:** Não é te vender o produto. É validar se a nossa arquitetura técnica (Modular Monolith em Python/Next.js) aguenta o tranco quando a gente escalar, e onde você vê buracos que eu não estou vendo."

---

## Fase 2: A Demo Guiada (10-15 Minutos)
**Objetivo:** Mostrar que funciona, mas focar na *Engenharia* por trás da tela.

**Tática:** Use o arquivo `02_DEMO_SCRIPT_PASSO_A_PASSO.md`, mas narre com "viés técnico".

**Momentos Chave (O que falar enquanto clica):**

1.  **No Login:**
    > "Optamos pelo **Supabase** pra não reinventar a roda na Auth. Queria manter a segurança robusta desde o dia 1."

2.  **No Wizard (P1 Garimpo):**
    > "Aqui é o desafio. O usuário preenche o input, e no backend nós disparamos um **Worker assíncrono** (ScoutAgent). Ele vai no Google (Serper API), pega concorrentes, e devolve pro frontend. Minha dúvida atual é se essa arquitetura de workers vai gargalar se tivermos 500 buscas simultâneas."

3.  **Na Calculadora Financeira (Diamond Core):**
    > "Essa é a parte crítica. Abandonamos o Pandas e fomos de **Polars**. Precisamos de performance vetorial porque rodamos simulações de Monte Carlo aqui. O tempo de resposta caiu de 4s pra milissegundos. O que você acha de Polars pra esse caso de uso vs numPy puro?"

---

## Fase 3: Extraindo o Feedback (Deep Dive)
**Objetivo:** Fazer o engenheiro trabalhar pra você. Transforme a crítica em consultoria.

**Frases para Puxar Feedback (Use estas):**

*   **Sobre Arquitetura:**
    > "Eu insisti em manter um **Modular Monolith** (Repo único, apps separados) em vez de Microservices agora. Muita gente diz pra já começar com microserviços, mas achei que ia trazer complexidade demais cedo demais. Qual sua visão sobre isso pra esse estágio?"

*   **Sobre "Gambimaps" (Dívida Técnica Consciente):**
    > "Sendo transparente: a parte de real-time updates do Worker pro Frontend hoje tá fazendo polling simples no banco. WebSockets seria o ideal, mas achamos overkill agora. Isso te assusta ou é aceitável pra um MVP?"

*   **Sobre Segurança:**
    > "Como lidamos com dados sensíveis de valor de terra, minha maior preocupação é vazamento de dados entre tenantes (clientes diferentes). O RLS (Row Level Security) do Supabase é suficiente ou deveríamos ter uma camada lógica na API também?"

---

## Fase 4: O Fechamento (Next Steps)
**Objetivo:** Sair com uma lista de tarefas clara e criar um "gancho" para o futuro.

**Script Final:**
> "Cara, excelente feedback. Anotei aqui: [Cite 1 ponto que ele falou].
>
> Pra fechar: **Se você fosse eu, qual seria a ÚNICA coisa que você mudaria nessa arquitetura amanhã cedo pra dormir mais tranquilo?**"

*(Escute a resposta. Geralmente é a mais valiosa.)*

> "Perfeito. Vou atuar nisso. Obrigado pela consultoria, me ajudou muito a clarear o roadmap técnico."

---

## Cheat Sheet: Vocabulário de "Engenheiro-Chefe"
*(Use com moderação para soar natural)*

*   **"Overkill":** Algo exagerado/complexo demais pro momento.
*   **"Gargalo" (Bottleneck):** Onde o sistema trava quando tem muita gente.
*   **"Latência":** Tempo de espera.
*   **"Stack":** As tecnologias usadas (Next, Python, Polars).
*   **"Trade-off":** "Escolhemos X em vez de Y porque..." (Mostra que você pensou antes de fazer).
*   **"Agnóstico":** O sistema não depende de uma ferramenta específica (ex: "Somos agnósticos a cloud").
