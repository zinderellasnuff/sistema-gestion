"""
Módulo de Gestión de Archivos Excel
Sistema JP Business Solutions
Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models.config_db import Database

class GestionArchivosExcel:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Archivos Excel - JP Business Solutions")
        self.ventana.geometry("1100x650")
        self.ventana.configure(bg="#F5F5F5")

        self.crear_interfaz()
        self.cargar_archivos()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#0047AB", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="GESTIÓN DE ARCHIVOS EXCEL",
            font=("Arial", 16, "bold"),
            bg="#0047AB",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel superior - Acciones
        panel_acciones = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_acciones.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            panel_acciones,
            text="Operaciones con Archivos Excel",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=10)

        btn_frame = tk.Frame(panel_acciones, bg="white")
        btn_frame.pack(pady=15)

        btn_style = {
            "font": ("Arial", 10, "bold"),
            "width": 18,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat",
            "height": 2
        }

        btn_importar = tk.Button(
            btn_frame,
            text="📥 Importar Clientes",
            bg="#28A745",
            fg="white",
            command=self.importar_clientes,
            **btn_style
        )
        btn_importar.grid(row=0, column=0, padx=10)

        btn_exportar = tk.Button(
            btn_frame,
            text="📤 Exportar Clientes",
            bg="#17A2B8",
            fg="white",
            command=self.exportar_clientes,
            **btn_style
        )
        btn_exportar.grid(row=0, column=1, padx=10)

        btn_reporte = tk.Button(
            btn_frame,
            text="📊 Generar Reporte",
            bg="#FFC107",
            fg="black",
            command=self.generar_reporte,
            **btn_style
        )
        btn_reporte.grid(row=0, column=2, padx=10)

        # Panel inferior - Historial
        panel_historial = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_historial.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            panel_historial,
            text="Historial de Archivos Procesados",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#0047AB"
        ).pack(pady=10)

        # Filtros
        filter_frame = tk.Frame(panel_historial, bg="white")
        filter_frame.pack(pady=5, padx=10, fill=tk.X)

        tk.Label(filter_frame, text="Tipo:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)

        self.combo_filtro = ttk.Combobox(
            filter_frame,
            values=["TODOS", "IMPORTACION", "EXPORTACION", "REPORTE"],
            state="readonly",
            font=("Arial", 10),
            width=15
        )
        self.combo_filtro.set("TODOS")
        self.combo_filtro.pack(side=tk.LEFT, padx=5)
        self.combo_filtro.bind('<<ComboboxSelected>>', lambda e: self.cargar_archivos())

        btn_refresh = tk.Button(
            filter_frame,
            text="↻ Actualizar",
            font=("Arial", 10, "bold"),
            bg="#0047AB",
            fg="white",
            command=self.cargar_archivos,
            cursor="hand2"
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de archivos
        tree_frame = tk.Frame(panel_historial, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Archivo", "Tipo", "Procesados", "Exitosos", "Errores", "Estado", "Fecha"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=15
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Archivo", text="Nombre Archivo")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Procesados", text="Procesados")
        self.tree.heading("Exitosos", text="Exitosos")
        self.tree.heading("Errores", text="Errores")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Fecha", text="Fecha")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Archivo", width=250)
        self.tree.column("Tipo", width=100, anchor="center")
        self.tree.column("Procesados", width=90, anchor="center")
        self.tree.column("Exitosos", width=80, anchor="center")
        self.tree.column("Errores", width=80, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")
        self.tree.column("Fecha", width=150, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def cargar_archivos(self):
        """Carga el historial de archivos procesados"""
        try:
            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            filtro = self.combo_filtro.get()

            if filtro == "TODOS":
                query = """
                    SELECT
                        id_archivo,
                        nombre_archivo,
                        tipo_operacion,
                        registros_procesados,
                        registros_exitosos,
                        registros_con_error,
                        estado_procesamiento,
                        DATE_FORMAT(fecha_procesamiento, '%Y-%m-%d %H:%i') AS fecha
                    FROM archivo_excel_gestion_clientes
                    ORDER BY id_archivo DESC
                    LIMIT 50
                """
                cursor.execute(query)
            else:
                query = """
                    SELECT
                        id_archivo,
                        nombre_archivo,
                        tipo_operacion,
                        registros_procesados,
                        registros_exitosos,
                        registros_con_error,
                        estado_procesamiento,
                        DATE_FORMAT(fecha_procesamiento, '%Y-%m-%d %H:%i') AS fecha
                    FROM archivo_excel_gestion_clientes
                    WHERE tipo_operacion = %s
                    ORDER BY id_archivo DESC
                    LIMIT 50
                """
                cursor.execute(query, (filtro,))

            archivos = cursor.fetchall()

            for archivo in archivos:
                # Color según estado
                tags = ()
                if archivo[6] == 'COMPLETADO':
                    tags = ('completado',)
                elif archivo[6] == 'ERROR':
                    tags = ('error',)

                self.tree.insert("", tk.END, values=archivo, tags=tags)

            # Configurar colores
            self.tree.tag_configure('completado', foreground='green')
            self.tree.tag_configure('error', foreground='red')

            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar archivos: {str(e)}")

    def importar_clientes(self):
        """Simula la importación de clientes desde Excel"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )

        if not archivo:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Simular procesamiento
            nombre_archivo = archivo.split('/')[-1]

            query = """
                CALL sp_insertar_archivo_excel(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            valores = (
                nombre_archivo,
                archivo,
                'IMPORTACION',
                100,  # simulado
                95,   # simulado
                5,    # simulado
                'admin',
                'COMPLETADO',
                'Ninguno',
                'Importación simulada'
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Importación Exitosa",
                f"Archivo: {nombre_archivo}\nRegistros procesados: 95/100"
            )

            self.cargar_archivos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al importar: {str(e)}")

    def exportar_clientes(self):
        """Simula la exportación de clientes a Excel"""
        archivo = filedialog.asksaveasfilename(
            title="Guardar archivo Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )

        if not archivo:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Obtener total de clientes
            cursor.execute("SELECT COUNT(*) FROM cliente WHERE estado = 'ACTIVO'")
            total = cursor.fetchone()[0]

            nombre_archivo = archivo.split('/')[-1]

            query = """
                CALL sp_insertar_archivo_excel(
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

            valores = (
                nombre_archivo,
                archivo,
                'EXPORTACION',
                total,
                total,
                0,
                'admin',
                'COMPLETADO',
                'Ninguno',
                'Exportación de clientes activos'
            )

            cursor.execute(query, valores)
            conn.commit()
            cursor.close()

            messagebox.showinfo(
                "Exportación Exitosa",
                f"Archivo: {nombre_archivo}\nClientes exportados: {total}"
            )

            self.cargar_archivos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def generar_reporte(self):
        """Genera un reporte en Excel"""
        messagebox.showinfo(
            "Generar Reporte",
            "Seleccione el tipo de reporte:\n\n- Clientes por Departamento\n- Resumen de Ventas\n- Auditoría\n\n(Funcionalidad en desarrollo)"
        )
