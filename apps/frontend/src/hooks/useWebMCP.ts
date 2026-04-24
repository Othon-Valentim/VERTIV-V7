/**
 * VERTIV V7 — useWebMCP React Hook
 *
 * Manages the full WebMCP lifecycle:
 *  1. MOUNT:   Detects navigator.modelContext, fetches tool catalog, registers tools
 *  2. CONTEXT: Provides project_id, current_vpl, role to the agent
 *  3. ROUTE:   Unregisters old tools, registers new ones based on active view
 *  4. UNMOUNT: clearContext() + unregisterTool() all — zero memory leaks
 *
 * The hook toggles CSS classes on target elements for the Shared Interface:
 *  - `.webmcp-active`      → static cyan border when agent is connected
 *  - `.webmcp-processing`  → pulsing animation while a tool callback executes
 *
 * Usage:
 *   const { isSupported, isActive, registeredTools, isProcessing } = useWebMCP({
 *     projectId: "abc-123",
 *     currentVpl: 1_500_000,
 *     role: "ANALYST",
 *     activeStep: "P10",
 *   });
 */

"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { api } from "@/lib/api-client";
import { bindToolCallbacks } from "@/lib/webmcp-tools";
import type {
  WebMCPState,
  WebMCPContext,
  WebMCPToolDefinition,
  WebMCPCatalogResponse,
} from "@/lib/webmcp-types";

const WEBMCP_ENABLED = process.env.NEXT_PUBLIC_WEBMCP_ENABLED === "true";

// ── Hook Configuration ─────────────────────────────────────────────────────

interface UseWebMCPOptions {
  /** Project ID for context injection */
  projectId?: string;
  /** Current VPL value (from the Diamond Core calculation) */
  currentVpl?: number;
  /** Current IRR value */
  currentIrr?: number;
  /** User role: ANALYST | DIRECTOR | ADMIN */
  role?: string;
  /** Active step in the Cockpit (P1, P5, P10, etc.) */
  activeStep?: string;
  /** CSS selector for elements that should glow during agent activity */
  targetSelector?: string;
  /** Whether to enable the hook (useful for feature flags) */
  enabled?: boolean;
}

// ── Tool filtering by active step ──────────────────────────────────────────

const STEP_TOOL_MAP: Record<string, string[]> = {
  // Financial view → simulation tools
  P10: ["simulate_what_if", "approve_capital_sentence"],
  P3: ["simulate_what_if"],
  // Legal view → legal tools
  P5: ["override_legal_flag", "highlight_pdf_evidence", "register_kill_reason"],
  // General audit view → all except approval
  AUDIT: ["simulate_what_if", "highlight_pdf_evidence", "register_kill_reason"],
  // Default → all tools
  ALL: [],
};

function filterToolsByStep(
  tools: WebMCPToolDefinition[],
  activeStep?: string,
): WebMCPToolDefinition[] {
  if (!activeStep) return tools;

  const allowedNames = STEP_TOOL_MAP[activeStep.toUpperCase()];

  // If step is not in the map or has empty array, return all tools
  if (!allowedNames || allowedNames.length === 0) return tools;

  return tools.filter((t) => allowedNames.includes(t.name));
}

// ── The Hook ───────────────────────────────────────────────────────────────

