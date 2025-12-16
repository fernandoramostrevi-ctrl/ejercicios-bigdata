import os
import sqlite3
import random
from datetime import datetime

from solucion_modelo_b import (
    RUTA_CSV,
    construir_dimensiones_y_productos,
    crear_tablas as crear_tablas_b,
    poblar_dimensiones,
    poblar_productos,
)

RUTA_DB_C = r"C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\ejercicios\01_bases_de_datos\1.1_introduccion_sqlite\modelos_tienda_fer\tienda_modelo_c.db"


def crear_tablas_extra(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS inventory;
    DROP TABLE IF EXISTS order_item;
    DROP TABLE IF EXISTS "order";
    DROP TABLE IF EXISTS customer;

    CREATE TABLE customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        address TEXT
    );

    CREATE TABLE "order" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customer(id)
    );

    CREATE TABLE order_item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES "order"(id),
        FOREIGN KEY (product_id) REFERENCES product(id)
    );

    CREATE TABLE inventory (
        product_id INTEGER PRIMARY KEY,
        stock INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES product(id)
    );
    """)
    conn.commit()


def generar_clientes(conn: sqlite3.Connection):
    clientes = [
        ("Ana García", "ana@example.com", "Calle A 123, Madrid"),
        ("Luis Pérez", "luis@example.com", "Avenida B 45, Barcelona"),
        ("Marta López", "marta@example.com", "Calle C 7, Valencia"),
        ("Juan Torres", "juan@example.com", "Calle D 9, Sevilla"),
        ("Sara Ruiz", "sara@example.com", "Plaza E 3, Bilbao"),
    ]
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO customer(name, email, address) VALUES (?, ?, ?)",
        clientes
    )
    conn.commit()


def inicializar_inventario(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id FROM product")
    product_ids = [row[0] for row in cur.fetchall()]

    registros = []
    for pid in product_ids:
        stock = random.randint(50, 200)
        registros.append((pid, stock))

    cur.executemany(
        "INSERT INTO inventory(product_id, stock) VALUES (?, ?)",
        registros
    )
    conn.commit()


def generar_pedidos_ejemplo(conn: sqlite3.Connection, num_pedidos: int = 3):
    cur = conn.cursor()

    # obtener clientes y productos
    cur.execute("SELECT id FROM customer")
    clientes = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id, price FROM product WHERE price IS NOT NULL")
    productos = cur.fetchall()  # lista de (product_id, price)

    pedidos_ids = []

    # crear pedidos
    for _ in range(num_pedidos):
        customer_id = random.choice(clientes)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = random.choice(["pending", "paid", "shipped"])

        cur.execute(
            'INSERT INTO "order"(customer_id, order_date, status) VALUES (?, ?, ?)',
            (customer_id, fecha, status)
        )
        pedidos_ids.append(cur.lastrowid)

    # crear items de pedido (2-4 productos por pedido)
    for order_id in pedidos_ids:
        num_items = random.randint(2, 4)
        for _ in range(num_items):
            product_id, price = random.choice(productos)
            quantity = random.randint(1, 3)
            unit_price = float(price)
            cur.execute(
                "INSERT INTO order_item(order_id, product_id, quantity, unit_price) "
                "VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, unit_price)
            )

    conn.commit()


def main():
    os.makedirs(os.path.dirname(RUTA_DB_C), exist_ok=True)
    conn = sqlite3.connect(RUTA_DB_C)

    # 1) Crear y poblar el Modelo B dentro de tienda_modelo_c.db
    crear_tablas_b(conn)
    fabricantes, colores, categorias, df_productos = construir_dimensiones_y_productos()
    map_manufacturer, map_color, map_category = poblar_dimensiones(conn, fabricantes, colores, categorias)
    poblar_productos(conn, df_productos, map_manufacturer, map_color, map_category)

    # (Si en tu Modelo B también poblas cpu/motherboard/memory/storage, puedes reutilizar aquí esa lógica.)

    # 2) Crear tablas extra de e-commerce
    crear_tablas_extra(conn)

    # 3) Generar datos de ejemplo
    generar_clientes(conn)              # 3–5 clientes ficticios
    inicializar_inventario(conn)        # stock aleatorio 50–200 por producto
    generar_pedidos_ejemplo(conn, 3)    # 2–3 pedidos de ejemplo

    conn.close()
    print("Modelo C creado en tienda_modelo_c.db")


if __name__ == "__main__":
    main()
