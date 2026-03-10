from dataclasses import dataclass, field
from typing import List

from src.domain.entities.product import MixtureProduct


@dataclass
class MixtureResult:
    """Value Object con los resultados de cálculo de una mezcla."""

    suma_reactivos: float
    total_mezcla: float
    agua_necesaria: float


@dataclass
class Mixture:
    """Agregado que representa una mezcla de productos fitosanitarios."""

    productos: List[MixtureProduct] = field(default_factory=list)
    volumen_total_por_ha: float = 0.0
    hectareas: float = 1.0

    def productos_ordenados(self) -> List[MixtureProduct]:
        """Retorna los productos ordenados según el orden de mezcla."""
        return sorted(self.productos, key=lambda p: p.orden)

    def calcular_por_hectarea(self) -> MixtureResult:
        """Calcula la mezcla para 1 hectárea."""
        suma_reactivos = sum(p.cantidad for p in self.productos)
        return MixtureResult(
            suma_reactivos=suma_reactivos,
            total_mezcla=self.volumen_total_por_ha,
            agua_necesaria=self.volumen_total_por_ha - suma_reactivos,
        )

    def calcular_total(self) -> MixtureResult:
        """Calcula la mezcla para el total de hectáreas."""
        por_ha = self.calcular_por_hectarea()
        return MixtureResult(
            suma_reactivos=por_ha.suma_reactivos * self.hectareas,
            total_mezcla=por_ha.total_mezcla * self.hectareas,
            agua_necesaria=por_ha.agua_necesaria * self.hectareas,
        )

    def reactivos_superan_volumen(self) -> bool:
        """Verifica si la suma de reactivos supera el volumen total."""
        suma = sum(p.cantidad for p in self.productos)
        return suma > self.volumen_total_por_ha
