# ANÁLISIS_DATOS.md

## 1. Resumen Ejecutivo

El conjunto de datos analizado está formado por archivos CSV, cada uno correspondiente a una categoría distinta de componentes de una tienda de informática (CPU, placas base, memorias RAM, discos, tarjetas gráficas, periféricos, etc.).  

En total, los archivos contienen 56.454 registros de productos (suma de las filas de todos los CSV), lo que representa un catálogo técnico amplio y variado de hardware.  

Las categorías diferentes coinciden con los nombres base de los archivos (sin la extensión `.csv`), dando lugar a 25 categorías, entre las que destacan: `cpu`, `motherboard`, `memory`, `internal-hard-drive`, `external-hard-drive`, `video-card`, `power-supply`, `case`, `keyboard`, `mouse`, `monitor`, `speakers`, `headphones`, `webcam`, `wired-network-card`, `wireless-network-card`, `os`, `sound-card`, `cpu-cooler`, `case-fan`, `case-accessory`, `fan-controller`, `optical-drive` y `ups`.  

## 2. Análisis de Estructura

El análisis exploratorio muestra que las únicas columnas realmente comunes a prácticamente todos los CSV son **`name`** (nombre del producto) y **`price`** (precio del producto). El resto de columnas son específicas de cada tipo de componente y describen características técnicas propias de cada categoría.  

Por ejemplo, en `cpu.csv` aparecen campos como `core_count`, `core_clock`, `boost_clock`, `tdp`, `graphics` y `smt`; en `motherboard.csv` encontramos `socket`, `form_factor`, `max_memory`, `memory_slots` y `color`; en `memory.csv` aparecen `speed`, `modules`, `price_per_gb`, `first_word_latency` y `cas_latency`. Los discos (`internal-hard-drive.csv` y `external-hard-drive.csv`) incluyen `capacity`, `type`, `form_factor`, `interface` y `cache`, mientras que las tarjetas gráficas (`video-card.csv`) tienen `chipset`, `vram`, `length`, `tdp` e `interface`, y las fuentes de alimentación (`power-supply.csv`) incluyen `wattage`, `efficiency_rating`, `modular` y `type`.  

Aunque cada archivo tiene su propia estructura, el patrón general es claro: cada CSV representa una **categoría de producto** con sus atributos técnicos específicos, manteniendo solo `name` y `price` como nexo común en todo el catálogo.

### Tabla resumen: nombre de archivo → número de filas


| Archivo (categoría)          | Filas |
| Archivo               | Filas |
|-----------------------|-------|
| case                  | 340   |
| case-accessory        | 133   |
| case-fan              | 65    |
| cpu                   | 5.811 |
| cpu-cooler            | 683   |
| external-hard-drive   | 149   |
| fan-controller        | 268   |
| headphones            | 77    |
| internal-hard-drive   | 2.805 |
| keyboard              | 62    |
| memory                | 227   |
| monitor               | 2.355 |
| motherboard           | 4.358 |
| mouse                 | 4.216 |
| optical-drive         | 11.734|
| os                    | 2.970 |
| power-supply          | 5.705 |
| sound-card            | 2.746 |
| speakers              | 37    |
| thermal-paste         | 519   |
| ups                   | 1.353 |
| video-card            | 2.166 |
| webcam                | 5.486 |
| wired-network-card    | 2.181 |
| wireless-network-card | 8     |


## 3. Análisis de Calidad

El EDA muestra que sí existen valores nulos, pero se concentran principalmente en columnas opcionales o muy específicas, como `color` y algunas especificaciones técnicas avanzadas que no aplican a todos los modelos. El número de nulos por columna es, en general, reducido y razonable para un catálogo de productos; solo en ciertos campos muy concretos el porcentaje de nulos es elevado, lo que indica información opcional más que errores sistemáticos.  

En cuanto a duplicados, el recuento de filas completamente duplicadas por archivo es bajo o nulo. En la práctica, cada fila representa un producto distinto; los pocos duplicados detectados pueden deberse a variantes casi idénticas o a pequeñas inconsistencias de la fuente original, pero no afectan de forma significativa al análisis global.  

Respecto a los precios, los valores mínimos, máximos y medios obtenidos en las columnas numéricas indican que no hay precios negativos y que los rangos son coherentes con el mercado de hardware: componentes de entrada con precios bajos, gamas medias razonables y productos de gama alta con precios elevados pero verosímiles. En un entorno productivo podría revisarse el tratamiento de precios igual a 0 o extremadamente altos, pero para los objetivos del ejercicio la calidad de los precios es aceptable.

## 4. Identificación de Entidades

A partir de los nombres de archivo y de los atributos observados se identifican claramente varias entidades de negocio:

- Fabricantes: analizando el primer término de la columna `name` aparecen fabricantes habituales como Intel, AMD, Nvidia, Asus, MSI, Gigabyte, ASRock, Corsair, Kingston, G.Skill, Crucial, Seagate, Western Digital, Samsung, entre otros. Esto sugiere la existencia de una entidad conceptual “Fabricante” o, como mínimo, de un atributo `fabricante` relevante dentro de cada categoría.  
- Colores: en las columnas `color` (cuando existen) se encuentran valores como Black, White, Red, Blue, Silver, RGB y combinaciones similares. Estos atributos son especialmente relevantes para cajas, ventiladores, memorias con iluminación y otros componentes estéticos.  
- Categorías: las categorías se corresponden directamente con los nombres de archivo (`cpu`, `motherboard`, `memory`, `internal-hard-drive`, `external-hard-drive`, `video-card`, `power-supply`, `case`, `keyboard`, `mouse`, `monitor`, `speakers`, `headphones`, `webcam`, `wired-network-card`, `wireless-network-card`, `os`, `sound-card`, `cpu-cooler`, `case-fan`, `case-accessory`, `fan-controller`, `optical-drive`, `ups`, etc.), que representan tipos de productos diferenciados dentro del catálogo.

