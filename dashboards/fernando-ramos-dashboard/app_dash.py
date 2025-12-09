import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# --- 1. Carga y Preparación de Datos ---

def cargar_y_preparar_datos():
    """
    Carga, prepara y devuelve el dataset de taxis de NYC junto con un resumen de la limpieza.
    """
    print("🔄 Cargando y preparando datos...")
    try:
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
        datos_dir = os.path.join(project_root, "datos")
        csv_path = os.path.join(datos_dir, "nyc_taxi.csv")

        if not os.path.exists(csv_path):
            print(f"❌ Error: No se encontró el archivo en: {csv_path}")
            return None, None

        df_raw = pd.read_csv(csv_path, low_memory=False)
        
        initial_rows = len(df_raw)
        initial_nulls = df_raw.isnull().sum()
        initial_dtypes = df_raw.dtypes
        
        df = df_raw.copy()
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce')
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce')

        df.dropna(subset=['total_amount', 'trip_distance', 'passenger_count', 'payment_type', 'tip_amount', 'tpep_pickup_datetime', 'tpep_dropoff_datetime'], inplace=True)
        df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 50) & (df['total_amount'] > 0) & (df['total_amount'] < 500)].copy()
        
        final_rows = len(df)
        
        df['hora_pickup'] = df['tpep_pickup_datetime'].dt.hour
        df['dia_semana'] = df['tpep_pickup_datetime'].dt.day_name()
        
        resumen_calidad = {
            "filas_iniciales": initial_rows,
            "filas_eliminadas": initial_rows - final_rows,
            "filas_finales": final_rows,
            "nulos_iniciales": initial_nulls[initial_nulls > 0].to_dict(),
            "tipos_datos_iniciales": initial_dtypes.astype(str).to_dict()
        }
        
        print("✅ Datos cargados y preparados.")
        return df, resumen_calidad

    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None, None

df, resumen_calidad_global = cargar_y_preparar_datos()

# --- 2. Inicialización de la App Dash ---

app = dash.Dash(__name__)

# --- 3. Layout de la Aplicación ---

