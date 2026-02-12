
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import glob

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "datos", "processed", "asia_central_processed_csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "trabajo_final", "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    """Carga el CSV más reciente generado por Spark."""
    csv_files = glob.glob(os.path.join(PROCESSED_DATA_DIR, "part-*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No se encontraron archivos CSV en {PROCESSED_DATA_DIR}. Ejecuta el pipeline primero.")
    
    # Combinar fragmentos de Spark si hay varios
    df = pd.concat([pd.read_csv(f) for f in csv_files])
    # Asegurar tipos
    df['year'] = df['year'].astype(int)
    return df

def create_color_map():
    return {
        'Kazakhstan': '#1f77b4',
        'Kyrgyzstan': '#ff7f0e',
        'Tajikistan': '#2ca02c',
        'Turkmenistan': '#d62728',
        'Uzbekistan': '#9467bd'
    }

def get_pib_series(df):
    """Grafico 1: Serie Temporal PIB Log"""
    color_map = create_color_map()
    fig = go.Figure()
    
    for pais in df['cname'].unique():
        df_pais = df[df['cname'] == pais].sort_values('year')
        # Calcular cambio porcentual para el hover
        df_pais['pct_change'] = df_pais['wdi_gdpcapcon2017'].pct_change() * 100
        
        fig.add_trace(go.Scatter(
            x=df_pais['year'],
            y=df_pais['wdi_gdpcapcon2017'],
            name=pais,
            mode='lines+markers',
            line=dict(color=color_map[pais], width=2.5),
            marker=dict(size=4),
            customdata=df_pais[['pct_change']],
            hovertemplate="<b>" + pais + "</b><br>Año: %{x}<br>PIB: $%{y:,.0f}<br>Cambio: %{customdata[0]:.1f}%<extra></extra>"
        ))

    fig.add_shape(type="line", x0=2008, x1=2008, y0=0, y1=1, xref="x", yref="y domain",
                  line=dict(color="gray", width=2, dash="dash"))
    fig.add_annotation(x=2008, y=1, text="Crisis financiera 2008", showarrow=False, 
                       yanchor="bottom", xanchor="center", xref="x", yref="y domain")

    fig.update_layout(
        title="Evolución del PIB per cápita por país<br><sub>Asia Central 2000-2021</sub>",
        xaxis_title="Año",
        yaxis_title="PIB per cápita PPP (USD constantes 2017, escala log)",
        yaxis_type="log",
        hovermode="x unified",
        template="plotly_white",
        width=900, height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def get_recursos_vs_pib(df):
    """Grafico 2: Recursos vs PIB Scatter Log"""
    color_map = create_color_map()
    fig = go.Figure()
    
    for pais in df['cname'].unique():
        df_pais = df[df['cname'] == pais]
        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wdi_gdpcapcon2017'],
            name=pais,
            mode='markers',
            marker=dict(size=10, color=color_map[pais], opacity=0.7, line=dict(width=1, color='white')),
            customdata=df_pais[['year']],
            hovertemplate="<b>" + pais + "</b><br>Año: %{customdata[0]}<br>Recursos: %{x:.2f}%<br>PIB: $%{y:,.0f}<extra></extra>"
        ))
    
    # Calcular línea de tendencia simple para los datos
    import numpy as np
    from scipy import stats
    # Limpiar nulos para la regresión
    valid_data = df.dropna(subset=['wdi_totalresrent', 'wdi_gdpcapcon2017'])
    slope, intercept, r_value, p_value, std_err = stats.linregress(valid_data['wdi_totalresrent'], np.log10(valid_data['wdi_gdpcapcon2017']))
    
    line_x = np.array([valid_data['wdi_totalresrent'].min(), valid_data['wdi_totalresrent'].max()])
    line_y = 10**(slope * line_x + intercept)
    
    fig.add_trace(go.Scatter(
        x=line_x, y=line_y,
        mode='lines',
        name=f'Regresión (r={r_value:.3f})',
        line=dict(color='black', dash='dash', width=2)
    ))

    fig.update_layout(
        title="Recursos Naturales vs PIB per cápita<br><sub>Asia Central 2000-2021</sub>",
        xaxis_title="Recursos Naturales (% PIB)",
        yaxis_title="PIB per cápita PPP (USD constantes 2017, escala log)",
        yaxis_type="log",
        template="plotly_white",
        width=900, height=500,
        annotations=[dict(xref="paper", yref="paper", x=0.98, y=0.02, showarrow=False,
                         text=f"<b>Correlación positiva fuerte (r={r_value:.3f})</b>",
                         xanchor="right", yanchor="bottom", bgcolor="rgba(255,255,255,0.8)", bordercolor="gray", borderwidth=1)]
    )
    return fig

