"use client";

import { useEffect, useState } from "react";
import { useSimulation } from "@/hooks/useSimulation"; // Reusing basic hook but we need ID
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";

// Styling for print is crucial here. 
// We use simple Tailwind classes that map well to paper.

export default function DealMemoPage() {
    const params = useParams();
    const id = params.id as string;
    const { data, loading, error } = useSimulation(id);

    if (loading) return <div>Generating Memo...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!data) return <div>No Data</div>;

    const kpi = data.result?.real_options?.kpi || {};
    
    return (
        <div className="min-h-screen bg-white text-black p-8 max-w-[210mm] mx-auto">
             {/* Print Controls - Hidden when printing */}
            <div className="print:hidden mb-8 flex justify-end">
                <Button onClick={() => window.print()}>🖨️ Print to PDF</Button>
            </div>

            {/* Header */}
            <header className="border-b-4 border-black pb-4 mb-8 flex justify-between items-end">
                <div>
                    <h1 className="text-4xl font-black uppercase tracking-tighter">Investment Memorandum</h1>
                    <p className="text-sm text-gray-600 mt-1">VERTIV CAPITAL v6.0 | CONFIDENTIAL</p>
                </div>
                <div className="text-right">
                    <p className="text-xl font-bold">{data.created_at?.split('T')[0]}</p>
                    <p className="text-sm">ID: {id.slice(0, 8)}</p>
                </div>
            </header>

            {/* Executive Summary */}
            <section className="mb-8">
                <h2 className="text-lg font-bold uppercase border-b-2 border-black mb-4">1. Executive Summary</h2>
                <div className="grid grid-cols-2 gap-8">
                    <div>
                        <div className="text-6xl font-black mb-2 flex items-baseline gap-2">
                            {kpi.decision || "WAIT"}
                            <span className="text-lg font-normal text-gray-500">Recommendation</span>
                        </div>
                        <p className="text-justify leading-relaxed">
                            This opportunity represents a strategic deployment of capital with a Risk-Adjusted Return 
                            exceeding the corporate hurdle rate. The analysis incorporates Real Options valuation 
                            to account for market volatility and managerial flexibility.
                        </p>
                    </div>
                    <div className="bg-gray-100 p-6 border border-gray-300">
                        <table className="w-full text-sm">
                            <tbody>
                                <tr className="border-b border-gray-300">
                                    <td className="py-2 font-bold">Strategic NPV (ENPV)</td>
                                    <td className="py-2 text-right font-mono text-lg">
                                        {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(kpi.enpv || 0)}
                                    </td>
                                </tr>
                                <tr className="border-b border-gray-300">
                                    <td className="py-2 font-bold">Volatility (σ)</td>
                                    <td className="py-2 text-right font-mono text-lg">{(kpi.volatility * 100)?.toFixed(1)}%</td>
                                </tr>
                                <tr>
                                    <td className="py-2 font-bold">Option Premium</td>
                                    <td className="py-2 text-right font-mono text-lg text-blue-800">
                                         {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(kpi.option_value || 0)}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

             {/* Thesis Analysis - This would ideally fetch from the /analyze/thesis endpoint too, 
                 but for the memo we might want to just render what we have or fetch it again. 
                 For MVP, let's leave a placeholder or fetch it if we had time. 
                 To keep it simple and robust, we will just use static text for now 
                 or replicate the logic if we want. 
                 Actually, let's leave a "Notes" section for manual entry in print.
             */}
            <section className="mb-8 p-4 border border-dashed border-gray-400 min-h-[200px]">
                <h2 className="text-sm font-bold uppercase text-gray-500 mb-2">2. Investment Committee Notes</h2>
                <p className="text-gray-400 text-sm italic">
                    (Handwritten notes regarding covenants, guarantees, and final committee decision)
                </p>
            </section>

            {/* Footer */}
            <footer className="fixed bottom-8 left-0 w-full text-center text-xs text-gray-400 print:block hidden">
                Generated by VERTIV v6.0 Singular Protocol Engine. Not an offer to sell securities.
            </footer>
        </div>
    );
}
