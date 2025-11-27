# 🏢 Sistema de Gestión Empresarial

> Sistema integral de gestión de clientes, empleados y consultas tributarias desarrollado con Python y Tkinter

<!-- [Insertar aquí captura de pantalla del menú principal] -->

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características-principales)
- [Tecnologías](#️-tecnologías)
- [Requisitos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Base de Datos](#-base-de-datos)
- [Seguridad](#-seguridad)
- [Capturas](#-capturas-de-pantalla)
- [Licencia](#-licencia)

---

## 📝 Descripción

Sistema empresarial desarrollado en Python que integra múltiples módulos para la gestión eficiente de información comercial. Incluye autenticación de usuarios, control de permisos por roles, validación con APIs externas, generación de reportes y exportación de datos.

### Propósito
Centralizar la administración de información empresarial en una aplicación de escritorio robusta, intuitiva y segura.

---

## ✨ Características Principales

### 🔐 Autenticación y Seguridad
- **Sistema de login** con validación de credenciales
- **Control de acceso** basado en roles (Administrador/Contabilidad)
- **Auditoría completa** de accesos y acciones
- **Configuración segura** con variables de entorno (.env)

### 👥 Gestión de Clientes
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Validación de RUC (11 dígitos)
- Búsqueda y filtrado en tiempo real
- Información de contacto completa

### 👔 Gestión de Empleados
- Registro completo de personal
- Asignación a clientes
- Validación de fechas de nacimiento
- Cálculo automático de edad
- Gestión de cargos y datos personales

### 🔍 Consultas SUNAT
- **Integración con API de SUNAT** para validación de RUC
- Consulta de estado tributario en tiempo real
- Historial de consultas realizadas
- Validación de razón social, estado y condición

### 📊 Reportes y Análisis
- **13 reportes predefinidos** con consultas SQL complejas
- Exportación a CSV
- Reportes con JOINs múltiples
- Análisis de datos empresariales

### 📑 Gestión de Archivos Excel
- Registro de archivos del sistema
- Control de fechas de creación/modificación
- Auditoría de cambios

### ⚙️ Configuración del Sistema
- Visualización de estadísticas en tiempo real
- Información de base de datos
- Panel de información del sistema

---

## 🛠️ Tecnologías

### Backend
- **Python 3.8+** - Lenguaje principal
- **MySQL/MariaDB** - Base de datos relacional
- **mysql-connector-python** - Conector de BD

### Frontend
- **Tkinter** - Interfaz gráfica nativa
- **ttk** - Widgets modernos

### Librerías Adicionales
- **python-dotenv** - Gestión de variables de entorno
- **requests** - Consumo de APIs REST
- **matplotlib** - Visualización de datos
- **reportlab** - Generación de PDFs

---

## 📋 Requisitos Previos

### Software Necesario
- Python 3.8 o superior
- MySQL 5.7+ o MariaDB 10.x
- pip (gestor de paquetes de Python)
- Git (opcional)

### Sistema Operativo
- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, Arch, etc.)
- ✅ macOS

---

## 🚀 Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tuusuario/sistema-gestion.git
cd sistema-gestion
```

### 2. Crear Entorno Virtual
```bash
# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

**Crear la base de datos:**
```bash
mysql -u root -p
```

```sql
CREATE DATABASE gestion_clientes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

**Importar esquema:**
```bash
mysql -u root -p gestion_clientes < sql/database_schema.sql
mysql -u root -p gestion_clientes < sql/stored_procedures.sql
mysql -u root -p gestion_clientes < sql/triggers.sql
mysql -u root -p gestion_clientes < sql/functions.sql
mysql -u root -p gestion_clientes < sql/vistas.sql
mysql -u root -p gestion_clientes < sql/tabla_usuarios.sql
mysql -u root -p gestion_clientes < sql/datos_prueba.sql
```

---

## ⚙️ Configuración

### Crear archivo `.env`

Copiar el archivo de ejemplo y configurar:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
# Configuración de Base de Datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password_aqui
DB_NAME=gestion_clientes
DB_CHARSET=utf8mb4
```

⚠️ **IMPORTANTE:** El archivo `.env` está en `.gitignore` y NO debe subirse al repositorio.

---

## 🎯 Uso

### Iniciar la Aplicación

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# Ejecutar aplicación
python main.py
```

### Usuarios por Defecto

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `admin123` | Administrador | ✅ Acceso total (incluye eliminar) |
| `contabilidad` | `conta123` | Contabilidad | ✅ Registrar/Actualizar (sin eliminar) |

### Navegación

1. **Login:** Ingresar credenciales en la pantalla inicial
2. **Menú Principal:** Seleccionar módulo desde los botones principales
3. **Módulos:** Cada módulo tiene navegación con botón "Volver al Menú Principal"

<!-- [Insertar aquí captura del flujo de navegación] -->

---

## 📁 Estructura del Proyecto

```
sistema-gestion/
├── 📂 models/               # Modelos y lógica de negocio
│   ├── config_db.py         # Configuración de base de datos
│   └── sesion.py            # Gestión de sesión de usuario
├── 📂 views/                # Interfaces gráficas (Tkinter)
│   ├── login.py             # Ventana de autenticación
│   ├── modulo_clientes.py   # Gestión de clientes
│   ├── modulo_empleados.py  # Gestión de empleados
│   ├── modulo_consulta_sunat.py # Consultas SUNAT
│   ├── modulo_archivos_excel.py # Gestión de archivos
│   ├── modulo_reportes.py   # Reportes y análisis
│   └── modulo_configuracion.py # Configuración del sistema
├── 📂 controllers/          # Controladores
│   └── sunat_controller.py  # Lógica de consultas SUNAT
├── 📂 sql/                  # Scripts de base de datos
│   ├── database_schema.sql  # Esquema principal
│   ├── stored_procedures.sql # Procedimientos almacenados
│   ├── triggers.sql         # Triggers de auditoría
│   ├── functions.sql        # Funciones SQL
│   ├── vistas.sql           # Vistas
│   ├── tabla_usuarios.sql   # Sistema de usuarios
│   └── datos_prueba.sql     # Datos de ejemplo
├── 📂 venv/                 # Entorno virtual (ignorado en git)
├── 📄 main.py               # Punto de entrada de la aplicación
├── 📄 requirements.txt      # Dependencias de Python
├── 📄 .env.example          # Ejemplo de configuración
├── 📄 .env                  # Configuración (NO subir a git)
├── 📄 .gitignore            # Archivos ignorados por git
├── 📄 LICENSE               # Licencia del proyecto
├── 📄 README.md             # Este archivo
└── 📄 PRUEBAS_LOGIN_ROLES.md # Guía de pruebas
```

---

## 🗄️ Base de Datos

### Esquema Principal

#### Tablas Principales
- **`cliente`** - Información de clientes
- **`empleado`** - Información de empleados
- **`consulta_sunat`** - Historial de consultas SUNAT
- **`archivo_excel_gestion_clientes`** - Registro de archivos
- **`usuarios`** - Sistema de autenticación

#### Tablas de Auditoría
- **`auditoria_cliente`** - Log de cambios en clientes
- **`auditoria_empleado`** - Log de cambios en empleados
- **`auditoria_archivo_excel`** - Log de cambios en archivos
- **`auditoria_accesos`** - Log de accesos al sistema

### Diagrama ER

<!-- [Insertar aquí diagrama de entidad-relación] -->

### Stored Procedures

El sistema incluye **13 procedimientos almacenados** para operaciones CRUD:
- `insertar_cliente`, `actualizar_cliente`, `eliminar_cliente`
- `insertar_empleado`, `actualizar_empleado`, `eliminar_empleado`
- `insertar_consulta_sunat`
- `insertar_archivo_excel`, `actualizar_archivo_excel`
- `registrar_acceso`
- Y más...

### Triggers

**9 triggers de auditoría** que registran automáticamente:
- Inserciones (AFTER INSERT)
- Actualizaciones (AFTER UPDATE)
- Eliminaciones (AFTER DELETE)

### Funciones SQL

**20+ funciones personalizadas** para:
- Validaciones (RUC, email, teléfono)
- Cálculos (edad, antigüedad)
- Formateado de datos

---

## 🔒 Seguridad

### Implementado

✅ **Variables de entorno** - Credenciales fuera del código
✅ **Sistema de autenticación** - Login obligatorio
✅ **Control de permisos** - Roles con permisos diferenciados
✅ **Auditoría completa** - Log de todas las acciones
✅ **Validaciones** - Frontend y backend
✅ **Conexiones seguras** - Manejo correcto de conexiones BD

### Recomendaciones para Producción

⚠️ **Hashear contraseñas** con bcrypt o Argon2
⚠️ **Certificados SSL** para conexiones a BD
⚠️ **Rate limiting** en consultas a APIs
⚠️ **Backups automáticos** de base de datos
⚠️ **Timeout de sesión** para usuarios inactivos

---

## 📸 Capturas de Pantalla

### Pantalla de Login
<!-- [Insertar captura de pantalla de login] -->

### Menú Principal
<!-- [Insertar captura de menú principal con header de usuario] -->

### Módulo de Clientes
<!-- [Insertar captura del módulo de clientes] -->

### Módulo de Empleados
<!-- [Insertar captura del módulo de empleados] -->

### Consultas SUNAT
<!-- [Insertar captura de consultas SUNAT con API] -->

### Reportes
<!-- [Insertar captura del módulo de reportes] -->

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Changelog

### Versión 3.0.0 (Actual)
- ✅ Sistema de autenticación con roles
- ✅ Control de permisos por usuario
- ✅ Navegación mejorada entre módulos
- ✅ Configuración segura con .env
- ✅ Integración con API SUNAT
- ✅ 13 reportes empresariales
- ✅ Auditoría completa de acciones

### Versión 2.0.0
- CRUD completo de todos los módulos
- Stored procedures y triggers
- Validaciones frontend/backend

### Versión 1.0.0
- Versión inicial con funcionalidad básica

---

## 🐛 Reporte de Bugs

Si encuentras un bug, por favor crea un issue con:
- Descripción detallada del problema
- Pasos para reproducirlo
- Comportamiento esperado vs. actual
- Capturas de pantalla (si aplica)
- Información del sistema (OS, versión Python, etc.)

---

## 📧 Contacto

Para consultas sobre el proyecto, por favor abre un issue en el repositorio.

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- Comunidad de Python
- Documentación de Tkinter
- Colaboradores del proyecto
- API SUNAT del Perú

---

## 🎓 Proyecto Académico

Este sistema fue desarrollado como proyecto académico para la materia de Base de Datos.

**Objetivos cumplidos:**
- ✅ Diseño de base de datos relacional
- ✅ Implementación de CRUD
- ✅ Stored procedures y triggers
- ✅ Funciones SQL personalizadas
- ✅ Consultas complejas con JOINs
- ✅ Integración con APIs externas
- ✅ Interfaz gráfica de usuario
- ✅ Sistema de autenticación

---

<div align="center">

**Desarrollado con ❤️ usando Python y Tkinter**

⭐ Si te gustó este proyecto, considera darle una estrella en GitHub

[🔝 Volver arriba](#-sistema-de-gestión-empresarial)

</div>
