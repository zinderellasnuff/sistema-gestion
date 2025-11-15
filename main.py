import tkinter as tk
from tkinter import messagebox, ttk
from models.config_db import Database
from views.modulo_clientes import GestionClientes
from views.modulo_empleados import GestionEmpleados
from views.modulo_consulta_sunat import ConsultaSUNAT
from views.modulo_archivos_excel import GestionArchivosExcel
from views.modulo_reportes import ModuloReportes

class AplicativoJP:

    def __init__(self, root):
        self.root = root
        self.root.title("JP Business Solutions - Sistema de Gestión")
        self.root.geometry("1100x700")
        self.root.configure(bg="#F5F5F5")

        # Centrar ventana
        self.centrar_ventana()

        try:
            Database.conectar()
            print("✓ Conectado a MySQL")
            self.crear_interfaz()
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"Error de conexión a la base de datos:\n{e}")

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_interfaz(self):
        # Header con degradado visual
        header_frame = tk.Frame(self.root, bg="#0047AB", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Logo y título
        titulo_container = tk.Frame(header_frame, bg="#0047AB")
        titulo_container.pack(expand=True)

        titulo = tk.Label(
            titulo_container,
            text="JP BUSINESS SOLUTIONS",
            font=("Segoe UI", 22, "bold"),
            bg="#0047AB",
            fg="white"
        )
        titulo.pack(pady=(15, 5))

        subtitulo_header = tk.Label(
            titulo_container,
            text="Sistema Integrado de Gestión Empresarial",
            font=("Segoe UI", 11),
            bg="#0047AB",
            fg="#B8D4FF"
        )
        subtitulo_header.pack()

        # Contenido principal con sombra
        main_container = tk.Frame(self.root, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Bienvenida
        welcome_frame = tk.Frame(main_container, bg="#F5F5F5")
        welcome_frame.pack(pady=(0, 25))

        welcome_label = tk.Label(
            welcome_frame,
            text="🏢 Panel de Control Principal",
            font=("Segoe UI", 16, "bold"),
            bg="#F5F5F5",
            fg="#333333"
        )
        welcome_label.pack()

        descripcion = tk.Label(
            welcome_frame,
            text="Seleccione el módulo con el que desea trabajar",
            font=("Segoe UI", 10),
            bg="#F5F5F5",
            fg="#666666"
        )
        descripcion.pack(pady=(5, 0))

        # Grid de módulos (2 columnas)
        modules_frame = tk.Frame(main_container, bg="#F5F5F5")
        modules_frame.pack(pady=10)

        # Configurar grid
        modules_frame.columnconfigure(0, weight=1)
        modules_frame.columnconfigure(1, weight=1)

        # Módulo 1: Gestión de Clientes
        self.crear_tarjeta_modulo(
            modules_frame,
            "👥 GESTIÓN DE CLIENTES",
            "Administrar información de clientes, RUC, contactos y más",
            "#28A745",
            self.gestion_clientes,
            0, 0
        )

        # Módulo 2: Gestión de Empleados
        self.crear_tarjeta_modulo(
            modules_frame,
            "👔 GESTIÓN DE EMPLEADOS",
            "Administrar personal, cargos, salarios y áreas",
            "#007BFF",
            self.gestion_empleados,
            0, 1
        )

        # Módulo 3: Consultas SUNAT
        self.crear_tarjeta_modulo(
            modules_frame,
            "🔍 CONSULTAS SUNAT",
            "Validar RUC y consultar estado de contribuyentes",
            "#FFC107",
            self.consultas_sunat,
            1, 0
        )

        # Módulo 4: Archivos Excel
        self.crear_tarjeta_modulo(
            modules_frame,
            "📊 ARCHIVOS EXCEL",
            "Importar, exportar y generar reportes en Excel",
            "#17A2B8",
            self.archivos_excel,
            1, 1
        )

        # Módulo 5: Reportes
        self.crear_tarjeta_modulo(
            modules_frame,
            "📈 REPORTES Y ANÁLISIS",
            "Visualizar estadísticas y reportes del sistema",
            "#6F42C1",
            self.reportes,
            2, 0
        )

        # Módulo 6: Configuración
        self.crear_tarjeta_modulo(
            modules_frame,
            "⚙️ CONFIGURACIÓN",
            "Ajustes del sistema y parámetros generales",
            "#6C757D",
            self.configuracion,
            2, 1
        )

        # Footer mejorado
        footer_frame = tk.Frame(self.root, bg="#E8E8E8", height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        footer_content = tk.Frame(footer_frame, bg="#E8E8E8")
        footer_content.pack(expand=True)

        footer_text = tk.Label(
            footer_content,
            text="© 2025 JP Business Solutions | Sistema Empresarial v1.0",
            font=("Segoe UI", 9),
            bg="#E8E8E8",
            fg="#555555"
        )
        footer_text.pack(side=tk.LEFT, padx=10)

        status_label = tk.Label(
            footer_content,
            text="● Conectado",
            font=("Segoe UI", 9),
            bg="#E8E8E8",
            fg="#28A745"
        )
        status_label.pack(side=tk.RIGHT, padx=10)

    def crear_tarjeta_modulo(self, parent, titulo, descripcion, color, comando, fila, columna):
        """Crea una tarjeta visual para cada módulo"""
        # Frame de la tarjeta
        card = tk.Frame(
            parent,
            bg="white",
            relief=tk.RAISED,
            bd=0,
            highlightthickness=1,
            highlightbackground="#DDDDDD"
        )
        card.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")

        # Frame interno con padding
        inner_frame = tk.Frame(card, bg="white")
        inner_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Barra de color superior
        color_bar = tk.Frame(inner_frame, bg=color, height=4)
        color_bar.pack(fill=tk.X, pady=(0, 15))

        # Título del módulo
        titulo_label = tk.Label(
            inner_frame,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#333333"
        )
        titulo_label.pack(anchor="w")

        # Descripción
        desc_label = tk.Label(
            inner_frame,
            text=descripcion,
            font=("Segoe UI", 9),
            bg="white",
            fg="#777777",
            wraplength=220,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(5, 15))

        # Botón de acción
        btn = tk.Button(
            inner_frame,
            text="Abrir Módulo →",
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=comando,
            padx=20,
            pady=8
        )
        btn.pack(anchor="w")

        # Efecto hover
        def on_enter(e):
            card.configure(highlightbackground=color, highlightthickness=2)

        def on_leave(e):
            card.configure(highlightbackground="#DDDDDD", highlightthickness=1)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        inner_frame.bind("<Enter>", on_enter)
        inner_frame.bind("<Leave>", on_leave)

    def gestion_clientes(self):
        """Abre el módulo de gestión de clientes"""
        try:
            GestionClientes(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Gestión de Clientes:\n{str(e)}")

    def gestion_empleados(self):
        """Abre el módulo de gestión de empleados"""
        try:
            GestionEmpleados(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Gestión de Empleados:\n{str(e)}")

    def consultas_sunat(self):
        """Abre el módulo de consultas SUNAT"""
        try:
            ConsultaSUNAT(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Consultas SUNAT:\n{str(e)}")

    def archivos_excel(self):
        """Abre el módulo de archivos Excel"""
        try:
            GestionArchivosExcel(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Archivos Excel:\n{str(e)}")

    def reportes(self):
        """Abre el módulo de reportes"""
        try:
            ModuloReportes(self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir Reportes:\n{str(e)}")

    def configuracion(self):
        """Muestra el módulo de configuración"""
        messagebox.showinfo(
            "Configuración del Sistema",
            "Módulo de configuración en desarrollo.\n\n" +
            "Funcionalidades previstas:\n" +
            "- Gestión de usuarios\n" +
            "- Permisos y roles\n" +
            "- Parámetros del sistema\n" +
            "- Respaldo de base de datos"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoJP(root)
    root.mainloop()