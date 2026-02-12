"""
Visualizaciones profesionales para análisis de Asia Central (2000-2021)
Proyecto: Impacto de recursos naturales en economía y corrupción
Autor: Fernando Ramos
Fecha: 09/02/2026

Genera 5 gráficos interactivos (HTML) + versiones estáticas (PNG):
1. Scatter: Recursos vs Corrupción
2. Scatter: Recursos vs PIB
3. Serie Temporal: Evolución PIB por país
4. Barras: Eficiencia de recursos por país
5. Heatmap: Matriz de correlación
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Rutas (MISMA LÓGICA QUE PIPELINE.PY)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "datos")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "trabajo_final", "output")

# Crear carpeta de salida
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Paleta de colores consistente (optimizada para daltonismo)
COLORES_PAISES = {
    'Kazakhstan': '#1f77b4',  # Azul
    'Kyrgyzstan': '#ff7f0e',  # Naranja
    'Tajikistan': '#2ca02c',  # Verde
    'Turkmenistan': '#d62728',  # Rojo
    'Uzbekistan': '#9467bd'  # Púrpura
}

# Configuración visual
TEMPLATE = "plotly_white"
FONT_FAMILY = "Arial, sans-serif"
FONT_SIZE_TITLE = 16
FONT_SIZE_AXIS = 14
FONT_SIZE_TICK = 12


# ============================================================================
# FUNCIÓN AUXILIAR: CARGAR DATOS
# ============================================================================

def cargar_datos():
    """Carga datos procesados desde Parquet"""
    parquet_path = os.path.join(PROCESSED_DIR, "asia_central_processed")

    print("=" * 70)
    print("CARGANDO DATOS PROCESADOS")
    print("=" * 70)

    try:
        # Leer el archivo parquet
        df = pd.read_parquet(parquet_path)
        print(f"✅ Datos cargados: {len(df)} registros")
        print(f"   Países: {sorted(df['cname'].unique())}")
        print(f"   Período: {df['year'].min()}-{df['year'].max()}")
        return df
    except Exception as e:
        print(f"❌ ERROR al cargar datos: {e}")
        # Intentar leer desde CSV como fallback
        print("   Intentando leer desde CSV como fallback...")
        try:
            csv_folder = os.path.join(PROCESSED_DIR, "asia_central_processed_csv")
            csv_files = [f for f in os.listdir(csv_folder) if f.startswith('part-') and f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError("No se encontraron archivos 'part-*.csv' en la carpeta de salida de Spark.")
            csv_file_path = os.path.join(csv_folder, csv_files[0])
            df = pd.read_csv(csv_file_path)
            print(f"✅ Datos cargados desde CSV: {len(df)} registros")
            return df
        except Exception as csv_e:
            print(f"❌ ERROR al cargar datos desde CSV: {csv_e}")
            exit(1)


# ============================================================================
# GRÁFICO 1: SCATTER RECURSOS VS CORRUPCIÓN
# ============================================================================

def grafico_recursos_corrupcion(df):
    """
    Scatter plot: Recursos Naturales (% PIB) vs Control de Corrupción
    Objetivo: Evaluar hipótesis "maldición de recursos"
    """
    print("\n" + "=" * 70)
    print("GRÁFICO 1: Recursos vs Corrupción")
    print("=" * 70)

    # Calcular correlación
    corr = df['wdi_totalresrent'].corr(df['wbgi_cce'])

    # Crear figura
    fig = go.Figure()

    # Añadir puntos por país
    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais]

        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wbgi_cce'],
            mode='markers',
            name=pais,
            marker=dict(
                color=COLORES_PAISES[pais],
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

    # Línea de regresión
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df['wdi_totalresrent'],
        df['wbgi_cce']
    )
    x_reg = np.array([df['wdi_totalresrent'].min(), df['wdi_totalresrent'].max()])
    y_reg = slope * x_reg + intercept

    fig.add_trace(go.Scatter(
        x=x_reg,
        y=y_reg,
        mode='lines',
        name=f'Regresión (r={corr:.3f})',
        line=dict(color='black', width=2, dash='dash'),
        showlegend=True
    ))

    # Layout
    fig.update_layout(
        title={
            'text': 'Recursos Naturales vs Control de Corrupción<br>' +
                    '<sub>Asia Central 2000-2021 (103 observaciones)</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': FONT_SIZE_TITLE}
        },
        xaxis=dict(
            title=dict(text='Recursos Naturales (% PIB)', font={'size': FONT_SIZE_AXIS}),
            range=[0, df['wdi_totalresrent'].max() * 1.05],
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        yaxis=dict(
            title=dict(text='Control de Corrupción (Índice Banco Mundial)', font={'size': FONT_SIZE_AXIS}),
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=800,
        height=500,
        hovermode='closest',
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    # Anotación
    fig.add_annotation(
        x=0.98, y=0.02,
        xref='paper', yref='paper',
        text=f'<b>Correlación débil (r={corr:.3f})</b><br>No se confirma "maldición de recursos"',
        showarrow=False,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=11)
    )
    
    return fig, corr, p_value


# ============================================================================
# GRÁFICO 2: SCATTER RECURSOS VS PIB
# ============================================================================

def grafico_recursos_pib(df):
    """
    Scatter plot: Recursos Naturales vs PIB per cápita (escala logarítmica)
    Objetivo: Demostrar que recursos SÍ impulsan PIB
    """
    print("\n" + "=" * 70)
    print("GRÁFICO 2: Recursos vs PIB")
    print("=" * 70)

    # Calcular correlación
    corr = df['wdi_totalresrent'].corr(df['wdi_gdpcapcon2017'])

    # Crear figura
    fig = go.Figure()

    # Añadir puntos por país
    for pais in sorted(df['cname'].unique()):
        df_pais = df[df['cname'] == pais]

        fig.add_trace(go.Scatter(
            x=df_pais['wdi_totalresrent'],
            y=df_pais['wdi_gdpcapcon2017'],
            mode='markers',
            name=pais,
            marker=dict(
                color=COLORES_PAISES[pais],
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

    # Línea de regresión (en espacio lineal, se verá curva en log)
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df['wdi_totalresrent'],
        df['wdi_gdpcapcon2017']
    )
    x_reg = np.linspace(df['wdi_totalresrent'].min(), df['wdi_totalresrent'].max(), 100)
    y_reg = slope * x_reg + intercept

    fig.add_trace(go.Scatter(
        x=x_reg,
        y=y_reg,
        mode='lines',
        name=f'Regresión (r={corr:.3f})',
        line=dict(color='black', width=2, dash='dash'),
        showlegend=True
    ))

    # Layout con escala logarítmica en Y
    fig.update_layout(
        title={
            'text': 'Recursos Naturales vs PIB per cápita<br>' +
                    '<sub>Asia Central 2000-2021 (103 observaciones)</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': FONT_SIZE_TITLE}
        },
        xaxis=dict(
            title=dict(text='Recursos Naturales (% PIB)', font={'size': FONT_SIZE_AXIS}),
            range=[0, df['wdi_totalresrent'].max() * 1.05],
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        yaxis=dict(
            title=dict(text='PIB per cápita PPP (USD constantes 2017, escala logarítmica)',
                       font={'size': FONT_SIZE_AXIS}),
            type='log',
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=800,
        height=500,
        hovermode='closest',
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    # Anotación
    fig.add_annotation(
        x=0.98, y=0.02,
        xref='paper', yref='paper',
        text=f'<b>Correlación positiva fuerte (r={corr:.3f})</b><br>Recursos impulsan PIB',
        showarrow=False,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='gray',
        borderwidth=1,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=11)
    )
    
    return fig, corr, p_value


# ============================================================================
# GRÁFICO 3: SERIE TEMPORAL PIB
# ============================================================================

def grafico_serie_temporal_pib(df, countries_to_plot=None, title_suffix=""):
    """
    Serie temporal: Evolución del PIB per cápita por país (2000-2021)
    Objetivo: Mostrar divergencia económica en 20 años
    """
    print("\n" + "=" * 70)
    print(f"GRÁFICO 3: Serie Temporal PIB {title_suffix}")
    print("=" * 70)

    if countries_to_plot:
        df_plot = df[df['cname'].isin(countries_to_plot)]
    else:
        df_plot = df

    # Crear figura
    fig = go.Figure()

    # Añadir línea por país
    for pais in sorted(df_plot['cname'].unique()):
        df_pais = df_plot[df_plot['cname'] == pais].sort_values('year')

        # Calcular cambio porcentual año a año
        df_pais = df_pais.copy()
        df_pais['cambio_pct'] = df_pais['wdi_gdpcapcon2017'].pct_change() * 100

        fig.add_trace(go.Scatter(
            x=df_pais['year'],
            y=df_pais['wdi_gdpcapcon2017'],
            mode='lines+markers',
            name=pais,
            line=dict(color=COLORES_PAISES[pais], width=2.5),
            marker=dict(size=4, color=COLORES_PAISES[pais]),
            hovertemplate=(
                    f"<b>{pais}</b><br>" +
                    "Año: %{x}<br>" +
                    "PIB: $%{y:,.0f}<br>" +
                    "Cambio: %{customdata[0]:.1f}%<br>" +
                    "<extra></extra>"
            ),
            customdata=df_pais[['cambio_pct']].values
        ))

    # Línea vertical crisis 2008
    fig.add_vline(
        x=2008,
        line_dash="dash",
        line_color="gray",
        line_width=2,
        annotation_text="Crisis financiera 2008",
        annotation_position="top",
        annotation=dict(font_size=11, bgcolor="rgba(255,255,255,0.8)")
    )

    # Layout con escala logarítmica
    fig.update_layout(
        title={
            'text': f'Evolución del PIB per cápita por país {title_suffix}<br>' +
                    '<sub>Asia Central 2000-2021</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': FONT_SIZE_TITLE}
        },
        xaxis=dict(
            title=dict(text='Año', font={'size': FONT_SIZE_AXIS}),
            dtick=2,
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        yaxis=dict(
            title=dict(text='PIB per cápita PPP (USD constantes 2017, escala logarítmica)',
                       font={'size': FONT_SIZE_AXIS}),
            type='log',
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=800,
        height=500,
        hovermode='x unified',
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    # Nota al pie
    fig.add_annotation(
        x=0.02, y=0.02,
        xref='paper', yref='paper',
        text='*Turkmenistan: datos incompletos 2020-2021',
        showarrow=False,
        bgcolor='rgba(255,255,200,0.8)',
        bordercolor='orange',
        borderwidth=1,
        xanchor='left',
        yanchor='bottom',
        font=dict(size=10, color='black')
    )
    
    return fig


# ============================================================================
# GRÁFICO 4: BARRAS EFICIENCIA RECURSOS
# ============================================================================

def grafico_barras_eficiencia(df):
    """
    Gráfico de barras: Eficiencia de recursos por país (promedio 2000-2021)
    Objetivo: Mostrar que países sin recursos son más eficientes
    """
    print("\n" + "=" * 70)
    print("GRÁFICO 4: Eficiencia de Recursos")
    print("=" * 70)

    # Calcular promedios por país
    df_promedio = df.groupby('cname').agg({
        'eficiencia_recursos': 'mean',
        'wdi_totalresrent': 'mean'
    }).reset_index()

    # Ordenar por eficiencia descendente
    df_promedio = df_promedio.sort_values('eficiencia_recursos', ascending=False)

    # Asignar colores por país
    colores = [COLORES_PAISES[pais] for pais in df_promedio['cname']]

    # Crear figura
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_promedio['cname'],
        y=df_promedio['eficiencia_recursos'],
        marker=dict(
            color=colores,
            line=dict(color='white', width=1.5)
        ),
        text=df_promedio['eficiencia_recursos'].apply(lambda x: f'{x:,.0f}'),
        textposition='outside',
        textfont=dict(size=12),
        hovertemplate=(
                "<b>%{x}</b><br>" +
                "Eficiencia: %{y:,.0f}<br>" +
                "Recursos promedio: %{customdata[0]:.2f}%<br>" +
                "<extra></extra>"
        ),
        customdata=df_promedio[['wdi_totalresrent']].values,
        showlegend=False
    ))

    # Layout con escala logarítmica
    fig.update_layout(
        title={
            'text': 'Eficiencia de Recursos por País<br>' +
                    '<sub>PIB generado por cada % de recursos naturales (promedio 2000-2021)</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': FONT_SIZE_TITLE}
        },
        xaxis=dict(
            title=dict(text='País', font={'size': FONT_SIZE_AXIS}),
            tickfont={'size': FONT_SIZE_TICK}
        ),
        yaxis=dict(
            title=dict(text='Eficiencia (PIB / % Recursos, escala logarítmica)', font={'size': FONT_SIZE_AXIS}),
            type='log',
            gridcolor='lightgray',
            tickfont={'size': FONT_SIZE_TICK}
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=700,
        height=500
    )

    # Nota al pie
    fig.add_annotation(
        x=0.5, y=-0.15,
        xref='paper', yref='paper',
        text='<b>Escala logarítmica:</b> Kyrgyzstan es ~30× más eficiente que Turkmenistan (economía diversificada vs Estado rentista)',
        showarrow=False,
        xanchor='center',
        font=dict(size=11)
    )
    
    return fig


# ============================================================================
# GRÁFICO 5: HEATMAP CORRELACIÓN
# ============================================================================

def grafico_heatmap_correlacion(df, variables_to_plot=None, title_suffix=""):
    """
    Heatmap: Matriz de correlación entre variables clave
    Objetivo: Visualizar todas las relaciones simultáneamente
    """
    print("\n" + "=" * 70)
    print(f"GRÁFICO 5: Matriz de Correlación {title_suffix}")
    print("=" * 70)

    # Variables para correlación
    if variables_to_plot:
        columnas = variables_to_plot
    else:
        columnas = [
            'wdi_totalresrent',
            'wdi_gdpcapcon2017',
            'wbgi_cce',
            'undp_hdi',
            'brecha_corrupcion_riqueza',
            'eficiencia_recursos',
            'indice_bienestar_redistributivo'
        ]

    # Nombres descriptivos cortos
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


    # Eliminar filas con nulos en las columnas seleccionadas antes de calcular correlación
    df_clean = df[columnas].dropna()

    # Calcular matriz de correlación
    corr_matrix = df_clean.corr()

    # Enmascarar diagonal (valores 1.0)
    mask = np.eye(len(corr_matrix), dtype=bool)
    corr_display = corr_matrix.copy()
    corr_display[mask] = np.nan

    # Crear heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_display.values,
        x=nombres_desc,
        y=nombres_desc,
        colorscale=[
            [0, '#2166ac'],  # Azul oscuro (-1)
            [0.5, '#f7f7f7'],  # Blanco (0)
            [1, '#b2182b']  # Rojo oscuro (+1)
        ],
        zmid=0,
        zmin=-1,
        zmax=1,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont=dict(size=11),
        hovertemplate=(
                '<b>%{y} vs %{x}</b><br>' +
                'Correlación: %{z:.3f}<br>' +
                '<extra></extra>'
        ),
        colorbar=dict(
            title=dict(text='Correlación', side='right'),  # ← CORREGIDO
            tickmode='linear',
            tick0=-1,
            dtick=0.5
        )
    ))

    # Layout
    fig.update_layout(
        title={
            'text': f'Matriz de Correlación - Variables Clave {title_suffix}<br>' +
                    f'<sub>Asia Central 2000-2021 (n={len(df_clean)})</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': FONT_SIZE_TITLE}
        },
        xaxis=dict(
            tickangle=-45,
            tickfont={'size': 11},
            side='bottom'
        ),
        yaxis=dict(
            tickfont={'size': 11},
            autorange='reversed'
        ),
        template=TEMPLATE,
        font=dict(family=FONT_FAMILY),
        width=700,
        height=700,
        margin=dict(l=150, r=100, t=100, b=150)
    )
    
    return fig, corr_matrix


# ============================================================================
# MAIN: GENERAR TODOS LOS GRÁFICOS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("GENERADOR DE VISUALIZACIONES - ASIA CENTRAL")
    print("=" * 70)

    # Cargar datos
    df = cargar_datos()

    # Generar y guardar gráficos
    fig1, _, _ = grafico_recursos_corrupcion(df)
    fig1.write_html(os.path.join(OUTPUT_DIR, "01_recursos_corrupcion.html"))

    fig2, _, _ = grafico_recursos_pib(df)
    fig2.write_html(os.path.join(OUTPUT_DIR, "02_recursos_pib.html"))

    fig3 = grafico_serie_temporal_pib(df)
    fig3.write_html(os.path.join(OUTPUT_DIR, "03_serie_temporal_pib.html"))

    fig4 = grafico_barras_eficiencia(df)
    fig4.write_html(os.path.join(OUTPUT_DIR, "04_barras_eficiencia.html"))

    fig5, _ = grafico_heatmap_correlacion(df)
    fig5.write_html(os.path.join(OUTPUT_DIR, "05_heatmap_correlacion.html"))

    # Resumen final
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    print(f"\n📁 Archivos generados en: {OUTPUT_DIR}")
    print("\nGráficos interactivos (HTML):")
    print("  1. 01_recursos_corrupcion.html")
    print("  2. 02_recursos_pib.html")
    print("  3. 03_serie_temporal_pib.html")
    print("  4. 04_barras_eficiencia.html")
    print("  5. 05_heatmap_correlacion.html")
    print("\n💡 Abre los HTML en tu navegador para interactividad completa")
    print("   (hover, zoom, click en leyenda para ocultar/mostrar países)")
    print("\n⚠️  Si los PNG no se guardaron, instala: pip install kaleido")
