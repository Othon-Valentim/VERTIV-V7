import { createClient } from "./supabase";

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
