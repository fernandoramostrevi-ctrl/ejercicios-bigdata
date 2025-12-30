-- Ejercicio 3.3: Análisis de inventario
-- Muestra los productos con stock crítico (stock < min_stock),
-- incluyendo categoría y valor del stock faltante.

SELECT
    p.id AS product_id,                                  -- Identificador del producto
    p.name AS product_name,                              -- Nombre del producto
    c.name AS category_name,                             -- Categoría del producto
    i.stock,                                             -- Stock actual
    i.min_stock,                                         -- Stock mínimo deseado
    (i.min_stock - i.stock) AS missing_units,            -- Unidades que faltan para alcanzar el mínimo
    p.price,                                             -- Precio unitario del producto
    (i.min_stock - i.stock) * p.price AS missing_value,  -- Valor económico del stock faltante
    i.location,                                          -- Ubicación en almacén
    i.last_update                                        -- Fecha de última actualización de inventario
FROM inventory AS i                                      -- Tabla de inventario
INNER JOIN product AS p                                  -- Relaciona inventario con producto
    ON i.product_id = p.id
LEFT JOIN category AS c                                  -- Categoría del producto (opcional)
    ON p.category_id = c.id
WHERE
    i.stock < i.min_stock                                -- Solo productos en situación crítica
    AND p.price IS NOT NULL                              -- Requiere precio para calcular valor faltante
ORDER BY
    missing_value DESC,                                  -- Primero los que más valor faltante acumulan
    missing_units DESC;                                  -- Desempata por unidades que faltan
