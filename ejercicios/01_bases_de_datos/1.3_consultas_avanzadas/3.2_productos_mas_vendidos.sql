-- Ejercicio 3.2: Productos más vendidos
-- Calcula la cantidad total vendida por producto,
-- incluyendo el fabricante y la categoría, y muestra el top 20.

SELECT
    p.id AS product_id,                           -- Identificador del producto
    p.name AS product_name,                       -- Nombre del producto
    m.name AS manufacturer_name,                  -- Nombre del fabricante
    c.name AS category_name,                      -- Nombre de la categoría
    SUM(oi.quantity) AS total_quantity_sold,      -- Unidades totales vendidas
    SUM(oi.quantity * oi.unit_price) AS total_revenue  -- Ingresos totales por producto
FROM order_item AS oi                             -- Líneas de pedido (detalle de ventas)
INNER JOIN product AS p                           -- Relaciona cada línea con su producto
    ON oi.product_id = p.id
LEFT JOIN manufacturer AS m                       -- Fabricante del producto (opcional si falta)
    ON p.manufacturer_id = m.id
LEFT JOIN category AS c                           -- Categoría del producto (opcional si falta)
    ON p.category_id = c.id
GROUP BY
    p.id,
    p.name,
    m.name,
    c.name
HAVING
    SUM(oi.quantity) > 0                          -- Solo productos que se han vendido al menos una unidad
ORDER BY
    total_quantity_sold DESC,                     -- Ordena por unidades vendidas (más vendidos primero)
    total_revenue DESC                            -- Desempata por ingresos totales
LIMIT 20;                                         -- Top 20 productos
