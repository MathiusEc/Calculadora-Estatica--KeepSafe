from dataclasses import dataclass


@dataclass(frozen=True)
class FlightOperation:
    """Value Object con los cálculos operativos de vuelo."""

    solucion_total: float  # Litros totales de solución
    vuelos_estimados: float  # Número de vuelos necesarios
    tiempo_estimado_horas: float  # Tiempo total en horas
