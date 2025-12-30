-- Ejercicio 2.4: Colores más populares
-- Cuenta cuántos productos están asociados a cada color
-- y muestra los 10 colores con más productos.

SELECT
    col.name AS color_name,                -- Nombre del color
    COUNT(p.id) AS product_count           -- Número de productos con ese color
FROM color AS col                          -- Tabla de colores
LEFT JOIN product AS p                     -- Relación opcional con productos
    ON p.color_id = col.id
GROUP BY
    col.id,
    col.name
ORDER BY
    product_count DESC,                    -- Colores con más productos primero
    color_name ASC                         -- Desempata por nombre
LIMIT 10;                                  -- Solo el top 10 de colores
