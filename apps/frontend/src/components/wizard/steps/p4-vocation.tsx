"use client";

import { useState } from "react";
import { Loader2, MapPin, Building, Zap, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface P4Output {
  total_score: number;
  score_100: number;
  decision: string;
  recommendation: string;
  pillars: {
    pilar_1_zoning: { score: number; max: number; weight: number };
    pilar_2_centrality: { score: number; max: number; weight: number };
    pilar_3_infrastructure: { score: number; max: number; weight: number };
  };
  product_recommendation: {
    primary: string;
    alternatives: string[];
    confidence: number;
  };
}

const ZONING_OPTIONS = [
  { value: "ZR1", label: "ZR1 - Residencial Unifamiliar" },
  { value: "ZR2", label: "ZR2 - Residencial Multifamiliar Baixa" },
  { value: "ZR3", label: "ZR3 - Residencial Multifamiliar Alta" },
  { value: "ZM", label: "ZM - Zona Mista" },
  { value: "ZC", label: "ZC - Zona Comercial" },
  { value: "ZEIS", label: "ZEIS - Interesse Social" },
  { value: "APA", label: "APA - Proteção Ambiental" },
];

const INFRASTRUCTURE_OPTIONS = [
  { value: "COMPLETE", label: "Completa" },
  { value: "PARTIAL", label: "Parcial" },
  { value: "BASIC", label: "Básica" },
  { value: "NONE", label: "Inexistente" },
];

export default function P4VocationStep() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<P4Output | null>(null);

  // Form state
  const [form, setForm] = useState({
    municipality: "",
    neighborhood: "",
    zoning_type: "ZR2",
    max_height_floors: 4,
    max_coverage_ratio: 0.6,
    max_floor_area_ratio: 2.0,
    distance_city_center_km: 2.0,
    distance_main_avenue_km: 0.5,
    public_transport_available: true,
    distance_metro_station_km: null as number | null,
    infrastructure_level: "COMPLETE",
    has_paved_access: true,
    has_water_network: true,
    has_sewage_network: true,
    has_electricity: true,
    has_gas_network: false,
    has_fiber_optic: false,
    land_area_sqm: 5000,
    land_price_per_sqm: 150,
    target_segment: "MEDIO",
  });

  const updateForm = (field: string, value: any) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");

    try {
      if (!form.municipality || !form.neighborhood) {
        throw new Error("Informe município e bairro");
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/wizard/p4/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!res.ok) throw new Error("Falha na análise");

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadExample = () => {
    setForm({
      municipality: "Leopoldina",
      neighborhood: "Centro",
      zoning_type: "ZR2",
      max_height_floors: 4,
      max_coverage_ratio: 0.6,
      max_floor_area_ratio: 2.0,
      distance_city_center_km: 1.5,
      distance_main_avenue_km: 0.3,
      public_transport_available: true,
      distance_metro_station_km: null,
      infrastructure_level: "COMPLETE",
      has_paved_access: true,
      has_water_network: true,
      has_sewage_network: true,
      has_electricity: true,
      has_gas_network: false,
      has_fiber_optic: true,
      land_area_sqm: 8000,
      land_price_per_sqm: 180,
      target_segment: "MEDIO",
    });
  };

  const getDecisionStyle = (decision: string) => {
    switch (decision) {
      case "GO": return "bg-green-500/10 text-green-500 border-green-500/50";
      case "CAUTION": return "bg-yellow-500/10 text-yellow-500 border-yellow-500/50";
      case "HOLD": return "bg-orange-500/10 text-orange-500 border-orange-500/50";
      default: return "bg-red-500/10 text-red-500 border-red-500/50";
    }
  };

  const getScoreWidth = (score: number, max: number) => `${(score / max) * 100}%`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div>
          <h3 className="text-lg font-medium flex items-center gap-2">
            <Building className="h-5 w-5 text-primary" />
            Vocação Imobiliária
          </h3>
          <p className="text-sm text-muted-foreground mt-1">
            Matriz de Atratividade 3 Pilares (Zoneamento, Centralidade, Infraestrutura)
          </p>
        </div>
        <button onClick={loadExample} className="text-xs text-primary underline">
          Carregar Exemplo
        </button>
      </div>

      {/* Form Sections */}
      <div className="space-y-6">
        {/* Location */}
        <div className="grid grid-cols-4 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Município</label>
            <input
              type="text"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
              value={form.municipality}
              onChange={(e) => updateForm("municipality", e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Bairro</label>
            <input
              type="text"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
              value={form.neighborhood}
              onChange={(e) => updateForm("neighborhood", e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Área (m²)</label>
            <input
              type="number"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.land_area_sqm}
              onChange={(e) => updateForm("land_area_sqm", parseFloat(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Preço/m² (R$)</label>
            <input
              type="number"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.land_price_per_sqm}
              onChange={(e) => updateForm("land_price_per_sqm", parseFloat(e.target.value))}
            />
          </div>
        </div>

        {/* Zoning */}
        <div className="grid grid-cols-4 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Zoneamento</label>
            <select
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
              value={form.zoning_type}
              onChange={(e) => updateForm("zoning_type", e.target.value)}
            >
              {ZONING_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Gabarito (pavimentos)</label>
            <input
              type="number"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.max_height_floors}
              onChange={(e) => updateForm("max_height_floors", parseInt(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Taxa Ocupação</label>
            <input
              type="number"
              step="0.1"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.max_coverage_ratio}
              onChange={(e) => updateForm("max_coverage_ratio", parseFloat(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Coef. Aproveitamento</label>
            <input
              type="number"
              step="0.1"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.max_floor_area_ratio}
              onChange={(e) => updateForm("max_floor_area_ratio", parseFloat(e.target.value))}
            />
          </div>
        </div>

        {/* Centrality */}
        <div className="grid grid-cols-4 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Distância Centro (km)</label>
            <input
              type="number"
              step="0.1"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.distance_city_center_km}
              onChange={(e) => updateForm("distance_city_center_km", parseFloat(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Distância Via Principal (km)</label>
            <input
              type="number"
              step="0.1"
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
              value={form.distance_main_avenue_km}
              onChange={(e) => updateForm("distance_main_avenue_km", parseFloat(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Infraestrutura</label>
            <select
              className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
              value={form.infrastructure_level}
              onChange={(e) => updateForm("infrastructure_level", e.target.value)}
            >
              {INFRASTRUCTURE_OPTIONS.map(opt => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Transporte Público</label>
            <div className="flex items-center gap-4 h-10">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={form.public_transport_available}
                  onChange={(e) => updateForm("public_transport_available", e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm">Disponível</span>
              </label>
            </div>
          </div>
        </div>

        {/* Utilities */}
        <div className="flex flex-wrap gap-4 p-4 bg-card/50 rounded-lg border border-border">
          <span className="text-sm font-medium w-full mb-2">Infraestrutura Disponível:</span>
          {[
            { key: "has_water_network", label: "Água" },
            { key: "has_electricity", label: "Energia" },
            { key: "has_sewage_network", label: "Esgoto" },
            { key: "has_paved_access", label: "Acesso Pavimentado" },
            { key: "has_gas_network", label: "Gás Encanado" },
            { key: "has_fiber_optic", label: "Fibra Óptica" },
          ].map(item => (
            <label key={item.key} className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={(form as any)[item.key]}
                onChange={(e) => updateForm(item.key, e.target.checked)}
                className="rounded"
              />
              <span className="text-sm">{item.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 flex items-center gap-2"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <MapPin className="h-4 w-4" />}
          Analisar Vocação
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">{error}</div>
      )}

      {/* Results */}
      {result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in space-y-6">
          {/* Score Summary */}
          <div className="grid grid-cols-4 gap-4">
            <div className={cn("p-4 rounded-lg border flex flex-col items-center", getDecisionStyle(result.decision))}>
              <span className="text-xs font-bold uppercase tracking-widest opacity-70">Score Total</span>
              <span className="text-3xl font-bold">{result.total_score.toFixed(1)}</span>
              <span className="text-xs opacity-70">/ 10</span>
            </div>
            <div className={cn("p-4 rounded-lg border flex flex-col items-center", getDecisionStyle(result.decision))}>
              <span className="text-xs font-bold uppercase tracking-widest opacity-70">Decisão</span>
              <span className="text-2xl font-bold mt-2">{result.decision}</span>
            </div>
            <div className="col-span-2 p-4 rounded-lg border border-blue-500/30 bg-blue-500/5">
              <span className="text-xs font-bold uppercase tracking-widest text-blue-400">Produto Recomendado</span>
              <div className="text-lg font-bold mt-1">{result.product_recommendation.primary?.replace(/_/g, " ") || "N/A"}</div>
              <div className="text-xs text-muted-foreground">
                Confiança: {(result.product_recommendation.confidence * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          {/* 3 Pillars */}
          <div className="space-y-4">
            <h4 className="text-sm font-medium">Matriz 3 Pilares</h4>
            {[
              { key: "pilar_1_zoning", label: "Pilar 1: Zoneamento & Potencial", weight: "30%" },
              { key: "pilar_2_centrality", label: "Pilar 2: Centralidade & Acessibilidade", weight: "40%" },
              { key: "pilar_3_infrastructure", label: "Pilar 3: Infraestrutura", weight: "30%" },
            ].map(pilar => {
              const data = (result.pillars as any)[pilar.key];
              return (
                <div key={pilar.key} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>{pilar.label}</span>
                    <span className="font-mono">{data.score.toFixed(1)} / {data.max} ({pilar.weight})</span>
                  </div>
                  <div className="h-2 bg-border rounded-full overflow-hidden">
                    <div
                      className={cn(
                        "h-full rounded-full transition-all",
                        data.score / data.max >= 0.7 ? "bg-green-500" :
                        data.score / data.max >= 0.5 ? "bg-yellow-500" : "bg-red-500"
                      )}
                      style={{ width: getScoreWidth(data.score, data.max) }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Recommendation */}
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
            <div className="text-sm font-medium text-primary mb-1">Recomendação</div>
            <div className="text-sm">{result.recommendation}</div>
          </div>
        </div>
      )}
    </div>
  );
}
