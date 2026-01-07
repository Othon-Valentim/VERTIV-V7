"use client";

import { useState } from "react";
import { Loader2, Shield, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

interface P5Output {
  gate_result: {
    decision: string;
    is_approved: boolean;
    recommendation: string;
  };
  summary: {
    total_checks: number;
    passed: number;
    failed: number;
    blocking_issues: number;
    compliance_score: number;
  };
  category_scores: Record<string, { passed: number; total: number; score: number }>;
  blocking_issues: Array<{
    id: string;
    description: string;
    finding: string;
    recommendation: string;
  }>;
  all_checks: Array<{
    id: string;
    category: string;
    description: string;
    is_passed: boolean;
    risk_level: string;
    finding: string | null;
    recommendation: string | null;
    blocking: boolean;
  }>;
}

export default function P5LegalStep() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<P5Output | null>(null);

  // Form state
  const [form, setForm] = useState({
    land_registration_number: "",
    municipality: "",
    notary_office: "1º Ofício de Registro de Imóveis",
    // Ownership
    has_clear_title: true,
    is_registered: true,
    has_pending_lawsuits: false,
    has_liens: false,
    has_usufruct: false,
    // Environmental
    is_in_app: false,
    is_in_apa: false,
    is_in_reserve: false,
    has_contamination: false,
    requires_environmental_study: false,
    has_environmental_license: null as boolean | null,
    // Urban
    complies_with_zoning: true,
    complies_with_master_plan: true,
    has_building_restrictions: false,
    has_heritage_protection: false,
    requires_eia_rima: false,
    // Fiscal
    has_iptu_debt: false,
    has_itr_debt: false,
    has_tax_liens: false,
    tax_debt_amount: 0,
    // Judicial
    pending_lawsuits_count: 0,
    has_adverse_possession_claims: false,
    has_expropriation_risk: false,
    has_neighborhood_disputes: false,
    // Documentation
    has_updated_registration: true,
    has_topographic_survey: false,
    has_georeferencing: false,
  });

  const updateForm = (field: string, value: any) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");

    try {
      if (!form.land_registration_number || !form.municipality) {
        throw new Error("Informe a matrícula e o município");
      }

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/wizard/p5/analyze`, {
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
    setForm(prev => ({
      ...prev,
      land_registration_number: "12.345",
      municipality: "Leopoldina-MG",
      notary_office: "1º Ofício de Registro de Imóveis",
    }));
  };

  const getDecisionStyle = (decision: string) => {
    switch (decision) {
      case "GO": return "bg-green-500/10 text-green-500 border-green-500/50";
      case "CAUTION": return "bg-yellow-500/10 text-yellow-500 border-yellow-500/50";
      case "HOLD": return "bg-orange-500/10 text-orange-500 border-orange-500/50";
      default: return "bg-red-500/10 text-red-500 border-red-500/50";
    }
  };

  const getRiskIcon = (riskLevel: string, isPassed: boolean) => {
    if (isPassed) return <CheckCircle className="h-4 w-4 text-green-500" />;
    if (riskLevel === "CRITICAL") return <XCircle className="h-4 w-4 text-red-500" />;
    if (riskLevel === "HIGH") return <AlertTriangle className="h-4 w-4 text-orange-500" />;
    return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
  };

  const CategorySection = ({ title, items }: { title: string; items: { label: string; field: string; type?: string }[] }) => (
    <div className="space-y-3">
      <h4 className="text-sm font-medium text-muted-foreground">{title}</h4>
      <div className="grid grid-cols-2 gap-3">
        {items.map(item => (
          <label key={item.field} className="flex items-center gap-2 cursor-pointer text-sm">
            <input
              type="checkbox"
              checked={item.type === "negative" ? !(form as any)[item.field] : (form as any)[item.field]}
              onChange={(e) => updateForm(item.field, item.type === "negative" ? !e.target.checked : e.target.checked)}
              className="rounded"
            />
            <span className={cn(
              (form as any)[item.field] === (item.type !== "negative") ? "text-green-600" : "text-muted-foreground"
            )}>
              {item.label}
            </span>
          </label>
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div>
          <h3 className="text-lg font-medium flex items-center gap-2">
            <Shield className="h-5 w-5 text-primary" />
            Due Diligence Legal
          </h3>
          <p className="text-sm text-muted-foreground mt-1">
            Checklist completo de regularidade jurídica (Gate Binário)
          </p>
        </div>
        <button onClick={loadExample} className="text-xs text-primary underline">
          Carregar Exemplo
        </button>
      </div>

      {/* Basic Info */}
      <div className="grid grid-cols-3 gap-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">Matrícula do Imóvel</label>
          <input
            type="text"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono"
            placeholder="Ex: 12.345"
            value={form.land_registration_number}
            onChange={(e) => updateForm("land_registration_number", e.target.value)}
          />
        </div>
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
          <label className="text-sm font-medium">Cartório</label>
          <input
            type="text"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50"
            value={form.notary_office}
            onChange={(e) => updateForm("notary_office", e.target.value)}
          />
        </div>
      </div>

      {/* Checklist Categories */}
      <div className="grid grid-cols-2 gap-6 p-4 bg-card/50 rounded-lg border border-border">
        <CategorySection
          title="📋 Titularidade"
          items={[
            { label: "Título limpo e regular", field: "has_clear_title" },
            { label: "Imóvel registrado", field: "is_registered" },
            { label: "Sem ônus (hipoteca, penhora)", field: "has_liens", type: "negative" },
            { label: "Sem usufruto", field: "has_usufruct", type: "negative" },
          ]}
        />

        <CategorySection
          title="🌿 Ambiental"
          items={[
            { label: "Fora de APP", field: "is_in_app", type: "negative" },
            { label: "Fora de APA restritiva", field: "is_in_apa", type: "negative" },
            { label: "Sem contaminação", field: "has_contamination", type: "negative" },
            { label: "Licença ambiental (se necessária)", field: "has_environmental_license" },
          ]}
        />

        <CategorySection
          title="🏛️ Urbanístico"
          items={[
            { label: "Conforme zoneamento", field: "complies_with_zoning" },
            { label: "Conforme Plano Diretor", field: "complies_with_master_plan" },
            { label: "Sem tombamento", field: "has_heritage_protection", type: "negative" },
            { label: "Sem restrições construtivas", field: "has_building_restrictions", type: "negative" },
          ]}
        />

        <CategorySection
          title="💰 Fiscal"
          items={[
            { label: "IPTU em dia", field: "has_iptu_debt", type: "negative" },
            { label: "Sem penhora fiscal", field: "has_tax_liens", type: "negative" },
          ]}
        />

        <CategorySection
          title="⚖️ Judicial"
          items={[
            { label: "Sem usucapião", field: "has_adverse_possession_claims", type: "negative" },
            { label: "Sem risco de desapropriação", field: "has_expropriation_risk", type: "negative" },
            { label: "Sem litígios vizinhança", field: "has_neighborhood_disputes", type: "negative" },
          ]}
        />

        <CategorySection
          title="📄 Documentação"
          items={[
            { label: "Matrícula atualizada", field: "has_updated_registration" },
            { label: "Levantamento topográfico", field: "has_topographic_survey" },
            { label: "Georreferenciamento (se rural)", field: "has_georeferencing" },
          ]}
        />
      </div>

      <div className="flex justify-end">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 flex items-center gap-2"
        >
          {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Shield className="h-4 w-4" />}
          Executar Due Diligence
        </button>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm">{error}</div>
      )}

      {/* Results */}
      {result && (
        <div className="mt-6 pt-6 border-t border-border animate-in fade-in space-y-6">
          {/* Gate Result */}
          <div className="grid grid-cols-4 gap-4">
            <div className={cn("p-4 rounded-lg border flex flex-col items-center", getDecisionStyle(result.gate_result.decision))}>
              <span className="text-xs font-bold uppercase tracking-widest opacity-70">Gate</span>
              <span className="text-2xl font-bold mt-1">{result.gate_result.decision}</span>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card">
              <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground">Compliance</span>
              <div className="text-2xl font-mono font-bold mt-1">{result.summary.compliance_score.toFixed(0)}%</div>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card">
              <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground">Aprovados</span>
              <div className="text-2xl font-mono font-bold mt-1 text-green-500">
                {result.summary.passed}/{result.summary.total_checks}
              </div>
            </div>
            <div className="p-4 rounded-lg border border-border bg-card">
              <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground">Bloqueios</span>
              <div className={cn("text-2xl font-mono font-bold mt-1", result.summary.blocking_issues > 0 ? "text-red-500" : "text-green-500")}>
                {result.summary.blocking_issues}
              </div>
            </div>
          </div>

          {/* Blocking Issues */}
          {result.blocking_issues.length > 0 && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <h4 className="text-sm font-medium text-red-400 mb-3 flex items-center gap-2">
                <XCircle className="h-4 w-4" />
                Impedimentos Críticos ({result.blocking_issues.length})
              </h4>
              <div className="space-y-2">
                {result.blocking_issues.map(issue => (
                  <div key={issue.id} className="bg-background/50 rounded p-3">
                    <div className="font-medium text-sm">{issue.description}</div>
                    <div className="text-xs text-red-400 mt-1">{issue.finding}</div>
                    <div className="text-xs text-muted-foreground mt-1">→ {issue.recommendation}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* All Checks */}
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Todos os Checks ({result.summary.total_checks})</h4>
            <div className="max-h-64 overflow-y-auto space-y-1 bg-card/50 rounded-lg border border-border p-3">
              {result.all_checks.map(check => (
                <div
                  key={check.id}
                  className={cn(
                    "flex items-center gap-3 p-2 rounded text-sm",
                    check.is_passed ? "bg-green-500/5" : check.blocking ? "bg-red-500/10" : "bg-yellow-500/5"
                  )}
                >
                  {getRiskIcon(check.risk_level, check.is_passed)}
                  <span className="flex-1">{check.description}</span>
                  <span className="text-xs text-muted-foreground">{check.category}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Recommendation */}
          <div className={cn("border rounded-lg p-4", result.gate_result.is_approved ? "bg-green-500/5 border-green-500/20" : "bg-red-500/5 border-red-500/20")}>
            <div className={cn("text-sm font-medium mb-1", result.gate_result.is_approved ? "text-green-400" : "text-red-400")}>
              {result.gate_result.is_approved ? "✓ Aprovado" : "✗ Reprovado"}
            </div>
            <div className="text-sm">{result.gate_result.recommendation}</div>
          </div>
        </div>
      )}
    </div>
  );
}
