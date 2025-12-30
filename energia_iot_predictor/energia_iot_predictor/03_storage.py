import pandas as pd
import sqlite3


def almacenar_datos():
    """
    Guarda los datos limpios en SQLite (consultas rápidas) y Parquet (análisis Big Data).
    """
    print("💾 Almacenando datos...")

    df = pd.read_csv('data/processed/sensores_clean.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 1. CAPA RELACIONAL: SQLite (para consultas SQL)
    print("Guardando en SQLite...")
    conn = sqlite3.connect('data/energia.db')
    df.to_sql('mediciones', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ Datos guardados en SQLite (data/energia.db)")

    # 2. CAPA ANALÍTICA: Parquet (Data Lake)
    print("Guardando en Parquet...")
    df.to_parquet('data/processed/sensores.parquet', compression='snappy')
    print("✅ Datos guardados en Parquet (data/processed/sensores.parquet)")

    # Comparar tamaños
    import os
    csv_size = os.path.getsize('data/processed/sensores_clean.csv') / 1024
    parquet_size = os.path.getsize('data/processed/sensores.parquet') / 1024
    print(f"\n📦 Comparación de tamaños:")
    print(f"   CSV: {csv_size:.1f} KB")
    print(f"   Parquet: {parquet_size:.1f} KB (ahorro: {100 * (1 - parquet_size / csv_size):.1f}%)")


if __name__ == "__main__":
    almacenar_datos()
