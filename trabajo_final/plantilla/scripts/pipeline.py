"""
Pipeline ETL para análisis de Asia Central (2000-2023)
Proyecto: Impacto de recursos naturales en economía y corrupción
Autor: Fernando Ramos
Fecha: 06/02/2026
"""

import os
import sys
import shutil

# ============================================================================
# CONFIGURACIÓN DE HADOOP EN WINDOWS (SOLUCIÓN A HADOOP_HOME)
# ============================================================================
# Asegurarse de que HADOOP_HOME y winutils.exe estén configurados
# antes de importar pyspark
if sys.platform.startswith('win'):
    hadoop_home = 'C:\\hadoop'
    if 'HADOOP_HOME' not in os.environ:
        os.environ['HADOOP_HOME'] = hadoop_home
    if hadoop_home not in os.environ['PATH']:
        os.environ['PATH'] += f";{os.path.join(hadoop_home, 'bin')}"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, avg, expr, min as spark_min, max as spark_max
from pyspark.sql.window import Window

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

DATA_DIR = os.path.join(PROJECT_ROOT, "datos")
EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, "external")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

CSV_PATH = os.path.join(EXTERNAL_DATA_DIR, "qog_std_ts_jan24.csv")
OUTPUT_PATH = PROCESSED_DATA_DIR

# Asegurar que el directorio de salida existe
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ============================================================================
# PASO 1: INICIALIZAR SPARKSESSION
# ============================================================================
print("\n" + "="*70)
print("INICIANDO PIPELINE ETL - ASIA CENTRAL 2000-2023")
print("="*70)

spark = SparkSession.builder \
    .appName("AsiaCentral_ETL_Pipeline") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

print(f"\n✓ SparkSession iniciada: {spark.sparkContext.appName}")

# ============================================================================
# PASO 2: LECTURA DEL CSV COMPLETO
# ============================================================================
print("\n" + "="*70)
print("PASO 2: LECTURA DE DATOS")
print("="*70)

try:
    # Leemos todo como STRING primero para evitar errores de parseo con "NA"
    df_raw = spark.read \
        .option("header", "true") \
        .option("inferSchema", "false") \
        .option("encoding", "utf-8") \
        .csv(CSV_PATH)

    print(f"\n✓ CSV leído correctamente")
    print(f"  - Total de filas: {df_raw.count():,}")
    print(f"  - Total de columnas: {len(df_raw.columns)}")

except Exception as e:
    print(f"\n❌ ERROR al leer el archivo CSV en: {CSV_PATH}")
    print(f"Detalle: {str(e)}")
    sys.exit(1)

# ============================================================================
# PASO 3: FILTRADO POR PAÍSES Y AÑOS
# ============================================================================
print("\n" + "="*70)
print("PASO 3: FILTRADO DE PAÍSES Y PERÍODO 2000-2023")
print("="*70)

PAISES_ASIA_CENTRAL = ['Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan', 'Uzbekistan']

# Filtramos primero por país y año (que suelen estar limpios) para reducir datos
# Nota: year se lee como string, así que casteamos para filtrar
df_filtered = df_raw.filter(
    (col('cname').isin(PAISES_ASIA_CENTRAL)) &
    (col('year').cast("int") >= 2000) &
    (col('year').cast("int") <= 2023)
)

print(f"\n✓ Filtrado aplicado")
print(f"  - Registros resultantes: {df_filtered.count()}")

# ============================================================================
# PASO 4: SELECCIÓN, LIMPIEZA Y RENOMBRADO DE COLUMNAS
# ============================================================================
print("\n" + "="*70)
print("PASO 4: SELECCIÓN Y RENOMBRADO DE VARIABLES")
print("="*70)

# Mapeo de columnas: Nombre Nuevo -> Nombre Original en CSV
column_mapping = {
    'cname': 'cname',
    'year': 'year',
    'wdi_totalresrent': 'wdi_oilrent',          # Renta petrolera (% PIB)
    'wdi_gdpcapcon2017': 'wdi_gdpcappppcon2017', # PIB per cápita PPA (cte 2017)
    'wbgi_cce': 'wbgi_cce',                     # Control de corrupción
    'undp_hdi': 'undp_hdi',                     # IDH
    'wdi_lifexp': 'wdi_lifexp'                  # Esperanza de vida
}

