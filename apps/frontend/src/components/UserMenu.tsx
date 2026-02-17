"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { User, LogOut, Settings, ChevronDown } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function UserMenu() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSignOut = async () => {
    await signOut();
    router.push("/");
  };

  if (!user) {
    return (
      <a
        href="/auth/login"
        className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
      >
        Entrar
      </a>
    );
  }

  const userName = user.user_metadata?.full_name || user.email?.split("@")[0] || "Usuario";
  const userInitial = userName.charAt(0).toUpperCase();

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 p-2 rounded-sm hover:bg-secondary/20 transition-colors"
      >
        <div className="h-8 w-8 rounded-sm bg-primary flex items-center justify-center text-white font-bold text-sm">
          {userInitial}
        </div>
        <span className="text-sm font-bold text-primary hidden md:block">{userName}</span>
        <ChevronDown className={`h-4 w-4 text-primary transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white border border-primary/20 rounded-sm shadow-xl py-1 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="px-4 py-3 border-b border-primary/10">
            <p className="text-sm font-bold text-primary truncate">{userName}</p>
            <p className="text-xs text-muted-foreground truncate">{user.email}</p>
          </div>

          <div className="py-1">
            <button
              onClick={() => {
                setIsOpen(false);
                router.push("/settings");
              }}
              className="w-full flex items-center gap-3 px-4 py-2 text-sm text-foreground hover:bg-accent/50 transition-colors"
            >
              <Settings className="h-4 w-4" />
              Configuracoes
            </button>
            <button
              onClick={() => {
                setIsOpen(false);
                // In a real app, this might open a modal or a docs route
                // For now, we simulate accessibility.
                window.open('https://docs.vertiv.tech', '_blank');
              }}
              className="w-full flex items-center gap-3 px-4 py-2 text-sm text-foreground hover:bg-accent/50 transition-colors"
            >
              <User className="h-4 w-4" />
              Manual de Operacoes
            </button>
          </div>

          <div className="border-t border-border py-1">
            <button
              onClick={handleSignOut}
              className="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-500 hover:bg-red-500/10 transition-colors"
            >
              <LogOut className="h-4 w-4" />
              Sair
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
