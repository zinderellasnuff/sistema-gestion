"""
Módulo de Configuración del Sistema
Sistema Gestion De Clientes
Versión: 1.0 - Completo y Funcional
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime

class ModuloConfiguracion:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Configuración del Sistema")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#F5F5F5")
        
        # Configurar para que se cierre correctamente
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.crear_interfaz()
        self.cargar_estadisticas()

    def cerrar_ventana(self):
        """Cierra la ventana correctamente"""
        self.ventana.destroy()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#6C757D", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="⚙️ CONFIGURACIÓN DEL SISTEMA",
            font=("Segoe UI", 16, "bold"),
            bg="#6C757D",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Crear notebook (pestañas)
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Estadísticas del Sistema
        tab_estadisticas = tk.Frame(notebook, bg="white")
        notebook.add(tab_estadisticas, text="📊 Estadísticas")
        self.crear_tab_estadisticas(tab_estadisticas)

        # Pestaña 2: Base de Datos
        tab_base_datos = tk.Frame(notebook, bg="white")
        notebook.add(tab_base_datos, text="🗄️ Base de Datos")
        self.crear_tab_base_datos(tab_base_datos)

        # Pestaña 3: Información del Sistema
        tab_info = tk.Frame(notebook, bg="white")
        notebook.add(tab_info, text="ℹ️ Información")
        self.crear_tab_informacion(tab_info)

    def crear_tab_estadisticas(self, parent):
        """Crea la pestaña de estadísticas"""
        # Título
        titulo = tk.Label(
            parent,
            text="Estadísticas Generales del Sistema",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        titulo.pack(pady=20)

        # Frame para cards de estadísticas
        stats_container = tk.Frame(parent, bg="white")
        stats_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Grid 2x3
        for i in range(2):
            stats_container.grid_rowconfigure(i, weight=1)
        for j in range(3):
            stats_container.grid_columnconfigure(j, weight=1)

        # Cards de estadísticas
        self.card_clientes = self.crear_stat_card(
            stats_container, "👥", "Clientes", "0", "#28A745", 0, 0
        )
        self.card_empleados = self.crear_stat_card(
            stats_container, "👔", "Empleados", "0", "#007BFF", 0, 1
        )
        self.card_consultas = self.crear_stat_card(
            stats_container, "🔍", "Consultas SUNAT", "0", "#FFC107", 0, 2
        )
        self.card_archivos = self.crear_stat_card(
            stats_container, "📊", "Archivos Excel", "0", "#17A2B8", 1, 0
        )
        self.card_activos = self.crear_stat_card(
            stats_container, "✅", "Clientes Activos", "0", "#28A745", 1, 1
        )
        self.card_inactivos = self.crear_stat_card(
            stats_container, "⚠️", "Con Problemas", "0", "#DC3545", 1, 2
        )

        # Frame para botones
        botones_frame = tk.Frame(parent, bg="white")
        botones_frame.pack(pady=20)

        # Botón actualizar
        btn_actualizar = tk.Button(
            botones_frame,
            text="🔄 Actualizar Estadísticas",
            font=("Segoe UI", 10, "bold"),
            bg="#6C757D",
            fg="white",
            command=self.cargar_estadisticas,
            cursor="hand2",
            bd=0,
            padx=20,
            pady=10
        )
        btn_actualizar.pack(side=tk.LEFT, padx=5)

        # Botón volver
        btn_volver = tk.Button(
            botones_frame,
            text="← Volver al Menú Principal",
            font=("Segoe UI", 10, "bold"),
            bg="#495057",
            fg="white",
            command=self.cerrar_ventana,
            cursor="hand2",
            bd=0,
            padx=20,
            pady=10
        )
        btn_volver.pack(side=tk.LEFT, padx=5)

    def crear_stat_card(self, parent, icono, titulo, valor, color, fila, columna):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
        card.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        # Icono
        lbl_icono = tk.Label(
            card,
            text=icono,
            font=("Segoe UI", 36),
            bg=color,
            fg="white"
        )
        lbl_icono.pack(pady=(20, 10))

        # Valor
        lbl_valor = tk.Label(
            card,
            text=valor,
            font=("Segoe UI", 28, "bold"),
            bg=color,
            fg="white"
        )
        lbl_valor.pack()

        # Título
        lbl_titulo = tk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 11),
            bg=color,
            fg="white"
        )
        lbl_titulo.pack(pady=(5, 20))

        return lbl_valor

    def crear_tab_base_datos(self, parent):
        """Crea la pestaña de base de datos"""
        titulo = tk.Label(
            parent,
            text="Información de la Base de Datos",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        titulo.pack(pady=20)

        # Frame para información
        info_frame = tk.Frame(parent, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Información de la BD
        info_items = [
            ("🗄️ Base de Datos:", "gestion_clientes_jp"),
            ("📊 Motor:", "MariaDB/MySQL"),
            ("🔧 Versión:", "10.x / 8.x"),
            ("🏢 Sistema:", "Gestion De Clientes"),
            ("📅 Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]

        for i, (etiqueta, valor) in enumerate(info_items):
            frame = tk.Frame(info_frame, bg="white")
            frame.pack(fill=tk.X, pady=10)

            lbl_etiqueta = tk.Label(
                frame,
                text=etiqueta,
                font=("Segoe UI", 12, "bold"),
                bg="white",
                fg="#333333",
                width=20,
                anchor="w"
            )
            lbl_etiqueta.pack(side=tk.LEFT, padx=10)

            lbl_valor = tk.Label(
                frame,
                text=valor,
                font=("Segoe UI", 12),
                bg="white",
                fg="#666666",
                anchor="w"
            )
            lbl_valor.pack(side=tk.LEFT, padx=10)

        # Separador
        ttk.Separator(info_frame, orient='horizontal').pack(fill=tk.X, pady=30)

        # Información de tablas
        titulo_tablas = tk.Label(
            info_frame,
            text="📋 Estructura de la Base de Datos",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#333333"
        )
        titulo_tablas.pack(pady=(0, 20))

        # Frame para tabla
        tree_frame = tk.Frame(info_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)

        self.tree_tablas = ttk.Treeview(
            tree_frame,
            columns=("Tabla", "Tipo", "Registros"),
            show="headings",
            yscrollcommand=scroll_y.set,
            height=10
        )

        scroll_y.config(command=self.tree_tablas.yview)

        self.tree_tablas.heading("Tabla", text="Nombre de Tabla")
        self.tree_tablas.heading("Tipo", text="Tipo")
        self.tree_tablas.heading("Registros", text="Registros")

        self.tree_tablas.column("Tabla", width=250)
        self.tree_tablas.column("Tipo", width=200, anchor="center")
        self.tree_tablas.column("Registros", width=150, anchor="center")

        self.tree_tablas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar información de tablas
        self.cargar_info_tablas()

        # Frame para botones
        botones_frame = tk.Frame(parent, bg="white")
        botones_frame.pack(pady=20)

        # Botón actualizar
        btn_actualizar = tk.Button(
            botones_frame,
            text="🔄 Actualizar Información",
            font=("Segoe UI", 10, "bold"),
            bg="#6C757D",
            fg="white",
            command=self.cargar_info_tablas,
            cursor="hand2",
            bd=0,
            padx=20,
            pady=10
        )
        btn_actualizar.pack(side=tk.LEFT, padx=5)

        # Botón volver
        btn_volver = tk.Button(
            botones_frame,
            text="← Volver al Menú Principal",
            font=("Segoe UI", 10, "bold"),
            bg="#495057",
            fg="white",
            command=self.cerrar_ventana,
            cursor="hand2",
            bd=0,
            padx=20,
            pady=10
        )
        btn_volver.pack(side=tk.LEFT, padx=5)

    def crear_tab_informacion(self, parent):
        """Crea la pestaña de información del sistema"""
        titulo = tk.Label(
            parent,
            text="Información del Sistema",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        titulo.pack(pady=20)

        # Frame contenedor
        info_container = tk.Frame(parent, bg="white")
        info_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Logo y nombre
        logo_frame = tk.Frame(info_container, bg="#E9ECEF", relief=tk.RAISED, bd=2)
        logo_frame.pack(fill=tk.X, pady=(0, 30))

        tk.Label(
            logo_frame,
            text="🏢",
            font=("Segoe UI", 48),
            bg="#E9ECEF"
        ).pack(pady=20)

        tk.Label(
            logo_frame,
            text="Gestion De Clientes",
            font=("Segoe UI", 18, "bold"),
            bg="#E9ECEF",
            fg="#0047AB"
        ).pack()

        tk.Label(
            logo_frame,
            text="Sistema Integrado de Gestión Empresarial",
            font=("Segoe UI", 11),
            bg="#E9ECEF",
            fg="#666666"
        ).pack(pady=(5, 20))

        # Información del sistema
        info_text = """
