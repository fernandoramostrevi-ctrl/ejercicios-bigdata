-- Ejercicio 1.1: Productos con su categoría
-- Muestra el nombre del producto, la categoría y el precio.
-- Nota: muchos productos no tienen price asignado (NULL),
-- por eso pueden aparecer numerosos valores NULL en la columna price.
SELECT
    p.name  AS product_name,       -- Nombre del producto
    c.name  AS category_name,      -- Nombre de la categoría del producto
    p.price AS price               -- Precio del producto (puede ser NULL)
FROM product AS p                  -- Tabla principal de productos
INNER JOIN category AS c           -- Relaciona cada producto con su categoría
    ON p.category_id = c.id
ORDER BY
    c.name ASC,                    -- Ordena primero por categoría (A-Z)
    p.price ASC;                   -- Dentro de cada categoría, del más barato al más caro
