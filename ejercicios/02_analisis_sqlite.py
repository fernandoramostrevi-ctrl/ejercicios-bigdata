# -*- coding: utf-8 -*-
"""
================================================================================
|| EJERCICIO DIDÁCTICO: Análisis de Datos desde SQLite con Visualización      ||
================================================================================
|| PROFESOR: Juan Marcelo Gutierrez Miranda                                   ||
|| CURSO: Big Data - Antigravity                                             ||
================================================================================

Objetivo:
---------
Este script se conecta a una base de datos SQLite existente, realiza consultas
analíticas y genera una visualización para entender mejor los datos.

Requisitos:
-----------
- Haber ejecutado previamente el script '01_cargar_sqlite.py'.
- Tener instaladas las librerías: pandas, sqlalchemy, matplotlib, seaborn.
  (pip install pandas sqlalchemy matplotlib seaborn)

"""

# ------------------------------------------------------------------------------
# PASO 1: Importación de librerías y configuración de rutas
# ------------------------------------------------------------------------------
import os
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("========================================================")
print("== INICIO DEL SCRIPT: Análisis y Visualización desde SQLite ==")
print("========================================================")

# --- Definición de Rutas ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RUTA_DB = os.path.join(BASE_DIR, "datos", "taxi.db")
NOMBRE_TABLA = "viajes_taxi"
RUTA_GRAFICO = os.path.join(BASE_DIR, "ejercicios", "distribucion_propinas.png")

print(f"\n[CONFIG] Usando la base de datos en: {RUTA_DB}")
print(f"[CONFIG] El gráfico se guardará en: {RUTA_GRAFICO}")

# ------------------------------------------------------------------------------
# PASO 2: Función para realizar el análisis y la visualización
# ------------------------------------------------------------------------------

def analizar_y_visualizar_propinas():
    """
    Se conecta a la BD, calcula estadísticas y genera un histograma de las propinas.
    """
    print("\n--- Análisis: Calculando estadísticas y generando visualización ---")

    if not os.path.exists(RUTA_DB):
        print(f"❌ ERROR: No se encontró la base de datos en {RUTA_DB}")
        return

    try:
        # 1. Conectar a la base de datos.
        print("🔌 Conectando a la base de datos...")
        motor_db = create_engine(f"sqlite:///{RUTA_DB}")

        # 2. Definir la consulta SQL.
        #    Traemos solo la columna 'tip_amount' para optimizar la memoria.
        #    Filtramos para excluir propinas de 0 o negativas, que no son informativas
        #    para la distribución de propinas reales, y valores atípicos muy grandes.
        consulta_sql = f"SELECT tip_amount FROM {NOMBRE_TABLA} WHERE tip_amount > 0 AND tip_amount < 50;"
        print(f"🔍 Ejecutando consulta: \"{consulta_sql}\"")

        # 3. Leer los datos en un DataFrame.
        df_propinas = pd.read_sql_query(consulta_sql, motor_db)
        
        if df_propinas.empty:
            print("❌ No se encontraron datos de propinas para analizar.")
            return

        # 4. Calcular estadísticas.
        propina_media = df_propinas['tip_amount'].mean()
        propina_mediana = df_propinas['tip_amount'].median()
        propina_maxima = df_propinas['tip_amount'].max()

        print("\n--------------------------------------------------------")
        print("📊 ESTADÍSTICAS DE PROPINAS (mayores a $0):")
        print(f"  - Propina Media:   ${propina_media:.2f}")
        print(f"  - Propina Mediana: ${propina_mediana:.2f} (el valor central)")
        print(f"  - Propina Máxima (en este rango): ${propina_maxima:.2f}")
        print("--------------------------------------------------------")

        # 5. Generar la visualización.
        print("\n🎨 Generando histograma de la distribución de propinas...")
        
        # Configurar el estilo del gráfico con Seaborn
        sns.set_style("whitegrid")
        plt.figure(figsize=(12, 7)) # Tamaño de la figura en pulgadas

        # Crear el histograma
        sns.histplot(df_propinas['tip_amount'], bins=50, kde=True)
        # - bins=50: divide los datos en 50 barras para ver más detalle.
        # - kde=True: dibuja una línea suave (Kernel Density Estimate) que estima la forma de la distribución.

        # Añadir títulos y etiquetas para que el gráfico sea fácil de entender
        plt.title('Distribución de Propinas en Taxis de NYC', fontsize=16)
        plt.xlabel('Monto de la Propina ($)', fontsize=12)
        plt.ylabel('Frecuencia (Número de Viajes)', fontsize=12)
        
        # Añadir una línea vertical para marcar la media
        plt.axvline(propina_media, color='red', linestyle='--', linewidth=2, label=f'Media: ${propina_media:.2f}')
        plt.legend() # Muestra la etiqueta de la línea de la media

        # 6. Guardar el gráfico en un archivo.
        plt.savefig(RUTA_GRAFICO)
        print(f"✅ Gráfico guardado con éxito en: {os.path.basename(RUTA_GRAFICO)}")

    except Exception as e:
        print(f"❌ Ocurrió un error durante el análisis: {e}")


# ------------------------------------------------------------------------------
# PASO 3: Ejecución principal del script
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    analizar_y_visualizar_propinas()
    print("\n========================================================")
    print("== FIN DEL SCRIPT ==")
    print("========================================================")