if df is not None:
    dias_semana_options = [{'label': 'Todos los Días', 'value': 'All'}] + \
                          [{'label': dia, 'value': dia} for dia in df['dia_semana'].unique()]

    app.layout = html.Div([
        html.H1("Dashboard de Análisis Exploratorio - Taxis de NYC", style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Div([
            html.Div([
                html.Label("Selecciona un día de la semana:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='dropdown-dia-semana', options=dias_semana_options, value='All'),
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '20px'}),
            html.Div(id='kpi-container', style={'width': '68%', 'display': 'inline-block', 'textAlign': 'center', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),

        html.Div([
            html.Div(id='calidad-datos-output', style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '1%'}),
            html.Div(id='estadisticas-output', style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '1%'})
        ], style={'marginBottom': '20px'}),

        html.Div([
            dcc.Graph(id='grafico-viajes-por-dia'),
            dcc.Graph(id='grafico-tipo-pago'),
            dcc.Graph(id='grafico-pasajeros-hora'),
            dcc.Graph(id='grafico-distancia-hist'),
            dcc.Graph(id='grafico-tarifa-hist'),
            dcc.Graph(id='grafico-distancia-vs-tarifa'),
            dcc.Graph(id='grafico-propina-vs-importe'),
            dcc.Graph(id='grafico-propina-por-pago'),
        ])
    ])
else:
    app.layout = html.Div([html.H1("Error al cargar los datos.")])

# --- 4. Callbacks para la Interactividad ---

@app.callback(
    [Output('kpi-container', 'children'),
     Output('calidad-datos-output', 'children'),
     Output('estadisticas-output', 'children'),
     Output('grafico-viajes-por-dia', 'figure'),
     Output('grafico-tipo-pago', 'figure'),
     Output('grafico-pasajeros-hora', 'figure'),
     Output('grafico-distancia-hist', 'figure'),
     Output('grafico-tarifa-hist', 'figure'),
     Output('grafico-distancia-vs-tarifa', 'figure'),
     Output('grafico-propina-vs-importe', 'figure'),
     Output('grafico-propina-por-pago', 'figure')],
    [Input('dropdown-dia-semana', 'value')]
)
def actualizar_dashboard(dia_seleccionado):
    if df is None:
        return [html.Div()] * 11

    print(f"🔄 Actualizando dashboard para: {dia_seleccionado}")
    
    if dia_seleccionado == 'All':
        df_filtrado = df
        titulo_sufijo = " (Todos los Días)"
    else:
        df_filtrado = df[df['dia_semana'] == dia_seleccionado]
        titulo_sufijo = f" ({dia_seleccionado})"

    # --- 1. KPIs ---
    kpis = html.Div([
        html.Div(f"Total Viajes: {len(df_filtrado):,.0f}", style={'display': 'inline-block', 'fontSize': 20, 'margin': '0 20px'}),
        html.Div(f"Tarifa Media: ${df_filtrado['total_amount'].mean():,.2f}", style={'display': 'inline-block', 'fontSize': 20, 'margin': '0 20px'}),
        html.Div(f"Distancia Media: {df_filtrado['trip_distance'].mean():,.2f} mi", style={'display': 'inline-block', 'fontSize': 20, 'margin': '0 20px'}),
    ])

    # --- 2. Análisis de Calidad de Datos (con estilo mejorado) ---
    calidad_div = html.Div([
        html.H3("Análisis de Calidad de Datos", style={'textAlign': 'center', 'color': '#333'}),
        html.P(f"Filas iniciales: {resumen_calidad_global['filas_iniciales']:,}"),
        html.P(f"Filas eliminadas (nulos/outliers): {resumen_calidad_global['filas_eliminadas']:,}", style={'color': '#dc3545'}),
        html.P(f"Filas finales para análisis: {resumen_calidad_global['filas_finales']:,}", style={'fontWeight': 'bold', 'color': '#28a745'}),
        html.H4("Valores Nulos Iniciales (Top 5)", style={'marginTop': '15px'}),
        html.Table([
            html.Thead(html.Tr([html.Th("Columna"), html.Th("Nulos")])),
            html.Tbody([
                html.Tr([html.Td(col), html.Td(f"{count:,}")])
                for col, count in list(resumen_calidad_global['nulos_iniciales'].items())[:5]
            ])
        ])
    ], style={'border': '1px solid #e9ecef', 'padding': '20px', 'borderRadius': '8px', 'backgroundColor': '#ffffff', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)'})

    # --- 3. Estadísticas Descriptivas (con estilo mejorado) ---
    stats_df = df_filtrado[['trip_distance', 'total_amount', 'tip_amount']].describe().round(2)
    estadisticas_div = html.Div([
        html.H3("Estadísticas Descriptivas" + titulo_sufijo, style={'textAlign': 'center', 'color': '#333'}),
        html.Table([
            html.Thead(html.Tr([html.Th('Métrica', style={'textAlign': 'left'})] + [html.Th(col) for col in stats_df.columns])),
            html.Tbody([
                html.Tr([html.Td(index, style={'fontWeight': 'bold'})] + [html.Td(stats_df.loc[index, col]) for col in stats_df.columns])
                for index in stats_df.index
            ])
        ])
    ], style={'border': '1px solid #e9ecef', 'padding': '20px', 'borderRadius': '8px', 'backgroundColor': '#ffffff', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.05)'})

    # --- 4. Gráficos ---
    payment_map = {1: 'Tarjeta', 2: 'Efectivo', 3: 'Sin Cargo', 4: 'Disputa', 5: 'Desconocido', 6: 'Viaje Anulado'}
    df_filtrado['payment_type_desc'] = df_filtrado['payment_type'].map(payment_map).fillna('Otro')
    
    viajes_por_dia = df.groupby('dia_semana').size().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index(name='count')
    fig_viajes_dia = px.bar(viajes_por_dia, x='dia_semana', y='count', title='Total de Viajes por Día de la Semana')

    fig_tipo_pago = px.pie(df_filtrado, names='payment_type_desc', title='Distribución por Tipo de Pago' + titulo_sufijo, hole=.3)
    fig_tipo_pago.update_traces(textposition='inside', textinfo='percent+label')

    pasajeros_hora = df_filtrado.groupby('hora_pickup')['passenger_count'].sum().reset_index()
    fig_pasajeros_hora = px.bar(pasajeros_hora, x='hora_pickup', y='passenger_count', title=f'Total de Pasajeros por Hora' + titulo_sufijo)

    fig_dist_hist = px.histogram(df_filtrado, x='trip_distance', nbins=50, title='Distribución de Distancia del Viaje' + titulo_sufijo)
    fig_tarifa_hist = px.histogram(df_filtrado, x='total_amount', nbins=50, title='Distribución de la Tarifa Total' + titulo_sufijo)

    df_sample = df_filtrado.sample(n=min(2000, len(df_filtrado)), random_state=42)
    fig_dist_vs_tarifa = px.scatter(df_sample, x='trip_distance', y='total_amount', title='Distancia vs. Tarifa' + titulo_sufijo, opacity=0.5)

    fig_propina_vs_importe = px.scatter(df_sample, x='total_amount', y='tip_amount', title='Relación entre Importe Total y Propina' + titulo_sufijo, labels={'total_amount': 'Importe Total ($)', 'tip_amount': 'Propina ($)'}, opacity=0.5)

    df_con_propina = df_filtrado[df_filtrado['tip_amount'] > 0]
    fig_propina_por_pago = px.box(df_con_propina, x='payment_type_desc', y='tip_amount', title='Distribución de Propinas por Tipo de Pago' + titulo_sufijo, labels={'payment_type_desc': 'Tipo de Pago', 'tip_amount': 'Propina ($)'}, color='payment_type_desc')

    return kpis, calidad_div, estadisticas_div, fig_viajes_dia, fig_tipo_pago, fig_pasajeros_hora, fig_dist_hist, fig_tarifa_hist, fig_dist_vs_tarifa, fig_propina_vs_importe, fig_propina_por_pago

# --- 5. Ejecución de la Aplicación ---
if __name__ == '__main__':
    if df is not None:
        app.run(debug=True)
    else:
        print("\n🚫 La aplicación no puede iniciar porque los datos no se cargaron.")
