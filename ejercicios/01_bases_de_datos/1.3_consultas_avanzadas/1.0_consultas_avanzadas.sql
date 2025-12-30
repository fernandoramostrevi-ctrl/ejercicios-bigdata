-- Ejercicio 1.1: Productos con su categoría
-- Muestra el nombre del producto, la categoría y el precio.
-- Nota: en este dataset muchos productos no tienen precio asignado,
-- por eso aparecen numerosos valores NULL en la columna price.
SELECT
    p.name  AS product_name,
    c.name  AS category_name,
    p.price AS price
FROM product AS p
INNER JOIN category AS c
    ON p.category_id = c.id
ORDER BY
    c.name ASC,
    p.price ASC;

-- (Opcional para análisis) Solo productos con precio informado
-- SELECT
--     p.name  AS product_name,
--     c.name  AS category_name,
--     p.price AS price
-- FROM product AS p
-- INNER JOIN category AS c
--     ON p.category_id = c.id
-- WHERE p.price IS NOT NULL
-- ORDER BY
--     c.name ASC,
--     p.price ASC;
-- Ejercicio 1.2: Productos con fabricante y categoría
-- Muestra fabricante, categoría, producto y precio
-- solo para productos con price > 200.
SELECT
    m.name AS manufacturer_name,
    c.name AS category_name,
    p.name AS product_name,
    p.price
FROM product AS p
INNER JOIN manufacturer AS m
    ON p.manufacturer_id = m.id
INNER JOIN category AS c
    ON p.category_id = c.id
WHERE p.price > 200
ORDER BY
    m.name ASC,
    c.name ASC,
    p.price DESC;
