"""
VERTIV v6.1.0-SINGULARITY - Database Backup Script
Creates backups of Supabase database tables.

Usage:
    python scripts/backup_database.py
    python scripts/backup_database.py --tables simulations,analyses
    python scripts/backup_database.py --output /path/to/backup
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Try to import supabase
try:
    from supabase import create_client, Client
except ImportError:
    print("ERROR: supabase package not installed. Run: pip install supabase")
    sys.exit(1)

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Default tables to backup
DEFAULT_TABLES = ["simulations", "analyses"]


def get_supabase_client() -> Client:
    """Initialize Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY environment variables must be set.\n"
            "Export them or create a .env file."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def backup_table(client: Client, table_name: str, output_dir: Path) -> dict:
    """
    Backup a single table to JSON file.

    Returns:
        dict with backup metadata
    """
    print(f"Backing up table: {table_name}...")

    try:
        # Fetch all rows (paginated if large)
        response = client.table(table_name).select("*").execute()
        data = response.data

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{table_name}_{timestamp}.json"
        filepath = output_dir / filename

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "table": table_name,
                "timestamp": timestamp,
                "row_count": len(data),
                "data": data
            }, f, indent=2, default=str)

        print(f"  -> Saved {len(data)} rows to {filepath}")

        return {
            "table": table_name,
            "rows": len(data),
            "file": str(filepath),
            "success": True
        }

    except Exception as e:
        print(f"  -> ERROR: {e}")
        return {
            "table": table_name,
            "rows": 0,
            "file": None,
            "success": False,
            "error": str(e)
        }


def restore_table(client: Client, filepath: Path) -> dict:
    """
    Restore a table from a backup file.

    WARNING: This will insert data, potentially creating duplicates.
    Use with caution.
    """
    print(f"Restoring from: {filepath}...")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            backup = json.load(f)

        table_name = backup["table"]
        data = backup["data"]

        if not data:
            print(f"  -> No data to restore")
            return {"success": True, "rows": 0}

        # Insert data (upsert to avoid duplicates if id exists)
        response = client.table(table_name).upsert(data).execute()

        print(f"  -> Restored {len(data)} rows to {table_name}")

        return {
            "table": table_name,
            "rows": len(data),
            "success": True
        }

    except Exception as e:
        print(f"  -> ERROR: {e}")
        return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="VERTIV Database Backup Utility"
    )
    parser.add_argument(
        "--tables",
        type=str,
        default=",".join(DEFAULT_TABLES),
        help="Comma-separated list of tables to backup"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./backups",
        help="Output directory for backup files"
    )
    parser.add_argument(
        "--restore",
        type=str,
        default=None,
        help="Path to backup file to restore (instead of backing up)"
    )

    args = parser.parse_args()

    # Initialize client
    try:
        client = get_supabase_client()
        print("Connected to Supabase")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Restore mode
    if args.restore:
        filepath = Path(args.restore)
        if not filepath.exists():
            print(f"ERROR: File not found: {filepath}")
            sys.exit(1)
        result = restore_table(client, filepath)
        sys.exit(0 if result["success"] else 1)

    # Backup mode
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    tables = [t.strip() for t in args.tables.split(",")]

    print(f"\nVERTIV Database Backup")
    print(f"Date: {datetime.now().isoformat()}")
    print(f"Tables: {tables}")
    print(f"Output: {output_dir}")
    print("-" * 40)

    results = []
    for table in tables:
        result = backup_table(client, table, output_dir)
        results.append(result)

    # Summary
    print("\n" + "=" * 40)
    print("BACKUP SUMMARY")
    print("=" * 40)

    success_count = sum(1 for r in results if r["success"])
    total_rows = sum(r["rows"] for r in results if r["success"])

    print(f"Tables backed up: {success_count}/{len(tables)}")
    print(f"Total rows: {total_rows}")

    # Create manifest
    manifest_path = output_dir / f"manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(manifest_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "supabase_url": SUPABASE_URL,
            "tables": results
        }, f, indent=2)

    print(f"Manifest: {manifest_path}")

    if success_count < len(tables):
        print("\nWARNING: Some tables failed to backup!")
        sys.exit(1)

    print("\nBackup completed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
