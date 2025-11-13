-- =====================================================
-- SISTEMA DE GESTIÓN DE CLIENTES JP
-- Script de creación de base de datos
-- Versión: 1.0
-- Fecha: 2025-11-13
-- =====================================================

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS gestion_clientes_jp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gestion_clientes_jp;

-- =====================================================
-- TABLA: cliente
-- Descripción: Almacena información de clientes
-- =====================================================
DROP TABLE IF EXISTS cliente;
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(11) UNIQUE NOT NULL COMMENT 'RUC del cliente (11 dígitos)',
    razon_social VARCHAR(255) NOT NULL COMMENT 'Razón social o nombre comercial',
    nombre_comercial VARCHAR(255) COMMENT 'Nombre comercial',
    direccion TEXT COMMENT 'Dirección fiscal',
    distrito VARCHAR(100) COMMENT 'Distrito',
    provincia VARCHAR(100) COMMENT 'Provincia',
    departamento VARCHAR(100) COMMENT 'Departamento',
    telefono VARCHAR(20) COMMENT 'Teléfono de contacto',
    email VARCHAR(150) COMMENT 'Correo electrónico',
    contacto_nombre VARCHAR(255) COMMENT 'Nombre del contacto principal',
    contacto_cargo VARCHAR(100) COMMENT 'Cargo del contacto',
    contacto_telefono VARCHAR(20) COMMENT 'Teléfono del contacto',
    contacto_email VARCHAR(150) COMMENT 'Email del contacto',
    estado ENUM('ACTIVO', 'INACTIVO', 'SUSPENDIDO') DEFAULT 'ACTIVO',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    observaciones TEXT COMMENT 'Observaciones adicionales',
    INDEX idx_ruc (ruc),
    INDEX idx_razon_social (razon_social),
    INDEX idx_estado (estado),
    INDEX idx_departamento (departamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabla de clientes del sistema';

-- =====================================================
-- TABLA: empleado
-- Descripción: Almacena información de empleados
-- =====================================================
DROP TABLE IF EXISTS empleado;
CREATE TABLE empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(8) UNIQUE NOT NULL COMMENT 'DNI del empleado',
    nombres VARCHAR(150) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE COMMENT 'Fecha de nacimiento',
    direccion TEXT COMMENT 'Dirección de domicilio',
    distrito VARCHAR(100),
    provincia VARCHAR(100),
    departamento VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(150),
    cargo VARCHAR(100) COMMENT 'Cargo del empleado',
    area VARCHAR(100) COMMENT 'Área de trabajo',
    fecha_ingreso DATE COMMENT 'Fecha de ingreso a la empresa',
    salario DECIMAL(10,2) COMMENT 'Salario mensual',
    estado ENUM('ACTIVO', 'INACTIVO', 'VACACIONES', 'LICENCIA') DEFAULT 'ACTIVO',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    observaciones TEXT,
    INDEX idx_dni (dni),
    INDEX idx_nombres (nombres, apellido_paterno),
    INDEX idx_cargo (cargo),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabla de empleados';

-- =====================================================
-- TABLA: consulta_sunat
-- Descripción: Almacena consultas realizadas a SUNAT
-- =====================================================
DROP TABLE IF EXISTS consulta_sunat;
CREATE TABLE consulta_sunat (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT COMMENT 'Cliente relacionado (puede ser NULL para consultas generales)',
    ruc_consultado VARCHAR(11) NOT NULL COMMENT 'RUC consultado',
    tipo_consulta ENUM('VALIDACION_RUC', 'ESTADO_CONTRIBUYENTE', 'COMPROBANTES', 'OTROS') DEFAULT 'VALIDACION_RUC',
    resultado_consulta TEXT COMMENT 'Resultado de la consulta en formato JSON o texto',
    estado_sunat VARCHAR(100) COMMENT 'Estado del contribuyente según SUNAT',
    condicion_sunat VARCHAR(100) COMMENT 'Condición del contribuyente',
    fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_consulta VARCHAR(100) COMMENT 'Usuario que realizó la consulta',
    observaciones TEXT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE SET NULL,
    INDEX idx_ruc_consultado (ruc_consultado),
    INDEX idx_tipo_consulta (tipo_consulta),
    INDEX idx_fecha_consulta (fecha_consulta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Tabla de consultas a SUNAT';

-- =====================================================
-- TABLA: archivo_excel_gestion_clientes
-- Descripción: Registro de archivos Excel procesados
-- =====================================================
DROP TABLE IF EXISTS archivo_excel_gestion_clientes;
CREATE TABLE archivo_excel_gestion_clientes (
    id_archivo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL COMMENT 'Nombre del archivo Excel',
    ruta_archivo TEXT COMMENT 'Ruta donde se almacenó el archivo',
    tipo_operacion ENUM('IMPORTACION', 'EXPORTACION', 'REPORTE') COMMENT 'Tipo de operación realizada',
    registros_procesados INT DEFAULT 0 COMMENT 'Cantidad de registros procesados',
    registros_exitosos INT DEFAULT 0 COMMENT 'Registros procesados con éxito',
    registros_con_error INT DEFAULT 0 COMMENT 'Registros con errores',
    fecha_procesamiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_procesamiento VARCHAR(100) COMMENT 'Usuario que procesó el archivo',
    estado_procesamiento ENUM('PENDIENTE', 'PROCESANDO', 'COMPLETADO', 'ERROR') DEFAULT 'PENDIENTE',
    log_errores TEXT COMMENT 'Log de errores durante el procesamiento',
    observaciones TEXT,
    INDEX idx_tipo_operacion (tipo_operacion),
    INDEX idx_fecha_procesamiento (fecha_procesamiento),
    INDEX idx_estado (estado_procesamiento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Registro de archivos Excel procesados';

-- =====================================================
-- TABLA: auditoria_cliente
-- Descripción: Auditoría de cambios en clientes
-- =====================================================
DROP TABLE IF EXISTS auditoria_cliente;
CREATE TABLE auditoria_cliente (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL COMMENT 'ID del cliente afectado',
    tipo_operacion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    usuario VARCHAR(100) COMMENT 'Usuario que realizó la operación',
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    datos_anteriores JSON COMMENT 'Datos antes de la operación',
    datos_nuevos JSON COMMENT 'Datos después de la operación',
    ip_origen VARCHAR(45) COMMENT 'Dirección IP de origen',
    observaciones TEXT,
    INDEX idx_cliente (id_cliente),
    INDEX idx_tipo_operacion (tipo_operacion),
    INDEX idx_fecha (fecha_operacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Auditoría de operaciones en clientes';

-- =====================================================
-- INSERTAR DATOS DE PRUEBA
-- =====================================================

-- Clientes de prueba
INSERT INTO cliente (ruc, razon_social, nombre_comercial, direccion, distrito, provincia, departamento, telefono, email, contacto_nombre, contacto_cargo, contacto_telefono, contacto_email, estado) VALUES
('20123456789', 'EMPRESA COMERCIAL SAC', 'Comercial SAC', 'Av. Principal 123', 'Lima', 'Lima', 'Lima', '01-2345678', 'contacto@comercial.com', 'Juan Pérez', 'Gerente General', '999888777', 'jperez@comercial.com', 'ACTIVO'),
('20987654321', 'SERVICIOS INTEGRALES EIRL', 'Servicios Int', 'Jr. Los Olivos 456', 'Miraflores', 'Lima', 'Lima', '01-3456789', 'info@servicios.com', 'María García', 'Administradora', '999777666', 'mgarcia@servicios.com', 'ACTIVO'),
('20555666777', 'DISTRIBUIDORA NORTE SA', 'Dist Norte', 'Calle Comercio 789', 'Los Olivos', 'Lima', 'Lima', '01-4567890', 'ventas@distnorte.com', 'Carlos López', 'Jefe de Ventas', '999666555', 'clopez@distnorte.com', 'ACTIVO'),
('20444555666', 'IMPORTACIONES GLOBALES SAC', 'Imp Global', 'Av. Industrial 321', 'Callao', 'Callao', 'Callao', '01-5678901', 'contacto@impglobal.com', 'Ana Torres', 'Gerente Comercial', '999555444', 'atorres@impglobal.com', 'ACTIVO'),
('20333444555', 'TECNOLOGÍA Y SISTEMAS PERU', 'Tech Systems', 'Jr. Tecnología 654', 'San Isidro', 'Lima', 'Lima', '01-6789012', 'info@techsystems.com', 'Roberto Díaz', 'Director TI', '999444333', 'rdiaz@techsystems.com', 'SUSPENDIDO');

-- Empleados de prueba
INSERT INTO empleado (dni, nombres, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, distrito, provincia, departamento, telefono, email, cargo, area, fecha_ingreso, salario, estado) VALUES
('12345678', 'Juan Carlos', 'Pérez', 'García', '1985-05-15', 'Av. Los Pinos 123', 'Lima', 'Lima', 'Lima', '987654321', 'jperez@jp.com', 'Gerente General', 'Gerencia', '2020-01-15', 8500.00, 'ACTIVO'),
('87654321', 'María Elena', 'López', 'Martínez', '1990-08-20', 'Jr. Las Flores 456', 'Miraflores', 'Lima', 'Lima', '987654322', 'mlopez@jp.com', 'Jefe de Ventas', 'Comercial', '2021-03-10', 5500.00, 'ACTIVO'),
('11223344', 'Carlos Alberto', 'Sánchez', 'Rojas', '1988-12-05', 'Calle Principal 789', 'San Isidro', 'Lima', 'Lima', '987654323', 'csanchez@jp.com', 'Contador', 'Contabilidad', '2019-06-01', 4500.00, 'ACTIVO'),
('55667788', 'Ana María', 'Torres', 'Vega', '1992-03-25', 'Av. Central 321', 'Surco', 'Lima', 'Lima', '987654324', 'atorres@jp.com', 'Asistente Administrativo', 'Administración', '2022-01-20', 2800.00, 'ACTIVO'),
('99887766', 'Roberto', 'Díaz', 'Flores', '1987-11-30', 'Jr. Comercio 654', 'Callao', 'Callao', 'Callao', '987654325', 'rdiaz@jp.com', 'Vendedor', 'Comercial', '2021-09-15', 3200.00, 'VACACIONES');

-- Consultas SUNAT de prueba
INSERT INTO consulta_sunat (id_cliente, ruc_consultado, tipo_consulta, estado_sunat, condicion_sunat, usuario_consulta) VALUES
(1, '20123456789', 'VALIDACION_RUC', 'ACTIVO', 'HABIDO', 'admin'),
(2, '20987654321', 'ESTADO_CONTRIBUYENTE', 'ACTIVO', 'HABIDO', 'admin'),
(3, '20555666777', 'VALIDACION_RUC', 'ACTIVO', 'HABIDO', 'admin'),
(4, '20444555666', 'ESTADO_CONTRIBUYENTE', 'ACTIVO', 'HABIDO', 'admin'),
(5, '20333444555', 'VALIDACION_RUC', 'SUSPENDIDO', 'NO HABIDO', 'admin');

-- Archivos Excel de prueba
INSERT INTO archivo_excel_gestion_clientes (nombre_archivo, tipo_operacion, registros_procesados, registros_exitosos, registros_con_error, usuario_procesamiento, estado_procesamiento) VALUES
('importacion_clientes_2025_01.xlsx', 'IMPORTACION', 150, 145, 5, 'admin', 'COMPLETADO'),
('reporte_clientes_activos.xlsx', 'EXPORTACION', 120, 120, 0, 'admin', 'COMPLETADO'),
('importacion_empleados_2025_01.xlsx', 'IMPORTACION', 45, 43, 2, 'admin', 'COMPLETADO');

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT 'Base de datos creada exitosamente' AS Mensaje;
SELECT COUNT(*) AS 'Total Clientes' FROM cliente;
SELECT COUNT(*) AS 'Total Empleados' FROM empleado;
SELECT COUNT(*) AS 'Total Consultas SUNAT' FROM consulta_sunat;
SELECT COUNT(*) AS 'Total Archivos Excel' FROM archivo_excel_gestion_clientes;
