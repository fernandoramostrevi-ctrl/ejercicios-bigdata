import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import numpy as np # <--- ¡IMPORTACIÓN AÑADIDA!
import os
import warnings

# Ignorar FutureWarnings de pandas/numpy
warnings.filterwarnings('ignore', category=FutureWarning)

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Rutas absolutas basadas en la ubicación de este script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "datos", "processed")
OUTPUT_HTML_PATH = os.path.join(PROJECT_ROOT, "trabajo_final", "plantilla", "informes", "dashboard_asia_central_profesional.html")

# Paleta de colores consistente
COLORES_PAISES = {
    'Kazakhstan': '#1f77b4',  # Azul
    'Kyrgyzstan': '#ff7f0e',  # Naranja
    'Tajikistan': '#2ca02c',  # Verde
    'Turkmenistan': '#d62728',  # Rojo
    'Uzbekistan': '#9467bd'  # Púrpura
}

# Configuración visual general
TEMPLATE = "plotly_white"
FONT_FAMILY = "Arial, sans-serif"
FONT_SIZE_TITLE = 16
FONT_SIZE_AXIS = 14
FONT_SIZE_TICK = 12

# ============================================================================
# FUNCIÓN PARA CARGAR DATOS
# ============================================================================

def cargar_datos():
    """Carga y combina los CSVs particionados desde la salida de Spark."""
    csv_folder = os.path.join(PROCESSED_DATA_DIR, "asia_central_processed_csv")
    
    if not os.path.exists(csv_folder):
        raise FileNotFoundError(f"La carpeta de datos procesados no existe: {csv_folder}. Asegúrate de ejecutar pipeline.py primero.")

    csv_files = [os.path.join(csv_folder, f) for f in os.listdir(csv_folder) if f.startswith('part-') and f.endswith('.csv')]
    
    if not csv_files:
        raise FileNotFoundError(f"No se encontraron archivos 'part-*.csv' en la carpeta: {csv_folder}.")

    # Leer y concatenar todos los archivos CSV
    list_df = []
    for f in csv_files:
        list_df.append(pd.read_csv(f))
    
    df = pd.concat(list_df, ignore_index=True)
    
    # Validaciones
    assert len(df) == 103, f"Error: Se esperaban 103 registros, se encontraron {len(df)}"
    expected_countries = {'Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan', 'Uzbekistan'}
    assert set(df['cname'].unique()) == expected_countries, f"Error: Países no coinciden. Esperado: {expected_countries}, Encontrado: {set(df['cname'].unique())}"
    
    print(f"✅ Datos cargados: {df.shape[0]} registros, {df.shape[1]} columnas")
    print(f"   Países únicos: {sorted(df['cname'].unique())}")
    print(f"   Rango de años: {df['year'].min()}-{df['year'].max()}")
    
    return df

# ============================================================================
# FUNCIONES PARA GENERAR GRÁFICOS PLOTLY
# ============================================================================

