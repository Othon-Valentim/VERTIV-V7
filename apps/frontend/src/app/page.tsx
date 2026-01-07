"use client";

import Link from "next/link";
import { ArrowRight, BarChart3, Layers, Terminal, LogIn } from "lucide-react";
import UserMenu from "@/components/UserMenu";
import { useAuth } from "@/contexts/AuthContext";

export default function Home() {
  const { user, loading } = useAuth();

  return (
    <main className="flex min-h-screen flex-col bg-background selection:bg-primary/20">
      {/* Background Grid Effect */}
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:60px_60px] pointer-events-none" />
      <div className="absolute inset-0 flex items-center justify-center bg-background [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)] pointer-events-none" />

      {/* Navbar */}
      <header className="z-10 flex w-full items-center justify-between px-8 py-6 border-b border-border/40 backdrop-blur-sm">
        <div className="flex items-center gap-2">
            <div className="h-8 w-8 bg-primary rounded-sm flex items-center justify-center">
                <Terminal className="text-primary-foreground h-5 w-5" />
            </div>
            <span className="font-mono text-lg font-bold tracking-tighter">VERTIV<span className="text-primary">.global</span></span>
        </div>
        <div className="flex items-center gap-6">
            <div className="flex gap-6 text-sm font-medium text-muted-foreground">
                <span>v6.0.0-RC1</span>
                <span className="text-green-500 flex items-center gap-1">● SYSTEMS OPERATIONAL</span>
            </div>
            {!loading && (
              user ? (
                <UserMenu />
              ) : (
                <Link
                  href="/auth/login"
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
                >
                  <LogIn className="h-4 w-4" />
                  Entrar
                </Link>
              )
            )}
        </div>
      </header>

      {/* Hero Section */}
      <div className="z-10 flex-1 flex flex-col items-center justify-center text-center px-4 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-primary/20 blur-[120px] rounded-full pointer-events-none opacity-20" />
        
        <h1 className="text-6xl md:text-8xl font-bold tracking-tighter mb-6 bg-gradient-to-b from-white to-white/50 bg-clip-text text-transparent">
          Advanced<br/>Real Estate Alpha.
        </h1>
        <p className="max-w-2xl text-xl text-muted-foreground mb-12 leading-relaxed">
          The <span className="text-foreground font-semibold">Diamond Core</span> engine for complex viabillity analysis. 
          Powered by Polars LazyFrames and Black-Scholes-Merton Real Options.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl w-full">
            {/* Wizard Card */}
            <Link href="/wizard" className="group relative overflow-hidden rounded-xl border border-border bg-card/50 p-8 transition-all hover:bg-card hover:border-primary/50 hover:shadow-2xl hover:shadow-primary/10">
                <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
                    <ArrowRight className="h-6 w-6 -rotate-45 group-hover:rotate-0 transition-transform duration-300" />
                </div>
                <div className="flex flex-col items-start text-left">
                    <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                        <Layers className="h-6 w-6" />
                    </div>
                    <h3 className="text-2xl font-bold mb-2">TIV Wizard</h3>
                    <p className="text-muted-foreground">
                        Structured 10-step methodology. P1 Garimpo to P10 Financial Modeling. 
                    </p>
                </div>
            </Link>

             {/* Dashboard Card */}
             <Link href="/dashboard/real-options" className="group relative overflow-hidden rounded-xl border border-border bg-card/50 p-8 transition-all hover:bg-card hover:border-primary/50 hover:shadow-2xl hover:shadow-primary/10">
                <div className="absolute top-0 right-0 p-4 opacity-50 group-hover:opacity-100 transition-opacity">
                    <ArrowRight className="h-6 w-6 -rotate-45 group-hover:rotate-0 transition-transform duration-300" />
                </div>
                <div className="flex flex-col items-start text-left">
                    <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                        <BarChart3 className="h-6 w-6" />
                    </div>
                    <h3 className="text-2xl font-bold mb-2">Real Options</h3>
                    <p className="text-muted-foreground">
                         Black-Scholes valuation engine. Visualize the Cone of Uncertainty and Greeks.
                    </p>
                </div>
            </Link>
        </div>

        {/* Frameworks Section */}
        <div className="mt-24 grid grid-cols-2 md:grid-cols-4 gap-8 w-full max-w-5xl opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
            <div className="flex flex-col items-center">
                <span className="text-2xl font-bold tracking-tighter">RICS</span>
                <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Global ESG Standard</span>
            </div>
            <div className="flex flex-col items-center">
                <span className="text-2xl font-bold tracking-tighter">USP</span>
                <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Rocha Lima Methodology</span>
            </div>
            <div className="flex flex-col items-center">
                <span className="text-2xl font-bold tracking-tighter">MIT</span>
                <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Geltner Real Options</span>
            </div>
            <div className="flex flex-col items-center">
                <span className="text-2xl font-bold tracking-tighter">HARVARD</span>
                <span className="text-[10px] uppercase tracking-widest text-muted-foreground">ULI Strategic Path</span>
            </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="z-10 py-6 border-t border-border/40 text-center text-sm text-muted-foreground font-mono">
        ENGINE: POLARS-LAZY // INTERFACE: NEXT.JS-SHADCN // BUILD: PRODUCTION
      </footer>
    </main>
  );
}
