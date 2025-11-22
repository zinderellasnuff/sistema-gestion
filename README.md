# Sistema de Gestión de Clientes JP

Sistema de gestión integral para clientes, empleados y consultas SUNAT desarrollado en Python con Tkinter y MySQL.

---

## 📋 Descripción

Aplicación de escritorio para JP Ingeniería y Servicios S.R.L. que permite gestionar clientes, empleados, consultas SUNAT y archivos Excel con auditoría automática y generación de reportes.

**Proyecto académico** - Curso de Diseño de Bases de Datos, UCSM Arequipa, Perú.

---

## ✨ Características

- ✅ **Gestión de Clientes**: CRUD completo con validaciones (RUC, email, teléfono)
- ✅ **Gestión de Empleados**: CRUD con cálculo de edad y asignación a clientes
- ✅ **Consultas SUNAT**: Registro de consultas RUC con estados y condiciones
- ✅ **Archivos Excel**: Importación y procesamiento automático
- ✅ **Reportes**: 13 reportes diferentes con exportación a Excel/PDF
- ✅ **Auditoría**: 9 triggers automáticos que registran todos los cambios

---

## 🛠️ Tecnologías

- **Python 3.8+** con Tkinter
- **MySQL 8.0+** / MariaDB 10.5+
- **mysql-connector-python** - Conexión a BD
- **openpyxl** - Manejo de Excel
- **pandas** - Análisis de datos
- **reportlab** - Generación de PDFs

---

## 📦 Instalación

### 1. Clonar repositorio
```bash
git clone https://github.com/[usuario]/gestion-clientes-jp.git
cd gestion-clientes-jp
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos
```bash
mysql -u root -p
```
```sql
CREATE DATABASE gestion_clientes_jp;
USE gestion_clientes_jp;
```

### 4. Ejecutar scripts SQL (en orden)
```bash
mysql -u root -p gestion_clientes_jp < sql/database_schema.sql
mysql -u root -p gestion_clientes_jp < sql/functions.sql
mysql -u root -p gestion_clientes_jp < sql/stored_procedures.sql
mysql -u root -p gestion_clientes_jp < sql/triggers.sql
mysql -u root -p gestion_clientes_jp < sql/vistas.sql
mysql -u root -p gestion_clientes_jp < sql/datos_prueba.sql
```

### 5. Configurar conexión
Editar `models/config_db.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'tu_password',
    'database': 'gestion_clientes_jp'
}
```

### 6. Ejecutar aplicación
```bash
python main.py
```

---

## 📁 Estructura del Proyecto

```
gestionclientesjp/
├── main.py                          # Archivo principal
├── requirements.txt                 # Dependencias
├── README.md                        # Este archivo
│
├── models/                          # Modelos y configuración
│   ├── __init__.py
│   └── config_db.py                 # Configuración de BD
│
├── views/                           # Módulos de la aplicación
│   ├── __init__.py
│   ├── modulo_clientes.py           # CRUD Clientes
│   ├── modulo_empleados.py          # CRUD Empleados
│   ├── modulo_consulta_sunat.py     # Registro consultas SUNAT
│   ├── modulo_archivos_excel.py     # Importación Excel
│   └── modulo_reportes.py           # 13 reportes
│
└── sql/                             # Scripts de base de datos
    ├── database_schema.sql          # Estructura de tablas
    ├── functions.sql                # 20 funciones SQL
    ├── stored_procedures.sql        # 13 procedimientos
    ├── triggers.sql                 # 9 triggers de auditoría
    ├── vistas.sql                   # 2 vistas
    ├── consultas_reportes.sql       # Consultas para reportes
    └── datos_prueba.sql             # Datos de prueba
```

---

## 🗄️ Base de Datos

### Tablas principales (7)
- `cliente` - Datos de clientes
- `empleado` - Datos de empleados
- `consulta_sunat` - Consultas RUC a SUNAT
- `archivo_excel_gestion_clientes` - Archivos importados
- `auditoria_cliente` - Auditoría de clientes
- `auditoria_empleado` - Auditoría de empleados
- `auditoria_archivo_excel` - Auditoría de archivos

### Componentes SQL
- **13 Procedimientos almacenados** - Todas las operaciones CRUD
- **20 Funciones** - Validaciones y cálculos
- **9 Triggers** - Auditoría automática (INSERT/UPDATE/DELETE)
- **2 Vistas** - Dashboard y clientes con empleados
- **13 Reportes** - 6+ con consultas JOIN

---

## 📊 Módulos del Sistema

### 1. Módulo Clientes
- Registrar, buscar, actualizar y eliminar clientes
- Validación de RUC (11 dígitos)
- Validación de correo y teléfono
- Búsqueda en tiempo real

### 2. Módulo Empleados
- CRUD completo de empleados
- Asignación a clientes
- Validación de edad (mayor de 18 años)
- Filtrado por cargo y sexo

### 3. Módulo Consultas SUNAT
- Registro de consultas RUC
- Estados: ACTIVO, BAJA, SUSPENDIDO
- Condiciones: HABIDO, NO HABIDO
- Historial de consultas

### 4. Módulo Archivos Excel
- Importación de archivos .xlsx
- Validación de estructura
- Procesamiento automático
- Historial de importaciones

### 5. Módulo Reportes
- 13 reportes diferentes
- Exportación a Excel y PDF
- Dashboard con estadísticas
- Consultas con JOIN

---

## 📈 Reportes Disponibles

1. **Dashboard Principal** - Estadísticas generales
2. **Listado Completo de Clientes**
3. **Clientes con Empleados Asignados** (JOIN)
4. **Empleados por Cliente** (JOIN)
5. **Consultas SUNAT Activas**
6. **Consultas SUNAT por Empleado** (JOIN)
7. **Empleados sin Cliente Asignado** (LEFT JOIN)
8. **Clientes sin Empleados** (LEFT JOIN)
9. **Empleados Mayores de 30 Años**
10. **Archivos Excel Importados**
11. **Auditoría de Clientes**
12. **Auditoría de Empleados**
13. **Auditoría de Archivos Excel**

---

## 🔧 Requisitos del Sistema

### Software
- Python 3.8 o superior
- MySQL 8.0+ o MariaDB 10.5+
- pip (gestor de paquetes)

### Hardware Mínimo
- Procesador: Intel Core i3 o equivalente
- RAM: 4 GB mínimo
- Disco: 500 MB libres
- Resolución: 1366x768

---

## 📝 Uso Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar base de datos
mysql -u root -p < sql/database_schema.sql

# 3. Ejecutar scripts SQL en orden (ver instalación)

# 4. Configurar conexión en models/config_db.py

# 5. Ejecutar aplicación
python main.py
```

---

## 🧪 Datos de Prueba

Después de ejecutar `datos_prueba.sql`:

**Clientes:**
- RUC: 20123456789 - Empresa Constructora SAC
- RUC: 20987654321 - Servicios Integrales EIRL

**Empleados:**
- Código: 1 - Juan Pérez
- Código: 2 - María García

---

## 📚 Documentación Adicional

- **Manual de Usuario** - `docs/Manual_Usuario.docx`
- **Memoria Descriptiva** - `docs/Memoria_Descriptiva.docx`
- **Modelo Físico de BD** - Diagrama de base de datos
- **Scripts SQL** - Carpeta `sql/`

---

## 📄 Licencia

Este proyecto es de uso académico para fines educativos.

---

## 🙏 Agradecimientos

- JP Ingeniería y Servicios S.R.L.
- Universidad Católica de Santa María (UCSM)
- Docentes del curso de Diseño de Bases de Datos

---

**Última actualización:** Noviembre 2024
