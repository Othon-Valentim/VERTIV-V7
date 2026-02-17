import { useState, useEffect } from 'react';
import { api } from '@/lib/api-client';


export interface SimulationResult {
  id: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  result?: any; // We can type this strictly if we share types with backend
  error?: string;
  created_at: string;
}

export function useSimulation(simulationId: string | null) {
  const [data, setData] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!simulationId) return;

    const fetchSimulation = async () => {
      setLoading(true);
      try {
        const res = await api.get(`/simulation/${simulationId}`);
        
        if (!res.ok) {
          throw new Error(`Failed to fetch simulation: ${res.statusText}`);
        }

        const result = await res.json();
        setData(result);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSimulation();
    
    // Optional: Polling if status is PENDING/PROCESSING
    // For dashboard view, we usually assume we are looking at a completed one, 
    // but if we land here from the wizard, polling might be handled by the wizard step.
    // For now, simple fetch is enough for the "Dashboard Wiring" task.
    
  }, [simulationId]);

  return { data, loading, error };
}

export function useLatestSimulation() {
  const [data, setData] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLatest = async () => {
      setLoading(true);
      try {
        const res = await api.get(`/simulations/recent?limit=1`);
        if (!res.ok) throw new Error("Failed to fetch recent simulations");
        
        const list = await res.json();
        if (list && list.length > 0) {
            // The list item might need mapping if structure differs, but assuming it matches SimulationResult partially
            // However, the list endpoint returns the DB row. 
            // The simulation endpoint returns a specific Pydantic model structure. 
            // Let's assume for now we use the ID from the list to get the full details via the other hook, 
            // OR just use the data if it's enough. 
            // The DB row has 'result' column which is JSONB.
            const latest = list[0];
            setData({
                id: latest.id,
                status: latest.status,
                result: latest.result, // This matches
                created_at: latest.created_at
            });
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLatest();
  }, []);

  return { data, loading, error };
}
