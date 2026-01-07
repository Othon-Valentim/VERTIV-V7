import { create } from 'zustand';
import { P1GarimpoInput, P1GarimpoOutput } from '@vertiv/shared/types';

interface WizardState {
  currentStep: number;
  
  // P1 Data
  p1Input: Partial<P1GarimpoInput>;
  p1Output: P1GarimpoOutput | null;

  // Actions
  setStep: (step: number) => void;
  setP1Input: (input: Partial<P1GarimpoInput>) => void;
  setP1Output: (output: P1GarimpoOutput) => void;
}

export const useWizardStore = create<WizardState>((set) => ({
  currentStep: 0,
  
  p1Input: {},
  p1Output: null,

  setStep: (step) => set({ currentStep: step }),
  setP1Input: (input) => set((state) => ({ p1Input: { ...state.p1Input, ...input } })),
  setP1Output: (output) => set({ p1Output: output }),
}));
