-- Ejercicio 2.2: Estadísticas de precios por fabricante
-- Calcula número de productos, precio medio, mínimo y máximo
-- para cada fabricante, considerando solo productos con price no nulo
-- y filtrando fabricantes con más de 10 productos.

SELECT
    m.name AS manufacturer_name,              -- Nombre del fabricante
    COUNT(p.id) AS product_count,             -- Número de productos con precio
    AVG(p.price) AS avg_price,                -- Precio medio
    MIN(p.price) AS min_price,                -- Precio mínimo
    MAX(p.price) AS max_price                 -- Precio máximo
FROM manufacturer AS m                        -- Tabla de fabricantes
INNER JOIN product AS p                       -- Productos asociados a cada fabricante
    ON p.manufacturer_id = m.id
WHERE p.price IS NOT NULL                     -- Ignora productos sin precio
GROUP BY
    m.id,
    m.name
HAVING
    COUNT(p.id) > 10                          -- Solo fabricantes con más de 10 productos
ORDER BY
    product_count DESC,                       -- Los fabricantes más “grandes” primero
    manufacturer_name ASC;                    -- Desempata por nombre de fabricante
