"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface HeatmapCell {
  row_val: number; // e.g., Construction Cost variation (-10%)
  col_val: number; // e.g., Sales Price variation (+5%)
  result_val: number; // e.g., NPV
}

interface SensitivityHeatmapProps {
  data: HeatmapCell[];
  rowLabel: string;
  colLabel: string;
}

export function SensitivityHeatmap({ data, rowLabel, colLabel }: SensitivityHeatmapProps) {
  // Extract unique row and column headers
  const uniqueRows = Array.from(new Set(data.map((d) => d.row_val))).sort((a, b) => a - b);
  const uniqueCols = Array.from(new Set(data.map((d) => d.col_val))).sort((a, b) => a - b);

  // Helper to find result for a specific cell
  const getResult = (r: number, c: number) => 
    data.find((d) => d.row_val === r && d.col_val === c)?.result_val || 0;

  // Color scale logic (Red to Green)
  // Assuming 0 is neutral. Positive is green, negative is red.
  const getColor = (value: number) => {
    if (value > 0) return "text-green-500 font-bold";
    if (value < 0) return "text-red-500 font-bold";
    return "text-muted-foreground";
  };
  
  const formatPercentage = (val: number) => `${val > 0 ? "+" : ""}${val}%`;
  const formatCurrency = (val: number) => 
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
      notation: "compact", 
      maximumFractionDigits: 1
    }).format(val);

  return (
    <Card className="col-span-1">
      <CardHeader>
        <CardTitle>Sensitivity Analysis</CardTitle>
        <CardDescription>
          {rowLabel} (Rows) vs. {colLabel} (Cols)
        </CardDescription>
      </CardHeader>
      <CardContent className="overflow-x-auto">
        <table className="w-full text-sm text-center">
            <thead>
                <tr>
                    <th className="p-2 border-b border-r border-border/50 bg-muted/50 text-muted-foreground font-mono text-xs">
                        {rowLabel} \ {colLabel}
                    </th>
                    {uniqueCols.map((col) => (
                        <th key={col} className="p-2 border-b border-border/50 font-medium">
                            {formatPercentage(col)}
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {uniqueRows.map((row) => (
                    <tr key={row} className="hover:bg-muted/10 transition-colors">
                        <td className="p-2 border-r border-border/50 font-medium bg-muted/20">
                            {formatPercentage(row)}
                        </td>
                        {uniqueCols.map((col) => {
                            const val = getResult(row, col);
                            return (
                                <td key={`${row}-${col}`} className={cn("p-2 border border-border/10", getColor(val))}>
                                    {formatCurrency(val)}
                                </td>
                            );
                        })}
                    </tr>
                ))}
            </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
