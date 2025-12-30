-- Ejercicio 2.5: Fabricantes con productos en múltiples categorías
-- Cuenta cuántas categorías distintas tiene cada fabricante
-- y muestra solo aquellos con productos en 2 o más categorías.

SELECT
    m.name AS manufacturer_name,                -- Nombre del fabricante
    COUNT(DISTINCT p.category_id) AS category_count  -- Número de categorías distintas
FROM manufacturer AS m                          -- Tabla de fabricantes
INNER JOIN product AS p                         -- Productos asociados a cada fabricante
    ON p.manufacturer_id = m.id
WHERE p.category_id IS NOT NULL                 -- Ignora productos sin categoría asignada
GROUP BY
    m.id,
    m.name
HAVING
    COUNT(DISTINCT p.category_id) >= 2          -- Solo fabricantes con 2+ categorías
ORDER BY
    category_count DESC,                        -- Más categorías primero
    manufacturer_name ASC;                      -- Desempata por nombre
