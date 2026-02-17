import { createClient } from './supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function authenticatedFetch(path: string, options: RequestInit = {}) {
  const supabase = createClient();
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  const headers = {
    "Content-Type": "application/json",
    ...(token ? { "Authorization": `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const url = path.startsWith("http") ? path : `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;

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
  get: (path: string, options?: RequestInit) => authenticatedFetch(path, { ...options, method: 'GET' }),
  post: (path: string, body: any, options?: RequestInit) => authenticatedFetch(path, { 
    ...options, 
    method: 'POST', 
    body: JSON.stringify(body) 
  }),
  put: (path: string, body: any, options?: RequestInit) => authenticatedFetch(path, { 
    ...options, 
    method: 'PUT', 
    body: JSON.stringify(body) 
  }),
  delete: (path: string, options?: RequestInit) => authenticatedFetch(path, { ...options, method: 'DELETE' }),
};
