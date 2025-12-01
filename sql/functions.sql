-- =====================================================
-- FUNCIONES SQL - Sistema de Gestión Empresarial
-- Versión: 1.0
-- =====================================================

USE gestion_clientes;

DELIMITER $$

-- =====================================================
-- FUNCIONES PARA CLIENTES
-- =====================================================

-- Función 1: Obtener nombre completo del cliente
DROP FUNCTION IF EXISTS fn_nombre_completo_cliente$$
CREATE FUNCTION fn_nombre_completo_cliente(p_ruc CHAR(11))
RETURNS VARCHAR(150)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_nombre_completo VARCHAR(150);
    
    SELECT CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno)
    INTO v_nombre_completo
    FROM cliente
    WHERE ruc = p_ruc;
    
    RETURN IFNULL(v_nombre_completo, 'Cliente no encontrado');
END$$

-- Función 2: Validar formato de RUC (11 dígitos)
DROP FUNCTION IF EXISTS fn_validar_ruc$$
CREATE FUNCTION fn_validar_ruc(p_ruc VARCHAR(20))
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    RETURN (p_ruc REGEXP '^[0-9]{11}$');
END$$

-- Función 3: Contar total de clientes
DROP FUNCTION IF EXISTS fn_contar_clientes$$
CREATE FUNCTION fn_contar_clientes()
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;
    
    SELECT COUNT(*) INTO v_total FROM cliente;
    
    RETURN v_total;
END$$

-- Función 4: Verificar si un cliente tiene datos completos
DROP FUNCTION IF EXISTS fn_cliente_datos_completos$$
CREATE FUNCTION fn_cliente_datos_completos(p_ruc CHAR(11))
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_completo BOOLEAN DEFAULT FALSE;
    
    SELECT 
        CASE 
            WHEN correo_electronico IS NOT NULL 
                 AND telefono IS NOT NULL 
                 AND pagina_web IS NOT NULL 
            THEN TRUE
            ELSE FALSE
        END INTO v_completo
    FROM cliente
    WHERE ruc = p_ruc;
    
    RETURN IFNULL(v_completo, FALSE);
END$$

-- Función 5: Obtener email del cliente
DROP FUNCTION IF EXISTS fn_obtener_email_cliente$$
CREATE FUNCTION fn_obtener_email_cliente(p_ruc CHAR(11))
RETURNS VARCHAR(100)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_email VARCHAR(100);
    
    SELECT correo_electronico INTO v_email
    FROM cliente
    WHERE ruc = p_ruc;
    
    RETURN IFNULL(v_email, 'Sin correo');
END$$

-- =====================================================
-- FUNCIONES PARA EMPLEADOS
-- =====================================================

-- Función 6: Calcular edad del empleado
DROP FUNCTION IF EXISTS fn_calcular_edad$$
CREATE FUNCTION fn_calcular_edad(p_fecha_nacimiento DATE)
RETURNS INT
DETERMINISTIC
NO SQL
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, p_fecha_nacimiento, CURDATE());
END$$

-- Función 7: Obtener nombre completo del empleado
DROP FUNCTION IF EXISTS fn_nombre_completo_empleado$$
CREATE FUNCTION fn_nombre_completo_empleado(p_codigo INT)
RETURNS VARCHAR(150)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_nombre_completo VARCHAR(150);
    
    SELECT CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno)
    INTO v_nombre_completo
    FROM empleado
    WHERE codigo = p_codigo;
    
    RETURN IFNULL(v_nombre_completo, 'Empleado no encontrado');
END$$

-- Función 8: Contar empleados por cargo
DROP FUNCTION IF EXISTS fn_contar_empleados_por_cargo$$
CREATE FUNCTION fn_contar_empleados_por_cargo(p_cargo VARCHAR(50))
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;
    
    SELECT COUNT(*) INTO v_total
    FROM empleado
    WHERE cargo = p_cargo;
    
    RETURN v_total;
END$$

-- Función 9: Verificar si empleado tiene cliente asignado
DROP FUNCTION IF EXISTS fn_empleado_tiene_cliente$$
CREATE FUNCTION fn_empleado_tiene_cliente(p_codigo INT)
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_tiene_cliente BOOLEAN;
    
    SELECT 
        CASE 
            WHEN ruc_cliente IS NOT NULL THEN TRUE
            ELSE FALSE
        END INTO v_tiene_cliente
    FROM empleado
    WHERE codigo = p_codigo;
    
    RETURN IFNULL(v_tiene_cliente, FALSE);
END$$

