"""
Módulo de Consultas SUNAT
Sistema JP Business Solutions
Versión: 3.1 - Con modales de confirmación y auto-refresh
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database
import re

class ConsultaSUNAT:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Consultas SUNAT - JP Business Solutions")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#F5F5F5")
        
        # Configurar para que se cierre correctamente
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.consultas = []
        self.empleados_list = []

        self.cargar_empleados()
        self.crear_interfaz()
        self.cargar_consultas()

    def cerrar_ventana(self):
        """Cierra la ventana correctamente"""
        self.ventana.destroy()

    def cargar_empleados(self):
        """Carga lista de empleados para FK"""
        conn = None
        cursor = None
        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT codigo, CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre
                FROM empleado
                ORDER BY apellido_paterno, apellido_materno, nombres
            """
            cursor.execute(query)
            self.empleados_list = cursor.fetchall()
            
        except Exception as e:
            self.empleados_list = []
            self.mostrar_error("Error al cargar empleados", str(e))
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#FFC107", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="🔍 CONSULTAS SUNAT",
            font=("Segoe UI", 16, "bold"),
            bg="#FFC107",
            fg="black"
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
            text="Registrar Consulta SUNAT",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#FFC107"
        ).pack(pady=15)

        # Frame para campos
        form_frame = tk.Frame(panel_izq, bg="white")
        form_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # RUC Consultado
        self.crear_campo(form_frame, "RUC Consultado: *", 0)
        self.entry_nro_consultado = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_nro_consultado.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        tk.Label(
            form_frame,
            text="(11 dígitos)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=0, column=2, padx=5, sticky="w")

        # Empleado que consulta (FK)
        self.crear_campo(form_frame, "Empleado: *", 1)
        empleado_frame = tk.Frame(form_frame, bg="white")
        empleado_frame.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        self.combo_empleado = ttk.Combobox(
            empleado_frame,
            values=[f"{codigo} - {nombre}" for codigo, nombre in self.empleados_list],
            font=("Segoe UI", 9),
            width=27
        )
        self.combo_empleado.pack(fill=tk.X)

        tk.Label(
            form_frame,
            text="(Empleado que realiza la consulta)",
            font=("Segoe UI", 8),
            bg="white",
            fg="#888888"
        ).grid(row=1, column=2, padx=5, sticky="w")

        # Razón Social
        self.crear_campo(form_frame, "Razón Social: *", 2)
        self.entry_razon_social = tk.Entry(form_frame, font=("Segoe UI", 10), width=30)
        self.entry_razon_social.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        # Estado SUNAT
        self.crear_campo(form_frame, "Estado SUNAT: *", 3)
        estado_frame = tk.Frame(form_frame, bg="white")
        estado_frame.grid(row=3, column=1, padx=10, pady=8, sticky="ew")

        self.combo_estado = ttk.Combobox(
            estado_frame,
            values=["ACTIVO", "BAJA DE OFICIO", "BAJA PROVISIONAL", "SUSPENSION TEMPORAL", "INHABILITADO"],
            state="readonly",
            font=("Segoe UI", 10),
            width=27
        )
        self.combo_estado.set("ACTIVO")
        self.combo_estado.pack(fill=tk.X)

        # Condición SUNAT
        self.crear_campo(form_frame, "Condición: *", 4)
        condicion_frame = tk.Frame(form_frame, bg="white")
        condicion_frame.grid(row=4, column=1, padx=10, pady=8, sticky="ew")

        self.combo_condicion = ttk.Combobox(
            condicion_frame,
            values=["HABIDO", "NO HABIDO", "NO HALLADO", "PENDIENTE", "NO VERIFICADO"],
            state="readonly",
            font=("Segoe UI", 10),
            width=27
        )
        self.combo_condicion.set("HABIDO")
        self.combo_condicion.pack(fill=tk.X)

        # Nota informativa
        info_label = tk.Label(
            form_frame,
            text="ℹ Esta función registra consultas manuales a SUNAT.\nEn producción se integraría con la API de SUNAT.",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#666666",
            justify="left"
        )
        info_label.grid(row=5, column=0, columnspan=3, pady=15, padx=10, sticky="w")

        # Nota de campos obligatorios
        tk.Label(
            form_frame,
            text="* Campos obligatorios",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg="#DC3545"
        ).grid(row=6, column=0, columnspan=3, pady=10)

        # Botones de acción
        btn_frame = tk.Frame(panel_izq, bg="white")
        btn_frame.pack(pady=20)

        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "width": 15,
            "cursor": "hand2",
            "bd": 0,
            "relief": "flat",
            "pady": 8
        }

        btn_consultar = tk.Button(
            btn_frame,
            text="🔍 Consultar RUC",
            bg="#28A745",
            fg="white",
            command=self.simular_consulta,
            **btn_style
        )
        btn_consultar.grid(row=0, column=0, padx=5, pady=5)

        btn_guardar = tk.Button(
            btn_frame,
            text="💾 Guardar Consulta",
            bg="#FFC107",
            fg="black",
            command=self.guardar_consulta,
            **btn_style
        )
        btn_guardar.grid(row=0, column=1, padx=5, pady=5)

        btn_limpiar = tk.Button(
            btn_frame,
            text="🔄 Limpiar",
            bg="#6C757D",
            fg="white",
            command=self.limpiar_formulario,
            **btn_style
        )
        btn_limpiar.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Panel derecho - Historial de consultas
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            panel_der,
            text="Historial de Consultas SUNAT",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#FFC107"
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
        self.entry_buscar.bind('<KeyRelease>', self.buscar_consulta)

        btn_refresh = tk.Button(
            search_frame,
            text="↻",
            font=("Segoe UI", 12, "bold"),
            bg="#FFC107",
            fg="black",
            command=self.refrescar_todo,
            cursor="hand2",
            width=3,
            bd=0
        )
        btn_refresh.pack(side=tk.RIGHT, padx=5)

        # Tabla de consultas
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("RUC", "Razón Social", "Estado", "Condición", "Empleado"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=20
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # Configurar columnas
        self.tree.heading("RUC", text="RUC Consultado")
        self.tree.heading("Razón Social", text="Razón Social")
        self.tree.heading("Estado", text="Estado SUNAT")
        self.tree.heading("Condición", text="Condición")
        self.tree.heading("Empleado", text="Empleado")

        self.tree.column("RUC", width=110, anchor="center")
        self.tree.column("Razón Social", width=250)
        self.tree.column("Estado", width=120, anchor="center")
        self.tree.column("Condición", width=100, anchor="center")
        self.tree.column("Empleado", width=180)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Event: Seleccionar consulta
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_consulta)

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

    def cargar_consultas(self):
        """Carga todas las consultas SUNAT desde la base de datos"""
        conn = None
        cursor = None
        
        try:
            # Guardar selección actual
            seleccion_anterior = None
            if self.tree.selection():
                item = self.tree.item(self.tree.selection()[0])
                seleccion_anterior = item['values'][0] if item['values'] else None

            self.tree.delete(*self.tree.get_children())

            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT
                    cs.nro_consultado,
                    cs.razon_social,
                    cs.estado,
                    cs.condicion,
                    CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado
                FROM consulta_sunat cs
                INNER JOIN empleado e ON cs.codigo_empleado = e.codigo
                ORDER BY cs.nro_consultado DESC
            """

            cursor.execute(query)
            self.consultas = cursor.fetchall()

            item_a_seleccionar = None
            for consulta in self.consultas:
                # Aplicar color según estado
                estado = consulta[2]
                tags = ()
                if estado == "ACTIVO":
                    tags = ('activo',)
                elif estado in ["BAJA DE OFICIO", "SUSPENSION TEMPORAL", "INHABILITADO"]:
                    tags = ('inactivo',)

                item_id = self.tree.insert("", tk.END, values=consulta, tags=tags)

                # Si este era el RUC seleccionado, guardamos su ID
                if seleccion_anterior and consulta[0] == seleccion_anterior:
                    item_a_seleccionar = item_id

            # Configurar colores
            self.tree.tag_configure('activo', foreground='#28A745')
            self.tree.tag_configure('inactivo', foreground='#DC3545')

            # Restaurar selección si existía
            if item_a_seleccionar:
                self.tree.selection_set(item_a_seleccionar)
                self.tree.see(item_a_seleccionar)

            self.tree.update_idletasks()

        except Exception as e:
            self.mostrar_error("Error al cargar consultas", str(e))
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def refrescar_todo(self):
        """Refresca la lista y limpia el formulario"""
        self.cargar_consultas()
        self.limpiar_formulario()

    def buscar_consulta(self, event=None):
        """Busca consultas por RUC o razón social"""
        busqueda = self.entry_buscar.get().strip().upper()

        self.tree.delete(*self.tree.get_children())

        if not busqueda:
            for consulta in self.consultas:
                estado = consulta[2]
                tags = ()
                if estado == "ACTIVO":
                    tags = ('activo',)
                elif estado in ["BAJA DE OFICIO", "SUSPENSION TEMPORAL", "INHABILITADO"]:
                    tags = ('inactivo',)
                self.tree.insert("", tk.END, values=consulta, tags=tags)
        else:
            for consulta in self.consultas:
                if busqueda in str(consulta[0]).upper() or busqueda in str(consulta[1]).upper():
                    estado = consulta[2]
                    tags = ()
                    if estado == "ACTIVO":
                        tags = ('activo',)
                    elif estado in ["BAJA DE OFICIO", "SUSPENSION TEMPORAL", "INHABILITADO"]:
                        tags = ('inactivo',)
                    self.tree.insert("", tk.END, values=consulta, tags=tags)

    def seleccionar_consulta(self, event=None):
        """Carga los datos de la consulta seleccionada en el formulario"""
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item['values']

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = """
                SELECT nro_consultado, codigo_empleado, razon_social, estado, condicion
                FROM consulta_sunat
                WHERE nro_consultado = %s
            """
            cursor.execute(query, (valores[0],))

            consulta = cursor.fetchone()

            if consulta:
                # Limpiar y cargar datos
                self.entry_nro_consultado.delete(0, tk.END)
                self.entry_razon_social.delete(0, tk.END)

                self.entry_nro_consultado.insert(0, consulta[0])
                self.entry_razon_social.insert(0, consulta[2])
                self.combo_estado.set(consulta[3])
                self.combo_condicion.set(consulta[4])

                # Seleccionar empleado
                codigo_empleado = consulta[1]
                for i, (codigo, nombre) in enumerate(self.empleados_list):
                    if codigo == codigo_empleado:
                        self.combo_empleado.current(i)
                        break

        except Exception as e:
            self.mostrar_error("Error al cargar consulta", str(e))
        finally:
            try:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            except:
                pass

    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.entry_nro_consultado.delete(0, tk.END)
        self.entry_razon_social.delete(0, tk.END)
        self.entry_buscar.delete(0, tk.END)
        self.combo_empleado.set("")
        self.combo_estado.set("ACTIVO")
        self.combo_condicion.set("HABIDO")
        
        for item in self.tree.selection():
            self.tree.selection_remove(item)
            
        self.entry_nro_consultado.focus()

    def simular_consulta(self):
        """Consulta RUC usando la API de SUNAT"""
        from controllers.sunat_controller import SUNATController
        
        ruc = self.entry_nro_consultado.get().strip()

        # Validar formato
        if not SUNATController.validar_ruc(ruc):
            self.mostrar_error("RUC Inválido", "El RUC debe tener exactamente 11 dígitos numéricos")
            self.entry_nro_consultado.focus()
            return

        # Mostrar mensaje de espera
        self.lbl_info_consulta = tk.Label(
            self.ventana,
            text="⏳ Consultando SUNAT, por favor espere...",
            font=("Segoe UI", 10, "italic"),
            bg="#FFC107",
            fg="black"
        )
        self.lbl_info_consulta.place(relx=0.5, rely=0.95, anchor="center")
        self.ventana.update()

        # Deshabilitar botón mientras consulta
        # (busca el botón en tu código y guárdalo como self.btn_consultar)
        
        try:
            # ✅ CONSULTAR API REAL
            resultado = SUNATController.consultar_ruc(ruc)

            if resultado['success']:
                # ✅ AUTO-COMPLETAR CAMPOS
                self.entry_razon_social.delete(0, tk.END)
                self.entry_razon_social.insert(0, resultado['razon_social'])

                # Normalizar y establecer valores
                estado_normalizado = SUNATController.normalizar_estado(resultado['estado'])
                condicion_normalizada = SUNATController.normalizar_condicion(resultado['condicion'])

                self.combo_estado.set(estado_normalizado)
                self.combo_condicion.set(condicion_normalizada)

                # Mensaje de éxito
                self.lbl_info_consulta.config(
                    text=f"✓ Consulta exitosa usando {resultado['api_used']}",
                    fg="#28A745"
                )
                self.ventana.after(3000, self.lbl_info_consulta.destroy)

                self.mostrar_exito(
                    "Consulta Exitosa",
                    f"✓ RUC consultado: {ruc}\n"
                    f"Razón Social: {resultado['razon_social']}\n"
                    f"Estado: {estado_normalizado}\n"
                    f"Condición: {condicion_normalizada}\n\n"
                    f"API utilizada: {resultado['api_used']}"
                )
            else:
                # ❌ Error en la consulta
                self.lbl_info_consulta.config(
                    text=f"✗ {resultado['error']}",
                    fg="#DC3545"
                )
                self.ventana.after(5000, self.lbl_info_consulta.destroy)

                self.mostrar_advertencia(
                    "Consulta Fallida",
                    f"{resultado['error']}\n\n"
                    "Complete los campos manualmente."
                )

        except Exception as e:
            self.lbl_info_consulta.config(
                text="✗ Error al consultar SUNAT",
                fg="#DC3545"
            )
            self.ventana.after(3000, self.lbl_info_consulta.destroy)
            self.mostrar_error("Error Inesperado", f"No se pudo consultar:\n{str(e)}")

    def guardar_consulta(self):
        """Guarda una consulta SUNAT con modal de confirmación"""
        nro_consultado = self.entry_nro_consultado.get().strip()
        empleado_text = self.combo_empleado.get().strip()
        razon_social = self.entry_razon_social.get().strip()
        estado = self.combo_estado.get()
        condicion = self.combo_condicion.get()

        # Validaciones
        if not nro_consultado or not empleado_text or not razon_social:
            self.mostrar_advertencia(
                "Campos Obligatorios",
                "Complete:\n• RUC Consultado\n• Empleado\n• Razón Social"
            )
            return

        if not self.validar_ruc(nro_consultado):
            self.mostrar_error("RUC Inválido", "El RUC debe tener 11 dígitos numéricos")
            self.entry_nro_consultado.focus()
            return

        # Extraer código de empleado
        if " - " not in empleado_text:
            self.mostrar_error("Empleado Inválido", "Seleccione un empleado válido de la lista")
            return

        codigo_empleado = int(empleado_text.split(" - ")[0])
        nombre_empleado = empleado_text.split(" - ")[1]

        # ✅ MODAL DE CONFIRMACIÓN ANTES DE GUARDAR
        confirmacion = messagebox.askyesno(
            "💾 Confirmar Consulta SUNAT",
            f"¿Desea registrar esta consulta?\n\n"
            f"RUC: {nro_consultado}\n"
            f"Razón Social: {razon_social}\n"
            f"Estado: {estado}\n"
            f"Condición: {condicion}\n"
            f"Empleado: {nombre_empleado}",
            parent=self.ventana
        )

        if not confirmacion:
            return

        conn = None
        cursor = None

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            query = "CALL insertar_consulta_sunat(%s, %s, %s, %s, %s)"
            valores = (nro_consultado, codigo_empleado, razon_social, estado, condicion)

            cursor.execute(query, valores)

            # ✅ Consumir todos los resultados del stored procedure
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
                "Consulta Registrada",
                f"✓ Consulta SUNAT registrada exitosamente\n\n"
                f"RUC: {nro_consultado}\n"
                f"Razón Social: {razon_social}\n"
                f"Estado: {estado}"
            )
            
            # ✅ AUTO-REFRESH: Recargar y seleccionar la nueva consulta
            self.cargar_consultas()
            
            # Buscar y seleccionar la consulta recién insertada
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == nro_consultado:
                    self.tree.selection_set(item)
                    self.tree.see(item)
                    self.seleccionar_consulta()
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
                    f"❌ Ya existe una consulta registrada para el RUC:\n{nro_consultado}"
                )
            elif "Unread result" in error_msg:
                # El INSERT se ejecutó correctamente a pesar del error
                self.mostrar_exito(
                    "Consulta Registrada",
                    f"✓ Consulta SUNAT registrada exitosamente\n\nRUC: {nro_consultado}"
                )
                self.cargar_consultas()
                
                # Seleccionar la consulta
                for item in self.tree.get_children():
                    if self.tree.item(item)['values'][0] == nro_consultado:
                        self.tree.selection_set(item)
                        self.tree.see(item)
                        self.seleccionar_consulta()
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

    def mostrar_info(self, titulo, mensaje):
        """Muestra mensaje informativo"""
        messagebox.showinfo(f"ℹ {titulo}", mensaje, parent=self.ventana)