import os
import pandas as pd
import sqlite3
import glob

# --- Constantes ---
# Define las rutas para que el script sea más fácil de leer y mantener.

# La ruta absoluta de la carpeta donde se encuentra este script.
# Esto asegura que las rutas funcionen sin importar desde dónde se ejecute el script.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# La ruta completa al archivo de la base de datos que vamos a crear.
# Se guardará en la misma carpeta que el script.
DB_PATH_A = os.path.join(SCRIPT_DIR, "tienda_modelo_a.db")

# La ruta a la carpeta que contiene los archivos CSV.
# Subimos un nivel desde SCRIPT_DIR para llegar a la raíz del proyecto.
CSV_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "datos", "csv_tienda_informatica"))


def crear_modelo_a():
    """
    Crea la base de datos para el Modelo A (Catálogo Simple - Desnormalizado).

    Lee todos los archivos CSV de la carpeta de datos y crea una tabla en la
    base de datos SQLite por cada archivo, insertando todos sus datos.
    """
    print("--- Iniciando la creación del Modelo A: Catálogo Simple ---")

    # --- 1. Conexión a la Base de Datos ---
    # sqlite3.connect() abre una conexión con el archivo de la base de datos.
    # Si el archivo no existe, lo crea automáticamente.
    try:
        conn = sqlite3.connect(DB_PATH_A)
        print(f"✅ Conexión establecida con la base de datos en: {DB_PATH_A}")
    except sqlite3.Error as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return

    # --- 2. Encontrar y procesar todos los archivos CSV ---
    # glob.glob() encuentra todos los archivos que coinciden con un patrón.
    # En este caso, todos los archivos que terminan en .csv dentro de CSV_DIR.
    csv_files = glob.glob(os.path.join(CSV_DIR, "*.csv"))

    if not csv_files:
        print(f"❌ Advertencia: No se encontraron archivos CSV en la carpeta: {CSV_DIR}")
        conn.close()
        return

    print(f"📂 Encontrados {len(csv_files)} archivos CSV para procesar.")

    # --- 3. Bucle para leer cada CSV y guardarlo en una tabla SQL ---
    for csv_file_path in csv_files:
        try:
            # Extraer el nombre del archivo sin la extensión para usarlo como nombre de tabla.
            # Ejemplo: de "C:/.../cpus_intel.csv" obtenemos "cpus_intel"
            table_name = os.path.basename(csv_file_path).replace(".csv", "")
            
            print(f"  - Procesando '{os.path.basename(csv_file_path)}' -> Creando tabla '{table_name}'...")

            # Leer el archivo CSV en un DataFrame de Pandas.
            df = pd.read_csv(csv_file_path)

            # --- El paso clave: DataFrame.to_sql() ---
            # Esta función de Pandas es extremadamente útil. Hace todo el trabajo por nosotros:
            # 1. Crea la tabla SQL si no existe.
            # 2. Infiere los tipos de datos de las columnas.
            # 3. Inserta todas las filas del DataFrame en la tabla.
            df.to_sql(
                name=table_name,      # Nombre de la tabla SQL.
                con=conn,             # La conexión a la base de datos.
                if_exists="replace",  # Si la tabla ya existe, la borra y la vuelve a crear. Muy útil para re-ejecutar el script.
                index=False           # No queremos guardar el índice del DataFrame como una columna en la tabla SQL.
            )

        except Exception as e:
            print(f"  ❌ Error procesando el archivo {os.path.basename(csv_file_path)}: {e}")

    # --- 4. Cierre de la conexión ---
    # Es una buena práctica cerrar siempre la conexión cuando hemos terminado.
    conn.close()
    print("\n✅ Proceso completado. Base de datos 'tienda_modelo_a.db' creada con éxito.")
    print("--- Fin del Modelo A ---")


# --- Punto de entrada del script ---
# El código dentro de este 'if' solo se ejecuta cuando corres el script directamente.
if __name__ == "__main__":
    # Llamamos a la función principal para crear la base de datos.
    crear_modelo_a()
