"""
DASHBOARD PROFESIONAL - ASIA CENTRAL (2000-2021)
Proyecto: Impacto de recursos naturales en economía y corrupción
Autor: Fernando Ramos
Fecha: 09/02/2026

Genera 5 gráficos interactivos (Plotly) y crea un único dashboard final en HTML:
dashboard_asia_central.html

Orden profesional:
1. Serie temporal PIB per cápita
2. Recursos vs PIB
3. Recursos vs Corrupción
4. Eficiencia de recursos por país
5. Heatmap correlaciones
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from scipy import stats


# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "datos")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "trabajo_final", "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORES_PAISES = {
    'Kazakhstan': '#1f77b4',
    'Kyrgyzstan': '#ff7f0e',
    'Tajikistan': '#2ca02c',
    'Turkmenistan': '#d62728',
    'Uzbekistan': '#9467bd'
}

TEMPLATE = "plotly_white"
FONT_FAMILY = "Arial, sans-serif"
FONT_SIZE_TITLE = 16
FONT_SIZE_AXIS = 14
FONT_SIZE_TICK = 12


# ============================================================================
# CARGA DE DATOS
# ============================================================================

def cargar_datos():
    """Carga datos procesados desde Parquet. Si falla, intenta CSV."""
    parquet_path = os.path.join(PROCESSED_DIR, "asia_central_processed")

    print("=" * 70)
    print("CARGANDO DATOS PROCESADOS")
    print("=" * 70)

    try:
        df = pd.read_parquet(parquet_path)
        print(f"✅ Datos cargados: {len(df)} registros")
        print(f"   Países: {sorted(df['cname'].unique())}")
        print(f"   Período: {df['year'].min()}-{df['year'].max()}")
        return df

    except Exception as e:
        print(f"❌ ERROR al cargar Parquet: {e}")
        print("   Intentando cargar desde CSV como fallback...")

        try:
            csv_folder = os.path.join(PROCESSED_DIR, "asia_central_processed_csv")
            csv_files = [f for f in os.listdir(csv_folder) if f.startswith("part-") and f.endswith(".csv")]

            if not csv_files:
                raise FileNotFoundError("No se encontraron archivos part-*.csv en la carpeta de Spark.")

            csv_file_path = os.path.join(csv_folder, csv_files[0])
            df = pd.read_csv(csv_file_path)

            print(f"✅ Datos cargados desde CSV: {len(df)} registros")
            return df

        except Exception as csv_e:
            print(f"❌ ERROR al cargar CSV: {csv_e}")
            raise


# ============================================================================
# GRÁFICO 1: RECURSOS VS CORRUPCIÓN
# ============================================================================

def grafico_recursos_corrupcion(df):
    corr = df['wdi_totalresrent'].corr(df['wbgi_cce'])

    fig = go.Figure()

    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais]

        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wbgi_cce'],
            mode='markers',
            name=pais,
            marker=dict(
                color=COLORES_PAISES.get(pais, "gray"),
                size=10,
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate=(
                f"<b>{pais}</b><br>" +
                "Año: %{customdata[0]}<br>" +
                "Recursos: %{x:.2f}%<br>" +
                "Corrupción: %{y:.3f}<br>" +
                "<extra></extra>"
            ),
            customdata=df_pais[['year']].values
        ))

    slope, intercept, _, p_value, _ = stats.linregress(df['wdi_totalresrent'], df['wbgi_cce'])
    x_reg = np.array([df['wdi_totalresrent'].min(), df['wdi_totalresrent'].max()])
    y_reg = slope * x_reg + intercept

    fig.add_trace(go.Scatter(
        x=x_reg,
        y=y_reg,
        mode='lines',
        name=f'Regresión (r={corr:.3f})',
        line=dict(color='black', width=2, dash='dash')
    ))

    fig.update_layout(
        title={
            'text': 'Recursos Naturales vs Control de Corrupción<br><sub>Asia Central 2000-2021</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title='Recursos Naturales (% PIB)',
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        yaxis=dict(
            title='Control de Corrupción (Banco Mundial)',
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=900,
        height=500
    )

    fig.add_annotation(
        x=0.98, y=0.02,
        xref='paper', yref='paper',
        text=f'<b>Correlación débil (r={corr:.3f})</b>',
        showarrow=False,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1,
        xanchor='right',
        yanchor='bottom'
    )

    return fig, corr, p_value


# ============================================================================
# GRÁFICO 2: RECURSOS VS PIB
# ============================================================================

def grafico_recursos_pib(df):
    corr = df['wdi_totalresrent'].corr(df['wdi_gdpcapcon2017'])

    fig = go.Figure()

    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais]

        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wdi_gdpcapcon2017'],
            mode='markers',
            name=pais,
            marker=dict(
                color=COLORES_PAISES.get(pais, "gray"),
                size=10,
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            hovertemplate=(
                f"<b>{pais}</b><br>" +
                "Año: %{customdata[0]}<br>" +
                "Recursos: %{x:.2f}%<br>" +
                "PIB: $%{y:,.0f}<br>" +
                "<extra></extra>"
            ),
            customdata=df_pais[['year']].values
        ))

    slope, intercept, _, p_value, _ = stats.linregress(df['wdi_totalresrent'], df['wdi_gdpcapcon2017'])
    x_reg = np.linspace(df['wdi_totalresrent'].min(), df['wdi_totalresrent'].max(), 100)
    y_reg = slope * x_reg + intercept

    fig.add_trace(go.Scatter(
        x=x_reg,
        y=y_reg,
        mode='lines',
        name=f'Regresión (r={corr:.3f})',
        line=dict(color='black', width=2, dash='dash')
    ))

    fig.update_layout(
        title={
            'text': 'Recursos Naturales vs PIB per cápita<br><sub>Asia Central 2000-2021</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            title='Recursos Naturales (% PIB)',
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        yaxis=dict(
            title='PIB per cápita PPP (USD constantes 2017, escala log)',
            type='log',
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=900,
        height=500
    )

    fig.add_annotation(
        x=0.98, y=0.02,
        xref='paper', yref='paper',
        text=f'<b>Correlación positiva fuerte (r={corr:.3f})</b>',
        showarrow=False,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1,
        xanchor='right',
        yanchor='bottom'
    )

    return fig, corr, p_value


# ============================================================================
# GRÁFICO 3: SERIE TEMPORAL PIB
# ============================================================================

def grafico_serie_temporal_pib(df):
    fig = go.Figure()

    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais].sort_values('year').copy()
        df_pais['cambio_pct'] = df_pais['wdi_gdpcapcon2017'].pct_change() * 100

        fig.add_trace(go.Scatter(
            x=df_pais['year'],
            y=df_pais['wdi_gdpcapcon2017'],
            mode='lines+markers',
            name=pais,
            line=dict(color=COLORES_PAISES.get(pais, "gray"), width=2.5),
            marker=dict(size=4),
            hovertemplate=(
                f"<b>{pais}</b><br>" +
                "Año: %{x}<br>" +
                "PIB: $%{y:,.0f}<br>" +
                "Cambio: %{customdata[0]:.1f}%<br>" +
                "<extra></extra>"
            ),
            customdata=df_pais[['cambio_pct']].values
        ))

    fig.add_vline(
        x=2008,
        line_dash="dash",
        line_color="gray",
        line_width=2,
        annotation_text="Crisis financiera 2008",
        annotation_position="top"
    )

    fig.update_layout(
        title={
            'text': 'Evolución del PIB per cápita por país<br><sub>Asia Central 2000-2021</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(title='Año', dtick=2, gridcolor='lightgray'),
        yaxis=dict(
            title='PIB per cápita PPP (USD constantes 2017, escala log)',
            type='log',
            gridcolor='lightgray'
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=900,
        height=500,
        hovermode='x unified'
    )

    return fig


# ============================================================================
# GRÁFICO 4: EFICIENCIA DE RECURSOS
# ============================================================================

def grafico_barras_eficiencia(df):
    df_prom = df.groupby('cname').agg({
        'eficiencia_recursos': 'mean',
        'wdi_totalresrent': 'mean'
    }).reset_index()

    df_prom = df_prom.sort_values('eficiencia_recursos', ascending=False)
    colores = [COLORES_PAISES.get(p, "gray") for p in df_prom['cname']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_prom['cname'],
        y=df_prom['eficiencia_recursos'],
        marker=dict(color=colores, line=dict(color='white', width=1.5)),
        text=df_prom['eficiencia_recursos'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside',
        hovertemplate=(
            "<b>%{x}</b><br>" +
            "Eficiencia: %{y:,.0f}<br>" +
            "Recursos promedio: %{customdata[0]:.2f}%<br>" +
            "<extra></extra>"
        ),
        customdata=df_prom[['wdi_totalresrent']].values
    ))

    fig.update_layout(
        title={
            'text': 'Eficiencia de Recursos por País<br><sub>Promedio 2000-2021</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(title='País'),
        yaxis=dict(title='Eficiencia (PIB / % Recursos, escala log)', type='log', gridcolor='lightgray'),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=900,
        height=500
    )

    return fig


# ============================================================================
# GRÁFICO 5: HEATMAP CORRELACIÓN
# ============================================================================

def grafico_heatmap_correlacion(df):
    columnas = [
        'wdi_totalresrent',
        'wdi_gdpcapcon2017',
        'wbgi_cce',
        'undp_hdi',
        'brecha_corrupcion_riqueza',
        'eficiencia_recursos',
        'indice_bienestar_redistributivo'
    ]

    nombres_desc_map = {
        'wdi_totalresrent': 'Recursos (%PIB)',
        'wdi_gdpcapcon2017': 'PIB per cápita',
        'wbgi_cce': 'Control corrupción',
        'undp_hdi': 'Desarrollo Humano',
        'brecha_corrupcion_riqueza': 'Brecha Gob-Riqueza',
        'eficiencia_recursos': 'Eficiencia Recursos',
        'indice_bienestar_redistributivo': 'Bienestar Compuesto'
    }

    nombres_desc = [nombres_desc_map.get(col, col) for col in columnas]

    df_clean = df[columnas].dropna()
    corr_matrix = df_clean.corr()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=nombres_desc,
        y=nombres_desc,
        colorscale="RdBu",
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate="%{text}",
        hovertemplate="<b>%{y} vs %{x}</b><br>Correlación: %{z:.3f}<extra></extra>"
    ))

    fig.update_layout(
        title={
            'text': f'Matriz de Correlación - Variables Clave<br><sub>Asia Central 2000-2021 (n={len(df_clean)})</sub>',
            'x': 0.5,
            'xanchor': 'center'
        },
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=900,
        height=700
    )

    return fig, corr_matrix


# ============================================================================
# EXPORTADOR DASHBOARD ÚNICO
# ============================================================================

def exportar_dashboard_unico(figs, output_path):

    html_parts = []
    for i, fig in enumerate(figs):
        if i == 0:
            html_parts.append(pio.to_html(fig, full_html=False, include_plotlyjs="cdn"))
        else:
            html_parts.append(pio.to_html(fig, full_html=False, include_plotlyjs=False))

    html_final = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Dashboard Asia Central (2000–2021)</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: #f4f6f9;
                color: #1f2937;
            }}

            .container {{
                width: 90%;
                max-width: 1200px;
                margin: auto;
                padding: 40px 0;
            }}

            .header {{
                background: #111827;
                color: white;
                padding: 60px 40px;
                border-radius: 18px;
                box-shadow: 0px 10px 25px rgba(0,0,0,0.25);
            }}

            .header h1 {{
                font-size: 36px;
                margin: 0;
                font-weight: 700;
            }}

            .header h2 {{
                font-size: 18px;
                margin-top: 12px;
                font-weight: 400;
                opacity: 0.9;
            }}

            .meta {{
                margin-top: 25px;
                font-size: 14px;
                opacity: 0.85;
            }}

            .card {{
                background: white;
                padding: 25px;
                border-radius: 16px;
                box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
                margin-top: 25px;
            }}

            .card h3 {{
                font-size: 18px;
                margin-top: 0;
                margin-bottom: 10px;
            }}

            .card p {{
                font-size: 14px;
                margin-bottom: 20px;
                color: #374151;
            }}

            .footer {{
                margin-top: 80px;
                padding: 30px;
                font-size: 13px;
                text-align: center;
                color: #6b7280;
            }}

            hr {{
                border: none;
                border-top: 1px solid #e5e7eb;
                margin: 25px 0;
            }}

            .badge {{
                display: inline-block;
                padding: 6px 12px;
                border-radius: 999px;
                background: #2563eb;
                color: white;
                font-size: 12px;
                font-weight: 600;
            }}
        </style>
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

            <div class="card">
                <h3>Figura 1. Evolución del PIB per cápita por país (2000–2021)</h3>
                <p>Serie temporal para observar divergencia económica y el impacto de la crisis de 2008.</p>
                {html_parts[0]}
            </div>

            <div class="card">
                <h3>Figura 2. Recursos Naturales vs PIB per cápita</h3>
                <p>Relación entre renta extractiva (% PIB) y desempeño económico (PIB per cápita).</p>
                {html_parts[1]}
            </div>

            <div class="card">
                <h3>Figura 3. Recursos Naturales vs Control de Corrupción</h3>
                <p>Relación entre dependencia de recursos y calidad institucional (control de corrupción).</p>
                {html_parts[2]}
            </div>

            <div class="card">
                <h3>Figura 4. Eficiencia de Recursos por País (promedio 2000–2021)</h3>
                <p>Comparación de la capacidad de convertir recursos en crecimiento económico.</p>
                {html_parts[3]}
            </div>

            <div class="card">
                <h3>Figura 5. Matriz de Correlación (Variables Clave)</h3>
                <p>Mapa global de relaciones entre variables económicas, sociales e institucionales.</p>
                {html_parts[4]}
            </div>

            <div class="footer">
                <hr>
                <p>Dashboard generado automáticamente con Python + Plotly.</p>
                <p>Proyecto académico: Asia Central (2000–2021).</p>
            </div>

        </div>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"✅ Dashboard único generado: {output_path}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("GENERADOR DASHBOARD - ASIA CENTRAL")
    print("=" * 70)

    df = cargar_datos()

    # Crear figuras
    fig_corrupcion, _, _ = grafico_recursos_corrupcion(df)
    fig_pib, _, _ = grafico_recursos_pib(df)
    fig_serie = grafico_serie_temporal_pib(df)
    fig_eficiencia = grafico_barras_eficiencia(df)
    fig_heatmap, _ = grafico_heatmap_correlacion(df)

    # Guardar dashboard único (orden profesional)
    dashboard_path = os.path.join(OUTPUT_DIR, "dashboard_asia_central.html")

    exportar_dashboard_unico(
        figs=[
            fig_serie,
            fig_pib,
            fig_corrupcion,
            fig_eficiencia,
            fig_heatmap
        ],
        output_path=dashboard_path
    )

    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    print(f"\n📁 Dashboard final generado en: {dashboard_path}")
    print("💡 Ábrelo con Chrome o Edge para máxima compatibilidad.")
