import os
import pandas as pd

RUTA_CSV = r"C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\datos\csv_tienda_informatica\csv_tienda_informatica"
RUTA_RESUMEN = r"C:\Users\Tucanae Ramos\PycharmProjects\ejercicios-bigdata\ejercicios\01_bases_de_datos\1.1_introduccion_sqlite\EDA\resumen_eda.md"


def extraer_fabricante(name: str) -> str:
    # muy simple: primer token del nombre
    if not isinstance(name, str) or not name.strip():
        return ""
    return name.split()[0]


def extraer_colores_serie(serie: pd.Series) -> set:
    colores = set()
    for v in serie.dropna().astype(str):
        colores.add(v.strip())
    return colores


def analizar_archivo(ruta_fichero, nombre_archivo):
    print(f"\n=== Análisis de {nombre_archivo} ===")

    df = pd.read_csv(ruta_fichero)

    filas, columnas = df.shape
    print(f"Filas: {filas}, Columnas: {columnas}")
    print("Columnas y tipos:")
    print(df.dtypes)

    print("\nPrimeras 3 filas:")
    print(df.head(3))

    # Calidad de datos
    print("\nValores nulos por columna:")
    nulos_abs = df.isna().sum()
    nulos_pct = (nulos_abs / len(df) * 100).round(2)
    print(pd.concat([nulos_abs.rename("nulos"), nulos_pct.rename("pct_nulos")], axis=1))

    print("\nFilas duplicadas (completas):")
    print(df.duplicated().sum())

    # Rangos numéricos (precio y otros numéricos)
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) > 0:
        print("\nResumen numérico:")
        print(df[num_cols].agg(["min", "max", "mean"]))
    else:
        print("\n(No hay columnas numéricas)")

    # Valores únicos categóricos
    print("\nValores únicos por columna categórica (resumen):")
    cat_cols = df.select_dtypes(exclude="number").columns
    for col in cat_cols:
        uniques = df[col].dropna().unique()
        print(f"- {col}: {len(uniques)} valores únicos")

    # Patrones: fabricantes y colores
    fabricantes = set()
    colores = set()

    if "name" in df.columns:
        fabricantes = {extraer_fabricante(n) for n in df["name"].dropna()}
        fabricantes.discard("")
        print(f"\nFabricantes (estimados a partir de 'name'): {len(fabricantes)} ejemplos:")
        print(list(sorted(fabricantes))[:10])

    if "color" in df.columns:
        colores = extraer_colores_serie(df["color"])
        print(f"\nColores detectados: {len(colores)}")
        print(list(sorted(colores)))

    info_archivo = {
        "nombre": nombre_archivo,
        "filas": filas,
        "columnas": columnas,
        "columnas_lista": list(df.columns),
        "tipos": df.dtypes.astype(str).to_dict(),
        "nulos_abs": nulos_abs.to_dict(),
        "nulos_pct": nulos_pct.to_dict(),
        "num_cols": list(num_cols),
        "cat_cols": list(cat_cols),
        "fabricantes": sorted(fabricantes),
        "colores": sorted(colores),
    }

    return info_archivo


def main():
    os.makedirs(os.path.dirname(RUTA_RESUMEN), exist_ok=True)

    archivos_csv = [
        f for f in os.listdir(RUTA_CSV)
        if f.lower().endswith(".csv")
    ]

    resumen = []
    columnas_por_archivo = {}

    for nombre_csv in sorted(archivos_csv):
        ruta_fichero = os.path.join(RUTA_CSV, nombre_csv)
        info = analizar_archivo(ruta_fichero, nombre_csv)
        resumen.append(info)
        columnas_por_archivo[nombre_csv] = set(info["columnas_lista"])

    # Columnas comunes entre todos los CSV
    if columnas_por_archivo:
        columnas_comunes = set.intersection(*columnas_por_archivo.values())
    else:
        columnas_comunes = set()

    # Categorías basadas en nombres de archivo
    categorias = sorted({os.path.splitext(f)[0] for f in archivos_csv})

    # Generar markdown
    lineas = []
    lineas.append("# Resumen EDA tienda informática\n")
    lineas.append(f"Archivos analizados: {len(resumen)}\n")

    lineas.append("## Columnas comunes entre todos los CSV\n")
    lineas.append(", ".join(sorted(columnas_comunes)) or "_Ninguna columna común en todos los archivos_")
    lineas.append("\n")

    lineas.append("## Categorías (basadas en nombres de archivo)\n")
    for cat in categorias:
        lineas.append(f"- {cat}")
    lineas.append("\n")

    lineas.append("## Resumen por archivo\n")
    for info in resumen:
        lineas.append(f"### {info['nombre']}\n")
        lineas.append(f"- Filas: {info['filas']}, Columnas: {info['columnas']}")
        lineas.append(f"- Columnas: {', '.join(info['columnas_lista'])}")
        lineas.append(f"- Columnas numéricas: {', '.join(info['num_cols']) or '_Ninguna_'}")
        lineas.append(f"- Columnas categóricas: {', '.join(info['cat_cols']) or '_Ninguna_'}")

        if info["fabricantes"]:
            lineas.append(f"- Fabricantes detectados (ejemplos): {', '.join(info['fabricantes'][:10])}")
        if info["colores"]:
            lineas.append(f"- Colores detectados: {', '.join(info['colores'])}")

        lineas.append("")

    with open(RUTA_RESUMEN, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"\nResumen EDA guardado en: {RUTA_RESUMEN}")


if __name__ == "__main__":
    main()