def crear_grafico_recursos_pib(df):
    """Genera scatter plot Recursos vs PIB"""
    fig = go.Figure()

    # Calcular regresión
    df_clean = df.dropna(subset=['wdi_totalresrent', 'wdi_gdpcapcon2017'])
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df_clean['wdi_totalresrent'], np.log(df_clean['wdi_gdpcapcon2017']) # Regresión en escala logarítmica
    )
    x_reg = np.array([df_clean['wdi_totalresrent'].min(), df_clean['wdi_totalresrent'].max()])
    y_reg = np.exp(slope * x_reg + intercept) # Volver a escala lineal para graficar

    # Añadir puntos por país
    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais]
        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wdi_gdpcapcon2017'],
            mode='markers',
            name=pais,
            marker=dict(color=COLORES_PAISES[pais], size=10, opacity=0.7),
            hovertemplate=f"<b>{pais}</b><br>Año: %{{customdata[0]}}<br>Recursos: %{{x:.2f}}%<br>PIB: $ %{{y:,.0f}}<extra></extra>",
            customdata=df_pais[['year']].values
        ))
    
    # Añadir línea de regresión
    fig.add_trace(go.Scatter(
        x=x_reg,
        y=y_reg,
        mode='lines',
        name=f'Regresión (r={r_value:.3f})',
        line=dict(color='black', width=2, dash='dash'),
        showlegend=True
    ))

    fig.update_layout(
        title_text='Recursos Naturales vs PIB per cápita',
        xaxis_title='Recursos Naturales (% PIB)',
        yaxis_title='PIB per cápita (USD 2017, escala logarítmica)',
        yaxis_type='log',
        template=TEMPLATE,
        font_family=FONT_FAMILY,
        height=600, width=800,
        hovermode='closest',
        legend=dict(x=1.02, y=1, xanchor='left', yanchor='top'),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def crear_grafico_serie_temporal(df):
    """Genera líneas de evolución temporal del PIB"""
    fig = go.Figure()

    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais].sort_values('year')
        fig.add_trace(go.Scatter(
            x=df_pais['year'],
            y=df_pais['wdi_gdpcapcon2017'],
            mode='lines+markers',
            name=pais,
            line=dict(color=COLORES_PAISES[pais], width=2.5),
            marker=dict(size=4),
            hovertemplate=f"<b>{pais}</b><br>Año: %{{x}}<br>PIB: $ %{{y:,.0f}}<extra></extra>"
        ))
    
    # Línea vertical Crisis 2008
    fig.add_vline(x=2008, line_dash="dash", line_color="gray", line_width=2,
                  annotation_text="Crisis Financiera 2008", annotation_position="top right",
                  annotation=dict(font_size=11, bgcolor="rgba(255,255,255,0.8)"))

    fig.update_layout(
        title_text='Evolución PIB per cápita 2000-2021',
        xaxis_title='Año',
        yaxis_title='PIB per cápita (USD 2017, escala logarítmica)',
        yaxis_type='log',
        template=TEMPLATE,
        font_family=FONT_FAMILY,
        height=600, width=800,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def crear_grafico_recursos_corrupcion(df):
    """Genera scatter plot Recursos vs Control de Corrupción"""
    fig = go.Figure()

    # Calcular regresión
    df_clean = df.dropna(subset=['wdi_totalresrent', 'wbgi_cce'])
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df_clean['wdi_totalresrent'], df_clean['wbgi_cce']
    )
    x_reg = np.array([df_clean['wdi_totalresrent'].min(), df_clean['wdi_totalresrent'].max()])
    y_reg = slope * x_reg + intercept

    # Añadir puntos por país
    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais]
        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wbgi_cce'],
            mode='markers',
            name=pais,
            marker=dict(color=COLORES_PAISES[pais], size=10, opacity=0.7),
            hovertemplate=f"<b>{pais}</b><br>Año: %{{customdata[0]}}<br>Recursos: %{{x:.2f}}%<br>Corrupción: %{{y:.3f}}<extra></extra>",
            customdata=df_pais[['year']].values
        ))
    
    # Añadir línea de regresión
    fig.add_trace(go.Scatter(
        x=x_reg,
        y=y_reg,
        mode='lines',
        name=f'Regresión (r={r_value:.3f})',
        line=dict(color='black', width=2, dash='dash'),
        showlegend=True
    ))

    fig.update_layout(
        title_text='Recursos Naturales vs Control de Corrupción',
        xaxis_title='Recursos Naturales (% PIB)',
        yaxis_title='Control de Corrupción (Índice BM)',
        template=TEMPLATE,
        font_family=FONT_FAMILY,
        height=600, width=800,
        hovermode='closest',
        legend=dict(x=1.02, y=1, xanchor='left', yanchor='top'),
        annotations=[
            dict(
                x=0.98, y=0.02,
                xref='paper', yref='paper',
                text=f"<b>Correlación débil (r={r_value:.3f})</b><br>No se confirma 'maldición de recursos'",
                showarrow=False,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='gray',
                borderwidth=1,
                xanchor='right',
                yanchor='bottom',
                font=dict(size=11)
            )
        ],
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def crear_grafico_barras_eficiencia(df):
    """Genera gráfico de barras de eficiencia de recursos por país"""
    df_promedio = df.groupby('cname').agg(
        eficiencia_recursos=('eficiencia_recursos', 'mean'),
        wdi_totalresrent=('wdi_totalresrent', 'mean')
    ).reset_index().sort_values('eficiencia_recursos', ascending=True) # Ordenar ascendente para barras horizontales

    fig = px.bar(
        df_promedio,
        x='eficiencia_recursos',
        y='cname',
        orientation='h',
        color='cname',
        color_discrete_map=COLORES_PAISES,
        text='eficiencia_recursos',
        title='Eficiencia de Recursos por País (promedio 2000-2021)',
        labels={'eficiencia_recursos': 'Eficiencia (PIB / % Recursos)', 'cname': 'País'},
        log_x=True # Escala logarítmica en X
    )

    fig.update_traces(texttemplate='%{x:,.0f}', textposition='outside')
    fig.update_layout(
        xaxis_title='Eficiencia (PIB / % Recursos, escala logarítmica)',
        yaxis_title='País',
        template=TEMPLATE,
        font_family=FONT_FAMILY,
        height=600, width=800,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def crear_grafico_heatmap_correlacion(df):
    """Genera heatmap de matriz de correlación"""
    columnas = [
        'wdi_totalresrent', 'wdi_gdpcapcon2017', 'wbgi_cce', 'undp_hdi',
        'brecha_corrupcion_riqueza', 'eficiencia_recursos', 'indice_bienestar_redistributivo'
    ]
    nombres_desc = {
        'wdi_totalresrent': 'Recursos (%PIB)',
        'wdi_gdpcapcon2017': 'PIB per cápita',
        'wbgi_cce': 'Control corrupción',
        'undp_hdi': 'Desarrollo Humano',
        'brecha_corrupcion_riqueza': 'Brecha Gob-Riqueza',
        'eficiencia_recursos': 'Eficiencia Recursos',
        'indice_bienestar_redistributivo': 'Bienestar Compuesto'
    }

    df_clean = df[columnas].dropna()
    corr_matrix = df_clean.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=[nombres_desc[col] for col in columnas],
        y=[nombres_desc[col] for col in columnas],
        colorscale='RdBu',
        zmid=0, zmin=-1, zmax=1,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont=dict(size=11),
        hovertemplate='<b>%{y} vs %{x}</b><br>Correlación: %{z:.2f}<extra></extra>',
        colorbar=dict(title='Correlación', tickmode='linear', tick0=-1, dtick=0.5)
    ))

    fig.update_layout(
        title_text='Matriz de Correlación - Variables Clave',
        xaxis_tickangle=-45,
        template=TEMPLATE,
        font_family=FONT_FAMILY,
        height=800, width=900,
        margin=dict(l=150, r=100, t=100, b=150)
    )
    return fig

