-- Ejercicio 3.1: Ventas por cliente
-- Calcula, para cada cliente:
-- - total gastado (suma de total de sus pedidos),
-- - número de pedidos realizados,
-- - ticket promedio (total gastado / número de pedidos).

SELECT
    c.id AS customer_id,                            -- Identificador del cliente
    c.first_name || ' ' || c.last_name AS customer_name,  -- Nombre completo del cliente
    COUNT(DISTINCT o.id) AS order_count,            -- Número de pedidos realizados
    SUM(o.total) AS total_spent,                    -- Total gastado (suma de total de pedidos)
    CASE
        WHEN COUNT(DISTINCT o.id) = 0 THEN NULL
        ELSE ROUND(SUM(o.total) / COUNT(DISTINCT o.id), 2)
    END AS avg_ticket                               -- Importe medio por pedido (ticket promedio)
FROM customer AS c                                  -- Tabla de clientes
LEFT JOIN "order" AS o                              -- Relaciona cada cliente con sus pedidos
    ON o.customer_id = c.id
-- LEFT JOIN order_item AS oi                       -- (Opcional) Join con líneas si hiciera falta detalle
--     ON oi.order_id = o.id
GROUP BY
    c.id,
    c.first_name,
    c.last_name
HAVING
    COUNT(DISTINCT o.id) > 0                        -- Solo clientes que han hecho al menos un pedido
ORDER BY
    total_spent DESC,                               -- Clientes que más han gastado primero
    customer_name ASC;                              -- Desempata por nombre
