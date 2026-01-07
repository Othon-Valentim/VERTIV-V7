
import { useState, useEffect } from 'react';

type SimulationStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';

interface SimulationResult {
    simulation_id: string;
    status: SimulationStatus;
    result?: any;
    error?: string;
}

export function useSimulationStatus(simulationId: string | null) {
    const [status, setStatus] = useState<SimulationStatus | null>(null);
    const [result, setResult] = useState<any | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isPolling, setIsPolling] = useState(false);

    useEffect(() => {
        if (!simulationId) return;

        let intervalId: NodeJS.Timeout | undefined;
        setIsPolling(true);

        const checkStatus = async () => {
            try {
                if (!process.env.NEXT_PUBLIC_API_URL) {
                     throw new Error("NEXT_PUBLIC_API_URL not set");
                }
                
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/simulation/${simulationId}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                
                if (data.status === 'COMPLETED') {
                     setStatus('COMPLETED');
                     setResult(data.result);
                     setIsPolling(false);
                } else if (data.status === 'FAILED') {
                     setStatus('FAILED');
                     setError(data.error || "Simulation Failed");
                     setIsPolling(false);
                } else {
                     setStatus('PENDING'); // Keep polling
                }

            } catch (err) {
                console.error("Polling Error:", err);
                // Don't stop polling on transient errors immediately? 
                // For now, let's keep retrying unless it's a 404/500 persistent.
                // But simplified:
                // setError(String(err));
                // setStatus('FAILED');
                // setIsPolling(false);
            }
        };

        checkStatus(); // Initial check
        
        // Poll every 3 seconds
        intervalId = setInterval(() => {
             if (status !== 'COMPLETED' && status !== 'FAILED') {
                 checkStatus();
             }
        }, 3000);

        return () => {
             if (intervalId) clearInterval(intervalId);
        };
    }, [simulationId]);

    return { status, result, error, isPolling };
}
