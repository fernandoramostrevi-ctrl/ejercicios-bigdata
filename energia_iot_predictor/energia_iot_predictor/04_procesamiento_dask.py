import dask.dataframe as dd


def procesar_con_dask():
    """
    Usa Dask para procesar datos que no cabrían en RAM (simulamos el caso).
    """
    print("⚡ Procesando con Dask (paralelizado)...")

    # Leer Parquet con Dask
    df = dd.read_parquet('data/processed/sensores.parquet')

    print(f"Tipo de dato: {type(df)}")  # dask.dataframe.DataFrame

    # Cálculos agregados (se ejecutan en paralelo)
    print("\n📊 Estadísticas agregadas por mes:")
    result = df.groupby('mes').agg({
        'consumo_kwh': ['mean', 'max', 'min'],
        'temperatura_c': 'mean'
    }).compute()  # .compute() ejecuta el cálculo

    print(result)

    return result


if __name__ == "__main__":
    procesar_con_dask()
import dask.dataframe as dd


def procesar_con_dask():
    """
    Usa Dask para procesar datos que no cabrían en RAM (simulamos el caso).
    """
    print("⚡ Procesando con Dask (paralelizado)...")

    # Leer Parquet con Dask
    df = dd.read_parquet('data/processed/sensores.parquet')

    print(f"Tipo de dato: {type(df)}")  # dask.dataframe.DataFrame

    # Cálculos agregados (se ejecutan en paralelo)
    print("\n📊 Estadísticas agregadas por mes:")
    result = df.groupby('mes').agg({
        'consumo_kwh': ['mean', 'max', 'min'],
        'temperatura_c': 'mean'
    }).compute()  # .compute() ejecuta el cálculo

    print(result)

    return result


if __name__ == "__main__":
    procesar_con_dask()
