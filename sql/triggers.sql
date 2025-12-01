-- =====================================================
-- TRIGGERS - Sistema de Gestión Empresarial
-- Versión: 1.0 - Adaptado a estructura REAL
-- =====================================================

USE gestion_clientes;

-- =====================================================
-- CREAR TABLAS DE AUDITORÍA
-- =====================================================

-- Tabla de auditoría para cliente
CREATE TABLE IF NOT EXISTS auditoria_cliente (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    ruc CHAR(11) NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores TEXT,
    datos_nuevos TEXT,
    observaciones VARCHAR(200),
    INDEX idx_ruc (ruc),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de auditoría para empleado
CREATE TABLE IF NOT EXISTS auditoria_empleado (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    codigo INT NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores TEXT,
    datos_nuevos TEXT,
    observaciones VARCHAR(200),
    INDEX idx_codigo (codigo),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de auditoría para archivo_excel
CREATE TABLE IF NOT EXISTS auditoria_archivo_excel (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores TEXT,
    datos_nuevos TEXT,
    observaciones VARCHAR(200),
    INDEX idx_nombre (nombre),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DELIMITER $$

-- =====================================================
-- TRIGGERS PARA: cliente
-- =====================================================

-- Trigger: INSERT en cliente
DROP TRIGGER IF EXISTS trg_cliente_insert$$
CREATE TRIGGER trg_cliente_insert
AFTER INSERT ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_cliente (ruc, tipo_operacion, usuario, datos_nuevos, observaciones)
    VALUES (
        NEW.ruc,
        'INSERT',
        USER(),
        CONCAT(
            'RUC: ', NEW.ruc, ', ',
            'Nombres: ', NEW.nombres, ' ', NEW.apellido_paterno, ' ', NEW.apellido_materno, ', ',
            'Email: ', IFNULL(NEW.correo_electronico, 'N/A'), ', ',
            'Teléfono: ', IFNULL(NEW.telefono, 'N/A')
        ),
        'Cliente registrado'
    );
END$$

-- Trigger: UPDATE en cliente
DROP TRIGGER IF EXISTS trg_cliente_update$$
CREATE TRIGGER trg_cliente_update
AFTER UPDATE ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_cliente (ruc, tipo_operacion, usuario, datos_anteriores, datos_nuevos, observaciones)
    VALUES (
        NEW.ruc,
        'UPDATE',
        USER(),
        CONCAT(
            'Nombres: ', OLD.nombres, ' ', OLD.apellido_paterno, ' ', OLD.apellido_materno, ', ',
            'Email: ', IFNULL(OLD.correo_electronico, 'N/A'), ', ',
            'Teléfono: ', IFNULL(OLD.telefono, 'N/A')
        ),
        CONCAT(
            'Nombres: ', NEW.nombres, ' ', NEW.apellido_paterno, ' ', NEW.apellido_materno, ', ',
            'Email: ', IFNULL(NEW.correo_electronico, 'N/A'), ', ',
            'Teléfono: ', IFNULL(NEW.telefono, 'N/A')
        ),
        'Cliente actualizado'
    );
END$$

-- Trigger: DELETE en cliente
DROP TRIGGER IF EXISTS trg_cliente_delete$$
CREATE TRIGGER trg_cliente_delete
BEFORE DELETE ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_cliente (ruc, tipo_operacion, usuario, datos_anteriores, observaciones)
    VALUES (
        OLD.ruc,
        'DELETE',
        USER(),
        CONCAT(
            'Nombres: ', OLD.nombres, ' ', OLD.apellido_paterno, ' ', OLD.apellido_materno, ', ',
            'Email: ', IFNULL(OLD.correo_electronico, 'N/A')
        ),
        'Cliente eliminado'
    );
END$$

-- =====================================================
-- TRIGGERS PARA: empleado
-- =====================================================

-- Trigger: INSERT en empleado
DROP TRIGGER IF EXISTS trg_empleado_insert$$
CREATE TRIGGER trg_empleado_insert
AFTER INSERT ON empleado
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_empleado (codigo, tipo_operacion, usuario, datos_nuevos, observaciones)
    VALUES (
        NEW.codigo,
        'INSERT',
        USER(),
        CONCAT(
            'Código: ', NEW.codigo, ', ',
            'Nombres: ', NEW.nombres, ' ', NEW.apellido_paterno, ' ', NEW.apellido_materno, ', ',
            'Cargo: ', NEW.cargo, ', ',
            'Sexo: ', NEW.sexo, ', ',
            'Cliente asignado: ', IFNULL(NEW.ruc_cliente, 'N/A')
        ),
        'Empleado registrado'
    );
END$$

-- Trigger: UPDATE en empleado
DROP TRIGGER IF EXISTS trg_empleado_update$$
CREATE TRIGGER trg_empleado_update
AFTER UPDATE ON empleado
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_empleado (codigo, tipo_operacion, usuario, datos_anteriores, datos_nuevos, observaciones)
    VALUES (
        NEW.codigo,
        'UPDATE',
        USER(),
        CONCAT(
            'Cargo: ', OLD.cargo, ', ',
            'Cliente: ', IFNULL(OLD.ruc_cliente, 'N/A')
        ),
        CONCAT(
            'Cargo: ', NEW.cargo, ', ',
            'Cliente: ', IFNULL(NEW.ruc_cliente, 'N/A')
        ),
        'Empleado actualizado'
    );
END$$

-- Trigger: DELETE en empleado
DROP TRIGGER IF EXISTS trg_empleado_delete$$
CREATE TRIGGER trg_empleado_delete
BEFORE DELETE ON empleado
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_empleado (codigo, tipo_operacion, usuario, datos_anteriores, observaciones)
    VALUES (
        OLD.codigo,
        'DELETE',
        USER(),
        CONCAT(
            'Nombres: ', OLD.nombres, ' ', OLD.apellido_paterno, ' ', OLD.apellido_materno, ', ',
            'Cargo: ', OLD.cargo
        ),
        'Empleado eliminado'
    );
END$$

-- =====================================================
-- TRIGGERS PARA: archivo_excel_gestion_clientes
-- =====================================================

-- Trigger: INSERT en archivo_excel
DROP TRIGGER IF EXISTS trg_archivo_excel_insert$$
CREATE TRIGGER trg_archivo_excel_insert
AFTER INSERT ON archivo_excel_gestion_clientes
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_archivo_excel (nombre, tipo_operacion, usuario, datos_nuevos, observaciones)
    VALUES (
        NEW.nombre,
        'INSERT',
        USER(),
        CONCAT(
            'Archivo: ', NEW.nombre, ', ',
            'Fecha creación: ', NEW.fecha_creacion
        ),
        'Archivo registrado'
    );
END$$

-- Trigger: UPDATE en archivo_excel
DROP TRIGGER IF EXISTS trg_archivo_excel_update$$
CREATE TRIGGER trg_archivo_excel_update
AFTER UPDATE ON archivo_excel_gestion_clientes
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_archivo_excel (nombre, tipo_operacion, usuario, datos_anteriores, datos_nuevos, observaciones)
    VALUES (
        NEW.nombre,
        'UPDATE',
        USER(),
        CONCAT('Fecha modificación: ', OLD.fecha_modificacion),
        CONCAT('Fecha modificación: ', NEW.fecha_modificacion),
        'Archivo actualizado'
    );
END$$

-- Trigger: DELETE en archivo_excel
DROP TRIGGER IF EXISTS trg_archivo_excel_delete$$
CREATE TRIGGER trg_archivo_excel_delete
BEFORE DELETE ON archivo_excel_gestion_clientes
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_archivo_excel (nombre, tipo_operacion, usuario, datos_anteriores, observaciones)
    VALUES (
        OLD.nombre,
        'DELETE',
        USER(),
        CONCAT('Archivo: ', OLD.nombre),
        'Archivo eliminado'
    );
END$$

DELIMITER ;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT '✓✓✓ Triggers creados exitosamente ✓✓✓' AS Mensaje;
SELECT '✓ 3 Tablas de auditoría creadas' AS Mensaje;
SELECT '✓ 9 Triggers activados (INSERT, UPDATE, DELETE)' AS Mensaje;
