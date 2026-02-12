import streamlit as st
import streamlit.components.v1 as components
import os

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Análisis Big Data",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título Principal
st.title("📊 Dashboard de Resultados: Quality of Government")
st.markdown("""
Este dashboard presenta los resultados del análisis de datos sobre el dataset QoG.
Se incluyen 5 visualizaciones interactivas generadas por el pipeline de Spark.
""")

# Ruta al directorio de outputs
OUTPUT_DIR = "output"

# Lista de archivos esperados (en orden)
expected_files = [
    "01_recursos_corrupcion.html",
    "02_recursos_pib.html",
    "03_serie_temporal_pib.html",
    "04_barras_eficiencia.html",
    "05_heatmap_correlacion.html"
]

# Verificar si el directorio existe
if not os.path.exists(OUTPUT_DIR):
    st.error(f"No se encontró el directorio '{OUTPUT_DIR}'. Asegúrate de ejecutar el pipeline primero.")
    st.stop()

# Función para limpiar nombres de archivos para títulos
def clean_title(filename):
    name = filename.replace(".html", "")
    # Quitar números iniciales (01_, 02_, etc)
    if name[0:2].isdigit() and name[2] == "_":
        name = name[3:]
    return name.replace("_", " ").title()

# Sidebar para navegación
st.sidebar.title("Navegación")
selection = st.sidebar.radio("Ir a:", ["Vista General"] + [clean_title(f) for f in expected_files])

if selection == "Vista General":
    st.header("Resumen de Gráficos")
    for filename in expected_files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            st.subheader(clean_title(filename))
            # Usar un contenedor con altura fija para cada gráfico
            components.html(html_content, height=600, scrolling=True)
            st.markdown("---")
        else:
            st.warning(f"Archivo no encontrado: {filename}")

else:
    # Mostrar solo el gráfico seleccionado
    # Encontrar el archivo correspondiente a la selección
    selected_file = None
    for f in expected_files:
        if clean_title(f) == selection:
            selected_file = f
            break
    
    if selected_file:
        filepath = os.path.join(OUTPUT_DIR, selected_file)
        if os.path.exists(filepath):
            st.header(selection)
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            components.html(html_content, height=800, scrolling=True)
        else:
            st.error(f"El archivo {selected_file} no se encuentra.")
