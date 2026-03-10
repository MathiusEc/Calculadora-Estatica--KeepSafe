from typing import List

from src.domain.entities.mixture import Mixture, MixtureResult
from src.domain.entities.product import MixtureProduct


class MixtureCalculatorService:
    """Servicio de dominio para cálculos de mezclas fitosanitarias."""

    @staticmethod
    def calcular_mezcla(
        productos: List[MixtureProduct],
        volumen_total_por_ha: float,
        hectareas: float,
    ) -> Mixture:
        """Crea y retorna un agregado Mixture con los datos proporcionados."""
        return Mixture(
            productos=productos,
            volumen_total_por_ha=volumen_total_por_ha,
            hectareas=hectareas,
        )
