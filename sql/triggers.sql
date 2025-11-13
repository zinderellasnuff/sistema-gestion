-- =====================================================
-- TRIGGERS DE AUDITORÍA
-- Sistema de Gestión de Clientes JP
-- =====================================================

USE gestion_clientes_jp;

DELIMITER $$

-- =====================================================
-- TRIGGERS PARA TABLA: cliente
-- =====================================================

-- Trigger: Auditar INSERT en cliente
DROP TRIGGER IF EXISTS trg_auditoria_cliente_insert$$
CREATE TRIGGER trg_auditoria_cliente_insert
AFTER INSERT ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_cliente (
        id_cliente,
        tipo_operacion,
        usuario,
        datos_nuevos,
        observaciones
    ) VALUES (
        NEW.id_cliente,
        'INSERT',
        USER(),
        JSON_OBJECT(
            'id_cliente', NEW.id_cliente,
            'ruc', NEW.ruc,
            'razon_social', NEW.razon_social,
            'nombre_comercial', NEW.nombre_comercial,
            'direccion', NEW.direccion,
            'distrito', NEW.distrito,
            'provincia', NEW.provincia,
            'departamento', NEW.departamento,
            'telefono', NEW.telefono,
            'email', NEW.email,
            'estado', NEW.estado
        ),
        'Nuevo cliente registrado'
    );
END$$

-- Trigger: Auditar UPDATE en cliente
DROP TRIGGER IF EXISTS trg_auditoria_cliente_update$$
CREATE TRIGGER trg_auditoria_cliente_update
AFTER UPDATE ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_cliente (
        id_cliente,
        tipo_operacion,
        usuario,
        datos_anteriores,
        datos_nuevos,
        observaciones
    ) VALUES (
        NEW.id_cliente,
        'UPDATE',
        USER(),
        JSON_OBJECT(
            'id_cliente', OLD.id_cliente,
            'ruc', OLD.ruc,
            'razon_social', OLD.razon_social,
            'nombre_comercial', OLD.nombre_comercial,
            'direccion', OLD.direccion,
            'distrito', OLD.distrito,
            'provincia', OLD.provincia,
            'departamento', OLD.departamento,
            'telefono', OLD.telefono,
            'email', OLD.email,
            'estado', OLD.estado
        ),
        JSON_OBJECT(
            'id_cliente', NEW.id_cliente,
            'ruc', NEW.ruc,
            'razon_social', NEW.razon_social,
            'nombre_comercial', NEW.nombre_comercial,
            'direccion', NEW.direccion,
            'distrito', NEW.distrito,
            'provincia', NEW.provincia,
            'departamento', NEW.departamento,
            'telefono', NEW.telefono,
            'email', NEW.email,
            'estado', NEW.estado
        ),
        'Cliente actualizado'
    );
END$$

-- Trigger: Auditar DELETE en cliente
DROP TRIGGER IF EXISTS trg_auditoria_cliente_delete$$
CREATE TRIGGER trg_auditoria_cliente_delete
BEFORE DELETE ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_cliente (
        id_cliente,
        tipo_operacion,
        usuario,
        datos_anteriores,
        observaciones
    ) VALUES (
        OLD.id_cliente,
        'DELETE',
        USER(),
        JSON_OBJECT(
            'id_cliente', OLD.id_cliente,
            'ruc', OLD.ruc,
            'razon_social', OLD.razon_social,
            'nombre_comercial', OLD.nombre_comercial,
            'direccion', OLD.direccion,
            'estado', OLD.estado
        ),
        'Cliente eliminado'
    );
END$$

-- =====================================================
-- TRIGGERS PARA TABLA: empleado
-- =====================================================