export function useWebMCP(options: UseWebMCPOptions = {}): WebMCPState {
  const {
    projectId,
    currentVpl,
    currentIrr,
    role,
    activeStep,
    targetSelector = "[data-webmcp-target]",
    enabled = WEBMCP_ENABLED,
  } = options;

  const [state, setState] = useState<WebMCPState>({
    isSupported: false,
    isActive: false,
    registeredTools: [],
    isProcessing: false,
    activeToolName: null,
    error: null,
  });

  // Track registered tool names for cleanup
  const registeredRef = useRef<string[]>([]);
  const catalogRef = useRef<WebMCPToolDefinition[]>([]);

  // ── CSS Class Management ───────────────────────────────────────────────

  const setActiveCSS = useCallback(
    (active: boolean, processing: boolean = false) => {
      if (typeof document === "undefined") return;
      const targets = document.querySelectorAll(targetSelector);
      targets.forEach((el) => {
        if (active) {
          el.classList.add("webmcp-active");
        } else {
          el.classList.remove("webmcp-active");
        }
        if (processing) {
          el.classList.add("webmcp-processing");
        } else {
          el.classList.remove("webmcp-processing");
        }
      });
    },
    [targetSelector],
  );

  // ── Core: Register Tools ───────────────────────────────────────────────

  const registerTools = useCallback(
    (tools: WebMCPToolDefinition[]) => {
      const mc = navigator.modelContext;
      if (!mc) return;

      // Unregister old tools first
      registeredRef.current.forEach((name) => {
        try {
          mc.unregisterTool(name);
        } catch {
          // Tool may not exist, ignore
        }
      });

      // Wrap callbacks with processing state management
      const wrappedTools = tools.map((tool) => ({
        ...tool,
        callback: async (input: Record<string, unknown>) => {
          setState((s) => ({
            ...s,
            isProcessing: true,
            activeToolName: tool.name,
          }));
          setActiveCSS(true, true);

          try {
            const result = tool.callback
              ? await tool.callback(input)
              : { error: "No callback bound" };
            return result;
          } finally {
            setState((s) => ({
              ...s,
              isProcessing: false,
              activeToolName: null,
            }));
            setActiveCSS(true, false);
          }
        },
      }));

      // Register each tool
      const registered: string[] = [];
      wrappedTools.forEach((tool) => {
        try {
          mc.registerTool(tool);
          registered.push(tool.name);
        } catch (err) {
          console.error(`[WebMCP] Failed to register tool: ${tool.name}`, err);
        }
      });

      registeredRef.current = registered;
      setState((s) => ({
        ...s,
        isActive: registered.length > 0,
        registeredTools: registered,
      }));
      setActiveCSS(registered.length > 0);

      console.log(
        `[WebMCP] Registered ${registered.length} tools:`,
        registered,
      );
    },
    [setActiveCSS],
  );

  // ── Effect: Initialize WebMCP on mount ─────────────────────────────────

  useEffect(() => {
    if (!enabled) return;

    // V7.0 Graceful Degradation — Rigorous feature detection.
    // Silent fallback: no console noise, no errors, no network calls.
    // WebMCP (V7.1) is isolated behind this gate.
    const isSupported =
      typeof window !== "undefined" &&
      "navigator" in window &&
      "modelContext" in navigator;

    setState((s) => ({ ...s, isSupported }));

    if (!isSupported) {
      // Silent no-op: Cockpit loads perfectly for Chrome/Safari/Firefox.
      // WebMCP activates only on Chrome 146+ with experimental flag.
      return;
    }

    // Fetch tool catalog from backend
    let cancelled = false;

    async function initWebMCP() {
      try {
        const res = await api.get("/api/v7/webmcp/schemas");
        if (!res.ok) throw new Error(`Catalog fetch failed: ${res.status}`);

        const catalog: WebMCPCatalogResponse = await res.json();
        const toolsWithCallbacks = bindToolCallbacks(catalog.tools);

        if (cancelled) return;

        catalogRef.current = toolsWithCallbacks;

        // Filter by active step and register
        const filtered = filterToolsByStep(toolsWithCallbacks, activeStep);
        registerTools(filtered);
      } catch (err) {
        if (cancelled) return;
        const message =
          err instanceof Error ? err.message : "Unknown WebMCP init error";
        console.error("[WebMCP] Init failed:", message);
        setState((s) => ({ ...s, error: message }));
      }
    }

    initWebMCP();

    // Cleanup on unmount
    return () => {
      cancelled = true;
      const mc = navigator.modelContext;
      if (mc) {
        registeredRef.current.forEach((name) => {
          try {
            mc.unregisterTool(name);
          } catch {
            // Ignore
          }
        });
        try {
          mc.clearContext();
        } catch {
          // Ignore
        }
      }
      registeredRef.current = [];
      setActiveCSS(false);
      console.log("[WebMCP] Cleanup complete — all tools unregistered.");
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled]);

  // ── Effect: Re-register tools when activeStep changes ──────────────────

  useEffect(() => {
    if (!state.isSupported || catalogRef.current.length === 0) return;

    const filtered = filterToolsByStep(catalogRef.current, activeStep);
    registerTools(filtered);
  }, [activeStep, state.isSupported, registerTools]);

  // ── Effect: Provide context to the agent ───────────────────────────────

  useEffect(() => {
    if (!state.isSupported) return;

    const mc = navigator.modelContext;
    if (!mc) return;

    const context: WebMCPContext = {
      project_id: projectId,
      current_vpl: currentVpl,
      current_irr: currentIrr,
      role: role,
      active_step: activeStep,
    };

    // Strip undefined values
    const cleanContext = Object.fromEntries(
      Object.entries(context).filter(([, v]) => v !== undefined),
    );

    try {
      mc.provideContext(cleanContext);
      console.log("[WebMCP] Context provided:", cleanContext);
    } catch (err) {
      console.error("[WebMCP] Failed to provide context:", err);
    }
  }, [projectId, currentVpl, currentIrr, role, activeStep, state.isSupported]);

  return state;
}

export default useWebMCP;
