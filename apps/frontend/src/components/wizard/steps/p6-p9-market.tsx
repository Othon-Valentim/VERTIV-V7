"use client";

import { useState } from "react";
import { Loader2, Users, Building2, TrendingUp, Target, CheckCircle } from "lucide-react";
import { cn } from "@/lib/utils";

// ==================== P6: DEMAND ====================
interface P6Output {
  funnel_stages: Record<string, { count: number; description: string; rate?: number }>;
  summary: {
    qualified_demand_units: number;
    target_segment: string;
    max_affordable_price: number;
  };
  funnel_efficiency: number;
}

export function P6DemandStep({ onComplete }: { onComplete?: (data: any) => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<P6Output | null>(null);

  const [form, setForm] = useState({
    municipality: "",
    influence_area_population: 50000,
    average_household_income: 5000,
    target_segment: "MEDIO",
    unit_price_min: 150000,
    unit_price_max: 250000,
    unit_type: "LOTE",
  });

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/wizard/p6/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Falha na análise");
      const data = await res.json();
      setResult(data);
      if (onComplete) onComplete(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-border pb-4">
        <h3 className="text-lg font-medium flex items-center gap-2">
          <Users className="h-5 w-5 text-primary" />
          Demanda Qualificada
        </h3>
        <p className="text-sm text-muted-foreground">Funil de 5 estágios para demanda efetiva.</p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Município</label>
          <input
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
            value={form.municipality}
            onChange={(e) => setForm(p => ({ ...p, municipality: e.target.value }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">População Área de Influência</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.influence_area_population}
            onChange={(e) => setForm(p => ({ ...p, influence_area_population: parseInt(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Renda Média Domiciliar (R$)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.average_household_income}
            onChange={(e) => setForm(p => ({ ...p, average_household_income: parseFloat(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Segmento Alvo</label>
          <select
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
            value={form.target_segment}
            onChange={(e) => setForm(p => ({ ...p, target_segment: e.target.value }))}
          >
            <option value="FAIXA_1">Faixa 1 (até R$ 2.640)</option>
            <option value="FAIXA_2">Faixa 2 (R$ 2.640 - 4.400)</option>
            <option value="FAIXA_3">Faixa 3 (R$ 4.400 - 8.000)</option>
            <option value="MEDIO">Médio (R$ 8.000 - 20.000)</option>
            <option value="ALTO">Alto (acima de R$ 20.000)</option>
          </select>
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Preço Mínimo Unidade (R$)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.unit_price_min}
            onChange={(e) => setForm(p => ({ ...p, unit_price_min: parseFloat(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Preço Máximo Unidade (R$)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.unit_price_max}
            onChange={(e) => setForm(p => ({ ...p, unit_price_max: parseFloat(e.target.value) }))}
          />
        </div>
      </div>

      <div className="flex justify-end">
        <button onClick={handleAnalyze} disabled={loading} className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 flex items-center gap-2">
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Users className="h-4 w-4" />}
          Calcular Demanda
        </button>
      </div>

      {error && <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">{error}</div>}

      {result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 rounded-lg border border-green-500/30 bg-green-500/5 text-center">
              <div className="text-xs font-bold uppercase text-green-400">Demanda Efetiva</div>
              <div className="text-3xl font-bold text-green-500">{result.summary.qualified_demand_units}</div>
              <div className="text-xs text-muted-foreground">unidades</div>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Preço Máx. Acessível</div>
              <div className="text-2xl font-mono font-bold">R$ {(result.summary.max_affordable_price / 1000).toFixed(0)}k</div>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Eficiência Funil</div>
              <div className="text-2xl font-mono font-bold">{result.funnel_efficiency.toFixed(2)}%</div>
            </div>
          </div>

          {/* Funnel visualization */}
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Funil de Demanda</h4>
            {Object.entries(result.funnel_stages).map(([key, stage], idx) => {
              const maxCount = result.funnel_stages.stage_1_total_families?.count || 1;
              const width = (stage.count / maxCount) * 100;
              return (
                <div key={key} className="flex items-center gap-3">
                  <div className="w-4 text-xs text-muted-foreground">{idx + 1}</div>
                  <div className="flex-1">
                    <div className="h-8 bg-border rounded overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-primary to-primary/60 flex items-center px-3"
                        style={{ width: `${Math.max(width, 10)}%` }}
                      >
                        <span className="text-xs font-mono text-primary-foreground">{stage.count.toLocaleString()}</span>
                      </div>
                    </div>
                    <div className="text-xs text-muted-foreground mt-1">{stage.description}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

// ==================== P7: SUPPLY ====================
export function P7SupplyStep({ onComplete }: { onComplete?: (data: any) => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);

  const [form, setForm] = useState({
    municipality: "",
    influence_area_km: 5.0,
    competitors: [] as any[],
    market_average_price_sqm: 300,
  });

  const [newCompetitor, setNewCompetitor] = useState({
    name: "",
    developer: "",
    total_units: 50,
    units_sold: 20,
    units_available: 30,
    price_per_sqm: 300,
    product_type: "LOTEAMENTO",
  });

  const addCompetitor = () => {
    if (newCompetitor.name) {
      setForm(p => ({ ...p, competitors: [...p.competitors, { ...newCompetitor }] }));
      setNewCompetitor({ name: "", developer: "", total_units: 50, units_sold: 20, units_available: 30, price_per_sqm: 300, product_type: "LOTEAMENTO" });
    }
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/wizard/p7/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Falha na análise");
      const data = await res.json();
      setResult(data);
      if (onComplete) onComplete(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-border pb-4">
        <h3 className="text-lg font-medium flex items-center gap-2">
          <Building2 className="h-5 w-5 text-primary" />
          Oferta & Mercado
        </h3>
        <p className="text-sm text-muted-foreground">Análise competitiva e benchmark de preços.</p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Município</label>
          <input
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
            value={form.municipality}
            onChange={(e) => setForm(p => ({ ...p, municipality: e.target.value }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Raio de Influência (km)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.influence_area_km}
            onChange={(e) => setForm(p => ({ ...p, influence_area_km: parseFloat(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Preço Médio Mercado (R$/m²)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.market_average_price_sqm}
            onChange={(e) => setForm(p => ({ ...p, market_average_price_sqm: parseFloat(e.target.value) }))}
          />
        </div>
      </div>

      {/* Add Competitor */}
      <div className="p-4 bg-card/50 rounded-lg border border-border space-y-3">
        <h4 className="text-sm font-medium">Adicionar Concorrente</h4>
        <div className="grid grid-cols-4 gap-3">
          <input placeholder="Nome" className="h-9 px-3 rounded border border-input bg-background/50 text-sm" value={newCompetitor.name} onChange={(e) => setNewCompetitor(p => ({ ...p, name: e.target.value }))} />
          <input placeholder="Incorporadora" className="h-9 px-3 rounded border border-input bg-background/50 text-sm" value={newCompetitor.developer} onChange={(e) => setNewCompetitor(p => ({ ...p, developer: e.target.value }))} />
          <input type="number" placeholder="Total Unid." className="h-9 px-3 rounded border border-input bg-background/50 text-sm font-mono" value={newCompetitor.total_units} onChange={(e) => setNewCompetitor(p => ({ ...p, total_units: parseInt(e.target.value) }))} />
          <button onClick={addCompetitor} className="h-9 px-4 bg-primary text-primary-foreground rounded text-sm">+ Adicionar</button>
        </div>
        {form.competitors.length > 0 && (
          <div className="text-xs text-muted-foreground mt-2">
            {form.competitors.length} concorrente(s): {form.competitors.map(c => c.name).join(", ")}
          </div>
        )}
      </div>

      <div className="flex justify-end">
        <button onClick={handleAnalyze} disabled={loading} className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 flex items-center gap-2">
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Building2 className="h-4 w-4" />}
          Analisar Oferta
        </button>
      </div>

      {error && <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">{error}</div>}

      {result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in space-y-4">
          <div className="grid grid-cols-4 gap-4">
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Concorrentes</div>
              <div className="text-2xl font-bold">{result.summary.competitors_count}</div>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Estoque Ativo</div>
              <div className="text-2xl font-bold">{result.summary.active_inventory_units}</div>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Preço Médio/m²</div>
              <div className="text-2xl font-mono font-bold">R$ {result.summary.average_price_sqm}</div>
            </div>
            <div className={cn("p-4 rounded-lg border text-center",
              result.summary.market_saturation === "LOW" ? "border-green-500/30 bg-green-500/5" :
              result.summary.market_saturation === "MEDIUM" ? "border-yellow-500/30 bg-yellow-500/5" :
              "border-red-500/30 bg-red-500/5"
            )}>
              <div className="text-xs font-bold uppercase text-muted-foreground">Saturação</div>
              <div className="text-xl font-bold">{result.summary.market_saturation}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==================== P8: ABSORPTION ====================
export function P8AbsorptionStep({ qualifiedDemand = 200, activeInventory = 50, onComplete }: { qualifiedDemand?: number; activeInventory?: number; onComplete?: (data: any) => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);

  const [form, setForm] = useState({
    municipality: "",
    project_units: 30,
    project_price_avg: 180000,
    qualified_demand: qualifiedDemand,
    active_inventory: activeInventory,
    market_vso_monthly: 0.08,
  });

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/wizard/p8/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Falha na análise");
      const data = await res.json();
      setResult(data);
      if (onComplete) onComplete(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-border pb-4">
        <h3 className="text-lg font-medium flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-primary" />
          Absorção (VSO)
        </h3>
        <p className="text-sm text-muted-foreground">Velocidade de vendas e timeline de absorção.</p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Município</label>
          <input
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
            value={form.municipality}
            onChange={(e) => setForm(p => ({ ...p, municipality: e.target.value }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Unidades do Projeto</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.project_units}
            onChange={(e) => setForm(p => ({ ...p, project_units: parseInt(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Preço Médio (R$)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.project_price_avg}
            onChange={(e) => setForm(p => ({ ...p, project_price_avg: parseFloat(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Demanda Qualificada (P6)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.qualified_demand}
            onChange={(e) => setForm(p => ({ ...p, qualified_demand: parseInt(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Estoque Ativo (P7)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.active_inventory}
            onChange={(e) => setForm(p => ({ ...p, active_inventory: parseInt(e.target.value) }))}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">VSO Mercado (% mensal)</label>
          <input
            type="number"
            step="0.01"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            value={form.market_vso_monthly}
            onChange={(e) => setForm(p => ({ ...p, market_vso_monthly: parseFloat(e.target.value) }))}
          />
        </div>
      </div>

      <div className="flex justify-end">
        <button onClick={handleAnalyze} disabled={loading} className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 flex items-center gap-2">
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <TrendingUp className="h-4 w-4" />}
          Calcular Absorção
        </button>
      </div>

      {error && <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">{error}</div>}

      {result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in space-y-4">
          <div className="grid grid-cols-4 gap-4">
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Vendas/Mês</div>
              <div className="text-2xl font-mono font-bold">{result.absorption_projection.monthly_sales_velocity.toFixed(1)}</div>
            </div>
            <div className={cn("p-4 rounded-lg border text-center",
              result.absorption_projection.projected_absorption_months <= 24 ? "border-green-500/30 bg-green-500/5" :
              result.absorption_projection.projected_absorption_months <= 36 ? "border-yellow-500/30 bg-yellow-500/5" :
              "border-red-500/30 bg-red-500/5"
            )}>
              <div className="text-xs font-bold uppercase text-muted-foreground">Prazo Absorção</div>
              <div className="text-2xl font-bold">{result.absorption_projection.projected_absorption_months} meses</div>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Fator Demanda:Oferta</div>
              <div className="text-2xl font-mono font-bold">{result.market_dynamics.demand_supply_ratio.toFixed(1)}:1</div>
            </div>
            <div className={cn("p-4 rounded-lg border text-center",
              result.absorption_projection.assessment === "EXCELLENT" || result.absorption_projection.assessment === "GOOD" ? "border-green-500/30 bg-green-500/5" :
              result.absorption_projection.assessment === "MODERATE" ? "border-yellow-500/30 bg-yellow-500/5" :
              "border-red-500/30 bg-red-500/5"
            )}>
              <div className="text-xs font-bold uppercase text-muted-foreground">Avaliação</div>
              <div className="text-xl font-bold">{result.absorption_projection.assessment}</div>
            </div>
          </div>
          <div className="bg-blue-500/5 border border-blue-500/20 rounded-lg p-4">
            <div className="text-sm">{result.absorption_projection.recommendation}</div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==================== P9: VALIDATION ====================
export function P9ValidationStep({ qualifiedDemand = 200, activeInventory = 50, absorptionMonths = 24, onComplete }: { qualifiedDemand?: number; activeInventory?: number; absorptionMonths?: number; onComplete?: (data: any) => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);

  const [form, setForm] = useState({
    municipality: "",
    qualified_demand: qualifiedDemand,
    active_inventory: activeInventory,
    competitors_count: 3,
    projected_absorption_months: absorptionMonths,
    project_units: 30,
    project_price_sqm: 300,
    market_price_sqm: 280,
  });

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/wizard/p9/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Falha na análise");
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
      case "CAUTION": return "bg-yellow-500/10 text-yellow-500 border-yellow-500/50";
      case "HOLD": return "bg-orange-500/10 text-orange-500 border-orange-500/50";
      default: return "bg-red-500/10 text-red-500 border-red-500/50";
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-border pb-4">
        <h3 className="text-lg font-medium flex items-center gap-2">
          <Target className="h-5 w-5 text-primary" />
          Convalidação 4:1
        </h3>
        <p className="text-sm text-muted-foreground">Gate estratégico final antes da modelagem financeira.</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Município</label>
          <input className="w-full h-10 px-3 rounded-md border border-input bg-background/50" value={form.municipality} onChange={(e) => setForm(p => ({ ...p, municipality: e.target.value }))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Demanda Qualificada</label>
          <input type="number" className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono" value={form.qualified_demand} onChange={(e) => setForm(p => ({ ...p, qualified_demand: parseInt(e.target.value) }))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Estoque Ativo</label>
          <input type="number" className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono" value={form.active_inventory} onChange={(e) => setForm(p => ({ ...p, active_inventory: parseInt(e.target.value) }))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Unidades Projeto</label>
          <input type="number" className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono" value={form.project_units} onChange={(e) => setForm(p => ({ ...p, project_units: parseInt(e.target.value) }))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Preço Projeto (R$/m²)</label>
          <input type="number" className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono" value={form.project_price_sqm} onChange={(e) => setForm(p => ({ ...p, project_price_sqm: parseFloat(e.target.value) }))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Preço Mercado (R$/m²)</label>
          <input type="number" className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono" value={form.market_price_sqm} onChange={(e) => setForm(p => ({ ...p, market_price_sqm: parseFloat(e.target.value) }))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Prazo Absorção (meses)</label>
          <input type="number" className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono" value={form.projected_absorption_months} onChange={(e) => setForm(p => ({ ...p, projected_absorption_months: parseInt(e.target.value) }))} />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Nº Concorrentes</label>
          <input type="number" className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono" value={form.competitors_count} onChange={(e) => setForm(p => ({ ...p, competitors_count: parseInt(e.target.value) }))} />
        </div>
      </div>

      <div className="flex justify-end">
        <button onClick={handleAnalyze} disabled={loading} className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 flex items-center gap-2">
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <CheckCircle className="h-4 w-4" />}
          Validar Gate 4:1
        </button>
      </div>

      {error && <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">{error}</div>}

      {result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in space-y-4">
          <div className="grid grid-cols-4 gap-4">
            <div className={cn("p-4 rounded-lg border flex flex-col items-center", getDecisionStyle(result.gate_result.decision))}>
              <span className="text-xs font-bold uppercase tracking-widest opacity-70">Gate 4:1</span>
              <span className="text-3xl font-bold mt-1">{result.key_ratio.gate_4_1_ratio.toFixed(1)}:1</span>
            </div>
            <div className={cn("p-4 rounded-lg border flex flex-col items-center", getDecisionStyle(result.gate_result.decision))}>
              <span className="text-xs font-bold uppercase tracking-widest opacity-70">Decisão</span>
              <span className="text-2xl font-bold mt-2">{result.gate_result.decision}</span>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card text-center">
              <div className="text-xs font-bold uppercase text-muted-foreground">Gates Aprovados</div>
              <div className="text-2xl font-bold text-green-500">{result.gates_summary.passed}/{result.gates_summary.total}</div>
            </div>
            <div className={cn("p-4 rounded-lg border text-center",
              result.market_position.price_position === "COMPETITIVE" ? "border-green-500/30 bg-green-500/5" :
              result.market_position.price_position === "PREMIUM" ? "border-yellow-500/30 bg-yellow-500/5" :
              "border-blue-500/30 bg-blue-500/5"
            )}>
              <div className="text-xs font-bold uppercase text-muted-foreground">Posição Preço</div>
              <div className="text-xl font-bold">{result.market_position.price_position}</div>
            </div>
          </div>

          {/* Gates Detail */}
          <div className="space-y-2">
            {result.gates_detail.map((gate: any) => (
              <div key={gate.gate} className={cn("flex items-center justify-between p-3 rounded-lg border", gate.passed ? "border-green-500/30 bg-green-500/5" : "border-red-500/30 bg-red-500/5")}>
                <span className="text-sm">{gate.gate.replace(/_/g, " ")}</span>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-mono">{gate.value} / {gate.threshold}</span>
                  <span className={cn("text-xs font-bold", gate.passed ? "text-green-500" : "text-red-500")}>{gate.status}</span>
                </div>
              </div>
            ))}
          </div>

          <div className={cn("border rounded-lg p-4", result.gate_result.is_validated ? "bg-green-500/5 border-green-500/20" : "bg-red-500/5 border-red-500/20")}>
            <div className={cn("text-sm font-medium mb-1", result.gate_result.is_validated ? "text-green-400" : "text-red-400")}>
              {result.gate_result.is_validated ? "✓ Validado" : "✗ Não Validado"}
            </div>
            <div className="text-sm">{result.gate_result.recommendation}</div>
          </div>
        </div>
      )}
    </div>
  );
}
