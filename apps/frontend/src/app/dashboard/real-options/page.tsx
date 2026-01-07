"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CashFlowChart } from "@/components/charts/CashFlowChart";
import { RealOptionsCone } from "@/components/charts/RealOptionsCone";
import { SensitivityHeatmap } from "@/components/charts/SensitivityHeatmap";
import { useLatestSimulation } from "@/hooks/useSimulation";
import { Skeleton } from "@/components/ui/skeleton";
import { AIInsightCard } from "@/components/dashboard/AIInsightCard";
import { exportDashboardToPDF, type KPIData } from "@/lib/pdf-generator";
import {
  FileDown,
  Loader2,
  Rocket,
  TrendingUp,
  TrendingDown,
  Activity,
  Target,
  DollarSign,
  Zap,
  ArrowUpRight,
  AlertTriangle
} from "lucide-react";

// --- Mock Data for Demo when no simulation exists ---
const generateMockData = () => {
  const cashFlow = [];
  let accum = -20000000;
  for (let i = 0; i <= 24; i++) {
    const net = i === 24 ? 35000000 : i > 12 ? 1000000 : -800000;
    accum += net;
    cashFlow.push({ period: i, net_cash_flow: net, accumulated_cash_flow: accum });
  }

  const coneData = [];
  const S0 = 35000000;
  const vol = 0.2;
  for (let t = 0; t <= 2; t += 0.2) {
    coneData.push({
      time_step: Number(t.toFixed(1)),
      underlying_price: S0,
      upside_scenario: S0 * Math.exp(vol * Math.sqrt(t)),
      downside_scenario: S0 * Math.exp(-vol * Math.sqrt(t)),
    });
  }

  const heatmapData = [
    { row_val: -10, col_val: -10, result_val: 5000000 },
    { row_val: -10, col_val: 0, result_val: 7000000 },
    { row_val: -10, col_val: 10, result_val: 9000000 },
    { row_val: 0, col_val: -10, result_val: 2000000 },
    { row_val: 0, col_val: 0, result_val: 4500000 },
    { row_val: 0, col_val: 10, result_val: 6800000 },
    { row_val: 10, col_val: -10, result_val: -1000000 },
    { row_val: 10, col_val: 0, result_val: 1500000 },
    { row_val: 10, col_val: 10, result_val: 4000000 },
  ];

  return {
    cashFlow,
    coneData,
    heatmapData,
    kpi: { enpv: 14230000, option_value: 2150000, volatility: 0.225, decision: "INVEST" },
  };
};

