import io
import base64

import streamlit as st
from PIL import Image


def render_header() -> None:
    """Renderiza el header con logo y título de la aplicación."""
    st.markdown(
        """
        <div class="header-container" style="margin-top:0; padding-top:0;">
            <div class="logo-container fade-in" style="margin-bottom:0;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    logo_base64 = _load_logo("img/KEEP SAFE LOGO-01.png")

    col_logo, col_title = st.columns([1, 5])

    with col_logo:
        if logo_base64:
            st.markdown(
                f'''
                <a href="https://mathiusec.github.io/KeepSafe-WebPage/" target="_blank" style="display:inline-block;">
                    <img src="{logo_base64}" width="200" alt="Keep Safe Logo" style="margin-bottom:0;"/>
                </a>
                ''',
                unsafe_allow_html=True,
            )
        else:
            st.error("Logo no encontrado. Verifica la ruta del archivo.")

    with col_title:
        st.markdown(
            """
            <div style="padding-top: 0.5rem;">
                <h1 style="margin-bottom: 0.5rem; margin-top: 0;">Keep Safe Operation</h1>
                <h3 style="color: var(--color-gray); font-weight: 400; margin-top: 0; margin-bottom: 0.5rem;">
                    Calculadora de Mezclas y Operaciones para Drones Agrícolas DJI Agras T50
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_description() -> None:
    """Renderiza la descripción introductoria."""
    st.markdown(
        """
        <div class="descripcion-intro" style="margin-top: 0.5rem; margin-bottom: 0.5rem;">
            <p style="margin: 0; font-size: 1.05rem; line-height: 1.6;">
                Bienvenido a la <strong>Calculadora de Mezclas y Operaciones para Drones Agrícolas DJI Agras T50</strong>.
                Esta herramienta está diseñada para complementar la Hoja de Recomendaciones Operativas, permitiendo
                calcular mezclas de productos fitosanitarios, gestionar ciclos de aplicación y determinar parámetros
                técnicos de manera precisa y alineada con las mejores prácticas de operación segura.
                Optimice sus aplicaciones agrícolas con agricultura de precisión.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _load_logo(path: str) -> str:
    """Carga el logo y lo convierte a base64 para embeber en HTML."""
    try:
        logo = Image.open(path)
        buffered = io.BytesIO()
        logo.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except FileNotFoundError:
        return ""
