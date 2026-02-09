# explorar_datos_completo.py (VERSIÓN CORREGIDA)
import pandas as pd
import numpy as np

csv_path = "F:/LABSTORAGE/data/qog_std_ts_jan24.csv"

# COLUMNAS CONFIRMADAS QUE EXISTEN EN EL CSV
columnas_interes = [
    'cname',
    'year',
    'wdi_oilrent',           # Renta de petróleo/gas (% PIB) - CONFIRMADA
    'wdi_gdpcappppcon2017',  # PIB per cápita PPP constante 2017 - CONFIRMADA
    'wbgi_cce',              # Control de corrupción - CONFIRMADA
    'undp_hdi',              # Índice Desarrollo Humano - CONFIRMADA
    'wdi_lifexp'             # Esperanza de vida - CONFIRMADA
]

print("="*70)
print("CARGANDO DATASET...")
print("="*70)

try:
    df = pd.read_csv(csv_path, usecols=columnas_interes)
    print(f"✅ Dataset cargado exitosamente: {len(df)} registros totales\n")
except Exception as e:
    print(f"❌ ERROR al cargar: {e}")
    exit()

# FILTRAR PAÍSES DE ASIA CENTRAL (2000-2023)
paises = ['Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan', 'Uzbekistan']
df = df[(df['cname'].isin(paises)) & (df['year'] >= 2000) & (df['year'] <= 2023)]

print("="*70)
print("1. RESUMEN GENERAL DEL FILTRADO")
print("="*70)
print(f"Total registros filtrados: {len(df)}")
print(f"Países únicos: {sorted(df['cname'].unique())}")
print(f"Periodo: {df['year'].min()} - {df['year'].max()}")
print(f"Registros por país:")
for pais in paises:
    n = len(df[df['cname'] == pais])
    print(f"  - {pais}: {n} registros")

print("\n" + "="*70)
print("2. ANÁLISIS DE NULOS (VALORES FALTANTES)")
print("="*70)

# Tabla de nulos general
nulos_total = df.isna().sum()
nulos_pct = (nulos_total / len(df)) * 100
df_nulos = pd.DataFrame({
    'Variable': nulos_total.index,
    'Nulos': nulos_total.values,
    'Porcentaje (%)': nulos_pct.values.round(2)
})
print("\nNulos totales (120 registros):")
print(df_nulos.to_string(index=False))

print("\n" + "="*70)
print("3. NULOS POR PAÍS (detectar patrones sistemáticos)")
print("="*70)

for pais in paises:
    df_pais = df[df['cname'] == pais]
    print(f"\n{pais} ({len(df_pais)} registros):")
    print("-" * 60)
    for col in ['wdi_oilrent', 'wdi_gdpcappppcon2017', 'wbgi_cce', 'undp_hdi', 'wdi_lifexp']:
        n_nulos = df_pais[col].isna().sum()
        pct = (n_nulos / len(df_pais)) * 100
        status = "⚠️ CRÍTICO" if pct > 20 else "✅ OK" if pct == 0 else "⚠️"
        print(f"  {col:25s}: {n_nulos:2d} nulos ({pct:5.1f}%) {status}")

print("\n" + "="*70)
print("4. ESTADÍSTICAS DESCRIPTIVAS (valores no-nulos)")
print("="*70)
print("\n" + df.describe().to_string())

print("\n" + "="*70)
print("5. DETECTAR PROBLEMAS EN VARIABLES CLAVE")
print("="*70)

# PETRÓLEO/GAS (wdi_oilrent)
print("\n📊 RENTA DE PETRÓLEO/GAS (wdi_oilrent):")
print(f"  Rango: [{df['wdi_oilrent'].min():.2f}, {df['wdi_oilrent'].max():.2f}]")
print(f"  Valores = 0: {(df['wdi_oilrent'] == 0).sum()} registros")
print(f"  Valores < 1%: {(df['wdi_oilrent'] < 1).sum()} registros")
print(f"  Valores > 30%: {(df['wdi_oilrent'] > 30).sum()} registros (países MUY dependientes)")

# PIB per cápita
print("\n💰 PIB PER CÁPITA PPP (wdi_gdpcappppcon2017):")
print(f"  Rango: [{df['wdi_gdpcappppcon2017'].min():.0f}, {df['wdi_gdpcappppcon2017'].max():.0f}] USD")
print(f"  Valores negativos: {(df['wdi_gdpcappppcon2017'] < 0).sum()}")

