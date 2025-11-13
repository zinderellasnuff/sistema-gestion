# 🏢 Sistema de Gestión de Clientes JP

**JP Business Solutions - Sistema Empresarial v1.0**

Sistema integral de gestión empresarial desarrollado en Python con interfaz gráfica Tkinter y base de datos MySQL.

---

## 📋 Descripción del Proyecto

Sistema de gestión empresarial que permite administrar clientes, empleados, consultas SUNAT y archivos Excel. El proyecto se encuentra en **30% de avance** con funcionalidades core implementadas.

## ✅ Estado de Implementación (30%)

### Completado

- ✅ Conexión exitosa con base de datos MySQL
- ✅ Interfaz gráfica principal con navegación entre módulos
- ✅ Módulo de Gestión de Clientes completo (CRUD)
- ✅ Procedimientos almacenados básicos (insertar, actualizar, eliminar)
- ✅ Triggers de auditoría para tabla cliente, empleado, consulta_sunat y archivo_excel
- ✅ 5 consultas SQL de reportes implementadas
- ✅ Módulo básico de Gestión de Empleados
- ✅ Módulo básico de Consultas SUNAT
- ✅ Módulo básico de Archivos Excel
- ✅ Estética mejorada al 30%

### Pendiente (70%)

- ⏳ Completar módulos de Empleados, Consultas SUNAT y Archivos Excel
- ⏳ Implementar 8 consultas SQL restantes
- ⏳ Desarrollar procedimientos almacenados para todas las tablas
- ⏳ Sistema de autenticación y permisos de usuario
- ⏳ Funcionalidad de exportación de reportes a PDF y Excel
- ⏳ Optimización de interfaz gráfica con estilos y temas visuales
- ⏳ Pruebas exhaustivas de validación y seguridad

---

## 🏗️ Arquitectura del Sistema

El aplicativo desarrollado sigue una **arquitectura de tres capas** que separa claramente la lógica de presentación, la lógica de negocio y la capa de acceso a datos. Esta separación facilita el mantenimiento, la escalabilidad y la reutilización del código.

### Capa de Presentación (Vista)
- **Ubicación:** `views/`
- **Tecnología:** Tkinter (Python)
- **Responsabilidad:** Proporciona la interfaz gráfica de usuario con ventanas, formularios, botones y tablas para la interacción con el sistema.
- **Módulos:** Cada módulo funcional (Gestión de Clientes, Gestión de Empleados, Consultas SUNAT, Archivos Excel) tiene su propia ventana independiente con controles específicos.

### Capa de Lógica de Negocio (Controlador)
- **Ubicación:** `controllers/`
- **Responsabilidad:** Contiene las clases y métodos que implementan las reglas de negocio, validaciones y coordinan las operaciones entre la vista y el modelo.
- **Funciones:** Valida los datos ingresados por el usuario antes de enviarlos a la base de datos y procesa las respuestas para mostrarlas en la interfaz.

### Capa de Acceso a Datos (Modelo)
- **Ubicación:** `models/`
- **Tecnología:** mysql-connector-python
- **Responsabilidad:** Gestiona la conexión con la base de datos MySQL. Ejecuta las consultas SQL, procedimientos almacenados y triggers, devolviendo los resultados a la capa de lógica de negocio.
- **Optimización:** Implementa un patrón Singleton para optimizar las conexiones.

---

## 🚀 Características Principales

### 1. Gestión de Clientes
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Búsqueda y filtrado de clientes
- Validación de RUC
- Auditoría automática de cambios

### 2. Gestión de Empleados
- Lista de empleados con detalles completos
- Visualización por cargo y área
- Control de salarios y estados

### 3. Consultas SUNAT
- Consulta de RUC en tiempo real
- Historial de consultas realizadas
- Validación de estado de contribuyente

### 4. Archivos Excel
- Importación de datos desde Excel
- Exportación de reportes
- Historial de archivos procesados

