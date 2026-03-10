import streamlit as st

from src.domain.entities.crop import Crop


def render_flight_recommendations(cultivo: Crop) -> None:
    """Renderiza las recomendaciones técnicas y parámetros de vuelo."""
    st.markdown("---")
    st.subheader("Recomendaciones Técnicas para el Operador")

    with st.expander("Parámetros de Vuelo y Aplicación", expanded=False):
        st.markdown(
            """
            <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1.5rem;">
            Configure los parámetros técnicos del dron DJI Agras T50 según las recomendaciones específicas
            para el cultivo seleccionado. Estos valores garantizan una aplicación segura y efectiva.
            </p>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Parámetros de Vuelo**")
            st.text_input(
                "Velocidad",
                value=cultivo.velocidad,
                help="Rango de velocidad recomendado para aplicación",
            )
            st.text_input(
                "Altura de vuelo",
                value=cultivo.altura,
                help="Altura sobre el cultivo",
            )
            st.text_input(
                "Ancho de faja",
                value=cultivo.ancho_faja,
                help="Ancho efectivo de aplicación",
            )
        with col2:
            st.markdown("**Parámetros de Aplicación**")
            st.text_input(
                "Tamaño de gota",
                value=cultivo.gota,
                help="Tamaño de gota según tipo de producto",
            )
            st.number_input(
                "Tasa de aplicación (L/ha)",
                value=float(cultivo.tasa_aplicacion),
                step=0.1,
                help="Volumen de aplicación por hectárea",
            )

        st.info(
            "**Importante:** Verifique las condiciones ambientales antes de iniciar la aplicación. "
            "Viento máximo recomendado: 10 km/h. Temperatura ideal: 18-27°C."
        )
