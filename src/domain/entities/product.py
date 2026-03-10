from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Entidad que representa un producto fitosanitario disponible."""

    nombre: str


@dataclass
class MixtureProduct:
    """Producto dentro de una mezcla, con cantidad y orden de aplicación."""

    producto: str
    cantidad: float  # L/ha
    orden: int
