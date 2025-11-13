"""
Módulo de Gestión de Clientes
Sistema JP Business Solutions
Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from models.config_db import Database
from datetime import datetime

class GestionClientes:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Clientes - JP Business Solutions")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#F5F5F5")

        # Variables
        self.clientes = []
        self.cliente_seleccionado = None

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#0047AB", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="GESTIÓN DE CLIENTES",
            font=("Arial", 16, "bold"),
            bg="#0047AB",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Formulario
        panel_izq = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Título del formulario
        tk.Label(
            panel_izq,
            text="Datos del Cliente",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=10)

        # Frame para campos
        form_frame = tk.Frame(panel_izq, bg="white")
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Campos del formulario
        self.crear_campo(form_frame, "RUC:", 0)
        self.entry_ruc = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_ruc.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Razón Social:", 1)
        self.entry_razon = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_razon.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Nombre Comercial:", 2)
        self.entry_comercial = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_comercial.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Dirección:", 3)
        self.entry_direccion = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_direccion.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Distrito:", 4)
        self.entry_distrito = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_distrito.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Provincia:", 5)
        self.entry_provincia = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_provincia.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Departamento:", 6)
        self.entry_departamento = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_departamento.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Teléfono:", 7)
        self.entry_telefono = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_telefono.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Email:", 8)
        self.entry_email = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_email.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Contacto:", 9)
        self.entry_contacto = tk.Entry(form_frame, font=("Arial", 10), width=30)
        self.entry_contacto.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        self.crear_campo(form_frame, "Estado:", 10)
        self.combo_estado = ttk.Combobox(
            form_frame,
            values=["ACTIVO", "INACTIVO", "SUSPENDIDO"],
            state="readonly",
            font=("Arial", 10),
            width=28
        )
        self.combo_estado.set("ACTIVO")
        self.combo_estado.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        # Botones de acción
        btn_frame = tk.Frame(panel_izq, bg="white")
        btn_frame.pack(pady=15)

        btn_style = {
            "font": ("Arial", 10, "bold"),
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
            command=self.nuevo_cliente,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar",
            bg="#0047AB",
            fg="white",
            command=self.guardar_cliente,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="Actualizar",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_cliente,
            **btn_style
        )
        btn_actualizar.grid(row=0, column=2, padx=5)

        btn_eliminar = tk.Button(
            btn_frame,
            text="Eliminar",
            bg="#DC3545",
            fg="white",
            command=self.eliminar_cliente,
            **btn_style
        )
        btn_eliminar.grid(row=0, column=3, padx=5)

        # Panel derecho - Lista de clientes
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Título lista
        tk.Label(
            panel_der,
            text="Lista de Clientes",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=10)

        # Buscador
        search_frame = tk.Frame(panel_der, bg="white")
        search_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(
            search_frame,
            text="Buscar:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=5)

        self.entry_buscar = tk.Entry(search_frame, font=("Arial", 10))
        self.entry_buscar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_buscar.bind('<KeyRelease>', self.buscar_cliente)

        btn_refresh = tk.Button(
            search_frame,
            text="↻",
            font=("Arial", 12, "bold"),
            bg="#0047AB",
            fg="white",
            command=self.cargar_clientes,
            cursor="hand2",
            width=3
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de clientes
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "RUC", "Razón Social", "Teléfono", "Estado"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("RUC", text="RUC")
        self.tree.heading("Razón Social", text="Razón Social")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("RUC", width=100, anchor="center")
        self.tree.column("Razón Social", width=250)
        self.tree.column("Teléfono", width=100, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        # Posicionar elementos
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Event: Seleccionar cliente
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_cliente)

    def crear_campo(self, parent, texto, fila):
        label = tk.Label(
            parent,
            text=texto,
            font=("Arial", 10, "bold"),
            bg="white",
            anchor="e"
        )
        label.grid(row=fila, column=0, padx=10, pady=5, sticky="e")

    def cargar_clientes(self):
        """Carga todos los clientes desde la base de datos"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT id_cliente, ruc, razon_social, telefono, estado
                FROM cliente
                ORDER BY id_cliente DESC
            """

            cursor.execute(query)
            self.clientes = cursor.fetchall()

            for cliente in self.clientes:
                self.tree.insert("", tk.END, values=cliente)

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {str(e)}")

    def buscar_cliente(self, event=None):
        """Busca clientes por RUC o Razón Social"""
        busqueda = self.entry_buscar.get().upper()

        self.tree.delete(*self.tree.get_children())

        for cliente in self.clientes:
            if busqueda in str(cliente[1]).upper() or busqueda in str(cliente[2]).upper():
                self.tree.insert("", tk.END, values=cliente)

    def seleccionar_cliente(self, event=None):
        """Carga los datos del cliente seleccionado en el formulario"""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "SELECT * FROM cliente WHERE id_cliente = %s"
            cursor.execute(query, (valores[0],))

            cliente = cursor.fetchone()
            cursor.close()

            if cliente:
                self.cliente_seleccionado = cliente[0]
                self.entry_ruc.delete(0, tk.END)
                self.entry_ruc.insert(0, cliente[1])
                self.entry_razon.delete(0, tk.END)
                self.entry_razon.insert(0, cliente[2])
                self.entry_comercial.delete(0, tk.END)
                self.entry_comercial.insert(0, cliente[3] or "")
                self.entry_direccion.delete(0, tk.END)
                self.entry_direccion.insert(0, cliente[4] or "")
                self.entry_distrito.delete(0, tk.END)
                self.entry_distrito.insert(0, cliente[5] or "")
                self.entry_provincia.delete(0, tk.END)
                self.entry_provincia.insert(0, cliente[6] or "")
                self.entry_departamento.delete(0, tk.END)
                self.entry_departamento.insert(0, cliente[7] or "")
                self.entry_telefono.delete(0, tk.END)
                self.entry_telefono.insert(0, cliente[8] or "")
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, cliente[9] or "")
                self.entry_contacto.delete(0, tk.END)
                self.entry_contacto.insert(0, cliente[10] or "")
                self.combo_estado.set(cliente[14])

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cliente: {str(e)}")

    def nuevo_cliente(self):
        """Limpia el formulario para un nuevo cliente"""
        self.cliente_seleccionado = None
        self.entry_ruc.delete(0, tk.END)
        self.entry_razon.delete(0, tk.END)
        self.entry_comercial.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_distrito.delete(0, tk.END)
        self.entry_provincia.delete(0, tk.END)
        self.entry_departamento.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_contacto.delete(0, tk.END)
        self.combo_estado.set("ACTIVO")
        self.entry_ruc.focus()

    def guardar_cliente(self):
        """Guarda un nuevo cliente"""
        # Validaciones
        if not self.entry_ruc.get() or not self.entry_razon.get():
            messagebox.showwarning("Advertencia", "RUC y Razón Social son obligatorios")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                CALL sp_insertar_cliente(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                self.entry_ruc.get(),
                self.entry_razon.get(),
                self.entry_comercial.get(),
                self.entry_direccion.get(),
                self.entry_distrito.get(),
                self.entry_provincia.get(),
                self.entry_departamento.get(),
                self.entry_telefono.get(),
                self.entry_email.get(),
                self.entry_contacto.get(),
                "",  # contacto_cargo
                "",  # contacto_telefono
                "",  # contacto_email
                ""   # observaciones
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            self.cargar_clientes()
            self.nuevo_cliente()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cliente: {str(e)}")

    def actualizar_cliente(self):
        """Actualiza un cliente existente"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                CALL sp_actualizar_cliente(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                self.cliente_seleccionado,
                self.entry_ruc.get(),
                self.entry_razon.get(),
                self.entry_comercial.get(),
                self.entry_direccion.get(),
                self.entry_distrito.get(),
                self.entry_provincia.get(),
                self.entry_departamento.get(),
                self.entry_telefono.get(),
                self.entry_email.get(),
                self.entry_contacto.get(),
                "",  # contacto_cargo
                "",  # contacto_telefono
                "",  # contacto_email
                self.combo_estado.get(),
                ""   # observaciones
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            self.cargar_clientes()

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente: {str(e)}")

    def eliminar_cliente(self):
        """Elimina (desactiva) un cliente"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de desactivar este cliente?"
        )

        if not confirmacion:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL sp_eliminar_cliente(%s)"
            cursor.execute(query, (self.cliente_seleccionado,))
            conn.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Cliente desactivado correctamente")
            self.cargar_clientes()
            self.nuevo_cliente()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
