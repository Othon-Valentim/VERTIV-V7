"use client";

import { useParams } from "next/navigation";
import { useEffect, useState, useRef, useCallback } from "react";
import { api } from "@/lib/api-client";

interface VarianceRow {
  field: string;
  ai_value: string | number;
  golden_value: string | number;
  mape: string;
  status: "PASS" | "FAIL";
}

/* ── Pipeline Steps ──────────────────────────────────────────────── */
const PIPELINE_STEPS = [
  { key: "UPLOADING", label: "Upload" },
  { key: "INGESTING", label: "Ingestão" },
  { key: "EXTRACTING", label: "Extração IA" },
  { key: "CALCULATING", label: "Polars" },
  { key: "EVALUATING", label: "Avaliação" },
  { key: "DONE", label: "Sentença" },
];

const TERMINAL_STATUSES = [
  "AUTONOMOUS_SENTENCED",
  "PENDING_HUMAN_AUDIT",
  "MANUAL_ASSISTED",
  "KILLED",
  "FAILED",
];
const POLL_INTERVAL_MS = 3000;

function getPipelineStep(status: string): number {
  if (status === "UPLOADING") return 0;
  if (status === "INGESTING") return 1;
  if (TERMINAL_STATUSES.includes(status)) return 5;
  return 2; // default mid-pipeline
}

/* ── Formatter ───────────────────────────────────────────────────── */
function formatCurrency(v: number | undefined | null): string {
  if (v == null) return "—";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(v);
}

function formatPct(v: number | undefined | null, decimals = 2): string {
  if (v == null) return "—";
  return `${v.toFixed(decimals)}%`;
}

/* ================================================================ */

