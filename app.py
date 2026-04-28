
# =============================
# PUNTO DE ENTRADA - ARQUITECTURA DDD
# =============================
# Este archivo es el orquestador principal que conecta todas las capas DDD.
# No contiene lógica de negocio, datos ni cálculos directamente.
# =============================

import streamlit as st

# Capa de Presentación
from src.presentation.utils import load_local_css
from src.presentation.components.header import render_header, render_description
from src.presentation.components.crop_form import render_general_data_form
from src.presentation.components.mixture_form import render_mixture_form
from src.presentation.components.results_display import render_mixture_results
from src.presentation.components.flight_recommendations import render_flight_recommendations
from src.presentation.components.flight_operations import render_flight_operations

# Capa de Aplicación (Casos de Uso)
from src.application.use_cases.calculate_mixture import CalculateMixtureUseCase
from src.application.use_cases.calculate_flight import CalculateFlightUseCase

# Capa de Infraestructura (Repositorios)
from src.infrastructure.repositories.crop_repository import CropRepository
from src.infrastructure.repositories.product_repository import ProductRepository


# =============================
# CONFIGURACIÓN DE LA PÁGINA
# =============================
st.set_page_config(
    page_title="Keep Safe Operation - Calculadora de Mezclas",
    page_icon="img/icons/favicon-16x16.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://wa.me/593983899314',
        'Report a bug': "mailto:keepsafe.ecuador@gmail.com",
        'About': """**Keep Safe S.A.S.**  
        Agricultura de Precisión con Drones DJI Agras T50  
        Guayaquil, Ecuador"""
    }
)

# Cargar estilos visuales personalizados
load_local_css("styles2.css")


# =============================
# FUNCIÓN PRINCIPAL
# =============================
def main():
    """Orquestador principal de la aplicación siguiendo arquitectura DDD."""

    # --- Presentación: Header y descripción ---
    render_header()
    render_description()

    # --- Infraestructura: Obtener datos de repositorios ---
    cultivos_nombres = CropRepository.obtener_nombres()
    productos_disponibles = ProductRepository.obtener_todos()

    # --- Presentación: Formulario de datos generales ---
    cultivo_nombre, hectareas, fecha_aplicacion = render_general_data_form(cultivos_nombres)

    # --- Presentación: Formulario de mezcla ---
    productos_mezcla, volumen_total, tiene_errores = render_mixture_form(productos_disponibles)

    # --- Lógica de aplicación: Cálculos solo si no hay errores ---
    if not tiene_errores and productos_mezcla and hectareas > 0:

        # Caso de uso: Calcular mezcla
        mixture_use_case = CalculateMixtureUseCase()
        resultado_mezcla = mixture_use_case.ejecutar(
            productos=productos_mezcla,
            volumen_total_por_ha=volumen_total,
            hectareas=hectareas,
        )

        if resultado_mezcla.es_valido:
            # Presentación: Mostrar resultados de mezcla
            render_mixture_results(
                resultado_por_ha=resultado_mezcla.resultado_por_ha,
                resultado_total=resultado_mezcla.resultado_total,
                productos_ordenados=resultado_mezcla.productos_ordenados,
                hectareas=hectareas,
            )

            # --- Infraestructura: Obtener datos del cultivo ---
            cultivo = CropRepository.obtener_por_nombre(cultivo_nombre)

            if cultivo:
                # Presentación: Recomendaciones técnicas
                render_flight_recommendations(cultivo)

                # Caso de uso: Calcular operación de vuelo
                flight_use_case = CalculateFlightUseCase()
                resultado_vuelo = flight_use_case.ejecutar(cultivo, hectareas)

                # Presentación: Cálculos operativos de vuelo
                render_flight_operations(
                    operacion=resultado_vuelo.operacion,
                    hectareas=hectareas,
                    fecha=fecha_aplicacion,
                )
        else:
            # Mostrar error de validación del caso de uso
            if "volumen" in resultado_mezcla.error.lower() and "mayor a cero" in resultado_mezcla.error.lower():
                st.warning(resultado_mezcla.error)
            elif "cantidad" in resultado_mezcla.error.lower():
                st.info(resultado_mezcla.error)
            else:
                st.error(resultado_mezcla.error)


if __name__ == "__main__":
    main()
