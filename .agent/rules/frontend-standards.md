---
trigger: glob
globs: apps/frontend/**/*.{ts,tsx}
---

# FRONTEND ENGINEERING STANDARDS (Next.js)

1. **Stack:** Next.js 14 (App Router), Tailwind CSS, Lucide Icons.
2. **Components:**
   - Use **Shadcn/UI** components for all UI elements. Do not invent custom CSS unless necessary.
   - Use `lucide-react` for icons.
3. **Data Fetching:**
   - Use typed fetch wrappers.
   - NEVER hardcode API URLs. Use `process.env.NEXT_PUBLIC_API_URL`.