### 5. Sistema de Auditoría
- Triggers automáticos para todas las operaciones
- Registro de cambios con datos anteriores y nuevos
- Trazabilidad completa

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.x
- **GUI:** Tkinter
- **Base de Datos:** MySQL 8.0+
- **Driver:** mysql-connector-python 8.2.0

---

## 📦 Instalación

### Requisitos Previos

- Python 3.8 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd gestionclientesjp
```

### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Configurar la base de datos

1. Crear la base de datos:

```bash
mysql -u root -p < sql/database_schema.sql
```

2. Crear procedimientos almacenados:

```bash
mysql -u root -p gestion_clientes_jp < sql/stored_procedures.sql
```

3. Crear triggers de auditoría:

```bash
mysql -u root -p gestion_clientes_jp < sql/triggers.sql
```

### Paso 4: Configurar credenciales

Editar el archivo `models/config_db.py` con tus credenciales de MySQL:

```python
CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'gestion_clientes_jp',
    'charset': 'utf8mb4'
}
```

### Paso 5: Ejecutar la aplicación

```bash
python main.py
```

---

## 📁 Estructura del Proyecto

```
gestionclientesjp/
│
├── main.py                          # Aplicación principal (punto de entrada)
│
├── views/                           # CAPA DE PRESENTACIÓN (Vista)
│   ├── __init__.py
│   ├── modulo_clientes.py          # Vista: Gestión de clientes
│   ├── modulo_empleados.py         # Vista: Gestión de empleados
│   ├── modulo_consulta_sunat.py    # Vista: Consultas SUNAT
│   └── modulo_archivos_excel.py    # Vista: Archivos Excel
│
├── controllers/                     # CAPA DE LÓGICA DE NEGOCIO (Controlador)
│   └── __init__.py                 # Validaciones y reglas de negocio
│
├── models/                          # CAPA DE ACCESO A DATOS (Modelo)
│   ├── __init__.py
│   └── config_db.py                # Configuración y conexión a BD
│
├── sql/                            # Scripts SQL
│   ├── database_schema.sql         # Esquema de base de datos
│   ├── stored_procedures.sql       # Procedimientos almacenados
│   ├── triggers.sql                # Triggers de auditoría
│   └── consultas_reportes.sql      # Consultas SQL de reportes
│
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Documentación
```

---

## 🗄️ Estructura de Base de Datos

### Tablas Principales

1. **cliente** - Información de clientes
2. **empleado** - Información de empleados
3. **consulta_sunat** - Historial de consultas SUNAT
4. **archivo_excel_gestion_clientes** - Registro de archivos Excel

### Tablas de Auditoría

1. **auditoria_cliente** - Auditoría de cambios en clientes
2. **auditoria_empleado** - Auditoría de cambios en empleados
3. **auditoria_consulta_sunat** - Auditoría de consultas SUNAT
4. **auditoria_archivo_excel** - Auditoría de archivos Excel

---

## 📊 Reportes Implementados

1. **Reporte 1:** Clientes Activos por Departamento
2. **Reporte 2:** Empleados por Área con Salarios
3. **Reporte 3:** Consultas SUNAT por Tipo
4. **Reporte 4:** Resumen de Archivos Excel Procesados
5. **Reporte 5:** Auditoría de Clientes (Últimas 30 operaciones)

### Vista Dashboard

- Total de clientes activos, inactivos y suspendidos
- Total de empleados activos y nómina total
- Consultas SUNAT del día
- Archivos procesados
- Operaciones del día

---

## 🎨 Interfaz Gráfica

### Características de Diseño

- **Paleta de colores corporativa:** Azul (#0047AB) como color principal
- **Diseño modular:** Tarjetas independientes para cada módulo
- **Efectos visuales:** Hover effects en tarjetas y botones
- **Responsive:** Adaptable a diferentes tamaños de pantalla
- **Iconos:** Uso de emojis para mejor UX

### Módulos de la Interfaz

- 🏢 Panel de Control Principal
- 👥 Gestión de Clientes
- 👔 Gestión de Empleados
- 🔍 Consultas SUNAT
- 📊 Archivos Excel
- 📈 Reportes y Análisis
- ⚙️ Configuración

---

## 🔒 Seguridad

### Implementado

- Validación de conexión a base de datos
- Transacciones con rollback automático
- Triggers de auditoría para trazabilidad

### Por Implementar

- Sistema de autenticación de usuarios
- Encriptación de contraseñas
- Control de permisos por rol
- Prevención de SQL Injection
- Logs de seguridad

---

## 📝 Procedimientos Almacenados

### Clientes
- `sp_insertar_cliente` - Insertar nuevo cliente
- `sp_actualizar_cliente` - Actualizar cliente existente
- `sp_eliminar_cliente` - Desactivar cliente (eliminación lógica)

### Empleados
- `sp_insertar_empleado` - Insertar nuevo empleado
- `sp_actualizar_empleado` - Actualizar empleado
- `sp_eliminar_empleado` - Desactivar empleado

### Consultas SUNAT
- `sp_insertar_consulta_sunat` - Registrar consulta SUNAT
- `sp_eliminar_consulta_sunat` - Eliminar consulta

### Archivos Excel
- `sp_insertar_archivo_excel` - Registrar archivo procesado
- `sp_actualizar_estado_archivo_excel` - Actualizar estado de archivo

---

## 🧪 Datos de Prueba

El sistema incluye datos de prueba en la base de datos:

- 5 clientes de ejemplo
- 5 empleados de ejemplo
- 5 consultas SUNAT de ejemplo
- 3 archivos Excel de ejemplo

---

## 🔧 Configuración Avanzada

### Cambiar Puerto de MySQL

Editar `config_db.py`:

```python
CONFIG = {
    'host': 'localhost',
    'port': 3307,  # Puerto personalizado
    # ... resto de configuración
}
```

### Cambiar Charset

El charset por defecto es `utf8mb4` para soportar emojis y caracteres especiales.

---

## 🐛 Solución de Problemas

### Error de Conexión a MySQL

**Problema:** `Error: Can't connect to MySQL server`

