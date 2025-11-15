"""
Módulo de Gestión de Archivos Excel
Sistema JP Business Solutions
Versión: 2.0 - Adaptado a estructura real de BD
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime

class GestionArchivosExcel:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Archivos Excel - JP Business Solutions")
        self.ventana.geometry("1100x650")
        self.ventana.configure(bg="#F5F5F5")

        self.archivos = []
        self.nombre_seleccionado = None

        self.crear_interfaz()
        self.cargar_archivos()

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
        self.entry_nombre = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(ej: clientes_2025.xlsx)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=0, column=2, padx=5, sticky="w")

        # Fecha Creación
        self.crear_campo(form_frame, "Fecha Creación: *", 1)
        fecha_creacion_frame = tk.Frame(form_frame, bg="white")
        fecha_creacion_frame.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        self.entry_fecha_creacion = tk.Entry(fecha_creacion_frame, font=("Segoe UI", 10), width=24)
        self.entry_fecha_creacion.pack(side=tk.LEFT)
        self.entry_fecha_creacion.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        tk.Label(
            form_frame,
            text="(YYYY-MM-DD HH:MM:SS)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=1, column=2, padx=5, sticky="w")

        # Fecha Modificación
        self.crear_campo(form_frame, "Fecha Modificación: *", 2)
        fecha_mod_frame = tk.Frame(form_frame, bg="white")
        fecha_mod_frame.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        self.entry_fecha_modificacion = tk.Entry(fecha_mod_frame, font=("Segoe UI", 10), width=24)
        self.entry_fecha_modificacion.pack(side=tk.LEFT)
        self.entry_fecha_modificacion.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        tk.Label(
            form_frame,
            text="(YYYY-MM-DD HH:MM:SS)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=2, column=2, padx=5, sticky="w")

        # Nota informativa
        info_label = tk.Label(
            form_frame,
            text="ℹ Este módulo registra metadatos de archivos Excel utilizados\nen el sistema de gestión de clientes.",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#666666",
            justify="left"
        )
        info_label.grid(row=3, column=0, columnspan=3, pady=15, padx=10, sticky="w")

        # Nota de campos obligatorios
        tk.Label(
            form_frame,
            text="* Campos obligatorios",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#DC3545"
        ).grid(row=4, column=0, columnspan=3, pady=10)

        # Botones de acción
        btn_frame = tk.Frame(panel_izq, bg="white")
        btn_frame.pack(pady=20)

        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "width": 15,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat"
        }

        btn_nuevo = tk.Button(
            btn_frame,
            text="Nuevo",
            bg="#28A745",
            fg="white",
            command=self.nuevo_archivo,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5, pady=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar",
            bg="#17A2B8",
            fg="white",
            command=self.guardar_archivo,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5, pady=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="Actualizar",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_archivo,
            **btn_style
        )
        btn_actualizar.grid(row=1, column=0, padx=5, pady=5)

        btn_actualizar_fecha = tk.Button(
            btn_frame,
            text="Actualizar Fecha",
            bg="#6F42C1",
            fg="white",
            command=self.actualizar_fecha_modificacion,
            **btn_style
        )
        btn_actualizar_fecha.grid(row=1, column=1, padx=5, pady=5)

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
            text="Buscar:",
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
            command=self.cargar_archivos,
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
            columns=("Nombre", "Fecha Creación", "Fecha Modificación", "Días Antigüedad"),
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
        self.tree.heading("Días Antigüedad", text="Días desde Modificación")

        self.tree.column("Nombre", width=250)
        self.tree.column("Fecha Creación", width=150, anchor="center")
        self.tree.column("Fecha Modificación", width=150, anchor="center")
        self.tree.column("Días Antigüedad", width=150, anchor="center")

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

    def validar_fecha(self, fecha_str):
        """Valida formato de fecha"""
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
            return True
        except:
            return False

    def calcular_dias(self, fecha_modificacion):
        """Calcula días desde la fecha de modificación"""
        try:
            if isinstance(fecha_modificacion, str):
                fecha = datetime.strptime(fecha_modificacion, "%Y-%m-%d %H:%M:%S")
            else:
                fecha = fecha_modificacion
            dias = (datetime.now() - fecha).days
            return dias
        except:
            return None

    def cargar_archivos(self):
        """Carga todos los archivos desde la base de datos"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    nombre,
                    DATE_FORMAT(fecha_creacion, '%Y-%m-%d %H:%i:%s') AS fecha_creacion,
                    DATE_FORMAT(fecha_modificacion, '%Y-%m-%d %H:%i:%s') AS fecha_modificacion,
                    TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) AS dias_antiguedad
                FROM archivo_excel_gestion_clientes
                ORDER BY fecha_modificacion DESC
            """

            cursor.execute(query)
            self.archivos = cursor.fetchall()

            for archivo in self.archivos:
                dias = archivo[3] if archivo[3] is not None else 0

                # Aplicar color según antigüedad
                tags = ()
                if dias > 180:
                    tags = ('muy_antiguo',)
                elif dias > 90:
                    tags = ('antiguo',)
                elif dias > 30:
                    tags = ('reciente',)
                else:
                    tags = ('actual',)

                valores = (
                    archivo[0],
                    archivo[1],
                    archivo[2],
                    f"{dias} días" if dias is not None else "N/A"
                )
                self.tree.insert("", tk.END, values=valores, tags=tags)

            # Configurar colores
            self.tree.tag_configure('actual', foreground='green')
            self.tree.tag_configure('reciente', foreground='blue')
            self.tree.tag_configure('antiguo', foreground='orange')
            self.tree.tag_configure('muy_antiguo', foreground='red')

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivos:\n{str(e)}")

    def buscar_archivo(self, event=None):
        """Busca archivos por nombre"""
        busqueda = self.entry_buscar.get().upper()

        self.tree.delete(*self.tree.get_children())

        for archivo in self.archivos:
            if busqueda in str(archivo[0]).upper():
                dias = archivo[3] if archivo[3] is not None else 0

                tags = ()
                if dias > 180:
                    tags = ('muy_antiguo',)
                elif dias > 90:
                    tags = ('antiguo',)
                elif dias > 30:
                    tags = ('reciente',)
                else:
                    tags = ('actual',)

                valores = (
                    archivo[0],
                    archivo[1],
                    archivo[2],
                    f"{dias} días" if dias is not None else "N/A"
                )
                self.tree.insert("", tk.END, values=valores, tags=tags)

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

                # Limpiar campos
                self.entry_nombre.delete(0, tk.END)
                self.entry_fecha_creacion.delete(0, tk.END)
                self.entry_fecha_modificacion.delete(0, tk.END)

                # Cargar datos
                self.entry_nombre.insert(0, archivo[0])
                self.entry_fecha_creacion.insert(0, str(archivo[1]))
                self.entry_fecha_modificacion.insert(0, str(archivo[2]))

                # Deshabilitar nombre (es PK, no se puede cambiar)
                self.entry_nombre.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivo:\n{str(e)}")

    def nuevo_archivo(self):
        """Limpia el formulario para un nuevo archivo"""
        self.nombre_seleccionado = None

        # Habilitar nombre
        self.entry_nombre.config(state='normal')

        # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_fecha_creacion.delete(0, tk.END)
        self.entry_fecha_modificacion.delete(0, tk.END)

        # Poner fechas actuales
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entry_fecha_creacion.insert(0, ahora)
        self.entry_fecha_modificacion.insert(0, ahora)

        self.entry_nombre.focus()

    def guardar_archivo(self):
        """Guarda un nuevo archivo"""
        # Obtener valores
        nombre = self.entry_nombre.get().strip()
        fecha_creacion = self.entry_fecha_creacion.get().strip()
        fecha_modificacion = self.entry_fecha_modificacion.get().strip()

        # Validaciones
        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre del archivo es obligatorio")
            return

        if not self.validar_fecha(fecha_creacion):
            messagebox.showerror("Error", "Formato de fecha de creación inválido (YYYY-MM-DD HH:MM:SS)")
            return

        if not self.validar_fecha(fecha_modificacion):
            messagebox.showerror("Error", "Formato de fecha de modificación inválido (YYYY-MM-DD HH:MM:SS)")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Llamar al procedimiento almacenado
            query = "CALL sp_insertar_archivo_excel(%s, %s, %s)"

            valores = (nombre, fecha_creacion, fecha_modificacion)

            cursor.execute(query, valores)
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Archivo registrado correctamente")
            self.cargar_archivos()
            self.nuevo_archivo()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar archivo:\n{str(e)}")

    def actualizar_archivo(self):
        """Actualiza los datos de un archivo (solo permite cambiar fechas)"""
        if not self.nombre_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un archivo para actualizar")
            return

        # Obtener valores
        fecha_modificacion = self.entry_fecha_modificacion.get().strip()

        # Validaciones
        if not self.validar_fecha(fecha_modificacion):
            messagebox.showerror("Error", "Formato de fecha de modificación inválido (YYYY-MM-DD HH:MM:SS)")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Llamar al procedimiento almacenado
            query = "CALL sp_actualizar_archivo_excel(%s, %s)"

            valores = (self.nombre_seleccionado, fecha_modificacion)

            cursor.execute(query, valores)
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Archivo actualizado correctamente")
            self.cargar_archivos()
            self.nuevo_archivo()

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar archivo:\n{str(e)}")

    def actualizar_fecha_modificacion(self):
        """Actualiza la fecha de modificación al momento actual"""
        if not self.nombre_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un archivo primero")
            return

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entry_fecha_modificacion.delete(0, tk.END)
        self.entry_fecha_modificacion.insert(0, ahora)

        messagebox.showinfo("Actualización", "Fecha de modificación actualizada al momento actual.\nPresione 'Actualizar' para guardar.")
