from dataclasses import dataclass, field
from typing import List

from src.domain.entities.product import MixtureProduct


@dataclass
class ValidationResult:
    """Resultado de la validación de una mezcla."""

    ordenes_duplicados: bool = False
    productos_duplicados: bool = False
    ordenes_conflictivos: List[int] = field(default_factory=list)
    productos_conflictivos: List[str] = field(default_factory=list)

    @property
    def es_valido(self) -> bool:
        return not self.ordenes_duplicados and not self.productos_duplicados

    @property
    def mensaje_error(self) -> str:
        """Genera mensaje de error descriptivo."""
        errores = []
        if self.ordenes_duplicados:
            errores.append("órdenes de mezcla duplicados")
        if self.productos_duplicados:
            errores.append("productos repetidos")
        return " y ".join(errores)


class MixtureValidator:
    """Validador de mezclas de productos fitosanitarios."""

    @staticmethod
    def validar_productos(productos: List[MixtureProduct]) -> ValidationResult:
        """Valida que no haya órdenes ni productos duplicados."""
        resultado = ValidationResult()

        ordenes_vistos = []
        productos_vistos = []

        for p in productos:
            if p.orden in ordenes_vistos:
                resultado.ordenes_duplicados = True
                if p.orden not in resultado.ordenes_conflictivos:
                    resultado.ordenes_conflictivos.append(p.orden)
            else:
                ordenes_vistos.append(p.orden)

            if p.producto in productos_vistos:
                resultado.productos_duplicados = True
                if p.producto not in resultado.productos_conflictivos:
                    resultado.productos_conflictivos.append(p.producto)
            else:
                productos_vistos.append(p.producto)

        return resultado
