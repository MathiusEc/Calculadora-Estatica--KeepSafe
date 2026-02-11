# Keep Safe Operation - Calculadora de Mezclas

Calculadora de mezclas y operaciones para drones agrícolas **DJI Agras T50**. Esta herramienta está diseñada para complementar la Hoja de Recomendaciones Operativas de Keep Safe S.A.S., permitiendo calcular mezclas de productos fitosanitarios, gestionar ciclos de aplicación y determinar parámetros técnicos de manera precisa.

## Cultivos Soportados
- Banano
- Maíz
- Arroz
- Cacao

## Características

- Cálculo automático de mezclas por hectárea y totales
- Orden de mezcla personalizable para aplicación correcta
- Parámetros técnicos de vuelo y aplicación para DJI Agras T50
- Estimación de recursos: vuelos necesarios, tiempo y solución total
- Validación de datos para evitar errores en la mezcla
- Interfaz intuitiva con diseño responsive
- Recomendaciones técnicas específicas por cultivo

## Tecnologías

- Streamlit: Framework de aplicaciones web
- Python 3.8+: Lenguaje de programación
- Pandas: Procesamiento de datos
- Pillow: Procesamiento de imágenes

## Instalación Local

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd Calculadora-KeepSafe
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

## Despliegue

La aplicación está desplegada en Streamlit Cloud y es accesible a través del link compartido.

### Despliegue Manual

1. Sube tu código a GitHub (repositorio privado o público)
2. Conecta tu repositorio a Streamlit Cloud
3. Selecciona el archivo `app.py` como punto de entrada
4. ¡Listo! La app estará disponible en pocos minutos

## Uso

1. Selecciona el cultivo y especifica las hectáreas a aplicar
2. Define la fecha de aplicación
3. Configura los productos a aplicar con sus cantidades y orden de mezcla
4. Revisa los resultados: mezcla calculada, agua necesaria y reactivos totales
5. Consulta las recomendaciones técnicas para el operador del dron

## Acerca de Keep Safe S.A.S.

Keep Safe S.A.S. es una empresa ecuatoriana que integra tecnología, drones y conocimiento técnico para brindar soluciones de agricultura de precisión, bioseguridad y gestión del riesgo.

## Licencia

© 2025 Keep Safe S.A.S. Todos los derechos reservados.

---

**Nota**: Esta aplicación es de uso exclusivo para clientes y colaboradores de Keep Safe S.A.S. El código fuente es privado y confidencial.
