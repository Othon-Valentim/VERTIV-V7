# VERTIV v6.0 — Roadmap de Profissionalização (30 Dias)

**Objetivo Macro:** Transformar o "MVP promissor" em um "Software de Engenharia Robusto". Sair do modo "Demo" para modo "Produção Seguro".

---

## Semana 1: Estancar Sangramentos (Blindagem)
**Objetivo:** Parar de gastar dinheiro à toa (API Serper) e garantir que o Front e Back falem a mesma língua.

*   **Entregáveis:**
    1.  **Cache no ScoutAgent:** Implementar Redis (ou tabela simples no Postgres) para armazenar buscas do Serper por 7 dias. Se o terreno já foi buscado, não paga API.
    2.  **Type Safety Pipeline:** Configurar script (`openapi-typescript-codegen`) para gerar tipos do Frontend automaticamente a cada build do Backend.
    3.  **Sanitização de Inputs:** Garantir que ninguém consiga injetar scripts nos campos de texto do Wizard.

*   **Risco Principal:** Quebrar o build do frontend ao descobrir que metade dos tipos manuais estavam errados.
*   **Como Validar:** Rodar `npm run build` no front sem erros e verificar se buscas repetidas no Worker não incrementam o contador de uso da Serper.dev.

---

## Semana 2: Arquitetura Real-Time (O Fim do Polling)
**Objetivo:** O sistema está engasgando com Polling ("Já acabou?"). Vamos mudar para "Me avise quando acabar".

*   **Entregáveis:**
    1.  **Server-Sent Events (SSE):** Implementar endpoint `/stream` no FastAPI para enviar updates de status do worker.
    2.  **Fila de Mensagens Robusta:** Migrar a task queue para algo com *retry* automático (ex: Celery ou BullMQ) se o Redis cair.
    3.  **UI de Progresso Real:** Trocar o spinner genérico por uma barra de progresso baseada nos eventos do SSE ("Buscando concorrentes... 30%").

*   **Risco Principal:** A complexidade de manter conexões abertas (SSE) no Cloud Run (timeout de proxy).
*   **Como Validar:** Abrir 5 abas simultâneas rodando simulações e ver se o banco de dados continua com CPU baixa (sem picos de polling).

---

## Semana 3: Qualidade e Testes (Confiança)
**Objetivo:** Garantir que o "Diamond Core" (Financeiro) não minta. Um erro de zero aqui destrói a reputação.

*   **Entregáveis:**
    1.  **Testes Unitários (Core):** Cobrir 100% das funções do `P1Screener` e `CashFlowEngine` com Pytest. Crie cenários de borda (juros negativos, terrenos de tamanho zero).
    2.  **Tratamento de Erros Global:** Middleware no Backend que captura exceções não tratadas e devolve JSON limpo, não "Internal Server Error" com stacktrace exposto.
    3.  **Rate Limiting:** Bloquear usuários que tentem fazer mais de 10 análises por minuto.

*   **Risco Principal:** Descobrir bugs lógicos antigos no motor financeiro que obriguem a refatorar a regra de negócio.
*   **Como Validar:** Rodar `pytest --cov` e ver cobertura > 90% no módulo `engine`. Tentar "floodar" a API e ser bloqueado.

---

## Semana 4: Observabilidade e "Go-Live"
**Objetivo:** Ter visão de Raio-X do sistema em produção. Se cair, eu quero saber antes do usuário.

*   **Entregáveis:**
    1.  **Logging Estruturado:** Logs em formato JSON (não texto puro) para serem ingeridos por ferramentas de monitoramento.
    2.  **Health Checks:** Endpoints `/health` profundos (verificam se DB e Redis estão vivos, não só se o servidor está online).
    3.  **Documentação de API (Final):** Swagger/Redoc revisado e limpo para consumo externo eventual.
    4.  **Faxina de Código:** Remover todos os `print()`, códigos comentados e arquivos mortos.

*   **Risco Principal:** O sistema ficar "barulhento" demais com logs inúteis, dificultando achar o erro real.
*   **Como Validar:** Simular uma queda do banco de dados e verificar se o sistema loga o erro corretamente e a UI avisa o usuário de forma elegante ("Serviço instável") em vez de travar.
