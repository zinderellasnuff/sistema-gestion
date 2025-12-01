-- =====================================================
-- DATOS DE PRUEBA - Sistema de Gestión Empresarial
-- Versión: 1.0
-- =====================================================

USE gestion_clientes;

-- =====================================================
-- INSERTAR CLIENTES DE PRUEBA
-- =====================================================

INSERT INTO cliente (ruc, nombres, apellido_paterno, apellido_materno, correo_electronico, pagina_web, telefono) VALUES
('20100070970', 'Juan Carlos', 'García', 'López', 'jgarcia@example1.com', 'www.empresa1.com', '987654321'),
('20100123456', 'María Elena', 'Rodríguez', 'Sánchez', 'mrodriguez@example2.com', 'www.empresa2.com', '987654322'),
('20100234567', 'Pedro José', 'Martínez', 'Fernández', 'pmartinez@example3.com', NULL, '987654323'),
('20100345678', 'Ana Lucía', 'González', 'Torres', NULL, 'www.empresa4.com', '987654324'),
('20100456789', 'Luis Alberto', 'Pérez', 'Ramírez', 'lperez@example5.com', 'www.empresa5.com', '987654325'),
('20100567890', 'Carmen Rosa', 'López', 'Díaz', 'clopez@example6.com', NULL, NULL),
('20100678901', 'Roberto Carlos', 'Hernández', 'Vargas', 'rhernandez@example7.com', 'www.empresa7.com', '987654327'),
('20100789012', 'Patricia Isabel', 'Flores', 'Castro', NULL, NULL, '987654328'),
('20100890123', 'Jorge Luis', 'Silva', 'Morales', 'jsilva@example9.com', 'www.empresa9.com', '987654329'),
('20100901234', 'Sofía Mercedes', 'Rojas', 'Gutiérrez', 'srojas@example10.com', 'www.empresa10.com', '987654330'),
('20101012345', 'Fernando Antonio', 'Medina', 'Navarro', 'fmedina@example11.com', NULL, '987654331'),
('20101123456', 'Gabriela Beatriz', 'Castillo', 'Herrera', 'gcastillo@example12.com', 'www.empresa12.com', '987654332'),
('20101234567', 'Diego Alejandro', 'Reyes', 'Paredes', NULL, 'www.empresa13.com', NULL),
('20101345678', 'Valentina Lucía', 'Mendoza', 'Chávez', 'vmendoza@example14.com', 'www.empresa14.com', '987654334'),
('20101456789', 'Andrés Felipe', 'Ruiz', 'Domínguez', 'aruiz@example15.com', NULL, '987654335');

-- =====================================================
-- INSERTAR EMPLEADOS DE PRUEBA
-- =====================================================

INSERT INTO empleado (codigo, sexo, cargo, fecha_nacimiento, nombres, apellido_paterno, apellido_materno, ruc_cliente, nombre_archivo) VALUES
(1001, 'Masculino', 'Gerente General', '1985-03-15', 'Carlos', 'Ramírez', 'Quispe', '20100070970', 'clientes_2025'),
(1002, 'Femenino', 'Gerente de Ventas', '1990-07-22', 'María', 'Flores', 'Gonzales', '20100123456', 'clientes_2025'),
(1003, 'Masculino', 'Supervisor', '1988-11-10', 'Juan', 'Torres', 'Mamani', '20100234567', 'clientes_2025'),
(1004, 'Femenino', 'Asistente', '1995-05-18', 'Ana', 'Silva', 'Condori', '20100345678', 'clientes_2025'),
(1005, 'Masculino', 'Ejecutivo Comercial', '1992-09-25', 'Pedro', 'Gutiérrez', 'Huamán', '20100456789', 'clientes_2025'),
(1006, 'Femenino', 'Ejecutiva Comercial', '1993-01-30', 'Laura', 'Mendoza', 'Ticona', '20100567890', 'clientes_2025'),
(1007, 'Masculino', 'Supervisor', '1987-04-12', 'Roberto', 'Castro', 'Apaza', '20100678901', 'clientes_2025'),
(1008, 'Femenino', 'Asistente', '1996-08-20', 'Isabel', 'Vargas', 'Choque', '20100789012', 'clientes_2025'),
(1009, 'Masculino', 'Ejecutivo Comercial', '1991-12-05', 'Miguel', 'Paredes', 'Nina', '20100890123', 'clientes_2025'),
(1010, 'Femenino', 'Gerente de Operaciones', '1989-06-14', 'Sofía', 'Herrera', 'Ccama', '20100901234', 'clientes_2025'),
(1011, 'Masculino', 'Analista', '1994-02-28', 'Fernando', 'Díaz', 'Mullisaca', NULL, 'clientes_2025'),
(1012, 'Femenino', 'Analista', '1993-10-17', 'Gabriela', 'Morales', 'Puma', NULL, 'clientes_2025'),
(1013, 'Masculino', 'Asistente', '1997-03-22', 'Diego', 'Navarro', 'Chambilla', NULL, 'clientes_2025');

