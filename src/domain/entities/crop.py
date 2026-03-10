from dataclasses import dataclass


@dataclass(frozen=True)
class Crop:
    """Entidad que representa un cultivo con sus parámetros técnicos de aplicación."""

    nombre: str
    tasa_aplicacion: float  # L/ha
    velocidad: str
    altura: str
    ancho_faja: str
    gota: str
