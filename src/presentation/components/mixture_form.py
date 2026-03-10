from typing import List, Tuple

import streamlit as st

from src.domain.entities.product import MixtureProduct
from src.application.validators import MixtureValidator


def render_mixture_form(
    productos_disponibles: List[str],
) -> Tuple[List[MixtureProduct], float, bool]:
    """
    Renderiza el formulario de mezcla de productos.
    Retorna: (productos_mezcla, volumen_total, tiene_errores_validacion)
    """
    st.markdown("---")
    st.subheader("Configuración de Mezcla de Productos")

    productos_mezcla: List[MixtureProduct] = []
    tiene_errores = False

    with st.expander("Productos a aplicar", expanded=True):
        st.markdown(
            """
            <p style="color: var(--color-gray); margin-bottom: 1.5rem;">
            Seleccione los productos fitosanitarios a aplicar, especifique las cantidades por hectárea
            y defina el orden de mezcla para asegurar una aplicación correcta y segura.
            </p>
            """,
            unsafe_allow_html=True,
        )

        volumen_total_mezcla = st.number_input(
            "Volumen total de mezcla (L/ha)",
            min_value=0.0,
            step=0.1,
            value=0.0,
            help="Ingrese el volumen total de mezcla por hectárea que desea preparar.",
        )

        num_productos = st.number_input(
            "¿Cuántos productos va a usar?",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
        )

        ordenes_usados: List[int] = []
        productos_usados: List[str] = []
        tiene_ordenes_duplicados = False
        tiene_productos_duplicados = False

        if num_productos > 0:
            for i in range(int(num_productos)):
                st.markdown(f"**Producto {i+1}**")
                col1, col2, col3 = st.columns([3, 2, 2])

                with col1:
                    producto = st.selectbox(
                        f"Producto {i+1} - Nombre",
                        productos_disponibles,
                        key=f"prod_{i}",
                        help="Seleccione el producto fitosanitario a aplicar",
                        index=0,
                    )
                with col2:
                    cantidad = st.number_input(
                        f"Cantidad (L/ha)",
                        min_value=0.0,
                        step=0.01,
                        key=f"cant_{i}",
                        format="%.3f",
                        help="Cantidad del producto por hectárea",
                    )
                with col3:
                    orden = st.number_input(
                        f"Orden de mezcla",
                        min_value=1,
                        max_value=int(num_productos),
                        value=min(i + 1, int(num_productos)),
                        step=1,
                        key=f"orden_{i}",
                        help="Orden en el que se agregará a la mezcla",
                    )

                # Validación de órdenes duplicados
                if orden in ordenes_usados:
                    tiene_ordenes_duplicados = True
                    _render_warning(
                        f"El orden {int(orden)} ya está asignado a otro producto. "
                        "Por favor, use un orden diferente."
                    )

                # Validación de productos duplicados
                if producto in productos_usados:
                    tiene_productos_duplicados = True
                    _render_error_inline(
                        f'El producto "{producto}" ya fue seleccionado. '
                        "Por favor, elija un producto diferente."
                    )

                # Guardar producto válido
                if cantidad > 0:
                    productos_mezcla.append(
                        MixtureProduct(producto=producto, cantidad=cantidad, orden=orden)
                    )
                    if orden not in ordenes_usados:
                        ordenes_usados.append(orden)
                    if producto not in productos_usados:
                        productos_usados.append(producto)

                if i < num_productos - 1:
                    st.markdown("")

    # Mostrar error general si hay duplicados
    tiene_errores = tiene_ordenes_duplicados or tiene_productos_duplicados
    if tiene_errores:
        _render_validation_error_summary(
            tiene_ordenes_duplicados, tiene_productos_duplicados
        )

    return productos_mezcla, volumen_total_mezcla, tiene_errores


def _render_warning(message: str) -> None:
    """Renderiza una advertencia inline de orden duplicado."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; background: #FFF4E6;
             border-left: 4px solid #FF9800; padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#FF9800">
                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
            </svg>
            <span style="color: #663C00; font-size: 0.9rem;">{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_error_inline(message: str) -> None:
    """Renderiza un error inline de producto duplicado."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; background: #FFEBEE;
             border-left: 4px solid #F44336; padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#F44336">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            <span style="color: #B71C1C; font-size: 0.9rem;">{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_validation_error_summary(
    tiene_ordenes_duplicados: bool, tiene_productos_duplicados: bool
) -> None:
    """Renderiza el resumen de errores de validación."""
    st.markdown("---")

    errores = []
    if tiene_ordenes_duplicados:
        errores.append("órdenes de mezcla duplicados")
    if tiene_productos_duplicados:
        errores.append("productos repetidos")
    mensaje_error = " y ".join(errores)

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 1rem; background: #FFF4E6;
             border: 2px solid #FF9800; padding: 1.25rem 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" style="flex-shrink: 0;">
                <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z" fill="#FF9800"/>
            </svg>
            <div>
                <h4 style="color: #E65100; margin: 0 0 0.5rem 0; font-size: 1.1rem;">
                    Corrija los errores antes de continuar
                </h4>
                <p style="color: #663C00; margin: 0; font-size: 0.95rem;">
                    Se detectaron {mensaje_error}. Por favor, corrija estos errores para continuar con los cálculos.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
