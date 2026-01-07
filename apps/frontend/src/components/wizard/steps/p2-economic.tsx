"use client";

import { useState } from "react";
import { Loader2, TrendingUp, TrendingDown, Activity, DollarSign, Users, Building2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface P2Output {
  municipality: string;
  p2i_lead_score: number;
  max_score: number;
  decision: string;
  recommendation: string;
  is_favorable: boolean;
  breakdown: {
    leading_indicators: {
      score: number;
      max: number;
      components: {
        employment_growth: number;
        credit_expansion: number;
        consumer_confidence: number;
      };
    };
    lagging_indicators: {
      score: number;
      max: number;
      components: {
        ipca_12m: number;
        pib_growth: number;
        selic_rate: number;
      };
    };
    contextual_factors: {
      score: number;
      max: number;
    };
  };
  live_indicators: {
    selic_rate: number;
    ipca_12m: number;
    pib_growth: number;
    unemployment_rate: number;
    consumer_confidence: number;
    credit_expansion: number;
    formal_employment_growth: number;
  };
}

interface P2EconomicStepProps {
  onComplete?: (data: P2Output) => void;
  initialMunicipality?: string;
}

export default function P2EconomicStep({ onComplete, initialMunicipality = "" }: P2EconomicStepProps) {
  const [municipality, setMunicipality] = useState(initialMunicipality);
  const [population, setPopulation] = useState(50000);
  const [isMetropolitan, setIsMetropolitan] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<P2Output | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");

    try {
      if (!municipality) {
        throw new Error("Informe o município");
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/wizard/p2/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          municipality,
          municipality_population: population,
          is_metropolitan: isMetropolitan
        }),
      });

      if (!res.ok) throw new Error("Falha na análise. Verifique a conexão.");

      const data = await res.json();
      setResult(data);
      if (onComplete) onComplete(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getDecisionStyle = (decision: string) => {
    switch (decision) {
      case "GO": return "bg-green-500/10 text-green-500 border-green-500/50";
      case "HOLD": return "bg-yellow-500/10 text-yellow-500 border-yellow-500/50";
      case "CAUTION": return "bg-orange-500/10 text-orange-500 border-orange-500/50";
      default: return "bg-red-500/10 text-red-500 border-red-500/50";
    }
  };

  const getScoreColor = (score: number, max: number) => {
    const pct = score / max;
    if (pct >= 0.7) return "text-green-500";
    if (pct >= 0.5) return "text-yellow-500";
    return "text-red-500";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-border pb-4">
        <h3 className="text-lg font-medium flex items-center gap-2">
          <Activity className="h-5 w-5 text-primary" />
          Dinâmica Econômica
        </h3>
        <p className="text-sm text-muted-foreground mt-1">
          Análise de indicadores macroeconômicos e score P2i-Lead.
        </p>
      </div>

      {/* Input Form */}
      <div className="grid grid-cols-3 gap-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Município</label>
          <input
            type="text"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 focus:outline-none focus:ring-1 focus:ring-primary"
            placeholder="Ex: Leopoldina-MG"
            value={municipality}
            onChange={(e) => setMunicipality(e.target.value)}
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">População</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono focus:outline-none focus:ring-1 focus:ring-primary"
            value={population}
            onChange={(e) => setPopulation(parseInt(e.target.value) || 0)}
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Região Metropolitana?</label>
          <div className="flex items-center gap-4 h-10">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={isMetropolitan}
                onChange={(e) => setIsMetropolitan(e.target.checked)}
                className="rounded border-input"
              />
              <span className="text-sm">Sim</span>
            </label>
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 transition-colors flex items-center gap-2"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <TrendingUp className="h-4 w-4" />}
          Analisar Indicadores
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-6">
          {/* Score Cards */}
          <div className="grid grid-cols-4 gap-4">
            {/* P2i-Lead Score */}
            <div className={cn("p-4 rounded-lg border flex flex-col items-center justify-center text-center", getDecisionStyle(result.decision))}>
              <span className="text-xs font-bold uppercase tracking-widest mb-1 opacity-70">P2i-Lead</span>
              <span className="text-3xl font-bold">{result.p2i_lead_score.toFixed(1)}</span>
              <span className="text-xs opacity-70">/ {result.max_score}</span>
            </div>

            {/* Leading Score */}
            <div className="p-4 rounded-lg border border-border bg-card">
              <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground">Leading</span>
              <div className={cn("text-2xl font-mono font-bold mt-1", getScoreColor(result.breakdown.leading_indicators.score, result.breakdown.leading_indicators.max))}>
                {result.breakdown.leading_indicators.score.toFixed(1)}
                <span className="text-xs text-muted-foreground">/{result.breakdown.leading_indicators.max}</span>
              </div>
            </div>

            {/* Lagging Score */}
            <div className="p-4 rounded-lg border border-border bg-card">
              <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground">Lagging</span>
              <div className={cn("text-2xl font-mono font-bold mt-1", getScoreColor(result.breakdown.lagging_indicators.score, result.breakdown.lagging_indicators.max))}>
                {result.breakdown.lagging_indicators.score.toFixed(1)}
                <span className="text-xs text-muted-foreground">/{result.breakdown.lagging_indicators.max}</span>
              </div>
            </div>

            {/* Decision */}
            <div className={cn("p-4 rounded-lg border flex flex-col items-center justify-center", getDecisionStyle(result.decision))}>
              <span className="text-xs font-bold uppercase tracking-widest mb-1 opacity-70">Decisão</span>
              <span className="text-xl font-bold">{result.decision}</span>
            </div>
          </div>

          {/* Live Indicators */}
          <div className="bg-card/50 rounded-lg border border-border p-4">
            <h4 className="text-sm font-medium mb-4 flex items-center gap-2">
              <Activity className="h-4 w-4" />
              Indicadores Live (BCB + IBGE)
            </h4>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center p-3 bg-background/50 rounded">
                <div className="text-xs text-muted-foreground">SELIC</div>
                <div className="text-lg font-mono font-bold">{result.live_indicators.selic_rate.toFixed(2)}%</div>
              </div>
              <div className="text-center p-3 bg-background/50 rounded">
                <div className="text-xs text-muted-foreground">IPCA 12m</div>
                <div className="text-lg font-mono font-bold">{result.live_indicators.ipca_12m.toFixed(2)}%</div>
              </div>
              <div className="text-center p-3 bg-background/50 rounded">
                <div className="text-xs text-muted-foreground">PIB Growth</div>
                <div className="text-lg font-mono font-bold">{result.live_indicators.pib_growth.toFixed(1)}%</div>
              </div>
              <div className="text-center p-3 bg-background/50 rounded">
                <div className="text-xs text-muted-foreground">Desemprego</div>
                <div className="text-lg font-mono font-bold">{result.live_indicators.unemployment_rate.toFixed(1)}%</div>
              </div>
            </div>
          </div>

          {/* Recommendation */}
          <div className="bg-blue-500/5 border border-blue-500/20 rounded-lg p-4">
            <div className="text-sm font-medium text-blue-400 mb-1">Recomendação</div>
            <div className="text-sm">{result.recommendation}</div>
          </div>
        </div>
      )}
    </div>
  );
}
