import pandas as pd
import matplotlib.pyplot as plt


def analisis_descriptivo():
    """
    Ejercicio 1: Estadística descriptiva básica
    """
    df = pd.read_parquet('data/processed/sensores.parquet')

    print("=== ANÁLISIS DESCRIPTIVO (Ejercicio 1) ===")
    print(df['consumo_kwh'].describe())

    # Gráfico de distribución
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.hist(df['consumo_kwh'], bins=50, edgecolor='black')
    plt.xlabel('Consumo (kWh)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución Original del Consumo')

    plt.subplot(1, 2, 2)
    df.boxplot(column='consumo_kwh')
    plt.ylabel('Consumo (kWh)')
    plt.title('Boxplot - Detección de Outliers')

    plt.tight_layout()
    plt.savefig('analisis_descriptivo.png')
    print("\n✅ Gráfico guardado: analisis_descriptivo.png")


if __name__ == "__main__":
    analisis_descriptivo()
