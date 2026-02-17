"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Loader2, LogIn, Eye, EyeOff, Building2, ArrowRight } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const { signIn } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const { error } = await signIn(email, password);

      if (error) {
        if (error.message.includes("Invalid login")) {
          setError("Email ou senha incorretos.");
        } else {
          setError(error.message);
        }
        return;
      }

      router.push("/wizard");
    } catch (err: any) {
      setError("Erro ao fazer login. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen seamless-bg flex">
      {/* Left Side - Branding (Monolithic) */}
      <div className="hidden lg:flex lg:w-1/2 bg-primary relative overflow-hidden">
        {/* Monolithic Background Texture */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.05)_0%,transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(255,255,255,0.02)_0%,transparent_50%)]" />

        <div className="relative z-10 flex flex-col justify-between p-12 text-white">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 bg-white/10 backdrop-blur-sm rounded-sm flex items-center justify-center border border-white/10">
              <Building2 className="h-7 w-7 text-white" />
            </div>
            <span className="text-2xl font-black tracking-tighter uppercase">
              VERTIV<span className="text-secondary opacity-80">.global</span>
            </span>
          </div>

          {/* Main content */}
          <div className="space-y-6">
            <h1 className="text-5xl xl:text-6xl font-black leading-none monolithic-headline text-white">
              TITANIUM<br/>FEASIBILITY
            </h1>
            <p className="text-lg text-white/80 max-w-md">
              Plataforma completa para análise, simulação e tomada de decisão em investimentos imobiliários comerciais.
            </p>
            <div className="flex items-center gap-4 pt-4">
              <div className="flex -space-x-3">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="w-10 h-10 rounded-full bg-white/20 border-2 border-white/30 backdrop-blur-sm"
                  />
                ))}
              </div>
              <p className="text-sm text-white/70">
                +500 profissionais confiam na plataforma
              </p>
            </div>
          </div>

          {/* Features */}
          <div className="grid grid-cols-2 gap-4">
            {[
              "Análise DCF Avançada",
              "Simulação Monte Carlo",
              "Real Options",
              "Relatórios Automáticos",
            ].map((feature) => (
              <div
                key={feature}
                className="flex items-center gap-2 text-sm text-white/80"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-white/60" />
                {feature}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-6 sm:p-12 relative">
        {/* Background pattern */}
        <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] [background-size:20px_20px] opacity-50" />

        <div className="relative w-full max-w-md animate-fade-in">
          {/* Mobile Logo */}
          <div className="lg:hidden text-center mb-8">
            <Link href="/" className="inline-flex items-center gap-2">
              <div className="h-10 w-10 bg-primary rounded-sm flex items-center justify-center">
                <Building2 className="h-6 w-6 text-primary-foreground" />
              </div>
              <span className="text-2xl font-bold tracking-tight">
                VERTIV<span className="text-primary">.global</span>
              </span>
            </Link>
          </div>

          {/* Header */}
          <div className="text-center mb-10">
            <h2 className="text-3xl font-black tracking-tighter uppercase text-primary">
              Access Core
            </h2>
            <div className="h-1 w-12 bg-secondary mx-auto mt-4" />
          </div>

          {/* Login Card */}
          <div className="bg-card border border-primary/10 rounded-sm p-10 shadow-elevated relative overflow-hidden">
            {/* Seamless side-bar equivalent inside card */}
            <div className="absolute top-0 left-0 w-1 h-full bg-secondary" />
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-xl text-destructive text-sm flex items-center gap-2 animate-scale-in">
                  <div className="w-2 h-2 rounded-full bg-destructive animate-pulse" />
                  {error}
                </div>
              )}

              <div className="space-y-2">
                <label className="text-sm font-medium text-foreground">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-field"
                  placeholder="seu@email.com"
                  required
                  autoComplete="email"
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium text-foreground">
                    Senha
                  </label>
                  <Link
                    href="/auth/forgot-password"
                    className="text-xs text-primary hover:text-primary/80 transition-colors font-medium"
                  >
                    Esqueceu a senha?
                  </Link>
                </div>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="input-field pr-12"
                    placeholder="••••••••"
                    required
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn-pill btn-primary w-full h-12 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed group"
              >
                {loading ? (
                  <Loader2 className="h-5 w-5 animate-spin" />
                ) : (
                  <>
                    Entrar na plataforma
                    <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>

            <div className="relative my-8">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-3 text-muted-foreground">
                  ou
                </span>
              </div>
            </div>

            <div className="text-center text-sm text-muted-foreground">
              Ainda não tem conta?{" "}
              <Link
                href="/auth/register"
                className="text-primary font-semibold hover:text-primary/80 transition-colors"
              >
                Criar conta gratuita
              </Link>
            </div>
          </div>

          {/* Footer */}
          <p className="text-center text-xs text-muted-foreground mt-8">
            Ao entrar, você concorda com nossos{" "}
            <Link
              href="/terms"
              className="text-foreground/70 hover:text-primary transition-colors underline underline-offset-2"
            >
              Termos de Uso
            </Link>{" "}
            e{" "}
            <Link
              href="/privacy"
              className="text-foreground/70 hover:text-primary transition-colors underline underline-offset-2"
            >
              Política de Privacidade
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
