
import React from 'react';
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

interface AgentProps {
    role: 'BLUE' | 'RED' | 'GOLD';
    name: string;
    title: string;
    avatarUrl?: string; // Optional for now
    argument: string;
    confidence?: number;
}

const roleStyles = {
    BLUE: {
        border: "border-blue-500/50",
        bg: "bg-blue-950/20",
        text: "text-blue-200",
        badge: "bg-blue-600 hover:bg-blue-700",
        icon: "🛡️"
    },
    RED: {
        border: "border-red-500/50",
        bg: "bg-red-950/20",
        text: "text-red-200",
        badge: "bg-red-600 hover:bg-red-700",
        icon: "⚔️"
    },
    GOLD: {
        border: "border-yellow-500/50",
        bg: "bg-yellow-950/20",
        text: "text-yellow-200",
        badge: "bg-yellow-600 hover:bg-yellow-700",
        icon: "⚖️"
    }
};

export function TribunalCard({ role, name, title, argument, confidence }: AgentProps) {
    const style = roleStyles[role];

    return (
        <Card className={cn("border-2 transition-all hover:scale-[1.02]", style.border, style.bg)}>
            <CardHeader className="flex flex-row items-center gap-4 pb-2">
                <Avatar className="h-12 w-12 border-2 border-white/10">
                    <AvatarFallback className={cn("text-lg font-bold", style.text)}>
                        {name[0]}
                    </AvatarFallback>
                </Avatar>
                <div className="flex flex-col">
                    <CardTitle className={cn("text-lg font-bold flex items-center gap-2", style.text)}>
                        {name} 
                        <Badge variant="secondary" className={cn("text-white text-xs", style.badge)}>
                            {style.icon} {role}
                        </Badge>
                    </CardTitle>
                    <span className="text-xs text-muted-foreground uppercase tracking-widest font-semibold">
                        {title}
                    </span>
                </div>
                {confidence && (
                     <div className="ml-auto flex flex-col items-end">
                        <span className="text-xs text-muted-foreground font-mono">CONFIDENCE</span>
                        <span className={cn("text-xl font-bold font-mono", style.text)}>{confidence}%</span>
                     </div>
                )}
            </CardHeader>
            <CardContent>
                <div className="relative pl-4 border-l-2 border-white/10 italic text-sm text-gray-300 leading-relaxed">
                    <span className={cn("absolute -top-2 -left-3 text-2xl opacity-50", style.text)}>“</span>
                    {argument}
                    <span className={cn("block text-right text-2xl opacity-50 -mt-4", style.text)}>”</span>
                </div>
            </CardContent>
        </Card>
    );
}
