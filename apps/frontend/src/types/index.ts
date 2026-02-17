/**
 * VERTIV v6.0 - Type Exports
 *
 * Central hub para tipos da API.
 *
 * Uso:
 *   import type { ProjectTIV, SimulationResponse } from '@/types';
 */

// Re-export generated types
export type {
  components,
  paths,
  operations
} from './api.generated';

// Helper type para extrair schemas
import type { components } from './api.generated';

type Schemas = components['schemas'];

// Export individual schema types for convenience
export type ProjectTIV = Schemas['ProjectTIV'];
export type SimulationResponse = Schemas['SimulationResponse'];
export type P1GarimpoInput = Schemas['P1GarimpoInput'];
export type P1GarimpoOutput = Schemas['P1GarimpoOutput'];
// V7: Wizard-specific types removed (P2Request, P4Request, P5Request)

// Enum types
export type SimulationStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
export type GoNoGoDecision = 'GO' | 'CAUTION' | 'NO_GO';
export type MarketCyclePhase = 'RECOVERY' | 'EXPANSION' | 'DECELERATION' | 'RECESSION';

// Utility type for API responses
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

// SSE Event types
export interface SSEStatusEvent {
  simulation_id: string;
  status: SimulationStatus;
  elapsed_seconds: number;
}

export interface SSECompletedEvent extends SSEStatusEvent {
  result: unknown;
}

export interface SSEFailedEvent extends SSEStatusEvent {
  error: string;
}
