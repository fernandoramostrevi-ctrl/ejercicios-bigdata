import os
import sqlite3
import glob
import pandas as pd

# --- Constantes ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH_B = os.path.join(SCRIPT_DIR, "tienda_modelo_b.db")
CSV_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "datos", "csv_tienda_informatica"))

def crear_tablas_normalizadas(conn):
    """
    Crea las tablas para el Modelo B (Normalizado) de forma individual y con depuración.
    """
    print("--- Creando estructura de tablas normalizadas (5 tablas) ---")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);")
        print("  [1/5] ✅ Tabla 'categorias' creada o ya existente.")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS fabricantes (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);")
        print("  [2/5] ✅ Tabla 'fabricantes' creada o ya existente.")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS colores (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);")
        print("  [3/5] ✅ Tabla 'colores' creada o ya existente.")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio REAL,
                categoria_id INTEGER,
                fabricante_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id),
                FOREIGN KEY (fabricante_id) REFERENCES fabricantes (id)
            );
        """)
        print("  [4/5] ✅ Tabla 'productos' creada o ya existente.")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos_colores (
                producto_id INTEGER,
                color_id INTEGER,
                PRIMARY KEY (producto_id, color_id),
                FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE,
                FOREIGN KEY (color_id) REFERENCES colores (id) ON DELETE CASCADE
            );
        """)
        print("  [5/5] ✅ Tabla 'productos_colores' creada o ya existente.")
        
        conn.commit()
        print("✅ Commit realizado. Todas las tablas deberían estar guardadas.")
        
    except sqlite3.Error as e:
        print(f"❌ Error al crear una de las tablas: {e}")
        print("   - El proceso se ha detenido. La base de datos puede estar incompleta.")
        conn.rollback()


def poblar_tablas(conn, csv_files):
    """Lee los archivos CSV, extrae los datos y los carga en las tablas normalizadas."""
    print("\n--- Poblando tablas normalizadas ---")
    cursor = conn.cursor()
    
    print("  - Extrayendo entidades únicas (categorías, fabricantes, colores)...")
    categorias, fabricantes, colores = set(), set(), set()
    
    for csv_file in csv_files:
        categorias.add(os.path.basename(csv_file).replace(".csv", ""))
        df = pd.read_csv(csv_file)
        if 'name' in df.columns:
            fabricantes.update(df['name'].str.split().str[0].dropna().unique())
        if 'color' in df.columns:
            colores_en_archivo = df['color'].dropna().str.split(',').explode().str.strip().unique()
            colores.update(colores_en_archivo)

    cursor.executemany("INSERT OR IGNORE INTO categorias (nombre) VALUES (?)", [(c,) for c in categorias])
    cursor.executemany("INSERT OR IGNORE INTO fabricantes (nombre) VALUES (?)", [(f,) for f in fabricantes])
    cursor.executemany("INSERT OR IGNORE INTO colores (nombre) VALUES (?)", [(c,) for c in colores if c])
    conn.commit()
    print(f"  ✅ Entidades insertadas.")

    categorias_map = pd.read_sql("SELECT id, nombre FROM categorias", conn).set_index('nombre')['id'].to_dict()
    fabricantes_map = pd.read_sql("SELECT id, nombre FROM fabricantes", conn).set_index('nombre')['id'].to_dict()
    colores_map = pd.read_sql("SELECT id, nombre FROM colores", conn).set_index('nombre')['id'].to_dict()
    
    print("\n  - Procesando y cargando productos y sus relaciones de color...")
    total_productos = 0
    for csv_file in csv_files:
        categoria_nombre = os.path.basename(csv_file).replace(".csv", "")
        categoria_id = categorias_map.get(categoria_nombre)
        df = pd.read_csv(csv_file)
        
        for _, row in df.iterrows():
            nombre_producto, precio = row.get('name'), row.get('price')
            if not nombre_producto or pd.isna(precio): continue

            fabricante_nombre = nombre_producto.split()[0]
            fabricante_id = fabricantes_map.get(fabricante_nombre)
            
            cursor.execute("INSERT INTO productos (nombre, precio, categoria_id, fabricante_id) VALUES (?, ?, ?, ?)",
                           (nombre_producto, precio, categoria_id, fabricante_id))
            producto_id = cursor.lastrowid
            total_productos += 1

            if 'color' in row and pd.notna(row['color']):
                colores_producto = [c.strip() for c in row['color'].split(',')]
                for color_nombre in colores_producto:
                    color_id = colores_map.get(color_nombre)
                    if color_id:
                        cursor.execute("INSERT OR IGNORE INTO productos_colores (producto_id, color_id) VALUES (?, ?)",
                                       (producto_id, color_id))
    conn.commit()
    print(f"  ✅ {total_productos} productos y sus relaciones de color insertados.")

def crear_modelo_b():
    """Crea y puebla la base de datos para el Modelo B (Normalizado)."""
    print("\n--- Iniciando la creación del Modelo B: Normalizado ---")
    try:
        if os.path.exists(DB_PATH_B):
            os.remove(DB_PATH_B)
            print(f"🗑️ Base de datos antigua '{os.path.basename(DB_PATH_B)}' eliminada.")
        conn = sqlite3.connect(DB_PATH_B)
        print(f"✅ Conexión establecida con la base de datos en: {DB_PATH_B}")
    except (sqlite3.Error, OSError) as e:
        print(f"❌ Error al conectar o eliminar la base de datos: {e}")
        return

    crear_tablas_normalizadas(conn)
    
    csv_files = glob.glob(os.path.join(CSV_DIR, "*.csv"))
    if not csv_files:
        print(f"❌ Advertencia: No se encontraron archivos CSV en la carpeta: {CSV_DIR}")
        conn.close()
        return
        
    poblar_tablas(conn, csv_files)

    conn.close()
    print("\n✅ Proceso del Modelo B completado con éxito.")
    print("--- Fin del Modelo B ---")

if __name__ == "__main__":
    crear_modelo_b()
