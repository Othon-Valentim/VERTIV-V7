import re
from typing import Optional, List

class PriceScraper:
    """
    Utility to extract pricing information from unstructured text snippets.
    Focuses on BRL currency patterns (R$, reais, /m2).
    """
    
    # Matches patterns like R$ 5.000, R$ 5000, 5.000,00 reais
    CURRENCY_PATTERN = r"(?:R\$|reais)\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
    PER_SQM_PATTERN = r"(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*(?:reais)?\s*(?:\/|por)\s*(?:m2|m²|metro)"

    @classmethod
    def extract_price(cls, text: str) -> Optional[float]:
        """
        Extracts the first monetary value found in the text.
        """
        # Try per sqm first
        sqm_match = re.search(cls.PER_SQM_PATTERN, text, re.IGNORECASE)
        if sqm_match:
            return cls._parse_portuguese_number(sqm_match.group(1))

        # Try generic currency
        currency_match = re.search(cls.CURRENCY_PATTERN, text, re.IGNORECASE)
        if currency_match:
            return cls._parse_portuguese_number(currency_match.group(1))
            
        return None

    @classmethod
    def _parse_portuguese_number(cls, value_str: str) -> float:
        """
        Converts '5.000,00' or '5.000' to 5000.0.
        """
        # Remove dots (thousands separator)
        clean = value_str.replace(".", "")
        # Replace comma with dot (decimal separator)
        clean = clean.replace(",", ".")
        try:
            return float(clean)
        except ValueError:
            return 0.0

    @classmethod
    def find_average_price(cls, snippets: List[str]) -> float:
        """
        Finds average market price from a list of snippets.
        """
        prices = []
        for s in snippets:
            price = cls.extract_price(s)
            if price and price > 100: # Filter out noise
                prices.append(price)
        
        if not prices:
            return 0.0
            
        return sum(prices) / len(prices)
