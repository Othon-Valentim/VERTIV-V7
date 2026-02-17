import os
import httpx
import json
import asyncio
from dotenv import load_dotenv

# Load .env from root
load_dotenv()

async def test_serper_connectivity():
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key or api_key == "YOUR_SERPER_KEY_HERE":
        print("❌ Error: SERPER_API_KEY not found or not set in .env")
        return

    print(f"🚀 Testing Serper API with key: {api_key[:5]}...")
    
    url = "https://google.serper.dev/search"
    payload = {
        "q": "preço m2 lançamento imobiliário Belo Horizonte Centro",
        "gl": "br",
        "hl": "pt-br"
    }
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if "organic" in data:
                print(f"✅ Success! Found {len(data['organic'])} organic results.")
                for i, result in enumerate(data['organic'][:3]):
                    print(f"  [{i+1}] {result.get('title')}")
                    print(f"      Link: {result.get('link')}")
            else:
                print("⚠️ Warning: No organic results found in response.")
                print(json.dumps(data, indent=2))
                
    except Exception as e:
        print(f"❌ API Call Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_serper_connectivity())
