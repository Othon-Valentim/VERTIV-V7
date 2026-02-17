import { useState, useEffect, useCallback, useRef } from 'react';

type SimulationStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';

interface SSEPayload {
    simulation_id: string;
    status: SimulationStatus;
    elapsed_seconds: number;
    result?: any;
    error?: string;
}

interface UseSimulationStatusReturn {
    status: SimulationStatus | null;
    result: any | null;
    error: string | null;
    isStreaming: boolean;
    elapsedSeconds: number;
    reconnect: () => void;
}

/**
 * Hook para monitorar status de simulação via SSE (Server-Sent Events).
 *
 * Substitui o antigo polling por streaming em tempo real.
 *
 * Vantagens sobre polling:
 * - Menor latência (updates instantâneos)
 * - Menor carga no servidor (1 conexão vs N requests)
 * - Menor carga no banco de dados
 *
 * @param simulationId - ID da simulação a monitorar
 * @returns Estado da simulação em tempo real
 */
export function useSimulationStatus(simulationId: string | null): UseSimulationStatusReturn {
    const [status, setStatus] = useState<SimulationStatus | null>(null);
    const [result, setResult] = useState<any | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const [elapsedSeconds, setElapsedSeconds] = useState(0);

    const eventSourceRef = useRef<EventSource | null>(null);
    const reconnectAttempts = useRef(0);
    const maxReconnectAttempts = 3;

    const cleanup = useCallback(() => {
        if (eventSourceRef.current) {
            eventSourceRef.current.close();
            eventSourceRef.current = null;
        }
        setIsStreaming(false);
    }, []);

    const connect = useCallback(() => {
        if (!simulationId) return;

        // Limpar conexão anterior
        cleanup();

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const token = localStorage.getItem('access_token');

        // SSE não suporta headers customizados nativamente
        // Passamos o token via query param (alternativa segura para SSE)
        const url = `${apiUrl}/simulation/${simulationId}/stream?token=${token}`;

        console.log('[SSE] Connecting to stream:', simulationId);

        const eventSource = new EventSource(url);
        eventSourceRef.current = eventSource;
        setIsStreaming(true);
        setStatus('PENDING');
        reconnectAttempts.current = 0;

        // Evento: status (PENDING/PROCESSING)
        eventSource.addEventListener('status', (event: MessageEvent) => {
            try {
                const data: SSEPayload = JSON.parse(event.data);
                setStatus(data.status);
                setElapsedSeconds(data.elapsed_seconds);
                console.log('[SSE] Status update:', data.status, `(${data.elapsed_seconds}s)`);
            } catch (e) {
                console.error('[SSE] Failed to parse status event:', e);
            }
        });

        // Evento: completed
        eventSource.addEventListener('completed', (event: MessageEvent) => {
            try {
                const data: SSEPayload = JSON.parse(event.data);
                console.log('[SSE] Simulation completed!', data.elapsed_seconds, 'seconds');
                setStatus('COMPLETED');
                setResult(data.result);
                setElapsedSeconds(data.elapsed_seconds);
                cleanup();
            } catch (e) {
                console.error('[SSE] Failed to parse completed event:', e);
            }
        });

        // Evento: failed
        eventSource.addEventListener('failed', (event: MessageEvent) => {
            try {
                const data: SSEPayload = JSON.parse(event.data);
                console.log('[SSE] Simulation failed:', data.error);
                setStatus('FAILED');
                setError(data.error || 'Simulation failed');
                setElapsedSeconds(data.elapsed_seconds);
                cleanup();
            } catch (e) {
                console.error('[SSE] Failed to parse failed event:', e);
            }
        });

        // Evento: timeout
        eventSource.addEventListener('timeout', (event: MessageEvent) => {
            console.log('[SSE] Stream timeout');
            setError('Timeout: simulação demorou mais de 5 minutos');
            cleanup();
        });

        // Evento: error (do servidor)
        eventSource.addEventListener('error', (event: MessageEvent) => {
            try {
                const data = JSON.parse((event as any).data || '{}');
                console.log('[SSE] Server error:', data.error);
                setError(data.error || 'Server error');
                cleanup();
            } catch (e) {
                // Erro de conexão (não é evento do servidor)
                console.error('[SSE] Connection error:', event);

                // Tentar reconectar
                if (reconnectAttempts.current < maxReconnectAttempts) {
                    reconnectAttempts.current++;
                    console.log(`[SSE] Reconnecting... attempt ${reconnectAttempts.current}/${maxReconnectAttempts}`);
                    cleanup();
                    setTimeout(() => connect(), 2000 * reconnectAttempts.current);
                } else {
                    setError('Connection lost. Please refresh the page.');
                    cleanup();
                }
            }
        });

        // Handler nativo de erro do EventSource
        eventSource.onerror = () => {
            // Isso é chamado quando a conexão é perdida
            if (eventSource.readyState === EventSource.CLOSED) {
                console.log('[SSE] Connection closed by server');
            }
        };

    }, [simulationId, cleanup]);

    // Conectar quando simulationId mudar
    useEffect(() => {
        if (simulationId) {
            connect();
        }

        return cleanup;
    }, [simulationId, connect, cleanup]);

    // Função para reconectar manualmente
    const reconnect = useCallback(() => {
        reconnectAttempts.current = 0;
        setError(null);
        connect();
    }, [connect]);

    return {
        status,
        result,
        error,
        isStreaming,
        elapsedSeconds,
        reconnect
    };
}

/**
 * Hook legado para compatibilidade (alias)
 * @deprecated Use useSimulationStatus
 */
export const useSimulationPolling = useSimulationStatus;
