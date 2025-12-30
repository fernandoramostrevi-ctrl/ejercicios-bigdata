import os
import sqlite3
import pandas as pd

# Ruta carpeta CSV
RUTA_CSV = r"C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\datos\csv_tienda_informatica\csv_tienda_informatica"

# Ruta BD salida (Modelo A)
RUTA_DB = r"C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\ejercicios\01_bases_de_datos\1.1_introduccion_sqlite\modelos_tienda_fer\informatica.db"


def main():
    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(RUTA_DB), exist_ok=True)

    # Conexión a SQLite
    conn = sqlite3.connect(RUTA_DB)

    # Listar todos los CSV de la carpeta
    archivos_csv = [
        f for f in os.listdir(RUTA_CSV)
        if f.lower().endswith(".csv")
    ]

    print("CSV encontrados:", archivos_csv)

    for nombre_csv in archivos_csv:
        ruta_fichero = os.path.join(RUTA_CSV, nombre_csv)

        # Nombre de tabla = nombre de archivo sin extensión
        nombre_tabla = os.path.splitext(nombre_csv)[0]

        print(f"Cargando {nombre_csv} -> tabla {nombre_tabla}")

        # Lee el CSV. Si tus CSV llevan otro separador, ajústalo (sep=";" por ejemplo)
        df = pd.read_csv(ruta_fichero)

        # Volcar a SQLite, reemplazando si ya existiera
        df.to_sql(nombre_tabla, conn, if_exists="replace", index=False)

    conn.close()
    print("Proceso terminado. Revisa tienda_modelo_a.db en PyCharm.")


if __name__ == "__main__":
    main()