export default function RealOptionsPage() {
  const { data: simulation, loading, error } = useLatestSimulation();
  const [exporting, setExporting] = useState(false);
  const mockData = generateMockData();

  // Safely extract results or use mock defaults
  const result = simulation?.result || {};
  const cfData = result.cash_flow?.length > 0 ? result.cash_flow : mockData.cashFlow;
  const coneData = result.real_options?.cone?.length > 0 ? result.real_options.cone : mockData.coneData;
  const heatmapData = result.real_options?.heatmap?.length > 0 ? result.real_options.heatmap : mockData.heatmapData;
  const kpi = result.real_options?.kpi?.enpv ? result.real_options.kpi : mockData.kpi;
  const isDemo = !simulation || !result.real_options?.kpi?.enpv;

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", notation: "compact", maximumFractionDigits: 1 }).format(value);

  // Enterprise PDF Export Handler
  const handleExportPDF = async () => {
    setExporting(true);
    try {
      const kpis: KPIData[] = [
        { label: "Strategic NPV (ENPV)", value: formatCurrency(kpi.enpv || 0), trend: (kpi.enpv || 0) > 0 ? "up" : "down" },
        { label: "Option Premium", value: formatCurrency(kpi.option_value || 0), trend: "up" },
        { label: "Volatility (σ)", value: `${((kpi.volatility || 0) * 100).toFixed(1)}%`, trend: "neutral" },
        { label: "Recommendation", value: kpi.decision || "WAIT", trend: kpi.decision === "INVEST" ? "up" : "neutral" },
      ];
      await exportDashboardToPDF(simulation?.id || "VERTIV_Analysis", kpis, ["chart-cashflow", "chart-heatmap", "chart-cone"]);
    } catch (err) {
      console.error("PDF Export failed:", err);
    } finally {
      setExporting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col gap-6 p-6 lg:p-8 min-h-screen bg-background">
        <div className="flex justify-between items-center animate-fade-in">
          <div className="space-y-2">
            <Skeleton className="h-10 w-[300px]" />
            <Skeleton className="h-4 w-[200px]" />
          </div>
          <div className="flex gap-2">
            <Skeleton className="h-10 w-[120px] rounded-full" />
            <Skeleton className="h-10 w-[160px] rounded-full" />
          </div>
        </div>
        <div className="grid gap-4 md:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-[130px] w-full rounded-xl" />
          ))}
        </div>
        <div className="grid gap-6 md:grid-cols-7">
          <Skeleton className="col-span-4 h-[400px] rounded-xl" />
          <Skeleton className="col-span-3 h-[400px] rounded-xl" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background p-8">
        <Card className="card-elevated max-w-md w-full text-center p-8">
          <div className="h-16 w-16 rounded-full bg-destructive/10 flex items-center justify-center mx-auto mb-4">
            <AlertTriangle className="h-8 w-8 text-destructive" />
          </div>
          <h2 className="text-xl font-bold mb-2">Error Loading Data</h2>
          <p className="text-muted-foreground mb-6">{error}</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6 p-6 lg:p-8 min-h-screen bg-background text-foreground">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 animate-fade-in">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center">
              <Activity className="h-5 w-5 text-primary" />
            </div>
            <h1 className="text-2xl lg:text-3xl font-bold tracking-tight">
              Real Options Valuation
            </h1>
          </div>
          <div className="ml-13">
            {isDemo ? (
              <div className="flex items-center gap-2 text-warning">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-warning opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-warning"></span>
                </span>
                <span className="text-sm">Demo Mode - Run a simulation for real data</span>
              </div>
            ) : (
              <p className="text-muted-foreground">
                Simulation:{" "}
                <span className="font-mono text-xs bg-muted px-2 py-1 rounded-md">
                  {simulation?.id}
                </span>
              </p>
            )}
          </div>
        </div>
        <div className="flex gap-3 self-start lg:self-auto">
          <Button
            variant="outline"
            onClick={handleExportPDF}
            disabled={exporting}
            className="rounded-full gap-2"
          >
            {exporting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <FileDown className="h-4 w-4" />
                Export PDF
              </>
            )}
          </Button>
          <Button
            onClick={() => window.location.href='/wizard'}
            className="btn-pill btn-primary gap-2"
          >
            <Rocket className="h-4 w-4" />
            New Simulation
            <ArrowUpRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* AI Analyst Section */}
      <div className="animate-slide-up">
        <AIInsightCard data={simulation} />
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 animate-slide-up" style={{ animationDelay: '0.1s' }}>
        <Card className="card-elevated border-none group hover:border-primary/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Strategic NPV (ENPV)
            </CardTitle>
            <div className="h-8 w-8 rounded-lg bg-success/10 flex items-center justify-center">
              <DollarSign className="h-4 w-4 text-success" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl lg:text-3xl font-bold text-success tabular-nums">
              {formatCurrency(kpi.enpv || 0)}
            </div>
            <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
              <TrendingUp className="h-3 w-3" />
              Expected Strategic Value
            </p>
          </CardContent>
        </Card>

        <Card className="card-elevated border-none">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Option Premium
            </CardTitle>
            <div className="h-8 w-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <Zap className="h-4 w-4 text-primary" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl lg:text-3xl font-bold text-primary tabular-nums">
              {formatCurrency(kpi.option_value || 0)}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Value of Wait-to-Build
            </p>
          </CardContent>
        </Card>

        <Card className="card-elevated border-none">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Volatility
            </CardTitle>
            <div className="h-8 w-8 rounded-lg bg-accent/10 flex items-center justify-center">
              <Activity className="h-4 w-4 text-accent" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl lg:text-3xl font-bold tabular-nums">
              {(kpi.volatility * 100)?.toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              Market Uncertainty
            </p>
          </CardContent>
        </Card>

        <Card className="card-elevated border-none">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Recommendation
            </CardTitle>
            <div className="h-8 w-8 rounded-lg bg-muted flex items-center justify-center">
              <Target className="h-4 w-4 text-foreground" />
            </div>
          </CardHeader>
          <CardContent>
            <Badge
              className={`
                text-base px-4 py-1.5 font-semibold
                ${kpi.decision === 'INVEST'
                  ? 'bg-success/10 text-success border-success/20 hover:bg-success/20'
                  : 'bg-warning/10 text-warning border-warning/20 hover:bg-warning/20'
                }
              `}
            >
              {kpi.decision === 'INVEST' ? (
                <TrendingUp className="h-4 w-4 mr-2" />
              ) : (
                <TrendingDown className="h-4 w-4 mr-2" />
              )}
              {kpi.decision || 'WAIT'}
            </Badge>
          </CardContent>
        </Card>
      </div>

      {/* Main Charts Area */}
      <div className="grid gap-6 lg:grid-cols-7 animate-slide-up" style={{ animationDelay: '0.2s' }}>
        <Card className="lg:col-span-4 card-subtle" id="chart-cashflow">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-primary" />
              Cash Flow Projection
            </CardTitle>
            <CardDescription>Net and accumulated cash flows over time</CardDescription>
          </CardHeader>
          <CardContent>
            <CashFlowChart data={cfData} />
          </CardContent>
        </Card>

        <Card className="lg:col-span-3 card-subtle" id="chart-heatmap">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-accent" />
              Sensitivity Matrix
            </CardTitle>
            <CardDescription>NPV sensitivity to key variables</CardDescription>
          </CardHeader>
          <CardContent>
            <SensitivityHeatmap
              data={heatmapData}
              rowLabel="Construction Cost"
              colLabel="Sales Price"
            />
          </CardContent>
        </Card>
      </div>

      {/* Secondary Charts Area */}
      <Card className="card-subtle animate-slide-up" style={{ animationDelay: '0.3s' }} id="chart-cone">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-primary" />
            Real Options Cone
          </CardTitle>
          <CardDescription>Value evolution with upside and downside scenarios</CardDescription>
        </CardHeader>
        <CardContent>
          <RealOptionsCone data={coneData} />
        </CardContent>
      </Card>

      {/* Footer */}
      <div className="border-t border-border pt-6 mt-4">
        <p className="text-xs text-muted-foreground text-center">
          VERTIV Global Real Estate Intelligence Platform v6.1.0 | Powered by Polars LazyFrames & Black-Scholes-Merton Engine
        </p>
      </div>
    </div>
  );
}
