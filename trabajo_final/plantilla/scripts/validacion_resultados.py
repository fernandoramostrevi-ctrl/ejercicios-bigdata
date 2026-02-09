# validar_resultados.py
import pandas as pd
import os

# Rutas
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "datos", "processed")

print("="*70)
print("VALIDACIÓN DE RESULTADOS DEL PIPELINE")
print("="*70)

# 1. CARGAR DATOS PROCESADOS
print("\n1. Cargando datos desde Parquet...")
parquet_path = os.path.join(PROCESSED_DIR, "asia_central_processed")

try:
    df = pd.read_parquet(parquet_path)
    print(f"✅ Datos cargados: {len(df)} registros, {len(df.columns)} columnas")
except Exception as e:
    print(f"❌ Error al cargar: {e}")
    exit()

# 2. RESUMEN GENERAL
print("\n" + "="*70)
print("2. RESUMEN GENERAL")
print("="*70)
print(f"\nPaíses: {sorted(df['cname'].unique())}")
print(f"Período: {df['year'].min()} - {df['year'].max()}")
print(f"Total años: {df['year'].nunique()}")

print("\nRegistros por país:")
print(df['cname'].value_counts().sort_index())

# 3. ESTADÍSTICAS DESCRIPTIVAS
print("\n" + "="*70)
print("3. ESTADÍSTICAS DESCRIPTIVAS")
print("="*70)
print(df.describe().round(2))

# 4. VERIFICAR NULOS
print("\n" + "="*70)
print("4. VERIFICACIÓN DE NULOS")
print("="*70)
nulos = df.isnull().sum()
if nulos.sum() > 0:
    print("\n⚠️ Columnas con nulos:")
    print(nulos[nulos > 0])
else:
    print("✅ No hay nulos en el dataset")

# 5. MATRIZ DE CORRELACIÓN
print("\n" + "="*70)
print("5. MATRIZ DE CORRELACIÓN (VARIABLES CLAVE)")
print("="*70)

cols_corr = [
    'wdi_totalresrent',
    'wdi_gdpcapcon2017',
    'wbgi_cce',
    'undp_hdi',
    'brecha_corrupcion_riqueza',
    'eficiencia_recursos',
    'indice_bienestar_redistributivo'
]

corr_matrix = df[cols_corr].corr()
print("\n" + corr_matrix.round(3).to_string())

# Guardar matriz
corr_output = os.path.join(PROCESSED_DIR, "matriz_correlacion.csv")
corr_matrix.to_csv(corr_output)
print(f"\n✅ Matriz guardada en: {corr_output}")

# 6. PROMEDIOS POR PAÍS (2000-2023)
print("\n" + "="*70)
print("6. PROMEDIOS POR PAÍS (PERÍODO COMPLETO)")
print("="*70)

resumen_pais = df.groupby('cname')[cols_corr].mean().round(2)
print("\n" + resumen_pais.to_string())

resumen_output = os.path.join(PROCESSED_DIR, "resumen_por_pais.csv")
resumen_pais.to_csv(resumen_output)
print(f"\n✅ Resumen guardado en: {resumen_output}")

# 7. HALLAZGOS PRELIMINARES
print("\n" + "="*70)
print("7. HALLAZGOS PRELIMINARES AUTOMÁTICOS")
print("="*70)

# Correlación Recursos vs Corrupción
corr_rec_corr = df['wdi_totalresrent'].corr(df['wbgi_cce'])
print(f"\n📊 Correlación Recursos Naturales vs Control Corrupción: {corr_rec_corr:.3f}")
if corr_rec_corr < -0.3:
    print("   → Correlación NEGATIVA moderada: Más recursos = MÁS corrupción")
elif corr_rec_corr < -0.1:
    print("   → Correlación negativa débil")
else:
    print("   → Correlación no significativa")

# Correlación Recursos vs PIB
corr_rec_pib = df['wdi_totalresrent'].corr(df['wdi_gdpcapcon2017'])
print(f"\n💰 Correlación Recursos Naturales vs PIB: {corr_rec_pib:.3f}")
if corr_rec_pib > 0.5:
    print("   → Correlación POSITIVA fuerte: Recursos impulsan PIB")
elif corr_rec_pib > 0.3:
    print("   → Correlación positiva moderada")
else:
    print("   → Correlación débil o no significativa")

# País con mayor dependencia de recursos
pais_max_recursos = resumen_pais['wdi_totalresrent'].idxmax()
max_recursos_val = resumen_pais.loc[pais_max_recursos, 'wdi_totalresrent']
print(f"\n🛢️ País MÁS dependiente de recursos: {pais_max_recursos} ({max_recursos_val:.1f}% PIB)")

# País con mejor control de corrupción
pais_mejor_corr = resumen_pais['wbgi_cce'].idxmax()
mejor_corr_val = resumen_pais.loc[pais_mejor_corr, 'wbgi_cce']
print(f"🏛️ País con MEJOR control corrupción: {pais_mejor_corr} (índice: {mejor_corr_val:.2f})")

# País con mayor PIB per cápita
pais_max_pib = resumen_pais['wdi_gdpcapcon2017'].idxmax()
max_pib_val = resumen_pais.loc[pais_max_pib, 'wdi_gdpcapcon2017']
print(f"💵 País con MAYOR PIB per cápita: {pais_max_pib} (${max_pib_val:,.0f})")

print("\n" + "="*70)
print("✅ VALIDACIÓN COMPLETADA")
print("="*70)
print(f"\nARCHIVOS GENERADOS:")
print(f"  1. {corr_output}")
print(f"  2. {resumen_output}")
print(f"\n📌 PRÓXIMO PASO: Crear visualizaciones con Plotly")
