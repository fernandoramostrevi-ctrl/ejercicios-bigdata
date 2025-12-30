import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data', 'raw')

def load_all():
    oficina = pd.read_csv(os.path.join(DATA_DIR, "oficina.csv"))
    empleado = pd.read_csv(os.path.join(DATA_DIR, "empleado.csv"))
    gama = pd.read_csv(os.path.join(DATA_DIR, "gama_producto.csv"))
    producto = pd.read_csv(os.path.join(DATA_DIR, "producto.csv"))
    cliente = pd.read_csv(os.path.join(DATA_DIR, "cliente.csv"))
    pedido = pd.read_csv(os.path.join(DATA_DIR, "pedido.csv"), parse_dates=["fecha_pedido","fecha_esperada","fecha_entrega"])
    detalle = pd.read_csv(os.path.join(DATA_DIR, "detalle_pedido.csv"))
    pago = pd.read_csv(os.path.join(DATA_DIR, "pago.csv"), parse_dates=["fecha_pago"])
    return oficina, empleado, gama, producto, cliente, pedido, detalle, pago
# Este script cargará y procesará los datos.
