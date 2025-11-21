-- =====================================================
-- PROCEDIMIENTOS ALMACENADOS - Adaptados a estructura REAL
-- Sistema de Gestión de Clientes JP
-- Versión: 2.1 
-- =====================================================

USE gestion_clientes_jp;

DELIMITER $$

-- =====================================================
-- PROCEDIMIENTOS PARA: cliente
-- Estructura REAL: ruc, nombres, apellido_paterno, apellido_materno,
--                  correo_electronico, pagina_web, telefono
-- =====================================================

-- Insertar cliente
DROP PROCEDURE IF EXISTS insertar_cliente$$
CREATE PROCEDURE insertar_cliente(
    IN p_ruc CHAR(11),
    IN p_nombres VARCHAR(50),
    IN p_apellido_paterno VARCHAR(50),
    IN p_apellido_materno VARCHAR(50),
    IN p_correo_electronico VARCHAR(100),
    IN p_pagina_web VARCHAR(200),
    IN p_telefono CHAR(9)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar cliente';
    END;

    START TRANSACTION;

    INSERT INTO cliente (ruc, nombres, apellido_paterno, apellido_materno,
                        correo_electronico, pagina_web, telefono)
    VALUES (p_ruc, p_nombres, p_apellido_paterno, p_apellido_materno,
            p_correo_electronico, p_pagina_web, p_telefono);

    COMMIT;
    SELECT p_ruc AS ruc_insertado;
END$$

-- Actualizar cliente
DROP PROCEDURE IF EXISTS actualizar_cliente;
CREATE PROCEDURE actualizar_cliente(
    IN p_ruc CHAR(11),
    IN p_nombres VARCHAR(50),
    IN p_apellido_paterno VARCHAR(50),
    IN p_apellido_materno VARCHAR(50),
    IN p_correo_electronico VARCHAR(100),
    IN p_pagina_web VARCHAR(200),
    IN p_telefono CHAR(9)
)
BEGIN
    UPDATE cliente SET
        nombres = p_nombres,
        apellido_paterno = p_apellido_paterno,
        apellido_materno = p_apellido_materno,
        correo_electronico = p_correo_electronico,
        pagina_web = p_pagina_web,
        telefono = p_telefono
    WHERE ruc = p_ruc;
END$$

-- Eliminar cliente

CREATE PROCEDURE eliminar_cliente(
    IN p_ruc CHAR(11)
)
BEGIN
    DELETE FROM cliente WHERE ruc = p_ruc;
END$$

-- Buscar cliente por RUC
DROP PROCEDURE IF EXISTS buscar_cliente_por_ruc$$
CREATE PROCEDURE buscar_cliente_por_ruc(
    IN p_ruc CHAR(11)
)
BEGIN
    SELECT ruc, nombres, apellido_paterno, apellido_materno,
           correo_electronico, pagina_web, telefono
    FROM cliente
    WHERE ruc = p_ruc;
END$$

-- Listar todos los clientes
DROP PROCEDURE IF EXISTS listar_clientes$$
CREATE PROCEDURE listar_clientes()
BEGIN
    SELECT ruc, nombres, apellido_paterno, apellido_materno,
           correo_electronico, pagina_web, telefono
    FROM cliente
    ORDER BY nombres, apellido_paterno;
END$$

-- =====================================================
-- PROCEDIMIENTOS PARA: empleado
-- Estructura REAL: codigo, sexo, cargo, fecha_nacimiento, nombres,
--                  apellido_paterno, apellido_materno, ruc_cliente, nombre_archivo
-- =====================================================

-- Insertar empleado
DROP PROCEDURE IF EXISTS insertar_empleado$$
CREATE PROCEDURE insertar_empleado(
    IN p_codigo INT,
    IN p_sexo VARCHAR(10),
    IN p_cargo VARCHAR(50),
    IN p_fecha_nacimiento DATE,
    IN p_nombres VARCHAR(50),
    IN p_apellido_paterno VARCHAR(20),
    IN p_apellido_materno VARCHAR(20),
    IN p_ruc_cliente CHAR(11),
    IN p_nombre_archivo VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar empleado';
    END;

    START TRANSACTION;

    INSERT INTO empleado (codigo, sexo, cargo, fecha_nacimiento, nombres,
                         apellido_paterno, apellido_materno, ruc_cliente, nombre_archivo)
    VALUES (p_codigo, p_sexo, p_cargo, p_fecha_nacimiento, p_nombres,
            p_apellido_paterno, p_apellido_materno, p_ruc_cliente, p_nombre_archivo);

    COMMIT;
    SELECT p_codigo AS codigo_insertado;
END$$

-- Actualizar empleado
DROP PROCEDURE IF EXISTS actualizar_empleado$$
CREATE PROCEDURE actualizar_empleado(
    IN p_codigo INT,
    IN p_sexo VARCHAR(10),
    IN p_cargo VARCHAR(50),
    IN p_fecha_nacimiento DATE,
    IN p_nombres VARCHAR(50),
    IN p_apellido_paterno VARCHAR(20),
    IN p_apellido_materno VARCHAR(20),
    IN p_ruc_cliente CHAR(11),
    IN p_nombre_archivo VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al actualizar empleado';
    END;

    START TRANSACTION;

    UPDATE empleado SET
        sexo = p_sexo,
        cargo = p_cargo,
        fecha_nacimiento = p_fecha_nacimiento,
        nombres = p_nombres,
        apellido_paterno = p_apellido_paterno,
        apellido_materno = p_apellido_materno,
        ruc_cliente = p_ruc_cliente,
        nombre_archivo = p_nombre_archivo
    WHERE codigo = p_codigo;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

-- Eliminar empleado
DROP PROCEDURE IF EXISTS eliminar_empleado$$
CREATE PROCEDURE eliminar_empleado(
    IN p_codigo INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al eliminar empleado';
    END;

    START TRANSACTION;

    DELETE FROM empleado WHERE codigo = p_codigo;

    COMMIT;
    SELECT ROW_COUNT() AS filas_afectadas;
END$$

-- Listar empleados
DROP PROCEDURE IF EXISTS listar_empleados$$
CREATE PROCEDURE listar_empleados()
BEGIN
    SELECT codigo, sexo, cargo, fecha_nacimiento, nombres,
           apellido_paterno, apellido_materno, ruc_cliente, nombre_archivo
    FROM empleado
    ORDER BY nombres, apellido_paterno;
END$$

-- =====================================================
-- PROCEDIMIENTOS PARA: consulta_sunat
-- Estructura REAL: nro_consultado, codigo_empleado, razon_social, estado, condicion
-- =====================================================

-- Insertar consulta SUNAT
DROP PROCEDURE IF EXISTS insertar_consulta_sunat$$
CREATE PROCEDURE insertar_consulta_sunat(
    IN p_nro_consultado VARCHAR(20),
    IN p_codigo_empleado INT,
    IN p_razon_social VARCHAR(200),
    IN p_estado VARCHAR(20),
    IN p_condicion VARCHAR(20)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar consulta SUNAT';
    END;

    START TRANSACTION;

    INSERT INTO consulta_sunat (nro_consultado, codigo_empleado, razon_social, estado, condicion)
    VALUES (p_nro_consultado, p_codigo_empleado, p_razon_social, p_estado, p_condicion);

    COMMIT;
    SELECT 'Consulta SUNAT insertada' AS mensaje;
END$$

-- Listar consultas SUNAT
DROP PROCEDURE IF EXISTS listar_consultas_sunat$$
CREATE PROCEDURE listar_consultas_sunat()
BEGIN
    SELECT nro_consultado, codigo_empleado, razon_social, estado, condicion
    FROM consulta_sunat
    ORDER BY nro_consultado;
END$$

-- =====================================================
-- PROCEDIMIENTOS PARA: archivo_excel_gestion_clientes
-- Estructura REAL: nombre, fecha_creacion, fecha_modificacion
-- =====================================================

-- Insertar archivo Excel
DROP PROCEDURE IF EXISTS insertar_archivo_excel$$
CREATE PROCEDURE insertar_archivo_excel(
    IN p_nombre VARCHAR(100),
    IN p_fecha_creacion DATETIME,
    IN p_fecha_modificacion DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al insertar archivo Excel';
    END;

    START TRANSACTION;

    INSERT INTO archivo_excel_gestion_clientes (nombre, fecha_creacion, fecha_modificacion)
    VALUES (p_nombre, p_fecha_creacion, p_fecha_modificacion);

    COMMIT;
    SELECT p_nombre AS archivo_insertado;
END$$

-- Actualizar archivo Excel
DROP PROCEDURE IF EXISTS actualizar_archivo_excel$$
CREATE PROCEDURE actualizar_archivo_excel(
    IN p_nombre VARCHAR(100),
    IN p_fecha_modificacion DATETIME
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error al actualizar archivo Excel';
    END;

    START TRANSACTION;

    UPDATE archivo_excel_gestion_clientes
    SET fecha_modificacion = p_fecha_modificacion
    WHERE nombre = p_nombre;

    COMMIT;
    -- ✅ Ya no devuelve resultado, así evita el error "Unread result found"
END$$

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT '✓✓✓ Procedimientos almacenados creados exitosamente ✓✓✓' AS Mensaje;
SELECT '✓ Sin prefijo sp_ para coincidir con llamadas Python' AS Mensaje;
