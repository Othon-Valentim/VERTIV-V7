"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api-client";

const MAX_UPLOAD_MB = 50;

export default function DataRoomUploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [legacySimId, setLegacySimId] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // UUID v4 strict regex — The Titanium Gate
  const uuidRegex =
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  const isUuidInvalid =
    legacySimId.trim() !== "" && !uuidRegex.test(legacySimId.trim());

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    setUploadError(null);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.toLowerCase().endsWith(".zip")) {
      setFile(droppedFile);
    } else {
      setUploadError("Apenas arquivos .zip são aceitos.");
    }
  }, []);

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setUploadError(null);
      const selected = e.target.files?.[0];
      if (selected && selected.name.toLowerCase().endsWith(".zip")) {
        setFile(selected);
      } else {
        setUploadError("Apenas arquivos .zip são aceitos.");
      }
    },
    [],
  );

  const handleSubmit = async () => {
    if (!file) return;
    // Titanium Gate: Block if UUID format is invalid
    if (isUuidInvalid) {
      setUploadError(
        "Erro: O ID de Calibração deve ser um UUID válido (36 caracteres) do histórico V6. Exemplo: bf2e52b9-203b-4e04-a22e-9a9f7f49bb1d",
      );
      return;
    }
    if (file.size > MAX_UPLOAD_MB * 1024 * 1024) {
      setUploadError(`Arquivo excede o limite de ${MAX_UPLOAD_MB} MB.`);
      return;
    }
    setIsUploading(true);
    setUploadError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);
      if (legacySimId.trim()) {
        formData.append("legacy_simulation_id", legacySimId.trim());
      }

      const res = await api.post("/api/v7/ingest", formData);

      if (!res.ok) {
        const errJson = await res.json().catch(() => null);
        const errText = await res.text().catch(() => "");
        const detail =
          errJson?.detail || errText || `Falha no upload (${res.status}).`;
        throw new Error(detail);
      }

      const data = await res.json();
      router.push(`/dashboard/audit/${data.ingestion_id}`);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Erro inesperado no upload.";
      setUploadError(message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center p-8">
      {/* Header */}
      <div className="mb-12 text-center">
        <div className="inline-flex items-center gap-2 mb-4">
          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
          <span className="text-xs uppercase tracking-[0.3em] text-zinc-500 font-mono">
            VERTIV V7 SINGULARITY
          </span>
        </div>
        <h1 className="text-4xl font-bold tracking-tight mb-2">
          Data Room{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
            Ingestão
          </span>
        </h1>
        <p className="text-zinc-500 text-sm max-w-md">
          Upload do ZIP com dados do empreendimento. O motor agêntico extrairá,
          validará e calculará automaticamente.
        </p>
      </div>

      {/* Dropzone */}
      <div
        className={`
          relative w-full max-w-xl border-2 border-dashed rounded-none p-16
          transition-all duration-200 cursor-pointer
          ${
            isDragging
              ? "border-emerald-400 bg-emerald-950/20"
              : file
                ? "border-emerald-600 bg-emerald-950/10"
                : "border-zinc-700 hover:border-zinc-500 bg-zinc-900/50"
          }
        `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById("file-input")?.click()}
      >
        <input
          id="file-input"
          type="file"
          accept=".zip"
          className="hidden"
          onChange={handleFileSelect}
        />

        <div className="flex flex-col items-center gap-4">
          {/* Icon */}
          <div
            className={`p-4 rounded-none border ${
              file
                ? "border-emerald-600 text-emerald-400"
                : "border-zinc-700 text-zinc-500"
            }`}
          >
            <svg
              className="w-8 h-8"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="square"
                strokeLinejoin="miter"
                strokeWidth={1.5}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>

          {file ? (
            <>
              <p className="text-sm font-mono text-emerald-400">{file.name}</p>
              <p className="text-xs text-zinc-500">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </>
          ) : (
            <>
              <p className="text-sm text-zinc-400">
                Arraste o <span className="font-mono text-zinc-200">.zip</span>{" "}
                aqui
              </p>
              <p className="text-xs text-zinc-600">ou clique para selecionar</p>
            </>
          )}
        </div>
      </div>

      {/* Legacy UUID Input (Calibration Mode) */}
      <div className="w-full max-w-xl mt-8">
        <label className="block text-xs uppercase tracking-[0.2em] text-zinc-500 font-mono mb-2">
          UUID de Calibração{" "}
          <span className="text-zinc-700">(opcional — Golden Forge)</span>
        </label>
        <input
          type="text"
          value={legacySimId}
          onChange={(e) => setLegacySimId(e.target.value)}
          placeholder="ex: bf2e52b9-203b-4e04-a22e-9a9f7f49bb1d"
          className={`
            w-full bg-zinc-900 border rounded-none px-4 py-3
            text-sm font-mono text-zinc-300 placeholder-zinc-700
            focus:outline-none transition-colors
            ${
              isUuidInvalid
                ? "border-red-600 focus:border-red-500"
                : "border-zinc-800 focus:border-emerald-600"
            }
          `}
        />
        {isUuidInvalid && (
          <p className="mt-2 text-xs text-red-400 font-mono">
            ✗ Formato inválido — use um UUID de 36 caracteres
            (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
          </p>
        )}
        {legacySimId.trim() && !isUuidInvalid && (
          <p className="mt-2 text-xs text-amber-500/80 font-mono">
            ⚡ Modo Calibração ativo — resultado será comparado com histórico V6
          </p>
        )}
      </div>

      {/* Error */}
      {uploadError && (
        <div className="w-full max-w-xl mt-4 p-3 bg-red-950/30 border border-red-800 text-red-400 text-sm font-mono">
          ✗ {uploadError}
        </div>
      )}

      {/* Submit */}
      <button
        onClick={handleSubmit}
        disabled={!file || isUploading || isUuidInvalid}
        className={`
          mt-8 px-12 py-4 font-mono text-sm uppercase tracking-[0.2em]
          transition-all duration-200 rounded-none
          ${
            !file || isUploading || isUuidInvalid
              ? "bg-zinc-800 text-zinc-600 cursor-not-allowed"
              : "bg-emerald-600 text-white hover:bg-emerald-500 active:bg-emerald-700"
          }
        `}
      >
        {isUploading ? (
          <span className="flex items-center gap-2">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            PROCESSANDO...
          </span>
        ) : (
          "INICIAR INGESTÃO"
        )}
      </button>

      {/* Footer Status */}
      <div className="mt-12 flex items-center gap-6 text-xs text-zinc-600 font-mono">
        <span>Motor: Polars Vectorized</span>
        <span className="text-zinc-800">|</span>
        <span>Provider: Gemini 2.5 Pro</span>
        <span className="text-zinc-800">|</span>
        <span>Validação: Golden Forge</span>
      </div>
    </div>
  );
}
