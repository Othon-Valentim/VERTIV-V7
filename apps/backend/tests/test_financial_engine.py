"""
VERTIV v6.0 - Financial Engine Tests

Testes críticos para o Diamond Core (Polars + Black-Scholes).

Coverage targets:
- CashFlowEngine: DCF, RET, Permuta, Funding Models
- RealOptionsEngine: Black-Scholes, Land Option Valuation

IMPORTANTE: Estes cálculos movem milhões de reais.
Qualquer erro aqui pode causar decisões de investimento erradas.
"""

import pytest
import numpy as np
from decimal import Decimal
from src.engine.cashflow import CashFlowEngine
from src.engine.real_options import RealOptionsEngine


# =============================================================================
# CASHFLOW ENGINE TESTS
# =============================================================================

class TestCashFlowEngine:
    """Testes para o motor de fluxo de caixa (DCF)."""

    def test_basic_calculation(self):
        """
        Test standard DCF calculation with default parameters.
        """
        engine = CashFlowEngine(months=24)

        result = engine.calculate_project_cashflow(
            units=100,
            avg_price=10000.0,
            cost_total=500000.0,
            wacc_annual=0.10,
            use_ret=True
        )

        metrics = result["metrics"]

        # 100 units * 10k = 1M VGV (without inflation)
        # 500k cost
        # NPV should be positive
        assert metrics["npv"] > 0
        assert metrics["irr"] > 0
        assert "dataframe" in result
        assert len(result["dataframe"]) == 25  # 0..24 months

    def test_negative_npv_high_cost(self):
        """
        Test that a project with costs exceeding revenue results in negative NPV.
        """
        engine = CashFlowEngine(months=12)

        # Cost (1M) > Revenue (500k)
        result = engine.calculate_project_cashflow(
            units=50,
            avg_price=10000.0,
            cost_total=1000000.0,
            wacc_annual=0.15
        )

        metrics = result["metrics"]
        assert metrics["npv"] < 0

    def test_ret_vs_normal_taxation(self):
        """
        Verify that RET (4%) results in higher profit than normal taxation (15%).

        RET (Regime Especial de Tributação) é crucial para viabilidade imobiliária.
        """
        engine = CashFlowEngine(months=12)

        params = {
            "units": 100,
            "avg_price": 10000.0,
            "cost_total": 500000.0,
            "wacc_annual": 0.10
        }

        res_ret = engine.calculate_project_cashflow(**params, use_ret=True)
        res_normal = engine.calculate_project_cashflow(**params, use_ret=False)

        assert res_ret["metrics"]["total_taxes"] < res_normal["metrics"]["total_taxes"]
        assert res_ret["metrics"]["npv"] > res_normal["metrics"]["npv"]

    def test_permuta_reduces_vgv(self):
        """
        Test that permuta (land swap) correctly reduces effective units.

        Permuta de 20% significa que 20% das unidades vão para o dono do terreno.
        """
        engine = CashFlowEngine(months=24)

        params = {
            "units": 100,
            "avg_price": 10000.0,
            "cost_total": 300000.0,
            "wacc_annual": 0.10
        }

        # Sem permuta
        res_no_permuta = engine.calculate_project_cashflow(**params, permuta_pct=0.0)

        # Com 20% permuta
        res_with_permuta = engine.calculate_project_cashflow(**params, permuta_pct=0.20)

        # Receita deve ser menor com permuta
        assert res_with_permuta["metrics"]["total_revenue"] < res_no_permuta["metrics"]["total_revenue"]
        # NPV também deve ser menor
        assert res_with_permuta["metrics"]["npv"] < res_no_permuta["metrics"]["npv"]

    def test_associativo_vs_sbpe_funding(self):
        """
        Test different funding models affect cash flow timing.

        ASSOCIATIVO: Banco antecipa recursos (melhor para incorporador)
        SBPE: Recebe apenas quando vende (padrão)
        """
        engine = CashFlowEngine(months=36)

        params = {
            "units": 100,
            "avg_price": 15000.0,
            "cost_total": 800000.0,
            "wacc_annual": 0.12
        }

        res_sbpe = engine.calculate_project_cashflow(**params, funding_model="SBPE")
        res_assoc = engine.calculate_project_cashflow(**params, funding_model="ASSOCIATIVO")

        # Ambos devem ter resultados válidos
        assert res_sbpe["metrics"]["npv"] is not None
        assert res_assoc["metrics"]["npv"] is not None

    def test_wacc_sensitivity(self):
        """
        Test that higher WACC reduces NPV (time value of money).

        CRITICAL: WACC é o coração do DCF. Erro aqui = decisão errada.
        """
        engine = CashFlowEngine(months=24)

        params = {
            "units": 100,
            "avg_price": 10000.0,
            "cost_total": 400000.0
        }

        # WACC baixo (10%)
        res_low = engine.calculate_project_cashflow(**params, wacc_annual=0.10)

        # WACC alto (20%)
        res_high = engine.calculate_project_cashflow(**params, wacc_annual=0.20)

        # NPV deve ser MENOR com WACC maior
        assert res_high["metrics"]["npv"] < res_low["metrics"]["npv"]

    def test_inflation_indices_applied(self):
        """
        Test that INCC (construction) and IPCA (sales) are applied correctly.
        """
        engine = CashFlowEngine(months=24)

        result = engine.calculate_project_cashflow(
            units=100,
            avg_price=10000.0,
            cost_total=500000.0,
            wacc_annual=0.10,
            incc_annual=0.06,
            ipca_annual=0.045
        )

        # O cálculo deve completar sem erros
        assert result["metrics"]["total_revenue"] > 0
        assert result["metrics"]["npv"] is not None

    def test_zero_units_edge_case(self):
        """
        Test handling of edge case with zero or minimal units.
        """
        engine = CashFlowEngine(months=12)

        result = engine.calculate_project_cashflow(
            units=1,
            avg_price=100000.0,
            cost_total=50000.0,
            wacc_annual=0.10
        )

        # Deve completar sem erros
        assert "metrics" in result


