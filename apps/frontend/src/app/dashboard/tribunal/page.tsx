"use client";

import React from 'react';
import { TribunalView } from "@/components/tribunal/TribunalView";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Scale, History, Plus, Sparkles } from "lucide-react";

export default function TribunalPage() {
    return (
        <div className="flex flex-col gap-8 p-6 lg:p-8 min-h-screen bg-background text-foreground">
            {/* Header */}
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 animate-fade-in">
                <div className="space-y-1">
                    <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-xl gradient-primary flex items-center justify-center">
                            <Scale className="h-5 w-5 text-white" />
                        </div>
                        <div className="flex items-center gap-3">
                            <h1 className="text-2xl lg:text-3xl font-bold tracking-tight">
                                Tribunal de Agentes
                            </h1>
                            <Badge
                                variant="outline"
                                className="bg-accent/10 text-accent border-accent/20 font-medium"
                            >
                                <Sparkles className="h-3 w-3 mr-1" />
                                Alpha
                            </Badge>
                        </div>
                    </div>
                    <p className="text-muted-foreground ml-13">
                        Sistema de Decisão Adversarial com múltiplos agentes de IA
                    </p>
                </div>
                <div className="flex gap-3 self-start lg:self-auto">
                    <Button
                        variant="outline"
                        className="rounded-full gap-2"
                    >
                        <History className="h-4 w-4" />
                        Consultar Histórico
                    </Button>
                    <Button className="btn-pill btn-primary gap-2">
                        <Plus className="h-4 w-4" />
                        Nova Sessão
                    </Button>
                </div>
            </div>

            {/* Tribunal View */}
            <div className="animate-slide-up">
                <TribunalView />
            </div>

            {/* Footer */}
            <div className="border-t border-border pt-6 mt-auto">
                <p className="text-xs text-muted-foreground text-center">
                    VERTIV Global Real Estate Intelligence Platform v6.1.0 | Adversarial Decision System
                </p>
            </div>
        </div>
    );
}
