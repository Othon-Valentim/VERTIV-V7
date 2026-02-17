# PROTOCOLO MANUS: Engenharia de Contexto & Rigor

Este protocolo define a metodologia de planejamento e execução do Agente no Workspace VERTIV.

## 1. Ciclo de Trabalho Obrigatório
Antes de modificar qualquer código funcional, o Agente DEVE:
1.  **Context Reading:** Ler este arquivo e o `REQUIREMENTS.md`.
2.  **Planning:** Criar ou atualizar `.agent/scratchpad.md` com a análise do contexto atual.
3.  **Task Plan:** Gerar um `task_plan.md` detalhado com os passos de execução.
4.  **Verification:** Validar se o plano respeita os Axiomas e Kill Switches.

## 2. Protocolo de Resiliência (Three Strike Error Protocol)
Se uma execução de comando ou script falhar:
1.  **Strike 1:** O Agente deve ler os logs de erro, identificar a causa raiz e tentar uma correção em código ou ambiente.
2.  **Strike 2:** Se falhar novamente, o Agente deve realizar uma pesquisa técnica (usando `firecrawl` ou `search_web`) ou consultar a documentação local (KB_CORE) para encontrar uma solução alternativa.
3.  **Strike 3:** Se o erro persistir, o Agente interrompe a execução e solicita intervenção do Arquiteto Humano apresentando o diagnóstico completo das tentativas.

## 3. Memória de Trabalho (Scratchpad)
O arquivo `scratchpad.md` é a memória de curto prazo. Use-o para:
- Guardar estados de variáveis temporárias.
- Rastrear o progresso de sub-tarefas.
- Documentar bugs encontrados durante o desenvolvimento.
