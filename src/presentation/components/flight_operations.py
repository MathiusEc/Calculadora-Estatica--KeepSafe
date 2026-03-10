from datetime import date

import streamlit as st

from src.domain.entities.flight_operation import FlightOperation
from src.domain.services.flight_calculator import FlightCalculatorService


def render_flight_operations(
    operacion: FlightOperation, hectareas: float, fecha: date
) -> None:
    """Renderiza los cálculos operativos de vuelo."""
    st.markdown("---")
    st.subheader("Cálculos Operativos de Vuelo")

    st.markdown(
        """
        <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1.5rem;">
        Estimaciones de recursos y tiempo necesarios para completar la aplicación
        según los parámetros configurados.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Solución Total",
            f"{operacion.solucion_total:.2f} L",
            help="Volumen total de solución a preparar",
        )
    with col2:
        st.metric(
            "Vuelos Estimados",
            f"{operacion.vuelos_estimados:.0f}",
            help=f"Número de vuelos necesarios (capacidad {FlightCalculatorService.TANQUE_LITROS}L)",
        )
    with col3:
        st.metric(
            "Tiempo Estimado",
            f"{operacion.tiempo_estimado_horas:.2f} h",
            help="Tiempo total de aplicación aproximado",
        )

    with st.expander("Detalles de Cálculo"):
        st.markdown(
            f"""
            - **Capacidad del tanque:** {FlightCalculatorService.TANQUE_LITROS} litros
            - **Tiempo promedio por vuelo:** {FlightCalculatorService.TIEMPO_VUELO_MIN} minutos
            - **Hectáreas a aplicar:** {hectareas:.1f} ha
            - **Tasa de aplicación:** {operacion.solucion_total / hectareas:.1f} L/ha
            - **Fecha planificada:** {fecha.strftime("%d/%m/%Y")}
            """
        )
