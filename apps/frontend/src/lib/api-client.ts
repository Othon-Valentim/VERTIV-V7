import { createClient } from "./supabase";
import type {
  ConfirmSentenceRequest,
  IngestResponse,
  IngestionActionResponse,
  IngestionDetail,
  ManualAuditRequest,
} from "../types/v7-api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function isFormDataBody(body: BodyInit | null | undefined): body is FormData {
  return typeof FormData !== "undefined" && body instanceof FormData;
}

function headersToObject(headers?: HeadersInit): Record<string, string> {
  if (!headers) return {};
  if (headers instanceof Headers) {
    return Object.fromEntries(headers.entries());
  }
  if (Array.isArray(headers)) {
    return Object.fromEntries(headers);
  }
  return headers;
}

export async function authenticatedFetch(
  path: string,
  options: RequestInit = {},
) {
  const supabase = createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();
  const token = session?.access_token;

  const headers: Record<string, string> = {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...headersToObject(options.headers),
  };

  const hasContentType = Object.keys(headers).some(
    (key) => key.toLowerCase() === "content-type",
  );

  // Let the browser set multipart boundaries for FormData bodies.
  if (isFormDataBody(options.body)) {
    for (const key of Object.keys(headers)) {
      if (key.toLowerCase() === "content-type") {
        delete headers[key];
      }
    }
  } else if (!hasContentType) {
    headers["Content-Type"] = "application/json";
  }

  const url = path.startsWith("http")
    ? path
    : `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;

  const res = await fetch(url, {
    ...options,
    headers,
  });

  if (res.status === 401) {
    console.error("API Authentication failed (401).");
    // Optional: redirect to login or refresh session
  }

  return res;
}

export const api = {
  get: (path: string, options?: RequestInit) =>
    authenticatedFetch(path, { ...options, method: "GET" }),
  post: (path: string, body: any, options?: RequestInit) =>
    authenticatedFetch(path, {
      ...options,
      method: "POST",
      body: isFormDataBody(body) ? body : JSON.stringify(body),
    }),
  put: (path: string, body: any, options?: RequestInit) =>
    authenticatedFetch(path, {
      ...options,
      method: "PUT",
      body: isFormDataBody(body) ? body : JSON.stringify(body),
    }),
  delete: (path: string, options?: RequestInit) =>
    authenticatedFetch(path, { ...options, method: "DELETE" }),
};

export type {
  ConfirmSentenceRequest,
  IngestResponse,
  IngestionActionResponse,
  IngestionDetail,
  ManualAuditRequest,
};

export type ManualAuditPayload = ManualAuditRequest;
export type ConfirmSentencePayload = ConfirmSentenceRequest;

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly detail?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function parseErrorResponse(res: Response): Promise<ApiError> {
  const body = await res.json().catch(() => null);
  const text = body ? "" : await res.text().catch(() => "");
  const detail = body?.detail ?? text;
  const message =
    typeof detail === "string" && detail
      ? detail
      : `Falha na API (${res.status}).`;
  return new ApiError(message, res.status, detail);
}

async function readJsonOrThrow<T>(res: Response): Promise<T> {
  if (!res.ok) {
    throw await parseErrorResponse(res);
  }
  return res.json() as Promise<T>;
}

export async function ingestDataRoom(
  formData: FormData,
): Promise<IngestResponse> {
  return readJsonOrThrow<IngestResponse>(
    await api.post("/api/v7/ingest", formData),
  );
}

export async function getIngestion(
  ingestionId: string,
): Promise<IngestionDetail> {
  return readJsonOrThrow<IngestionDetail>(
    await api.get(`/api/v7/ingestion/${ingestionId}`),
  );
}

export async function requestManualAudit(
  ingestionId: string,
  payload: ManualAuditRequest,
): Promise<IngestionActionResponse> {
  return readJsonOrThrow<IngestionActionResponse>(
    await api.post(
      `/api/v7/ingestion/${ingestionId}/manual-audit`,
      payload,
      payload.idempotency_key
        ? { headers: { "Idempotency-Key": payload.idempotency_key } }
        : undefined,
    ),
  );
}

export async function confirmSentence(
  ingestionId: string,
  payload: ConfirmSentenceRequest,
): Promise<IngestionActionResponse> {
  return readJsonOrThrow<IngestionActionResponse>(
    await api.post(
      `/api/v7/ingestion/${ingestionId}/confirm-sentence`,
      payload,
      payload.idempotency_key
        ? { headers: { "Idempotency-Key": payload.idempotency_key } }
        : undefined,
    ),
  );
}