def get_recursos_vs_corr(df):
    """Grafico 3: Recursos vs Corrupción"""
    color_map = create_color_map()
    fig = go.Figure()
    
    for pais in df['cname'].unique():
        df_pais = df[df['cname'] == pais]
        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wbgi_cce'],
            name=pais,
            mode='markers',
            marker=dict(size=10, color=color_map[pais], opacity=0.7, line=dict(width=1, color='white')),
            customdata=df_pais[['year']],
            hovertemplate="<b>" + pais + "</b><br>Año: %{customdata[0]}<br>Recursos: %{x:.2f}%<br>Corrupción: %{y:.3f}<extra></extra>"
        ))
    
    from scipy import stats
    valid_data = df.dropna(subset=['wdi_totalresrent', 'wbgi_cce'])
    slope, intercept, r_value, p_value, std_err = stats.linregress(valid_data['wdi_totalresrent'], valid_data['wbgi_cce'])
    
    line_x = [valid_data['wdi_totalresrent'].min(), valid_data['wdi_totalresrent'].max()]
    line_y = [slope * x + intercept for x in line_x]
    
    fig.add_trace(go.Scatter(
        x=line_x, y=line_y,
        mode='lines',
        name=f'Regresión (r={r_value:.3f})',
        line=dict(color='black', dash='dash', width=2)
    ))

    fig.update_layout(
        title="Recursos Naturales vs Control de Corrupción<br><sub>Asia Central 2000-2021</sub>",
        xaxis_title="Recursos Naturales (% PIB)",
        yaxis_title="Control de Corrupción (Banco Mundial)",
        template="plotly_white",
        width=900, height=500,
        annotations=[dict(xref="paper", yref="paper", x=0.98, y=0.02, showarrow=False,
                         text=f"<b>Correlación débil (r={r_value:.3f})</b>",
                         xanchor="right", yanchor="bottom", bgcolor="rgba(255,255,255,0.8)", bordercolor="gray", borderwidth=1)]
    )
    return fig

def get_eficiencia_barras(df):
    """Grafico 4: Barras Eficiencia"""
    color_map = create_color_map()
    # Promedio por país
    df_avg = df.groupby('cname').agg({
        'eficiencia_recursos': 'mean',
        'wdi_totalresrent': 'mean'
    }).sort_values('eficiencia_recursos', ascending=False).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_avg['cname'],
        y=df_avg['eficiencia_recursos'],
        marker_color=[color_map[c] for c in df_avg['cname']],
        marker_line=dict(color='white', width=1.5),
        text=[f"{v:,.0f}" for v in df_avg['eficiencia_recursos']],
        textposition='outside',
        customdata=df_avg[['wdi_totalresrent']],
        hovertemplate="<b>%{x}</b><br>Eficiencia: %{y:,.0f}<br>Recursos promedio: %{customdata[0]:.2f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title="Eficiencia de Recursos por País<br><sub>Promedio 2000-2021</sub>",
        yaxis_title="Eficiencia (PIB / % Recursos, escala log)",
        xaxis_title="País",
        yaxis_type="log",
        template="plotly_white",
        width=900, height=500
    )
    return fig