-- Función 10: Contar clientes asignados a un empleado
DROP FUNCTION IF EXISTS fn_contar_clientes_por_empleado$$
CREATE FUNCTION fn_contar_clientes_por_empleado(p_codigo INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;
    
    SELECT COUNT(*) INTO v_total
    FROM empleado
    WHERE codigo = p_codigo AND ruc_cliente IS NOT NULL;
    
    RETURN v_total;
END$$

-- =====================================================
-- FUNCIONES PARA CONSULTAS SUNAT
-- =====================================================

-- Función 11: Verificar si RUC está activo en SUNAT
DROP FUNCTION IF EXISTS fn_ruc_activo_sunat$$
CREATE FUNCTION fn_ruc_activo_sunat(p_nro_consultado VARCHAR(20))
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_activo BOOLEAN;
    
    SELECT 
        CASE 
            WHEN estado = 'ACTIVO' AND condicion = 'HABIDO' THEN TRUE
            ELSE FALSE
        END INTO v_activo
    FROM consulta_sunat
    WHERE nro_consultado = p_nro_consultado
    LIMIT 1;
    
    RETURN IFNULL(v_activo, FALSE);
END$$

-- Función 12: Contar consultas SUNAT por empleado
DROP FUNCTION IF EXISTS fn_contar_consultas_sunat$$
CREATE FUNCTION fn_contar_consultas_sunat(p_codigo_empleado INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;
    
    SELECT COUNT(*) INTO v_total
    FROM consulta_sunat
    WHERE codigo_empleado = p_codigo_empleado;
    
    RETURN v_total;
END$$

-- Función 13: Obtener razón social desde SUNAT
DROP FUNCTION IF EXISTS fn_obtener_razon_social$$
CREATE FUNCTION fn_obtener_razon_social(p_nro_consultado VARCHAR(20))
RETURNS VARCHAR(200)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_razon_social VARCHAR(200);
    
    SELECT razon_social INTO v_razon_social
    FROM consulta_sunat
    WHERE nro_consultado = p_nro_consultado
    LIMIT 1;
    
    RETURN IFNULL(v_razon_social, 'No consultado');
END$$

-- =====================================================
-- FUNCIONES DE ESTADÍSTICAS GENERALES
-- =====================================================

-- Función 14: Contar total de empleados
DROP FUNCTION IF EXISTS fn_contar_empleados$$
CREATE FUNCTION fn_contar_empleados()
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;
    
    SELECT COUNT(*) INTO v_total FROM empleado;
    
    RETURN v_total;
END$$

-- Función 15: Calcular porcentaje de clientes con datos completos
DROP FUNCTION IF EXISTS fn_porcentaje_clientes_completos$$
CREATE FUNCTION fn_porcentaje_clientes_completos()
RETURNS DECIMAL(5,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total INT;
    DECLARE v_completos INT;
    DECLARE v_porcentaje DECIMAL(5,2);
    
    SELECT COUNT(*) INTO v_total FROM cliente;
    
    SELECT COUNT(*) INTO v_completos
    FROM cliente
    WHERE correo_electronico IS NOT NULL 
          AND telefono IS NOT NULL 
          AND pagina_web IS NOT NULL;
    
    IF v_total > 0 THEN
        SET v_porcentaje = (v_completos / v_total) * 100;
    ELSE
        SET v_porcentaje = 0;
    END IF;
    
    RETURN v_porcentaje;
END$$

-- Función 16: Obtener cargo de un empleado
DROP FUNCTION IF EXISTS fn_obtener_cargo_empleado$$
CREATE FUNCTION fn_obtener_cargo_empleado(p_codigo INT)
RETURNS VARCHAR(50)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_cargo VARCHAR(50);
    
    SELECT cargo INTO v_cargo
    FROM empleado
    WHERE codigo = p_codigo;
    
    RETURN IFNULL(v_cargo, 'Empleado no encontrado');
END$$

-- Función 17: Verificar si cliente existe
DROP FUNCTION IF EXISTS fn_cliente_existe$$
CREATE FUNCTION fn_cliente_existe(p_ruc CHAR(11))
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_existe BOOLEAN;
    
    SELECT COUNT(*) > 0 INTO v_existe
    FROM cliente
    WHERE ruc = p_ruc;
    
    RETURN v_existe;
END$$

-- Función 18: Verificar si empleado existe
DROP FUNCTION IF EXISTS fn_empleado_existe$$
CREATE FUNCTION fn_empleado_existe(p_codigo INT)
RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_existe BOOLEAN;
    
    SELECT COUNT(*) > 0 INTO v_existe
    FROM empleado
    WHERE codigo = p_codigo;
    
    RETURN v_existe;
END$$

-- Función 19: Obtener días desde última modificación de archivo
DROP FUNCTION IF EXISTS fn_dias_desde_modificacion$$
CREATE FUNCTION fn_dias_desde_modificacion(p_nombre VARCHAR(100))
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_dias INT;
    
    SELECT TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) INTO v_dias
    FROM archivo_excel_gestion_clientes
    WHERE nombre = p_nombre;
    
    RETURN IFNULL(v_dias, -1);
END$$

-- Función 20: Validar formato de teléfono (9 dígitos)
DROP FUNCTION IF EXISTS fn_validar_telefono$$
CREATE FUNCTION fn_validar_telefono(p_telefono VARCHAR(20))
RETURNS BOOLEAN
DETERMINISTIC
NO SQL
BEGIN
    RETURN (p_telefono REGEXP '^[0-9]{9}$');
END$$

DELIMITER ;

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT '✓✓✓ Funciones SQL creadas exitosamente ✓✓✓' AS Mensaje;
SELECT '✓ 20 funciones disponibles para uso en el sistema' AS Mensaje;

-- =====================================================
-- EJEMPLOS DE USO DE LAS FUNCIONES
-- =====================================================

-- Ejemplo 1: Obtener nombre completo de un cliente
-- SELECT fn_nombre_completo_cliente('20000000001');

-- Ejemplo 2: Validar un RUC
-- SELECT fn_validar_ruc('20000000001');

-- Ejemplo 3: Calcular edad de empleado
-- SELECT fn_calcular_edad('1990-05-15');

-- Ejemplo 4: Contar total de clientes
-- SELECT fn_contar_clientes();

-- Ejemplo 5: Verificar si cliente tiene datos completos
-- SELECT fn_cliente_datos_completos('20000000001');

-- Ejemplo 6: Obtener porcentaje de clientes con datos completos
-- SELECT fn_porcentaje_clientes_completos();

-- Ejemplo 7: Contar empleados por cargo
-- SELECT fn_contar_empleados_por_cargo('Gerente');

-- Ejemplo 8: Verificar si RUC está activo en SUNAT
-- SELECT fn_ruc_activo_sunat('20000000001');