
import React from 'react';
import { TribunalCard } from './TribunalCard';

export function TribunalView() {
    // MOCK DATA - In Prod, fetch from Backend Agent Swarm
    const agents = {
        blue: {
            role: 'BLUE' as const,
            name: "Agente Optimus",
            title: "Diretor Comercial",
            argument: "O ciclo de mercado local está em fase inicial de recuperação (Sinal Verde). A demanda represada por tickets médios (R$ 400k) é massiva, como mostram os dados de absorção do concorrente 'Jardins'. O VSO projetado de 12% a.m. é conservador. É um 'Home Run' claro.",
            confidence: 92
        },
        red: {
            role: 'RED' as const,
            name: "Agente Cpt. Risk",
            title: "Officer de Risco",
            argument: "Cuidado. A liquidez do mercado secundário está travada. O CUB subiu 8% no último semestre, pressionando a margem. Além disso, o licenciamento ambiental na região da 'Mata Atlântica' tem histórico de atrasos de 18 meses. O risco de capex estourar é real.",
            confidence: 85
        },
        gold: {
            role: 'GOLD' as const,
            name: "The Architect",
            title: "Sintetizador Executivo",
            argument: "Embora o risco de licenciamento (Red) seja válido, ele pode ser mitigado via 'Real Options' (Land Banking com opção de abandono). O potencial de vendas (Blue) justifica a exposição. RECOMENDAÇÃO: Aprove o projeto, mas trave o Capex com contrato turn-key e adicione 6 meses de buffer no cronograma.",
            confidence: 89
        }
    };

    return (
        <div className="space-y-8 p-6 bg-black/40 rounded-xl border border-white/5 backdrop-blur-sm">
            <div className="text-center space-y-2 mb-8">
                <h2 className="text-3xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-yellow-200 to-red-400">
                    O TRIBUNAL
                </h2>
                <p className="text-muted-foreground text-sm uppercase tracking-[0.2em]">
                    Inteligência Adversarial Sintética
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* BLUE vs RED */}
                <div className="space-y-2">
                    <span className="text-xs font-mono text-blue-400 opacity-50 ml-1">TESE (BULL)</span>
                    <TribunalCard {...agents.blue} />
                </div>
                <div className="space-y-2">
                     <span className="text-xs font-mono text-red-400 opacity-50 ml-1">ANTÍTESE (BEAR)</span>
                    <TribunalCard {...agents.red} />
                </div>
            </div>

            {/* GOLD - The Synthesis */}
            <div className="relative mt-12 pt-8">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-background px-4 py-1 rounded-full border border-yellow-500/30 text-yellow-500 text-xs font-mono font-bold">
                    SÍNTESE FINAL
                </div>
                <div className="border-t border-dashed border-white/10 absolute top-0 left-0 right-0" />
                
                <div className="max-w-3xl mx-auto transform hover:scale-[1.01] transition-all duration-500">
                    <TribunalCard {...agents.gold} />
                </div>
            </div>
        </div>
    );
}
