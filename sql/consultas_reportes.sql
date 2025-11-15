-- =====================================================
-- CONSULTAS SQL DE REPORTES - Adaptadas a estructura REAL
-- Sistema de Gestión de Clientes JP
-- 13 Consultas implementadas (100% completo)
-- =====================================================

USE gestion_clientes_jp;

-- =====================================================
-- CONSULTA 1: Listado completo de clientes
-- =====================================================
SELECT 'CONSULTA 1: Listado Completo de Clientes' AS Reporte;

SELECT
    ruc,
    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
    correo_electronico,
    pagina_web,
    telefono
FROM cliente
ORDER BY apellido_paterno, apellido_materno, nombres;

-- =====================================================
-- CONSULTA 2: Clientes con información completa
-- =====================================================
SELECT 'CONSULTA 2: Clientes con Información Completa' AS Reporte;

SELECT
    ruc,
    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
    correo_electronico,
    telefono,
    pagina_web
FROM cliente
WHERE correo_electronico IS NOT NULL
  AND telefono IS NOT NULL
  AND pagina_web IS NOT NULL
ORDER BY apellido_paterno;

-- =====================================================
-- CONSULTA 3: Clientes con información incompleta
-- =====================================================
SELECT 'CONSULTA 3: Clientes con Información Incompleta' AS Reporte;

SELECT
    ruc,
    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
    CASE
        WHEN correo_electronico IS NULL THEN 'Falta correo'
        WHEN pagina_web IS NULL THEN 'Falta página web'
        ELSE 'Datos incompletos'
    END AS dato_faltante,
    correo_electronico,
    telefono,
    pagina_web
FROM cliente
WHERE correo_electronico IS NULL OR pagina_web IS NULL
ORDER BY apellido_paterno;

-- =====================================================
-- CONSULTA 4: Búsqueda flexible de clientes
-- =====================================================
SELECT 'CONSULTA 4: Búsqueda Flexible de Clientes' AS Reporte;

SELECT
    ruc,
    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
    correo_electronico,
    telefono,
    pagina_web
FROM cliente
WHERE nombres LIKE '%a%'
   OR apellido_paterno LIKE '%a%'
   OR apellido_materno LIKE '%a%'
ORDER BY apellido_paterno;

-- =====================================================
-- CONSULTA 5: Conteo de clientes por apellido paterno
-- =====================================================
SELECT 'CONSULTA 5: Conteo de Clientes por Apellido Paterno' AS Reporte;

SELECT
    apellido_paterno,
    COUNT(*) AS total_clientes,
    GROUP_CONCAT(CONCAT(nombres, ' ', apellido_materno) ORDER BY nombres SEPARATOR ', ') AS clientes
FROM cliente
GROUP BY apellido_paterno
ORDER BY total_clientes DESC, apellido_paterno;

-- =====================================================
-- CONSULTA 6: Clientes asignados a empleados (JOIN)
-- =====================================================
SELECT 'CONSULTA 6: Clientes Asignados a Empleados (JOIN)' AS Reporte;

SELECT
    e.codigo,
    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
    e.cargo,
    e.sexo,
    c.ruc,
    CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS cliente,
    c.telefono,
    c.correo_electronico
FROM empleado e
INNER JOIN cliente c ON e.ruc_cliente = c.ruc
ORDER BY e.codigo;

-- =====================================================
-- CONSULTA 7: Estadísticas de empleados por cargo
-- =====================================================
SELECT 'CONSULTA 7: Estadísticas de Empleados por Cargo' AS Reporte;

SELECT
    cargo,
    COUNT(*) AS total_empleados,
    SUM(CASE WHEN sexo = 'Masculino' THEN 1 ELSE 0 END) AS hombres,
    SUM(CASE WHEN sexo = 'Femenino' THEN 1 ELSE 0 END) AS mujeres,
    MIN(fecha_nacimiento) AS empleado_mas_antiguo,
    MAX(fecha_nacimiento) AS empleado_mas_joven
FROM empleado
GROUP BY cargo
ORDER BY total_empleados DESC;

-- =====================================================
-- CONSULTA 8: Empleados sin clientes asignados
-- =====================================================
SELECT 'CONSULTA 8: Empleados sin Clientes Asignados' AS Reporte;

SELECT
    e.codigo,
    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
    e.cargo,
    e.sexo,
    e.fecha_nacimiento,
    TIMESTAMPDIFF(YEAR, e.fecha_nacimiento, CURDATE()) AS edad
FROM empleado e
WHERE e.ruc_cliente IS NULL
ORDER BY e.codigo;

-- =====================================================
-- CONSULTA 9: Historial completo de consultas SUNAT (JOIN)
-- =====================================================
SELECT 'CONSULTA 9: Historial Completo de Consultas SUNAT (JOIN)' AS Reporte;

SELECT
    cs.nro_consultado,
    cs.razon_social,
    cs.estado,
    cs.condicion,
    cs.codigo_empleado,
    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
    e.cargo
FROM consulta_sunat cs
INNER JOIN empleado e ON cs.codigo_empleado = e.codigo
ORDER BY cs.nro_consultado;

-- =====================================================
-- CONSULTA 10: Clientes con problemas en SUNAT
-- =====================================================
SELECT 'CONSULTA 10: Clientes con Problemas en SUNAT' AS Reporte;

SELECT
    c.ruc,
    CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS cliente,
    c.correo_electronico,
    c.telefono,
    cs.razon_social,
    cs.estado,
    cs.condicion,
    CASE
        WHEN cs.estado != 'ACTIVO' THEN 'URGENTE - Estado inactivo'
        WHEN cs.condicion != 'HABIDO' THEN 'IMPORTANTE - No habido'
        ELSE 'REVISAR'
    END AS prioridad
