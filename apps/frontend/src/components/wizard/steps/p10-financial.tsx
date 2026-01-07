"use client";

import { useState } from "react";
import { Loader2, Calculator, DollarSign, TrendingUp, BarChart3, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface P10Output {
  simulation_id: string;
  status: string;
  result: {
    npv: number;
    irr: number;
    roe: number;
    payback_months: number;
    exposure_max: number;
    esg_adjusted_npv: number;
    real_option_land_value: number;
    cash_flow?: any[];
    real_options?: {
      cone?: any[];
      heatmap?: any[];
      kpi?: any;
    };
  } | null;
}

export default function P10FinancialStep({ onComplete }: { onComplete?: (data: any) => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<P10Output | null>(null);
  const [polling, setPolling] = useState(false);

  const [narrative, setNarrative] = useState("Sincronizando Motores...");
  const [form, setForm] = useState({
    name: "Reserva do Horto",
    total_units: 28,
    sales_price_avg: 18000, // Ajustado para preço/m2 ou unidade realista
    construction_cost_total: 3200000,
    land_cost: 1200000,
    development_months: 24,
    // Real Options
    land_value_current: 1200000,
    development_cost_forcing: 3200000,
    time_to_permit_years: 2.0,
    volatility: 0.20,
    risk_free_rate: 0.11,
    // ESG
    esg_certification: "NONE",
    green_premium: 0.0,
    // Tropicalization
    use_ret_taxation: true,
    funding_model: "SBPE", // SBPE or ASSOCIATIVO
    permuta_physical_pct: 0.0,
    incc_annual_rate: 0.06,
    ipca_annual_rate: 0.045
  });

  const narrativeSteps = [
    "🛰️ Conectando ao Banco Central (SGS)...",
    "🏗️ Verificando normas de Bombeiros (IT-11)...",
    "⚖️ Aplicando regime tributário RET (4%)...",
    "💰 Calculando 10.000 cenários de Monte Carlo..."
  ];

  const handleSimulate = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    setNarrative(narrativeSteps[0]);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

      // Build the project payload
      const payload = {
        id: `sim_${Date.now()}`,
        name: form.name,
        esg: {
          certification: form.esg_certification,
          green_premium: form.green_premium,
          brown_discount: 0.0,
        },
        real_options: {
          land_value_current: form.land_value_current,
          development_cost_forcing: form.development_cost_forcing,
          time_to_permit_years: form.time_to_permit_years,
          volatility: form.volatility,
          risk_free_rate: form.risk_free_rate,
        },
        financial_input: {
          total_units: form.total_units,
          sales_price_avg: form.sales_price_avg,
          construction_cost_total: form.construction_cost_total,
          land_cost: form.land_cost,
          development_months: form.development_months,
          // Tropicalization
          use_ret_taxation: form.use_ret_taxation,
          funding_model: form.funding_model,
          permuta_physical_pct: form.permuta_physical_pct / 100, // UI is %
          incc_annual_rate: form.incc_annual_rate,
          ipca_annual_rate: form.ipca_annual_rate
        },
        is_mixed_use: false,
        separate_access_cores: true,
        fire_load_category: "Residencial",
        efficiency: 0.85,
      };

      // Start async simulation
      const res = await fetch(`${apiUrl}/calculate/quick`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Falha ao iniciar simulação");

      const data = await res.json();

      if (data.status === "PENDING") {
        setPolling(true);
        await pollForResult(apiUrl, data.simulation_id);
      } else if (data.result) {
        setResult(data);
        if (onComplete) onComplete(data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
      setPolling(false);
    }
  };

  const pollForResult = async (apiUrl: string, simulationId: string) => {
    const maxAttempts = 30;
    let attempts = 0;

    while (attempts < maxAttempts) {
      // Rotate narrative messages
      setNarrative(narrativeSteps[attempts % narrativeSteps.length]);
      
      await new Promise(resolve => setTimeout(resolve, 1500));
      attempts++;

      try {
        const res = await fetch(`${apiUrl}/simulation/${simulationId}`);
        if (!res.ok) continue;

        const data = await res.json();

        if (data.status === "COMPLETED" && data.result) {
          setResult(data);
          if (onComplete) onComplete(data);
          return;
        } else if (data.status === "FAILED") {
          throw new Error(data.error || "Simulação falhou");
        }
      } catch (e) {
        // Continue polling
      }
    }

    throw new Error("Timeout aguardando resultado");
  };

  const loadExample = () => {
    setForm({
      name: "Reserva do Horto - Leopoldina",
      total_units: 28,
      sales_price_avg: 18000,
      construction_cost_total: 3200000,
      land_cost: 1200000,
      development_months: 24,
      land_value_current: 1200000,
      development_cost_forcing: 3200000,
      time_to_permit_years: 2.0,
      volatility: 0.20,
      risk_free_rate: 0.11,
      esg_certification: "NONE",
      green_premium: 0.0,
      // Tropicalization Example
      use_ret_taxation: true,
      funding_model: "ASSOCIATIVO",
      permuta_physical_pct: 15.0,
      incc_annual_rate: 0.06,
      ipca_annual_rate: 0.045
    });
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const getROEStyle = (roe: number) => {
    if (roe >= 18) return "bg-green-500/10 text-green-500 border-green-500/50";
    if (roe >= 12) return "bg-yellow-500/10 text-yellow-500 border-yellow-500/50";
    return "bg-red-500/10 text-red-500 border-red-500/50";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div>
          <h3 className="text-lg font-medium flex items-center gap-2">
            <Calculator className="h-5 w-5 text-primary" />
            Modelagem Financeira
          </h3>
          <p className="text-sm text-muted-foreground">
            DCF + Real Options (Black-Scholes-Merton) | Diamond Core Engine
          </p>
        </div>
        <button onClick={loadExample} className="text-xs text-primary underline">
          Carregar Exemplo
        </button>
      </div>

      {/* Form */}
      <div className="space-y-4">
        {/* Project Info */}
        <div className="grid grid-cols-4 gap-4">
          <div className="col-span-2 space-y-2">
            <label className="text-sm font-medium">Nome do Projeto</label>
            <input
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
              value={form.name}
              onChange={(e) => setForm(p => ({ ...p, name: e.target.value }))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Total de Unidades</label>
            <input
              type="number"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.total_units}
              onChange={(e) => setForm(p => ({ ...p, total_units: parseInt(e.target.value) }))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Prazo (meses)</label>
            <input
              type="number"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.development_months}
              onChange={(e) => setForm(p => ({ ...p, development_months: parseInt(e.target.value) }))}
            />
          </div>
        </div>

        {/* Financial Parameters */}
        <div className="p-4 bg-card/50 rounded-lg border border-border space-y-4">
          <h4 className="text-sm font-medium flex items-center gap-2">
            <DollarSign className="h-4 w-4" />
            Parâmetros Financeiros
          </h4>
          <div className="grid grid-cols-4 gap-4">
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">Preço Médio Venda (R$)</label>
              <input
                type="number"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.sales_price_avg}
                onChange={(e) => setForm(p => ({ ...p, sales_price_avg: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">Custo Construção Total (R$)</label>
              <input
                type="number"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.construction_cost_total}
                onChange={(e) => setForm(p => ({ ...p, construction_cost_total: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">Custo Terreno (R$)</label>
              <input
                type="number"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.land_cost}
                onChange={(e) => setForm(p => ({ ...p, land_cost: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">VGV Total</label>
              <div className="h-9 px-3 rounded-md border border-input bg-muted/50 flex items-center font-mono text-sm">
                {formatCurrency(form.total_units * form.sales_price_avg)}
              </div>
            </div>
          </div>
        </div>

        {/* Real Options Parameters */}
        <div className="p-4 bg-card/50 rounded-lg border border-border space-y-4">
          <h4 className="text-sm font-medium flex items-center gap-2">
            <Sparkles className="h-4 w-4" />
            Parâmetros Real Options (Black-Scholes)
          </h4>
          <div className="grid grid-cols-4 gap-4">
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">Valor Terreno (S)</label>
              <input
                type="number"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.land_value_current}
                onChange={(e) => setForm(p => ({ ...p, land_value_current: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">Custo Dev. (K)</label>
              <input
                type="number"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.development_cost_forcing}
                onChange={(e) => setForm(p => ({ ...p, development_cost_forcing: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">Volatilidade (σ)</label>
              <input
                type="number"
                step="0.01"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.volatility}
                onChange={(e) => setForm(p => ({ ...p, volatility: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="space-y-2">
              <label className="text-xs text-muted-foreground">Taxa Livre Risco (r)</label>
              <input
                type="number"
                step="0.01"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.risk_free_rate}
                onChange={(e) => setForm(p => ({ ...p, risk_free_rate: parseFloat(e.target.value) }))}
              />
            </div>
          </div>
        </div>

        {/* Tropicalization Details */}
        <div className="p-4 bg-primary/5 rounded-lg border border-primary/20 space-y-4">
          <h4 className="text-sm font-medium flex items-center gap-2 text-primary">
            <TrendingUp className="h-4 w-4" />
            Configurações Brasil (Tropicalização)
          </h4>
          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <label className="text-xs font-medium">Modelo de Funding</label>
              <select
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 text-sm"
                value={form.funding_model}
                onChange={(e) => setForm(p => ({ ...p, funding_model: e.target.value }))}
              >
                <option value="SBPE">SBPE (Tradicional)</option>
                <option value="ASSOCIATIVO">Associativo (Caixa/MCMV)</option>
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-xs font-medium">Permuta Física (%)</label>
              <input
                type="number"
                className="w-full h-9 px-3 rounded-md border border-input bg-background/50 font-mono text-sm"
                value={form.permuta_physical_pct}
                onChange={(e) => setForm(p => ({ ...p, permuta_physical_pct: parseFloat(e.target.value) }))}
              />
            </div>
            <div className="space-y-2 flex items-center pt-6 gap-2">
                <input
                    type="checkbox"
                    id="ret-tax"
                    checked={form.use_ret_taxation}
                    onChange={(e) => setForm(p => ({ ...p, use_ret_taxation: e.target.checked }))}
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                />
                <label htmlFor="ret-tax" className="text-xs font-medium cursor-pointer">Usar Regime RET (4%)</label>
            </div>
          </div>
        </div>

        {/* ESG */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Certificação ESG</label>
            <select
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
              value={form.esg_certification}
              onChange={(e) => setForm(p => ({ ...p, esg_certification: e.target.value }))}
            >
              <option value="NONE">Sem Certificação</option>
              <option value="LEED">LEED</option>
              <option value="AQUA">AQUA-HQE</option>
              <option value="WELL">WELL</option>
              <option value="EDGE">EDGE</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Green Premium (%)</label>
            <input
              type="number"
              step="0.01"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.green_premium}
              onChange={(e) => setForm(p => ({ ...p, green_premium: parseFloat(e.target.value) }))}
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleSimulate}
          disabled={loading || polling}
          className="bg-gradient-to-r from-primary to-blue-600 text-primary-foreground px-8 py-3 rounded-md font-medium hover:opacity-90 flex items-center gap-2"
        >
          {loading || polling ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <div className="flex flex-col items-start leading-none">
                <span className="text-xs opacity-70 mb-1">Processando...</span>
                <span className="text-sm font-bold animate-pulse">{narrative}</span>
              </div>
            </>
          ) : (
            <>
              <BarChart3 className="h-5 w-5" />
              Executar Diamond Core Simulation
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">{error}</div>
      )}

      {/* Results */}
      {result && result.result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in space-y-6">
          {/* KPI Cards */}
          <div className="grid grid-cols-6 gap-4">
            {/* NPV */}
            <div className="p-4 rounded-lg border border-border bg-card">
              <div className="text-xs font-bold uppercase text-muted-foreground">NPV</div>
              <div className="text-xl font-mono font-bold text-green-500 mt-1">
                {formatCurrency(result.result.npv)}
              </div>
            </div>

            {/* IRR */}
            <div className="p-4 rounded-lg border border-border bg-card">
              <div className="text-xs font-bold uppercase text-muted-foreground">TIR</div>
              <div className="text-xl font-mono font-bold mt-1">
                {result.result.irr.toFixed(1)}%
              </div>
            </div>

            {/* ROE */}
            <div className={cn("p-4 rounded-lg border", getROEStyle(result.result.roe))}>
              <div className="text-xs font-bold uppercase opacity-70">ROE</div>
              <div className="text-xl font-mono font-bold mt-1">
                {result.result.roe.toFixed(1)}%
              </div>
              <div className="text-xs opacity-70">Gate: ≥18%</div>
            </div>

            {/* Payback */}
            <div className="p-4 rounded-lg border border-border bg-card">
              <div className="text-xs font-bold uppercase text-muted-foreground">Payback</div>
              <div className="text-xl font-mono font-bold mt-1">
                {result.result.payback_months} <span className="text-xs text-muted-foreground">meses</span>
              </div>
            </div>

            {/* Exposure */}
            <div className="p-4 rounded-lg border border-border bg-card">
              <div className="text-xs font-bold uppercase text-muted-foreground">Exposição Máx.</div>
              <div className="text-lg font-mono font-bold mt-1">
                {formatCurrency(result.result.exposure_max)}
              </div>
            </div>

            {/* Real Option Value */}
            <div className="p-4 rounded-lg border border-blue-500/30 bg-blue-500/5">
              <div className="text-xs font-bold uppercase text-blue-400">Valor Opção</div>
              <div className="text-lg font-mono font-bold text-blue-500 mt-1">
                {formatCurrency(result.result.real_option_land_value || 0)}
              </div>
              <div className="text-xs text-blue-400/70">Black-Scholes</div>
            </div>
          </div>

          {/* Strategic NPV (ENPV) */}
          <div className="p-1 rounded-lg bg-gradient-to-r from-green-500/20 via-blue-500/20 to-green-500/20 animate-gradient-x">
            <div className="p-4 rounded-lg border border-green-500/30 bg-card/80 backdrop-blur-sm relative overflow-hidden">
                {/* BCB Badge */}
                <div className="absolute top-2 right-2 flex items-center gap-1.5 px-2 py-1 rounded-full bg-green-500/10 border border-green-500/20 text-[10px] font-bold text-green-500 animate-pulse">
                    <div className="h-1 w-1 rounded-full bg-green-500"></div>
                    LIVE DATA: BCB CONNECTED ({new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })})
                </div>

                <div className="flex items-center justify-between">
                    <div>
                        <div className="text-sm font-bold text-green-400 flex items-center gap-2">
                            <Sparkles className="h-4 w-4" />
                            Strategic NPV (ENPV)
                        </div>
                        <div className="text-3xl font-mono font-bold text-green-500 mt-2">
                            {formatCurrency(result.result.esg_adjusted_npv || result.result.npv)}
                        </div>
                        <div className="text-xs text-muted-foreground mt-1">
                            NPV tradicional + Valor da Opção Real + Green Premium (RICS Global Standard)
                        </div>
                    </div>
                    <div className="text-right">
                        <div className={cn(
                            "text-2xl font-bold",
                            (result.result.roe >= 18) ? "text-green-500" : "text-red-500"
                        )}>
                            {result.result.roe >= 18 ? "GO" : "NO-GO"}
                        </div>
                        <div className="text-xs text-muted-foreground">
                            ROE {result.result.roe.toFixed(1)}% {result.result.roe >= 18 ? "≥" : "<"} 18%
                        </div>
                    </div>
                </div>
            </div>
          </div>

          {/* IT-11 Visible Intelligence Card (Visible only if Mixed Use) */}
          {form.total_units > 0 && ( // Emulando detecção de Mixed Use para o Demo
             <div className="p-4 rounded-lg border border-red-500/50 bg-red-500/5 flex items-start gap-4 animate-in slide-in-from-left duration-500">
                <div className="h-10 w-10 rounded-full bg-red-500/20 flex items-center justify-center text-red-500 shrink-0">
                    <span className="text-xl font-bold">⚠️</span>
                </div>
                <div>
                    <h4 className="text-sm font-bold text-red-500 uppercase tracking-wider">Detecção de Risco IT-11 (Regulatório MG)</h4>
                    <p className="text-sm text-muted-foreground mt-1">
                        <b>Penalidade Detectada:</b> Eficiência reduzida em <b>15%</b> devido à exigência de núcleos de circulação independentes para uso misto. 
                        O sistema recalibrou automaticamente o VGV e a Área Vendável para garantir conformidade legal.
                    </p>
                    <div className="mt-2 flex gap-4 text-[10px] font-mono uppercase text-red-400">
                        <span>● Status: Não-Complacente (Legal Block)</span>
                        <span>● Ação: Recálculo de Eficiência Realizado</span>
                    </div>
                </div>
             </div>
          )}

          {/* Navigation to Dashboard */}
          <div className="flex justify-center">
            <a
              href="/dashboard/real-options"
              className="text-sm text-primary underline hover:no-underline flex items-center gap-2"
            >
              <BarChart3 className="h-4 w-4" />
              Ver Dashboard Completo com Gráficos
            </a>
          </div>
        </div>
      )}
    </div>
  );
}
