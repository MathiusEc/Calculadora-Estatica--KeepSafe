from dataclasses import dataclass
from typing import List, Optional

from src.domain.entities.mixture import Mixture, MixtureResult
from src.domain.entities.product import MixtureProduct
from src.domain.services.mixture_calculator import MixtureCalculatorService
from src.application.validators.mixture_validator import MixtureValidator


@dataclass
class MixtureCalculationResult:
    """Resultado del caso de uso de cálculo de mezcla."""

    resultado_por_ha: Optional[MixtureResult] = None
    resultado_total: Optional[MixtureResult] = None
    productos_ordenados: Optional[List[MixtureProduct]] = None
    error: Optional[str] = None

    @property
    def es_valido(self) -> bool:
        return self.error is None


class CalculateMixtureUseCase:
    """Caso de uso: calcular mezcla de productos fitosanitarios."""

    def __init__(self):
        self._calculator = MixtureCalculatorService()
        self._validator = MixtureValidator()

    def ejecutar(
        self,
        productos: List[MixtureProduct],
        volumen_total_por_ha: float,
        hectareas: float,
    ) -> MixtureCalculationResult:
        """Ejecuta el cálculo de mezcla con validaciones."""
        # Validar volumen
        if volumen_total_por_ha <= 0:
            return MixtureCalculationResult(
                error="Ingrese un volumen total de mezcla (L/ha) mayor a cero para realizar los cálculos."
            )

        # Validar que todos los productos tengan cantidad
        if any(p.cantidad <= 0 for p in productos):
            return MixtureCalculationResult(
                error="Ingrese la cantidad de todos los productos para ver los resultados de la mezcla."
            )

        # Crear mezcla
        mezcla = self._calculator.calcular_mezcla(
            productos, volumen_total_por_ha, hectareas
        )

        # Validar que los reactivos no superen el volumen
        if mezcla.reactivos_superan_volumen():
            return MixtureCalculationResult(
                error="La suma de los reactivos supera el volumen total de mezcla por hectárea. Ajuste las cantidades."
            )

        return MixtureCalculationResult(
            resultado_por_ha=mezcla.calcular_por_hectarea(),
            resultado_total=mezcla.calcular_total(),
            productos_ordenados=mezcla.productos_ordenados(),
        )
