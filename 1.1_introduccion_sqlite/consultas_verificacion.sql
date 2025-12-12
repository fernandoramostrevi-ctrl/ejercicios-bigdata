-- =============================================================================
-- Parte 4: Consultas de Verificación
-- =============================================================================

-- Este archivo contiene consultas SQL para verificar la integridad y el contenido
-- de las bases de datos generadas para los Modelos A, B y C.

-- Para ejecutar estas consultas:
-- 1. Abre la base de datos correspondiente (ej. tienda_modelo_a.db) con DB Browser for SQLite.
-- 2. Ve a la pestaña "Execute SQL".
-- 3. Copia y pega la consulta que deseas ejecutar y haz clic en el botón de "play".


-- =============================================================================
-- Consultas para el Modelo A (tienda_modelo_a.db)
-- =============================================================================

-- ¿Cuántas CPUs hay en el catálogo?
-- Nota: El nombre de la tabla puede variar. Usamos 'cpus_amd' como ejemplo.
-- Deberás ajustar el nombre de la tabla según el archivo CSV que quieras consultar.
SELECT COUNT(*) AS total_cpus
FROM cpus_amd;


-- ¿Cuál es el precio promedio de las placas base?
-- Nota: Ajusta el nombre de la tabla 'motherboards_amd' si es diferente.
SELECT AVG(price) AS precio_promedio_placas_base
FROM motherboards_amd;


-- Top 5 tarjetas gráficas más caras
-- Nota: Ajusta el nombre de la tabla 'gpus_nvidia' si es diferente.
SELECT
    name,
    price
FROM gpus_nvidia
ORDER BY price DESC
LIMIT 5;


-- =============================================================================
-- Consultas para el Modelo B (tienda_modelo_b.db)
-- =============================================================================

-- ¿Cuántos productos hay por categoría?
-- Usamos un JOIN para conectar la tabla 'productos' con la tabla 'categorias'
-- a través de sus IDs y luego agrupamos por el nombre de la categoría.
SELECT
    c.nombre AS categoria,
    COUNT(p.id) AS numero_de_productos
FROM productos p
JOIN categorias c ON p.categoria_id = c.id
GROUP BY c.nombre
ORDER BY numero_de_productos DESC;


-- ¿Qué fabricantes tienen más productos?
-- Similar a la consulta anterior, pero uniendo 'productos' con 'fabricantes'.
SELECT
    f.nombre AS fabricante,
    COUNT(p.id) AS numero_de_productos
FROM productos p
JOIN fabricantes f ON p.fabricante_id = f.id
GROUP BY f.nombre
ORDER BY numero_de_productos DESC
LIMIT 10; -- Mostramos el top 10


-- Productos con color "Black" del fabricante "Corsair"
-- Esta es una consulta más compleja que une 4 tablas:
-- 1. Empezamos en 'productos'.
-- 2. Nos unimos a 'fabricantes' para filtrar por "Corsair".
-- 3. Nos unimos a la tabla de unión 'productos_colores' para acceder a los colores.
-- 4. Finalmente, nos unimos a 'colores' para filtrar por el nombre "Black".
SELECT
    p.nombre AS producto,
    p.price,
    f.nombre AS fabricante,
    co.nombre AS color
FROM productos p
JOIN fabricantes f ON p.fabricante_id = f.id
JOIN productos_colores pc ON p.id = pc.producto_id
JOIN colores co ON pc.color_id = co.id
WHERE f.nombre = 'Corsair' AND co.nombre = 'Black';


-- =============================================================================
-- Consultas para el Modelo C (tienda_modelo_c.db)
-- =============================================================================

-- ¿Cuántos pedidos tiene cada cliente?
-- Unimos 'clientes' con 'pedidos' y contamos los pedidos por cada cliente.
-- Usamos un LEFT JOIN para incluir también a los clientes que no tienen ningún pedido.
SELECT
    c.nombre,
    c.apellido,
    c.email,
    COUNT(p.id) AS numero_de_pedidos
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id
GROUP BY c.id;


-- ¿Cuál es el total de ventas por categoría?
-- Esta consulta requiere unir varias tablas:
-- lineas_pedido (para cantidad y precio) -> productos -> categorias
SELECT
    cat.nombre AS categoria,
    SUM(lp.cantidad * lp.precio_unitario) AS ventas_totales
FROM lineas_pedido lp
JOIN productos p ON lp.producto_id = p.id
JOIN categorias cat ON p.categoria_id = cat.id
GROUP BY cat.nombre
ORDER BY ventas_totales DESC;


-- Productos con stock bajo (stock actual < stock mínimo)
-- Unimos 'inventario' con 'productos' para obtener el nombre del producto.
SELECT
    p.nombre AS producto,
    i.stock AS stock_actual,
    i.stock_minimo
FROM inventario i
JOIN productos p ON i.producto_id = p.id
WHERE i.stock < i.stock_minimo;
