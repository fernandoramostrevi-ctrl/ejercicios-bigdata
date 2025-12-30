-- Ejercicio 1.5: Productos sin color asignado
-- Cuenta cuántos productos NO tienen color asociado (color_id nulo).
SELECT
    COUNT(*) AS products_without_color   -- Número total de productos sin color
FROM product AS p                        -- Tabla principal de productos
LEFT JOIN color AS col                   -- Relación opcional con la tabla de colores
    ON p.color_id = col.id
WHERE p.color_id IS NULL;                -- Filtra solo productos sin color asignado
