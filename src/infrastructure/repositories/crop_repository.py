from typing import Dict, List, Optional

from src.domain.entities.crop import Crop


class CropRepository:
    """Repositorio de datos de cultivos y sus parámetros técnicos."""

    _CULTIVOS: Dict[str, Crop] = {
        "Banano": Crop(
            nombre="Banano",
            tasa_aplicacion=18,
            velocidad="20-30 km/h",
            altura="7-8 m",
            ancho_faja="7-9.5 m",
            gota="Fina/Media",
        ),
        "Maíz": Crop(
            nombre="Maíz",
            tasa_aplicacion=19,
            velocidad="20-25 km/h",
            altura="5-6 m",
            ancho_faja="7-8.5 m",
            gota="Fina/Media/Gruesa",
        ),
        "Arroz": Crop(
            nombre="Arroz",
            tasa_aplicacion=16.5,
            velocidad="25-30 km/h",
            altura="4-7 m",
            ancho_faja="6.5-8 m",
            gota="Muy Fina/Fina/Media",
        ),
        "Cacao": Crop(
            nombre="Cacao",
            tasa_aplicacion=25,
            velocidad="20-25 km/h",
            altura="7 m",
            ancho_faja="7-8.5 m",
            gota="Muy Fina/Fina/Media",
        ),
    }

    @classmethod
    def obtener_todos(cls) -> Dict[str, Crop]:
        """Retorna todos los cultivos disponibles."""
        return cls._CULTIVOS.copy()

    @classmethod
    def obtener_nombres(cls) -> List[str]:
        """Retorna la lista de nombres de cultivos."""
        return list(cls._CULTIVOS.keys())

    @classmethod
    def obtener_por_nombre(cls, nombre: str) -> Optional[Crop]:
        """Retorna un cultivo por su nombre."""
        return cls._CULTIVOS.get(nombre)
