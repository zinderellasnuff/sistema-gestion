"""
Módulo Dashboard del Sistema
Sistema de Gestión Empresarial
Dashboard con estadísticas y gráficos en tiempo real
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ModuloConfiguracion:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Dashboard - Sistema de Gestión")
        self.ventana.geometry("1400x800")
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
        header = tk.Frame(self.ventana, bg="#0047AB", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        titulo = tk.Label(
            header,
            text="📊 DASHBOARD EMPRESARIAL",
            font=("Segoe UI", 18, "bold"),
            bg="#0047AB",
            fg="white"
        )
        titulo.pack(pady=25)

        # Contenedor principal con scroll
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Canvas para scroll
        canvas = tk.Canvas(main_container, bg="#F5F5F5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F5F5F5")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Contenido del dashboard
        content_frame = tk.Frame(scrollable_frame, bg="#F5F5F5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Sección 1: Cards de Estadísticas Rápidas
        self.crear_seccion_cards(content_frame)

        # Sección 2: Gráficos
        self.crear_seccion_graficos(content_frame)

        # Sección 3: Base de Datos
        self.crear_seccion_base_datos(content_frame)

        # Botones de acción
        botones_frame = tk.Frame(scrollable_frame, bg="#F5F5F5")
        botones_frame.pack(pady=20)

        btn_actualizar = tk.Button(
            botones_frame,
            text="🔄 Actualizar Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#28A745",
            fg="white",
            command=self.actualizar_todo,
            cursor="hand2",
            bd=0,
            padx=30,
            pady=12
        )
        btn_actualizar.pack(side=tk.LEFT, padx=10)

        btn_volver = tk.Button(
            botones_frame,
            text="← Volver al Menú Principal",
            font=("Segoe UI", 11, "bold"),
            bg="#6C757D",
            fg="white",
            command=self.cerrar_ventana,
            cursor="hand2",
            bd=0,
            padx=30,
            pady=12
        )
        btn_volver.pack(side=tk.LEFT, padx=10)

    def crear_seccion_cards(self, parent):
        """Crea la sección de tarjetas de estadísticas"""
        titulo_seccion = tk.Label(
            parent,
            text="📈 Resumen General del Sistema",
            font=("Segoe UI", 15, "bold"),
            bg="#F5F5F5",
            fg="#333333"
        )
        titulo_seccion.pack(pady=(10, 20), anchor="w")

        # Frame para cards
        cards_container = tk.Frame(parent, bg="#F5F5F5")
        cards_container.pack(fill=tk.X, pady=(0, 30))

        # Grid 2x4
        for i in range(2):
            cards_container.grid_rowconfigure(i, weight=1)
        for j in range(4):
            cards_container.grid_columnconfigure(j, weight=1)

        # Cards
        self.card_clientes = self.crear_stat_card(
            cards_container, "👥", "Total Clientes", "0", "#28A745", 0, 0
        )
        self.card_empleados = self.crear_stat_card(
            cards_container, "👔", "Total Empleados", "0", "#007BFF", 0, 1
        )
        self.card_consultas = self.crear_stat_card(
            cards_container, "🔍", "Consultas SUNAT", "0", "#FFC107", 0, 2
        )
        self.card_archivos = self.crear_stat_card(
            cards_container, "📊", "Archivos Excel", "0", "#17A2B8", 0, 3
        )
        self.card_activos = self.crear_stat_card(
            cards_container, "✅", "Clientes Activos", "0", "#20C997", 1, 0
        )
        self.card_inactivos = self.crear_stat_card(
            cards_container, "⚠️", "Con Problemas", "0", "#DC3545", 1, 1
        )
        self.card_auditoria = self.crear_stat_card(
            cards_container, "🔒", "Registros Auditoría", "0", "#6F42C1", 1, 2
        )
        self.card_usuarios = self.crear_stat_card(
            cards_container, "👤", "Usuarios Sistema", "0", "#FD7E14", 1, 3
        )

    def crear_stat_card(self, parent, icono, titulo, valor, color, fila, columna):
        """Crea una tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
        card.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")

        # Icono
        lbl_icono = tk.Label(
            card,
            text=icono,
            font=("Segoe UI", 32),
            bg=color,
            fg="white"
        )
        lbl_icono.pack(pady=(15, 5))

        # Valor
        lbl_valor = tk.Label(
            card,
            text=valor,
            font=("Segoe UI", 24, "bold"),
            bg=color,
            fg="white"
        )
        lbl_valor.pack()

        # Título
        lbl_titulo = tk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 10),
            bg=color,
            fg="white"
        )
        lbl_titulo.pack(pady=(5, 15))

        return lbl_valor

    def crear_seccion_graficos(self, parent):
        """Crea la sección de gráficos con matplotlib"""
        titulo_seccion = tk.Label(
            parent,
            text="📊 Visualización de Datos",
            font=("Segoe UI", 15, "bold"),
            bg="#F5F5F5",
            fg="#333333"
        )
        titulo_seccion.pack(pady=(20, 20), anchor="w")

        # Frame para gráficos
        graficos_container = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
        graficos_container.pack(fill=tk.BOTH, expand=True, pady=(0, 30))

        # Configurar grid 1x2 para dos gráficos lado a lado
        graficos_container.grid_columnconfigure(0, weight=1)
        graficos_container.grid_columnconfigure(1, weight=1)

        # Frame para gráfico de barras
        frame_barras = tk.Frame(graficos_container, bg="white")
        frame_barras.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Frame para gráfico circular
        frame_pie = tk.Frame(graficos_container, bg="white")
        frame_pie.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        # Crear figuras de matplotlib
        self.crear_grafico_barras(frame_barras)
        self.crear_grafico_circular(frame_pie)

    def crear_grafico_barras(self, parent):
        """Crea gráfico de barras con estadísticas generales"""
        titulo = tk.Label(
            parent,
            text="Registros por Módulo",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#333333"
        )
        titulo.pack(pady=(10, 5))

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=80)
        ax = fig.add_subplot(111)

        # Datos iniciales (se actualizarán)
        self.datos_barras = {
            'Clientes': 0,
            'Empleados': 0,
            'Consultas': 0,
            'Archivos': 0
        }

        # Configurar gráfico
        categorias = list(self.datos_barras.keys())
        valores = list(self.datos_barras.values())
        colores = ['#28A745', '#007BFF', '#FFC107', '#17A2B8']

        bars = ax.bar(categorias, valores, color=colores, alpha=0.8, edgecolor='black')
        ax.set_ylabel('Cantidad de Registros', fontsize=10, fontweight='bold')
        ax.set_title('Distribución de Registros', fontsize=11, fontweight='bold', pad=10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        # Agregar valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=9)

        fig.tight_layout()

        # Guardar referencia para actualizar
        self.ax_barras = ax
        self.fig_barras = fig

        # Añadir a tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def crear_grafico_circular(self, parent):
        """Crea gráfico circular con estado de clientes"""
        titulo = tk.Label(
            parent,
            text="Estado de Clientes SUNAT",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#333333"
        )
        titulo.pack(pady=(10, 5))

        # Crear figura
        fig = Figure(figsize=(6, 4), dpi=80)
        ax = fig.add_subplot(111)

        # Datos iniciales (se actualizarán)
        self.datos_pie = {
            'Activos': 1,
            'Con Problemas': 1,
            'Sin Consultar': 1
        }

        # Configurar gráfico
        labels = list(self.datos_pie.keys())
        sizes = list(self.datos_pie.values())
        colores = ['#20C997', '#DC3545', '#6C757D']
        explode = (0.05, 0.05, 0)

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            colors=colores,
            explode=explode,
            shadow=True,
            startangle=90
        )

        # Mejorar estilo
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')

        ax.set_title('Distribución por Estado', fontsize=11, fontweight='bold', pad=10)
        fig.tight_layout()

        # Guardar referencia para actualizar
        self.ax_pie = ax
        self.fig_pie = fig

        # Añadir a tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def crear_seccion_base_datos(self, parent):
        """Crea la sección de información de base de datos"""
        titulo_seccion = tk.Label(
            parent,
            text="🗄️ Información de Base de Datos",
            font=("Segoe UI", 15, "bold"),
            bg="#F5F5F5",
            fg="#333333"
        )
        titulo_seccion.pack(pady=(20, 20), anchor="w")

        # Frame contenedor
        db_container = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
        db_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Información general
        info_frame = tk.Frame(db_container, bg="white")
        info_frame.pack(fill=tk.X, padx=30, pady=20)

        info_items = [
            ("🗄️ Base de Datos:", "gestion_clientes_jp"),
            ("📊 Motor:", "MariaDB/MySQL"),
            ("📅 Última Actualización:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ("🔧 Estado:", "● Conectado")
        ]

        for etiqueta, valor in info_items:
            frame = tk.Frame(info_frame, bg="white")
            frame.pack(fill=tk.X, pady=5)

            lbl_etiqueta = tk.Label(
                frame,
                text=etiqueta,
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#333333",
                width=25,
                anchor="w"
            )
            lbl_etiqueta.pack(side=tk.LEFT, padx=10)

            color_valor = "#28A745" if valor == "● Conectado" else "#666666"
            lbl_valor = tk.Label(
                frame,
                text=valor,
                font=("Segoe UI", 11),
                bg="white",
                fg=color_valor,
                anchor="w"
            )
            lbl_valor.pack(side=tk.LEFT, padx=10)

        # Separador
        ttk.Separator(db_container, orient='horizontal').pack(fill=tk.X, pady=20, padx=30)

        # Tabla de información
        tabla_titulo = tk.Label(
            db_container,
            text="📋 Estructura de Tablas",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#333333"
        )
        tabla_titulo.pack(pady=(0, 15))

        tree_frame = tk.Frame(db_container, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

        # Scrollbar
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)

        # Treeview
        self.tree_tablas = ttk.Treeview(
            tree_frame,
            columns=("Tabla", "Tipo", "Registros"),
            show="headings",
            yscrollcommand=scroll_y.set,
            height=8
        )

        scroll_y.config(command=self.tree_tablas.yview)

        self.tree_tablas.heading("Tabla", text="Nombre de Tabla")
        self.tree_tablas.heading("Tipo", text="Tipo")
        self.tree_tablas.heading("Registros", text="Registros")

        self.tree_tablas.column("Tabla", width=300, anchor="w")
        self.tree_tablas.column("Tipo", width=200, anchor="center")
        self.tree_tablas.column("Registros", width=150, anchor="center")

        # Estilo para el treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)

        self.tree_tablas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar información de tablas
        self.cargar_info_tablas()

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

            # Total registros de auditoría
            cursor.execute("""
                SELECT
                    (SELECT COUNT(*) FROM auditoria_cliente) +
                    (SELECT COUNT(*) FROM auditoria_empleado) +
                    (SELECT COUNT(*) FROM auditoria_archivo_excel) +
                    (SELECT COUNT(*) FROM auditoria_accesos) AS total
            """)
            total_auditoria = cursor.fetchone()[0]
            self.card_auditoria.config(text=str(total_auditoria))

            # Total usuarios
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = TRUE")
            total_usuarios = cursor.fetchone()[0]
            self.card_usuarios.config(text=str(total_usuarios))

            # Actualizar datos para gráficos
            self.datos_barras = {
                'Clientes': total_clientes,
                'Empleados': total_empleados,
                'Consultas': total_consultas,
                'Archivos': total_archivos
            }

            # Clientes sin consultar
            cursor.execute("""
                SELECT COUNT(*)
                FROM cliente c
                LEFT JOIN consulta_sunat cs ON c.ruc = cs.nro_consultado
                WHERE cs.nro_consultado IS NULL
            """)
            sin_consultar = cursor.fetchone()[0]

            self.datos_pie = {
                'Activos': clientes_activos if clientes_activos > 0 else 1,
                'Con Problemas': clientes_problemas if clientes_problemas > 0 else 1,
                'Sin Consultar': sin_consultar if sin_consultar > 0 else 1
            }

            cursor.close()

            # Actualizar gráficos
            self.actualizar_graficos()

        except Exception as e:
            self.mostrar_error("Error al cargar estadísticas", str(e))

    def actualizar_graficos(self):
        """Actualiza los gráficos con nuevos datos"""
        try:
            # Actualizar gráfico de barras
            self.ax_barras.clear()
            categorias = list(self.datos_barras.keys())
            valores = list(self.datos_barras.values())
            colores = ['#28A745', '#007BFF', '#FFC107', '#17A2B8']

            bars = self.ax_barras.bar(categorias, valores, color=colores, alpha=0.8, edgecolor='black')
            self.ax_barras.set_ylabel('Cantidad de Registros', fontsize=10, fontweight='bold')
            self.ax_barras.set_title('Distribución de Registros', fontsize=11, fontweight='bold', pad=10)
            self.ax_barras.grid(axis='y', alpha=0.3, linestyle='--')

            for bar in bars:
                height = bar.get_height()
                self.ax_barras.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontweight='bold', fontsize=9)

            self.fig_barras.canvas.draw()

            # Actualizar gráfico circular
            self.ax_pie.clear()
            labels = list(self.datos_pie.keys())
            sizes = list(self.datos_pie.values())
            colores = ['#20C997', '#DC3545', '#6C757D']
            explode = (0.05, 0.05, 0)

            wedges, texts, autotexts = self.ax_pie.pie(
                sizes,
                labels=labels,
                autopct='%1.1f%%',
                colors=colores,
                explode=explode,
                shadow=True,
                startangle=90
            )

            for text in texts:
                text.set_fontsize(10)
                text.set_fontweight('bold')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_fontweight('bold')

            self.ax_pie.set_title('Distribución por Estado', fontsize=11, fontweight='bold', pad=10)
            self.fig_pie.canvas.draw()

        except Exception as e:
            print(f"Error al actualizar gráficos: {e}")

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
                ("usuarios", "Sistema", "SELECT COUNT(*) FROM usuarios"),
                ("auditoria_cliente", "Auditoría", "SELECT COUNT(*) FROM auditoria_cliente"),
                ("auditoria_empleado", "Auditoría", "SELECT COUNT(*) FROM auditoria_empleado"),
                ("auditoria_archivo_excel", "Auditoría", "SELECT COUNT(*) FROM auditoria_archivo_excel"),
                ("auditoria_accesos", "Auditoría", "SELECT COUNT(*) FROM auditoria_accesos"),
            ]

            for tabla, tipo, query in tablas_info:
                try:
                    cursor.execute(query)
                    count = cursor.fetchone()[0]
                    self.tree_tablas.insert("", tk.END, values=(tabla, tipo, count))
                except:
                    self.tree_tablas.insert("", tk.END, values=(tabla, tipo, "N/A"))

            cursor.close()

        except Exception as e:
            self.mostrar_error("Error al cargar info de tablas", str(e))

    def actualizar_todo(self):
        """Actualiza todas las estadísticas y gráficos"""
        self.cargar_estadisticas()
        self.cargar_info_tablas()
        messagebox.showinfo(
            "Dashboard Actualizado",
            "Todas las estadísticas han sido actualizadas correctamente",
            parent=self.ventana
        )

    def mostrar_error(self, titulo, mensaje):
        """Muestra mensaje de error"""
        messagebox.showerror(f"✗ {titulo}", mensaje, parent=self.ventana)
