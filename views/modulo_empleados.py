"""
Módulo de Gestión de Empleados - CRUD Completo
Sistema JP Business Solutions
Versión: 3.0 - Adaptado a estructura real de BD
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime
import re

class GestionEmpleados:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Empleados - JP Business Solutions")
        self.ventana.geometry("1300x750")
        self.ventana.configure(bg="#F5F5F5")

        self.empleados = []
        self.codigo_seleccionado = None
        self.clientes_list = []
        self.archivos_list = []

        self.cargar_listas_fk()
        self.crear_interfaz()
        self.cargar_empleados()

    def cargar_listas_fk(self):
        """Carga listas de clientes y archivos para FKs"""
        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Cargar clientes
            cursor.execute("SELECT ruc, CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) FROM cliente ORDER BY apellido_paterno")
            self.clientes_list = cursor.fetchall()

            # Cargar archivos Excel
            cursor.execute("SELECT nombre FROM archivo_excel_gestion_clientes ORDER BY nombre")
            self.archivos_list = [row[0] for row in cursor.fetchall()]

            cursor.close()
        except Exception as e:
            print(f"Error al cargar listas FK: {e}")
            self.clientes_list = []
            self.archivos_list = []

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#007BFF", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="👔 GESTIÓN DE EMPLEADOS",
            font=("Segoe UI", 16, "bold"),
            bg="#007BFF",
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
            text="Datos del Empleado",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#007BFF"
        ).pack(pady=15)

        # Frame para campos con scroll
        canvas = tk.Canvas(panel_izq, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel_izq, orient="vertical", command=canvas.yview)
        form_frame = tk.Frame(canvas, bg="white")

        form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Código (PK)
        self.crear_campo(form_frame, "Código: *", 0)
        self.entry_codigo = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(Número entero único)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=0, column=2, padx=5, sticky="w")

        # Sexo
        self.crear_campo(form_frame, "Sexo: *", 1)
        self.combo_sexo = ttk.Combobox(
            form_frame,
            values=["Masculino", "Femenino"],
            state="readonly",
            font=("Segoe UI", 10),
            width=28
        )
        self.combo_sexo.set("Masculino")
        self.combo_sexo.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        # Cargo
        self.crear_campo(form_frame, "Cargo: *", 2)
        self.entry_cargo = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_cargo.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        # Fecha Nacimiento
        self.crear_campo(form_frame, "Fecha Nacimiento: *", 3)
        fecha_frame = tk.Frame(form_frame, bg="white")
        fecha_frame.grid(row=3, column=1, padx=10, pady=8, sticky="ew")

        self.entry_fecha_nac = tk.Entry(fecha_frame, font=("Segoe UI", 10), width=24)
        self.entry_fecha_nac.pack(side=tk.LEFT)
        self.entry_fecha_nac.insert(0, "YYYY-MM-DD")

        tk.Label(
            form_frame,
            text="(Debe ser mayor de 18 años)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=3, column=2, padx=5, sticky="w")

        # Nombres
        self.crear_campo(form_frame, "Nombres: *", 4)
        self.entry_nombres = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_nombres.grid(row=4, column=1, padx=10, pady=8, sticky="ew")

        # Apellido Paterno
        self.crear_campo(form_frame, "Apellido Paterno: *", 5)
        self.entry_ap_paterno = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_ap_paterno.grid(row=5, column=1, padx=10, pady=8, sticky="ew")

        # Apellido Materno
        self.crear_campo(form_frame, "Apellido Materno: *", 6)
        self.entry_ap_materno = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_ap_materno.grid(row=6, column=1, padx=10, pady=8, sticky="ew")

        # RUC Cliente (FK)
        self.crear_campo(form_frame, "Cliente Asignado:", 7)
        cliente_frame = tk.Frame(form_frame, bg="white")
        cliente_frame.grid(row=7, column=1, padx=10, pady=8, sticky="ew")

        self.combo_ruc_cliente = ttk.Combobox(
            cliente_frame,
            values=[""] + [f"{ruc} - {nombre}" for ruc, nombre in self.clientes_list],
            font=("Segoe UI", 9),
            width=27
        )
        self.combo_ruc_cliente.pack(fill=tk.X)

        tk.Label(
            form_frame,
            text="(Opcional)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=7, column=2, padx=5, sticky="w")

        # Nombre Archivo (FK)
        self.crear_campo(form_frame, "Archivo Excel:", 8)
        archivo_frame = tk.Frame(form_frame, bg="white")
        archivo_frame.grid(row=8, column=1, padx=10, pady=8, sticky="ew")

        self.combo_archivo = ttk.Combobox(
            archivo_frame,
            values=[""] + self.archivos_list,
            font=("Segoe UI", 9),
            width=27
        )
        self.combo_archivo.pack(fill=tk.X)

        tk.Label(
            form_frame,
            text="(Opcional)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=8, column=2, padx=5, sticky="w")

        # Nota de campos obligatorios
        tk.Label(
            form_frame,
            text="* Campos obligatorios",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#DC3545"
        ).grid(row=9, column=0, columnspan=3, pady=15)

        # Botones de acción
        btn_frame = tk.Frame(panel_izq, bg="white")
        btn_frame.pack(pady=20)

        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "width": 12,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat"
        }

        btn_nuevo = tk.Button(
            btn_frame,
            text="Nuevo",
            bg="#28A745",
            fg="white",
            command=self.nuevo_empleado,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5, pady=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar",
            bg="#007BFF",
            fg="white",
            command=self.guardar_empleado,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5, pady=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="Actualizar",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_empleado,
            **btn_style
        )
        btn_actualizar.grid(row=1, column=0, padx=5, pady=5)

        btn_eliminar = tk.Button(
            btn_frame,
            text="Eliminar",
            bg="#DC3545",
            fg="white",
            command=self.eliminar_empleado,
            **btn_style
        )
        btn_eliminar.grid(row=1, column=1, padx=5, pady=5)

        # Panel derecho - Lista de empleados
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            panel_der,
            text="Lista de Empleados",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#007BFF"
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
        self.entry_buscar.bind('<KeyRelease>', self.buscar_empleado)

        btn_refresh = tk.Button(
            search_frame,
            text="↻",
            font=("Segoe UI", 12, "bold"),
            bg="#007BFF",
            fg="white",
            command=self.cargar_empleados,
            cursor="hand2",
            width=3,
            bd=0
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de empleados
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Código", "Nombre Completo", "Sexo", "Cargo", "Edad", "Cliente"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=22
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre Completo", text="Nombre Completo")
        self.tree.heading("Sexo", text="Sexo")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Cliente", text="Cliente Asignado")

        self.tree.column("Código", width=70, anchor="center")
        self.tree.column("Nombre Completo", width=200)
        self.tree.column("Sexo", width=80, anchor="center")
        self.tree.column("Cargo", width=150)
        self.tree.column("Edad", width=60, anchor="center")
        self.tree.column("Cliente", width=200)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Event: Seleccionar empleado
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_empleado)

    def crear_campo(self, parent, texto, fila):
        label = tk.Label(
            parent,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            anchor="e"
        )
        label.grid(row=fila, column=0, padx=10, pady=5, sticky="e")

    def validar_edad(self, fecha_nac):
        """Valida que el empleado sea mayor de 18 años"""
        try:
            if fecha_nac == "YYYY-MM-DD" or not fecha_nac:
                return False
            fecha = datetime.strptime(fecha_nac, "%Y-%m-%d")
            edad = (datetime.now() - fecha).days / 365.25
            return edad >= 18
        except:
            return False

    def calcular_edad(self, fecha_nac):
        """Calcula la edad en años"""
        try:
            if not fecha_nac:
                return None
            fecha = datetime.strptime(str(fecha_nac), "%Y-%m-%d")
            edad = int((datetime.now() - fecha).days / 365.25)
            return edad
        except:
            return None

    def cargar_empleados(self):
        """Carga todos los empleados desde la base de datos"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    e.codigo,
                    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS nombre_completo,
                    e.sexo,
                    e.cargo,
                    TIMESTAMPDIFF(YEAR, e.fecha_nacimiento, CURDATE()) AS edad,
                    CONCAT(c.nombres, ' ', c.apellido_paterno) AS cliente_nombre
                FROM empleado e
                LEFT JOIN cliente c ON e.ruc_cliente = c.ruc
                ORDER BY e.codigo
            """

            cursor.execute(query)
            self.empleados = cursor.fetchall()

            for empleado in self.empleados:
                # Formatear valores
                edad = empleado[4] if empleado[4] else ""
                cliente = empleado[5] if empleado[5] else "Sin asignar"

                valores = (
                    empleado[0],  # codigo
                    empleado[1],  # nombre_completo
                    empleado[2],  # sexo
                    empleado[3],  # cargo
                    f"{edad} años" if edad else "",
                    cliente
                )
                self.tree.insert("", tk.END, values=valores)

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados:\n{str(e)}")

    def buscar_empleado(self, event=None):
        """Busca empleados por código o nombre"""
        busqueda = self.entry_buscar.get().upper()

        self.tree.delete(*self.tree.get_children())

        for empleado in self.empleados:
            if busqueda in str(empleado[0]).upper() or busqueda in str(empleado[1]).upper():
                edad = empleado[4] if empleado[4] else ""
                cliente = empleado[5] if empleado[5] else "Sin asignar"

                valores = (
                    empleado[0],
                    empleado[1],
                    empleado[2],
                    empleado[3],
                    f"{edad} años" if edad else "",
                    cliente
                )
                self.tree.insert("", tk.END, values=valores)

    def seleccionar_empleado(self, event=None):
        """Carga los datos del empleado seleccionado en el formulario"""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT codigo, sexo, cargo, fecha_nacimiento, nombres,
                       apellido_paterno, apellido_materno, ruc_cliente, nombre_archivo
                FROM empleado
                WHERE codigo = %s
            """
            cursor.execute(query, (valores[0],))

            empleado = cursor.fetchone()
            cursor.close()

            if empleado:
                self.codigo_seleccionado = empleado[0]

                # Limpiar campos
                self.entry_codigo.delete(0, tk.END)
                self.entry_nombres.delete(0, tk.END)
                self.entry_ap_paterno.delete(0, tk.END)
                self.entry_ap_materno.delete(0, tk.END)
                self.entry_fecha_nac.delete(0, tk.END)
                self.entry_cargo.delete(0, tk.END)

                # Cargar datos
                self.entry_codigo.insert(0, empleado[0])
                self.combo_sexo.set(empleado[1])
                self.entry_cargo.insert(0, empleado[2])
                self.entry_fecha_nac.insert(0, str(empleado[3]) if empleado[3] else "YYYY-MM-DD")
                self.entry_nombres.insert(0, empleado[4])
                self.entry_ap_paterno.insert(0, empleado[5])
                self.entry_ap_materno.insert(0, empleado[6])

                # RUC Cliente
                ruc_cliente = empleado[7]
                if ruc_cliente:
                    # Buscar en la lista de clientes
                    for i, (ruc, nombre) in enumerate(self.clientes_list):
                        if ruc == ruc_cliente:
                            self.combo_ruc_cliente.current(i + 1)  # +1 porque el primer item es ""
                            break
                else:
                    self.combo_ruc_cliente.set("")

                # Nombre Archivo
                nombre_archivo = empleado[8]
                if nombre_archivo and nombre_archivo in self.archivos_list:
                    self.combo_archivo.set(nombre_archivo)
                else:
                    self.combo_archivo.set("")

                # Deshabilitar código (es PK, no se puede cambiar)
                self.entry_codigo.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleado:\n{str(e)}")

    def nuevo_empleado(self):
        """Limpia el formulario para un nuevo empleado"""
        self.codigo_seleccionado = None

        # Habilitar código
        self.entry_codigo.config(state='normal')

        # Limpiar campos
        self.entry_codigo.delete(0, tk.END)
        self.combo_sexo.set("Masculino")
        self.entry_cargo.delete(0, tk.END)
        self.entry_fecha_nac.delete(0, tk.END)
        self.entry_fecha_nac.insert(0, "YYYY-MM-DD")
        self.entry_nombres.delete(0, tk.END)
        self.entry_ap_paterno.delete(0, tk.END)
        self.entry_ap_materno.delete(0, tk.END)
        self.combo_ruc_cliente.set("")
        self.combo_archivo.set("")

        self.entry_codigo.focus()

    def guardar_empleado(self):
        """Guarda un nuevo empleado"""
        # Obtener valores
        codigo = self.entry_codigo.get().strip()
        sexo = self.combo_sexo.get()
        cargo = self.entry_cargo.get().strip()
        fecha_nac = self.entry_fecha_nac.get().strip()
        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()

        # Validaciones
        if not codigo or not sexo or not cargo or not nombres or not ap_paterno or not ap_materno:
            messagebox.showwarning(
                "Advertencia",
                "Código, Sexo, Cargo, Nombres, Apellido Paterno y Apellido Materno son obligatorios"
            )
            return

        if not codigo.isdigit():
            messagebox.showerror("Error", "El código debe ser un número entero")
            return

        if not self.validar_edad(fecha_nac):
            messagebox.showerror("Error", "Debe ingresar una fecha de nacimiento válida y el empleado debe ser mayor de 18 años")
            return

        # Obtener RUC cliente (FK)
        ruc_cliente_text = self.combo_ruc_cliente.get().strip()
        ruc_cliente = None
        if ruc_cliente_text and ruc_cliente_text != "":
            # Extraer el RUC (formato: "12345678901 - Nombre Cliente")
            ruc_cliente = ruc_cliente_text.split(" - ")[0] if " - " in ruc_cliente_text else None

        # Obtener nombre archivo (FK)
        nombre_archivo = self.combo_archivo.get().strip()
        nombre_archivo = nombre_archivo if nombre_archivo else None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Llamar al procedimiento almacenado
            query = "CALL sp_insertar_empleado(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            valores = (
                int(codigo),
                sexo,
                cargo,
                fecha_nac,
                nombres,
                ap_paterno,
                ap_materno,
                ruc_cliente,
                nombre_archivo
            )

            cursor.execute(query, valores)
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Empleado guardado correctamente")
            self.cargar_empleados()
            self.nuevo_empleado()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar empleado:\n{str(e)}")

    def actualizar_empleado(self):
        """Actualiza un empleado existente"""
        if not self.codigo_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para actualizar")
            return

        # Obtener valores
        sexo = self.combo_sexo.get()
        cargo = self.entry_cargo.get().strip()
        fecha_nac = self.entry_fecha_nac.get().strip()
        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()

        # Validaciones
        if not sexo or not cargo or not nombres or not ap_paterno or not ap_materno:
            messagebox.showwarning(
                "Advertencia",
                "Sexo, Cargo, Nombres, Apellido Paterno y Apellido Materno son obligatorios"
            )
            return

        if not self.validar_edad(fecha_nac):
            messagebox.showerror("Error", "Debe ingresar una fecha de nacimiento válida y el empleado debe ser mayor de 18 años")
            return

        # Obtener RUC cliente (FK)
        ruc_cliente_text = self.combo_ruc_cliente.get().strip()
        ruc_cliente = None
        if ruc_cliente_text and ruc_cliente_text != "":
            ruc_cliente = ruc_cliente_text.split(" - ")[0] if " - " in ruc_cliente_text else None

        # Obtener nombre archivo (FK)
        nombre_archivo = self.combo_archivo.get().strip()
        nombre_archivo = nombre_archivo if nombre_archivo else None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Llamar al procedimiento almacenado
            query = "CALL sp_actualizar_empleado(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            valores = (
                self.codigo_seleccionado,
                sexo,
                cargo,
                fecha_nac,
                nombres,
                ap_paterno,
                ap_materno,
                ruc_cliente,
                nombre_archivo
            )

            cursor.execute(query, valores)
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
            self.cargar_empleados()
            self.nuevo_empleado()

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar empleado:\n{str(e)}")

    def eliminar_empleado(self):
        """Elimina un empleado"""
        if not self.codigo_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el empleado con código {self.codigo_seleccionado}?\n\n" +
            "Esta acción no se puede deshacer."
        )

        if not confirmacion:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL sp_eliminar_empleado(%s)"
            cursor.execute(query, (self.codigo_seleccionado,))
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
            self.cargar_empleados()
            self.nuevo_empleado()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar empleado:\n{str(e)}")
