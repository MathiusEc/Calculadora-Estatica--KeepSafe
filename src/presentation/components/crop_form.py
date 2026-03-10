from datetime import date
from typing import List, Tuple

import streamlit as st


def render_general_data_form(cultivos: List[str]) -> Tuple[str, float, date]:
    """Renderiza el formulario de datos generales y retorna los valores seleccionados."""
    st.markdown("---")
    st.subheader("Datos Generales de la Aplicación")

    col1, col2, col3 = st.columns(3)
    with col1:
        cultivo = st.selectbox("Cultivo", cultivos)
    with col2:
        hectareas = st.number_input("Hectáreas", min_value=0.1, step=0.1, value=1.0)
    with col3:
        fecha_aplicacion = st.date_input("Fecha de aplicación", key="fecha_aplicacion")

    return cultivo, hectareas, fecha_aplicacion
