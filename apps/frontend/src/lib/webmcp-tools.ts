/**
 * VERTIV V7 — WebMCP Tool Callbacks
 *
 * Imperative tool implementations for the Agentic Cockpit.
 * Each tool callback receives validated JSON from the browser agent,
 * POSTs to the FastAPI backend, and returns the result.
 *
 * CRITICAL: The AI is a courier. ALL math is computed by Polars on the backend.
 * These callbacks never calculate anything — they transport JSON.
 */

import { api } from "./api-client";
import type { WebMCPToolDefinition } from "./webmcp-types";

// ── Callback: simulate_what_if ─────────────────────────────────────────────

async function simulateWhatIf(
  input: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  const res = await api.post(
    "/calculate/quick",
    {
      id: input.project_id as string,
      name: "WebMCP What-If Simulation",
      municipality: "São Paulo",
      financial_input: {
        total_units: input.total_units,
        sales_price_avg: input.sales_price_avg,
        construction_cost_total: input.construction_cost_total,
        land_cost: input.land_cost,
        development_months: input.development_months,
        incc_annual_rate: input.incc_annual_rate,
        ipca_annual_rate: input.ipca_annual_rate,
      },
    },
    {
      headers: { "X-WebMCP-Origin": "agent" },
    },
  );

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Backend error" }));
    throw new Error(err.detail || `Backend returned ${res.status}`);
  }

  const data = await res.json();
  return {
    simulation_id: data.simulation_id,
    status: data.status,
    new_vpl: data.result?.npv ?? null,
    new_irr: data.result?.irr ?? null,
    new_roe: data.result?.roe ?? null,
    payback_months: data.result?.payback_months ?? null,
    exposure_max: data.result?.exposure_max ?? null,
  };
}

// ── Callback: highlight_pdf_evidence ───────────────────────────────────────

async function highlightPdfEvidence(
  input: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  const page = input.page as number;
  const exactText = input.exact_text as string;

  // Dispatch a custom DOM event that the PDF viewer component will listen to
  const event = new CustomEvent("vertiv:highlight-pdf", {
    detail: { page, exactText },
  });
  window.dispatchEvent(event);

  return { success: true };
}

// ── Callback: register_kill_reason ─────────────────────────────────────────

async function registerKillReason(
  input: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  const res = await api.post(
    "/api/v7/kill-reasons",
    {
      category: input.category,
      citation: input.citation,
      source_document: input.source_document || null,
      page_number: input.page_number || null,
    },
    {
      headers: { "X-WebMCP-Origin": "agent" },
    },
  );

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Backend error" }));
    throw new Error(err.detail || `Backend returned ${res.status}`);
  }

  const data = await res.json();
  return { saved_id: data.id };
}

// ── Callback: override_legal_flag ──────────────────────────────────────────

async function overrideLegalFlag(
  input: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  const res = await api.put(
    "/api/v7/legal/override",
    {
      has_contamination: input.has_contamination,
      has_liens: input.has_liens,
      has_adverse_possession: input.has_adverse_possession,
      justification: input.justification,
    },
    {
      headers: { "X-WebMCP-Origin": "agent" },
    },
  );

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Backend error" }));
    throw new Error(err.detail || `Backend returned ${res.status}`);
  }

  return { updated: true };
}

// ── Callback: approve_capital_sentence ──────────────────────────────────────

async function approveCapitalSentence(
  input: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  const res = await api.post(
    "/api/v7/sentence/approve",
    {
      project_id: input.project_id,
    },
    {
      headers: { "X-WebMCP-Origin": "agent" },
    },
  );

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Backend error" }));
    throw new Error(err.detail || `Backend returned ${res.status}`);
  }

  return { status: "GO" };
}

// ── Callback Registry ──────────────────────────────────────────────────────

type ToolCallback = (
  input: Record<string, unknown>,
) => Promise<Record<string, unknown>>;

const TOOL_CALLBACKS: Record<string, ToolCallback> = {
  simulate_what_if: simulateWhatIf,
  highlight_pdf_evidence: highlightPdfEvidence,
  register_kill_reason: registerKillReason,
  override_legal_flag: overrideLegalFlag,
  approve_capital_sentence: approveCapitalSentence,
};

/**
 * Get the callback function for a given tool name.
 * Returns undefined if the tool is not found.
 */
export function getToolCallback(toolName: string): ToolCallback | undefined {
  return TOOL_CALLBACKS[toolName];
}

/**
 * Bind callbacks to a tool definition array from the backend catalog.
 * Returns the tools with their `callback` property set.
 */
export function bindToolCallbacks(
  tools: WebMCPToolDefinition[],
): WebMCPToolDefinition[] {
  return tools.map((tool) => ({
    ...tool,
    callback: TOOL_CALLBACKS[tool.name],
  }));
}
