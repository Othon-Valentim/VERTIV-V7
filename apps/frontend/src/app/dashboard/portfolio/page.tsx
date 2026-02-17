"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api-client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import {
  Rocket,
  FileText,
  TrendingUp,
  TrendingDown,
  Building2,
  BarChart3,
  ArrowUpRight,
  Clock,
  CheckCircle2,
  AlertCircle
} from "lucide-react";

interface SimulationSummary {
  id: string;
  status: string;
  created_at: string;
  result?: {
    project?: {
        name?: string;
    };
    real_options?: {
        kpi?: {
            enpv?: number;
            volatility?: number;
            decision?: string;
        }
    }
  }
}

export default function PortfolioPage() {
    const [simulations, setSimulations] = useState<SimulationSummary[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSims = async () => {
             try {
                const res = await api.get("/simulations?limit=20");
                if (res.ok) {
                    const data = await res.json();
                    setSimulations(data);
                }
             } catch (e) {
                 console.error(e);
             } finally {
                 setLoading(false);
             }
        };
        fetchSims();
    }, []);

    const formatCurrency = (val?: number) => val ? new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', notation: 'compact' }).format(val) : '-';

    // Calculate summary stats
    const totalSimulations = simulations.length;
    const completedSimulations = simulations.filter(s => s.status === 'COMPLETED').length;
    const totalENPV = simulations.reduce((acc, sim) => acc + (sim.result?.real_options?.kpi?.enpv || 0), 0);
    const investDecisions = simulations.filter(s => s.result?.real_options?.kpi?.decision === 'INVEST').length;

    return (
        <div className="flex flex-col gap-8 p-6 lg:p-8 min-h-screen seamless-bg text-foreground">
            {/* Header */}
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 animate-fade-in">
                <div className="space-y-1">
                    <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-sm bg-primary flex items-center justify-center">
                            <Building2 className="h-5 w-5 text-white" />
                        </div>
                        <h1 className="text-3xl font-black tracking-tighter uppercase text-primary">
                            Portfolio Command
                        </h1>
                    </div>
                    <p className="text-muted-foreground ml-13">
                        Centralized governance of all Real Estate Assets.
                    </p>
                </div>
                <Button
                    onClick={() => window.location.href='/wizard'}
                    className="btn-pill btn-primary gap-2 self-start lg:self-auto"
                >
                    <Rocket className="h-4 w-4" />
                    New Simulation
                    <ArrowUpRight className="h-4 w-4" />
                </Button>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 animate-slide-up">
                <Card className="card-elevated border-none">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Total Simulations
                        </CardTitle>
                        <BarChart3 className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold">{totalSimulations}</div>
                        <p className="text-xs text-muted-foreground mt-1">
                            In the global registry
                        </p>
                    </CardContent>
                </Card>

                <Card className="card-elevated border-none">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Completed
                        </CardTitle>
                        <CheckCircle2 className="h-4 w-4 text-success" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold text-success">{completedSimulations}</div>
                        <p className="text-xs text-muted-foreground mt-1">
                            Successfully processed
                        </p>
                    </CardContent>
                </Card>

                <Card className="card-elevated border-none">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-bold uppercase tracking-widest text-muted-foreground">
                            Total ENPV
                        </CardTitle>
                        <TrendingUp className="h-4 w-4 text-primary" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-black text-primary tabular-nums tracking-tighter">
                            {formatCurrency(totalENPV)}
                        </div>
                        <p className="text-xs text-muted-foreground mt-1">
                            Aggregated strategic value
                        </p>
                    </CardContent>
                </Card>

                <Card className="card-elevated border-none">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Invest Decisions
                        </CardTitle>
                        <Rocket className="h-4 w-4 text-accent" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold text-accent">{investDecisions}</div>
                        <p className="text-xs text-muted-foreground mt-1">
                            Recommended to proceed
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Simulations Table */}
            <Card className="card-subtle animate-slide-up" style={{ animationDelay: '0.1s' }}>
                <CardHeader className="pb-4">
                    <div className="flex items-center justify-between">
                        <CardTitle className="text-lg font-semibold">Active Simulations</CardTitle>
                        <Badge variant="secondary" className="font-normal">
                            {totalSimulations} total
                        </Badge>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="rounded-sm border-none overflow-hidden">
                        <Table>
                            <TableHeader>
                                <TableRow className="bg-secondary/20 hover:bg-secondary/20 border-b-primary/10">
                                    <TableHead className="w-[100px] font-semibold">ID</TableHead>
                                    <TableHead className="font-semibold">Date</TableHead>
                                    <TableHead className="font-semibold">Status</TableHead>
                                    <TableHead className="text-right font-semibold">Strategic NPV</TableHead>
                                    <TableHead className="text-right font-semibold">Volatility</TableHead>
                                    <TableHead className="text-center font-semibold">Decision</TableHead>
                                    <TableHead className="text-right font-semibold">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {loading ? (
                                    [...Array(5)].map((_, i) => (
                                        <TableRow key={i}>
                                            <TableCell><Skeleton className="h-4 w-16" /></TableCell>
                                            <TableCell><Skeleton className="h-4 w-24" /></TableCell>
                                            <TableCell><Skeleton className="h-6 w-20 rounded-full" /></TableCell>
                                            <TableCell><Skeleton className="h-4 w-20 ml-auto" /></TableCell>
                                            <TableCell><Skeleton className="h-4 w-12 ml-auto" /></TableCell>
                                            <TableCell><Skeleton className="h-6 w-16 mx-auto rounded-full" /></TableCell>
                                            <TableCell><Skeleton className="h-8 w-8 ml-auto rounded-lg" /></TableCell>
                                        </TableRow>
                                    ))
                                ) : simulations.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={7} className="text-center py-16">
                                            <div className="flex flex-col items-center gap-3">
                                                <div className="h-12 w-12 rounded-full bg-muted flex items-center justify-center">
                                                    <AlertCircle className="h-6 w-6 text-muted-foreground" />
                                                </div>
                                                <p className="text-muted-foreground">No simulations found in the Global Registry.</p>
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => window.location.href='/wizard'}
                                                    className="mt-2"
                                                >
                                                    <Rocket className="h-4 w-4 mr-2" />
                                                    Create your first simulation
                                                </Button>
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    simulations.map((sim, index) => {
                                        const kpi = sim.result?.real_options?.kpi;
                                        return (
                                            <TableRow
                                                key={sim.id}
                                                className="cursor-pointer hover:bg-muted/50 transition-colors group"
                                                onClick={() => window.location.href=`/dashboard/real-options?id=${sim.id}`}
                                                style={{ animationDelay: `${index * 0.05}s` }}
                                            >
                                                <TableCell className="font-mono text-xs text-muted-foreground">
                                                    {sim.id.slice(0,8)}
                                                </TableCell>
                                                <TableCell className="flex items-center gap-2">
                                                    <Clock className="h-3 w-3 text-muted-foreground" />
                                                    {new Date(sim.created_at).toLocaleDateString('pt-BR')}
                                                </TableCell>
                                                <TableCell>
                                                    <Badge
                                                        variant={sim.status === 'COMPLETED' ? 'default' : 'secondary'}
                                                        className={`
                                                            rounded-sm font-bold uppercase tracking-tight text-[10px]
                                                            ${sim.status === 'COMPLETED'
                                                                ? 'bg-success/10 text-success border-none'
                                                                : 'bg-secondary text-primary border-none'
                                                            }
                                                        `}
                                                    >
                                                        {sim.status}
                                                    </Badge>
                                                </TableCell>
                                                <TableCell className="text-right font-semibold tabular-nums">
                                                    <span className={kpi?.enpv && kpi.enpv > 0 ? 'text-success' : 'text-destructive'}>
                                                        {formatCurrency(kpi?.enpv)}
                                                    </span>
                                                </TableCell>
                                                <TableCell className="text-right tabular-nums text-muted-foreground">
                                                    {kpi?.volatility ? `${(kpi.volatility * 100).toFixed(1)}%` : '-'}
                                                </TableCell>
                                                <TableCell className="text-center">
                                                    {kpi?.decision && (
                                                        <Badge
                                                            variant="outline"
                                                            className={`
                                                                ${kpi.decision === 'INVEST'
                                                                    ? 'text-success border-success/50 bg-success/5'
                                                                    : 'text-warning border-warning/50 bg-warning/5'
                                                                }
                                                            `}
                                                        >
                                                            {kpi.decision === 'INVEST' ? (
                                                                <TrendingUp className="h-3 w-3 mr-1" />
                                                            ) : (
                                                                <TrendingDown className="h-3 w-3 mr-1" />
                                                            )}
                                                            {kpi.decision}
                                                        </Badge>
                                                    )}
                                                </TableCell>
                                                <TableCell className="text-right">
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        className="opacity-0 group-hover:opacity-100 transition-opacity hover:bg-primary/10 hover:text-primary"
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            window.open(`/reports/deal-memo/${sim.id}`, '_blank');
                                                        }}
                                                    >
                                                        <FileText className="h-4 w-4" />
                                                    </Button>
                                                </TableCell>
                                            </TableRow>
                                        );
                                    })
                                )}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>

            {/* Footer */}
            <div className="border-t border-border pt-6 mt-auto">
                <p className="text-xs text-muted-foreground text-center">
                    VERTIV Global Real Estate Intelligence Platform v6.1.0 | Portfolio Command Center
                </p>
            </div>
        </div>
    );
}