export default function AuditPage() {
  const params = useParams();
  const ingestionId = String(params.id || "");

  const [ingestion, setIngestion] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const pollingRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearTimeout(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  const fetchIngestion = useCallback(async (): Promise<boolean> => {
    if (!ingestionId) {
      setLoadError("ID de ingestão inválido.");
      setIsLoading(false);
      return false;
    }

    try {
      const res = await api.get(`/api/v7/ingestion/${ingestionId}`);

      if (res.status === 401 || res.status === 403) {
        setLoadError("Sessão expirada. Faça login novamente.");
        return false;
      }
      if (res.status === 404) {
        setLoadError("Ingestão não encontrada ou sem acesso.");
        return false;
      }
      if (!res.ok) {
        const errorBody = await res.text().catch(() => "");
        throw new Error(errorBody || `Falha ao consultar ingestão (${res.status}).`);
      }

      const data = await res.json();
      setIngestion(data);
      setLoadError(null);

      if (TERMINAL_STATUSES.includes(data.status)) {
        return false;
      }
      return true;
    } catch (error: unknown) {
      const message =
        error instanceof Error
          ? error.message
          : "Erro de conexão ao consultar ingestão.";
      setLoadError(message);
      return true;
    } finally {
      setIsLoading(false);
    }
  }, [ingestionId]);

  useEffect(() => {
    let cancelled = false;

    const poll = async () => {
      const shouldContinue = await fetchIngestion();
      if (!cancelled && shouldContinue) {
        pollingRef.current = setTimeout(poll, POLL_INTERVAL_MS);
      }
    };

    poll();

    return () => {
      cancelled = true;
      stopPolling();
    };
  }, [fetchIngestion, stopPolling]);

  /* ── Derived values ─────────────────────────────────────────────── */
  const polars = ingestion?.polars_calculations;
  const accuracyScore =
    ingestion?.accuracy_score ?? ingestion?.validation_metrics?.accuracy_score;
  const operationLevel = ingestion?.status ?? "AWAITING";
  const vplMape =
    ingestion?.validation_metrics?.step_2_impact?.details?.vpl_mape;
  const currentStep = getPipelineStep(operationLevel);
  const isTerminal = TERMINAL_STATUSES.includes(operationLevel);
  const isSuccess = operationLevel === "AUTONOMOUS_SENTENCED";

  const varianceRows: VarianceRow[] =
    ingestion?.validation_metrics?.step_1_inputs?.details?.numeric_errors?.map(
      (err: any) => ({
        field: err.field,
        ai_value: err.ai,
        golden_value: err.golden,
        mape: `${(err.mape * 100).toFixed(1)}%`,
        status: err.mape <= 0.05 ? "PASS" : "FAIL",
      }),
    ) || [];

  /* ── Status color ───────────────────────────────────────────────── */
  const statusColor = isSuccess
    ? "bg-emerald-500"
    : operationLevel === "PENDING_HUMAN_AUDIT"
      ? "bg-amber-500 animate-pulse"
      : operationLevel === "KILLED" || operationLevel === "FAILED"
        ? "bg-red-500"
        : "bg-cyan-500 animate-pulse";

  const scoreColor =
    (accuracyScore ?? 0) >= 92
      ? "text-emerald-400 border-emerald-800 bg-emerald-950"
      : (accuracyScore ?? 0) >= 85
        ? "text-amber-400 border-amber-800 bg-amber-950"
        : "text-red-400 border-red-800 bg-red-950";

  return (
    <>
      {/* Print-only styles */}
      <style jsx global>{`
        @media print {
          body {
            background: white !important;
            color: black !important;
          }
          .no-print {
            display: none !important;
          }
          .print-break {
            page-break-after: always;
          }
          * {
            color: #1a1a1a !important;
            background: white !important;
            border-color: #ccc !important;
          }
        }
      `}</style>

      <div className="min-h-screen bg-zinc-950 text-zinc-100">
        {/* ── Header Bar ─────────────────────────────────────────── */}
        <div className="border-b border-zinc-800 px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className={`w-3 h-3 rounded-none ${statusColor}`} />
            <h1 className="text-lg font-mono tracking-tight">
              AUDIT <span className="text-zinc-500">/</span>{" "}
              <span className="text-zinc-400 text-sm">
                {ingestionId?.slice(0, 8)}...
              </span>
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-zinc-500 uppercase tracking-wider">
              {operationLevel.replace(/_/g, " ")}
            </span>
            {accuracyScore != null && (
              <span
                className={`px-3 py-1 text-xs font-mono tracking-wider border ${scoreColor}`}
              >
                SCORE:{" "}
                {typeof accuracyScore === "number"
                  ? accuracyScore.toFixed(1)
                  : accuracyScore}
              </span>
            )}
          </div>
        </div>

        {/* ── Pipeline Progress Bar ──────────────────────────────── */}
        <div className="border-b border-zinc-800 px-8 py-3 no-print">
          <div className="flex items-center gap-1">
            {PIPELINE_STEPS.map((step, i) => {
              const isActive = i === currentStep && !isTerminal;
              const isDone = i < currentStep || isTerminal;
              return (
                <div key={step.key} className="flex items-center gap-1 flex-1">
                  <div
                    className={`
                      flex-1 h-1.5 rounded-none transition-all duration-500
                      ${isDone ? "bg-emerald-500" : isActive ? "bg-cyan-500 animate-pulse" : "bg-zinc-800"}
                    `}
                  />
                  <span
                    className={`text-[10px] font-mono uppercase tracking-wider whitespace-nowrap ${
                      isDone
                        ? "text-emerald-500"
                        : isActive
                          ? "text-cyan-400"
                          : "text-zinc-700"
                    }`}
                  >
                    {step.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Loading State ──────────────────────────────────────── */}
        {!isTerminal && !polars && (
          <div className="flex flex-col items-center justify-center py-24 no-print">
            <div className="relative">
              <div className="w-16 h-16 border-2 border-zinc-800 rounded-none animate-spin" />
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-3 h-3 bg-cyan-500 rounded-none animate-pulse" />
              </div>
            </div>
            <p className="mt-6 text-sm font-mono text-zinc-500 animate-pulse">
              {operationLevel === "UPLOADING"
                ? "Enviando para Supabase Storage..."
                : operationLevel === "INGESTING"
                  ? "Motor agêntico processando Data Room..."
                  : "Calculando via Polars (Diamond Core)..."}
            </p>
            <p className="mt-2 text-xs font-mono text-zinc-700">
              Polling a cada 3 segundos
            </p>
            {loadError && (
              <p className="mt-4 text-xs font-mono text-red-400">{loadError}</p>
            )}
          </div>
        )}

        {/* ── Financial Dashboard (appears when polars data arrives) */}
        {polars && (
          <>
            <div className="grid grid-cols-5 gap-px bg-zinc-800 border-b border-zinc-800">
              {/* NPV */}
              <div className="bg-zinc-950 p-6 text-center">
                <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-600 font-mono mb-2">
                  VPL (NPV)
                </p>
                <p
                  className={`text-xl font-mono ${
                    (polars.npv ?? 0) > 0 ? "text-emerald-400" : "text-red-400"
                  }`}
                >
                  {formatCurrency(polars.npv)}
                </p>
              </div>

              {/* IRR */}
              <div className="bg-zinc-950 p-6 text-center">
                <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-600 font-mono mb-2">
                  TIR (IRR)
                </p>
                <p
                  className={`text-xl font-mono ${
                    (polars.irr ?? 0) > 14.5
                      ? "text-emerald-400"
                      : "text-amber-400"
                  }`}
                >
                  {formatPct(polars.irr)}
                </p>
              </div>

              {/* ROE */}
              <div className="bg-zinc-950 p-6 text-center">
                <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-600 font-mono mb-2">
                  ROE
                </p>
                <p className="text-xl font-mono text-zinc-200">
                  {polars.roe != null ? formatPct(polars.roe * 100) : "—"}
                </p>
              </div>

              {/* Payback */}
              <div className="bg-zinc-950 p-6 text-center">
                <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-600 font-mono mb-2">
                  Payback
                </p>
                <p className="text-xl font-mono text-zinc-200">
                  {polars.payback_months != null
                    ? `${polars.payback_months} meses`
                    : "—"}
                </p>
              </div>

              {/* Score */}
              <div className="bg-zinc-950 p-6 text-center">
                <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-600 font-mono mb-2">
                  Score
                </p>
                <p
                  className={`text-xl font-mono ${
                    (accuracyScore ?? 0) >= 92
                      ? "text-emerald-400"
                      : (accuracyScore ?? 0) >= 85
                        ? "text-amber-400"
                        : "text-red-400"
                  }`}
                >
                  {accuracyScore != null
                    ? Number(accuracyScore).toFixed(1)
                    : "—"}
                </p>
              </div>
            </div>

            {/* Viability Badge */}
            <div
              className={`border-b px-8 py-3 text-center text-sm font-mono tracking-wider uppercase ${
                polars.is_viable
                  ? "bg-emerald-950/30 border-emerald-900 text-emerald-400"
                  : "bg-red-950/30 border-red-900 text-red-400"
              }`}
            >
              {polars.is_viable
                ? "✓ PROJETO VIÁVEL — TIR > WACC (GOLDEN RULE)"
                : "✗ PROJETO INVIÁVEL — TIR < WACC"}
            </div>
          </>
        )}

        {/* ── Split Screen (Data + Comparison) ──────────────────── */}
        {isTerminal && (
          <div className="grid grid-cols-2 divide-x divide-zinc-800 min-h-[50vh]">
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

              {ingestion?.llm_extracted_payload ? (
                <pre className="text-xs font-mono text-zinc-400 bg-zinc-900 border border-zinc-800 p-4 overflow-auto max-h-[50vh] whitespace-pre-wrap">
                  {JSON.stringify(ingestion.llm_extracted_payload, null, 2)}
                </pre>
              ) : (
                <div className="text-sm text-zinc-600 font-mono border border-zinc-800 p-8 text-center">
                  Nenhum dado extraído disponível.
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
        )}

        {/* ── Action Bar ──────────────────────────────────────────── */}
        <div className="fixed bottom-0 left-0 right-0 border-t border-zinc-800 bg-zinc-950/95 backdrop-blur px-8 py-4 flex items-center justify-between no-print">
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-zinc-600">
              {ingestionId}
            </span>
            {polars && (
              <span className="text-xs font-mono text-zinc-700">
                WACC:{" "}
                {formatPct(polars.wacc_used ? polars.wacc_used * 100 : null)} |{" "}
                Units: {polars.total_units ?? "—"}
              </span>
            )}
          </div>

          <div className="flex items-center gap-4">
            <button
              className="
                px-8 py-3 text-xs font-mono uppercase tracking-[0.2em]
                bg-rose-950 text-rose-400 border border-rose-800
                hover:bg-rose-900 transition-colors
              "
              onClick={() => {
                alert("Enviado para auditoria manual");
              }}
            >
              Auditoria Manual
            </button>

            <button
              className="
                px-8 py-3 text-xs font-mono uppercase tracking-[0.2em]
                bg-zinc-800 text-zinc-300 border border-zinc-700
                hover:bg-zinc-700 transition-colors
              "
              disabled={!isTerminal}
              onClick={() => window.print()}
            >
              Exportar Sentença (PDF)
            </button>

            <button
              className="
                px-8 py-3 text-xs font-mono uppercase tracking-[0.2em]
                bg-emerald-600 text-white
                hover:bg-emerald-500 transition-colors
              "
              disabled={operationLevel === "KILLED" || !isTerminal}
              onClick={() => {
                alert("Projeto sentenciado — VPL registrado");
              }}
            >
              Confirmar Sentença
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