**Solución:**
1. Verificar que MySQL esté corriendo
2. Verificar credenciales en `config_db.py`
3. Verificar puerto de MySQL

### Error de Importación de Módulos

**Problema:** `ModuleNotFoundError: No module named 'mysql'`

**Solución:**
```bash
pip install mysql-connector-python==8.2.0
```

### Base de Datos No Existe

**Problema:** `Unknown database 'gestion_clientes_jp'`

**Solución:**
```bash
mysql -u root -p < database_schema.sql
```

---

## 📅 Roadmap de Desarrollo

### Fase 1 (Actual - 30%)
- ✅ Estructura de base de datos
- ✅ Módulos básicos
- ✅ CRUD de clientes

### Fase 2 (40%)
- Completar CRUD de empleados
- Sistema de autenticación
- Permisos de usuario

### Fase 3 (60%)
- Exportación a PDF y Excel
- Reportes avanzados
- Dashboard con gráficos

### Fase 4 (80%)
- Consultas SUNAT en tiempo real (API)
- Optimización de rendimiento
- Testing automatizado

### Fase 5 (100%)
- Documentación completa
- Deploy en producción
- Capacitación de usuarios

---

## 👥 Créditos

**Desarrollado por:** JP Business Solutions
**Versión:** 1.0 (30% completado)
**Fecha:** 2025-11-13

---

## 📄 Licencia

© 2025 JP Business Solutions. Todos los derechos reservados.

---

## 📞 Soporte

Para soporte técnico o consultas:
- Email: soporte@jpbusiness.com
- Teléfono: (01) 234-5678

---

## 🔄 Actualizaciones

### v1.0 (2025-11-13)
- Versión inicial del sistema
- Módulos básicos implementados
- Base de datos configurada
- Interfaz gráfica mejorada
