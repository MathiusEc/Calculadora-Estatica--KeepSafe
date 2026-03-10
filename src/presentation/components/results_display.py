from typing import List

import streamlit as st
import pandas as pd

from src.domain.entities.mixture import MixtureResult
from src.domain.entities.product import MixtureProduct


def render_mixture_results(
    resultado_por_ha: MixtureResult,
    resultado_total: MixtureResult,
    productos_ordenados: List[MixtureProduct],
    hectareas: float,
) -> None:
    """Renderiza los resultados de la mezcla calculada."""
    st.markdown("---")
    st.subheader("Resultados de Mezcla")
    st.success("Cálculos completados exitosamente. Revise los resultados a continuación.")

    # --- Tabla y métricas para 1 hectárea ---
    _render_per_hectare(resultado_por_ha, productos_ordenados)

    # --- Tabla y métricas para total de hectáreas ---
    _render_total(resultado_total, productos_ordenados, hectareas)


def _render_per_hectare(
    resultado: MixtureResult, productos: List[MixtureProduct]
) -> None:
    """Renderiza los resultados para 1 hectárea."""
    st.markdown("#### Mezcla para 1 Hectárea")
    st.markdown(
        """
        <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1rem;">
        Esta tabla muestra las cantidades necesarias de cada producto para aplicar en una hectárea.
        </p>
        """,
        unsafe_allow_html=True,
    )

    tabla_1ha = pd.DataFrame(
        [
            {
                "Producto": p.producto,
                "Cantidad (L/ha)": f"{p.cantidad:.3f}",
                "Orden de Mezcla": p.orden,
            }
            for p in productos
        ]
    )
    st.dataframe(tabla_1ha, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Suma de Reactivos",
            f"{resultado.suma_reactivos:.3f} L/ha",
            help="Total de productos fitosanitarios",
        )
    with col2:
        st.metric(
            "Total Mezcla",
            f"{resultado.total_mezcla:.3f} L/ha",
            help="Volumen total de la solución",
        )
    with col3:
        st.metric(
            "Agua Necesaria",
            f"{resultado.agua_necesaria:.3f} L/ha",
            help="Agua requerida para la dilución",
        )


def _render_total(
    resultado: MixtureResult,
    productos: List[MixtureProduct],
    hectareas: float,
) -> None:
    """Renderiza los resultados para el total de hectáreas."""
    st.markdown("---")
    st.markdown(f"#### Mezcla Total para {hectareas:.1f} Hectáreas")
    st.markdown(
        """
        <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1rem;">
        Esta tabla muestra las cantidades totales necesarias para aplicar en todas las hectáreas especificadas.
        </p>
        """,
        unsafe_allow_html=True,
    )

    tabla_total = pd.DataFrame(
        [
            {
                "Producto": p.producto,
                "Cantidad Total (L)": f"{p.cantidad * hectareas:.3f}",
                "Orden de Mezcla": p.orden,
            }
            for p in productos
        ]
    )
    st.dataframe(tabla_total, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Suma de Reactivos",
            f"{resultado.suma_reactivos:.3f} L",
            help="Total de productos fitosanitarios",
        )
    with col2:
        st.metric(
            "Total Mezcla",
            f"{resultado.total_mezcla:.3f} L",
            help="Volumen total de la solución",
        )
    with col3:
        st.metric(
            "Agua Necesaria",
            f"{resultado.agua_necesaria:.3f} L",
            help="Agua requerida para la dilución",
        )
