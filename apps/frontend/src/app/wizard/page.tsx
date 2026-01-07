"use client";

import { useState, useEffect, useCallback, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  CheckCircle,
  Loader2,
  Save,
  FolderOpen,
  Plus,
  Trash2,
  ChevronLeft,
  ChevronRight,
  Building2,
  X,
  FileText,
  Clock,
  Sparkles
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { analysesService, Analysis, AnalysisData } from "@/lib/analyses";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

// Step Components
import P1GarimpoStep from "@/components/wizard/steps/p1-garimpo";
import P2EconomicStep from "@/components/wizard/steps/p2-economic";
import P4VocationStep from "@/components/wizard/steps/p4-vocation";
import P5LegalStep from "@/components/wizard/steps/p5-legal";
import { P6DemandStep, P7SupplyStep, P8AbsorptionStep, P9ValidationStep } from "@/components/wizard/steps/p6-p9-market";
import P10FinancialStep from "@/components/wizard/steps/p10-financial";

// TIV Methodology Steps
const steps = [
  { id: "p1", label: "P1: Garimpo & Ciclo", description: "Screening & Market Cycle Analysis", icon: "🔍" },
  { id: "p2", label: "P2: Dinâmica Econômica", description: "BCB Live Indicators & P2i-Lead", icon: "📊" },
  { id: "p3", label: "P3: Área de Influência", description: "Isochrones & Demographics", icon: "🗺️" },
  { id: "p4", label: "P4: Vocação & Produto", description: "3-Pillar Matrix & Best Use", icon: "🏗️" },
  { id: "p5", label: "P5: Legal & Restrições", description: "Due Diligence Gate (Binary)", icon: "⚖️" },
  { id: "p6", label: "P6: Demanda Qualificada", description: "5-Stage Demand Funnel", icon: "👥" },
  { id: "p7", label: "P7: Oferta & Mercado", description: "Competitor Benchmark", icon: "🏢" },
  { id: "p8", label: "P8: Absorção (VSO)", description: "Sales Velocity Projection", icon: "📈" },
  { id: "p9", label: "P9: Convalidação 4:1", description: "Strategic Validation Gate", icon: "🎯" },
  { id: "p10", label: "P10: Modelagem Financeira", description: "DCF + Real Options (Diamond Core)", icon: "💎" },
];

function WizardContent() {
  const searchParams = useSearchParams();
  const { user } = useAuth();

  const [currentStep, setCurrentStep] = useState(0);
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());
  const [stepResults, setStepResults] = useState<Record<string, any>>({});
  const [sessionId, setSessionId] = useState<string>("");

  // Persistence state
  const [currentAnalysis, setCurrentAnalysis] = useState<Analysis | null>(null);
  const [savedAnalyses, setSavedAnalyses] = useState<Analysis[]>([]);
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [showLoadModal, setShowLoadModal] = useState(false);
  const [analysisName, setAnalysisName] = useState("");
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  // Generate session ID on mount
  useEffect(() => {
    setSessionId(Math.random().toString(36).substring(2, 10).toUpperCase());
  }, []);

  // Load analysis if ID in URL
  useEffect(() => {
    const analysisId = searchParams.get('id');
    if (analysisId && user) {
      loadAnalysis(analysisId);
    }
  }, [searchParams, user]);

  // Load saved analyses list
  useEffect(() => {
    if (user) {
      loadAnalysesList();
    }
  }, [user]);

  const loadAnalysesList = async () => {
    try {
      const analyses = await analysesService.list();
      setSavedAnalyses(analyses);
    } catch (error) {
      console.error('Erro ao carregar análises:', error);
    }
  };

  const loadAnalysis = async (id: string) => {
    setIsLoading(true);
    try {
      const analysis = await analysesService.get(id);
      if (analysis) {
        setCurrentAnalysis(analysis);
        setCurrentStep(analysis.data.currentStep);
        setCompletedSteps(new Set(analysis.data.completedSteps));
        setStepResults(analysis.data.stepResults);
        setSessionId(analysis.data.sessionId);
        setAnalysisName(analysis.name);
      }
    } catch (error) {
      console.error('Erro ao carregar análise:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getCurrentData = useCallback((): AnalysisData => ({
    currentStep,
    completedSteps: Array.from(completedSteps),
    stepResults,
    sessionId
  }), [currentStep, completedSteps, stepResults, sessionId]);

  const handleSave = async () => {
    if (!user) {
      alert('Faça login para salvar análises');
      return;
    }

    if (!currentAnalysis && !analysisName.trim()) {
      setShowSaveModal(true);
      return;
    }

    setIsSaving(true);
    try {
      const data = getCurrentData();
      const saved = await analysesService.autoSave(
        currentAnalysis?.id || null,
        analysisName || `Análise ${new Date().toLocaleDateString('pt-BR')}`,
        data
      );
      setCurrentAnalysis(saved);
      setLastSaved(new Date());
      setShowSaveModal(false);
      loadAnalysesList();
    } catch (error) {
      console.error('Erro ao salvar:', error);
      alert('Erro ao salvar análise');
    } finally {
      setIsSaving(false);
    }
  };

  const handleSaveAs = async () => {
    if (!analysisName.trim()) {
      alert('Digite um nome para a análise');
      return;
    }

    setIsSaving(true);
    try {
      const data = getCurrentData();
      const saved = await analysesService.create(analysisName, '', data);
      setCurrentAnalysis(saved);
      setLastSaved(new Date());
      setShowSaveModal(false);
      loadAnalysesList();
    } catch (error) {
      console.error('Erro ao salvar:', error);
      alert('Erro ao salvar análise');
    } finally {
      setIsSaving(false);
    }
  };

  const handleNewAnalysis = () => {
    setCurrentAnalysis(null);
    setCurrentStep(0);
    setCompletedSteps(new Set());
    setStepResults({});
    setSessionId(Math.random().toString(36).substring(2, 10).toUpperCase());
    setAnalysisName("");
    setLastSaved(null);
  };

  const handleDeleteAnalysis = async (id: string) => {
    if (!confirm('Tem certeza que deseja excluir esta análise?')) return;

    try {
      await analysesService.delete(id);
      if (currentAnalysis?.id === id) {
        handleNewAnalysis();
      }
      loadAnalysesList();
    } catch (error) {
      console.error('Erro ao excluir:', error);
      alert('Erro ao excluir análise');
    }
  };

  const handleStepComplete = (stepIndex: number, data: any) => {
    setCompletedSteps(prev => new Set([...Array.from(prev), stepIndex]));
    setStepResults(prev => ({ ...prev, [steps[stepIndex].id]: data }));
  };

  const goToNextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const goToPrevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return <P1GarimpoStep />;
      case 1:
        return (
          <P2EconomicStep
            initialMunicipality={stepResults.p1?.municipality || ""}
            onComplete={(data) => handleStepComplete(1, data)}
          />
        );
      case 2:
        return (
          <div className="space-y-6">
            <div className="border-b border-border pb-4">
              <h3 className="text-lg font-medium">Área de Influência</h3>
              <p className="text-sm text-muted-foreground">
                Definição de isócronas e análise demográfica.
              </p>
            </div>
            <div className="bg-primary/5 border border-primary/20 rounded-xl p-8 text-center">
              <div className="h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">🗺️</span>
              </div>
              <h4 className="font-semibold text-lg mb-2">Módulo de Mapeamento</h4>
              <p className="text-sm text-muted-foreground mb-6 max-w-md mx-auto">
                Este passo requer integração com API de mapas (Mapbox/Google Maps).
                Por ora, defina manualmente a população e renda da área de influência
                nos passos P6-P9.
              </p>
              <Button onClick={goToNextStep} className="btn-pill btn-primary">
                Prosseguir para P4
                <ChevronRight className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </div>
        );
      case 3:
        return <P4VocationStep />;
      case 4:
        return <P5LegalStep />;
      case 5:
        return (
          <P6DemandStep
            onComplete={(data) => handleStepComplete(5, data)}
          />
        );
      case 6:
        return (
          <P7SupplyStep
            onComplete={(data) => handleStepComplete(6, data)}
          />
        );
      case 7:
        return (
          <P8AbsorptionStep
            qualifiedDemand={stepResults.p6?.summary?.qualified_demand_units || 200}
            activeInventory={stepResults.p7?.summary?.active_inventory_units || 50}
            onComplete={(data) => handleStepComplete(7, data)}
          />
        );
      case 8:
        return (
          <P9ValidationStep
            qualifiedDemand={stepResults.p6?.summary?.qualified_demand_units || 200}
            activeInventory={stepResults.p7?.summary?.active_inventory_units || 50}
            absorptionMonths={stepResults.p8?.absorption_projection?.projected_absorption_months || 24}
            onComplete={(data) => handleStepComplete(8, data)}
          />
        );
      case 9:
        return (
          <P10FinancialStep
            onComplete={(data) => handleStepComplete(9, data)}
          />
        );
      default:
        return null;
    }
  };

  const getStepStatus = (index: number) => {
    if (completedSteps.has(index)) return "completed";
    if (index === currentStep) return "current";
    return "pending";
  };

  const progressPercentage = (completedSteps.size / 10) * 100;

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="text-center animate-fade-in">
          <div className="h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
          <p className="text-muted-foreground">Carregando análise...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      {/* Sidebar */}
      <aside className="w-80 border-r border-border bg-card/50 flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="h-11 w-11 rounded-xl gradient-primary flex items-center justify-center">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight">VERTIV.global</h1>
              <p className="text-xs text-muted-foreground">TIV Wizard - 10 Passos</p>
            </div>
          </div>
        </div>

        {/* Actions */}
        {user && (
          <div className="p-4 border-b border-border space-y-3">
            <div className="flex gap-2">
              <Button
                onClick={handleSave}
                disabled={isSaving}
                size="sm"
                className="flex-1 gap-2"
              >
                {isSaving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                Salvar
              </Button>
              <Button
                onClick={() => setShowLoadModal(true)}
                variant="outline"
                size="sm"
                className="flex-1 gap-2"
              >
                <FolderOpen className="h-4 w-4" />
                Abrir
              </Button>
            </div>
            <Button
              onClick={handleNewAnalysis}
              variant="outline"
              size="sm"
              className="w-full gap-2"
            >
              <Plus className="h-4 w-4" />
              Nova Análise
            </Button>
            {currentAnalysis && (
              <div className="text-xs text-center pt-1 space-y-1">
                <p className="text-muted-foreground truncate">{currentAnalysis.name}</p>
                {lastSaved && (
                  <p className="text-success flex items-center justify-center gap-1">
                    <CheckCircle className="h-3 w-3" />
                    Salvo às {lastSaved.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                  </p>
                )}
              </div>
            )}
          </div>
        )}

        {/* Steps Navigation */}
        <nav className="flex-1 overflow-y-auto py-4 scrollbar-hide">
          <ul className="space-y-1 px-3">
            {steps.map((step, index) => {
              const status = getStepStatus(index);
              return (
                <li key={step.id}>
                  <button
                    onClick={() => setCurrentStep(index)}
                    className={cn(
                      "w-full text-left px-4 py-3 rounded-xl text-sm transition-all duration-200",
                      "hover:bg-accent/50 group",
                      status === "current" && "bg-primary/10 border border-primary/30 shadow-sm",
                      status === "completed" && "bg-success/5 hover:bg-success/10",
                      status === "pending" && "opacity-60 hover:opacity-80"
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <div className={cn(
                        "w-7 h-7 rounded-lg flex items-center justify-center text-xs font-medium transition-all",
                        status === "completed" && "bg-success text-white",
                        status === "current" && "bg-primary text-primary-foreground",
                        status === "pending" && "bg-muted text-muted-foreground group-hover:bg-muted/80"
                      )}>
                        {status === "completed" ? (
                          <CheckCircle className="h-4 w-4" />
                        ) : (
                          <span>{index + 1}</span>
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className={cn(
                          "font-medium truncate text-sm",
                          status === "current" && "text-primary"
                        )}>
                          {step.label}
                        </div>
                        <div className="text-[10px] text-muted-foreground truncate">
                          {step.description}
                        </div>
                      </div>
                    </div>
                  </button>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Progress Footer */}
        <div className="p-4 border-t border-border space-y-4">
          <div>
            <div className="mb-2 flex justify-between text-xs">
              <span className="text-muted-foreground">Progresso</span>
              <span className="font-semibold tabular-nums">{completedSteps.size}/10</span>
            </div>
            <div className="h-2 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-primary to-success transition-all duration-500 ease-out"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>
          </div>
          <div className="glass rounded-lg p-3">
            <div className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">Session ID</div>
            <div className="text-xs font-mono text-foreground">{sessionId || "..."}</div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 border-b border-border flex items-center px-6 lg:px-8 justify-between glass">
          <div className="flex items-center gap-4">
            <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center">
              <span className="text-xl">{steps[currentStep].icon}</span>
            </div>
            <div>
              <h2 className="text-lg font-semibold">{steps[currentStep].label}</h2>
              <p className="text-xs text-muted-foreground">{steps[currentStep].description}</p>
            </div>
          </div>
          <Badge
            variant="outline"
            className={cn(
              "font-mono text-xs",
              completedSteps.has(currentStep)
                ? "bg-success/10 text-success border-success/30"
                : "bg-warning/10 text-warning border-warning/30"
            )}
          >
            {completedSteps.has(currentStep) ? (
              <>
                <CheckCircle className="h-3 w-3 mr-1" />
                COMPLETED
              </>
            ) : (
              <>
                <Sparkles className="h-3 w-3 mr-1" />
                IN PROGRESS
              </>
            )}
          </Badge>
        </header>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 lg:p-8">
          <div className="max-w-5xl mx-auto animate-fade-in">
            <div className="card-subtle rounded-2xl p-6 lg:p-8 min-h-[500px]">
              {renderStepContent()}
            </div>

            {/* Navigation */}
            <div className="mt-6 flex justify-between items-center">
              <Button
                onClick={goToPrevStep}
                disabled={currentStep === 0}
                variant="outline"
                className="gap-2 rounded-full"
              >
                <ChevronLeft className="h-4 w-4" />
                Voltar
              </Button>

              <div className="flex items-center gap-1.5">
                {steps.map((_, idx) => (
                  <button
                    key={idx}
                    onClick={() => setCurrentStep(idx)}
                    className={cn(
                      "h-2 rounded-full transition-all duration-300",
                      idx === currentStep
                        ? "bg-primary w-6"
                        : completedSteps.has(idx)
                        ? "bg-success w-2 hover:w-3"
                        : "bg-muted w-2 hover:bg-muted-foreground/50"
                    )}
                  />
                ))}
              </div>

              <Button
                onClick={goToNextStep}
                disabled={currentStep === steps.length - 1}
                className="btn-pill btn-primary gap-2"
              >
                {currentStep === steps.length - 1 ? "Finalizar" : "Próximo"}
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </main>

      {/* Save Modal */}
      {showSaveModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
          <div className="glass rounded-2xl p-6 w-full max-w-md mx-4 animate-scale-in shadow-elevated">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">Salvar Análise</h3>
              <button
                onClick={() => setShowSaveModal(false)}
                className="h-8 w-8 rounded-lg hover:bg-muted flex items-center justify-center transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <input
              type="text"
              value={analysisName}
              onChange={(e) => setAnalysisName(e.target.value)}
              placeholder="Nome da análise (ex: Terreno Alphaville)"
              className="input-field mb-6"
              autoFocus
            />
            <div className="flex gap-3 justify-end">
              <Button
                onClick={() => setShowSaveModal(false)}
                variant="outline"
              >
                Cancelar
              </Button>
              <Button
                onClick={handleSaveAs}
                disabled={isSaving || !analysisName.trim()}
                className="gap-2"
              >
                {isSaving ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Salvando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" />
                    Salvar
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Load Modal */}
      {showLoadModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-fade-in">
          <div className="glass rounded-2xl p-6 w-full max-w-lg mx-4 max-h-[80vh] flex flex-col animate-scale-in shadow-elevated">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">Minhas Análises</h3>
              <button
                onClick={() => setShowLoadModal(false)}
                className="h-8 w-8 rounded-lg hover:bg-muted flex items-center justify-center transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto space-y-2 scrollbar-hide">
              {savedAnalyses.length === 0 ? (
                <div className="text-center py-12">
                  <div className="h-12 w-12 rounded-full bg-muted flex items-center justify-center mx-auto mb-3">
                    <FileText className="h-6 w-6 text-muted-foreground" />
                  </div>
                  <p className="text-muted-foreground">Nenhuma análise salva ainda.</p>
                </div>
              ) : (
                savedAnalyses.map((analysis) => (
                  <div
                    key={analysis.id}
                    className="flex items-center justify-between p-4 rounded-xl border border-border hover:border-primary/30 hover:bg-accent/30 transition-all group"
                  >
                    <button
                      onClick={() => {
                        loadAnalysis(analysis.id);
                        setShowLoadModal(false);
                      }}
                      className="flex-1 text-left"
                    >
                      <div className="font-medium group-hover:text-primary transition-colors">
                        {analysis.name}
                      </div>
                      <div className="text-xs text-muted-foreground flex items-center gap-2 mt-1">
                        <Clock className="h-3 w-3" />
                        {new Date(analysis.updated_at).toLocaleDateString('pt-BR', {
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                        <span className="text-muted-foreground/50">•</span>
                        <span className="tabular-nums">{analysis.data.completedSteps?.length || 0}/10 passos</span>
                      </div>
                    </button>
                    <button
                      onClick={() => handleDeleteAnalysis(analysis.id)}
                      className="p-2 text-destructive opacity-0 group-hover:opacity-100 hover:bg-destructive/10 rounded-lg transition-all"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))
              )}
            </div>
            <div className="mt-4 pt-4 border-t border-border">
              <Button
                onClick={() => setShowLoadModal(false)}
                variant="outline"
                className="w-full"
              >
                Fechar
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function WizardPage() {
  return (
    <Suspense fallback={
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="text-center animate-fade-in">
          <div className="h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
          <p className="text-muted-foreground">Carregando...</p>
        </div>
      </div>
    }>
      <WizardContent />
    </Suspense>
  );
}
