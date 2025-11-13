"""
Módulo de Consultas SUNAT
Sistema JP Business Solutions
Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime

class ConsultaSUNAT:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Consultas SUNAT - JP Business Solutions")
        self.ventana.geometry("1100x650")
        self.ventana.configure(bg="#F5F5F5")

        self.crear_interfaz()
        self.cargar_consultas()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#0047AB", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="CONSULTAS SUNAT",
            font=("Arial", 16, "bold"),
            bg="#0047AB",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel superior - Formulario de consulta
        panel_consulta = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_consulta.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            panel_consulta,
            text="Nueva Consulta RUC",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=10)

        # Formulario de consulta
        form_frame = tk.Frame(panel_consulta, bg="white")
        form_frame.pack(padx=20, pady=10)

        tk.Label(form_frame, text="RUC:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.entry_ruc = tk.Entry(form_frame, font=("Arial", 10), width=20)
        self.entry_ruc.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tipo:", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(
            form_frame,
            values=["VALIDACION_RUC", "ESTADO_CONTRIBUYENTE", "COMPROBANTES", "OTROS"],
            state="readonly",
            font=("Arial", 10),
            width=20
        )
        self.combo_tipo.set("VALIDACION_RUC")
        self.combo_tipo.grid(row=0, column=3, padx=5, pady=5)

        btn_consultar = tk.Button(
            form_frame,
            text="Consultar",
            font=("Arial", 10, "bold"),
            bg="#28A745",
            fg="white",
            command=self.realizar_consulta,
            cursor="hand2",
            width=12
        )
        btn_consultar.grid(row=0, column=4, padx=10, pady=5)

        # Panel inferior - Historial
        panel_historial = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_historial.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            panel_historial,
            text="Historial de Consultas",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=10)

        # Filtros
        filter_frame = tk.Frame(panel_historial, bg="white")
        filter_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(filter_frame, text="Filtrar:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)

        self.entry_filtro = tk.Entry(filter_frame, font=("Arial", 10))
        self.entry_filtro.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        btn_refresh = tk.Button(
            filter_frame,
            text="↻ Actualizar",
            font=("Arial", 10, "bold"),
            bg="#0047AB",
            fg="white",
            command=self.cargar_consultas,
            cursor="hand2"
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de consultas
        tree_frame = tk.Frame(panel_historial, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "RUC", "Tipo", "Estado", "Condición", "Fecha", "Usuario"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("RUC", text="RUC Consultado")
        self.tree.heading("Tipo", text="Tipo Consulta")
        self.tree.heading("Estado", text="Estado SUNAT")
        self.tree.heading("Condición", text="Condición")
        self.tree.heading("Fecha", text="Fecha Consulta")
        self.tree.heading("Usuario", text="Usuario")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("RUC", width=110, anchor="center")
        self.tree.column("Tipo", width=150)
        self.tree.column("Estado", width=120, anchor="center")
        self.tree.column("Condición", width=120, anchor="center")
        self.tree.column("Fecha", width=150, anchor="center")
        self.tree.column("Usuario", width=100, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def cargar_consultas(self):
        """Carga todas las consultas SUNAT"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    id_consulta,
                    ruc_consultado,
                    tipo_consulta,
                    estado_sunat,
                    condicion_sunat,
                    DATE_FORMAT(fecha_consulta, '%Y-%m-%d %H:%i') AS fecha,
                    usuario_consulta
                FROM consulta_sunat
                ORDER BY id_consulta DESC
                LIMIT 100
            """

            cursor.execute(query)
            consultas = cursor.fetchall()

            for consulta in consultas:
                self.tree.insert("", tk.END, values=consulta)

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar consultas: {str(e)}")

    def realizar_consulta(self):
        """Simula una consulta a SUNAT y la registra"""
        ruc = self.entry_ruc.get().strip()

        if not ruc or len(ruc) != 11:
            messagebox.showwarning("Advertencia", "Ingrese un RUC válido (11 dígitos)")
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Simular consulta SUNAT (en producción, aquí iría la consulta real)
            estado_simulado = "ACTIVO"
            condicion_simulada = "HABIDO"

            query = """
                CALL sp_insertar_consulta_sunat(
                    NULL, %s, %s, %s, %s, %s, %s, %s
                )
            """

            valores = (
                ruc,
                self.combo_tipo.get(),
                f"Resultado de consulta para RUC {ruc}",
                estado_simulado,
                condicion_simulada,
                "admin",
                "Consulta realizada desde el sistema"
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Consulta Exitosa",
                f"RUC: {ruc}\nEstado: {estado_simulado}\nCondición: {condicion_simulada}"
            )

            self.cargar_consultas()
            self.entry_ruc.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar consulta: {str(e)}")