-- Tabla de auditoría para empleados
DROP TABLE IF EXISTS auditoria_empleado$$
CREATE TABLE auditoria_empleado (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores JSON,
    datos_nuevos JSON,
    observaciones TEXT,
    INDEX idx_empleado (id_empleado),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4$$

-- Trigger: Auditar INSERT en empleado
DROP TRIGGER IF EXISTS trg_auditoria_empleado_insert$$
CREATE TRIGGER trg_auditoria_empleado_insert
AFTER INSERT ON empleado
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_empleado (
        id_empleado,
        tipo_operacion,
        usuario,
        datos_nuevos,
        observaciones
    ) VALUES (
        NEW.id_empleado,
        'INSERT',
        USER(),
        JSON_OBJECT(
            'id_empleado', NEW.id_empleado,
            'dni', NEW.dni,
            'nombres', NEW.nombres,
            'apellido_paterno', NEW.apellido_paterno,
            'apellido_materno', NEW.apellido_materno,
            'cargo', NEW.cargo,
            'area', NEW.area,
            'salario', NEW.salario,
            'estado', NEW.estado
        ),
        'Nuevo empleado registrado'
    );
END$$

-- Trigger: Auditar UPDATE en empleado
DROP TRIGGER IF EXISTS trg_auditoria_empleado_update$$
CREATE TRIGGER trg_auditoria_empleado_update
AFTER UPDATE ON empleado
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_empleado (
        id_empleado,
        tipo_operacion,
        usuario,
        datos_anteriores,
        datos_nuevos,
        observaciones
    ) VALUES (
        NEW.id_empleado,
        'UPDATE',
        USER(),
        JSON_OBJECT(
            'id_empleado', OLD.id_empleado,
            'dni', OLD.dni,
            'nombres', OLD.nombres,
            'cargo', OLD.cargo,
            'area', OLD.area,
            'salario', OLD.salario,
            'estado', OLD.estado
        ),
        JSON_OBJECT(
            'id_empleado', NEW.id_empleado,
            'dni', NEW.dni,
            'nombres', NEW.nombres,
            'cargo', NEW.cargo,
            'area', NEW.area,
            'salario', NEW.salario,
            'estado', NEW.estado
        ),
        'Empleado actualizado'
    );
END$$

-- Trigger: Auditar DELETE en empleado
DROP TRIGGER IF EXISTS trg_auditoria_empleado_delete$$
CREATE TRIGGER trg_auditoria_empleado_delete
BEFORE DELETE ON empleado
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_empleado (
        id_empleado,
        tipo_operacion,
        usuario,
        datos_anteriores,
        observaciones
    ) VALUES (
        OLD.id_empleado,
        'DELETE',
        USER(),
        JSON_OBJECT(
            'id_empleado', OLD.id_empleado,
            'dni', OLD.dni,
            'nombres', OLD.nombres,
            'cargo', OLD.cargo,
            'estado', OLD.estado
        ),
        'Empleado eliminado'
    );
END$$

-- =====================================================
-- TRIGGERS PARA TABLA: consulta_sunat
-- =====================================================

-- Tabla de auditoría para consultas SUNAT
DROP TABLE IF EXISTS auditoria_consulta_sunat$$
CREATE TABLE auditoria_consulta_sunat (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores JSON,
    datos_nuevos JSON,
    observaciones TEXT,
    INDEX idx_consulta (id_consulta),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4$$

-- Trigger: Auditar INSERT en consulta_sunat
DROP TRIGGER IF EXISTS trg_auditoria_consulta_sunat_insert$$
CREATE TRIGGER trg_auditoria_consulta_sunat_insert
AFTER INSERT ON consulta_sunat
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_consulta_sunat (
        id_consulta,
        tipo_operacion,
        usuario,
        datos_nuevos,
        observaciones
    ) VALUES (
        NEW.id_consulta,
        'INSERT',
        USER(),
        JSON_OBJECT(
            'id_consulta', NEW.id_consulta,
            'ruc_consultado', NEW.ruc_consultado,
            'tipo_consulta', NEW.tipo_consulta,
            'estado_sunat', NEW.estado_sunat,
            'condicion_sunat', NEW.condicion_sunat
        ),
        'Nueva consulta SUNAT registrada'
    );
END$$

-- Trigger: Auditar DELETE en consulta_sunat
DROP TRIGGER IF EXISTS trg_auditoria_consulta_sunat_delete$$
CREATE TRIGGER trg_auditoria_consulta_sunat_delete
BEFORE DELETE ON consulta_sunat
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_consulta_sunat (
        id_consulta,
        tipo_operacion,
        usuario,
        datos_anteriores,
        observaciones
    ) VALUES (
        OLD.id_consulta,
        'DELETE',
        USER(),
        JSON_OBJECT(
            'id_consulta', OLD.id_consulta,
            'ruc_consultado', OLD.ruc_consultado,
            'tipo_consulta', OLD.tipo_consulta
        ),
        'Consulta SUNAT eliminada'
    );
END$$

-- =====================================================
-- TRIGGERS PARA TABLA: archivo_excel_gestion_clientes
-- =====================================================

-- Tabla de auditoría para archivos Excel
DROP TABLE IF EXISTS auditoria_archivo_excel$$
CREATE TABLE auditoria_archivo_excel (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_archivo INT NOT NULL,
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores JSON,
    datos_nuevos JSON,
    observaciones TEXT,
    INDEX idx_archivo (id_archivo),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4$$

-- Trigger: Auditar INSERT en archivo_excel_gestion_clientes
DROP TRIGGER IF EXISTS trg_auditoria_archivo_excel_insert$$
CREATE TRIGGER trg_auditoria_archivo_excel_insert
AFTER INSERT ON archivo_excel_gestion_clientes
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_archivo_excel (
        id_archivo,
        tipo_operacion,
        usuario,
        datos_nuevos,
        observaciones
    ) VALUES (
        NEW.id_archivo,
        'INSERT',
        USER(),
        JSON_OBJECT(
            'id_archivo', NEW.id_archivo,
            'nombre_archivo', NEW.nombre_archivo,
            'tipo_operacion', NEW.tipo_operacion,
            'estado_procesamiento', NEW.estado_procesamiento
        ),
        'Nuevo archivo Excel registrado'
    );
END$$

-- Trigger: Auditar UPDATE en archivo_excel_gestion_clientes
DROP TRIGGER IF EXISTS trg_auditoria_archivo_excel_update$$
CREATE TRIGGER trg_auditoria_archivo_excel_update
AFTER UPDATE ON archivo_excel_gestion_clientes
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_archivo_excel (
        id_archivo,
        tipo_operacion,
        usuario,
        datos_anteriores,
        datos_nuevos,
        observaciones
    ) VALUES (
        NEW.id_archivo,
        'UPDATE',
        USER(),
        JSON_OBJECT(
            'estado_procesamiento', OLD.estado_procesamiento,
            'registros_procesados', OLD.registros_procesados
        ),
        JSON_OBJECT(
            'estado_procesamiento', NEW.estado_procesamiento,
            'registros_procesados', NEW.registros_procesados
        ),
        'Archivo Excel actualizado'
    );
END$$

DELIMITER ;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT 'Triggers de auditoría creados exitosamente' AS Mensaje;