def get_heatmap(df):
    """Grafico 5: Heatmap Correlación"""
    cols = ['wdi_totalresrent', 'wdi_gdpcapcon2017', 'wbgi_cce', 'undp_hdi', 
            'brecha_corrupcion_riqueza', 'eficiencia_recursos', 'indice_bienestar_redistributivo']
    labels = ["Recursos (%PIB)", "PIB per cápita", "Control corrupción", "Desarrollo Humano", 
              "Brecha Gob-Riqueza", "Eficiencia Recursos", "Bienestar Compuesto"]
    
    corr = df[cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale='RdBu',
        zmid=0,
        text=corr.values,
        texttemplate="%{z:.3f}",
        hovertemplate="<b>%{y} vs %{x}</b><br>Correlación: %{z:.3f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=f"Matriz de Correlación - Variables Clave<br><sub>Asia Central 2000-2021 (n={len(df)})</sub>",
        template="plotly_white",
        width=900, height=700
    )
    return fig

def generate_dashboard():
    print("Iniciando generación de dashboard profesional...")
    df = load_data()
    
    charts = [
        (get_pib_series(df), "Figura 1. Evolución del PIB per cápita por país (2000–2021)", "Serie temporal para observar divergencia económica y el impacto de la crisis de 2008."),
        (get_recursos_vs_pib(df), "Figura 2. Recursos Naturales vs PIB per cápita", "Relación entre renta extractiva (% PIB) y desempeño económico (PIB per cápita)."),
        (get_recursos_vs_corr(df), "Figura 3. Recursos Naturales vs Control de Corrupción", "Relación entre dependencia de recursos y calidad institucional (control de corrupción)."),
        (get_eficiencia_barras(df), "Figura 4. Eficiencia de Recursos por País (promedio 2000–2021)", "Comparación de la capacidad de convertir recursos en crecimiento económico."),
        (get_heatmap(df), "Figura 5. Matriz de Correlación (Variables Clave)", "Mapa global de relaciones entre variables económicas, sociales e institucionales.")
    ]
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Dashboard Asia Central (2000–2021)</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f4f6f9; color: #1f2937; }}
            .container {{ width: 90%; max-width: 1200px; margin: auto; padding: 40px 0; }}
            .header {{ background: #111827; color: white; padding: 60px 40px; border-radius: 18px; box-shadow: 0px 10px 25px rgba(0,0,0,0.25); }}
            .header h1 {{ size: 36px; margin: 0; font-weight: 700; }}
            .header h2 {{ size: 18px; margin-top: 12px; font-weight: 400; opacity: 0.9; }}
            .meta {{ margin-top: 25px; font-size: 14px; opacity: 0.85; }}
            .card {{ background: white; padding: 25px; border-radius: 16px; box-shadow: 0px 8px 20px rgba(0,0,0,0.08); margin-top: 25px; }}
            .card h3 {{ font-size: 18px; margin-top: 0; margin-bottom: 10px; }}
            .card p {{ font-size: 14px; margin-bottom: 20px; color: #374151; }}
            .footer {{ margin-top: 80px; padding: 30px; font-size: 13px; text-align: center; color: #6b7280; }}
            .badge {{ display: inline-block; padding: 6px 12px; border-radius: 999px; background: #2563eb; color: white; font-size: 12px; font-weight: 600; margin-bottom: 10px; }}
        </style>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <span class="badge">Dashboard Interactivo</span>
                <h1>Asia Central (2000–2021)</h1>
                <h2>Recursos Naturales, Crecimiento Económico y Corrupción</h2>
                <div class="meta">
                    <p><b>Autor:</b> Fernando Ramos</p>
                    <p><b>Fuente:</b> Quality of Government Dataset (QoG, enero 2024)</p>
                </div>
            </div>
    """
    
    for fig, title, desc in charts:
        chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
        html_content += f"""
            <div class="card">
                <h3>{title}</h3>
                <p>{desc}</p>
                {chart_html}
            </div>
        """
        
    html_content += """
            <div class="footer">
                <hr>
                <p>Dashboard generado automáticamente con Python + Plotly.</p>
                <p>Proyecto académico: Asia Central (2000–2021).</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    output_file = os.path.join(OUTPUT_DIR, "dashboard_asia_central.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✓ Dashboard generado con éxito en: {output_file}")

if __name__ == "__main__":
    generate_dashboard()