# Función auxiliar para limpiar y castear
def clean_and_cast(col_name, target_type="double"):
    # Reemplaza "NA", ".." y vacíos por NULL, luego castea
    c = col(col_name)
    return when((c == "NA") | (c == "..") | (c == ""), None).otherwise(c).cast(target_type)

select_exprs = []
for new_col, orig_col in column_mapping.items():
    if new_col == 'cname':
        select_exprs.append(col(orig_col).alias(new_col))
    elif new_col == 'year':
        select_exprs.append(clean_and_cast(orig_col, "int").alias(new_col))
    else:
        select_exprs.append(clean_and_cast(orig_col, "double").alias(new_col))

df_selected = df_filtered.select(*select_exprs)

print("\n✓ Columnas seleccionadas, limpiadas y casteadas:")
df_selected.printSchema()

# ============================================================================
# PASO 5: LIMPIEZA DE NULOS (Imputación simple o eliminación)
# ============================================================================
# Para evitar errores en cálculos matemáticos, eliminamos filas con nulos en variables clave
df_clean = df_selected.dropna(subset=['wdi_gdpcapcon2017', 'wbgi_cce', 'wdi_totalresrent'])
print(f"\n✓ Registros tras eliminar nulos en variables clave: {df_clean.count()}")

# ============================================================================
# PASO 6: CÁLCULO DE VARIABLES DERIVADAS
# ============================================================================
print("\n" + "="*70)
print("PASO 6: CÁLCULO DE VARIABLES DERIVADAS")
print("="*70)

# 1. Brecha Corrupción-Riqueza: PIB / (Corrupción + 3)
df_derived = df_clean.withColumn(
    "brecha_corrupcion_riqueza",
    col("wdi_gdpcapcon2017") / (col("wbgi_cce") + 3)
)

# 2. Eficiencia de Recursos: PIB / Recursos Naturales
df_derived = df_derived.withColumn(
    "eficiencia_recursos",
    when(col("wdi_totalresrent") > 0, col("wdi_gdpcapcon2017") / col("wdi_totalresrent"))
    .otherwise(0)
)

# 3. Índice de Bienestar Redistributivo: (PIB_norm + Corrupción_norm) / 2
stats_row = df_derived.agg(
    spark_min("wdi_gdpcapcon2017").alias("min_pib"),
    spark_max("wdi_gdpcapcon2017").alias("max_pib"),
    spark_min("wbgi_cce").alias("min_corr"),
    spark_max("wbgi_cce").alias("max_corr")
).collect()

if stats_row:
    stats = stats_row[0]
    min_pib = stats["min_pib"]
    max_pib = stats["max_pib"]
    min_corr = stats["min_corr"]
    max_corr = stats["max_corr"]

    df_derived = df_derived.withColumn(
        "pib_norm",
        (col("wdi_gdpcapcon2017") - min_pib) / (max_pib - min_pib)
    ).withColumn(
        "corr_norm",
        (col("wbgi_cce") - min_corr) / (max_corr - min_corr)
    )

    df_final = df_derived.withColumn(
        "indice_bienestar_redistributivo",
        (col("pib_norm") + col("corr_norm")) / 2
    ).drop("pib_norm", "corr_norm")
else:
    print("⚠️ No se pudieron calcular estadísticas para normalización")
    df_final = df_derived

print("\n✓ Variables derivadas calculadas:")
df_final.select("cname", "year", "brecha_corrupcion_riqueza", "eficiencia_recursos", "indice_bienestar_redistributivo").show(5)

# ============================================================================
# PASO 7: GUARDADO DE DATOS
# ============================================================================
print("\n" + "="*70)
print("PASO 7: GUARDADO DE RESULTADOS")
print("="*70)

# Definir función de log (si no existe)
def log_step(step, msg):
    print(f"\n[PASO {step}] {msg}")

log_step(7, "Guardar datos limpios en Parquet")

# FORZAR LIMPIEZA ANTES DE ESCRIBIR
output_file = os.path.join(OUTPUT_PATH, "asia_central_processed")

if os.path.exists(output_file):
    try:
        shutil.rmtree(output_file)
        print(f"✓ Carpeta anterior eliminada: {output_file}")
    except Exception as e:
        print(f"⚠️ No se pudo eliminar la carpeta anterior: {e}")

print(f"Guardando en: {output_file}")

df_final.write.mode("overwrite").parquet(output_file)
df_final.write.mode("overwrite").option("header", "true").csv(output_file + "_csv")

print("\n✓ Proceso finalizado con éxito.")

spark.stop()
