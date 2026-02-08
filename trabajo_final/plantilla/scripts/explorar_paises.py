import pandas as pd

csv_path = "F:/LABSTORAGE/data/qog_std_ts_jan24.csv"

print("Leyendo CSV...")
df_explore = pd.read_csv(csv_path, usecols=['cname', 'year'])
print(f"Total de filas: {len(df_explore)}")

keywords = ['Kazakhstan', 'Kazakh', 'Kyrgyz', 'Tajik', 'Turkmen', 'Uzbek']

paises_encontrados = []
for keyword in keywords:
    matches = df_explore['cname'].unique()
    matches = [p for p in matches if keyword.lower() in str(p).lower()]
    paises_encontrados.extend(matches)

paises_encontrados = list(set(paises_encontrados))
paises_encontrados.sort()

print("\n=== PAÍSES ENCONTRADOS ===")
for pais in paises_encontrados:
    print(f"  - {pais}")

df_asia_central = df_explore[df_explore['cname'].isin(paises_encontrados)]
print(f"\nAño mínimo: {df_asia_central['year'].min()}")
print(f"Año máximo: {df_asia_central['year'].max()}")

print("\n=== REGISTROS POR PAÍS (2000-2023) ===")
df_periodo = df_asia_central[(df_asia_central['year'] >= 2000) & (df_asia_central['year'] <= 2023)]
conteo = df_periodo['cname'].value_counts().sort_index()
print(conteo)
print(f"\nTotal: {len(df_periodo)} registros")
print(f"Esperado: {5 * 24} registros")
