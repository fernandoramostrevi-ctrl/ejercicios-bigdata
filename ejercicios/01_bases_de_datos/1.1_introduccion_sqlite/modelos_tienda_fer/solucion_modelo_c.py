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
    cur.executescript(
        """
    -- Borrado previo para regenerar limpio
    DROP TABLE IF EXISTS cart_item;
    DROP TABLE IF EXISTS cart;
    DROP TABLE IF EXISTS inventory;
    DROP TABLE IF EXISTS order_item;
    DROP TABLE IF EXISTS "order";
    DROP TABLE IF EXISTS customer;

    -- Clientes
    CREATE TABLE customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name    TEXT NOT NULL,
        last_name     TEXT,
        email         TEXT NOT NULL UNIQUE,
        address       TEXT,
        registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    -- Pedidos
    CREATE TABLE "order" (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        order_date  DATETIME NOT NULL,
        status      TEXT CHECK(status IN ('pending','processing','paid','shipped','cancelled')),
        total       REAL,
        FOREIGN KEY (customer_id) REFERENCES customer(id)
    );

    -- Líneas de pedido
    CREATE TABLE order_item (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id   INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity   INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES "order"(id),
        FOREIGN KEY (product_id) REFERENCES product(id)
    );

    -- Inventario
    CREATE TABLE inventory (
        product_id  INTEGER PRIMARY KEY,
        stock       INTEGER NOT NULL,
        min_stock   INTEGER DEFAULT 10,
        location    TEXT,
        last_update DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES product(id)
    );

    -- Carritos
    CREATE TABLE cart (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id      INTEGER NOT NULL,
        created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_modified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        active           INTEGER DEFAULT 1,
        FOREIGN KEY (customer_id) REFERENCES customer(id),
        UNIQUE(customer_id)
    );

    -- Items de carrito
    CREATE TABLE cart_item (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id    INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity   INTEGER NOT NULL,
        FOREIGN KEY (cart_id) REFERENCES cart(id),
        FOREIGN KEY (product_id) REFERENCES product(id),
        UNIQUE(cart_id, product_id)
    );
    """
    )
    conn.commit()


def generar_clientes(conn: sqlite3.Connection):
    clientes = [
        ("Ana", "García", "ana@example.com", "Calle A 123, Madrid"),
        ("Luis", "Pérez", "luis@example.com", "Avenida B 45, Barcelona"),
        ("Marta", "López", "marta@example.com", "Calle C 7, Valencia"),
        ("Juan", "Torres", "juan@example.com", "Calle D 9, Sevilla"),
        ("Sara", "Ruiz", "sara@example.com", "Plaza E 3, Bilbao"),
    ]
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO customer(first_name, last_name, email, address) VALUES (?, ?, ?, ?)",
        clientes,
    )
    conn.commit()


def inicializar_inventario(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id FROM product")
    product_ids = [row[0] for row in cur.fetchall()]

    registros = []
    ubicaciones = ["WH-A", "WH-B", "STORE-1", "STORE-2"]
    for pid in product_ids:
        stock = random.randint(5, 200)
        min_stock = random.randint(5, 30)
        location = random.choice(ubicaciones)
        registros.append((pid, stock, min_stock, location))

    cur.executemany(
        "INSERT INTO inventory(product_id, stock, min_stock, location) "
        "VALUES (?, ?, ?, ?)",
        registros,
    )
    conn.commit()


def generar_pedidos_ejemplo(conn: sqlite3.Connection, num_pedidos: int = 3):
    cur = conn.cursor()

    # obtener clientes y productos
    cur.execute("SELECT id FROM customer")
    clientes = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id, price FROM product WHERE price IS NOT NULL")
    productos = cur.fetchall()  # lista de (product_id, price)

    # crear pedidos
    for _ in range(num_pedidos):
        customer_id = random.choice(clientes)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = random.choice(["pending", "processing", "paid", "shipped"])

        cur.execute(
            'INSERT INTO "order"(customer_id, order_date, status, total) '
            "VALUES (?, ?, ?, ?)",
            (customer_id, fecha, status, 0.0),
        )
        order_id = cur.lastrowid

        # crear items de pedido (2-4 productos por pedido)
        total_pedido = 0.0
        num_items = random.randint(2, 4)
        for _ in range(num_items):
            product_id, price = random.choice(productos)
            quantity = random.randint(1, 3)
            unit_price = float(price)
            subtotal = unit_price * quantity
            total_pedido += subtotal

            cur.execute(
                "INSERT INTO order_item(order_id, product_id, quantity, unit_price) "
                "VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, unit_price),
            )

        # actualizar total del pedido
        cur.execute('UPDATE "order" SET total = ? WHERE id = ?', (total_pedido, order_id))

    conn.commit()


def generar_carritos(conn: sqlite3.Connection):
    """Genera carritos activos para algunos clientes."""
    cur = conn.cursor()

    cur.execute("SELECT id FROM customer")
    customers = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT id FROM product WHERE price IS NOT NULL LIMIT 50")
    products = [row[0] for row in cur.fetchall()]

    # seleccionamos hasta 3 clientes al azar para tener carrito
    for customer_id in random.sample(customers, min(3, len(customers))):
        cur.execute(
            "INSERT INTO cart(customer_id, active) VALUES (?, 1)",
            (customer_id,),
        )
        cart_id = cur.lastrowid

        num_items = random.randint(1, 3)
        for product_id in random.sample(products, num_items):
            quantity = random.randint(1, 2)
            cur.execute(
                "INSERT INTO cart_item(cart_id, product_id, quantity) "
                "VALUES (?, ?, ?)",
                (cart_id, product_id, quantity),
            )

    conn.commit()


def main():
    os.makedirs(os.path.dirname(RUTA_DB_C), exist_ok=True)
    conn = sqlite3.connect(RUTA_DB_C)

    # 1) Crear y poblar el Modelo B dentro de tienda_modelo_c.db
    crear_tablas_b(conn)
    fabricantes, colores, categorias, df_productos = construir_dimensiones_y_productos()
    map_manufacturer, map_color, map_category = poblar_dimensiones(
        conn, fabricantes, colores, categorias
    )
    poblar_productos(conn, df_productos, map_manufacturer, map_color, map_category)

    # 2) Crear tablas extra de e-commerce (tu Modelo C extendido)
    crear_tablas_extra(conn)

    # 3) Generar datos de ejemplo
    generar_clientes(conn)
    inicializar_inventario(conn)
    generar_pedidos_ejemplo(conn, 3)
    generar_carritos(conn)

    conn.close()
    print("Modelo C creado en tienda_modelo_c.db")


if __name__ == "__main__":
    main()