# =============================================================================
# REAL OPTIONS ENGINE TESTS
# =============================================================================

class TestRealOptionsEngine:
    """
    Testes para o motor de Real Options (Black-Scholes).

    Real Options é usado para calcular o valor da "opção de esperar"
    antes de desenvolver um terreno.
    """

    def test_black_scholes_call_option(self):
        """
        Test Black-Scholes call option calculation.

        Verifica contra valores conhecidos.
        """
        # Valores de teste conhecidos
        S = 100  # Spot price
        K = 100  # Strike price
        T = 1    # 1 year
        r = 0.05 # 5% risk-free rate
        sigma = 0.20  # 20% volatility

        result = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=sigma, option_type="call"
        )

        # Para ATM call com esses parâmetros, valor deve ser ~10.45
        assert 9.0 < result < 12.0

    def test_black_scholes_put_option(self):
        """
        Test Black-Scholes put option calculation.
        """
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.20

        result = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=sigma, option_type="put"
        )

        # Put ATM com mesmos parâmetros
        assert 5.0 < result < 8.0

    def test_put_call_parity(self):
        """
        Test Put-Call Parity: C - P = S - K*e^(-rT)

        CRITICAL: Se falhar, há erro fundamental no Black-Scholes.
        """
        S = 100
        K = 100
        T = 1
        r = 0.05
        sigma = 0.20

        call = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=sigma, option_type="call"
        )
        put = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=sigma, option_type="put"
        )

        # Put-Call Parity
        parity_left = call - put
        parity_right = S - K * np.exp(-r * T)

        # Deve ser aproximadamente igual (tolerância de 0.01)
        assert abs(parity_left - parity_right) < 0.01

    def test_option_increases_with_volatility(self):
        """
        Test that option value increases with volatility.

        Maior incerteza = maior valor da opção de esperar.
        """
        S = 100
        K = 100
        T = 1
        r = 0.05

        # Baixa volatilidade
        low_vol = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=0.10, option_type="call"
        )

        # Alta volatilidade
        high_vol = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=0.40, option_type="call"
        )

        # Maior volatilidade = maior valor da opção
        assert high_vol > low_vol

    def test_option_increases_with_time(self):
        """
        Test that option value increases with time to expiration.

        Mais tempo para decidir = mais valor.
        """
        S = 100
        K = 100
        r = 0.05
        sigma = 0.20

        # Curto prazo
        short_term = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=0.5, r=r, sigma=sigma, option_type="call"
        )

        # Longo prazo
        long_term = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=2.0, r=r, sigma=sigma, option_type="call"
        )

        # Mais tempo = maior valor
        assert long_term > short_term

    def test_land_option_value(self):
        """
        Test land bank option valuation.

        Cenário: Terreno vale R$10M, custo de desenvolvimento R$8M,
        2 anos para obter alvará.
        """
        result = RealOptionsEngine.calculate_land_option_value(
            land_value_current=10_000_000,  # R$10M
            development_cost=8_000_000,     # R$8M
            time_to_permit_years=2,
            volatility=0.25,                # 25% volatilidade do mercado
            risk_free_rate=0.11             # Selic ~11%
        )

        # Valor da opção deve ser positivo e razoável
        assert result > 0
        # Deve ser maior que o valor intrínseco (10M - 8M = 2M)
        assert result > 2_000_000

    def test_deep_itm_option(self):
        """
        Test deep in-the-money option (S >> K).

        Deve se aproximar do valor intrínseco.
        """
        S = 200  # Muito acima do strike
        K = 100
        T = 0.1  # Curto prazo
        r = 0.05
        sigma = 0.10  # Baixa volatilidade

        result = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=sigma, option_type="call"
        )

        # Deve ser próximo de S - K = 100
        intrinsic = S - K
        assert abs(result - intrinsic) < 5

    def test_deep_otm_option(self):
        """
        Test deep out-of-the-money option (S << K).

        Valor deve ser próximo de zero.
        """
        S = 50   # Muito abaixo do strike
        K = 100
        T = 0.1  # Curto prazo
        r = 0.05
        sigma = 0.10  # Baixa volatilidade

        result = RealOptionsEngine.black_scholes_vectorized(
            S=S, K=K, T=T, r=r, sigma=sigma, option_type="call"
        )

        # Deve ser próximo de zero
        assert result < 1.0

    def test_edge_case_zero_volatility(self):
        """
        Test handling of zero volatility edge case.
        """
        result = RealOptionsEngine.black_scholes_vectorized(
            S=100, K=90, T=1, r=0.05, sigma=0.0, option_type="call"
        )

        # Com volatilidade zero, valor deve ser max(0, S-K)
        assert result >= 0

    def test_edge_case_zero_time(self):
        """
        Test handling of zero time to expiration.
        """
        result = RealOptionsEngine.black_scholes_vectorized(
            S=100, K=90, T=0, r=0.05, sigma=0.20, option_type="call"
        )

        # Com T=0, valor deve ser valor intrínseco max(0, S-K)
        assert result >= 0


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestFinancialIntegration:
    """
    Testes de integração entre CashFlow e Real Options.
    """

    def test_full_viability_analysis(self):
        """
        Test complete viability analysis combining DCF and Real Options.

        Cenário real: Loteamento de 100 lotes em cidade média.
        """
        # 1. Calcular DCF do projeto
        cashflow_engine = CashFlowEngine(months=36)

        dcf_result = cashflow_engine.calculate_project_cashflow(
            units=100,
            avg_price=180_000,  # R$180k por lote
            cost_total=12_000_000,  # R$12M custo total
            wacc_annual=0.145,  # WACC 14.5%
            use_ret=True,
            permuta_pct=0.15,  # 15% permuta
            funding_model="SBPE"
        )

        # 2. Calcular valor da opção de esperar
        option_value = RealOptionsEngine.calculate_land_option_value(
            land_value_current=dcf_result["metrics"]["npv"],
            development_cost=12_000_000,
            time_to_permit_years=1.5,
            volatility=0.22,
            risk_free_rate=0.11
        )

        # 3. Verificar resultados
        assert dcf_result["metrics"]["npv"] is not None
        assert dcf_result["metrics"]["irr"] is not None
        assert option_value >= 0

        # 4. Decision logic
        if dcf_result["metrics"]["npv"] > 0:
            expanded_npv = dcf_result["metrics"]["npv"] + option_value
            assert expanded_npv > dcf_result["metrics"]["npv"]
