"""
Módulo de Clientes
Sistema Gestion De Clientes
Versión: 3.0 - Optimizado con mejores prácticas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
from models.sesion import SesionUsuario
import re

class GestionClientes:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gestión de Clientes")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#F5F5F5")
        
        # Configurar para que se cierre correctamente
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        # Variables
        self.clientes = []
        self.ruc_seleccionado = None

        self.crear_interfaz()
        self.cargar_clientes()

    def cerrar_ventana(self):
        """Cierra la ventana correctamente"""
        self.ventana.destroy()

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
            "relief": "flat",
            "pady": 8
        }

        btn_nuevo = tk.Button(
            btn_frame,
            text="✚ Nuevo",
            bg="#28A745",
            fg="white",
            command=self.nuevo_cliente,
            **btn_style
        )
        btn_nuevo.grid(row=0, column=0, padx=5, pady=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="💾 Guardar",
            bg="#0047AB",
            fg="white",
            command=self.guardar_cliente,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5, pady=5)

        btn_actualizar = tk.Button(
            btn_frame,
            text="🔄 Actualizar",
            bg="#FFC107",
            fg="black",
            command=self.actualizar_cliente,
            **btn_style
        )
        btn_actualizar.grid(row=1, column=0, padx=5, pady=5)

        btn_eliminar = tk.Button(
            btn_frame,
            text="🗑️ Eliminar",
            bg="#DC3545",
            fg="white",
            command=self.eliminar_cliente,
            **btn_style
        )
        btn_eliminar.grid(row=1, column=1, padx=5, pady=5)

        # Deshabilitar eliminar si no es administrador
        if not SesionUsuario.puede_eliminar():
            btn_eliminar.config(
                state='disabled',
                bg="#CCCCCC",
                fg="#666666",
                cursor="arrow"
            )
            # Tooltip al pasar el mouse
            self.crear_tooltip(btn_eliminar, "⚠️ Solo Administradores pueden eliminar")

        # Botón de navegación - Volver al menú
        btn_volver = tk.Button(
            btn_frame,
            text="← Volver al Menú Principal",
            bg="#6C757D",
            fg="white",
            command=self.cerrar_ventana,
            font=("Segoe UI", 9, "bold"),
            width=26,
            cursor="hand2",
            bd=0,
            relief="flat",
            pady=8
        )
        btn_volver.grid(row=2, column=0, columnspan=2, padx=5, pady=(15, 5), sticky="ew")

        # Panel derecho - Lista de clientes
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
            text="🔍 Buscar:",
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
            command=self.refrescar_todo,
            cursor="hand2",
            width=3,
            bd=0
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de clientes
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

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
        """Valida que el RUC tenga 11 dígitos numéricos"""
        if not ruc:
            return False
        return bool(re.match(r'^\d{11}$', ruc))

    def validar_telefono(self, telefono):
        """Valida que el teléfono tenga 9 dígitos numéricos"""
        if not telefono:
            return True  # Teléfono es opcional
        return bool(re.match(r'^\d{9}$', telefono))

    def validar_correo(self, correo):
        """Valida formato básico de correo electrónico"""
        if not correo:
            return True  # Correo es opcional
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, correo))

    def validar_campos_obligatorios(self, ruc, nombres, ap_paterno, ap_materno):
        """Valida que los campos obligatorios no estén vacíos"""
        if not ruc or not nombres or not ap_paterno or not ap_materno:
            return False
        if not ruc.strip() or not nombres.strip() or not ap_paterno.strip() or not ap_materno.strip():
            return False
        return True

    def cargar_clientes(self):
        """Carga todos los clientes desde la base de datos"""
        try:
            # Guardar selección actual
            seleccion_anterior = None
            if self.tree.selection():
                item = self.tree.item(self.tree.selection()[0])
                seleccion_anterior = item['values'][0] if item['values'] else None

            # Limpiar tabla
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

            # Insertar clientes en la tabla
            item_a_seleccionar = None
            for cliente in self.clientes:
                item_id = self.tree.insert("", tk.END, values=cliente)
                if seleccion_anterior and cliente[0] == seleccion_anterior:
                    item_a_seleccionar = item_id

            cursor.close()

            # Restaurar selección si existía
            if item_a_seleccionar:
                self.tree.selection_set(item_a_seleccionar)
                self.tree.see(item_a_seleccionar)

            self.tree.update_idletasks()

        except Exception as e:
            self.mostrar_error("Error al cargar clientes", str(e))

    def refrescar_todo(self):
        """Refresca la lista y limpia el formulario"""
        self.cargar_clientes()
        self.nuevo_cliente()

    def buscar_cliente(self, event=None):
        """Busca clientes por RUC o nombre"""
        busqueda = self.entry_buscar.get().strip().upper()

        self.tree.delete(*self.tree.get_children())

        if not busqueda:
            for cliente in self.clientes:
                self.tree.insert("", tk.END, values=cliente)
        else:
            for cliente in self.clientes:
                ruc_str = str(cliente[0]).upper()
                nombre_str = str(cliente[1]).upper()
                if busqueda in ruc_str or busqueda in nombre_str:
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

                # Habilitar RUC temporalmente
                self.entry_ruc.config(state='normal')

                # Limpiar y cargar datos
                self.entry_ruc.delete(0, tk.END)
                self.entry_nombres.delete(0, tk.END)
                self.entry_ap_paterno.delete(0, tk.END)
                self.entry_ap_materno.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_pagina_web.delete(0, tk.END)
                self.entry_telefono.delete(0, tk.END)

                self.entry_ruc.insert(0, cliente[0])
                self.entry_nombres.insert(0, cliente[1])
                self.entry_ap_paterno.insert(0, cliente[2])
                self.entry_ap_materno.insert(0, cliente[3])
                self.entry_correo.insert(0, cliente[4] if cliente[4] else "")
                self.entry_pagina_web.insert(0, cliente[5] if cliente[5] else "")
                self.entry_telefono.insert(0, cliente[6] if cliente[6] else "")

                # Deshabilitar RUC (PK)
                self.entry_ruc.config(state='disabled')

        except Exception as e:
            self.mostrar_error("Error al cargar cliente", str(e))

    def nuevo_cliente(self):
        """Limpia el formulario para un nuevo cliente"""
        self.ruc_seleccionado = None

        self.entry_ruc.config(state='normal')

        self.entry_ruc.delete(0, tk.END)
        self.entry_nombres.delete(0, tk.END)
        self.entry_ap_paterno.delete(0, tk.END)
        self.entry_ap_materno.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_pagina_web.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_buscar.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.entry_ruc.focus()

    def guardar_cliente(self):
        """Guarda un nuevo cliente con validaciones completas"""
        ruc = self.entry_ruc.get().strip()
        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()
        correo = self.entry_correo.get().strip()
        pagina_web = self.entry_pagina_web.get().strip()
        telefono = self.entry_telefono.get().strip()

        # Validaciones
        if not self.validar_campos_obligatorios(ruc, nombres, ap_paterno, ap_materno):
            self.mostrar_advertencia(
                "Campos Obligatorios",
                "Complete los campos:\n• RUC\n• Nombres\n• Apellido Paterno\n• Apellido Materno"
            )
            return

        if not self.validar_ruc(ruc):
            self.mostrar_error("RUC Inválido", "El RUC debe contener 11 dígitos numéricos")
            self.entry_ruc.focus()
            return

        if telefono and not self.validar_telefono(telefono):
            self.mostrar_error("Teléfono Inválido", "El teléfono debe contener 9 dígitos numéricos")
            self.entry_telefono.focus()
            return

        if correo and not self.validar_correo(correo):
            self.mostrar_error("Correo Inválido", "Formato inválido. Ej: usuario@dominio.com")
            self.entry_correo.focus()
            return

        # ✅ MODAL DE CONFIRMACIÓN ANTES DE GUARDAR
        confirmacion = messagebox.askyesno(
            "💾 Confirmar Registro",
            f"¿Desea registrar este cliente?\n\n"
            f"RUC: {ruc}\n"
            f"Nombre: {nombres} {ap_paterno} {ap_materno}\n"
            f"Correo: {correo if correo else 'No especificado'}\n"
            f"Teléfono: {telefono if telefono else 'No especificado'}",
            parent=self.ventana
        )

        if not confirmacion:
            return

        conn = None
        cursor = None
        
        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL insertar_cliente(%s, %s, %s, %s, %s, %s, %s)"
            valores = (
                ruc, nombres, ap_paterno, ap_materno,
                correo if correo else None,
                pagina_web if pagina_web else None,
                telefono if telefono else None
            )

            cursor.execute(query, valores)
            
            # ✅ Consumir todos los resultados
            for result in cursor.stored_results():
                result.fetchall()
            
            # ✅ Consumir con nextset()
            while True:
                try:
                    if not cursor.nextset():
                        break
                except:
                    break
            
            conn.commit()

            # ✅ MODAL DE ÉXITO
            self.mostrar_exito(
                "Cliente Registrado",
                f"✓ Cliente guardado exitosamente\n\n"
                f"RUC: {ruc}\n"
                f"Nombre: {nombres} {ap_paterno} {ap_materno}"
            )
            
            # ✅ AUTO-REFRESH: Recargar y seleccionar el nuevo cliente
            self.cargar_clientes()
            
            # Buscar y seleccionar el cliente recién insertado
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == ruc:
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    self.seleccionar_cliente()
                    break

        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            
            error_msg = str(e)
            if "Duplicate entry" in error_msg:
                self.mostrar_error(
                    "RUC Duplicado",
                    f"❌ Ya existe un cliente registrado con el RUC:\n{ruc}\n\n"
                    f"Por favor, verifique el número de RUC."
                )
            elif "Unread result" in error_msg:
                # El INSERT se ejecutó correctamente a pesar del error
                self.mostrar_exito(
                    "Cliente Registrado",
                    f"✓ Cliente guardado exitosamente\n\n"
                    f"RUC: {ruc}\n"
                    f"Nombre: {nombres} {ap_paterno} {ap_materno}"
                )
                self.cargar_clientes()
                
                # Seleccionar el cliente
                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == ruc:
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        self.seleccionar_cliente()
                        break
            else:
                self.mostrar_error("Error al Guardar", f"❌ {error_msg}")
        
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass


    def actualizar_cliente(self):
        """Actualiza un cliente existente"""
        if not self.ruc_seleccionado:
            self.mostrar_advertencia("Sin Selección", "Seleccione un cliente para actualizar")
            return

        nombres = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()
        correo = self.entry_correo.get().strip()
        pagina_web = self.entry_pagina_web.get().strip()
        telefono = self.entry_telefono.get().strip()

        if not nombres or not ap_paterno or not ap_materno:
            self.mostrar_advertencia("Campos Obligatorios", "Complete: Nombres, Apellidos")
            return

        if telefono and not self.validar_telefono(telefono):
            self.mostrar_error("Teléfono Inválido", "Debe contener 9 dígitos")
            return

        if correo and not self.validar_correo(correo):
            self.mostrar_error("Correo Inválido", "Formato inválido")
            return

        # ✅ MODAL DE CONFIRMACIÓN ANTES DE ACTUALIZAR
        confirmacion = messagebox.askyesno(
            "🔄 Confirmar Actualización",
            f"¿Desea actualizar los datos de este cliente?\n\n"
            f"RUC: {self.ruc_seleccionado}\n"
            f"Nuevo nombre: {nombres} {ap_paterno} {ap_materno}\n"
            f"Correo: {correo if correo else 'No especificado'}\n"
            f"Teléfono: {telefono if telefono else 'No especificado'}",
            parent=self.ventana
        )

        if not confirmacion:
            return

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL actualizar_cliente(%s, %s, %s, %s, %s, %s, %s)"
            valores = (
                self.ruc_seleccionado, nombres, ap_paterno, ap_materno,
                correo if correo else None,
                pagina_web if pagina_web else None,
                telefono if telefono else None
            )

            cursor.execute(query, valores)
            
            # ✅ Consumir todos los resultados
            for result in cursor.stored_results():
                result.fetchall()
            
            while True:
                try:
                    if not cursor.nextset():
                        break
                except:
                    break
            
            conn.commit()

            # ✅ MODAL DE ÉXITO
            self.mostrar_exito(
                "Cliente Actualizado",
                f"✓ Datos actualizados exitosamente\n\n"
                f"RUC: {self.ruc_seleccionado}\n"
                f"Nombre: {nombres} {ap_paterno} {ap_materno}"
            )
            
            # ✅ AUTO-REFRESH: Recargar y mantener selección
            self.cargar_clientes()

        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            
            self.mostrar_error("Error al Actualizar", f"❌ {str(e)}")
        
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def eliminar_cliente(self):
        """Elimina un cliente con confirmación"""
        if not self.ruc_seleccionado:
            self.mostrar_advertencia("Sin Selección", "Seleccione un cliente para eliminar")
            return

        nombre_completo = f"{self.entry_nombres.get()} {self.entry_ap_paterno.get()} {self.entry_ap_materno.get()}"

        confirmacion = messagebox.askyesno(
            "⚠ Confirmar Eliminación",
            f"¿Eliminar cliente?\n\nRUC: {self.ruc_seleccionado}\nNombre: {nombre_completo}\n\nEsta acción no se puede deshacer.",
            parent=self.ventana
        )

        if not confirmacion:
            return

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL eliminar_cliente(%s)"
            cursor.execute(query, (self.ruc_seleccionado,))
            
            # ✅ CRÍTICO: Consumir todos los resultados
            for result in cursor.stored_results():
                result.fetchall()
            
            conn.commit()
            cursor.close()
            conn.close()

            self.mostrar_exito("Cliente Eliminado", "Cliente eliminado correctamente")
            self.cargar_clientes()
            self.nuevo_cliente()

        except Exception as e:
            if "foreign key constraint" in str(e).lower():
                self.mostrar_error(
                    "No se puede eliminar",
                    "Este cliente tiene empleados asignados.\nPrimero elimine o reasigne los empleados."
                )
            else:
                self.mostrar_error("Error al Eliminar", str(e))

    # Métodos de mensajes modales
    def mostrar_exito(self, titulo, mensaje):
        """Muestra mensaje de éxito"""
        messagebox.showinfo(f"✓ {titulo}", mensaje, parent=self.ventana)

    def mostrar_error(self, titulo, mensaje):
        """Muestra mensaje de error"""
        messagebox.showerror(f"✗ {titulo}", mensaje, parent=self.ventana)

    def mostrar_advertencia(self, titulo, mensaje):
        """Muestra mensaje de advertencia"""
        messagebox.showwarning(f"⚠ {titulo}", mensaje, parent=self.ventana)

    def crear_tooltip(self, widget, texto):
        """Crea un tooltip para un widget"""
        def mostrar_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(
                tooltip,
                text=texto,
                background="#FFE4B5",
                relief=tk.SOLID,
                borderwidth=1,
                font=("Segoe UI", 9)
            )
            label.pack()
            widget.tooltip = tooltip

        def ocultar_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')

        widget.bind('<Enter>', mostrar_tooltip)
        widget.bind('<Leave>', ocultar_tooltip)
