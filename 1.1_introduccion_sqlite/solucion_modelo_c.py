import os
import sqlite3
import glob
import pandas as pd
import random
from datetime import datetime, timedelta

# --- Constantes ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH_C = os.path.join(SCRIPT_DIR, "tienda_modelo_c.db")
CSV_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "datos", "csv_tienda_informatica"))

# --- Funciones de Creación de Tablas ---

def crear_tablas_catalogo_normalizado(conn):
    """Crea las tablas del catálogo normalizado (Modelo B)."""
    print("--- [1/4] Creando estructura de tablas del catálogo (5 tablas) ---")
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS fabricantes (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS colores (id INTEGER PRIMARY KEY, nombre TEXT NOT NULL UNIQUE);")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, precio REAL,
                categoria_id INTEGER, fabricante_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id),
                FOREIGN KEY (fabricante_id) REFERENCES fabricantes (id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos_colores (
                producto_id INTEGER, color_id INTEGER,
                PRIMARY KEY (producto_id, color_id),
                FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE,
                FOREIGN KEY (color_id) REFERENCES colores (id) ON DELETE CASCADE
            );
        """)
        conn.commit()
        print("      ✅ Tablas del catálogo creadas con éxito.")
    except sqlite3.Error as e:
        print(f"      ❌ Error al crear las tablas del catálogo: {e}")
        conn.rollback()

def crear_tablas_ecommerce(conn):
    """Crea las tablas adicionales para la funcionalidad de e-commerce."""
    print("\n--- [2/4] Creando estructura de tablas de E-Commerce ---")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, apellido TEXT, email TEXT NOT NULL UNIQUE
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY, cliente_id INTEGER NOT NULL, fecha TEXT NOT NULL, 
                estado TEXT NOT NULL CHECK(estado IN ('pendiente', 'enviado', 'entregado', 'cancelado')),
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lineas_pedido (
                id INTEGER PRIMARY KEY, pedido_id INTEGER NOT NULL, producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL, precio_unitario REAL NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                producto_id INTEGER PRIMARY KEY, stock INTEGER NOT NULL, stock_minimo INTEGER DEFAULT 5,
                FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
            );
        """)
        conn.commit()
        print("      ✅ Tablas de E-Commerce creadas con éxito.")
    except sqlite3.Error as e:
        print(f"      ❌ Error al crear las tablas de E-Commerce: {e}")
        conn.rollback()

# --- Funciones de Poblado de Datos ---

def poblar_tablas_catalogo(conn, csv_files):
    """Puebla las tablas del catálogo normalizado (lógica del Modelo B)."""
    print("\n--- [3/4] Poblando tablas del catálogo ---")
    cursor = conn.cursor()
    
    print("  - Extrayendo entidades únicas...")
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

    categorias_map = pd.read_sql("SELECT id, nombre FROM categorias", conn).set_index('nombre')['id'].to_dict()
    fabricantes_map = pd.read_sql("SELECT id, nombre FROM fabricantes", conn).set_index('nombre')['id'].to_dict()
    colores_map = pd.read_sql("SELECT id, nombre FROM colores", conn).set_index('nombre')['id'].to_dict()
    
    print("  - Cargando productos y relaciones...")
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
            if 'color' in row and pd.notna(row['color']):
                colores_producto = [c.strip() for c in row['color'].split(',')]
                for color_nombre in colores_producto:
                    color_id = colores_map.get(color_nombre)
                    if color_id:
                        cursor.execute("INSERT OR IGNORE INTO productos_colores (producto_id, color_id) VALUES (?, ?)",
                                       (producto_id, color_id))
    conn.commit()
    print("      ✅ Tablas del catálogo pobladas.")

def poblar_tablas_ecommerce(conn):
    """Genera y carga datos de ejemplo para las tablas de e-commerce."""
    print("\n--- [4/4] Poblando tablas de E-Commerce con datos de ejemplo ---")
    cursor = conn.cursor()

    # 1. Generar clientes ficticios
    clientes = [("Juan", "Pérez", "juan.perez@email.com"), ("Maria", "García", "maria.garcia@email.com"), ("Carlos", "Ruiz", "carlos.ruiz@email.com")]
    cursor.executemany("INSERT INTO clientes (nombre, apellido, email) VALUES (?, ?, ?)", clientes)
    print(f"  - {len(clientes)} clientes ficticios insertados.")

    # 2. Inicializar inventario con stock aleatorio
    producto_ids = cursor.execute("SELECT id FROM productos").fetchall()
    inventario = [(pid[0], random.randint(50, 200)) for pid in producto_ids]
    cursor.executemany("INSERT INTO inventario (producto_id, stock) VALUES (?, ?)", inventario)
    print(f"  - Inventario inicializado para {len(inventario)} productos.")

    # 3. Generar pedidos de ejemplo
    cliente_ids = [c[0] for c in cursor.execute("SELECT id FROM clientes").fetchall()]
    for i in range(3): # Crear 3 pedidos
        cliente_id = random.choice(cliente_ids)
        fecha = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")
        estado = random.choice(['pendiente', 'enviado', 'entregado'])
        cursor.execute("INSERT INTO pedidos (cliente_id, fecha, estado) VALUES (?, ?, ?)", (cliente_id, fecha, estado))
        pedido_id = cursor.lastrowid
        
        # Añadir entre 1 y 3 productos diferentes a cada pedido
        for _ in range(random.randint(1, 3)):
            producto_aleatorio = random.choice(producto_ids)
            producto_id = producto_aleatorio[0]
            # Obtener el precio actual del producto
            precio_unitario = cursor.execute("SELECT precio FROM productos WHERE id = ?", (producto_id,)).fetchone()[0]
            cantidad = random.randint(1, 5)
            cursor.execute("INSERT INTO lineas_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                           (pedido_id, producto_id, cantidad, precio_unitario))
    print("  - 3 pedidos de ejemplo con sus líneas de pedido han sido generados.")
    
    conn.commit()
    print("      ✅ Tablas de E-Commerce pobladas.")

def crear_modelo_c():
    """Crea y puebla la base de datos para el Modelo C (E-Commerce Completo)."""
    print("\n--- Iniciando la creación del Modelo C: E-Commerce Completo ---")
    try:
        if os.path.exists(DB_PATH_C):
            os.remove(DB_PATH_C)
        conn = sqlite3.connect(DB_PATH_C)
        print(f"✅ Conexión establecida con la base de datos en: {DB_PATH_C}")
    except (sqlite3.Error, OSError) as e:
        print(f"❌ Error al conectar o eliminar la base de datos: {e}")
        return

    crear_tablas_catalogo_normalizado(conn)
    crear_tablas_ecommerce(conn)
    
    csv_files = glob.glob(os.path.join(CSV_DIR, "*.csv"))
    if csv_files:
        poblar_tablas_catalogo(conn, csv_files)
        poblar_tablas_ecommerce(conn)
    else:
        print(f"❌ Advertencia: No se encontraron archivos CSV en {CSV_DIR}. No se pudo poblar el catálogo.")

    conn.close()
    print("\n✅ Proceso del Modelo C completado con éxito.")
    print("--- Fin del Modelo C ---")

if __name__ == "__main__":
    crear_modelo_c()
