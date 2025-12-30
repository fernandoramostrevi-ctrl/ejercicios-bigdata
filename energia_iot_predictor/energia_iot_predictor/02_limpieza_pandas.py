import pandas as pd
import numpy as np


def limpiar_datos():
    """
    Limpia los datos usando Pandas: elimina outliers, nulos, duplicados.
    """
    print("🧹 Iniciando limpieza con Pandas...")

    # Cargar datos crudos
    df = pd.read_csv('data/raw/sensores_raw.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    print(f"Registros originales: {len(df):,}")

    # 1. Eliminar duplicados por timestamp
    df = df.drop_duplicates(subset=['timestamp'])

    # 2. Eliminar valores nulos
    antes = len(df)
    df = df.dropna()
    print(f"Nulos eliminados: {antes - len(df)}")

    # 3. Eliminar outliers (IQR method)
    def eliminar_outliers(df, columna):
        Q1 = df[columna].quantile(0.25)
        Q3 = df[columna].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        return df[(df[columna] >= lower) & (df[columna] <= upper)]

    antes = len(df)
    df = eliminar_outliers(df, 'temperatura_c')
    df = eliminar_outliers(df, 'consumo_kwh')
    print(f"Outliers eliminados: {antes - len(df)}")

    # 4. Feature Engineering: Añadir columnas útiles
    df['mes'] = df['timestamp'].dt.month
    df['hora'] = df['timestamp'].dt.hour
    df['dia_semana'] = df['timestamp'].dt.dayofweek  # 0=Lunes, 6=Domingo

    print(f"✅ Limpieza completada. Registros finales: {len(df):,}")

    # Guardar temporalmente (lo usaremos en la siguiente fase)
    df.to_csv('data/processed/sensores_clean.csv', index=False)

    return df


if __name__ == "__main__":
    df_limpio = limpiar_datos()
    print("\n📊 Primeras filas después de limpieza:")
    print(df_limpio.head())
