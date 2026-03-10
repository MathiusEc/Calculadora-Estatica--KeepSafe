from dataclasses import dataclass

from src.domain.entities.crop import Crop
from src.domain.entities.flight_operation import FlightOperation
from src.domain.services.flight_calculator import FlightCalculatorService


@dataclass
class FlightCalculationResult:
    """Resultado del caso de uso de cálculo de vuelo."""

    operacion: FlightOperation
    cultivo: Crop
    hectareas: float


class CalculateFlightUseCase:
    """Caso de uso: calcular operación de vuelo del dron."""

    def ejecutar(self, cultivo: Crop, hectareas: float) -> FlightCalculationResult:
        """Ejecuta el cálculo de operación de vuelo."""
        operacion = FlightCalculatorService.calcular_operacion(cultivo, hectareas)
        return FlightCalculationResult(
            operacion=operacion,
            cultivo=cultivo,
            hectareas=hectareas,
        )
