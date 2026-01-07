"use client";

import { useState } from "react";
import { useWizardStore } from "@/store/wizard-store";
import { P1GarimpoInput, MarketCyclePhase, GoNoGoDecision } from "@vertiv/shared/types";
import { Loader2, CheckCircle2, AlertTriangle, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export default function P1GarimpoStep() {
  const { p1Input, p1Output, setP1Input, setP1Output } = useWizardStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");

    try {
      // Basic validation
      if (!p1Input.area_sqm || !p1Input.asking_price || !p1Input.location_municipality) {
         throw new Error("Please fill in all required fields.");
      }

      const payload: P1GarimpoInput = {
          location_municipality: p1Input.location_municipality!,
          location_neighborhood: p1Input.location_neighborhood || "",
          area_sqm: Number(p1Input.area_sqm),
          asking_price: String(p1Input.asking_price) // Send as string to preserve decimal precision if needed
      };

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/p1/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error("Analysis failed. Check backend connection.");
      }

      const data = await res.json();
      setP1Output(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getBadgeColor = (decision: GoNoGoDecision) => {
      switch(decision) {
          case GoNoGoDecision.GO: return "bg-green-500/10 text-green-500 border-green-500/50";
          case GoNoGoDecision.CAUTION: return "bg-yellow-500/10 text-yellow-500 border-yellow-500/50";
          case GoNoGoDecision.NO_GO: return "bg-red-500/10 text-red-500 border-red-500/50";
          default: return "bg-muted text-muted-foreground";
      }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div>
            <h3 className="text-lg font-medium">Input Parameters</h3>
            <p className="text-sm text-muted-foreground">Define the basic land characteristics.</p>
        </div>
        <button 
            onClick={() => setP1Input({ location_municipality: "São Paulo", location_neighborhood: "Jardins", area_sqm: 1000, asking_price: "500000" })}
            className="text-xs text-primary underline"
        >
            Load Example Deal
        </button>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="space-y-2">
          <label className="text-sm font-medium">Municipality</label>
          <input
            type="text"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
            placeholder="e.g. Leopoldina-MG"
            value={p1Input.location_municipality || ""}
            onChange={(e) => setP1Input({ location_municipality: e.target.value })}
          />
        </div>
        
        <div className="space-y-2">
            <label className="text-sm font-medium">Neighborhood</label>
            <input
                type="text"
                className="w-full h-10 px-3 rounded-md border border-input bg-background/50 focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted-foreground/50"
                placeholder="e.g. Centro"
                value={p1Input.location_neighborhood || ""}
                onChange={(e) => setP1Input({ location_neighborhood: e.target.value })}
            />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Total Area (m²)</label>
          <input
            type="number"
            className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono focus:outline-none focus:ring-1 focus:ring-primary"
            placeholder="0.00"
            value={p1Input.area_sqm || ""}
            onChange={(e) => setP1Input({ area_sqm: parseFloat(e.target.value) })}
          />
        </div>

        <div className="space-y-2">
            <label className="text-sm font-medium">Asking Price (BRL)</label>
            <input
                type="number"
                className="w-full h-10 px-3 rounded-md border border-input bg-background/50 font-mono focus:outline-none focus:ring-1 focus:ring-primary"
                placeholder="0.00"
                value={p1Input.asking_price || ""}
                onChange={(e) => setP1Input({ asking_price: e.target.value })}
            />
        </div>
      </div>

      <div className="flex justify-end pt-4">
        <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-primary text-primary-foreground px-6 py-2 rounded-md font-medium hover:bg-primary/90 transition-colors flex items-center gap-2"
        >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Run Analysis"}
        </button>
      </div>

      {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded text-sm flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" />
              {error}
          </div>
      )}

      {/* Results Section */}
      {p1Output && (
          <div className="mt-8 pt-6 border-t border-border animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-lg font-medium mb-4">Analysis Result</h3>
              
              <div className="grid grid-cols-3 gap-4">
                  {/* Decision Card */}
                  <div className={cn("p-4 rounded-lg border flex flex-col items-center justify-center text-center", getBadgeColor(p1Output.decision))}>
                      <span className="text-xs font-bold uppercase tracking-widest mb-1 opacity-70">Decision</span>
                      <span className="text-2xl font-bold">{p1Output.decision.replace("_", " ")}</span>
                  </div>

                  {/* Score Card */}
                  <div className="p-4 rounded-lg border border-border bg-card flex flex-col items-center justify-center text-center">
                       <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground mb-1">Attractiveness</span>
                       <div className="text-2xl font-mono font-bold">{p1Output.score_attractiveness.toFixed(1)}<span className="text-xs text-muted-foreground">/100</span></div>
                  </div>

                  {/* Cycle Card */}
                  <div className="p-4 rounded-lg border border-border bg-card flex flex-col items-center justify-center text-center">
                       <span className="text-xs font-bold uppercase tracking-widest text-muted-foreground mb-1">Market Cycle</span>
                       <div className="text-lg font-bold text-blue-400">{p1Output.cycle_phase}</div>
                  </div>
              </div>
          </div>
      )}
    </div>
  );
}