else:
    main()

# ============================================
# PIE DE PÁGINA - FOOTER INTEGRADO
# Usa st.markdown() para renderizado nativo (sin iframe)
# Fondo claro que se integra con el resto de la app
# ============================================
st.markdown("---")
st.markdown("""
<style>
    .ks-footer {
        font-family: 'Poppins', sans-serif;
        background: #F5F7FA;
        border-top: 3px solid #1E5F9E;
        padding: 3rem 4rem 0;
        margin: 3rem 0 0 0;
        border-radius: 8px 8px 0 0;
        width: 100%;
        box-sizing: border-box;
    }
    .ks-footer-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr 1fr 1.5fr;
        gap: 3rem;
        max-width: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
    }
    .ks-footer h4 {
        color: #1E5F9E;
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        margin-top: 0;
        position: relative;
        padding-bottom: 0.75rem;
    }
    .ks-footer h4::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        width: 30px; height: 2px;
        background: linear-gradient(135deg, #D96B2A, #C75A1F);
        border-radius: 1px;
    }
    .ks-footer p {
        color: #6B7280;
        font-size: 0.9rem;
        line-height: 1.8;
        margin: 0.5rem 0;
    }
    .ks-footer ul {
        list-style: none;
        padding: 0; margin: 0;
    }
    .ks-footer ul li {
        margin-bottom: 0.9rem;
    }
    .ks-footer ul li a {
        color: #4B5563;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        display: inline-block;
    }
    .ks-footer ul li a:hover {
        color: #D96B2A;
        padding-left: 6px;
    }
    .ks-footer-social {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    .ks-footer-social a {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: rgba(30, 95, 158, 0.1);
        transition: all 0.3s ease;
    }
    .ks-footer-social a:hover {
        background: #1E5F9E;
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(30, 95, 158, 0.3);
    }
    .ks-footer-social a img {
        width: 20px;
        height: 20px;
    }
    .ks-footer-location {
        margin-top: 1.5rem;
        padding-top: 1.25rem;
        border-top: 1px solid #E5E7EB;
    }
    .ks-footer-location strong {
        color: #1E5F9E;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .ks-footer-location p {
        margin-top: 0.5rem;
    }
    .ks-footer-contact strong {
        color: #1E5F9E;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .ks-footer-contact a {
        color: #4B5563;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    .ks-footer-contact a:hover {
        color: #D96B2A;
    }
    .ks-footer-contact p {
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }
    .ks-footer-contact p:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    .ks-footer-bottom {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        margin-top: 2.5rem;
        border-top: 1px solid #E5E7EB;
    }
    .ks-footer-bottom p {
        color: #9CA3AF;
        font-size: 0.85rem;
        margin: 0;
    }
    @media (max-width: 1024px) {
        /* AJUSTA ESTOS VALORES PARA MOVER MANUALMENTE EL CONTENIDO */
        --offset-horizontal: 125px; /* Cambia este valor para mover a izq/der: ej. -10px, 15px */
        
        .ks-footer-grid {
            grid-template-columns: 1fr !important;
            gap: 2rem !important;
        }
        .ks-footer { 
            padding: 2rem 1.5rem 0 !important; 
        }
        .ks-footer-grid > div {
            position: relative !important;
            left: var(--offset-horizontal, 0px) !important;
            margin: 0 auto !important;
            width: fit-content !important;
        }
        .ks-footer h4 {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            margin-left: auto !important;
            margin-right: auto !important;
            width: fit-content !important;
            position: relative !important;
        }
        .ks-footer h4::after {
            left: 50% !important;
            transform: translateX(-50%) !important;
            right: auto !important;
        }
        .ks-footer p {
            margin-left: auto !important;
            margin-right: auto !important;
            width: fit-content !important;
        }
        .ks-footer ul {
            padding-left: 0 !important;
            margin: 0 auto !important;
            list-style: none !important;
            width: fit-content !important;
        }
        .ks-footer ul li {
            margin: 0.6rem auto !important;
            width: fit-content !important;
        }
        .ks-footer ul li a:hover {
            transform: none !important;
            padding-left: 0 !important;
        }
        .ks-footer-social {
            justify-content: center !important;
            margin: 1rem auto !important;
        }
        .ks-footer-location,
        .ks-footer-contact {
            margin: 0 auto !important;
            width: fit-content !important;
        }
        .ks-footer-contact p {
            margin-left: auto !important;
            margin-right: auto !important;
            width: fit-content !important;
        }
    }
</style>

<div class="ks-footer">
    <div class="ks-footer-grid">
        <div>
            <h4>Keep Safe S.A.S.</h4>
            <p>Es una empresa ecuatoriana que integra tecnología, drones y conocimiento técnico para brindar soluciones de agricultura de precisión, bioseguridad y gestión del riesgo, con altos estándares operativos.</p>
            <div class="ks-footer-social">
                <a href="URL YouTube" target="_blank" title="YouTube">
                    <img src="data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='%231E5F9E' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z'/%3E%3C/svg%3E" alt="YouTube">
                </a>
                <a href="https://www.instagram.com/keepsafe_ec?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" target="_blank" title="Instagram">
                    <img src="data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='%231E5F9E' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z'/%3E%3C/svg%3E" alt="Instagram">
                </a>
                <a href="https://www.linkedin.com/company/keepsafeagriculture" target="_blank" title="LinkedIn">
                    <img src="data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='%231E5F9E' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z'/%3E%3C/svg%3E" alt="LinkedIn">
                </a>
            </div>
            <div class="ks-footer-location">
                <p><strong>Ubicación</strong></p>
                <p>Guayaquil, Ecuador</p>
            </div>
        </div>
        <div>
            <h4>Enlaces</h4>
            <ul>
                <li><a href="https://www.keepsafeagriculture.com/" class="active">Inicio</a></li>
                <li><a href="https://www.keepsafeagriculture.com/nosotros/">Nosotros</a></li>
                <li><a href="https://www.keepsafeagriculture.com/servicios/">Servicios</a></li>
                <li><a href="https://calculadora-keepsafe.streamlit.app/" target="_blank" rel="noopener">Calculadora</a></li>
                <li><a href="https://www.weathernerds.org/satellite/?initsatsrc=On&initsatname=GOES-E&initsattype=ir&initcscheme=ir1&initimdimx=1050&initimdimy=777&initrange=-1.000:-81.750:-3.000:-78.500&initloop=True&initnframes=20&initlightningge=On&initlightninggw=Off&initltngfed=Off&initltngtoe=Off&initinterstates=On&initwarnings=On&initlatlon=Off&initascatb=Off&initascatc=Off&initascatambb=Off&initascatambc=Off&initsst=Off&initecens=Off&initgefs=Off" target="_blank" rel="noopener">Pron&#243;stico</a></li>
                <li><a href="https://www.keepsafeagriculture.com/contactanos/">Contacto</a></li>
            </ul>
        </div>
        <div>
            <h4>Servicios</h4>
            <ul>
                <li><a href="https://www.keepsafeagriculture.com/servicios/">Fumigación con drones</a></li>
                <li><a href="https://www.keepsafeagriculture.com/servicios/">Fertilización de precisión</a></li>
                <li><a href="https://www.keepsafeagriculture.com/servicios/">Mapeo aéreo</a></li>
                <li><a href="https://www.keepsafeagriculture.com/servicios/">Análisis de cultivos</a></li>
                <li><a href="https://www.keepsafeagriculture.com/servicios/">Inteligencia de Aplicaciones</a></li>
            </ul>
        </div>
        <div class="ks-footer-contact">
            <h4>Contactos</h4>
            <p><strong>E-Mail:</strong></p>
            <p><a href="mailto:keepsafe.ecuador@gmail.com">keepsafe.ecuador@gmail.com</a></p>
            <p style="margin-top:12px"><strong>Teléfonos:</strong></p>
            <p><a href="https://wa.me/593979459949?text=%C2%A1Hola!%20Me%20interesa%20conocer%20m%C3%A1s%20sobre%20sus%20soluciones%20agr%C3%ADcolas%20y%20c%C3%B3mo%20podr%C3%ADan%20implementarse%20en%20mi%20cultivo." target="_blank" rel="noopener noreferrer">+593 97 945 9949</a></p>
        </div>
    </div>
    <div class="ks-footer-bottom">
        <p>&copy; 2025 Todos los derechos reservados.</p>
    </div>
</div>
""", unsafe_allow_html=True)