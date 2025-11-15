-- =====================================================
-- SISTEMA DE GESTIÓN DE CLIENTES JP
-- Documentación de estructura REAL de base de datos
-- Versión: 2.0 (Adaptado)
-- =====================================================

USE gestion_clientes_jp;

-- =====================================================
-- NOTA: Este script NO recrea las tablas existentes
-- Solo documenta la estructura real y agrega tablas
-- de auditoría opcionales
-- =====================================================

-- =====================================================
-- ESTRUCTURA REAL - Tabla: cliente
-- =====================================================
-- ruc (PK, CHAR(11)) - RUC del cliente
-- nombres (VARCHAR(50)) - Nombres del cliente
-- apellido_paterno (VARCHAR(50)) - Apellido paterno
-- apellido_materno (VARCHAR(50)) - Apellido materno
-- correo_electronico (VARCHAR(100)) - Email
-- pagina_web (VARCHAR(200)) - Sitio web
-- telefono (CHAR(9)) - Teléfono de contacto

-- =====================================================
-- ESTRUCTURA REAL - Tabla: empleado
-- =====================================================
-- codigo (PK, INT) - Código del empleado
-- sexo (VARCHAR(10)) - Sexo (Masculino/Femenino)
-- cargo (VARCHAR(50)) - Cargo del empleado
-- fecha_nacimiento (DATE) - Fecha de nacimiento
-- nombres (VARCHAR(50)) - Nombres del empleado
-- apellido_paterno (VARCHAR(20)) - Apellido paterno
-- apellido_materno (VARCHAR(20)) - Apellido materno
-- ruc_cliente (CHAR(11), FK) - RUC del cliente asignado
-- nombre_archivo (VARCHAR(100), FK) - Archivo Excel relacionado

-- =====================================================
-- ESTRUCTURA REAL - Tabla: consulta_sunat
-- =====================================================
-- nro_consultado - Número consultado (RUC)
-- codigo_empleado - Código del empleado que consulta
-- razon_social - Razón social encontrada
-- estado - Estado en SUNAT
-- condicion - Condición del contribuyente

-- =====================================================
-- ESTRUCTURA REAL - Tabla: archivo_excel_gestion_clientes
-- =====================================================
-- nombre - Nombre del archivo
-- fecha_creacion - Fecha de creación
-- fecha_modificacion - Última modificación

-- =====================================================
-- TABLAS DE AUDITORÍA (OPCIONALES)
-- =====================================================

-- Auditoría para cliente
CREATE TABLE IF NOT EXISTS auditoria_cliente (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(11) NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores TEXT,
    datos_nuevos TEXT,
    INDEX idx_ruc (ruc),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Auditoría para empleado
CREATE TABLE IF NOT EXISTS auditoria_empleado (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    codigo INT NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores TEXT,
    datos_nuevos TEXT,
    INDEX idx_codigo (codigo),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- VISTAS ÚTILES
-- =====================================================

-- Vista: Clientes con empleados asignados
CREATE OR REPLACE VIEW vista_clientes_con_empleados AS
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

-- Vista: Dashboard principal
CREATE OR REPLACE VIEW vista_dashboard AS
SELECT
    (SELECT COUNT(*) FROM cliente) AS total_clientes,
    (SELECT COUNT(*) FROM empleado) AS total_empleados,
    (SELECT COUNT(*) FROM consulta_sunat) AS total_consultas_sunat,
    (SELECT COUNT(*) FROM archivo_excel_gestion_clientes) AS total_archivos,
    (SELECT COUNT(*) FROM empleado WHERE sexo = 'Masculino') AS empleados_masculinos,
    (SELECT COUNT(*) FROM empleado WHERE sexo = 'Femenino') AS empleados_femeninos;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT '✓ Tablas de auditoría creadas (si no existían)' AS Mensaje;
SELECT '✓ Vistas creadas exitosamente' AS Mensaje;
SELECT '' AS '';
SELECT 'RESUMEN DEL SISTEMA:' AS Info;
SELECT COUNT(*) AS 'Total Clientes' FROM cliente;
SELECT COUNT(*) AS 'Total Empleados' FROM empleado;
SELECT COUNT(*) AS 'Total Consultas SUNAT' FROM consulta_sunat;
SELECT COUNT(*) AS 'Total Archivos Excel' FROM archivo_excel_gestion_clientes;
