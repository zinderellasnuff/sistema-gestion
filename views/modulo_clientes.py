"""
Módulo de Gestión de Clientes
Sistema JP Business Solutions
Versión: 2.0 - Adaptado a estructura real de BD
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
import re

class GestionClientes:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Clientes - JP Business Solutions")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#F5F5F5")

        # Variables
        self.clientes = []
        self.ruc_seleccionado = None

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#0047AB", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="👥 GESTIÓN DE CLIENTES",
            font=("Segoe UI", 16, "bold"),
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
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=15)

        # Frame para campos
        form_frame = tk.Frame(panel_izq, bg="white")
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # RUC (PK)
        self.crear_campo(form_frame, "RUC: *", 0)
        self.entry_ruc = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_ruc.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(11 dígitos)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=0, column=2, padx=5, sticky="w")

        # Nombres
        self.crear_campo(form_frame, "Nombres: *", 1)
        self.entry_nombres = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_nombres.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        # Apellido Paterno
        self.crear_campo(form_frame, "Apellido Paterno: *", 2)
        self.entry_ap_paterno = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_ap_paterno.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        # Apellido Materno
        self.crear_campo(form_frame, "Apellido Materno: *", 3)
        self.entry_ap_materno = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_ap_materno.grid(row=3, column=1, padx=10, pady=8, sticky="ew")

        # Correo Electrónico
        self.crear_campo(form_frame, "Correo Electrónico:", 4)
        self.entry_correo = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_correo.grid(row=4, column=1, padx=10, pady=8, sticky="ew")

        # Página Web
        self.crear_campo(form_frame, "Página Web:", 5)
        self.entry_pagina_web = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_pagina_web.grid(row=5, column=1, padx=10, pady=8, sticky="ew")

        # Teléfono
        self.crear_campo(form_frame, "Teléfono:", 6)
        self.entry_telefono = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_telefono.grid(row=6, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(9 dígitos)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=6, column=2, padx=5, sticky="w")

        # Nota de campos obligatorios
        tk.Label(
            form_frame,
            text="* Campos obligatorios",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#DC3545"
        ).grid(row=7, column=0, columnspan=3, pady=10)

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
            command=self.nuevo_cliente,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5, pady=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="Guardar",
            bg="#0047AB",
            fg="white",
            command=self.guardar_cliente,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5, pady=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="Actualizar",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_cliente,
            **btn_style
        )
        btn_actualizar.grid(row=1, column=0, padx=5, pady=5)

        btn_eliminar = tk.Button(
            btn_frame,
            text="Eliminar",
            bg="#DC3545",
            fg="white",
            command=self.eliminar_cliente,
            **btn_style
        )
        btn_eliminar.grid(row=1, column=1, padx=5, pady=5)

        # Panel derecho - Lista de clientes
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Título lista
        tk.Label(
            panel_der,
            text="Lista de Clientes",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#0047AB"
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
        self.entry_buscar.bind('<KeyRelease>', self.buscar_cliente)

        btn_refresh = tk.Button(
            search_frame,
            text="↻",
            font=("Segoe UI", 12, "bold"),
            bg="#0047AB",
            fg="white",
            command=self.cargar_clientes,
            cursor="hand2",
            width=3,
            bd=0
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
            columns=("RUC", "Nombre Completo", "Correo", "Teléfono"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=20
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("RUC", text="RUC")
        self.tree.heading("Nombre Completo", text="Nombre Completo")
        self.tree.heading("Correo", text="Correo Electrónico")
        self.tree.heading("Teléfono", text="Teléfono")

        self.tree.column("RUC", width=100, anchor="center")
        self.tree.column("Nombre Completo", width=250)
        self.tree.column("Correo", width=200)
        self.tree.column("Teléfono", width=100, anchor="center")

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
            font=("Segoe UI", 10, "bold"),
            bg="white",
            anchor="e"
        )
        label.grid(row=fila, column=0, padx=10, pady=5, sticky="e")

    def validar_ruc(self, ruc):
        """Valida que el RUC tenga 11 dígitos"""
        return bool(re.match(r'^\d{11}$', ruc))

    def validar_telefono(self, telefono):
        """Valida que el teléfono tenga 9 dígitos"""
        if not telefono:
            return True  # Teléfono es opcional
        return bool(re.match(r'^\d{9}$', telefono))

    def validar_correo(self, correo):
        """Valida formato básico de correo electrónico"""
        if not correo:
            return True  # Correo es opcional
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo))

    def cargar_clientes(self):
        """Carga todos los clientes desde la base de datos"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    ruc,
                    CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
                    correo_electronico,
                    telefono
                FROM cliente
                ORDER BY apellido_paterno, apellido_materno, nombres
            """

            cursor.execute(query)
            self.clientes = cursor.fetchall()

            for cliente in self.clientes:
                self.tree.insert("", tk.END, values=cliente)

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes:\n{str(e)}")

    def buscar_cliente(self, event=None):
        """Busca clientes por RUC o nombre"""
        busqueda = self.entry_buscar.get().upper()

        self.tree.delete(*self.tree.get_children())

        for cliente in self.clientes:
            # Buscar en RUC o nombre completo
            if busqueda in str(cliente[0]).upper() or busqueda in str(cliente[1]).upper():
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

            query = """
                SELECT ruc, nombres, apellido_paterno, apellido_materno,
                       correo_electronico, pagina_web, telefono
                FROM cliente
                WHERE ruc = %s
            """
            cursor.execute(query, (valores[0],))

            cliente = cursor.fetchone()
            cursor.close()

            if cliente:
                self.ruc_seleccionado = cliente[0]

                # Limpiar campos
                self.entry_ruc.delete(0, tk.END)
                self.entry_nombres.delete(0, tk.END)
                self.entry_ap_paterno.delete(0, tk.END)
                self.entry_ap_materno.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_pagina_web.delete(0, tk.END)
                self.entry_telefono.delete(0, tk.END)

                # Cargar datos
                self.entry_ruc.insert(0, cliente[0])
                self.entry_nombres.insert(0, cliente[1])
                self.entry_ap_paterno.insert(0, cliente[2])
                self.entry_ap_materno.insert(0, cliente[3])
                self.entry_correo.insert(0, cliente[4] or "")
                self.entry_pagina_web.insert(0, cliente[5] or "")
                self.entry_telefono.insert(0, cliente[6] or "")

                # Deshabilitar RUC (es PK, no se puede cambiar)
                self.entry_ruc.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cliente:\n{str(e)}")

    def nuevo_cliente(self):
        """Limpia el formulario para un nuevo cliente"""
        self.ruc_seleccionado = None

        # Habilitar RUC
        self.entry_ruc.config(state='normal')

        # Limpiar campos
        self.entry_ruc.delete(0, tk.END)
        self.entry_nombres.delete(0, tk.END)
        self.entry_ap_paterno.delete(0, tk.END)
        self.entry_ap_materno.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_pagina_web.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)

        self.entry_ruc.focus()

    def guardar_cliente(self):
        """Guarda un nuevo cliente"""
        # Obtener valores
        ruc = self.entry_ruc.get().strip()
        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()
        correo = self.entry_correo.get().strip()
        pagina_web = self.entry_pagina_web.get().strip()
        telefono = self.entry_telefono.get().strip()

        # Validaciones
        if not ruc or not nombres or not ap_paterno or not ap_materno:
            messagebox.showwarning(
                "Advertencia",
                "RUC, Nombres, Apellido Paterno y Apellido Materno son obligatorios"
            )
            return

        if not self.validar_ruc(ruc):
            messagebox.showerror("Error", "El RUC debe tener exactamente 11 dígitos")
            return

        if not self.validar_telefono(telefono):
            messagebox.showerror("Error", "El teléfono debe tener exactamente 9 dígitos")
            return

        if not self.validar_correo(correo):
            messagebox.showerror("Error", "El formato del correo electrónico no es válido")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Llamar al procedimiento almacenado
            query = "CALL sp_insertar_cliente(%s, %s, %s, %s, %s, %s, %s)"

            valores = (
                ruc,
                nombres,
                ap_paterno,
                ap_materno,
                correo if correo else None,
                pagina_web if pagina_web else None,
                telefono if telefono else None
            )

            cursor.execute(query, valores)
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            self.cargar_clientes()
            self.nuevo_cliente()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cliente:\n{str(e)}")

    def actualizar_cliente(self):
        """Actualiza un cliente existente"""
        if not self.ruc_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para actualizar")
            return

        # Obtener valores
        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()
        correo = self.entry_correo.get().strip()
        pagina_web = self.entry_pagina_web.get().strip()
        telefono = self.entry_telefono.get().strip()

        # Validaciones
        if not nombres or not ap_paterno or not ap_materno:
            messagebox.showwarning(
                "Advertencia",
                "Nombres, Apellido Paterno y Apellido Materno son obligatorios"
            )
            return

        if not self.validar_telefono(telefono):
            messagebox.showerror("Error", "El teléfono debe tener exactamente 9 dígitos")
            return

        if not self.validar_correo(correo):
            messagebox.showerror("Error", "El formato del correo electrónico no es válido")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Llamar al procedimiento almacenado
            query = "CALL sp_actualizar_cliente(%s, %s, %s, %s, %s, %s, %s)"

            valores = (
                self.ruc_seleccionado,
                nombres,
                ap_paterno,
                ap_materno,
                correo if correo else None,
                pagina_web if pagina_web else None,
                telefono if telefono else None
            )

            cursor.execute(query, valores)
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            self.cargar_clientes()
            self.nuevo_cliente()

        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar cliente:\n{str(e)}")

    def eliminar_cliente(self):
        """Elimina un cliente"""
        if not self.ruc_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el cliente con RUC {self.ruc_seleccionado}?\n\n" +
            "Esta acción no se puede deshacer."
        )

        if not confirmacion:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL sp_eliminar_cliente(%s)"
            cursor.execute(query, (self.ruc_seleccionado,))
            conn.commit()

            # Consumir resultado del procedimiento
            cursor.fetchall()
            cursor.close()

            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            self.cargar_clientes()
            self.nuevo_cliente()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente:\n{str(e)}")
