"""
Módulo de Login
Sistema de Gestión Empresarial
Ventana de autenticación de usuarios
"""

import tkinter as tk
from tkinter import messagebox
from models.config_db import Database
from models.sesion import SesionUsuario

class VentanaLogin:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.login_exitoso = False

        # Configurar ventana
        self.root.title("Iniciar Sesión - Sistema de Gestión")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F5F5")

        # Centrar ventana
        self.centrar_ventana()

        # Crear interfaz
        self.crear_interfaz()

        # Bind Enter para login
        self.root.bind('<Return>', lambda e: self.iniciar_sesion())

        # Cerrar aplicación si se cierra login
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = 500
        alto = 650
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

    def crear_interfaz(self):
        """Crea la interfaz de login"""
        # Header con logo
        header_frame = tk.Frame(self.root, bg="#0047AB", height=150)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Logo/Icono
        logo_label = tk.Label(
            header_frame,
            text="🏢",
            font=("Segoe UI", 64),
            bg="#0047AB",
            fg="white"
        )
        logo_label.pack(pady=(20, 5))

        # Título
        titulo_label = tk.Label(
            header_frame,
            text="Gestión De Clientes",
            font=("Segoe UI", 18, "bold"),
            bg="#0047AB",
            fg="white"
        )
        titulo_label.pack()

        subtitulo_label = tk.Label(
            header_frame,
            text="Inicio de Sesión",
            font=("Segoe UI", 11),
            bg="#0047AB",
            fg="#B8D4FF"
        )
        subtitulo_label.pack(pady=(5, 15))

        # Contenedor principal
        main_container = tk.Frame(self.root, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Card de login
        login_card = tk.Frame(main_container, bg="white", relief=tk.FLAT, bd=0)
        login_card.pack(fill=tk.BOTH, expand=True)

        # Padding interno
        form_frame = tk.Frame(login_card, bg="white")
        form_frame.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)

        # Título del formulario
        form_titulo = tk.Label(
            form_frame,
            text="Acceder al Sistema",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        form_titulo.pack(pady=(0, 20))

        # Usuario
        user_label = tk.Label(
            form_frame,
            text="Usuario:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#555555",
            anchor="w"
        )
        user_label.pack(fill=tk.X, pady=(10, 5))

        self.entry_usuario = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground="#CCCCCC",
            highlightcolor="#0047AB"
        )
        self.entry_usuario.pack(fill=tk.X, ipady=8)
        self.entry_usuario.focus()

        # Contraseña
        pass_label = tk.Label(
            form_frame,
            text="Contraseña:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#555555",
            anchor="w"
        )
        pass_label.pack(fill=tk.X, pady=(20, 5))

        self.entry_password = tk.Entry(
            form_frame,
            font=("Segoe UI", 12),
            show="●",
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground="#CCCCCC",
            highlightcolor="#0047AB"
        )
        self.entry_password.pack(fill=tk.X, ipady=8)

        # Botón de login
        btn_login = tk.Button(
            form_frame,
            text="Iniciar Sesión",
            font=("Segoe UI", 12, "bold"),
            bg="#0047AB",
            fg="white",
            activebackground="#003580",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.iniciar_sesion
        )
        btn_login.pack(fill=tk.X, pady=(30, 10), ipady=12)

        # Información de usuarios
        info_frame = tk.Frame(form_frame, bg="#F0F8FF", relief=tk.SOLID, bd=1)
        info_frame.pack(fill=tk.X, pady=(20, 0))

        info_label = tk.Label(
            info_frame,
            text="ℹ️ Usuarios de Prueba",
            font=("Segoe UI", 9, "bold"),
            bg="#F0F8FF",
            fg="#0047AB"
        )
        info_label.pack(anchor="w", padx=10, pady=(10, 5))

        usuarios_text = tk.Label(
            info_frame,
            text="• Admin: admin / admin123\n• Contabilidad: contabilidad / conta123",
            font=("Segoe UI", 9),
            bg="#F0F8FF",
            fg="#555555",
            justify="left"
        )
        usuarios_text.pack(anchor="w", padx=10, pady=(0, 10))

        # Footer
        footer_label = tk.Label(
            self.root,
            text="© 2025 Sistema de Gestión Empresarial",
            font=("Segoe UI", 8),
            bg="#F5F5F5",
            fg="#999999"
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def iniciar_sesion(self):
        """Valida credenciales e inicia sesión"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        # Validar campos vacíos
        if not usuario or not password:
            messagebox.showwarning(
                "Campos Requeridos",
                "Por favor ingrese usuario y contraseña",
                parent=self.root
            )
            return

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor(dictionary=True)

            # Buscar usuario
            query = """
                SELECT id, usuario, password, rol, nombre_completo, email, activo
                FROM usuarios
                WHERE usuario = %s AND activo = TRUE
            """
            cursor.execute(query, (usuario,))
            usuario_data = cursor.fetchone()

            if not usuario_data:
                # Registrar intento fallido
                messagebox.showerror(
                    "Error de Autenticación",
                    "Usuario no encontrado o inactivo",
                    parent=self.root
                )
                self.entry_password.delete(0, tk.END)
                return

            # Verificar contraseña (en texto plano por simplicidad)
            if usuario_data['password'] != password:
                # Registrar intento fallido
                cursor.execute(
                    "CALL registrar_acceso(%s, %s, 'LOGIN_FALLIDO', FALSE, 'Contraseña incorrecta')",
                    (usuario_data['id'], usuario)
                )
                conn.commit()

                messagebox.showerror(
                    "Error de Autenticación",
                    "Contraseña incorrecta",
                    parent=self.root
                )
                self.entry_password.delete(0, tk.END)
                return

            # Login exitoso
            # Iniciar sesión en el sistema
            SesionUsuario.iniciar_sesion({
                'id': usuario_data['id'],
                'usuario': usuario_data['usuario'],
                'rol': usuario_data['rol'],
                'nombre_completo': usuario_data['nombre_completo'],
                'email': usuario_data['email']
            })

            # Registrar acceso exitoso
            cursor.execute(
                "CALL registrar_acceso(%s, %s, 'LOGIN_EXITOSO', TRUE, 'Acceso al sistema')",
                (usuario_data['id'], usuario)
            )
            conn.commit()

            # Marcar como exitoso
            self.login_exitoso = True

            # Mostrar mensaje de bienvenida
            messagebox.showinfo(
                "Bienvenido",
                f"¡Bienvenido {usuario_data['nombre_completo']}!\n\nRol: {usuario_data['rol']}",
                parent=self.root
            )

            # Cerrar ventana de login
            self.root.destroy()

            # Callback para mostrar menú principal
            if self.on_login_success:
                self.on_login_success()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al conectar con la base de datos:\n{str(e)}",
                parent=self.root
            )
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def cerrar_aplicacion(self):
        """Cierra la aplicación si se cancela el login"""
        if not self.login_exitoso:
            respuesta = messagebox.askyesno(
                "Salir",
                "¿Está seguro que desea salir?",
                parent=self.root
            )
            if respuesta:
                self.root.quit()
