from core.price_scraper import PriceScraper

def test_price_scraper():
    print(">>> Testing PriceScraper heuristics...")
    
    test_cases = [
        ("Preco: R$ 5.500/m2 no coracao da Vila da Serra", 5500.0),
        ("Unidades a partir de R$ 750.000,00 reais", 750000.0),
        ("Valor estimado de 8.200 reais por m²", 8200.0),
        ("Sem preco informado", None),
        ("R$ 1.200.000 de VGV", 1200000.0)
    ]
    
    for text, expected in test_cases:
        result = PriceScraper.extract_price(text)
        print(f"Text: '{text}' | Expected: {expected} | Got: {result}")
        if expected is not None:
            assert result == expected
        else:
            assert result is None

    # Test Average
    snippets = [
        "R$ 5.000/m2",
        "R$ 6.000/m2",
        "Sem info",
        "Apartamento de 7.000 reais por metro"
    ]
    avg = PriceScraper.find_average_price(snippets)
    print(f"Average of snippets: {avg} (Expected ~6000)")
    assert 5900 < avg < 6100

    print("\n[SUCCESS] PRICESCRAPER VERIFIED.")

if __name__ == "__main__":
    test_price_scraper()
