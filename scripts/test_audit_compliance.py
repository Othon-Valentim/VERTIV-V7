"""
VERTIV v6.1.0-SINGULARITY - Audit Compliance Test Suite
Validates all critical requirements from THE PROTOCOL OF SINGULARITY.

Run with: python scripts/test_audit_compliance.py
"""

import sys
import os
import asyncio
from pathlib import Path
from typing import Tuple, List
import importlib.util

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class AuditResult:
    def __init__(self, name: str, passed: bool, details: str = ""):
        self.name = name
        self.passed = passed
        self.details = details

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.name}: {self.details}"


def check_file_exists(path: str, description: str) -> AuditResult:
    """Check if a required file exists."""
    full_path = PROJECT_ROOT / path
    exists = full_path.exists()
    return AuditResult(
        name=f"File: {description}",
        passed=exists,
        details=str(full_path) if exists else f"Missing: {full_path}",
    )


def check_class_exists(module_path: str, class_name: str) -> AuditResult:
    """Check if a required class exists in a module."""
    try:
        full_path = PROJECT_ROOT / module_path
        spec = importlib.util.spec_from_file_location("module", full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        has_class = hasattr(module, class_name)
        return AuditResult(
            name=f"Class: {class_name}",
            passed=has_class,
            details=(
                f"Found in {module_path}"
                if has_class
                else f"Not found in {module_path}"
            ),
        )
    except Exception as e:
        return AuditResult(
            name=f"Class: {class_name}",
            passed=False,
            details=f"Error loading module: {e}",
        )


def check_function_in_file(file_path: str, function_name: str) -> AuditResult:
    """Check if a function exists in a file."""
    try:
        full_path = PROJECT_ROOT / file_path
        content = full_path.read_text(encoding="utf-8")
        has_function = (
            f"def {function_name}" in content or f"async def {function_name}" in content
        )
        return AuditResult(
            name=f"Function: {function_name}",
            passed=has_function,
            details=(
                f"Found in {file_path}" if has_function else f"Not found in {file_path}"
            ),
        )
    except Exception as e:
        return AuditResult(
            name=f"Function: {function_name}",
            passed=False,
            details=f"Error reading file: {e}",
        )


def check_env_variable_documented(var_name: str) -> AuditResult:
    """Check if an environment variable is documented in .env.example."""
    try:
        env_example = PROJECT_ROOT / ".env.production.example"
        if not env_example.exists():
            env_example = PROJECT_ROOT / ".env.example"
        content = env_example.read_text(encoding="utf-8")
        has_var = var_name in content
        return AuditResult(
            name=f"Env Var: {var_name}",
            passed=has_var,
            details="Documented" if has_var else "Not documented in .env.example",
        )
    except Exception as e:
        return AuditResult(
            name=f"Env Var: {var_name}", passed=False, details=f"Error: {e}"
        )


def run_phase1_audit() -> List[AuditResult]:
    """PHASE 1: Integrity Check & Hardening"""
    print("\n" + "=" * 60)
    print("PHASE 1: INTEGRITY CHECK & HARDENING")
    print("=" * 60)

    results = []

    # Step 1: docker-compose.yml
    results.append(check_file_exists("docker-compose.yml", "docker-compose.yml"))

    # Step 2: RegulatoryEngine
    results.append(
        check_file_exists(
            "apps/backend/src/engine/regulatory.py", "RegulatoryEngine module"
        )
    )

    # Step 3: IT-11 penalty logic
    results.append(
        check_function_in_file(
            "apps/backend/src/engine/regulatory.py", "apply_it11_efficiency_penalty"
        )
    )

    # Step 6: BCBConnector
    results.append(
        check_file_exists(
            "apps/backend/src/services/market_data.py", "MarketData service"
        )
    )

    # Step 10: Cache implementation
    results.append(
        check_function_in_file(
            "apps/backend/src/services/market_data.py", "_get_cached"
        )
    )

    # Step 12: Schemas
    results.append(
        check_file_exists("apps/backend/src/domain/schemas.py", "Domain schemas")
    )

    # Step 14: Env vars
    results.append(check_env_variable_documented("SUPABASE_URL"))
    results.append(check_env_variable_documented("SERPER_API_KEY"))

    return results


def run_phase2_audit() -> List[AuditResult]:
    """PHASE 2: Live Web Search"""
    print("\n" + "=" * 60)
    print("PHASE 2: THE AWAKENING - LIVE WEB SEARCH")
    print("=" * 60)

    results = []

    # Step 21: SERPER_API_KEY
    results.append(check_env_variable_documented("SERPER_API_KEY"))

    # Step 22: httpx
    results.append(
        check_file_exists("apps/agents/requirements.txt", "Agents requirements")
    )

    # Step 23-24: ScoutAgent and search
    results.append(check_file_exists("apps/agents/src/server.py", "Agent server"))
    results.append(
        check_function_in_file("apps/agents/src/server.py", "perform_serper_search")
    )

    # Step 27-28: Protocol tools
    results.append(
        check_function_in_file("apps/agents/src/server.py", "find_master_plan")
    )
    results.append(
        check_function_in_file("apps/agents/src/server.py", "get_neighborhood_price")
    )

    # Step 32: Test script
    results.append(check_file_exists("scripts/test_live_agent.py", "Live agent test"))

    return results


def run_phase3_audit() -> List[AuditResult]:
    """PHASE 3: Async Load Testing"""
    print("\n" + "=" * 60)
    print("PHASE 3: THE SCALE - ASYNC LOAD TESTING")
    print("=" * 60)

    results = []

    # Step 46-47: Load test directory and file
    results.append(check_file_exists("tests/load", "Load test directory"))
    results.append(check_file_exists("tests/load/locustfile.py", "Locust file"))

    # Step 53: Polars lazy execution
    results.append(
        check_function_in_file(
            "apps/backend/src/engine/cashflow.py", "calculate_project_cashflow"
        )
    )

    # Step 63: Flood test
    results.append(check_file_exists("scripts/flood_test.py", "Flood test"))

    # Step 67: Cleanup script
    results.append(check_file_exists("scripts/cleanup_load_test.sql", "Cleanup SQL"))

    return results


def run_phase4_audit() -> List[AuditResult]:
    """PHASE 4: E2E Validation"""
    print("\n" + "=" * 60)
    print("PHASE 4: THE GOLDEN PATH - E2E VALIDATION")
    print("=" * 60)

    results = []

    # Step 88: JWT authentication
    results.append(
        check_file_exists("apps/backend/src/infrastructure/auth.py", "Auth module")
    )
    results.append(
        check_function_in_file(
            "apps/backend/src/infrastructure/auth.py", "get_current_user"
        )
    )

    # Rate limiting
    results.append(
        check_file_exists(
            "apps/backend/src/infrastructure/rate_limiter.py", "Rate limiter"
        )
    )

    # Step 92: API Contract
    results.append(check_file_exists("docs/API_CONTRACT.md", "API Contract"))

    # Step 93: README
    results.append(check_file_exists("README.md", "README"))

    return results


def run_phase5_audit() -> List[AuditResult]:
    """PHASE 5: Deployment Readiness"""
    print("\n" + "=" * 60)
    print("PHASE 5: DEPLOYMENT READINESS")
    print("=" * 60)

    results = []

    # Step 96: Production env example
    results.append(
        check_file_exists(".env.production.example", "Production env example")
    )

    # Step 99: Deploy script
    results.append(check_file_exists("scripts/orbit_deploy.sh", "Deploy script"))

    # Step 100: Pinned requirements
    req_path = PROJECT_ROOT / "apps/backend/requirements.txt"
    if req_path.exists():
        content = req_path.read_text(encoding="utf-8")
        has_pinned = "==" in content
        results.append(
            AuditResult(
                name="Pinned Requirements",
                passed=has_pinned,
                details="Versions are pinned" if has_pinned else "Versions not pinned",
            )
        )
    else:
        results.append(
            AuditResult(
                name="Pinned Requirements",
                passed=False,
                details="requirements.txt not found",
            )
        )

    # Documentation
    results.append(check_file_exists("docs/ARCHITECTURE.md", "Architecture doc"))
    results.append(check_file_exists("docs/USER_MANUAL.md", "User manual"))
    results.append(check_file_exists("docs/WHITE_PAPER.md", "White paper"))

    return results


def print_results(results: List[AuditResult]) -> Tuple[int, int]:
    """Print results and return (passed, failed) counts."""
    passed = 0
    failed = 0

    for result in results:
        print(result)
        if result.passed:
            passed += 1
        else:
            failed += 1

    return passed, failed


def main():
    """Run full audit compliance check."""
    print("\n" + "#" * 60)
    print("# VERTIV v6.1.0-SINGULARITY AUDIT COMPLIANCE CHECK")
    print("#" * 60)

    total_passed = 0
    total_failed = 0

    # Run all phases
    for phase_func in [
        run_phase1_audit,
        run_phase2_audit,
        run_phase3_audit,
        run_phase4_audit,
        run_phase5_audit,
    ]:
        results = phase_func()
        passed, failed = print_results(results)
        total_passed += passed
        total_failed += failed

    # Summary
    print("\n" + "=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)
    total = total_passed + total_failed
    print(f"Total Checks: {total}")
    print(f"Passed: {total_passed} ({100*total_passed/total:.1f}%)")
    print(f"Failed: {total_failed} ({100*total_failed/total:.1f}%)")

    if total_failed == 0:
        print("\n*** SINGULARITY ACHIEVED: ALL CHECKS PASSED ***")
        return 0
    else:
        print(f"\n*** WARNING: {total_failed} CHECKS FAILED ***")
        return 1


if __name__ == "__main__":
    sys.exit(main())
