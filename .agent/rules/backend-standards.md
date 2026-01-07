---
trigger: glob
globs: apps/backend/**/*.py
---

# BACKEND ENGINEERING STANDARDS (Python/FastAPI)

1. **Stack:** FastAPI, Pydantic v2, Polars, SQLAlchemy (Async).
2. **Database Pattern:**
   - Use `SQLAlchemy 2.0` syntax with `async/await`.
   - Never use blocking DB calls.
3. **API Contracts:**
   - All API inputs/outputs must be defined as Pydantic Models in `src/app/schemas`.
   - Ensure Snake_Case for Python and CamelCase for JSON responses.