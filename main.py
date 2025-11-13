import tkinter as tk
from tkinter import messagebox
from config_db import Database

class AplicativoJP:

    def __init__(self, root):
        self.root = root
        self.root.title("JP Business Solutions")
        self.root.geometry("1000x600")
        self.root.configure(bg="#FFFFFF")  # Fondo blanco corporativo

        try:
            Database.conectar()
            print("✓ Conectado a MySQL")
            self.crear_interfaz()
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"Error de conexión: {e}")

    def crear_interfaz(self):
        # Header con color corporativo
        header_frame = tk.Frame(self.root, bg="#0047AB", height=80)  # Azul corporativo
        header_frame.pack(fill=tk.X)
        
        # Título en el header
        titulo = tk.Label(
            header_frame, 
            text="SISTEMA DE GESTIÓN DE CLIENTES", 
            font=("Arial", 18, "bold"), 
            bg="#0047AB", 
            fg="white"
        )
        titulo.pack(pady=25)
        
        # Contenido principal
        content_frame = tk.Frame(self.root, bg="#FFFFFF")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Subtítulo descriptivo
        subtitulo = tk.Label(
            content_frame,
            text="Plataforma para la funcionalidad de clientes",
            font=("Arial", 12),
            bg="#FFFFFF",
            fg="#555555"
        )
        subtitulo.pack(pady=(0, 30))
        
        # Frame de botones con diseño más moderno
        frame_btns = tk.Frame(content_frame, bg="#FFFFFF")
        frame_btns.pack(pady=20)

        # Estilo de botones mejorado
        btn_style = {
            "width": 20,
            "height": 3,
            "bg": "#0047AB",  # Azul corporativo
            "fg": "white",
            "font": ("Arial", 12, "bold"),
            "activebackground": "#003380",  # Azul más oscuro al hacer clic
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2"  # Cambia el cursor a una mano
        }

        # Botones con algo más de espacio y sombra
        btn_clientes = tk.Button(frame_btns, text="Gestión Clientes", command=self.gestion_clientes, **btn_style)
        btn_clientes.pack(side=tk.LEFT, padx=15)
        
        btn_reportes = tk.Button(frame_btns, text="Reportes", command=self.reportes, **btn_style) 
        btn_reportes.pack(side=tk.LEFT, padx=15)
        
        # Footer con información corporativa
        footer_frame = tk.Frame(self.root, bg="#F0F0F0", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_text = tk.Label(
            footer_frame,
            text="© 2025 JP Business Solutions - Sistema Empresarial v1.0",
            font=("Arial", 9),
            bg="#F0F0F0",
            fg="#777777"
        )
        footer_text.pack(pady=12)
        
    def gestion_clientes(self):
        messagebox.showinfo("Gestión Clientes", "Aquí irá la gestión de clientes")

    def reportes(self):
        messagebox.showinfo("Reportes", "Aquí irán los reportes")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicativoJP(root)
    root.mainloop()