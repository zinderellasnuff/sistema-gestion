-- =====================================================
-- CONSULTAS SQL DE REPORTES
-- Sistema de Gestión de Clientes JP
-- 5 Consultas implementadas (30% del total de 13 consultas planificadas)
-- =====================================================

USE gestion_clientes_jp;

-- =====================================================
-- CONSULTA 1: Reporte de Clientes Activos por Departamento
-- Descripción: Lista todos los clientes activos agrupados por departamento
-- =====================================================
SELECT
    'REPORTE 1: Clientes Activos por Departamento' AS Reporte;

SELECT
    departamento,
    COUNT(*) AS total_clientes,
    GROUP_CONCAT(razon_social SEPARATOR ', ') AS clientes
FROM cliente
WHERE estado = 'ACTIVO'
GROUP BY departamento
ORDER BY total_clientes DESC;

-- =====================================================
-- CONSULTA 2: Reporte de Empleados por Área y Cargo
-- Descripción: Muestra empleados agrupados por área con total de salarios
-- =====================================================
SELECT
    'REPORTE 2: Empleados por Área con Salarios' AS Reporte;

SELECT
    area,
    cargo,
    COUNT(*) AS total_empleados,
    SUM(salario) AS total_salarios,
    AVG(salario) AS salario_promedio,
    MIN(salario) AS salario_minimo,
    MAX(salario) AS salario_maximo
FROM empleado
WHERE estado = 'ACTIVO'
GROUP BY area, cargo
ORDER BY area, total_salarios DESC;

-- =====================================================
-- CONSULTA 3: Reporte de Consultas SUNAT por Tipo
-- Descripción: Estadísticas de consultas realizadas a SUNAT
-- =====================================================
SELECT
    'REPORTE 3: Consultas SUNAT por Tipo' AS Reporte;

SELECT
    tipo_consulta,
    COUNT(*) AS total_consultas,
    COUNT(DISTINCT ruc_consultado) AS rucs_unicos,
    estado_sunat,
    condicion_sunat,
    DATE_FORMAT(MIN(fecha_consulta), '%Y-%m-%d') AS primera_consulta,
    DATE_FORMAT(MAX(fecha_consulta), '%Y-%m-%d') AS ultima_consulta
FROM consulta_sunat
GROUP BY tipo_consulta, estado_sunat, condicion_sunat
ORDER BY total_consultas DESC;

-- =====================================================
-- CONSULTA 4: Reporte de Archivos Excel Procesados
-- Descripción: Resumen de archivos Excel con estadísticas de procesamiento
-- =====================================================
SELECT
    'REPORTE 4: Resumen de Archivos Excel Procesados' AS Reporte;

SELECT
    tipo_operacion,
    COUNT(*) AS total_archivos,
    SUM(registros_procesados) AS total_registros,
    SUM(registros_exitosos) AS total_exitosos,
    SUM(registros_con_error) AS total_errores,
    ROUND((SUM(registros_exitosos) / SUM(registros_procesados)) * 100, 2) AS porcentaje_exito,
    estado_procesamiento
FROM archivo_excel_gestion_clientes
GROUP BY tipo_operacion, estado_procesamiento
ORDER BY tipo_operacion, total_archivos DESC;

-- =====================================================
-- CONSULTA 5: Reporte de Auditoría de Clientes (Últimas 30 operaciones)
-- Descripción: Muestra las últimas operaciones de auditoría en clientes
-- =====================================================
SELECT
    'REPORTE 5: Auditoría de Clientes (Últimas 30 operaciones)' AS Reporte;

SELECT
    a.id_auditoria,
    a.id_cliente,
    c.razon_social,
    c.ruc,
    a.tipo_operacion,
    a.usuario,
    DATE_FORMAT(a.fecha_operacion, '%Y-%m-%d %H:%i:%s') AS fecha_hora,
    a.observaciones
FROM auditoria_cliente a
LEFT JOIN cliente c ON a.id_cliente = c.id_cliente
ORDER BY a.fecha_operacion DESC
LIMIT 30;

-- =====================================================
-- VISTA ADICIONAL: Dashboard Principal
-- Descripción: Vista consolidada para el dashboard principal
-- =====================================================
DROP VIEW IF EXISTS vista_dashboard_principal;
CREATE VIEW vista_dashboard_principal AS
SELECT
    (SELECT COUNT(*) FROM cliente WHERE estado = 'ACTIVO') AS total_clientes_activos,
    (SELECT COUNT(*) FROM cliente WHERE estado = 'INACTIVO') AS total_clientes_inactivos,
    (SELECT COUNT(*) FROM cliente WHERE estado = 'SUSPENDIDO') AS total_clientes_suspendidos,
    (SELECT COUNT(*) FROM empleado WHERE estado = 'ACTIVO') AS total_empleados_activos,
    (SELECT SUM(salario) FROM empleado WHERE estado = 'ACTIVO') AS nomina_total,
    (SELECT COUNT(*) FROM consulta_sunat WHERE DATE(fecha_consulta) = CURDATE()) AS consultas_sunat_hoy,
    (SELECT COUNT(*) FROM archivo_excel_gestion_clientes WHERE estado_procesamiento = 'COMPLETADO') AS archivos_procesados,
    (SELECT COUNT(*) FROM auditoria_cliente WHERE DATE(fecha_operacion) = CURDATE()) AS operaciones_hoy;

-- Consultar la vista del dashboard
SELECT 'VISTA DASHBOARD: Resumen General del Sistema' AS Reporte;
SELECT * FROM vista_dashboard_principal;

-- =====================================================
-- CONSULTAS ADICIONALES ÚTILES (Bonus)
-- =====================================================

-- Clientes por provincia (Top 10)
SELECT
    'BONUS: Top 10 Provincias con más Clientes' AS Reporte;

SELECT
    provincia,
    departamento,
    COUNT(*) AS total_clientes
FROM cliente
WHERE estado = 'ACTIVO'
GROUP BY provincia, departamento
ORDER BY total_clientes DESC
LIMIT 10;

-- Empleados próximos a cumplir años
SELECT
    'BONUS: Empleados con Cumpleaños este Mes' AS Reporte;

SELECT
    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
    dni,
    cargo,
    DATE_FORMAT(fecha_nacimiento, '%d-%m-%Y') AS fecha_nacimiento,
    TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS edad
FROM empleado
WHERE MONTH(fecha_nacimiento) = MONTH(CURDATE())
  AND estado = 'ACTIVO'
ORDER BY DAY(fecha_nacimiento);

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT '✓ 5 Consultas de Reportes implementadas exitosamente' AS Mensaje;
SELECT '✓ 1 Vista de Dashboard creada' AS Mensaje;
SELECT '✓ 2 Consultas Bonus agregadas' AS Mensaje;
