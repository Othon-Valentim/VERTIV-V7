"use client";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface ConeData {
  time_step: number;     // e.g. Year 0, 0.5, 1.0...
  underlying_price: number; // Current Asset Value
  upside_scenario: number;  // Upper bound (e.g. +1 std dev)
  downside_scenario: number;// Lower bound (e.g. -1 std dev)
}

interface RealOptionsConeProps {
  data: ConeData[];
}

export function RealOptionsCone({ data }: RealOptionsConeProps) {
  const currencyFormatter = (value: number) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
      notation: "compact", 
      maximumFractionDigits: 1,
    }).format(value);

  return (
    <Card className="col-span-1 md:col-span-2">
      <CardHeader>
        <CardTitle>Cone of Uncertainty</CardTitle>
        <CardDescription>Asset Value Evolution Scenarios (Geometric Brownian Motion)</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[350px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorUpside" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorDownside" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="time_step" label={{ value: "Years", position: "insideBottomRight", offset: -5 }} />
              <YAxis tickFormatter={currencyFormatter} />
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <Tooltip 
                 formatter={(value: number) => currencyFormatter(value)}
                 contentStyle={{ backgroundColor: "#1e1e1e", borderColor: "#333" }}
              />
              <Legend />
              
              {/* Render Upside Area */}
              <Area 
                type="monotone" 
                dataKey="upside_scenario" 
                stroke="#8884d8" 
                fillOpacity={1} 
                fill="url(#colorUpside)" 
                name="Optimistic (+1σ)"
                stackId="1" // Not stacking, just render
              />
               {/* Render Expected Area (Middle) - Not strictly needed if showing bounds, but maybe helpful? 
                   For now, let's show Downside as separate area
               */}
              <Area 
                type="monotone" 
                dataKey="downside_scenario" 
                stroke="#82ca9d" 
                fillOpacity={0.5} 
                fill="url(#colorDownside)" 
                name="Pessimistic (-1σ)"
              />
                {/* 
                  Note: In a true cone, we often fill the 'spread'. 
                  Recharts requires custom logic for "Range Area" (Area between two lines).
                  For simplicity in V6.0, we overlay two areas. 
                 */}
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
