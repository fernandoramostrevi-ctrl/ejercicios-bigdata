-- Ejercicio 2.1: Contar productos por categoría
-- Cuenta cuántos productos hay en cada categoría,
-- incluyendo también las categorías sin productos asociados.
SELECT
    c.name AS category_name,             -- Nombre de la categoría
    COUNT(p.id) AS product_count         -- Número de productos en esa categoría
FROM category AS c                       -- Lista de todas las categorías
LEFT JOIN product AS p                   -- Relación opcional con productos
    ON p.category_id = c.id
GROUP BY
    c.id,                                -- Agrupa por id de categoría
    c.name                               -- y por su nombre
ORDER BY
    product_count DESC,                  -- Categorías con más productos primero
    category_name ASC;                   -- Desempata alfabéticamente por nombre
