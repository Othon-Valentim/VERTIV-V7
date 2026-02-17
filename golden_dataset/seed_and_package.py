"""
Seed golden_simulations into Supabase and generate Data Room ZIPs.
Reads simulation_results.json + benchmark_projects.json,
inserts into Supabase golden_simulations table, then creates
individual ZIP Data Rooms for each project.
"""

import json
import os
import sys
import zipfile
import uuid
from pathlib import Path
from datetime import datetime

# Add backend to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


def load_data() -> tuple:
    """Load simulation results and benchmark projects."""
    with open(SCRIPT_DIR / "simulation_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)
    with open(SCRIPT_DIR / "benchmark_projects.json", "r", encoding="utf-8") as f:
        projects = json.load(f)
    # Index projects by dataset_id
    projects_map = {p["dataset_id"]: p for p in projects}
    return results, projects_map


def extract_segment(project: dict) -> str:
    """Extract segment label from project data."""
    p6 = project.get("p6", {})
    segment = p6.get("target_segment", "UNKNOWN")
    return segment


def extract_metrics(result: dict) -> dict:
    """Extract key financial metrics from simulation result."""
    cf = result.get("cashflow_metrics", {})
    p3 = result.get("p3", {})
    p9 = result.get("p9", {})

    return {
        "vpl": cf.get("npv", p3.get("npv", 0)),
        "tir_annual": cf.get("irr_annual", 0),
        "roi_pct": round(p3.get("roi", 0) * 100, 2) if p3.get("roi") else 0,
        "is_viable": p3.get("is_viable", False),
        "p9_decision": p9.get("gate_result", {}).get("decision", "N/A"),
    }


def seed_supabase(results: list, projects_map: dict) -> list:
    """Insert simulations into Supabase via REST API and return UUIDs."""
    try:
        import httpx
    except ImportError:
        print("Installing httpx...")
        os.system(f"{sys.executable} -m pip install httpx -q")
        import httpx

    # Supabase config
    SUPABASE_URL = "https://nutilcpmpapjowqmxoqf.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dGlsY3BtcGFwam93cW14b3FmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU5NDg1OTksImV4cCI6MjA4MTUyNDU5OX0.VhvEhOJOLc_Xkf2BvMQs4IbqcJtnmSEXPNfMwvuPXgY"

    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    records = []
    for result in results:
        did = result["dataset_id"]
        project = projects_map.get(did, {})
        metrics = extract_metrics(result)

        record = {
            "id": str(uuid.uuid4()),
            "dataset_id": did,
            "project_name": result.get("project_name", ""),
            "municipality": result.get("municipality", ""),
            "segment": extract_segment(project),
            "vpl": float(metrics["vpl"]),
            "tir_annual": float(metrics["tir_annual"]),
            "roi_pct": float(metrics["roi_pct"]),
            "is_viable": metrics["is_viable"],
            "p9_decision": metrics["p9_decision"],
            "simulation_data": result,
        }
        records.append(record)

    # Upsert via REST API
    with httpx.Client(timeout=30) as client:
        resp = client.post(
            f"{SUPABASE_URL}/rest/v1/golden_simulations",
            headers={
                **headers,
                "Prefer": "return=representation,resolution=merge-duplicates",
            },
            json=records,
        )
        if resp.status_code in (200, 201):
            inserted = resp.json()
            print(
                f"\n✅ {len(inserted)} records upserted into Supabase golden_simulations\n"
            )
            return inserted
        else:
            print(f"\n❌ Supabase error {resp.status_code}: {resp.text}")
            # Fallback: return records with generated UUIDs
            return records


def create_data_rooms(results: list, projects_map: dict, uuids_map: dict) -> None:
    """Create individual ZIP Data Rooms for each project."""
    data_rooms_dir = SCRIPT_DIR / "data_rooms"
    data_rooms_dir.mkdir(exist_ok=True)

    for result in results:
        did = result["dataset_id"]
        project = projects_map.get(did, {})
        metrics = extract_metrics(result)
        sim_uuid = uuids_map.get(did, "N/A")

        # Clean project name for filename
        name_clean = result.get("project_name", did).replace(" ", "_").replace("—", "-")
        name_clean = "".join(c for c in name_clean if c.isalnum() or c in "_-")
        zip_name = f"{did}_{name_clean[:50]}.zip"
        zip_path = data_rooms_dir / zip_name

        # Build Data Room contents
        resumo = {
            "legacy_simulation_id": sim_uuid,
            "dataset_id": did,
            "project_name": result.get("project_name"),
            "municipality": result.get("municipality"),
            "segment": extract_segment(project),
            "generated_at": datetime.now().isoformat(),
            "key_metrics": {
                "vpl_brl": round(metrics["vpl"], 2),
                "tir_annual_pct": metrics["tir_annual"],
                "roi_pct": metrics["roi_pct"],
                "is_viable": metrics["is_viable"],
                "p9_gate": metrics["p9_decision"],
            },
            "engine_version": "VERTIV V6 → V7 Calibration",
        }

        # Market analysis bundle
        market = {
            "p6_demand": result.get("p6", {}),
            "p7_supply": result.get("p7", {}),
            "p8_absorption": result.get("p8", {}),
            "p9_gate": result.get("p9", {}),
        }

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(
                "00_RESUMO.json", json.dumps(resumo, indent=2, ensure_ascii=False)
            )
            zf.writestr(
                "01_INPUT_DATA.json", json.dumps(project, indent=2, ensure_ascii=False)
            )
            zf.writestr(
                "02_ENGINE_RESULTS.json",
                json.dumps(result, indent=2, ensure_ascii=False),
            )
            zf.writestr(
                "03_CASHFLOW.json",
                json.dumps(
                    result.get("cashflow_metrics", {}), indent=2, ensure_ascii=False
                ),
            )
            zf.writestr(
                "04_MARKET_ANALYSIS.json",
                json.dumps(market, indent=2, ensure_ascii=False),
            )
            zf.writestr(
                "05_LEGAL_DILIGENCE.json",
                json.dumps(result.get("p5", {}), indent=2, ensure_ascii=False),
            )
            zf.writestr(
                "06_REAL_OPTIONS.json",
                json.dumps(
                    {"real_options_value": result.get("real_options_value", 0)},
                    indent=2,
                    ensure_ascii=False,
                ),
            )

        size_kb = zip_path.stat().st_size / 1024
        print(f"  📦 {zip_name} ({size_kb:.1f} KB)")

    print(f"\n✅ {len(results)} Data Room ZIPs created in: {data_rooms_dir}")


def print_uuid_table(records: list) -> None:
    """Print formatted UUID table for Mentor review."""
    print("\n" + "=" * 100)
    print("  GOLDEN DATASET — LEGACY SIMULATION IDs (para envio ao Mentor Senior)")
    print("=" * 100)
    print(f"  {'ID':<14} {'Projeto':<55} {'UUID (legacy_simulation_id)'}")
    print("  " + "─" * 96)

    for r in records:
        did = r.get("dataset_id", "")
        name = r.get("project_name", "")[:52]
        uid = r.get("id", "N/A")
        print(f"  {did:<14} {name:<55} {uid}")

    print("  " + "─" * 96)
    print(f"  Total: {len(records)} simulações")
    print("=" * 100)


def main():
    print("🚀 VERTIV Golden Dataset — Supabase Seed + Data Room Generator\n")

    # 1. Load data
    print("📂 Loading data...")
    results, projects_map = load_data()
    print(
        f"   Found {len(results)} simulation results, {len(projects_map)} benchmark projects\n"
    )

    # 2. Seed Supabase
    print("☁️  Seeding Supabase golden_simulations...")
    inserted = seed_supabase(results, projects_map)

    # Build UUID map
    uuids_map = {r["dataset_id"]: r["id"] for r in inserted}

    # 3. Print UUID table
    print_uuid_table(inserted)

    # 4. Create Data Room ZIPs
    print("\n📦 Creating Data Room ZIPs...")
    create_data_rooms(results, projects_map, uuids_map)

    # 5. Save UUID manifest
    manifest_path = SCRIPT_DIR / "data_rooms" / "MANIFEST_UUIDs.json"
    manifest = [
        {
            "dataset_id": r["dataset_id"],
            "project_name": r["project_name"],
            "legacy_simulation_id": r["id"],
            "is_viable": r.get("is_viable"),
            "vpl": r.get("vpl"),
            "tir_annual": r.get("tir_annual"),
        }
        for r in inserted
    ]
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\n📋 UUID manifest saved to: {manifest_path}")

    print("\n✅ DONE. Share the UUIDs with the Mentor Senior.")


if __name__ == "__main__":
    main()