# CORRUPCIÓN (escala Banco Mundial)
print("\n🏛️ CONTROL DE CORRUPCIÓN (wbgi_cce):")
print(f"  Rango real: [{df['wbgi_cce'].min():.2f}, {df['wbgi_cce'].max():.2f}]")
print(f"  Escala teórica: -2.5 (MUY corrupto) a +2.5 (MUY limpio)")
print(f"  Interpretación: Valores negativos = alta corrupción")

# HDI
print("\n📈 ÍNDICE DESARROLLO HUMANO (undp_hdi):")
print(f"  Rango: [{df['undp_hdi'].min():.3f}, {df['undp_hdi'].max():.3f}]")
print(f"  Escala teórica: 0 (bajo) a 1 (alto)")

# ESPERANZA DE VIDA
print("\n🏥 ESPERANZA DE VIDA (wdi_lifexp):")
print(f"  Rango: [{df['wdi_lifexp'].min():.1f}, {df['wdi_lifexp'].max():.1f}] años")

print("\n" + "="*70)
print("6. REGISTROS CON NULOS EN VARIABLES CRÍTICAS")
print("="*70)

# Identificar registros problemáticos
df_problemas = df[df[['wdi_oilrent', 'wdi_gdpcappppcon2017', 'wbgi_cce']].isna().any(axis=1)]

if len(df_problemas) > 0:
    print(f"\n⚠️  {len(df_problemas)} registros tienen nulos en variables clave:")
    print(df_problemas[['cname', 'year', 'wdi_oilrent', 'wbgi_cce', 'undp_hdi']].to_string(index=False))
else:
    print("\n✅ NO hay nulos en variables críticas (Petróleo, PIB, Corrupción)")

print("\n" + "="*70)
print("7. VERIFICAR AÑOS CON DATOS COMPLETOS POR PAÍS")
print("="*70)

for pais in paises:
    df_pais = df[df['cname'] == pais].copy()
    # Registros sin nulos en variables clave
    df_completo = df_pais.dropna(subset=['wdi_oilrent', 'wdi_gdpcappppcon2017', 'wbgi_cce'])
    años_completos = sorted(df_completo['year'].unique())
    print(f"\n{pais}:")
    print(f"  Años CON datos completos: {len(años_completos)} de 24")
    if len(años_completos) < 24:
        años_faltantes = set(range(2000, 2024)) - set(años_completos)
        print(f"  Años problemáticos: {sorted(años_faltantes)}")

print("\n" + "="*70)
print("8. ANÁLISIS PARA VARIABLES DERIVADAS")
print("="*70)

# Simular cálculos de variables derivadas para detectar problemas
print("\n🔍 Verificar si fórmulas son seguras:")

# 1. Eficiencia de Recursos (PIB / Petróleo)
df_test = df.dropna(subset=['wdi_gdpcappppcon2017', 'wdi_oilrent'])
div_cero = df_test[df_test['wdi_oilrent'] == 0]
print(f"\n1. Eficiencia Recursos (PIB / Petróleo):")
print(f"   Registros con Petróleo = 0: {len(div_cero)} → ⚠️  DIVISIÓN POR CERO")
print(f"   Solución: Añadir +0.01 al denominador o filtrar países sin petróleo")

# 2. Brecha Corrupción-Riqueza
df_test2 = df.dropna(subset=['wdi_gdpcappppcon2017', 'wbgi_cce'])
print(f"\n2. Brecha Corrupción-Riqueza (PIB / (Corrupción_inv + 3)):")
corr_invertida = -df_test2['wbgi_cce']
brecha_test = corr_invertida + 3
print(f"   Rango (Corrupción_inv + 3): [{brecha_test.min():.2f}, {brecha_test.max():.2f}]")
if brecha_test.min() < 0.5:
    print(f"   ⚠️  Denominador muy cercano a 0 → considerar otro offset")
else:
    print(f"   ✅ Denominador seguro (todos > 0.5)")

print("\n" + "="*70)
print("ANÁLISIS COMPLETADO")
print("="*70)
print("\n📌 PRÓXIMO PASO: Copiar este output completo y enviarlo para:")
print("   1. Validar estrategia de nulos personalizada por país")
print("   2. Ajustar fórmulas de variables derivadas")
print("   3. Generar pipeline.py definitivo")
