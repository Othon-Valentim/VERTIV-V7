from mcp.server.fastmcp import FastMCP
from typing import List, Dict
import httpx
import json
import os
from pydantic import BaseModel

# Inicializa o Servidor FastMCP
mcp = FastMCP("Vertiv-Intelligence-Swarm")


# --- HELPER FUNCTIONS ---
async def perform_serper_search(query: str, num_results: int = 3) -> List[Dict]:
    import os
    import json

    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    results = []

    if SERPER_API_KEY:
        try:
            print(f"🌐 Serper Search: '{query}'")
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": query, "num": num_results})
            headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, headers=headers, data=payload, timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                if "organic" in data:
                    results = data["organic"]
        except Exception as e:
            print(f"⚠️ Serper Error: {e}")
    return results


async def read_url_content(url: str) -> str:
    """Reads HTML or PDF content from a URL."""
    try:
        print(f"📥 Reading content from: {url}")
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, timeout=15.0)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "").lower()

            if "application/pdf" in content_type or url.lower().endswith(".pdf"):
                # Handle PDF
                import io
                from pypdf import PdfReader

                f = io.BytesIO(response.content)
                reader = PdfReader(f)
                text = ""
                for page in reader.pages[:5]:  # Read first 5 pages to save time/tokens
                    text += page.extract_text() + "\n"
                return f"[PDF CONTENT EXTRACTED]:\n{text[:2000]}..."  # Limit size
            else:
                # Handle HTML
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(response.text, "html.parser")
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()
                # Break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # Break multi-headlines into a line each
                chunks = (
                    phrase.strip() for line in lines for phrase in line.split("  ")
                )
                # Drop blank lines
                text = "\n".join(chunk for chunk in chunks if chunk)
                return f"[HTML CONTENT EXTRACTED]:\n{text[:2000]}..."

    except Exception as e:
        return f"failed to read content: {str(e)}"


# --- AGENTE A: SCOUT (Inteligência Regulatória) ---
@mcp.tool()
async def scout_regulatory_search(municipality: str, query: str) -> str:
    """
    Agente Scout: Busca informações regulatórias (Plano Diretor, Zoneamento).
    Usa Serper.dev para pesquisa real e TENTA LER O CONTEÚDO dos links.
    """

    # 1. Search
    search_query = f"Plano Diretor {municipality} {query} pdf"
    results = await perform_serper_search(search_query)

    TRUSTED_DOMAINS = [".gov.br", ".leg.br", ".jusbrasil.com.br", ".org.br"]

    if results:
        report = f"🔎 Relatório Scout AO VIVO para {municipality}:\n\n"

        # Filter for trusted domains first
        trusted_results = [
            r for r in results if any(d in r.get("link", "") for d in TRUSTED_DOMAINS)
        ]

        # If no trusted, use top generic result
        candidates = trusted_results if trusted_results else [results[0]]

        for idx, result in enumerate(candidates[:2]):  # Analyze top 2 candidates
            title = result.get("title", "No Title")
            link = result.get("link", "")
            snippet = result.get("snippet", "")

            is_trusted = (
                "✅ TRUSTED"
                if any(d in link for d in TRUSTED_DOMAINS)
                else "⚠️ GENERAL WEB"
            )

            report += f"🏆 Result {idx+1} [{is_trusted}]: {title}\n🔗 Link: {link}\n📝 Snippet: {snippet}\n"

            # Deep Read (Only first one to save time)
            if idx == 0:
                content = await read_url_content(link)
                report += f"\n📖 Conteúdo Lido:\n{content}\n"

        return report

    # Fallback Mock
    mock_knowledge_base = {
        "Leopoldina": {
            "coeficiente_aproveitamento": "Zona Central (ZC): CA Max 4.0",
            "recuo_frontal": "Obrigatório 5m em vias arteriais",
            "gabarito": "Livre, respeitando cone de aproximação se houver aeródromo",
        },
        "Sao Paulo": {
            "coeficiente_aproveitamento": "Eixo de Estruturação: CA Max 4.0",
            "outorga": "Onerosa acima de CA 1.0",
        },
    }

    city_data = mock_knowledge_base.get(municipality, {})
    if not city_data:
        return f"Nenhuma informação específica encontrada para {municipality} (Mock). Adicione SERPER_API_KEY para busca real."

    return f"Relatório Scout (MOCK) para {municipality}:\n" + "\n".join(
        [f"- {k}: {v}" for k, v in city_data.items()]
    )


