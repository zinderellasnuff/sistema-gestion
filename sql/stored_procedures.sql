-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS
-- Sistema de Gestión de Clientes JP
-- =====================================================

USE gestion_clientes_jp;

DELIMITER $$

-- =====================================================
-- PROCEDIMIENTOS PARA TABLA: cliente
-- =====================================================

-- Procedimiento: Insertar Cliente
DROP PROCEDURE IF EXISTS sp_insertar_cliente$$
CREATE PROCEDURE sp_insertar_cliente(
    IN p_ruc VARCHAR(11),
    IN p_razon_social VARCHAR(255),
    IN p_nombre_comercial VARCHAR(255),
    IN p_direccion TEXT,
    IN p_distrito VARCHAR(100),
    IN p_provincia VARCHAR(100),
    IN p_departamento VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_email VARCHAR(150),
    IN p_contacto_nombre VARCHAR(255),
    IN p_contacto_cargo VARCHAR(100),
    IN p_contacto_telefono VARCHAR(20),
    IN p_contacto_email VARCHAR(150),
    IN p_observaciones TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar cliente';
    END;

    START TRANSACTION;

    INSERT INTO cliente (
        ruc, razon_social, nombre_comercial, direccion, distrito, provincia,
        departamento, telefono, email, contacto_nombre, contacto_cargo,
        contacto_telefono, contacto_email, observaciones
    ) VALUES (
        p_ruc, p_razon_social, p_nombre_comercial, p_direccion, p_distrito,
        p_provincia, p_departamento, p_telefono, p_email, p_contacto_nombre,
        p_contacto_cargo, p_contacto_telefono, p_contacto_email, p_observaciones
    );

    COMMIT;
    SELECT LAST_INSERT_ID() AS id_cliente;
END$$

-- Procedimiento: Actualizar Cliente
DROP PROCEDURE IF EXISTS sp_actualizar_cliente$$
CREATE PROCEDURE sp_actualizar_cliente(
    IN p_id_cliente INT,
    IN p_ruc VARCHAR(11),
    IN p_razon_social VARCHAR(255),
    IN p_nombre_comercial VARCHAR(255),
    IN p_direccion TEXT,
    IN p_distrito VARCHAR(100),
    IN p_provincia VARCHAR(100),
    IN p_departamento VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_email VARCHAR(150),
    IN p_contacto_nombre VARCHAR(255),
    IN p_contacto_cargo VARCHAR(100),
    IN p_contacto_telefono VARCHAR(20),
    IN p_contacto_email VARCHAR(150),
    IN p_estado VARCHAR(20),
    IN p_observaciones TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al actualizar cliente';
    END;

    START TRANSACTION;

    UPDATE cliente SET
        ruc = p_ruc,
        razon_social = p_razon_social,
        nombre_comercial = p_nombre_comercial,
        direccion = p_direccion,
        distrito = p_distrito,
        provincia = p_provincia,
        departamento = p_departamento,
        telefono = p_telefono,
        email = p_email,
        contacto_nombre = p_contacto_nombre,
        contacto_cargo = p_contacto_cargo,
        contacto_telefono = p_contacto_telefono,
        contacto_email = p_contacto_email,
        estado = p_estado,
        observaciones = p_observaciones,
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id_cliente = p_id_cliente;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

-- Procedimiento: Eliminar Cliente (Lógico)
DROP PROCEDURE IF EXISTS sp_eliminar_cliente$$
CREATE PROCEDURE sp_eliminar_cliente(
    IN p_id_cliente INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al eliminar cliente';
    END;

    START TRANSACTION;

    UPDATE cliente
    SET estado = 'INACTIVO',
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id_cliente = p_id_cliente;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

-- =====================================================
-- PROCEDIMIENTOS PARA TABLA: empleado
-- =====================================================

-- Procedimiento: Insertar Empleado
DROP PROCEDURE IF EXISTS sp_insertar_empleado$$
CREATE PROCEDURE sp_insertar_empleado(
    IN p_dni VARCHAR(8),
    IN p_nombres VARCHAR(150),
    IN p_apellido_paterno VARCHAR(100),
    IN p_apellido_materno VARCHAR(100),
    IN p_fecha_nacimiento DATE,
    IN p_direccion TEXT,
    IN p_distrito VARCHAR(100),
    IN p_provincia VARCHAR(100),
    IN p_departamento VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_email VARCHAR(150),
    IN p_cargo VARCHAR(100),
    IN p_area VARCHAR(100),
    IN p_fecha_ingreso DATE,
    IN p_salario DECIMAL(10,2),
    IN p_observaciones TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar empleado';
    END;

    START TRANSACTION;

    INSERT INTO empleado (
        dni, nombres, apellido_paterno, apellido_materno, fecha_nacimiento,
        direccion, distrito, provincia, departamento, telefono, email,
        cargo, area, fecha_ingreso, salario, observaciones
    ) VALUES (
        p_dni, p_nombres, p_apellido_paterno, p_apellido_materno, p_fecha_nacimiento,
        p_direccion, p_distrito, p_provincia, p_departamento, p_telefono, p_email,
        p_cargo, p_area, p_fecha_ingreso, p_salario, p_observaciones
    );

    COMMIT;
    SELECT LAST_INSERT_ID() AS id_empleado;
END$$

-- Procedimiento: Actualizar Empleado
DROP PROCEDURE IF EXISTS sp_actualizar_empleado$$
CREATE PROCEDURE sp_actualizar_empleado(
    IN p_id_empleado INT,
    IN p_dni VARCHAR(8),
    IN p_nombres VARCHAR(150),
    IN p_apellido_paterno VARCHAR(100),
    IN p_apellido_materno VARCHAR(100),
    IN p_direccion TEXT,
    IN p_telefono VARCHAR(20),
    IN p_email VARCHAR(150),
    IN p_cargo VARCHAR(100),
    IN p_area VARCHAR(100),
    IN p_salario DECIMAL(10,2),
    IN p_estado VARCHAR(20),
    IN p_observaciones TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al actualizar empleado';
    END;

    START TRANSACTION;

    UPDATE empleado SET
        dni = p_dni,
        nombres = p_nombres,
        apellido_paterno = p_apellido_paterno,
        apellido_materno = p_apellido_materno,
        direccion = p_direccion,
        telefono = p_telefono,
        email = p_email,
        cargo = p_cargo,
        area = p_area,
        salario = p_salario,
        estado = p_estado,
        observaciones = p_observaciones,
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id_empleado = p_id_empleado;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

-- Procedimiento: Eliminar Empleado (Lógico)
DROP PROCEDURE IF EXISTS sp_eliminar_empleado$$
CREATE PROCEDURE sp_eliminar_empleado(
    IN p_id_empleado INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al eliminar empleado';
    END;

    START TRANSACTION;

    UPDATE empleado
    SET estado = 'INACTIVO',
        fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id_empleado = p_id_empleado;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

-- =====================================================
-- PROCEDIMIENTOS PARA TABLA: consulta_sunat
-- =====================================================

-- Procedimiento: Insertar Consulta SUNAT
DROP PROCEDURE IF EXISTS sp_insertar_consulta_sunat$$
CREATE PROCEDURE sp_insertar_consulta_sunat(
    IN p_id_cliente INT,
    IN p_ruc_consultado VARCHAR(11),
    IN p_tipo_consulta VARCHAR(50),
    IN p_resultado_consulta TEXT,
    IN p_estado_sunat VARCHAR(100),
    IN p_condicion_sunat VARCHAR(100),
    IN p_usuario_consulta VARCHAR(100),
    IN p_observaciones TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar consulta SUNAT';
    END;

    START TRANSACTION;

    INSERT INTO consulta_sunat (
        id_cliente, ruc_consultado, tipo_consulta, resultado_consulta,
        estado_sunat, condicion_sunat, usuario_consulta, observaciones
    ) VALUES (
        p_id_cliente, p_ruc_consultado, p_tipo_consulta, p_resultado_consulta,
        p_estado_sunat, p_condicion_sunat, p_usuario_consulta, p_observaciones
    );

    COMMIT;
    SELECT LAST_INSERT_ID() AS id_consulta;
END$$

-- Procedimiento: Eliminar Consulta SUNAT
DROP PROCEDURE IF EXISTS sp_eliminar_consulta_sunat$$
CREATE PROCEDURE sp_eliminar_consulta_sunat(
    IN p_id_consulta INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al eliminar consulta SUNAT';
    END;

    START TRANSACTION;

    DELETE FROM consulta_sunat WHERE id_consulta = p_id_consulta;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

-- =====================================================
-- PROCEDIMIENTOS PARA TABLA: archivo_excel_gestion_clientes
-- =====================================================

-- Procedimiento: Insertar Archivo Excel
DROP PROCEDURE IF EXISTS sp_insertar_archivo_excel$$
CREATE PROCEDURE sp_insertar_archivo_excel(
    IN p_nombre_archivo VARCHAR(255),
    IN p_ruta_archivo TEXT,
    IN p_tipo_operacion VARCHAR(50),
    IN p_registros_procesados INT,
    IN p_registros_exitosos INT,
    IN p_registros_con_error INT,
    IN p_usuario_procesamiento VARCHAR(100),
    IN p_estado_procesamiento VARCHAR(50),
    IN p_log_errores TEXT,
    IN p_observaciones TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar archivo Excel';
    END;

    START TRANSACTION;

    INSERT INTO archivo_excel_gestion_clientes (
        nombre_archivo, ruta_archivo, tipo_operacion, registros_procesados,
        registros_exitosos, registros_con_error, usuario_procesamiento,
        estado_procesamiento, log_errores, observaciones
    ) VALUES (
        p_nombre_archivo, p_ruta_archivo, p_tipo_operacion, p_registros_procesados,
        p_registros_exitosos, p_registros_con_error, p_usuario_procesamiento,
        p_estado_procesamiento, p_log_errores, p_observaciones
    );

    COMMIT;
    SELECT LAST_INSERT_ID() AS id_archivo;
END$$

-- Procedimiento: Actualizar Estado Archivo Excel
DROP PROCEDURE IF EXISTS sp_actualizar_estado_archivo_excel$$
CREATE PROCEDURE sp_actualizar_estado_archivo_excel(
    IN p_id_archivo INT,
    IN p_estado_procesamiento VARCHAR(50),
    IN p_registros_procesados INT,
    IN p_registros_exitosos INT,
    IN p_registros_con_error INT,
    IN p_log_errores TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al actualizar estado archivo';
    END;

    START TRANSACTION;

    UPDATE archivo_excel_gestion_clientes SET
        estado_procesamiento = p_estado_procesamiento,
        registros_procesados = p_registros_procesados,
        registros_exitosos = p_registros_exitosos,
        registros_con_error = p_registros_con_error,
        log_errores = p_log_errores
    WHERE id_archivo = p_id_archivo;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

DELIMITER ;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT 'Procedimientos almacenados creados exitosamente' AS Mensaje;
