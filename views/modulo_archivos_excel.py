"""
Módulo de Gestión de Archivos Excel
Sistema JP Business Solutions
Versión: 3.0 - Profesional con validaciones completas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime
import re

class GestionArchivosExcel:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Archivos Excel - JP Business Solutions")
        self.ventana.geometry("1400x700")
        self.ventana.configure(bg="#F5F5F5")
        
        # Configurar para que se cierre correctamente
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.archivos = []
        self.nombre_seleccionado = None

        self.crear_interfaz()
        self.cargar_archivos()

    def cerrar_ventana(self):
        """Cierra la ventana correctamente"""
        self.ventana.destroy()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#17A2B8", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="📊 GESTIÓN DE ARCHIVOS EXCEL",
            font=("Segoe UI", 16, "bold"),
            bg="#17A2B8",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Formulario
        panel_izq = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(
            panel_izq,
            text="Registro de Archivo Excel",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#17A2B8"
        ).pack(pady=15)

        # Frame para campos
        form_frame = tk.Frame(panel_izq, bg="white")
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Nombre (PK)
        self.crear_campo(form_frame, "Nombre Archivo: *", 0)
        self.entry_nombre = tk.Entry(form_frame, font=("Segoe UI", 10), width=35)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(Debe terminar en .xlsx o .xls)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=0, column=2, padx=5, sticky="w")

        # Fecha Creación (automática, solo lectura)
        self.crear_campo(form_frame, "Fecha Creación:", 1)
        self.entry_fecha_creacion = tk.Entry(
            form_frame, 
            font=("Segoe UI", 10), 
            width=35,
            state='readonly',
            bg="#F0F0F0"
        )
        self.entry_fecha_creacion.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(Se asigna automáticamente)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=1, column=2, padx=5, sticky="w")

        # Fecha Modificación (automática, solo lectura)
        self.crear_campo(form_frame, "Última Modificación:", 2)
        self.entry_fecha_modificacion = tk.Entry(
            form_frame, 
            font=("Segoe UI", 10), 
            width=35,
            state='readonly',
            bg="#F0F0F0"
        )
        self.entry_fecha_modificacion.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(Se actualiza automáticamente)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=2, column=2, padx=5, sticky="w")

        # Nota informativa
        info_label = tk.Label(
            form_frame,
            text="ℹ Este módulo registra metadatos de archivos Excel utilizados\n" +
                 "en el sistema de gestión de clientes JP Business Solutions.",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#666666",
            justify="left"
        )
        info_label.grid(row=3, column=0, columnspan=3, pady=20, padx=10, sticky="w")

        # Nota de campos obligatorios
        tk.Label(
            form_frame,
            text="* Campos obligatorios",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#DC3545"
        ).grid(row=4, column=0, columnspan=3, pady=5)

        # Botones de acción
        btn_frame = tk.Frame(panel_izq, bg="white")
        btn_frame.pack(pady=20)

        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "width": 15,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat",
            "pady": 10
        }

        btn_nuevo = tk.Button(
            btn_frame,
            text="✚ Nuevo",
            bg="#28A745",
            fg="white",
            command=self.nuevo_archivo,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5, pady=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="💾 Guardar",
            bg="#17A2B8",
            fg="white",
            command=self.guardar_archivo,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5, pady=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="🔄 Actualizar Fecha",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_archivo,
            **btn_style
        )
        btn_actualizar.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Panel derecho - Lista de archivos
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            panel_der,
            text="Archivos Excel Registrados",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#17A2B8"
        ).pack(pady=15)

        # Buscador
        search_frame = tk.Frame(panel_der, bg="white")
        search_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            font=("Segoe UI", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=5)

        self.entry_buscar = tk.Entry(search_frame, font=("Segoe UI", 10))
        self.entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_buscar.bind('<KeyRelease>', self.buscar_archivo)

        btn_refresh = tk.Button(
            search_frame,
            text="↻",
            font=("Segoe UI", 12, "bold"),
            bg="#17A2B8",
            fg="white",
            command=self.refrescar_todo,
            cursor="hand2",
            width=3,
            bd=0
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de archivos
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Nombre", "Fecha Creación", "Fecha Modificación", "Días"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=20
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("Nombre", text="Nombre Archivo")
        self.tree.heading("Fecha Creación", text="Fecha Creación")
        self.tree.heading("Fecha Modificación", text="Última Modificación")
        self.tree.heading("Días", text="Días Antigüedad")

        self.tree.column("Nombre", width=250)
        self.tree.column("Fecha Creación", width=150, anchor="center")
        self.tree.column("Fecha Modificación", width=150, anchor="center")
        self.tree.column("Días", width=120, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Event: Seleccionar archivo
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_archivo)

    def crear_campo(self, parent, texto, fila):
        label = tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            anchor="e"
        )
        label.grid(row=fila, column=0, padx=10, pady=5, sticky="e")

    def validar_nombre_archivo(self, nombre):
        """Valida que el nombre tenga extensión .xlsx o .xls"""
        if not nombre:
            return False, "El nombre del archivo no puede estar vacío"
        
        if not nombre.strip():
            return False, "El nombre del archivo no puede estar vacío"
        
        # Verificar que termine en .xlsx o .xls
        if not (nombre.lower().endswith('.xlsx') or nombre.lower().endswith('.xls')):
            return False, "El archivo debe tener extensión .xlsx o .xls"
        
        # Verificar caracteres válidos
        if re.search(r'[<>:"/\\|?*]', nombre):
            return False, "El nombre contiene caracteres no permitidos"
        
        # Verificar longitud
        if len(nombre) > 100:
            return False, "El nombre es demasiado largo (máximo 100 caracteres)"
        
        if len(nombre) < 5:  # al menos "a.xls"
            return False, "El nombre es demasiado corto"
        
        return True, ""

    def cargar_archivos(self):
        """Carga todos los archivos desde la base de datos"""
        try:
            # Guardar selección actual
            seleccion_anterior = None
            if self.tree.selection():
                item = self.tree.item(self.tree.selection()[0])
                seleccion_anterior = item['values'][0] if item['values'] else None

            # Limpiar tabla
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    nombre,
                    fecha_creacion,
                    fecha_modificacion,
                    TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) AS dias_antiguedad
                FROM archivo_excel_gestion_clientes
                ORDER BY fecha_modificacion DESC
            """

            cursor.execute(query)
            self.archivos = cursor.fetchall()

            # Insertar archivos en la tabla
            item_a_seleccionar = None
            for archivo in self.archivos:
                dias = archivo[3] if archivo[3] is not None and archivo[3] >= 0 else 0

                # Aplicar color según antigüedad
                tags = self.obtener_tag_por_dias(dias)

                valores = (
                    archivo[0],
                    archivo[1],
                    archivo[2],
                    f"{dias} días" if dias >= 0 else "N/A"
                )
                item_id = self.tree.insert("", tk.END, values=valores, tags=tags)

                # Si este era el archivo seleccionado, guardamos su ID
                if seleccion_anterior and archivo[0] == seleccion_anterior:
                    item_a_seleccionar = item_id

            # Configurar colores
            self.tree.tag_configure('actual', foreground='#28A745')
            self.tree.tag_configure('reciente', foreground='#17A2B8')
            self.tree.tag_configure('antiguo', foreground='#FFC107')
            self.tree.tag_configure('muy_antiguo', foreground='#DC3545')

            cursor.close()

            # Restaurar selección si existía
            if item_a_seleccionar:
                self.tree.selection_set(item_a_seleccionar)
                self.tree.see(item_a_seleccionar)

            # Actualizar la interfaz
            self.tree.update_idletasks()

        except Exception as e:
            self.mostrar_error("Error al cargar archivos", str(e))

    def refrescar_todo(self):
        """Refresca la lista y limpia el formulario"""
        self.cargar_archivos()
        self.nuevo_archivo()

    def buscar_archivo(self, event=None):
        """Busca archivos por nombre en tiempo real"""
        busqueda = self.entry_buscar.get().strip().upper()

        self.tree.delete(*self.tree.get_children())

        if not busqueda:
            # Si no hay búsqueda, mostrar todos
            for archivo in self.archivos:
                dias = archivo[3] if archivo[3] is not None and archivo[3] >= 0 else 0
                tags = self.obtener_tag_por_dias(dias)
                valores = (archivo[0], archivo[1], archivo[2], f"{dias} días" if dias >= 0 else "N/A")
                self.tree.insert("", tk.END, values=valores, tags=tags)
        else:
            # Filtrar por búsqueda
            for archivo in self.archivos:
                if busqueda in str(archivo[0]).upper():
                    dias = archivo[3] if archivo[3] is not None and archivo[3] >= 0 else 0
                    tags = self.obtener_tag_por_dias(dias)
                    valores = (archivo[0], archivo[1], archivo[2], f"{dias} días" if dias >= 0 else "N/A")
                    self.tree.insert("", tk.END, values=valores, tags=tags)

    def obtener_tag_por_dias(self, dias):
        """Retorna el tag apropiado según los días"""
        if dias > 180:
            return ('muy_antiguo',)
        elif dias > 90:
            return ('antiguo',)
        elif dias > 30:
            return ('reciente',)
        else:
            return ('actual',)

    def seleccionar_archivo(self, event=None):
        """Carga los datos del archivo seleccionado en el formulario"""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # ✅ QUERY CORRECTA con WHERE:
            query = """
                SELECT nombre, fecha_creacion, fecha_modificacion
                FROM archivo_excel_gestion_clientes
                WHERE nombre = %s
            """
            cursor.execute(query, (valores[0],))

            archivo = cursor.fetchone()
            cursor.close()

            if archivo:
                self.nombre_seleccionado = archivo[0]

                # Habilitar campos temporalmente
                self.entry_nombre.config(state='normal')
                self.entry_fecha_creacion.config(state='normal')
                self.entry_fecha_modificacion.config(state='normal')

                # Limpiar campos
                self.entry_nombre.delete(0, tk.END)
                self.entry_fecha_creacion.delete(0, tk.END)
                self.entry_fecha_modificacion.delete(0, tk.END)

                # Cargar datos
                self.entry_nombre.insert(0, archivo[0])
                self.entry_fecha_creacion.insert(0, str(archivo[1]))
                self.entry_fecha_modificacion.insert(0, str(archivo[2]))

                # Deshabilitar campos (solo lectura para edición)
                self.entry_nombre.config(state='disabled')
                self.entry_fecha_creacion.config(state='readonly')
                self.entry_fecha_modificacion.config(state='readonly')

        except Exception as e:
            self.mostrar_error("Error al cargar archivo", str(e))

    def nuevo_archivo(self):
        """Limpia el formulario para un nuevo archivo"""
        self.nombre_seleccionado = None

        # Habilitar campos
        self.entry_nombre.config(state='normal')
        self.entry_fecha_creacion.config(state='normal')
        self.entry_fecha_modificacion.config(state='normal')

        # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_fecha_creacion.delete(0, tk.END)
        self.entry_fecha_modificacion.delete(0, tk.END)

        # Las fechas se asignan automáticamente en el servidor
        self.entry_fecha_creacion.insert(0, "Se asignará automáticamente")
        self.entry_fecha_modificacion.insert(0, "Se asignará automáticamente")

        # Deshabilitar fechas (automáticas)
        self.entry_fecha_creacion.config(state='readonly')
        self.entry_fecha_modificacion.config(state='readonly')

        # Limpiar búsqueda
        self.entry_buscar.delete(0, tk.END)

        # Limpiar selección del tree
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.entry_nombre.focus()

    def guardar_archivo(self):
        """Guarda un nuevo archivo con validaciones completas"""
        # Obtener y limpiar valores
        nombre = self.entry_nombre.get().strip()

        # Validar nombre
        valido, mensaje_error = self.validar_nombre_archivo(nombre)
        if not valido:
            self.mostrar_advertencia("Nombre Inválido", mensaje_error)
            self.entry_nombre.focus()
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Fechas automáticas en el servidor
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Llamar al procedimiento almacenado
            query = "CALL insertar_archivo_excel(%s, %s, %s)"
            valores = (nombre, ahora, ahora)

            cursor.execute(query, valores)
            conn.commit()

            # Consumir todos los resultados del stored procedure
            for result in cursor.stored_results():
                result.fetchall()

            cursor.close()

            self.mostrar_exito("Archivo Registrado", f"El archivo '{nombre}' se registró correctamente")
            
            # Recargar y seleccionar el nuevo archivo
            self.cargar_archivos()
            
            # Buscar y seleccionar el archivo recién insertado
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == nombre:
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    self.seleccionar_archivo()
                    break

        except Exception as e:
            error_msg = str(e)
            if "Duplicate entry" in error_msg or "duplicate key" in error_msg.lower():
                self.mostrar_error(
                    "Archivo Duplicado",
                    f"Ya existe un archivo registrado con el nombre:\n{nombre}"
                )
            else:
                self.mostrar_error("Error al Guardar", f"No se pudo guardar el archivo:\n{error_msg}")

    def actualizar_archivo(self):
        """Actualiza la fecha de modificación del archivo seleccionado"""
        if not self.nombre_seleccionado:
            self.mostrar_advertencia(
                "Sin Selección",
                "Por favor seleccione un archivo de la lista para actualizar su fecha de modificación"
            )
            return

        # Confirmar actualización
        respuesta = messagebox.askyesno(
            "Confirmar Actualización",
            f"¿Desea actualizar la fecha de modificación del archivo?\n\n" +
            f"Archivo: {self.nombre_seleccionado}\n" +
            f"Nueva fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            icon='question',
            parent=self.ventana
        )

        if not respuesta:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Fecha actual
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Llamar al procedimiento almacenado
            query = "CALL actualizar_archivo_excel(%s, %s)"
            valores = (self.nombre_seleccionado, ahora)

            cursor.execute(query, valores)
            conn.commit()

            # ✅ CONSUMIR todos los resultados del stored procedure
            for result in cursor.stored_results():
                result.fetchall()

            cursor.close()

            self.mostrar_exito(
                "Fecha Actualizada",
                f"La fecha de modificación del archivo '{self.nombre_seleccionado}' se actualizó correctamente"
            )
            
            # Recargar datos manteniendo la selección
            self.cargar_archivos()

        except Exception as e:
            self.mostrar_error("Error al Actualizar", f"No se pudo actualizar el archivo:\n{str(e)}")
    # Métodos para mostrar mensajes modales profesionales
    def mostrar_exito(self, titulo, mensaje):
        """Muestra un mensaje de éxito"""
        messagebox.showinfo(f"✓ {titulo}", mensaje, parent=self.ventana)

    def mostrar_error(self, titulo, mensaje):
        """Muestra un mensaje de error"""
        messagebox.showerror(f"✗ {titulo}", mensaje, parent=self.ventana)

    def mostrar_advertencia(self, titulo, mensaje):
        """Muestra un mensaje de advertencia"""
        messagebox.showwarning(f"⚠ {titulo}", mensaje, parent=self.ventana)
