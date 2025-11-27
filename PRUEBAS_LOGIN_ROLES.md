# 🧪 GUÍA DE PRUEBAS - Sistema de Login y Roles

## 📋 Usuarios de Prueba

### 👑 Usuario Administrador
```
Usuario: admin
Contraseña: admin123
Rol: Administrador
```
**Permisos:**
- ✅ Ver todos los módulos
- ✅ Crear/Registrar datos
- ✅ Actualizar datos
- ✅ **ELIMINAR datos** (solo este rol)
- ✅ Generar reportes
- ✅ Exportar archivos

---

### 👔 Usuario Contabilidad
```
Usuario: contabilidad
Contraseña: conta123
Rol: Contabilidad
```
**Permisos:**
- ✅ Ver todos los módulos
- ✅ Crear/Registrar datos
- ✅ Actualizar datos
- ❌ **NO puede ELIMINAR** (botón deshabilitado)
- ✅ Generar reportes
- ✅ Exportar archivos

---

## 🧪 Plan de Pruebas

### PASO 1: Prueba con Usuario Admin

1. **Iniciar aplicación:**
   ```bash
   cd /home/nexus/Projects/gestionclientesjp
   source venv/bin/activate
   python main.py
   ```

2. **Login como Admin:**
   - Usuario: `admin`
   - Contraseña: `admin123`
   - Verificar: Aparece mensaje "Bienvenido Administrador del Sistema"

3. **Verificar Header:**
   - ✅ Debe mostrar: "👤 Administrador del Sistema"
   - ✅ Debe mostrar: "🔐 Administrador"

4. **Probar Módulo Clientes:**
   - Abrir módulo Clientes
   - ✅ Botón "🗑️ Eliminar" debe estar **HABILITADO** (color rojo)
   - ✅ Click en cliente → Click Eliminar → Debe funcionar

5. **Probar Módulo Empleados:**
   - Abrir módulo Empleados
   - ✅ Botón "🗑️ Eliminar" debe estar **HABILITADO** (color rojo)
   - ✅ Click en empleado → Click Eliminar → Debe funcionar

6. **Cerrar sesión**

---

### PASO 2: Prueba con Usuario Contabilidad

1. **Reiniciar aplicación**

2. **Login como Contabilidad:**
   - Usuario: `contabilidad`
   - Contraseña: `conta123`
   - Verificar: Aparece mensaje "Bienvenido Usuario Contabilidad"

3. **Verificar Header:**
   - ✅ Debe mostrar: "👤 Usuario Contabilidad"
   - ✅ Debe mostrar: "🔐 Contabilidad"

4. **Probar Módulo Clientes:**
   - Abrir módulo Clientes
   - ✅ Botón "🗑️ Eliminar" debe estar **DESHABILITADO** (color gris)
   - ✅ Al pasar el mouse sobre "Eliminar" → Tooltip: "⚠️ Solo Administradores pueden eliminar"
   - ✅ Botones "✚ Nuevo", "💾 Guardar", "🔄 Actualizar" deben estar **HABILITADOS**
   - ✅ Crear nuevo cliente → Debe funcionar
   - ✅ Actualizar cliente → Debe funcionar

5. **Probar Módulo Empleados:**
   - Abrir módulo Empleados
   - ✅ Botón "🗑️ Eliminar" debe estar **DESHABILITADO** (color gris)
   - ✅ Tooltip al pasar mouse: "⚠️ Solo Administradores pueden eliminar"
   - ✅ Crear nuevo empleado → Debe funcionar
   - ✅ Actualizar empleado → Debe funcionar

6. **Probar Módulo Consulta SUNAT:**
   - Abrir módulo Consulta SUNAT
   - ✅ Todos los botones habilitados
   - ✅ Puede consultar RUC
   - ✅ Puede guardar consultas

7. **Probar Módulo Reportes:**
   - Abrir módulo Reportes
   - ✅ Puede generar reportes
   - ✅ Puede exportar a CSV

8. **Probar Módulo Archivos Excel:**
   - Abrir módulo Archivos Excel
   - ✅ Puede registrar archivos
   - ✅ Puede actualizar fechas

9. **Probar Módulo Configuración:**
   - Abrir módulo Configuración
   - ✅ Puede ver estadísticas
   - ✅ Puede ver información BD

---

## ✅ Checklist de Verificación

### Seguridad
- [ ] Login rechaza credenciales incorrectas
- [ ] No se puede acceder sin login
- [ ] Sesión persiste en toda la aplicación
- [ ] Permisos se aplican correctamente

### Interfaz
- [ ] Header muestra usuario actual
- [ ] Header muestra rol actual
- [ ] Botones se deshabilitan según rol
- [ ] Tooltips aparecen correctamente
- [ ] Colores indican estado (rojo activo, gris deshabilitado)

### Funcionalidad
- [ ] Admin puede eliminar en Clientes
- [ ] Admin puede eliminar en Empleados
- [ ] Contabilidad NO puede eliminar en Clientes
- [ ] Contabilidad NO puede eliminar en Empleados
- [ ] Ambos roles pueden crear/actualizar
- [ ] Ambos roles pueden generar reportes
- [ ] Ambos roles pueden consultar SUNAT

---

## 🐛 Problemas Conocidos

Ninguno por el momento.

---

## 📝 Notas

- Las contraseñas están en texto plano por simplicidad
- En producción usar bcrypt para hashear passwords
- La tabla `auditoria_accesos` registra todos los intentos de login
- El procedimiento `registrar_acceso` actualiza fecha de último acceso

---

## 🎯 Próximas Mejoras

1. Agregar botón "Cerrar Sesión" en header
2. Implementar timeout de sesión
3. Mostrar último acceso en ventana de configuración
4. Agregar historial de acciones por usuario
