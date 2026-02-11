import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import os
import io
import base64


# Configuración de página con favicon actualizado
st.set_page_config(
    page_title="Keep Safe Operation - Calculadora de Mezclas",
    page_icon="img/icons/favicon-16x16.png",  # Favicon 
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

# Función para cargar CSS local optimizado para Streamlit
def load_local_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"No se encontró el archivo CSS: {file_name}")

# Cargar CSS de la web original (un solo archivo para web y app)
load_local_css("styles2.css")

# ============================================
# SECCIÓN 1: HEADER - LOGO Y TÍTULO
# ============================================
# Header container con diseño mejorado
st.markdown("""
<div class="header-container" style="margin-top:0; padding-top:0;">
    <div class="logo-container fade-in" style="margin-bottom:0;">
        <!-- El logo se muestra con st.image más abajo -->
    </div>
</div>
""", unsafe_allow_html=True)

# Logo de la empresa
logo_path = "img/KEEP SAFE LOGO-01.png"
try:
    logo = Image.open(logo_path)
    buffered = io.BytesIO()
    logo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    logo_base64 = f"data:image/png;base64,{img_str}"
except FileNotFoundError:
    logo_base64 = ""  # Si no encuentra la imagen, no muestra nada

col_logo, col_title = st.columns([1, 5])

with col_logo:
    if logo_base64:
        st.markdown(
            f'''
            <a href="https://mathiusec.github.io/KeepSafe-WebPage/" target="_blank" style="display:inline-block;">
                <img src="{logo_base64}" width="200" alt="Keep Safe Logo" style="margin-bottom:0;"/>
            </a>
            ''',
            unsafe_allow_html=True
        )
    else:
        st.error("Logo no encontrado. Verifica la ruta del archivo.")