# Protocol Alias
@mcp.tool()
async def find_master_plan(city: str) -> str:
    """Protocol Alias for scout_regulatory_search"""
    return await scout_regulatory_search(city, "zoneamento coeficiente aproveitamento")


# --- AGENTE B: BENCHMARK (Espião de Mercado) ---
@mcp.tool()
async def benchmark_market_scan(
    neighborhood: str, product_type: str
) -> Dict[str, float]:
    """
    Agente Benchmark: Varre portais imobiliários para encontrar preço médio.
    """
    print(f"🕵️ [BENCHMARK] Escaneando {neighborhood} para {product_type}")

    # 1. Search
    query = f"preço m2 apartamento venda {neighborhood} {product_type}"
    results = await perform_serper_search(query)

    import re

    price_regex = r"R\$\s?([\d\.,]+)"

    prices_found = []

    if results:
        for res in results[:5]:
            snippet = res.get("snippet", "")
            title = res.get("title", "")
            text = f"{title} {snippet}"

            matches = re.findall(price_regex, text)
            for m in matches:
                # Clean string "2.500,00" -> 2500.00
                clean_val = m.replace(".", "").replace(",", ".")
                try:
                    val = float(clean_val)
                    # Sanity check: Price/sqm usually > 2000 and < 100000
                    if 2000 < val < 100000:
                        prices_found.append(val)
                    elif 200000 < val < 2000000:
                        # Maybe total price? Ignore for now, focused on m2 or fix logic
                        pass
                except:
                    pass

    if prices_found:
        avg = sum(prices_found) / len(prices_found)
        return {
            "avg_price_sqm": round(avg, 2),
            "listing_count": len(prices_found),
            "samples": prices_found,
            "source": "Live Web Search (Serper)",
        }

    # Fallback Stub
    return {
        "avg_price_sqm": 7500.00,
        "listing_count": 42,
        "absorption_rate_mo": 0.08,  # 8% ao mês
        "source": "Mock (Fallback)",
    }


# Protocol Alias
@mcp.tool()
async def get_neighborhood_price(neighborhood: str) -> Dict[str, float]:
    """Protocol Alias for benchmark_market_scan"""
    return await benchmark_market_scan(neighborhood, "apartamento padrão")


@mcp.tool()
async def benchmark_greenium_search() -> Dict[str, float]:
    """
    Agente Benchmark: Busca taxas de Debêntures Incentivadas vs NTN-B
    para estimar o Spread Verde (Greenium).
    """
    print(f"🌿 [BENCHMARK] Buscando Greenium Spread na Web...")

    query = "spread debêntures incentivadas ipca+ hoje report"
    results = await perform_serper_search(query, num_results=3)

    found_spread = 0.003  # 0.30% default fallback
    source_info = "Mock/Conservative Estimate"

    if results:
        # Simplistic logic: Just returning the snippet for now as "proof of search"
        # In a real agent, we would use LLM to extract the exact spread from the text.
        # For this tool, we will return the search metadata.
        top_snippet = results[0].get("snippet", "")
        source_info = f"Serper Search: {results[0].get('title')}"

        # Fake intelligence extraction (placeholder for LLM extraction)
        if "0,50%" in top_snippet:
            found_spread = 0.005
        elif "0,20%" in top_snippet:
            found_spread = 0.002

    return {
        "greenium_spread_bps": found_spread * 10000,
        "greenium_rate": found_spread,
        "source": source_info,
    }


# --- AGENTE C: AUDITOR (Polícia de Proveniência) ---
@mcp.tool()
async def auditor_verify_source(claim: str, source_cited: str) -> bool:
    """
    Agente Auditor: Verifica se uma afirmação corresponde à fonte citada.
    """
    print(f"⚖️ [AUDITOR] Verificando: '{claim}' vs Fonte: '{source_cited}'")

    # Lógica de Verificação (Poderia usar LLM para comparar Texto vs Fonte)
    if "IBGE" in source_cited and "população" in claim.lower():
        return True  # Assume IBGE é autoridade para população

    return False  # Default cético


if __name__ == "__main__":
    # Rodar servidor
    mcp.run()
