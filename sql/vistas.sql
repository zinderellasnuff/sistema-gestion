-- =====================================================
-- VISTAS - Sistema de Gestión Empresarial
-- Versión: 1.0
-- =====================================================

USE gestion_clientes;

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

SELECT '✓✓✓ Vistas creadas exitosamente ✓✓✓' AS Mensaje;
