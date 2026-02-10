
import streamlit as st
from PIL import Image
import pandas as pd

# Función para cargar CSS externo
def load_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Si el archivo no existe, continúa sin estilos

# Cargar estilos
load_css("style.css")

# Logo
logo = Image.open("logo1.0.png")
st.image(logo, width=180)

st.title("Keep Safe Operation")
st.markdown("### Hoja de Recomendaciones Operativas para Fumigación con Dron DJI Agras T50")

# Cultivos data
cultivos_data = {
    "Banano": {"tasa_aplicacion": 18, "velocidad": "20-30 km/h", "altura": "7-8 m", "ancho_faja": "7-9.5 m", "gota": "Fina/Media"},
    "Maíz": {"tasa_aplicacion": 19, "velocidad": "20-25 km/h", "altura": "5-6 m", "ancho_faja": "7-8.5 m", "gota": "Fina/Media/Gruesa"},
    "Arroz": {"tasa_aplicacion": 16.5, "velocidad": "25-30 km/h", "altura": "4-7 m", "ancho_faja": "6.5-8 m", "gota": "Muy Fina/Fina/Media"},
    "Cacao": {"tasa_aplicacion": 25, "velocidad": "20-25 km/h", "altura": "7 m", "ancho_faja": "7-8.5 m", "gota": "Muy Fina/Fina/Media"},
}


# Selección de cultivo y datos de entrada
st.markdown("---")
st.subheader("Datos Generales")
col1, col2, col3 = st.columns(3)
with col1:
    cultivo = st.selectbox("Cultivo", list(cultivos_data.keys()))
with col2:
    hectareas = st.number_input("Hectáreas", min_value=0.1, step=0.1, value=1.0)
with col3:
    fecha_aplicacion = st.date_input("Fecha de aplicación", key="fecha_aplicacion")

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

st.markdown(":green[Frecuencia (días desde última aplicación):]" if frecuencia is not None else ":blue[Primera aplicación del año]")
if frecuencia is not None:
    st.info(f"Frecuencia: {frecuencia} días")
    st.info(f"Ciclo: {ciclo}")
else:
    st.info("Esta es la primera aplicación del año. El ciclo no se llena.")

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

# Configuración de mezcla
st.markdown("---")
st.subheader("Configuración de Mezcla")

with st.expander("Productos a aplicar", expanded=True):
    num_productos = st.number_input("¿Cuántos productos va a usar?", min_value=1, max_value=10, value=1, step=1)
    
    # Tabla dinámica de productos
    productos_mezcla = []
    if num_productos > 0:
        for i in range(int(num_productos)):
            st.markdown(f"**Producto {i+1}**")
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                producto = st.selectbox(f"Nombre", productos_disponibles, key=f"prod_{i}", label_visibility="collapsed")
            with col2:
                cantidad = st.number_input(f"Cantidad (L/ha)", min_value=0.0, step=0.01, key=f"cant_{i}", format="%.3f")
            with col3:
                orden = st.number_input(f"Orden", min_value=1, max_value=10, value=i+1, step=1, key=f"orden_{i}")
            
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
    
    # Mostrar tablas
    st.markdown("---")
    st.subheader("Resultados de Mezcla")
    
    # Tabla para 1 ha
    st.markdown("#### Para 1 Hectárea")
    tabla_1ha = pd.DataFrame([
        {"Producto": p['producto'], "Cantidad (L/ha)": f"{p['cantidad']:.3f}", "Orden": p['orden']}
        for p in productos_mezcla_ordenados
    ])
    st.dataframe(tabla_1ha, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Suma de Reactivos", f"{suma_reactivos_1ha:.3f} L/ha")
    with col2:
        st.metric("Total Mezcla", f"{total_mezcla_1ha:.3f} L/ha")
    with col3:
        st.metric("Agua Necesaria", f"{agua_necesaria_1ha:.3f} L/ha")
    
    # Tabla para total de hectáreas
    st.markdown("---")
    st.markdown(f"#### Para {hectareas:.1f} Hectáreas (Total)")
    tabla_total = pd.DataFrame([
        {"Producto": p['producto'], "Cantidad Total (L)": f"{p['cantidad'] * hectareas:.3f}", "Orden": p['orden']}
        for p in productos_mezcla_ordenados
    ])
    st.dataframe(tabla_total, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Suma de Reactivos", f"{suma_reactivos_total:.3f} L")
    with col2:
        st.metric("Total Mezcla", f"{total_mezcla_total:.3f} L")
    with col3:
        st.metric("Agua Necesaria", f"{agua_necesaria_total:.3f} L")

# Mostrar Recomendaciones Técnicas y Cálculos Operativos
if cultivo and hectareas and productos_mezcla:
    datos = cultivos_data[cultivo]
    tasa = datos["tasa_aplicacion"]
    total_sol = tasa * hectareas
    vuelos = total_sol / 40
    tiempo = vuelos * 10 / 60

    st.markdown("---")
    
    with st.expander("Recomendaciones Técnicas - para el operador", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            velocidad = st.text_input(f"Velocidad (rango sugerido: {datos['velocidad']})")
            altura = st.text_input(f"Altura (rango sugerido: {datos['altura']})")
            faja = st.text_input(f"Ancho de faja (rango sugerido: {datos['ancho_faja']})")
        with col2:
            gota = st.text_input(f"Tamaño de gota (sugerido: {datos['gota']})")
            tasa_aplicacion_input = st.text_input(f"Tasa de aplicación (sugerida: {tasa} L/ha)", value=str(tasa))

    st.markdown("---")
    st.subheader("Cálculos Operativos")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Solución Total", f"{total_sol:.2f} L")
    with col2:
        st.metric("Vuelos Estimados", f"{vuelos:.0f}")
    with col3:
        st.metric("Tiempo Estimado", f"{tiempo:.2f} h")