📋 Versión: 1.0.0
📅 Fecha de Desarrollo: 2025
👨‍💻 Desarrollador: Aron - UCSM
🎓 Universidad: Universidad Católica de Santa María
📚 Curso: Base de Datos

🔧 Componentes del Sistema:
- Gestión de Clientes (CRUD completo)
- Gestión de Empleados (CRUD completo)
- Consultas SUNAT (Validación de RUC)
- Gestión de Archivos Excel
- Reportes y Análisis (13 reportes con JOINs)

💾 Base de Datos:
- 7 Tablas principales
- 9 Triggers de auditoría
- 13 Procedimientos almacenados
- 20 Funciones SQL
- 2 Vistas personalizadas

🔒 Características:
- Validaciones completas en frontend y backend
- Auditoría automática de operaciones
- Interfaz gráfica profesional con Tkinter
- Arquitectura MVC simplificada
        """

        text_widget = tk.Text(
            info_container,
            font=("Segoe UI", 10),
            bg="#F8F9FA",
            fg="#333333",
            relief=tk.FLAT,
            padx=20,
            pady=20,
            wrap=tk.WORD,
            height=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", info_text)
        text_widget.config(state=tk.DISABLED)

        # Botón de navegación - Volver al menú
        btn_volver = tk.Button(
            parent,
            text="← Volver al Menú Principal",
            font=("Segoe UI", 10, "bold"),
            bg="#6C757D",
            fg="white",
            command=self.cerrar_ventana,
            cursor="hand2",
            bd=0,
            padx=30,
            pady=12
        )
        btn_volver.pack(pady=10)

        # Footer
        footer_label = tk.Label(
            parent,
            text="© 2025 Todos los derechos reservados",
            font=("Segoe UI", 9),
            bg="white",
            fg="#999999"
        )
        footer_label.pack(pady=10)

    def cargar_estadisticas(self):
        """Carga las estadísticas del sistema"""
        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Total clientes
            cursor.execute("SELECT COUNT(*) FROM cliente")
            total_clientes = cursor.fetchone()[0]
            self.card_clientes.config(text=str(total_clientes))

            # Total empleados
            cursor.execute("SELECT COUNT(*) FROM empleado")
            total_empleados = cursor.fetchone()[0]
            self.card_empleados.config(text=str(total_empleados))

            # Total consultas SUNAT
            cursor.execute("SELECT COUNT(*) FROM consulta_sunat")
            total_consultas = cursor.fetchone()[0]
            self.card_consultas.config(text=str(total_consultas))

            # Total archivos
            cursor.execute("SELECT COUNT(*) FROM archivo_excel_gestion_clientes")
            total_archivos = cursor.fetchone()[0]
            self.card_archivos.config(text=str(total_archivos))

            # Clientes con estado ACTIVO
            cursor.execute("""
                SELECT COUNT(DISTINCT c.ruc) 
                FROM cliente c
                LEFT JOIN consulta_sunat cs ON c.ruc = cs.nro_consultado
                WHERE cs.estado = 'ACTIVO' AND cs.condicion = 'HABIDO'
            """)
            clientes_activos = cursor.fetchone()[0]
            self.card_activos.config(text=str(clientes_activos))

            # Clientes con problemas
            cursor.execute("""
                SELECT COUNT(DISTINCT c.ruc) 
                FROM cliente c
                LEFT JOIN consulta_sunat cs ON c.ruc = cs.nro_consultado
                WHERE cs.estado IS NOT NULL 
                  AND (cs.estado != 'ACTIVO' OR cs.condicion != 'HABIDO')
            """)
            clientes_problemas = cursor.fetchone()[0]
            self.card_inactivos.config(text=str(clientes_problemas))

            cursor.close()

        except Exception as e:
            self.mostrar_error("Error al cargar estadísticas", str(e))

    def cargar_info_tablas(self):
        """Carga información de las tablas"""
        try:
            # Limpiar tree
            for item in self.tree_tablas.get_children():
                self.tree_tablas.delete(item)

            conn = Database.conectar()
            cursor = conn.cursor()

            tablas_info = [
                ("cliente", "Principal", "SELECT COUNT(*) FROM cliente"),
                ("empleado", "Principal", "SELECT COUNT(*) FROM empleado"),
                ("consulta_sunat", "Principal", "SELECT COUNT(*) FROM consulta_sunat"),
                ("archivo_excel_gestion_clientes", "Principal", "SELECT COUNT(*) FROM archivo_excel_gestion_clientes"),
                ("auditoria_cliente", "Auditoría", "SELECT COUNT(*) FROM auditoria_cliente"),
                ("auditoria_empleado", "Auditoría", "SELECT COUNT(*) FROM auditoria_empleado"),
                ("auditoria_archivo_excel", "Auditoría", "SELECT COUNT(*) FROM auditoria_archivo_excel"),
            ]

            for tabla, tipo, query in tablas_info:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                self.tree_tablas.insert("", tk.END, values=(tabla, tipo, count))

            cursor.close()

        except Exception as e:
            self.mostrar_error("Error al cargar info de tablas", str(e))

    def mostrar_error(self, titulo, mensaje):
        """Muestra mensaje de error"""
        messagebox.showerror(f"✗ {titulo}", mensaje, parent=self.ventana)