-- =====================================================
-- INSERTAR CONSULTAS SUNAT DE PRUEBA
-- =====================================================

INSERT INTO consulta_sunat (nro_consultado, codigo_empleado, razon_social, estado, condicion) VALUES
('20100070970', 1001, 'EMPRESA UNO S.A.C.', 'ACTIVO', 'HABIDO'),
('20100123456', 1002, 'COMERCIAL DOS E.I.R.L.', 'ACTIVO', 'HABIDO'),
('20100234567', 1003, 'SERVICIOS TRES S.R.L.', 'ACTIVO', 'HABIDO'),
('20100345678', 1004, 'INDUSTRIAS CUATRO S.A.', 'ACTIVO', 'NO HABIDO'),
('20100456789', 1005, 'DISTRIBUIDORA CINCO S.A.C.', 'ACTIVO', 'HABIDO'),
('20100567890', 1006, 'CONSULTORA SEIS E.I.R.L.', 'BAJA', 'HABIDO'),
('20100678901', 1007, 'LOGÍSTICA SIETE S.R.L.', 'ACTIVO', 'HABIDO'),
('20100789012', 1008, 'TECNOLOGÍA OCHO S.A.', 'ACTIVO', 'NO HABIDO'),
('20100890123', 1009, 'INVERSIONES NUEVE S.A.C.', 'ACTIVO', 'HABIDO'),
('20100901234', 1010, 'GRUPO DIEZ S.R.L.', 'ACTIVO', 'HABIDO'),
('20101012345', 1001, 'COMERCIO ONCE E.I.R.L.', 'SUSPENDIDO', 'HABIDO'),
('20101123456', 1002, 'SERVICIOS DOCE S.A.C.', 'ACTIVO', 'HABIDO'),
('20101234567', 1003, 'INDUSTRIAS TRECE S.A.', 'ACTIVO', 'NO HABIDO'),
('20101345678', 1004, 'DISTRIBUIDORA CATORCE S.R.L.', 'ACTIVO', 'HABIDO'),
('20101456789', 1005, 'CONSULTORA QUINCE E.I.R.L.', 'ACTIVO', 'HABIDO');

-- =====================================================
-- INSERTAR MÁS ARCHIVOS EXCEL DE PRUEBA
-- =====================================================

INSERT INTO archivo_excel_gestion_clientes (nombre, fecha_creacion, fecha_modificacion) VALUES
('Clientes_2024_Q1.xlsx', '2024-01-15 08:00:00', '2024-01-20 10:30:00'),
('Clientes_2024_Q2.xlsx', '2024-04-10 09:15:00', '2024-04-15 14:20:00'),
('Clientes_2024_Q3.xlsx', '2024-07-05 10:30:00', '2024-07-10 16:45:00'),
('Clientes_2024_Q4.xlsx', '2024-10-01 11:00:00', '2024-10-05 09:30:00'),
('Backup_Enero_2025.xlsx', '2025-01-05 08:00:00', '2025-01-10 12:00:00'),
('Backup_Febrero_2025.xlsx', '2025-02-01 08:00:00', '2025-02-05 15:30:00'),
('Backup_Marzo_2025.xlsx', '2025-03-01 08:00:00', '2025-03-05 11:45:00'),
('Reporte_Anual_2024.xlsx', '2024-12-20 10:00:00', '2024-12-31 17:00:00');

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================
SELECT '✓✓✓ Datos de prueba insertados exitosamente ✓✓✓' AS Mensaje;
SELECT CONCAT('✓ ', COUNT(*), ' Clientes insertados') AS Resumen FROM cliente;
SELECT CONCAT('✓ ', COUNT(*), ' Empleados insertados') AS Resumen FROM empleado;
SELECT CONCAT('✓ ', COUNT(*), ' Consultas SUNAT insertadas') AS Resumen FROM consulta_sunat;
SELECT CONCAT('✓ ', COUNT(*), ' Archivos Excel registrados') AS Resumen FROM archivo_excel_gestion_clientes;
