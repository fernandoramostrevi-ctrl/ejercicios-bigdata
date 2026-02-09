# diagnosticar_columnas.py
import pandas as pd

csv_path = "F:/LABSTORAGE/data/qog_std_ts_jan24.csv"

# Leer solo la primera fila para ver todas las columnas disponibles
df_sample = pd.read_csv(csv_path, nrows=0)

print("="*60)
print("COLUMNAS DISPONIBLES EN EL CSV")
print("="*60)
print(f"Total columnas: {len(df_sample.columns)}\n")

# Mostrar todas las columnas
for i, col in enumerate(df_sample.columns, 1):
    print(f"{i:3d}. {col}")

print("\n" + "="*60)
print("BUSCAR COLUMNAS RELACIONADAS CON NUESTRAS VARIABLES")
print("="*60)

# Buscar columnas que contengan palabras clave
keywords = ['gdp', 'corrupt', 'resource', 'rent', 'hdi', 'life', 'wbgi', 'wdi', 'undp']

for keyword in keywords:
    columnas_encontradas = [col for col in df_sample.columns if keyword.lower() in col.lower()]
    if columnas_encontradas:
        print(f"\nColumnas con '{keyword}':")
        for col in columnas_encontradas:
            print(f"  - {col}")
