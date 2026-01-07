import sys
import os

# Add backend SOURCE to path (not just apps/backend repo root, but src parent if needed, or handle package mode)
# Structure: apps/backend/src
sys.path.append(os.path.join(os.path.dirname(__file__), "../apps/backend"))

# Important: The backend code expects to run as module usually, but for script we import directly.
from src.domain.schemas import ProjectTIV, ProductType
from src.engine.regulatory import RegulatoryEngine


def test_it11_compliance():
    print("--- Teste de Conformidade IT-11 (Bombeiros MG) ---")

    # Caso 1: Uso Misto SEM Núcleos Separados (Deve Falhar)
    project_fail = ProjectTIV(
        id="test-fail",
        name="Projeto Irregular",
        is_mixed_use=True,
        separate_access_cores=False,  # VIOLAÇÃO
    )

    is_ok, reasons = RegulatoryEngine.check_it11_compliance(project_fail)
    print(f"\n1. Projeto Irregular (Misto sem núcleo separado):")
    print(f"   Aprovado? {is_ok}")
    if not is_ok:
        print(f"   Motivo: {reasons[0]}")

    # Caso 2: Uso Misto COM Núcleos Separados (Deve Passar)
    project_pass = ProjectTIV(
        id="test-pass",
        name="Projeto Regular",
        is_mixed_use=True,
        separate_access_cores=True,  # OK
    )

    is_ok2, _ = RegulatoryEngine.check_it11_compliance(project_pass)
    print(f"\n2. Projeto Regular (Misto com núcleo separado):")
    print(f"   Aprovado? {is_ok2}")

    if not is_ok and is_ok2:
        print("\n✅ SUCESSO: Motor Regulatório IT-11 Validado.")
    else:
        print("\n❌ FALHA: Lógica incorreta.")


if __name__ == "__main__":
    test_it11_compliance()
