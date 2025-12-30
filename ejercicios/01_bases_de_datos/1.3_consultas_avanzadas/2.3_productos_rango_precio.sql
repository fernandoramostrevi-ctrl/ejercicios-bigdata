-- Ejercicio 2.3: Productos por rango de precio
-- Clasifica los productos en rangos Económico, Medio y Premium
-- y calcula cuántos productos hay en cada rango y su precio medio.

SELECT
    CASE
        WHEN p.price < 100 THEN 'Economico'        -- Productos baratos
        WHEN p.price < 300 THEN 'Medio'            -- Rango intermedio
        ELSE 'Premium'                             -- Productos de gama alta
    END AS price_range,                            -- Nombre del rango de precio
    COUNT(*) AS product_count,                     -- Número de productos en el rango
    AVG(p.price) AS avg_price                      -- Precio medio dentro del rango
FROM product AS p                                  -- Tabla principal de productos
WHERE p.price IS NOT NULL                          -- Solo productos con precio conocido
GROUP BY
    price_range                                    -- Agrupa por el rango calculado con CASE
ORDER BY
    CASE price_range                               -- Orden lógico de los rangos
        WHEN 'Economico' THEN 1
        WHEN 'Medio' THEN 2
        WHEN 'Premium' THEN 3
    END;
