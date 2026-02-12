import pandas as pd
from fpdf import FPDF
import os
import sys

# Añadir el directorio actual al path para poder importar visualizaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar funciones de visualización
from visualizaciones import (
    cargar_datos,
    grafico_recursos_pib,
    grafico_serie_temporal_pib,
    grafico_barras_eficiencia,
    grafico_heatmap_correlacion
)

# --- 1. CONFIGURACIÓN DE RUTAS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "trabajo_final", "plantilla", "informes")
IMAGE_DIR = os.path.join(OUTPUT_DIR, "imagenes_dashboard")

# Crear carpetas si no existen
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# --- 2. CARGAR DATOS Y GENERAR GRÁFICOS ---
print("Cargando datos y generando gráficos para el dashboard...")
df = cargar_datos()

# --- CÁLCULOS PARA MÉTRICAS ---
df_last_year = df[df['year'] == df['year'].max()]
pib_kaz = df_last_year[df_last_year['cname'] == 'Kazakhstan']['wdi_gdpcapcon2017'].iloc[0]
pib_taj = df_last_year[df_last_year['cname'] == 'Tajikistan']['wdi_gdpcapcon2017'].iloc[0]
divergencia_pib = pib_kaz / pib_taj if pib_taj != 0 else 0

# --- GENERACIÓN DE GRÁFICOS PERSONALIZADOS ---
# Gráfico principal: Scatter Recursos vs PIB
fig_main_scatter, corr_rp, _ = grafico_recursos_pib(df)
path_main_scatter = os.path.join(IMAGE_DIR, "main_scatter_recursos_pib.png")
fig_main_scatter.write_image(path_main_scatter, width=1000, height=600, scale=2)

# Mini-gráfico complementario: Serie temporal PIB simplificada
paises_representativos = ['Kazakhstan', 'Uzbekistan', 'Tajikistan']
fig_mini_ts = grafico_serie_temporal_pib(df, countries_to_plot=paises_representativos, title_suffix="(Selección)")
path_mini_ts = os.path.join(IMAGE_DIR, "mini_ts_pib.png")
fig_mini_ts.write_image(path_mini_ts, width=800, height=450, scale=2)

# Heatmap de correlación (reducido)
variables_heatmap = ['wdi_totalresrent', 'wdi_gdpcapcon2017', 'wbgi_cce', 'undp_hdi']
fig_heatmap, _ = grafico_heatmap_correlacion(df, variables_to_plot=variables_heatmap, title_suffix="(Reducido)")
path_heatmap = os.path.join(IMAGE_DIR, "heatmap_reducido.png")
fig_heatmap.write_image(path_heatmap, width=600, height=600, scale=2)

# Gráfico de barras eficiencia
fig_barras_eficiencia = grafico_barras_eficiencia(df)
path_barras_eficiencia = os.path.join(IMAGE_DIR, "barras_eficiencia.png")
fig_barras_eficiencia.write_image(path_barras_eficiencia, width=800, height=500, scale=2)

print("✓ Gráficos generados y guardados como PNG para el dashboard.")

# --- 3. CREAR EL INFORME PDF CON LAYOUT PROFESIONAL ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Dashboard de Análisis: Recursos y Desarrollo en Asia Central', 0, 1, 'L')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Usar formato horizontal (apaisado) para el dashboard
pdf = PDF(orientation='L', unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)
pdf.add_page()

# --- ZONA SUPERIOR (33%) ---
pdf.set_y(15)
pdf.set_font('Arial', 'B', 24)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 10, 'Recursos, Crecimiento y Corrupción en Asia Central', 0, 1, 'C')
pdf.set_font('Arial', '', 14)
pdf.cell(0, 10, 'Análisis del período 2000-2021', 0, 1, 'C')
pdf.ln(8)

# Métrica secundaria
pdf.set_font('Arial', 'B', 16)
pdf.set_text_color(214, 39, 40) # Rojo
pdf.cell(0, 10, f"Divergencia Económica 2021: Kazajistán es {divergencia_pib:.1f}x más rico que Tayikistán", 0, 1, 'C')
pdf.set_text_color(0, 0, 0)
pdf.line(10, pdf.get_y() + 5, 287, pdf.get_y() + 5) # Línea separadora
pdf.ln(10)


# --- ZONA MEDIA (40%) ---
# Coordenadas y dimensiones
y_middle = pdf.get_y()
main_scatter_width = 160 # 60% del ancho útil (277mm)
mini_ts_width = 110 # 40%
x_start = 10
x_middle = x_start + main_scatter_width + 5

pdf.image(path_main_scatter, x=x_start, y=y_middle, w=main_scatter_width)
pdf.image(path_mini_ts, x=x_middle, y=y_middle, w=mini_ts_width)
pdf.ln(75) # Espacio para los gráficos

# --- ZONA INFERIOR (27%) ---
y_bottom = pdf.get_y()
heatmap_width = 130 # 50%
barras_width = 130 # 50%
x_start_bottom = 15
x_middle_bottom = x_start_bottom + heatmap_width + 5

pdf.image(path_heatmap, x=x_start_bottom, y=y_bottom, w=heatmap_width)
pdf.image(path_barras_eficiencia, x=x_middle_bottom, y=y_bottom, w=barras_width)

# --- FINALIZAR ---
pdf_output_path = os.path.join(OUTPUT_DIR, "Dashboard_Profesional_AsiaCentral.pdf")
pdf.output(pdf_output_path)

print(f"\n✓ Dashboard PDF profesional generado con éxito en: {pdf_output_path}")
print(f"   Ruta: {pdf_output_path}")
