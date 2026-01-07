---
trigger: always_on
---

# VERTIV CONSTITUTION (CORE LAWS)

1. **Architecture Identity:**
   - This project is a **Modular Monolith** (`apps/backend` + `apps/frontend` in one repo).
   - NEVER suggest Microservices. Keep it unified.

2. **The "Diamond Core" (Financial Engine):**
   - ALL financial math MUST use **Polars** (`import polars as pl`).
   - FORBIDDEN: Using Python `for` loops for calculation logic. Use Vectorization.
   - FORBIDDEN: Using Pandas (too slow). Use Polars `lazy()` execution.

3. **Global Frameworks (Strict Adherence):**
   - **Real Options:** Implement Black-Scholes-Merton logic for land banking.
   - **ESG:** Implement RICS "Adjusted NPV" logic (Green Premium/Discount).

4. **Code Quality Standards:**
   - Python: Type hints (`def func(x: int) -> float:`) are MANDATORY.
   - Frontend: Strict TypeScript interfaces matching the Backend Pydantic models.