import os
import sqlite3
import pandas as pd

# Rutas
RUTA_CSV = r"C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\datos\csv_tienda_informatica\csv_tienda_informatica"
RUTA_DB_B = r"C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\ejercicios\01_bases_de_datos\1.1_introduccion_sqlite\modelos_tienda_fer\tienda_modelo_b.db"


def extraer_fabricante(name: str) -> str:
    if not isinstance(name, str):
        return ""
    name = name.strip()
    if not name:
        return ""
    return name.split()[0]   # aproximación simple: primer token


def crear_tablas(conn: sqlite3.Connection):
    cur = conn.cursor()

    # Eliminar tablas si existen (para rehacer el modelo B desde cero)
    cur.executescript("""
    DROP TABLE IF EXISTS storage;
    DROP TABLE IF EXISTS memory;
    DROP TABLE IF EXISTS motherboard;
    DROP TABLE IF EXISTS cpu;
    DROP TABLE IF EXISTS product;
    DROP TABLE IF EXISTS category;
    DROP TABLE IF EXISTS color;
    DROP TABLE IF EXISTS manufacturer;
    """)

    cur.executescript("""
    CREATE TABLE manufacturer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE color (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL,
        manufacturer_id INTEGER,
        color_id INTEGER,
        category_id INTEGER NOT NULL,
        source_table TEXT NOT NULL,
        source_row_index INTEGER,
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(id),
        FOREIGN KEY (color_id) REFERENCES color(id),
        FOREIGN KEY (category_id) REFERENCES category(id)
    );

    CREATE TABLE cpu (
        product_id INTEGER PRIMARY KEY,
        core_count INTEGER,
        core_clock REAL,
        boost_clock REAL,
        tdp INTEGER,
        graphics TEXT,
        smt TEXT,
        socket TEXT,
        FOREIGN KEY (product_id) REFERENCES product(id)
    );

    CREATE TABLE motherboard (
        product_id INTEGER PRIMARY KEY,
        socket TEXT,
        form_factor TEXT,
        max_memory INTEGER,
        memory_slots INTEGER,
        color TEXT,
        FOREIGN KEY (product_id) REFERENCES product(id)
    );

    CREATE TABLE memory (
        product_id INTEGER PRIMARY KEY,
        speed TEXT,
        modules TEXT,
        price_per_gb REAL,
        color TEXT,
        first_word_latency TEXT,
        cas_latency TEXT,
        FOREIGN KEY (product_id) REFERENCES product(id)
    );

    CREATE TABLE storage (
        product_id INTEGER PRIMARY KEY,
        capacity TEXT,
        type TEXT,
        cache TEXT,
        form_factor TEXT,
        interface TEXT,
        FOREIGN KEY (product_id) REFERENCES product(id)
    );
    """)
    conn.commit()


def construir_dimensiones_y_productos():
    """
    Lee todos los CSV y construye:
      - set de fabricantes
      - set de colores
      - set de categorías
      - DataFrame de productos normalizados
    """
    archivos_csv = [
        f for f in os.listdir(RUTA_CSV)
        if f.lower().endswith(".csv")
    ]

    fabricantes = set()
    colores = set()
    categorias = set()

    registros_productos = []

    for nombre_csv in sorted(archivos_csv):
        categoria = os.path.splitext(nombre_csv)[0]  # p.ej. cpu, motherboard, ...
        categorias.add(categoria)

        ruta_fichero = os.path.join(RUTA_CSV, nombre_csv)
        df = pd.read_csv(ruta_fichero)

        tiene_color = "color" in df.columns

        for idx, row in df.iterrows():
            name = row.get("name")
            price = row.get("price")

            fabricante = extraer_fabricante(name)
            if fabricante:
                fabricantes.add(fabricante)

            color_val = row.get("color") if tiene_color else None
            if isinstance(color_val, str) and color_val.strip():
                colores.add(color_val.strip())

            registros_productos.append({
                "name": name,
                "price": price,
                "manufacturer_name": fabricante if fabricante else None,
                "color_name": color_val.strip() if isinstance(color_val, str) and color_val.strip() else None,
                "category_name": categoria,
                "source_table": categoria,
                "source_row_index": idx
            })

    df_productos = pd.DataFrame(registros_productos)

    return fabricantes, colores, categorias, df_productos


def poblar_dimensiones(conn, fabricantes, colores, categorias):
    """
    Inserta fabricantes, colores y categorías en sus tablas
    y devuelve diccionarios de mapeo nombre -> id.
    """
    cur = conn.cursor()

    # manufacturer
    for nombre in sorted(fabricantes):
        cur.execute("INSERT INTO manufacturer(name) VALUES (?)", (nombre,))
    # color
    for nombre in sorted(colores):
        cur.execute("INSERT INTO color(name) VALUES (?)", (nombre,))
    # category
    for nombre in sorted(categorias):
        cur.execute("INSERT INTO category(name) VALUES (?)", (nombre,))

    conn.commit()

    # construir mapas
    cur.execute("SELECT id, name FROM manufacturer")
    map_manufacturer = {name: mid for (mid, name) in cur.fetchall()}

    cur.execute("SELECT id, name FROM color")
    map_color = {name: cid for (cid, name) in cur.fetchall()}

    cur.execute("SELECT id, name FROM category")
    map_category = {name: cid for (cid, name) in cur.fetchall()}

    return map_manufacturer, map_color, map_category


def poblar_productos(conn, df_productos, map_manufacturer, map_color, map_category):
    """
    Inserta los productos en la tabla product utilizando las FKs correctas.
    """
    registros = []
    for _, row in df_productos.iterrows():
        man_id = map_manufacturer.get(row["manufacturer_name"]) if row["manufacturer_name"] else None
        col_id = map_color.get(row["color_name"]) if row["color_name"] else None
        cat_id = map_category[row["category_name"]]

        registros.append((
            row["name"],
            float(row["price"]) if pd.notna(row["price"]) else None,
            man_id,
            col_id,
            cat_id,
            row["source_table"],
            int(row["source_row_index"])
        ))

    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO product(name, price, manufacturer_id, color_id, category_id, source_table, source_row_index)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, registros)
    conn.commit()


def main():
    os.makedirs(os.path.dirname(RUTA_DB_B), exist_ok=True)
    conn = sqlite3.connect(RUTA_DB_B)

    # 1) Crear tablas normalizadas
    crear_tablas(conn)

    # 2) Extraer fabricantes, colores, categorías y productos
    fabricantes, colores, categorias, df_productos = construir_dimensiones_y_productos()

    # 3) Poblar tablas manufacturer, color, category
    map_manufacturer, map_color, map_category = poblar_dimensiones(conn, fabricantes, colores, categorias)

    # 4) Insertar productos con FKs correctas
    poblar_productos(conn, df_productos, map_manufacturer, map_color, map_category)

    # 5) (Opcional, siguiente paso) poblar tablas cpu/motherboard/memory/storage
    #    usando product.id y filtrando df_productos por category_name.

    conn.close()
    print("Modelo B creado en tienda_modelo_b.db")


if __name__ == "__main__":
    main()
