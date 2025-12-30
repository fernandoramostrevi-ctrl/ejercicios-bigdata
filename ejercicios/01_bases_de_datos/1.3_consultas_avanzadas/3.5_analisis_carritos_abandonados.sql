-- Ejemplo teórico: Análisis de carritos abandonados (si existiera tabla cart y cart_item)

SELECT
    c.id AS customer_id,                            -- Cliente
    c.first_name || ' ' || c.last_name AS customer_name,
    SUM(ci.quantity * p.price) AS cart_value        -- Valor estimado del carrito
FROM cart AS ca                                     -- Tabla de carritos
INNER JOIN customer AS c
    ON ca.customer_id = c.id
INNER JOIN cart_item AS ci                          -- Líneas del carrito
    ON ci.cart_id = ca.id
INNER JOIN product AS p
    ON ci.product_id = p.id
WHERE
    ca.active = 1                                   -- Carrito activo
    AND NOT EXISTS (                                -- ...pero sin pedidos recientes
        SELECT 1
        FROM "order" AS o
        WHERE o.customer_id = c.id
          AND o.order_date >= DATE('now', '-30 day')
    )
GROUP BY
    c.id, c.first_name, c.last_name;
-- Ejercicio 3.5: Análisis de carritos abandonados
-- En el modelo C actual no existe ninguna tabla de carritos (cart, shopping_cart, etc.),
-- solo se almacenan pedidos confirmados ("order") y sus líneas (order_item).
-- Por tanto, no es posible identificar carritos activos ni carritos abandonados
-- ni calcular su valor estimado con este esquema.
-- Arriba se incluye una consulta de ejemplo teórica que supondría la existencia
-- de tablas cart y cart_item, pero no puede ejecutarse en esta base de datos.
