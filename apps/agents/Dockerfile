FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expor porta padrão MCP (SSE ou Stdio - aqui configuraremos para SSE via uvicorn se necessário, 
# mas o FastMCP mcp.run() geralmente usa stdio por padrão.
# Para HTTP/SSE, precisamos adaptar. O FastMCP tem suporte a sse.
# Vamos assumir uso via stdio para integração local ou wrapper HTTP.
# PARA CLOUD RUN: Melhor expor via HTTP SSE.

CMD ["python", "src/server.py"]
