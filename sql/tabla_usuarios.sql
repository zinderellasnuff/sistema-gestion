-- ============================================
-- TABLA DE USUARIOS Y SISTEMA DE AUTENTICACIÓN
-- Sistema de Gestión Empresarial
-- ============================================

USE gestion_clientes;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('Administrador', 'Contabilidad') NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL,
    intentos_fallidos INT DEFAULT 0,
    INDEX idx_usuario (usuario),
    INDEX idx_rol (rol),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar usuarios por defecto
-- Contraseñas en texto plano por simplicidad (en producción usar bcrypt)
INSERT INTO usuarios (usuario, password, rol, nombre_completo, email) VALUES
('admin', 'admin123', 'Administrador', 'Administrador del Sistema', 'admin@system.local'),
('contabilidad', 'conta123', 'Contabilidad', 'Usuario Contabilidad', 'contabilidad@system.local')
ON DUPLICATE KEY UPDATE
    password = VALUES(password),
    rol = VALUES(rol);

-- Crear tabla de auditoría de accesos
CREATE TABLE IF NOT EXISTS auditoria_accesos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    usuario VARCHAR(50) NOT NULL,
    accion VARCHAR(50) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    exitoso BOOLEAN DEFAULT TRUE,
    detalles TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_fecha (fecha_hora)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Procedimiento para registrar acceso
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS registrar_acceso(
    IN p_usuario_id INT,
    IN p_usuario VARCHAR(50),
    IN p_accion VARCHAR(50),
    IN p_exitoso BOOLEAN,
    IN p_detalles TEXT
)
BEGIN
    INSERT INTO auditoria_accesos (usuario_id, usuario, accion, exitoso, detalles)
    VALUES (p_usuario_id, p_usuario, p_accion, p_exitoso, p_detalles);

    -- Actualizar último acceso si fue exitoso
    IF p_exitoso THEN
        UPDATE usuarios
        SET ultimo_acceso = CURRENT_TIMESTAMP,
            intentos_fallidos = 0
        WHERE id = p_usuario_id;
    ELSE
        UPDATE usuarios
        SET intentos_fallidos = intentos_fallidos + 1
        WHERE id = p_usuario_id;
    END IF;
END //

DELIMITER ;

-- Verificar que se crearon las tablas
SELECT 'Tabla usuarios creada correctamente' AS mensaje;
SELECT * FROM usuarios;
