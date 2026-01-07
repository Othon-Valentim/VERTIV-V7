"use client";

import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface CashFlowData {
  period: number;
  net_cash_flow: number;
  accumulated_cash_flow: number;
}

interface CashFlowChartProps {
  data: CashFlowData[];
}

export function CashFlowChart({ data }: CashFlowChartProps) {
  // Format currency for tooltip
  const currencyFormatter = (value: number) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
      notation: "compact", // Abbreviate large numbers (e.g., 1M)
      maximumFractionDigits: 1,
    }).format(value);

  return (
    <Card className="col-span-1 md:col-span-2">
      <CardHeader>
        <CardTitle>Cash Flow Evolution</CardTitle>
        <CardDescription>Monthly vs. Accumulated Cash Flow</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[350px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis 
                dataKey="period" 
                label={{ value: "Month", position: "insideBottomRight", offset: -10 }} 
                stroke="#888888"
              />
              <YAxis 
                yAxisId="left" 
                tickFormatter={currencyFormatter} 
                stroke="#888888"
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                tickFormatter={currencyFormatter} 
                stroke="#888888"
              />
              <Tooltip 
                formatter={(value: number) => currencyFormatter(value)}
                contentStyle={{ backgroundColor: "#1e1e1e", borderColor: "#333" }}
                itemStyle={{ color: "#fff" }}
              />
              <Legend />
              {/* Monthly Cash Flow (Bars) */}
              <Bar 
                yAxisId="left" 
                dataKey="net_cash_flow" 
                name="Monthly Net" 
                fill="#22c55e" 
                barSize={20} 
                radius={[4, 4, 0, 0]} 
              />
              {/* Accumulated Cash Flow (Line) */}
              <Line 
                yAxisId="right" 
                type="monotone" 
                dataKey="accumulated_cash_flow" 
                name="Accumulated" 
                stroke="#3b82f6" 
                strokeWidth={3} 
                dot={{ r: 0 }} // Minimalist: no dots
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
