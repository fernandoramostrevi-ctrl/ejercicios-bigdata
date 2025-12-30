import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
from faker import Faker

fake = Faker('es_ES')
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data', 'raw')
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------
# Parámetros de volumen
# -------------------------
N_OFICINAS = 8
N_EMPLEADOS = 60
N_GAMAS = 6
N_PRODUCTOS = 400
N_CLIENTES = 800
N_PEDIDOS = 6000
MEDIA_LINEAS_POR_PEDIDO = 4
N_PAGOS = 2500

# Rango de fechas
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)

def random_date(start, end, n=1):
    delta = (end - start).days
    days = np.random.randint(0, delta + 1, n)
    return [start + timedelta(int(d)) for d in days]

# -------------------------
# Tabla oficina
# -------------------------
def generar_oficinas():
    ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Lisboa", "París", "Roma"]
    paises = ["España", "España", "España", "España", "España", "Portugal", "Francia", "Italia"]
    oficinas = []

    for i in range(N_OFICINAS):
        oficinas.append({
            "codigo_oficina": f"OF-{i+1:03d}",
            "ciudad": ciudades[i % len(ciudades)],
            "pais": paises[i % len(paises)],
            "region": fake.state(),
            "codigo_postal": fake.postcode(),
            "telefono": fake.phone_number(),
            "linea_direccion1": fake.street_address(),
            "linea_direccion2": fake.secondary_address() if np.random.rand() < 0.3 else None
        })
    df = pd.DataFrame(oficinas)
    df.to_csv(os.path.join(DATA_DIR, "oficina.csv"), index=False)
    return df

# -------------------------
# Tabla empleado
# -------------------------
def generar_empleados(oficinas):
    empleados = []
    puestos = ["Representante Ventas", "Gerente Oficina", "Soporte", "Director Regional"]

    for i in range(N_EMPLEADOS):
        cod_emp = i + 1
        empleados.append({
            "codigo_empleado": cod_emp,
            "nombre": fake.first_name(),
            "apellido1": fake.last_name(),
            "apellido2": fake.last_name() if np.random.rand() < 0.6 else None,
            "extension": str(np.random.randint(100, 999)),
            "email": fake.email(),
            "codigo_oficina": np.random.choice(oficinas["codigo_oficina"]),
            "codigo_jefe": np.random.choice(range(1, cod_emp)) if cod_emp > 1 and np.random.rand() < 0.8 else None,
            "puesto": np.random.choice(puestos)
        })
    df = pd.DataFrame(empleados)
    df.to_csv(os.path.join(DATA_DIR, "empleado.csv"), index=False)
    return df

# -------------------------
# Tabla gama_producto
# -------------------------
def generar_gamas():
    gamas = ["Herramientas", "Plantas", "Riego", "Abonos", "Decoración", "Maquinaria"]
    registros = []
    for g in gamas[:N_GAMAS]:
        registros.append({
            "gama": g,
            "descripcion_texto": f"Gama de productos de {g.lower()}",
            "descripcion_html": f"<p>Gama de productos de {g.lower()}</p>",
            "imagen": f"/img/{g.lower()}.png"
        })
    df = pd.DataFrame(registros)
    df.to_csv(os.path.join(DATA_DIR, "gama_producto.csv"), index=False)
    return df

# -------------------------
# Tabla producto
# -------------------------
def generar_productos(gamas):
    productos = []
    for i in range(N_PRODUCTOS):
        gama = np.random.choice(gamas["gama"])
        precio_proveedor = np.round(np.random.uniform(2, 80), 2)
        margen = np.random.uniform(1.1, 1.8)
        precio_venta = np.round(precio_proveedor * margen, 2)

        productos.append({
            "codigo_producto": f"P-{i+1:05d}",
            "nombre": f"Producto {i+1}",
            "gama": gama,
            "dimensiones": f"{np.random.randint(5,100)}x{np.random.randint(5,100)}x{np.random.randint(5,100)}",
            "proveedor": fake.company(),
            "descripcion": fake.sentence(nb_words=8),
            "cantidad_en_stock": np.random.randint(0, 1000),
            "precio_venta": precio_venta,
            "precio_proveedor": precio_proveedor
        })
    df = pd.DataFrame(productos)
    df.to_csv(os.path.join(DATA_DIR, "producto.csv"), index=False)
    return df

