-- Ejercicio 1.2: Productos con fabricante y categoría
SELECT
    m.name AS manufacturer_name,   -- Nombre del fabricante
    c.name AS category_name,       -- Nombre de la categoría del producto
    p.name AS product_name,        -- Nombre del producto
    p.price                        -- Precio del producto
FROM product AS p                  -- Tabla principal de productos
INNER JOIN manufacturer AS m       -- Relaciona cada producto con su fabricante
    ON p.manufacturer_id = m.id
INNER JOIN category AS c           -- Relaciona cada producto con su categoría
    ON p.category_id = c.id
WHERE p.price > 200                -- Solo productos de precio superior a 200
ORDER BY
    m.name ASC,                    -- Ordena primero por fabricante (A-Z)
    c.name ASC,                    -- Luego por categoría (A-Z)
    p.price DESC;                  -- Dentro de cada grupo, del más caro al más barato