# ============================================================================
# FUNCIÓN PRINCIPAL PARA GENERAR EL DASHBOARD HTML
# ============================================================================

def generar_dashboard():
    """Genera el HTML completo con pestañas y gráficos interactivos."""
    df = cargar_datos()
    
    # Generar figuras Plotly
    fig1 = crear_grafico_recursos_pib(df)
    fig2 = crear_grafico_serie_temporal(df)
    fig3 = crear_grafico_recursos_corrupcion(df)
    fig4 = crear_grafico_barras_eficiencia(df)
    fig5 = crear_grafico_heatmap_correlacion(df)

    # Convertir figuras a HTML (solo el div del gráfico)
    fig1_html = fig1.to_html(include_plotlyjs=False, full_html=False)
    fig2_html = fig2.to_html(include_plotlyjs=False, full_html=False)
    fig3_html = fig3.to_html(include_plotlyjs=False, full_html=False)
    fig4_html = fig4.to_html(include_plotlyjs=False, full_html=False)
    fig5_html = fig5.to_html(include_plotlyjs=False, full_html=False)


    # HTML base con CSS y JavaScript para pestañas
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard Analítico: Asia Central</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: {FONT_FAMILY}; margin: 0; padding: 0; background-color: #f4f4f4; }}
            .container {{ width: 95%; margin: 20px auto; background-color: #fff; box-shadow: 0 0 10px rgba(0,0,0,0.1); padding: 20px; border-radius: 8px; }}
            h1 {{ text-align: center; color: #333; margin-bottom: 20px; font-size: 24px; }}
            .tabs {{ display: flex; border-bottom: 1px solid #ddd; margin-bottom: 20px; }}
            .tab-button {{ 
                background-color: #f1f1f1; border: none; outline: none; cursor: pointer;
                padding: 14px 20px; transition: 0.3s; font-size: 17px; border-radius: 5px 5px 0 0;
                margin-right: 5px;
            }}
            .tab-button:hover {{ background-color: #ddd; }}
            .tab-button.active {{ background-color: #ccc; border-bottom: 3px solid #1f77b4; }}
            .tab-content {{ display: none; padding: 20px 0; border-top: none; min-height: 900px; }}
            .tab-content.active {{ display: block; }}
            .plotly-graph-div {{ margin-bottom: 30px; border: 1px solid #eee; border-radius: 5px; padding: 10px; background-color: #fff; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Dashboard Analítico: Recursos Naturales y Desarrollo en Asia Central (2000-2021)</h1>
            
            <div class="tabs">
                <button class="tab-button active" onclick="openTab(event, 'tab1')">Recursos y Economía</button>
                <button class="tab-button" onclick="openTab(event, 'tab2')">Gobernanza y Eficiencia</button>
                <button class="tab-button" onclick="openTab(event, 'tab3')">Correlaciones</button>
            </div>

            <div id="tab1" class="tab-content active">
                {fig1_html}
                {fig2_html}
            </div>

            <div id="tab2" class="tab-content">
                {fig3_html}
                {fig4_html}
            </div>

            <div id="tab3" class="tab-content">
                {fig5_html}
            </div>
        </div>

        <script>
            function openTab(evt, tabName) {{
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tab-content");
                for (i = 0; i < tabcontent.length; i++) {{
                    tabcontent[i].style.display = "none";
                }}
                tablinks = document.getElementsByClassName("tab-button");
                for (i = 0; i < tablinks.length; i++) {{
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }}
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
                // Redimensionar gráficos Plotly al cambiar de pestaña
                var gd = document.getElementById(tabName).getElementsByClassName('js-plotly-plot');
                for (i = 0; i < gd.length; i++) {{
                    Plotly.relayout(gd[i].id, {{autosize: true}});
                }}
            }}

            // Abrir la primera pestaña por defecto al cargar
            document.addEventListener("DOMContentLoaded", function() {{
                document.querySelector(".tab-button").click();
            }});
        </script>
    </body>
    </html>
    """
    
    # Guardar el HTML final
    os.makedirs(os.path.dirname(OUTPUT_HTML_PATH), exist_ok=True)
    with open(OUTPUT_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"✅ Dashboard HTML generado: {OUTPUT_HTML_PATH}")
    print("   Ábrelo en tu navegador para interactuar.")

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == '__main__':
    generar_dashboard()
