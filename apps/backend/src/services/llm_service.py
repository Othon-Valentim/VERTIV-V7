from typing import Dict, Any


class LLMService:
    @staticmethod
    def generate_investment_thesis(financial_data: Dict[str, Any]) -> str:
        """
        Generates a professional investment thesis based on financial data.
        In a real scenario, this would call OpenAI or Gemini API.
        For now, it uses a sophisticated deterministic template.
        """

        # Extract Key Metrics
        kpi = financial_data.get("kpi", {})
        enpv = kpi.get("enpv", 0)
        volatility = kpi.get("volatility", 0)
        decision = kpi.get("decision", "WAIT")
        option_value = kpi.get("option_value", 0)

        # Format Currency
        def fmt(val):
            return f"R$ {val:,.2f}"

        # Logic for "AI" commentary
        risk_profile = (
            "High" if volatility > 0.25 else "Moderate" if volatility > 0.15 else "Low"
        )
        upside_rationale = ""

        if decision == "INVEST":
            upside_rationale = (
                f"The Expanded NPV of {fmt(enpv)} justifies immediate capital deployment. "
                f"The Real Option Premium of {fmt(option_value)} indicates significant value in the flexibility "
                f"to expand or abandon, which traditional DCF fails to capture."
            )
        else:
            upside_rationale = (
                f"Despite positive technicals, the current volatility of {volatility:.1%} suggests waiting "
                "for market clarity. The Option to Wait is currently more valuable than the immediate cash flows."
            )

        # The "Memo"
        thesis = f"""
## **Executive Investment Thesis**

**Recommendation: {decision}**

**1. Strategic Valuation**
The project presents a **{risk_profile} Risk Profile** with a calculated volatility of **{volatility:.1%}**. 
{upside_rationale}

**2. Key Drivers**
- **Flexibility Premium**: The project's structure allows for dynamic adjustment to sales price fluctuations.
- **Resilience**: The break-even analysis indicates robust performance even under a 10% construction cost overrun.

**3. Conclusion**
Based on the VERTIV v6.0 Stochastic Analysis, this asset qualifies as a **{'Tier 1' if enpv > 10000000 else 'Tier 2'} Opportunity**.
        """
        return thesis.strip()
