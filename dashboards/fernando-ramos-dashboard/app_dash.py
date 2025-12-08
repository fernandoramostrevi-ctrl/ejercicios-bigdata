import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# --- 1. Carga y Preparación de Datos ---

def cargar_y_preparar_datos():
    """
    Carga y prepara el dataset de taxis de NYC.
    """
    print("🔄 Cargando y preparando datos...")
    try:
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
        datos_dir = os.path.join(project_root, "datos")
        csv_path = os.path.join(datos_dir, "nyc_taxi.csv")

        if not os.path.exists(csv_path):
            print(f"❌ Error: No se encontró el archivo en: {csv_path}")
            return None

        df = pd.read_csv(csv_path, low_memory=False, parse_dates=['tpep_pickup_datetime'])
        
        # Limpieza y Feature Engineering
        df.dropna(subset=['total_amount', 'trip_distance', 'passenger_count', 'payment_type', 'tip_amount'], inplace=True)
        df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 50) & (df['total_amount'] > 0) & (df['total_amount'] < 500)].copy()
        df['hora_pickup'] = df['tpep_pickup_datetime'].dt.hour
        df['dia_semana'] = df['tpep_pickup_datetime'].dt.day_name()
        
        print("✅ Datos cargados y preparados.")
        return df
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

df = cargar_y_preparar_datos()

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
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div(id='kpi-container', style={'width': '68%', 'display': 'inline-block', 'textAlign': 'center', 'verticalAlign': 'top'}),
        ], style={'marginBottom': '20px'}),

        html.Div([
            dcc.Graph(id='grafico-viajes-por-dia'),
            dcc.Graph(id='grafico-tipo-pago'),
            dcc.Graph(id='grafico-pasajeros-hora'),
            dcc.Graph(id='grafico-distancia-hist'),
            dcc.Graph(id='grafico-tarifa-hist'),
            dcc.Graph(id='grafico-distancia-vs-tarifa'),
            dcc.Graph(id='grafico-propina-vs-importe'),
            dcc.Graph(id='grafico-propina-por-pago'), # Nuevo gráfico de cajas
        ])
    ])
else:
    app.layout = html.Div([html.H1("Error al cargar los datos.")])

# --- 4. Callbacks para la Interactividad ---

@app.callback(
    [Output('kpi-container', 'children'),
     Output('grafico-viajes-por-dia', 'figure'),
     Output('grafico-tipo-pago', 'figure'),
     Output('grafico-pasajeros-hora', 'figure'),
     Output('grafico-distancia-hist', 'figure'),
     Output('grafico-tarifa-hist', 'figure'),
     Output('grafico-distancia-vs-tarifa', 'figure'),
     Output('grafico-propina-vs-importe', 'figure'),
     Output('grafico-propina-por-pago', 'figure')], # Output para el nuevo gráfico
    [Input('dropdown-dia-semana', 'value')]
)
def actualizar_dashboard(dia_seleccionado):
    if df is None:
        return [html.Div()] + [{}] * 8 # Actualizado a 8 gráficos

    print(f"🔄 Actualizando dashboard para: {dia_seleccionado}")
    
    if dia_seleccionado == 'All':
        df_filtrado = df
        titulo_sufijo = " (Todos los Días)"
    else:
        df_filtrado = df[df['dia_semana'] == dia_seleccionado]
        titulo_sufijo = f" ({dia_seleccionado})"

    # --- KPIs ---
    kpis = html.Div([
        html.Div(f"Total Viajes: {len(df_filtrado):,.0f}", style={'display': 'inline-block', 'fontSize': 20, 'margin': '0 20px'}),
        html.Div(f"Tarifa Media: ${df_filtrado['total_amount'].mean():,.2f}", style={'display': 'inline-block', 'fontSize': 20, 'margin': '0 20px'}),
        html.Div(f"Distancia Media: {df_filtrado['trip_distance'].mean():,.2f} mi", style={'display': 'inline-block', 'fontSize': 20, 'margin': '0 20px'}),
    ])

    # --- Gráficos ---
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

    # Nuevo Gráfico: Distribución de propinas por tipo de pago
    df_con_propina = df_filtrado[df_filtrado['tip_amount'] > 0]
    fig_propina_por_pago = px.box(
        df_con_propina,
        x='payment_type_desc',
        y='tip_amount',
        title='Distribución de Propinas por Tipo de Pago (Propinas > 0)' + titulo_sufijo,
        labels={'payment_type_desc': 'Tipo de Pago', 'tip_amount': 'Propina ($)'},
        color='payment_type_desc'
    )

    return kpis, fig_viajes_dia, fig_tipo_pago, fig_pasajeros_hora, fig_dist_hist, fig_tarifa_hist, fig_dist_vs_tarifa, fig_propina_vs_importe, fig_propina_por_pago

# --- 5. Ejecución de la Aplicación ---

if __name__ == '__main__':
    if df is not None:
        app.run(debug=True)
    else:
        print("\n🚫 La aplicación no puede iniciar porque los datos no se cargaron.")
