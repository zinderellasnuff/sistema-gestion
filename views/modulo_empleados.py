"""
Módulo de Gestión de Empleados
Sistema JP Business Solutions
Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database

class GestionEmpleados:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Empleados - JP Business Solutions")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#F5F5F5")

        self.empleado_seleccionado = None
        self.crear_interfaz()
        self.cargar_empleados()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#0047AB", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="GESTIÓN DE EMPLEADOS",
            font=("Arial", 16, "bold"),
            bg="#0047AB",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="white", relief=tk.RAISED, bd=2)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        tk.Label(
            main_container,
            text="Lista de Empleados",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=10)

        # Buscador
        search_frame = tk.Frame(main_container, bg="white")
        search_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(search_frame, text="Buscar:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)

        self.entry_buscar = tk.Entry(search_frame, font=("Arial", 10))
        self.entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn_refresh = tk.Button(
            search_frame,
            text="↻ Actualizar",
            font=("Arial", 10, "bold"),
            bg="#0047AB",
            fg="white",
            command=self.cargar_empleados,
            cursor="hand2"
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de empleados
        tree_frame = tk.Frame(main_container, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "DNI", "Nombres", "Cargo", "Área", "Salario", "Estado"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=20
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombres", text="Nombres Completos")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Área", text="Área")
        self.tree.heading("Salario", text="Salario")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("DNI", width=100, anchor="center")
        self.tree.column("Nombres", width=250)
        self.tree.column("Cargo", width=150)
        self.tree.column("Área", width=120)
        self.tree.column("Salario", width=100, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Botones de acción
        btn_frame = tk.Frame(main_container, bg="white")
        btn_frame.pack(pady=15)

        btn_style = {
            "font": ("Arial", 10, "bold"),
            "width": 15,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat"
        }

        btn_ver = tk.Button(
            btn_frame,
            text="Ver Detalles",
            bg="#17A2B8",
            fg="white",
            command=self.ver_detalles,
            **btn_style
        )
        btn_ver.pack(side=tk.LEFT, padx=5)

        btn_nuevo = tk.Button(
            btn_frame,
            text="Nuevo Empleado",
            bg="#28A745",
            fg="white",
            command=lambda: messagebox.showinfo("Info", "Funcionalidad en desarrollo"),
            **btn_style
        )
        btn_nuevo.pack(side=tk.LEFT, padx=5)

    def cargar_empleados(self):
        """Carga todos los empleados desde la base de datos"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    id_empleado,
                    dni,
                    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
                    cargo,
                    area,
                    CONCAT('S/ ', FORMAT(salario, 2)) AS salario,
                    estado
                FROM empleado
                ORDER BY id_empleado DESC
            """

            cursor.execute(query)
            empleados = cursor.fetchall()

            for empleado in empleados:
                # Cambiar color según estado
                tags = ('activo',) if empleado[6] == 'ACTIVO' else ('inactivo',)
                self.tree.insert("", tk.END, values=empleado, tags=tags)

            # Configurar tags de colores
            self.tree.tag_configure('activo', foreground='green')
            self.tree.tag_configure('inactivo', foreground='red')

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {str(e)}")

    def ver_detalles(self):
        """Muestra los detalles del empleado seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado")
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "SELECT * FROM empleado WHERE id_empleado = %s"
            cursor.execute(query, (valores[0],))

            empleado = cursor.fetchone()
            cursor.close()

            if empleado:
                detalles = f"""
ID: {empleado[0]}
DNI: {empleado[1]}
Nombres: {empleado[2]} {empleado[3]} {empleado[4]}
Fecha Nacimiento: {empleado[5] or 'N/A'}
Dirección: {empleado[6] or 'N/A'}
Distrito: {empleado[7] or 'N/A'}
Teléfono: {empleado[11] or 'N/A'}
Email: {empleado[12] or 'N/A'}
Cargo: {empleado[13] or 'N/A'}
Área: {empleado[14] or 'N/A'}
Fecha Ingreso: {empleado[15] or 'N/A'}
Salario: S/ {empleado[16] or 0}
Estado: {empleado[17]}
                """
                messagebox.showinfo("Detalles del Empleado", detalles)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar detalles: {str(e)}")