with col_title:
    st.markdown("""
    <div style="padding-top: 0.5rem;">
        <h1 style="margin-bottom: 0.5rem; margin-top: 0;">Keep Safe Operation</h1>
        <h3 style="color: var(--color-gray); font-weight: 400; margin-top: 0; margin-bottom: 0.5rem;">Calculadora de Mezclas y Operaciones para Drones Agrícolas DJI Agras T50</h3>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SECCIÓN 2: DESCRIPCIÓN BREVE
# ============================================
st.markdown("""
<div class="descripcion-intro" style="margin-top: 0.5rem; margin-bottom: 0.5rem;">
    <p style="margin: 0; font-size: 1.05rem; line-height: 1.6;">
        Bienvenido a la <strong>Calculadora de Mezclas y Operaciones para Drones Agrícolas DJI Agras T50</strong>. 
        Esta herramienta está diseñada para complementar la Hoja de Recomendaciones Operativas, permitiendo 
        calcular mezclas de productos fitosanitarios, gestionar ciclos de aplicación y determinar parámetros 
        técnicos de manera precisa y alineada con las mejores prácticas de operación segura. 
        Optimice sus aplicaciones agrícolas con agricultura de precisión.
    </p>
</div>
""", unsafe_allow_html=True)

# ======================
# DATOS DE CULTIVOS
# Modifica aquí los cultivos disponibles y sus parámetros técnicos
# ======================
cultivos_data = {
    "Banano": {"tasa_aplicacion": 18, "velocidad": "20-30 km/h", "altura": "7-8 m", "ancho_faja": "7-9.5 m", "gota": "Fina/Media"},
    "Maíz": {"tasa_aplicacion": 19, "velocidad": "20-25 km/h", "altura": "5-6 m", "ancho_faja": "7-8.5 m", "gota": "Fina/Media/Gruesa"},
    "Arroz": {"tasa_aplicacion": 16.5, "velocidad": "25-30 km/h", "altura": "4-7 m", "ancho_faja": "6.5-8 m", "gota": "Muy Fina/Fina/Media"},
    "Cacao": {"tasa_aplicacion": 25, "velocidad": "20-25 km/h", "altura": "7 m", "ancho_faja": "7-8.5 m", "gota": "Muy Fina/Fina/Media"},
}

# ======================
# LISTA DE PRODUCTOS DISPONIBLES
# Modifica aquí los productos fitosanitarios que aparecen en el select
# ======================
productos_disponibles = [
    "Seleccionar...",
    "Glifosato 480 SL",
    "Mancozeb",
    "Clorpirifos",
    "Cipermetrina",
    "Folliup",
    "Kill Bac",
    "Aceite Agrícola",
    "Adherente",
    "Urea Foliar",
    "Fosfito de Potasio",
    "Otro"
]

# ======================
# PARÁMETROS DE DRON Y CÁLCULOS OPERATIVOS
# Si el cliente pide cambiar capacidad de tanque, tiempo de vuelo, etc., modificar aquí
# ======================
TANQUE_LITROS = 40  # Capacidad del tanque del dron en litros
TIEMPO_VUELO_MIN = 10  # Tiempo promedio por vuelo en minutos

# ============================================
# SECCIÓN 3: DATOS GENERALES
# ============================================
st.markdown("---")
st.subheader("Datos Generales de la Aplicación")

col1, col2, col3 = st.columns(3)
with col1:
    cultivo = st.selectbox("Cultivo", list(cultivos_data.keys()))
with col2:
    hectareas = st.number_input("Hectáreas", min_value=0.1, step=0.1, value=1.0)
with col3:
    fecha_aplicacion = st.date_input("Fecha de aplicación", key="fecha_aplicacion")

# ============================================
# SECCIÓN 4: CONFIGURACIÓN DE MEZCLA
# ============================================
st.markdown("---")
st.subheader("Configuración de Mezcla de Productos")

with st.expander("Productos a aplicar", expanded=True):
    st.markdown("""
    <p style="color: var(--color-gray); margin-bottom: 1.5rem;">
    Seleccione los productos fitosanitarios a aplicar, especifique las cantidades por hectárea 
    y defina el orden de mezcla para asegurar una aplicación correcta y segura.
    </p>
    """, unsafe_allow_html=True)
    
    num_productos = st.number_input("¿Cuántos productos va a usar?", min_value=1, max_value=10, value=1, step=1)
    
    # Tabla dinámica de productos
    productos_mezcla = []
    ordenes_usados = []
    tiene_ordenes_duplicados = False
    
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
                    index=0
                )
            with col2:
                cantidad = st.number_input(
                    f"Cantidad (L/ha)", 
                    min_value=0.0, 
                    step=0.01, 
                    key=f"cant_{i}", 
                    format="%.3f",
                    help="Cantidad del producto por hectárea"
                )
            with col3:
                orden = st.number_input(
                    f"Orden de mezcla", 
                    min_value=1, 
                    max_value=int(num_productos), 
                    value=min(i+1, int(num_productos)), 
                    step=1, 
                    key=f"orden_{i}",
                    help="Orden en el que se agregará a la mezcla"
                )
            
            # Validación de orden duplicado
            if orden in ordenes_usados and producto != "Seleccionar...":
                tiene_ordenes_duplicados = True
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 0.5rem; background: #FFF4E6; border-left: 4px solid #FF9800; padding: 0.75rem 1rem; border-radius: 4px; margin: 0.5rem 0;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="#FF9800">
                        <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                    </svg>
                    <span style="color: #663C00; font-size: 0.9rem;">El orden {int(orden)} ya está asignado a otro producto. Por favor, use un orden diferente.</span>
                </div>
                """, unsafe_allow_html=True)
            
            if producto != "Seleccionar..." and cantidad > 0:
                productos_mezcla.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "orden": orden
                })
                if orden not in ordenes_usados:
                    ordenes_usados.append(orden)
            
            if i < num_productos - 1:
                st.markdown("")

# Mostrar mensaje si hay errores de validación
if tiene_ordenes_duplicados:
    st.markdown("---")
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 1rem; background: #FFF4E6; border: 2px solid #FF9800; padding: 1.25rem 1.5rem; border-radius: 8px; margin: 1rem 0;">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" style="flex-shrink: 0;">
            <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z" fill="#FF9800"/>
        </svg>
        <div>
            <h4 style="color: #E65100; margin: 0 0 0.5rem 0; font-size: 1.1rem;">Corrija los errores antes de continuar</h4>
            <p style="color: #663C00; margin: 0; font-size: 0.95rem;">Por favor, asigne órdenes de mezcla únicos a cada producto. Los cálculos se mostrarán una vez que corrija los órdenes duplicados.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Cálculos automáticos - solo si no hay errores de validación
