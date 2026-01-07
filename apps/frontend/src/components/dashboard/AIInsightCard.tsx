"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Bot, Sparkles, Brain } from "lucide-react";
import ReactMarkdown from 'react-markdown';

interface AIInsightCardProps {
    data: any;
}

export function AIInsightCard({ data }: AIInsightCardProps) {
    const [thesis, setThesis] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!data) return;

        const fetchThesis = async () => {
            setLoading(true);
            try {
                const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
                const res = await fetch(`${apiUrl}/analyze/thesis`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ financial_data: data.result })
                });

                if (res.ok) {
                    const json = await res.json();
                    setThesis(json.thesis);
                }
            } catch (error) {
                console.error("Failed to fetch AI thesis", error);
            } finally {
                setLoading(false);
            }
        };

        fetchThesis();
    }, [data]);

    return (
        <Card className="relative overflow-hidden border-none">
            {/* Gradient background */}
            <div className="absolute inset-0 gradient-primary opacity-95" />

            {/* Decorative elements */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2" />

            {/* Content */}
            <div className="relative z-10">
                <CardHeader className="flex flex-row items-center justify-between pb-3">
                    <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
                            <Brain className="h-5 w-5 text-white" />
                        </div>
                        <div>
                            <CardTitle className="text-xl font-bold text-white flex items-center gap-2">
                                VERTIV AI Analyst
                            </CardTitle>
                            <p className="text-sm text-white/70">Strategic Investment Analysis</p>
                        </div>
                    </div>
                    <Badge
                        variant="outline"
                        className="bg-white/10 border-white/20 text-white backdrop-blur-sm"
                    >
                        <Sparkles className="h-3 w-3 mr-1" />
                        AI Powered
                    </Badge>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="space-y-3">
                            <div className="flex items-center gap-2 mb-4">
                                <div className="h-2 w-2 rounded-full bg-white/60 animate-pulse" />
                                <span className="text-sm text-white/70">Analyzing investment data...</span>
                            </div>
                            <Skeleton className="h-4 w-full bg-white/20" />
                            <Skeleton className="h-4 w-5/6 bg-white/20" />
                            <Skeleton className="h-4 w-4/6 bg-white/20" />
                            <Skeleton className="h-4 w-3/4 bg-white/20" />
                        </div>
                    ) : thesis ? (
                        <div className="prose prose-invert max-w-none">
                            <div className="text-white/90 leading-relaxed [&>p]:mb-3 [&>ul]:list-disc [&>ul]:pl-5 [&>ul]:mb-3 [&>h3]:text-lg [&>h3]:font-semibold [&>h3]:text-white [&>h3]:mt-4 [&>h3]:mb-2 [&>strong]:text-white">
                                <ReactMarkdown>{thesis}</ReactMarkdown>
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center gap-3 text-white/60">
                            <Bot className="h-5 w-5" />
                            <p className="italic">Waiting for simulation data to generate insights...</p>
                        </div>
                    )}
                </CardContent>
            </div>
        </Card>
    );
}
