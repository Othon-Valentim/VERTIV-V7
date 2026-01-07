import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../apps/backend"))

# Import Service
from src.services.market_data import get_market_service, AnbimaEstimator
from src.engine.regulatory import RegulatoryEngine


def verify_market_data():
    print("--- 📡 Verificando Conectividade de Dados de Mercado (Live) ---")
    service = get_market_service()

    print(f"Service Type: {type(service).__name__}")

    # 1. Selic
    try:
        selic = service.get_selic_rate()
        print(f"✅ Selic (BCB): {selic*100:.2f}%")
    except Exception as e:
        print(f"❌ Falha Selic: {e}")

    # 2. IPCA
    try:
        ipca = service.get_ipca_rate()
        print(f"✅ IPCA (12m accum): {ipca*100:.2f}%")
    except Exception as e:
        print(f"❌ Falha IPCA: {e}")

    # 3. Greenium
    try:
        greenium = AnbimaEstimator.get_greenium_spread()
        print(f"✅ Greenium Spread (Est): {greenium*100:.2f}%")
    except Exception as e:
        print(f"❌ Falha Greenium: {e}")


def verify_it11_penalty():
    print("\n--- 🚒 Verificando Penalidade IT-11 (Minas Gerais) ---")

    base_efficiency = 0.80  # 80%

    # Case A: Residential (Non-Mixed)
    eff_res = RegulatoryEngine.apply_it11_efficiency_penalty(
        "VERTICAL_RESIDENCIAL", base_efficiency
    )
    print(
        f"Case A (Residencial): {base_efficiency} -> {eff_res} (Esperado: {base_efficiency})"
    )
    if eff_res == base_efficiency:
        print("✅ OK (Sem penalidade)")
    else:
        print("❌ ERRO (Penalidade indevida)")

    # Case B: Mixed Use
    eff_mixed = RegulatoryEngine.apply_it11_efficiency_penalty("MISTO", base_efficiency)
    expected_mixed = base_efficiency * 0.85
    print(
        f"Case B (Misto): {base_efficiency} -> {eff_mixed:.4f} (Esperado: {expected_mixed:.4f})"
    )

    if abs(eff_mixed - expected_mixed) < 0.0001:
        print("✅ OK (Penalidade de 15% aplicada)")
    else:
        print("❌ ERRO (Cálculo incorreto)")


if __name__ == "__main__":
    verify_market_data()
    verify_it11_penalty()