# -------------------------
# Tabla cliente
# -------------------------
def generar_clientes(empleados):
    clientes = []
    for i in range(N_CLIENTES):
        clientes.append({
            "codigo_cliente": i + 1,
            "nombre_cliente": fake.company(),
            "nombre_contacto": fake.first_name() if np.random.rand() < 0.9 else None,
            "apellido_contacto": fake.last_name() if np.random.rand() < 0.9 else None,
            "telefono": fake.phone_number(),
            "fax": fake.phone_number(),
            "linea_direccion1": fake.street_address(),
            "linea_direccion2": fake.secondary_address() if np.random.rand() < 0.3 else None,
            "ciudad": fake.city(),
            "region": fake.state() if np.random.rand() < 0.5 else None,
            "pais": fake.country(),
            "codigo_postal": fake.postcode() if np.random.rand() < 0.8 else None,
            "codigo_empleado_rep_ventas": int(np.random.choice(empleados["codigo_empleado"])),
            "limite_credito": np.round(np.random.uniform(1000, 20000), 2)
        })
    df = pd.DataFrame(clientes)
    df.to_csv(os.path.join(DATA_DIR, "cliente.csv"), index=False)
    return df

# -------------------------
# Tabla pedido
# -------------------------
def generar_pedidos(clientes):
    pedidos = []
    fechas_pedido = random_date(START_DATE, END_DATE, N_PEDIDOS)

    estados_posibles = ["Entregado", "Pendiente", "Cancelado", "Rechazado"]

    for i in range(N_PEDIDOS):
        fecha_p = fechas_pedido[i]
        delta_esp = np.random.randint(2, 15)
        fecha_esp = fecha_p + timedelta(days=delta_esp)

        estado = np.random.choice(estados_posibles, p=[0.7, 0.2, 0.05, 0.05])
        if estado == "Entregado":
            fecha_ent = fecha_esp + timedelta(days=np.random.randint(-2, 7))
        elif estado == "Pendiente":
            fecha_ent = None
        else:
            fecha_ent = None

        pedidos.append({
            "codigo_pedido": i + 1,
            "fecha_pedido": fecha_p.date(),
            "fecha_esperada": fecha_esp.date(),
            "fecha_entrega": fecha_ent.date() if fecha_ent else None,
            "estado": estado,
            "comentarios": fake.sentence(nb_words=6) if np.random.rand() < 0.3 else None,
            "codigo_cliente": int(np.random.choice(clientes["codigo_cliente"]))
        })
    df = pd.DataFrame(pedidos)
    df.to_csv(os.path.join(DATA_DIR, "pedido.csv"), index=False)
    return df

# -------------------------
# Tabla detalle_pedido
# -------------------------
def generar_detalle_pedido(pedidos, productos):
    detalles = []
    codigos_productos = productos["codigo_producto"].values
    precios_dict = productos.set_index("codigo_producto")["precio_venta"].to_dict()

    for _, row in pedidos.iterrows():
        n_lineas = max(1, int(np.random.poisson(MEDIA_LINEAS_POR_PEDIDO)))
        productos_pedido = np.random.choice(codigos_productos, size=n_lineas, replace=False)

        for idx, cod_prod in enumerate(productos_pedido, start=1):
            cantidad = np.random.randint(1, 20)
            precio_unidad = float(precios_dict[cod_prod] * np.random.uniform(0.9, 1.05))

            detalles.append({
                "codigo_pedido": row["codigo_pedido"],
                "codigo_producto": cod_prod,
                "cantidad": cantidad,
                "precio_unidad": round(precio_unidad, 2),
                "numero_linea": idx
            })

    df = pd.DataFrame(detalles)
    df.to_csv(os.path.join(DATA_DIR, "detalle_pedido.csv"), index=False)
    return df

# -------------------------
# Tabla pago
# -------------------------
def generar_pagos(clientes):
    pagos = []
    fechas = random_date(START_DATE, END_DATE, N_PAGOS)
    formas_pago = ["Tarjeta", "Transferencia", "Paypal", "Efectivo"]

    for i in range(N_PAGOS):
        pagos.append({
            "codigo_cliente": int(np.random.choice(clientes["codigo_cliente"])),
            "forma_pago": np.random.choice(formas_pago),
            "id_transaccion": f"TRX-{i+1:06d}",
            "fecha_pago": fechas[i].date(),
            "total": np.round(np.random.uniform(50, 3000), 2)
        })
    df = pd.DataFrame(pagos)
    df.to_csv(os.path.join(DATA_DIR, "pago.csv"), index=False)
    return df

if __name__ == "__main__":
    oficinas = generar_oficinas()
    empleados = generar_empleados(oficinas)
    gamas = generar_gamas()
    productos = generar_productos(gamas)
    clientes = generar_clientes(empleados)
    pedidos = generar_pedidos(clientes)
    detalle = generar_detalle_pedido(pedidos, productos)
    pagos = generar_pagos(clientes)
    print("CSV generados en data/raw")
# Este script generará datos sintéticos para el análisis.
