from typing import List, Tuple
from src.domain.schemas import ProjectTIV


class RegulatoryEngine:
    """
    Validates regulatory constraints, including Fire Safety (IT-11) and Zoning.
    """

    @staticmethod
    def check_it11_compliance(project: ProjectTIV) -> Tuple[bool, List[str]]:
        """
        Validates IT-11 (Minas Gerais) requirements for Mixed-Use buildings.
        Rule: Mixed-use buildings MUST have independent access cores (staircases/entries)
        for residential and commercial uses.

        Returns:
            (is_compliant: bool, reasons: List[str])
        """
        reasons = []
        is_compliant = True

        if project.is_mixed_use:
            if not project.separate_access_cores:
                is_compliant = False
                reasons.append(
                    "FATAL: Mixed-Use project lacks separate access cores (IT-11 violation). "
                    "Residential and Commercial flows must be independent."
                )

        # Future Rules: Fire Load calculation based on 'fire_load_category'
        # if project.fire_load_category == "Industrial" and ...

        return is_compliant, reasons

    @staticmethod
    def apply_it11_efficiency_penalty(
        typology: str, current_efficiency: float
    ) -> float:
        """
        Applies a penalty to the project's efficiency (sellable area ratio) if it is mixed-use,
        reflecting the loss of area due to duplicated circulation cores required by IT-11 (Minas Gerais).

        Args:
            typology (str): The product type/typology (e.g., "MISTO", "VERTICAL_RESIDENCIAL").
            current_efficiency (float): The base efficiency of the project (sellable/total area).

        Returns:
            float: The adjusted efficiency.
        """
        # IT-11 Penalty: Mixed-Use projects lose ~15% efficiency due to separate cores
        if typology == "MISTO":
            penalty_factor = 0.85
            return current_efficiency * penalty_factor

        return current_efficiency
