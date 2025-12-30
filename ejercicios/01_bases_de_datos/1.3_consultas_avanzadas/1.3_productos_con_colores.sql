-- Ejercicio 1.3: Productos con colores
-- Muestra cada producto junto con la lista de colores asociados,
-- concatenados en una sola columna usando GROUP_CONCAT.
-- Nota: en este modelo cada producto tiene como máximo un color (color_id),
-- por lo que la lista suele contener un único valor por producto.
SELECT
    p.name AS product_name,                        -- Nombre del producto
    GROUP_CONCAT(col.name, ', ') AS colors         -- Colores asociados al producto (lista separada por comas)
FROM product AS p                                  -- Tabla principal de productos
LEFT JOIN color AS col                             -- Relaciona cada producto con su color
    ON p.color_id = col.id
GROUP BY
    p.id,                                          -- Agrupa por el identificador del producto
    p.name                                         -- y por su nombre para obtener una fila por producto
ORDER BY
    p.name ASC;                                    -- Ordena los productos alfabéticamente
