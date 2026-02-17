"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

interface VarianceRow {
  field: string;
  ai_value: string | number;
  golden_value: string | number;
  mape: string;
  status: "PASS" | "FAIL";
}

export default function AuditPage() {
  const params = useParams();
  const ingestionId = params.id as string;

  const [ingestion, setIngestion] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const apiUrl =
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/api/v7/ingestion/${ingestionId}`);
        if (res.ok) {
          setIngestion(await res.json());
        }
      } catch {
        // Stub mode: show placeholder
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, [ingestionId]);

  // Extract variance data from validation_metrics
  const varianceRows: VarianceRow[] = ingestion?.validation_metrics
    ?.step_1_inputs?.details?.numeric_errors?.map((err: any) => ({
      field: err.field,
      ai_value: err.ai,
      golden_value: err.golden,
      mape: `${(err.mape * 100).toFixed(1)}%`,
      status: err.mape <= 0.05 ? "PASS" : "FAIL",
    })) || [];

  const accuracyScore =
    ingestion?.validation_metrics?.accuracy_score ?? "—";
  const operationLevel = ingestion?.status ?? "AWAITING";
  const vplMape =
    ingestion?.validation_metrics?.step_2_impact?.details?.vpl_mape;

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* Header Bar */}
      <div className="border-b border-zinc-800 px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div
            className={`w-3 h-3 rounded-none ${
              operationLevel === "AUTONOMOUS_SENTENCED"
                ? "bg-emerald-500"
                : operationLevel === "PENDING_HUMAN_AUDIT"
                ? "bg-amber-500 animate-pulse"
                : operationLevel === "KILLED"
                ? "bg-red-500"
                : "bg-zinc-600"
            }`}
          />
          <h1 className="text-lg font-mono tracking-tight">
            AUDIT <span className="text-zinc-500">/</span>{" "}
            <span className="text-zinc-400 text-sm">{ingestionId.slice(0, 8)}...</span>
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-zinc-500 uppercase tracking-wider">
            {operationLevel.replace(/_/g, " ")}
          </span>
          <span
            className={`px-3 py-1 text-xs font-mono tracking-wider ${
              Number(accuracyScore) >= 92
                ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                : Number(accuracyScore) >= 85
                ? "bg-amber-950 text-amber-400 border border-amber-800"
                : "bg-red-950 text-red-400 border border-red-800"
            }`}
          >
            SCORE: {accuracyScore}
          </span>
        </div>
      </div>

      {/* Split Screen */}
      <div className="grid grid-cols-2 divide-x divide-zinc-800 min-h-[calc(100vh-64px)]">
        {/* LEFT: AI Evidence */}
        <div className="p-8">
          <div className="mb-6">
            <h2 className="text-sm uppercase tracking-[0.2em] text-cyan-400 font-mono mb-1">
              IA — Dados Extraídos
            </h2>
            <p className="text-xs text-zinc-600">
              Payload estruturado pelo motor agêntico
            </p>
          </div>

          {isLoading ? (
            <div className="flex items-center gap-2 text-zinc-600 text-sm font-mono">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              Carregando...
            </div>
          ) : ingestion?.llm_extracted_payload ? (
            <pre className="text-xs font-mono text-zinc-400 bg-zinc-900 border border-zinc-800 p-4 overflow-auto max-h-[60vh] whitespace-pre-wrap">
              {JSON.stringify(ingestion.llm_extracted_payload, null, 2)}
            </pre>
          ) : (
            <div className="text-sm text-zinc-600 font-mono border border-zinc-800 p-8 text-center">
              Nenhum dado extraído disponível.
              <br />
              <span className="text-zinc-700 text-xs">
                O processamento pode ainda estar em andamento.
              </span>
            </div>
          )}

          {/* Kill Reasons */}
          {ingestion?.kill_reasons && ingestion.kill_reasons.length > 0 && (
            <div className="mt-6 p-4 bg-red-950/20 border border-red-900">
              <h3 className="text-xs uppercase tracking-wider text-red-400 font-mono mb-2">
                ✗ Kill Reasons
              </h3>
              <ul className="text-xs text-red-300 font-mono space-y-1">
                {ingestion.kill_reasons.map((r: string, i: number) => (
                  <li key={i}>• {r}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* RIGHT: V6 Historical */}
        <div className="p-8">
          <div className="mb-6">
            <h2 className="text-sm uppercase tracking-[0.2em] text-amber-400 font-mono mb-1">
              V6 — Histórico Golden
            </h2>
            <p className="text-xs text-zinc-600">
              Referência validada do dataset calibrado
            </p>
          </div>

          {/* Variance Table */}
          {varianceRows.length > 0 ? (
            <div className="border border-zinc-800">
              <table className="w-full text-xs font-mono">
                <thead>
                  <tr className="border-b border-zinc-800 text-zinc-500">
                    <th className="text-left p-3">Campo</th>
                    <th className="text-right p-3">IA</th>
                    <th className="text-right p-3">Golden</th>
                    <th className="text-right p-3">MAPE</th>
                    <th className="text-center p-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {varianceRows.map((row, i) => (
                    <tr
                      key={i}
                      className="border-b border-zinc-900 hover:bg-zinc-900/50"
                    >
                      <td className="p-3 text-zinc-400">{row.field}</td>
                      <td className="p-3 text-right text-zinc-300">
                        {row.ai_value}
                      </td>
                      <td className="p-3 text-right text-zinc-500">
                        {row.golden_value}
                      </td>
                      <td className="p-3 text-right text-zinc-300">
                        {row.mape}
                      </td>
                      <td className="p-3 text-center">
                        <span
                          className={`px-2 py-0.5 ${
                            row.status === "PASS"
                              ? "text-emerald-400 bg-emerald-950/50"
                              : "text-red-400 bg-red-950/50"
                          }`}
                        >
                          {row.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-sm text-zinc-600 font-mono border border-zinc-800 p-8 text-center">
              Sem dados de comparação.
              <br />
              <span className="text-zinc-700 text-xs">
                UUID de calibração não fornecido ou processamento pendente.
              </span>
            </div>
          )}

          {/* VPL Impact */}
          {vplMape !== undefined && vplMape !== null && (
            <div
              className={`mt-6 p-4 border ${
                vplMape <= 0.02
                  ? "border-emerald-800 bg-emerald-950/20"
                  : "border-red-800 bg-red-950/20"
              }`}
            >
              <h3 className="text-xs uppercase tracking-wider font-mono mb-2 text-zinc-400">
                VPL Impact
              </h3>
              <div className="flex items-baseline gap-3">
                <span
                  className={`text-2xl font-mono ${
                    vplMape <= 0.02 ? "text-emerald-400" : "text-red-400"
                  }`}
                >
                  {(vplMape * 100).toFixed(2)}%
                </span>
                <span className="text-xs text-zinc-600">
                  MAPE (threshold: 2.00%)
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Action Bar */}
      <div className="fixed bottom-0 left-0 right-0 border-t border-zinc-800 bg-zinc-950/95 backdrop-blur px-8 py-4 flex items-center justify-between">
        <span className="text-xs font-mono text-zinc-600">
          {ingestionId}
        </span>

        <div className="flex items-center gap-4">
          <button
            className="
              px-8 py-3 text-xs font-mono uppercase tracking-[0.2em]
              bg-rose-950 text-rose-400 border border-rose-800
              hover:bg-rose-900 transition-colors
            "
            onClick={() => {
              // TODO: Trigger manual audit flow
              alert("Enviado para auditoria manual");
            }}
          >
            Auditoria Manual
          </button>

          <button
            className="
              px-8 py-3 text-xs font-mono uppercase tracking-[0.2em]
              bg-emerald-600 text-white
              hover:bg-emerald-500 transition-colors
            "
            disabled={operationLevel === "KILLED"}
            onClick={() => {
              // TODO: Confirm autonomous sentence
              alert("Projeto sentenciado — VPL registrado");
            }}
          >
            Confirmar Sentença
          </button>
        </div>
      </div>
    </div>
  );
}