Estas observaciones permiten derivar un conjunto claro de entidades para un modelo de datos más estructurado.

Diagrama E‑R del Modelo A: [ver diagrama en dbdiagram] https://dbdiagram.io/d/Modelo_a-69419db06167ba74147c530b

## 5. Conclusiones para el Diseño del Modelo B

A partir del análisis estructural y de calidad, y del significado funcional de los datos, se proponen como entidades principales del Modelo B (núcleo del PC):

- `CPU`  
- `Motherboard`  
- `Memory` (RAM)  
- `Storage` (discos y SSD, internos y externos, según se quiera unificar o separar)  
- `VideoCard` (tarjetas gráficas)  
- `PowerSupply` (fuentes de alimentación)  
- `Case` (cajas de PC)  

Además, se pueden mantener como entidades adicionales los **periféricos** (`Keyboard`, `Mouse`, `Monitor`, `Speakers`, `Headphones`, `Webcam`) y otros componentes (`SoundCard`, `NetworkCard`, `OpticalDrive`, `UPS`, `CaseAccessory`, `CaseFan`, `FanController`), dependiendo del alcance que se quiera dar al diseño lógico.

Las principales relaciones entre estas entidades se basan en atributos de compatibilidad identificados en el EDA:

- `CPU` ↔ `Motherboard` mediante el atributo `socket`.  
- `Motherboard` ↔ `Memory` mediante el tipo de memoria soportado (`memory_type`) y el número de `memory_slots`.  
- `Motherboard` ↔ `Storage` mediante la `interface` (SATA, M.2/PCIe) y el `form_factor`.  
- `Motherboard` ↔ `VideoCard` mediante la interfaz PCIe (`interface` / `pcie_version`).  
- `Case` ↔ `Motherboard` mediante el `form_factor` físico (ATX, Micro-ATX, Mini-ITX, etc.).  
- `Case` ↔ `PowerSupply` mediante el `psu_form_factor` (ATX, SFX, etc.).  

Estas relaciones permiten construir un Modelo B en el que la compatibilidad entre componentes pueda consultarse de forma natural mediante claves foráneas y joins.

Por último, se justifica que el Modelo A, aunque muy simple de construir (una tabla por CSV, sin decisiones de normalización), resulta **ineficiente** desde el punto de vista relacional:

- Genera 25 tablas desconectadas entre sí, sin claves primarias ni foráneas explícitas.  
- Duplica información común (por ejemplo `name` y `price` en todas las tablas) y obliga a reconstruir las relaciones lógicas a partir de coincidencias de texto o columnas compartidas.  
- Complica las consultas de negocio, especialmente las que requieren analizar compatibilidad entre componentes (CPU–placa–RAM–GPU–caja–fuente).  

El Modelo B busca solucionar estas limitaciones agrupando los datos en un conjunto más pequeño de entidades bien definidas, introduciendo claves y relaciones explícitas, y basando el diseño en la estructura y patrones descubiertos durante el análisis exploratorio de datos.

## 6. Síntesis del Modelo B (Normalizado)

A partir del análisis exploratorio y del Modelo A se ha construido un Modelo B con una base de datos `tienda_modelo_b.db` más normalizada. En este modelo se introducen tablas de dimensión para fabricantes (`manufacturer`), colores (`color`) y categorías (`category`), así como una tabla central de productos (`product`) que referencia a estas mediante claves foráneas.  

Además, se han creado tablas específicas para algunos tipos de componentes (por ejemplo `cpu`, `motherboard`, `memory`, `storage`), cada una relacionada 1:1 con `product`. Esto reduce la redundancia, permite reutilizar fabricantes y colores entre distintas categorías y facilita las consultas de catálogo (por ejemplo, listar todos los productos de un fabricante o todas las categorías disponibles).


Diagrama E‑R del Modelo B: [ver diagrama en dbdiagram](https://dbdiagram.io/d/Modelo_b-6941b9826167ba74147eafbd)

## 7. Síntesis del Modelo C (E‑Commerce Completo)

El Modelo C extiende el Modelo B para simular un sistema de e‑commerce. La base de datos `tienda_modelo_c.db` añade tablas de clientes (`customer`), pedidos (`order`), líneas de pedido (`order_item`) e inventario (`inventory`). Los clientes se relacionan con sus pedidos, los pedidos con los productos del catálogo, y cada producto tiene un nivel de stock asociado.  

Sobre este modelo se han generado datos de ejemplo: varios clientes ficticios, unos cuantos pedidos con diferentes productos y cantidades, y un inventario inicial con existencias aleatorias entre 50 y 200 unidades por producto. Esto permite probar consultas típicas de negocio, como el recuento de clientes, el número de pedidos o la distribución del stock, y muestra cómo el catálogo técnico de componentes puede integrarse en un flujo completo de ventas.

Diagrama E‑R del Modelo C: [ver diagrama en dbdiagram](https://dbdiagram.io/d/Modelo_c-6941b9f46167ba74147eb723)
