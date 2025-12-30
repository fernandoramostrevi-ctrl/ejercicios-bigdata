-- Ejercicio 1.4: Top productos por fabricante
-- Muestra, para cada fabricante, el producto más caro (price máximo).
-- Usa una window function (ROW_NUMBER) para seleccionar el top 1 por fabricante.

WITH products_ranked AS (
    SELECT
        m.name AS manufacturer_name,      -- Nombre del fabricante
        p.name AS product_name,           -- Nombre del producto
        p.price,                          -- Precio del producto
        ROW_NUMBER() OVER (
            PARTITION BY m.id             -- Re-inicia la numeración por cada fabricante
            ORDER BY p.price DESC         -- Ordena de más caro a más barato dentro de cada fabricante
        ) AS rn
    FROM product AS p                     -- Tabla principal de productos
    INNER JOIN manufacturer AS m          -- Relaciona cada producto con su fabricante
        ON p.manufacturer_id = m.id
    WHERE p.price IS NOT NULL             -- Ignora productos sin precio
)
SELECT
    manufacturer_name,                    -- Nombre del fabricante
    product_name,                         -- Nombre del producto más caro
    price                                 -- Precio del producto más caro
FROM products_ranked
WHERE rn = 1                              -- Se queda solo con el producto nº1 (más caro) por fabricante
ORDER BY
    manufacturer_name ASC;                -- Ordena fabricantes alfabéticamente
