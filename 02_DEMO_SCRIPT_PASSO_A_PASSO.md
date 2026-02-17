# VERTIV v6.0 — Roteiro de Demonstração (15 Minutos)

## Pré-requisitos
-   Certifique-se de que o backend (`apps/backend` na porta 8000) e o frontend (`apps/frontend` na porta 3000) estão rodando.
-   Tenha uma conta de demonstração funcional no Supabase.
-   Chave da API `Serper` ativa no `.env` do backend.

---

## 00:00 – 02:00 | Introdução e Login (O "Impacto Inicial")
1.  **Acesse:** `http://localhost:3000`
2.  **Tela:** Landing Page "Stoic Premium".
3.  **Ação:** Role suavemente para mostrar a estética minimalista e as animações de entrada.
4.  **Ação:** Clique em "Entrar na Plataforma".
5.  **Ação:** Preencha login/senha de demo.
6.  **Observar:** A velocidade do Auth e o redirecionamento imediato para o Dashboard.
    *   *Direcione o olhar do engenheiro:* "Note que não usamos bibliotecas de UI pesadas, é Tailwind puro para performance máxima."

## 02:00 – 05:00 | O Dashboard e a Arquitetura
1.  **Tela:** Dashboard Principal.
2.  **Cenário:** Mostrar os cards de "Projetos Recentes" e "Indicadores de Mercado".
3.  **Ação:** Passe o mouse sobre os cards para mostrar os efeitos de "Hover" e micro-interações.
4.  **Erro (Intencional):** Tente clicar em um módulo desativado (ex: "Fase 3 - Jurídico").
    *   **Resultado Esperado:** Um Toast/Notificação elegante dizendo "Módulo indisponível no seu plano atual" ou "Em desenvolvimento".
    *   *Observar:* O sistema de tratamento de erros no frontend não quebra a tela, apenas informa o usuário.

## 05:00 – 10:00 | O "Core": P1 Garimpo e ScoutAgent
1.  **Ação:** Navegue para "Novo Projeto" > "P1 Garimpo".
2.  **Tela:** Wizard Passo 1 - Dados do Terreno.
3.  **Ação (Entrada):**
    *   Nome: "Residencial Jardins da Aurora"
    *   Área: `5000` m²
    *   Preço Pedido: `15000000` (15M)
4.  **Ação:** Clique em "Analisar Viabilidade Preliminar".
5.  **O "Wow Moment" (ScoutAgent):**
    *   Enquanto o sistema processa, aponte para o indicador de "ScoutAgent Active".
    *   *Explique:* "Aqui o backend Python dispara workers assíncronos que vão ao Google (via Serper API) buscar concorrentes na região em tempo real."
6.  **Resultado:** A tela exibe o "Score de Atratividade" e o "Go/No-Go Reasoning".
    *   *Observar:* A integração de dados financeiros (Polars) com dados externos.

## 10:00 – 13:00 | Deep Dive: Real Options (Financeiro)
1.  **Ação:** Clique em "Detalhes Financeiros" (ou navegue para a calculadora Black-Scholes).
2.  **Cenário:** Alterar a volatilidade do mercado.
3.  **Ação:** Mude a volatilidade de `20%` para `40%`.
4.  **Resultado:** O gráfico de "Opção de Espera" e o VPL expandido atualizam *instantaneamente*.
    *   *Observar:* "Não há refresh de página. O Polars recalcula no backend e o React atualiza o estado via SWR/React Query."

## 13:00 – 15:00 | Encerramento e Perguntas
1.  **Ação:** Logout.
2.  **Abertura para Feedback:** "Como você viu, focamos em manter o 'Core' extremamente rápido. Alguma consideração sobre como estruturamos a comunicação assíncrona dos agentes?"

---

## Pontos de Atenção para o Engenheiro
-   **Latência:** Verificar se a busca do ScoutAgent não está bloqueando a UI (non-blocking IO).
-   **Tipagem:** Confirmar se as interfaces TypeScript estão batendo 100% com os schemas Pydantic.
-   **Escalabilidade:** Perguntar como lidaríamos com 10.000 requisições simultâneas no Polars.
