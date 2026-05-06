from dash import Dash, html, dcc, Input, Output
import os

# Instanciamos la aplicación Dash
app = Dash(__name__)

# Definimos el servidor para Gunicorn, tal como se pide en el Paso 1
server = app.server

# Ruta al directorio de outputs (donde están los HTML)
OUTPUT_DIR = "output"

expected_files = [
    "01_recursos_corrupcion.html",
    "02_recursos_pib.html",
    "03_serie_temporal_pib.html",
    "04_barras_eficiencia.html",
    "05_heatmap_correlacion.html"
]

def clean_title(filename):
    name = filename.replace(".html", "")
    if name[0:2].isdigit() and name[2] == "_":
        name = name[3:]
    return name.replace("_", " ").title()

def get_html_content(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return f"<h2>No se ha encontrado el archivo: {filename}. Asegúrate de haber ejecutado el pipeline.</h2>"

# Layout de la app en Dash
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("📊 Dashboard de Resultados: Quality of Government"),
    html.P("Este dashboard presenta los resultados del análisis de datos sobre el dataset QoG en Asia Central."),
    
    html.Label("Selecciona la visualización:"),
    dcc.Dropdown(
        id='file-selector',
        options=[{'label': clean_title(f), 'value': f} for f in expected_files],
        value=expected_files[0],
        style={'width': '50%', 'marginBottom': '20px'}
    ),
    
    html.Div(id='graph-container')
])

# Callback para actualizar el iframe con el archivo HTML seleccionado
@app.callback(
    Output('graph-container', 'children'),
    [Input('file-selector', 'value')]
)
def update_graph(selected_file):
    if not selected_file:
        return ""
    content = get_html_content(selected_file)
    return html.Iframe(
        srcDoc=content,
        style={'width': '100%', 'height': '800px', 'border': 'none', 'borderRadius': '5px', 'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'}
    )

# Configuración del bloque principal para producción, tal como se pide en el Paso 1
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000)
