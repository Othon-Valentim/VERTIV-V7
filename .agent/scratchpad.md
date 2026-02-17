# SCRATCHPAD: VERTIV Corporate Architect Upgrade

## Current Context
- **Security Hardening:** Updated `.antigravityrules` with "Minimum Privilege" (blocked webhooks, restricted terminal commands).
- **Project Requirements:** Created `REQUIREMENTS.md` with technical non-negotiables.
- **Protocol Manus:** Initialized `.agent/rules/protocol_manus.md`.
- **Pending Issue:** Airtable automation `A04_NURTURE_SCHEDULER` failing since Jan 7th.

## Initial Observations
- **GCP Billing:** `build_error.txt` shows `vertiv-prod-v1` has a disabled billing account (state: delinquent). This might be a global issue affecting multiple SaaS accounts if they share the same credit card/owner.
- **Worker Errors:** `worker_log.txt` shows an import error (`No module named 'src'`) and a port binding error (10048).
- **Airtable Code:** Not found in `apps/` or root. Re-searching for Airtable integrations.

## Debugging Airtable (A04_NURTURE_SCHEDULER)
- **Status:** Automation is highly likely external (Airtable native or n8n) calling `https://worker.vertiv.tech/tasks/process-simulation`.
- **Primary Failure:** GCP Billing delinquent -> Service Stopped.
- **Secondary Failure:** Code errors (`No module named 'src'`, busy ports) would block recovery even if billing is fixed.
- **Action Taken:**
    - [x] Fixed `PYTHONPATH` in `apps/worker/core/main.py`.
    - [x] Created `scripts/kill_ports.py` to clear development environment.
    - [x] Created `scripts/verify_worker_local.py` to simulate Airtable payload.

## UI Upgrade: Monolithic Seamless (Arquiteto Valentim Hou)
### Design Palette (Tropicalization: Monofloor Spirit)
- **Everest (Backgrounds/Surfaces):** `hsl(0 0% 96%)` - Off-white, clean, spacious.
- **Kalahari (Secondary/Accents):** `hsl(35 30% 85%)` - Warm sand, organic.
- **Arabia (Headings/Primary):** `hsl(25 40% 15%)` - Deep earth, authoritative.

### Architectural Decisions
1. **Layout:** Remove sharp borders. Use `box-shadow: 0 4px 20px -5px rgba(0,0,0,0.05)` for floating surfaces.
2. **Typography:** Lock `Outfit` font weights. Heavy `700` for "Arabia" headings, Light `300` for descriptions.
3. **Seamlessness:** Integrated background transitions between Sidebar and Content.
4. **Componentization:** "Monolithic" blocks (large, solid surfaces) instead of fragmented cards.
