import streamlit as st


def load_local_css(file_name: str) -> None:
    """Carga un archivo CSS local e inyecta los estilos en la app de Streamlit."""
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"No se encontró el archivo CSS: {file_name}")
