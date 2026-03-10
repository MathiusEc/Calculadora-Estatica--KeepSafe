from src.domain.entities.crop import Crop
from src.domain.entities.flight_operation import FlightOperation


class FlightCalculatorService:
    """Servicio de dominio para cálculos operativos de vuelo del dron."""

    TANQUE_LITROS: int = 40  # Capacidad del tanque del dron
    TIEMPO_VUELO_MIN: int = 10  # Tiempo promedio por vuelo en minutos

    @classmethod
    def calcular_operacion(cls, cultivo: Crop, hectareas: float) -> FlightOperation:
        """Calcula los parámetros operativos de vuelo."""
        solucion_total = cultivo.tasa_aplicacion * hectareas
        vuelos = solucion_total / cls.TANQUE_LITROS
        tiempo_horas = vuelos * cls.TIEMPO_VUELO_MIN / 60

        return FlightOperation(
            solucion_total=solucion_total,
            vuelos_estimados=vuelos,
            tiempo_estimado_horas=tiempo_horas,
        )
