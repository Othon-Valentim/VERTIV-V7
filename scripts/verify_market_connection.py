import sys
import os

# Ensure backend src is in path
sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))

from src.services.market_data import BCBConnector


def test_market_connection():
    print(">>> Testing BCB Connector Live Data...")
    connector = BCBConnector()

    # 1. Test Selic
    try:
        selic = connector.get_selic_rate()
        print(f"Live Selic Rate: {selic * 100:.2f}%")
        assert selic > 0, "Selic rate should be positive"
        # Optional: Assert it's not the fallback if we want to be strict
        # assert selic != 0.1125, "Likely hit fallback (11.25%)"
    except Exception as e:
        print(f"Selic Test Failed: {e}")
        raise

    # 2. Test IPCA
    try:
        ipca = connector.get_ipca_rate()
        print(f"Live IPCA Rate: {ipca * 100:.2f}%")
        assert ipca > 0, "IPCA rate should be positive"
    except Exception as e:
        print(f"IPCA Test Failed: {e}")
        raise

    print("\n[SUCCESS] MARKET CONNECTIVITY VERIFIED.")


if __name__ == "__main__":
    test_market_connection()