elif productos_mezcla and hectareas > 0:
    # Ordenar por orden de mezcla
    productos_mezcla_ordenados = sorted(productos_mezcla, key=lambda x: x["orden"])
    
    # Cálculos para 1 hectárea
    suma_reactivos_1ha = sum([p["cantidad"] for p in productos_mezcla])
    datos_cultivo = cultivos_data[cultivo]
    total_mezcla_1ha = datos_cultivo["tasa_aplicacion"]
    agua_necesaria_1ha = total_mezcla_1ha - suma_reactivos_1ha
    
    # Cálculos para el total de hectáreas
    suma_reactivos_total = suma_reactivos_1ha * hectareas
    total_mezcla_total = total_mezcla_1ha * hectareas
    agua_necesaria_total = agua_necesaria_1ha * hectareas
    
    # ============================================
    # SECCIÓN 5: RESULTADOS DE MEZCLA
    # ============================================
    st.markdown("---")
    st.subheader("Resultados de Mezcla")
    
    st.success("Cálculos completados exitosamente. Revise los resultados a continuación.")
    
    # Tabla para 1 ha
    st.markdown("#### Mezcla para 1 Hectárea")
    st.markdown("""
    <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1rem;">
    Esta tabla muestra las cantidades necesarias de cada producto para aplicar en una hectárea.
    </p>
    """, unsafe_allow_html=True)
    
    tabla_1ha = pd.DataFrame([
        {"Producto": p['producto'], "Cantidad (L/ha)": f"{p['cantidad']:.3f}", "Orden de Mezcla": p['orden']}
        for p in productos_mezcla_ordenados
    ])
    st.dataframe(tabla_1ha, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Suma de Reactivos", f"{suma_reactivos_1ha:.3f} L/ha", help="Total de productos fitosanitarios")
    with col2:
        st.metric("Total Mezcla", f"{total_mezcla_1ha:.3f} L/ha", help="Volumen total de la solución")
    with col3:
        st.metric("Agua Necesaria", f"{agua_necesaria_1ha:.3f} L/ha", help="Agua requerida para la dilución")
    
    # Tabla para total de hectáreas
    st.markdown("---")
    st.markdown(f"#### Mezcla Total para {hectareas:.1f} Hectáreas")
    st.markdown("""
    <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1rem;">
    Esta tabla muestra las cantidades totales necesarias para aplicar en todas las hectáreas especificadas.
    </p>
    """, unsafe_allow_html=True)
    
    tabla_total = pd.DataFrame([
        {"Producto": p['producto'], "Cantidad Total (L)": f"{p['cantidad'] * hectareas:.3f}", "Orden de Mezcla": p['orden']}
        for p in productos_mezcla_ordenados
    ])
    st.dataframe(tabla_total, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Suma de Reactivos", f"{suma_reactivos_total:.3f} L", help="Total de productos fitosanitarios")
    with col2:
        st.metric("Total Mezcla", f"{total_mezcla_total:.3f} L", help="Volumen total de la solución")
    with col3:
        st.metric("Agua Necesaria", f"{agua_necesaria_total:.3f} L", help="Agua requerida para la dilución")

    # ============================================
    # SECCIÓN 6: RECOMENDACIONES TÉCNICAS
    # ============================================
    datos = cultivos_data[cultivo]
    tasa = datos["tasa_aplicacion"]
    total_sol = tasa * hectareas
    vuelos = total_sol / 40
    tiempo = vuelos * 10 / 60

    st.markdown("---")
    st.subheader("Recomendaciones Técnicas para el Operador")
    
    with st.expander("Parámetros de Vuelo y Aplicación", expanded=False):
        st.markdown("""
        <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1.5rem;">
        Configure los parámetros técnicos del dron DJI Agras T50 según las recomendaciones específicas 
        para el cultivo seleccionado. Estos valores garantizan una aplicación segura y efectiva.
        </p>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Parámetros de Vuelo**")
            velocidad = st.text_input(f"Velocidad", value=datos['velocidad'], 
                                     help="Rango de velocidad recomendado para aplicación")
            altura = st.text_input(f"Altura de vuelo", value=datos['altura'], 
                                  help="Altura sobre el cultivo")
            faja = st.text_input(f"Ancho de faja", value=datos['ancho_faja'], 
                                help="Ancho efectivo de aplicación")
        with col2:
            st.markdown("**Parámetros de Aplicación**")
            gota = st.text_input(f"Tamaño de gota", value=datos['gota'], 
                                help="Tamaño de gota según tipo de producto")
            tasa_aplicacion_input = st.number_input(f"Tasa de aplicación (L/ha)", 
                                                    value=float(tasa), step=0.1,
                                                    help="Volumen de aplicación por hectárea")
        
        st.info("**Importante:** Verifique las condiciones ambientales antes de iniciar la aplicación. "
                "Viento máximo recomendado: 10 km/h. Temperatura ideal: 18-27°C.")

    # ============================================
    # SECCIÓN 7: CÁLCULOS OPERATIVOS
    # ============================================
    st.markdown("---")
    st.subheader("Cálculos Operativos de Vuelo")
    
    st.markdown("""
    <p style="color: var(--color-gray); font-size: 0.95rem; margin-bottom: 1.5rem;">
    Estimaciones de recursos y tiempo necesarios para completar la aplicación según los parámetros configurados.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Solución Total", f"{total_sol:.2f} L", 
                 help="Volumen total de solución a preparar")
    with col2:
        st.metric("Vuelos Estimados", f"{vuelos:.0f}", 
                 help="Número de vuelos necesarios (capacidad 40L)")
    with col3:
        st.metric("Tiempo Estimado", f"{tiempo:.2f} h", 
                 help="Tiempo total de aplicación aproximado")
    
    # Información adicional
    with st.expander("Detalles de Cálculo"):
        st.markdown(f"""
        - **Capacidad del tanque:** 40 litros
        - **Tiempo promedio por vuelo:** 10 minutos
        - **Hectáreas a aplicar:** {hectareas:.1f} ha
        - **Tasa de aplicación:** {tasa:.1f} L/ha
        - **Fecha planificada:** {fecha_aplicacion.strftime("%d/%m/%Y")}
        """)

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
    @media (max-width: 768px) {
        .ks-footer-grid {
            grid-template-columns: 1fr;
            gap: 2.5rem;
        }
        .ks-footer { 
            padding: 2rem 1.5rem 0; 
        }
    }
</style>

<div class="ks-footer">
    <div class="ks-footer-grid">
        <div>
            <h4>Keep Safe S.A.S.</h4>
            <p>Es una empresa ecuatoriana que integra tecnología, drones y conocimiento técnico para brindar soluciones de agricultura de precisión, bioseguridad y gestión del riesgo.</p>
            <div class="ks-footer-social">
                <a href="https://www.youtube.com/@keepsafe_ec" target="_blank" title="YouTube">
                    <img src="data:image/svg+xml,%3Csvg viewBox='0 0 24 24' fill='%231E5F9E' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z'/%3E%3C/svg%3E" alt="YouTube">
                </a>
                <a href="https://www.instagram.com/keepsafe_ec" target="_blank" title="Instagram">
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
                <li><a href="https://keepsafeagriculture.com" target="_blank">Inicio</a></li>
                <li><a href="https://keepsafeagriculture.com/servicios" target="_blank">Servicios</a></li>
                <li><a href="https://keepsafeagriculture.com/nosotros" target="_blank">Nosotros</a></li>
                <li><a href="https://keepsafeagriculture.com/contactanos" target="_blank">Contacto</a></li>
            </ul>
        </div>
        <div>
            <h4>Servicios</h4>
            <ul>
                <li><a href="https://keepsafeagriculture.com/servicios#fumigacion" target="_blank">Fumigación con drones</a></li>
                <li><a href="https://keepsafeagriculture.com/servicios#fertilizacion" target="_blank">Fertilización de precisión</a></li>
                <li><a href="https://keepsafeagriculture.com/servicios#mapeo" target="_blank">Mapeo aéreo</a></li>
                <li><a href="https://keepsafeagriculture.com/servicios#analisis" target="_blank">Análisis de cultivos</a></li>
            </ul>
        </div>
        <div class="ks-footer-contact">
            <h4>Contactos</h4>
            <p><strong>E-Mail:</strong></p>
            <p><a href="mailto:keepsafe.ecuador@gmail.com">keepsafe.ecuador@gmail.com</a></p>
            <p style="margin-top:12px"><strong>Teléfonos:</strong></p>
            <p><a href="https://wa.me/593983899314?text=Hola,%20me%20interesa%20información%20sobre%20sus%20servicios" target="_blank">+593 98 389 9314</a></p>
            <p><a href="https://wa.me/593963632101?text=Hola,%20me%20interesa%20información%20sobre%20sus%20servicios" target="_blank">+593 96 363 2101</a></p>
        </div>
    </div>
    <div class="ks-footer-bottom">
        <p>&copy; 2025 Keep Safe S.A.S. Todos los derechos reservados.</p>
    </div>
</div>
""", unsafe_allow_html=True)