FROM cliente c
LEFT JOIN consulta_sunat cs ON c.ruc = cs.nro_consultado
WHERE cs.estado IS NOT NULL
  AND (cs.estado != 'ACTIVO' OR cs.condicion != 'HABIDO')
ORDER BY
    CASE
        WHEN cs.estado != 'ACTIVO' THEN 1
        WHEN cs.condicion != 'HABIDO' THEN 2
        ELSE 3
    END;

-- =====================================================
-- CONSULTA 11: Productividad de consultas SUNAT por empleado
-- =====================================================
SELECT 'CONSULTA 11: Productividad de Consultas SUNAT por Empleado' AS Reporte;

SELECT
    e.codigo,
    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
    e.cargo,
    COUNT(cs.nro_consultado) AS total_consultas,
    SUM(CASE WHEN cs.estado = 'ACTIVO' THEN 1 ELSE 0 END) AS consultas_activas,
    SUM(CASE WHEN cs.condicion = 'HABIDO' THEN 1 ELSE 0 END) AS consultas_habidas
FROM empleado e
LEFT JOIN consulta_sunat cs ON e.codigo = cs.codigo_empleado
GROUP BY e.codigo, empleado, e.cargo
ORDER BY total_consultas DESC;

-- =====================================================
-- CONSULTA 12: Análisis de archivos Excel
-- =====================================================
SELECT 'CONSULTA 12: Análisis de Uso de Archivos Excel' AS Reporte;

SELECT
    nombre,
    DATE_FORMAT(fecha_creacion, '%Y-%m-%d %H:%i') AS fecha_creacion,
    DATE_FORMAT(fecha_modificacion, '%Y-%m-%d %H:%i') AS fecha_modificacion,
    TIMESTAMPDIFF(DAY, fecha_creacion, fecha_modificacion) AS dias_entre_modificaciones,
    TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) AS dias_desde_ultima_modificacion,
    CASE
        WHEN TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) > 180 THEN 'Archivo antiguo'
        WHEN TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) > 90 THEN 'Archivo desactualizado'
        ELSE 'Archivo reciente'
    END AS estado_archivo
FROM archivo_excel_gestion_clientes
ORDER BY fecha_modificacion DESC;

-- =====================================================
-- CONSULTA 13: Reporte consolidado Cliente-Empleado-SUNAT (JOIN múltiple)
-- =====================================================
SELECT 'CONSULTA 13: Reporte Consolidado Cliente-Empleado-SUNAT (JOIN Múltiple)' AS Reporte;

SELECT
    c.ruc,
    CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS cliente,
    c.correo_electronico,
    c.telefono,
    c.pagina_web,
    e.codigo AS empleado_codigo,
    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado_asignado,
    e.cargo,
    e.sexo,
    cs.razon_social,
    cs.estado AS estado_sunat,
    cs.condicion AS condicion_sunat,
    CASE
        WHEN cs.estado = 'ACTIVO' AND cs.condicion = 'HABIDO' THEN 'VALIDADO'
        WHEN cs.estado != 'ACTIVO' THEN 'ALERTA - Inactivo'
        WHEN cs.condicion != 'HABIDO' THEN 'ALERTA - No habido'
        ELSE 'REVISAR'
    END AS clasificacion
FROM cliente c
LEFT JOIN empleado e ON c.ruc = e.ruc_cliente
LEFT JOIN consulta_sunat cs ON c.ruc = cs.nro_consultado
ORDER BY c.apellido_paterno, c.apellido_materno;

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista: Dashboard principal
DROP VIEW IF EXISTS vista_dashboard_principal;
CREATE VIEW vista_dashboard_principal AS
SELECT
    (SELECT COUNT(*) FROM cliente) AS total_clientes,
    (SELECT COUNT(*) FROM empleado) AS total_empleados,
    (SELECT COUNT(*) FROM consulta_sunat) AS total_consultas_sunat,
    (SELECT COUNT(*) FROM archivo_excel_gestion_clientes) AS total_archivos,
    (SELECT COUNT(*) FROM empleado WHERE sexo = 'Masculino') AS empleados_masculinos,
    (SELECT COUNT(*) FROM empleado WHERE sexo = 'Femenino') AS empleados_femeninos,
    (SELECT COUNT(*) FROM consulta_sunat WHERE estado = 'ACTIVO') AS consultas_activas,
    (SELECT COUNT(*) FROM consulta_sunat WHERE condicion = 'HABIDO') AS consultas_habidas;

-- Vista: Clientes con empleados asignados
DROP VIEW IF EXISTS vista_clientes_empleados;
CREATE VIEW vista_clientes_empleados AS
SELECT
    c.ruc,
    CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS cliente_nombre,
    c.correo_electronico,
    c.telefono,
    c.pagina_web,
    e.codigo AS empleado_codigo,
    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado_nombre,
    e.cargo,
    e.sexo
FROM cliente c
LEFT JOIN empleado e ON c.ruc = e.ruc_cliente;

-- Consultar vistas
SELECT 'VISTA: Dashboard Principal' AS Reporte;
SELECT * FROM vista_dashboard_principal;

SELECT 'VISTA: Clientes con Empleados Asignados' AS Reporte;
SELECT * FROM vista_clientes_empleados LIMIT 20;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT '✓✓✓ 13 Consultas SQL implementadas y adaptadas a estructura REAL ✓✓✓' AS Mensaje;
SELECT '✓ 2 Vistas de base de datos creadas' AS Mensaje;
SELECT '✓ 6 Consultas con JOIN implementadas' AS Mensaje;
