
import streamlit as st
from PIL import Image

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
cultivo = st.selectbox("Cultivo", list(cultivos_data.keys()))
hectareas = st.number_input("Hectáreas", min_value=0.1, step=0.1)

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
num_productos = st.number_input("¿Cuántos productos va a usar?", min_value=1, max_value=10, value=1, step=1)

# Tabla dinámica de productos
productos_mezcla = []
if num_productos > 0:
    st.markdown("#### Productos a aplicar")
    
    for i in range(int(num_productos)):
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            producto = st.selectbox(f"Producto {i+1}", productos_disponibles, key=f"prod_{i}")
        with col2:
            cantidad = st.number_input(f"Cantidad (L/ha o kg/ha)", min_value=0.0, step=0.01, key=f"cant_{i}", format="%.3f")
        with col3:
            orden = st.number_input(f"Orden de mezcla", min_value=1, max_value=10, value=i+1, step=1, key=f"orden_{i}")
        
        if producto != "Seleccionar..." and cantidad > 0:
            productos_mezcla.append({
                "producto": producto,
                "cantidad": cantidad,
                "orden": orden
            })

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
    st.subheader("Tabla de Mezcla - Para 1 Hectárea")
    
    # Tabla para 1 ha
    st.markdown("| Producto | Cantidad (L/ha) | Orden |")
    st.markdown("|----------|-----------------|-------|")
    for p in productos_mezcla_ordenados:
        st.markdown(f"| {p['producto']} | {p['cantidad']:.3f} | {p['orden']} |")
    
    st.markdown(f"| **SUMA DE REACTIVOS** | **{suma_reactivos_1ha:.3f}** | |")
    st.markdown(f"| **TOTAL MEZCLA** | **{total_mezcla_1ha:.3f}** | |")
    st.markdown(f"| **AGUA NECESARIA** | **{agua_necesaria_1ha:.3f}** | |")
    
    # Tabla para total de hectáreas
    st.markdown("---")
    st.subheader(f"Tabla de Mezcla - Para {hectareas:.1f} Hectáreas")
    
    st.markdown("| Producto | Cantidad Total (L) | Orden |")
    st.markdown("|----------|-------------------|-------|")
    for p in productos_mezcla_ordenados:
        cantidad_total = p['cantidad'] * hectareas
        st.markdown(f"| {p['producto']} | {cantidad_total:.3f} | {p['orden']} |")
    
    st.markdown(f"| **SUMA DE REACTIVOS** | **{suma_reactivos_total:.3f}** | |")
    st.markdown(f"| **TOTAL MEZCLA** | **{total_mezcla_total:.3f}** | |")
    st.markdown(f"| **AGUA NECESARIA** | **{agua_necesaria_total:.3f}** | |")

st.markdown("---")
condiciones_terreno = st.text_area(
    "Condiciones del terreno",
    placeholder="Ej: Terreno plano, con pendiente leve hacia el sur. Obstáculos: árboles dispersos, cables eléctricos en el borde este."
)


condiciones_ambientales = st.text_area(
    "Condiciones ambientales esperadas",
    placeholder="Ej: Aplicación entre 06h00 y 08h00. Viento <10 km/h. Temperatura 26°C aprox."
)


seguridad_observaciones = st.text_area(
    "Seguridad / Observaciones especiales",
    placeholder="Observaciones específicas según el producto o condiciones del sitio."
)


# Mostrar Recomendaciones Técnicas y Cálculos Operativos
if cultivo and hectareas and productos_mezcla:
    datos = cultivos_data[cultivo]
    tasa = datos["tasa_aplicacion"]
    total_sol = tasa * hectareas
    vuelos = total_sol / 40
    tiempo = vuelos * 10 / 60

    st.markdown("---")
    st.subheader("Recomendaciones Técnicas - para el operador")
    velocidad = st.text_input(f"Velocidad (rango sugerido: {datos['velocidad']})")
    altura = st.text_input(f"Altura (rango sugerido: {datos['altura']})")
    faja = st.text_input(f"Ancho de faja (rango sugerido: {datos['ancho_faja']})")
    gota = st.text_input(f"Tamaño de gota (sugerido: {datos['gota']})")
    tasa_aplicacion_input = st.text_input(f"Tasa de aplicación (sugerida: {tasa} L/ha)", value=str(tasa))

    st.subheader("Cálculos Operativos")
    st.write(f"Solución total: {total_sol:.2f} L")
    st.write(f"Vuelos: {vuelos:.0f}")
    st.write(f"Tiempo estimado: {tiempo:.2f} h")
