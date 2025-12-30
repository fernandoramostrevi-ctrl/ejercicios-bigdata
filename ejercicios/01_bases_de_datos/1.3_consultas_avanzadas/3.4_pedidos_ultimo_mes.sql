-- Ejercicio 3.4: Pedidos del último mes
-- Resume, por día, los pedidos de los últimos 30 días:
-- número de pedidos, total de ventas y ticket promedio.

SELECT
    DATE(o.order_date) AS order_day,                    -- Día del pedido (sin hora)
    COUNT(DISTINCT o.id) AS order_count,                -- Número de pedidos en ese día
    SUM(o.total) AS total_sales,                        -- Importe total vendido en ese día
    CASE
        WHEN COUNT(DISTINCT o.id) = 0 THEN NULL
        ELSE ROUND(SUM(o.total) / COUNT(DISTINCT o.id), 2)
    END AS avg_ticket                                   -- Ticket promedio por pedido en ese día
FROM "order" AS o                                       -- Tabla de pedidos
INNER JOIN customer AS c                                -- Join con cliente (por si se necesita información de cliente)
    ON o.customer_id = c.id
WHERE
    o.order_date >= DATE('now', '-30 day')              -- Solo pedidos de los últimos 30 días
GROUP BY
    DATE(o.order_date)
ORDER BY
    order_day DESC;                                     -- Días más recientes primero
