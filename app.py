
import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Keep Safe Operation - Calculadora de Mezclas",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Función para cargar CSS externo
def load_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Si el archivo no existe, continúa sin estilos

# Cargar estilos
load_css("style.css")

# ============================================
# SECCIÓN 1: LOGO Y TÍTULO
# ============================================
logo = Image.open("logo1.0.png")
col_logo, col_space = st.columns([1, 4])
with col_logo:
    st.image(logo, width=180)

st.title("Keep Safe Operation")
st.markdown("### Calculadora de Mezclas y Operaciones para Drones Agrícolas DJI Agras T50")

# ============================================
# SECCIÓN 2: DESCRIPCIÓN BREVE
# ============================================
st.markdown("""
<div class="descripcion-intro">
    <p style="margin: 0; font-size: 1.05rem; line-height: 1.8;">
        Bienvenido a la <strong>Calculadora de Mezclas y Operaciones para Drones Agrícolas DJI Agras T50</strong>. 
        Esta herramienta está diseñada para complementar la Hoja de Recomendaciones Operativas, permitiendo 
        calcular mezclas de productos fitosanitarios, gestionar ciclos de aplicación y determinar parámetros 
        técnicos de manera precisa y alineada con las mejores prácticas de operación segura. 
        Optimice sus aplicaciones agrícolas con agricultura de precisión.
    </p>
</div>
""", unsafe_allow_html=True)

# Cultivos data
cultivos_data = {
    "Banano": {"tasa_aplicacion": 18, "velocidad": "20-30 km/h", "altura": "7-8 m", "ancho_faja": "7-9.5 m", "gota": "Fina/Media"},
    "Maíz": {"tasa_aplicacion": 19, "velocidad": "20-25 km/h", "altura": "5-6 m", "ancho_faja": "7-8.5 m", "gota": "Fina/Media/Gruesa"},
    "Arroz": {"tasa_aplicacion": 16.5, "velocidad": "25-30 km/h", "altura": "4-7 m", "ancho_faja": "6.5-8 m", "gota": "Muy Fina/Fina/Media"},
    "Cacao": {"tasa_aplicacion": 25, "velocidad": "20-25 km/h", "altura": "7 m", "ancho_faja": "7-8.5 m", "gota": "Muy Fina/Fina/Media"},
}


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
# SECCIÓN 4: HISTORIAL DE APLICACIONES
# ============================================
st.markdown("---")
st.subheader("Historial y Ciclos de Aplicación")

# Simulación de historial de aplicaciones previas (para demo)
historial_aplicaciones = [
    {"cultivo": "Banano", "fecha": pd.to_datetime("2026-01-10")},
    {"cultivo": "Banano", "fecha": pd.to_datetime("2026-02-01")},
    {"cultivo": "Maíz", "fecha": pd.to_datetime("2026-01-15")},
]

# Calcular ciclo y frecuencia
ciclo = 1
frecuencia = None
aplicaciones_cultivo = [a for a in historial_aplicaciones if a["cultivo"] == cultivo and a["fecha"].year == fecha_aplicacion.year]
if aplicaciones_cultivo:
    fechas_previas = sorted([a["fecha"] for a in aplicaciones_cultivo])
    ult_fecha = fechas_previas[-1]
    if ult_fecha < pd.to_datetime(fecha_aplicacion):
        frecuencia = (pd.to_datetime(fecha_aplicacion) - ult_fecha).days
        ciclo = len(fechas_previas) + 1
    else:
        frecuencia = None
        ciclo = len(fechas_previas)
else:
    ciclo = 1
    frecuencia = None

# Mostrar información de ciclos
if frecuencia is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Frecuencia", f"{frecuencia} días", "Desde última aplicación")
    with col2:
        st.metric("Ciclo", f"{ciclo}", "Aplicación del año")
    
    # Mostrar historial en tabla
    with st.expander("Ver historial de aplicaciones"):
        historial_df = pd.DataFrame([
            {"Cultivo": a["cultivo"], "Fecha": a["fecha"].strftime("%d/%m/%Y")}
            for a in aplicaciones_cultivo
        ])
        st.dataframe(historial_df, use_container_width=True, hide_index=True)
else:
    st.info("✨ Esta es la primera aplicación del año. El ciclo comenzará con esta aplicación.")

# Lista de productos agroquímicos comunes
productos_disponibles = [
    "Seleccionar...",
    "Glifosato 480 SL",
    "Paraquat",
    "2,4-D",
    "Mancozeb",
    "Clorpirifos",
    "Cipermetrina",
    "Lambda Cyhalotrina",
    "Folliup",
    "Kill Bac",
    "Cari Gold",
    "Azoxistrobina",
    "Tebuconazol",
    "Aceite Agrícola",
    "Adherente",
    "Urea Foliar",
    "Nitrato de Potasio",
    "Fosfito de Potasio",
    "Otro"
]

# ============================================
# SECCIÓN 5: CONFIGURACIÓN DE MEZCLA
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
    if num_productos > 0:
        for i in range(int(num_productos)):
            st.markdown(f"**Producto {i+1}**")
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                producto = st.selectbox(f"Nombre del producto", productos_disponibles, key=f"prod_{i}")
            with col2:
                cantidad = st.number_input(f"Cantidad (L/ha)", min_value=0.0, step=0.01, key=f"cant_{i}", format="%.3f")
            with col3:
                orden = st.number_input(f"Orden de mezcla", min_value=1, max_value=10, value=i+1, step=1, key=f"orden_{i}")
            
            if producto != "Seleccionar..." and cantidad > 0:
                productos_mezcla.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "orden": orden
                })
            
            if i < num_productos - 1:
                st.markdown("")

# Cálculos automáticos
if productos_mezcla and hectareas > 0:
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
    # SECCIÓN 6: RESULTADOS DE MEZCLA
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
    # SECCIÓN 7: RECOMENDACIONES TÉCNICAS
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
    # SECCIÓN 8: CÁLCULOS OPERATIVOS
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
        - **Ciclo de aplicación:** {'Primer ciclo del año' if frecuencia is None else f'Ciclo {ciclo} - {frecuencia} días desde última aplicación'}
        """)

# ============================================
# PIE DE PÁGINA
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: var(--color-gray);">
    <p style="margin: 0; font-size: 0.9rem;">
        <strong>Keep Safe Operation</strong> | Agricultura de Precisión con Drones DJI Agras T50
    </p>
    <p style="margin: 0.5rem 0; font-size: 0.85rem;">
        Herramienta diseñada para complementar la Hoja de Recomendaciones Operativas
    </p>
    <p style="margin: 1rem 0 0 0; font-size: 0.8rem; opacity: 0.7;">
        © 2026 Keep Safe. Todos los derechos reservados.
    </p>
</div>
""", unsafe_allow_html=True)
