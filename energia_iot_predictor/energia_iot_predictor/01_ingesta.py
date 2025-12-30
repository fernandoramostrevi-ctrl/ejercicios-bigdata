import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def simular_descarga_sensores():
    """
    Simula la descarga de datos desde una API de sensores IoT.
    En un caso real, harías: requests.get('https://api-sensores.com/data')
    """
    print("📥 Descargando datos de sensores IoT...")

    # Simular 12 meses de datos (medición cada hora)
    fechas = pd.date_range('2024-01-01', '2024-12-31 23:00:00', freq='H')
    n = len(fechas)

    # Simular temperatura con estacionalidad (verano más calor)
    mes = pd.to_datetime(fechas).month
    temp_base = 15 + 10 * np.sin((mes - 1) * np.pi / 6)  # Onda senoidal
    temperatura = temp_base + np.random.normal(0, 3, n)

    # Simular humedad (correlacionada inversamente con temp)
    humedad = 70 - 0.5 * temperatura + np.random.normal(0, 10, n)
    humedad = np.clip(humedad, 30, 95)  # Limitar rango realista

    # Simular consumo (basado en Ejercicio 5)
    consumo_base = 183.29 + 6.12 * temperatura + 1.88 * humedad
    consumo = consumo_base + np.random.normal(0, 20, n)  # Ruido
    consumo = np.clip(consumo, 0, None)  # No puede ser negativo

    df = pd.DataFrame({
        'timestamp': fechas,
        'temperatura_c': temperatura,
        'humedad_pct': humedad,
        'consumo_kwh': consumo
    })

    # Guardar como CSV (datos crudos)
    df.to_csv('data/raw/sensores_raw.csv', index=False)
    print(f"✅ {len(df):,} registros descargados y guardados en data/raw/")

    return df


if __name__ == "__main__":
    datos = simular_descarga_sensores()
    print(datos.head())
