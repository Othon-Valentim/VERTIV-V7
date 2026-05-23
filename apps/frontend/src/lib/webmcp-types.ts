/**
 * VERTIV V7 — WebMCP Type Definitions
 *
 * TypeScript declarations for the navigator.modelContext API surface (W3C Draft, Chrome 146+).
 * These types mirror the WebMCP specification for imperative tool registration.
 *
 * IMPORTANT: This API is experimental. Feature-detect before use:
 *   if ('modelContext' in navigator) { ... }
 */

// ── JSON Schema Types ──────────────────────────────────────────────────────

export interface JSONSchema {
  $schema?: string;
  type?: string;
  properties?: Record<string, JSONSchema>;
  required?: string[];
  description?: string;
  title?: string;
  enum?: (string | number | boolean)[];
  items?: JSONSchema;
  $defs?: Record<string, JSONSchema>;
  format?: string;
  anyOf?: JSONSchema[];
  [key: string]: unknown;
}

// ── WebMCP Tool Definition ─────────────────────────────────────────────────

export interface WebMCPToolDefinition {
  /** Unique tool identifier (e.g. "simulate_what_if") */
  name: string;
  /** Human/LLM-readable description of what the tool does */
  description: string;
  /** JSON Schema for the tool's input payload */
  inputSchema: JSONSchema;
  /** JSON Schema for the tool's output payload */
  outputSchema?: JSONSchema;
  /** Risk level classification */
  riskLevel?: "LOW" | "MEDIUM" | "HIGH" | "FATAL";
  /**
   * If true, the browser freezes the agent and shows a native popup
   * requiring a physical mouse click before execution.
   * MANDATORY for destructive/financial actions.
   */
  requestUserInteraction?: boolean;
  /** The callback function invoked when the agent triggers this tool */
  callback?: (
    input: Record<string, unknown>,
  ) => Promise<Record<string, unknown>>;
}

// ── WebMCP Context ─────────────────────────────────────────────────────────

export interface WebMCPContext {
  /** Current project identifier */
  project_id?: string;
  /** Current calculated VPL */
  current_vpl?: number;
  /** Current calculated IRR */
  current_irr?: number;
  /** User role (ANALYST, DIRECTOR, ADMIN) */
  role?: string;
  /** Active step in the Cockpit (P1, P5, P10, etc.) */
  active_step?: string;
}

// ── navigator.modelContext API Surface ─────────────────────────────────────

export interface ModelContextAPI {
  /**
   * Register a tool with the browser's agent runtime.
   * The agent can discover and invoke this tool via JSON Schema.
   */
  registerTool(tool: WebMCPToolDefinition): void;

  /**
   * Unregister a previously registered tool by name.
   * Call on unmount or route change to prevent memory leaks.
   */
  unregisterTool(name: string): void;

  /**
   * Provide situational context to the agent.
   * Keep minimal: only project_id, VPL, role, active_step.
   */
  provideContext(context: WebMCPContext): void;

  /**
   * Clear all provided context.
   * Call on tab close or route change.
   */
  clearContext(): void;
}

// ── Extend the Navigator interface ─────────────────────────────────────────

declare global {
  interface Navigator {
    /**
     * WebMCP Model Context API (Chrome 146+, W3C Draft).
     * Only available when the experimental flag is enabled.
     */
    modelContext?: ModelContextAPI;
  }
}

// ── Backend Tool Catalog Response ──────────────────────────────────────────

export interface WebMCPCatalogResponse {
  version: string;
  protocol: string;
  tools: WebMCPToolDefinition[];
  context_policy: {
    max_fields: number;
    allowed_fields: string[];
  };
}

// ── WebMCP Hook State ──────────────────────────────────────────────────────

export interface WebMCPState {
  /** Whether navigator.modelContext is available */
  isSupported: boolean;
  /** Whether tools are currently registered */
  isActive: boolean;
  /** List of currently registered tool names */
  registeredTools: string[];
  /** Whether a tool callback is currently executing */
  isProcessing: boolean;
  /** Name of the tool currently being processed */
  activeToolName: string | null;
  /** Error state */
  error: string | null;
}

export type WebMCPOriginHeader = { "X-WebMCP-Origin": "agent" };
