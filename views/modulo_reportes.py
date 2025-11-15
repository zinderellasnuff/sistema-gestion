"""
Módulo de Reportes y Análisis
Sistema JP Business Solutions
Versión: 2.0 - Adaptado a estructura real de BD
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.config_db import Database

class ModuloReportes:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Reportes y Análisis - JP Business Solutions")
        self.ventana.geometry("1400x800")
        self.ventana.configure(bg="#F5F5F5")

        # Diccionario de reportes con sus consultas SQL
        self.reportes = {
            0: {
                "nombre": "CONSULTA 1: Listado completo de clientes",
                "descripcion": "Muestra todos los clientes ordenados por apellido",
                "query": """
                    SELECT
                        ruc,
                        CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
                        correo_electronico,
                        pagina_web,
                        telefono
                    FROM cliente
                    ORDER BY apellido_paterno, apellido_materno, nombres
                """,
                "columnas": ["RUC", "Nombre Completo", "Correo Electrónico", "Página Web", "Teléfono"]
            },
            1: {
                "nombre": "CONSULTA 2: Clientes con información completa",
                "descripcion": "Clientes que tienen todos los datos de contacto",
                "query": """
                    SELECT
                        ruc,
                        CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
                        correo_electronico,
                        telefono,
                        pagina_web
                    FROM cliente
                    WHERE correo_electronico IS NOT NULL
                      AND telefono IS NOT NULL
                      AND pagina_web IS NOT NULL
                    ORDER BY apellido_paterno
                """,
                "columnas": ["RUC", "Nombre Completo", "Correo Electrónico", "Teléfono", "Página Web"]
            },
            2: {
                "nombre": "CONSULTA 3: Clientes con información incompleta",
                "descripcion": "Clientes con datos de contacto faltantes",
                "query": """
                    SELECT
                        ruc,
                        CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
                        CASE
                            WHEN correo_electronico IS NULL THEN 'Falta correo'
                            WHEN pagina_web IS NULL THEN 'Falta página web'
                            ELSE 'Datos incompletos'
                        END AS dato_faltante,
                        correo_electronico,
                        telefono,
                        pagina_web
                    FROM cliente
                    WHERE correo_electronico IS NULL OR pagina_web IS NULL
                    ORDER BY apellido_paterno
                """,
                "columnas": ["RUC", "Nombre Completo", "Dato Faltante", "Correo", "Teléfono", "Página Web"]
            },
            3: {
                "nombre": "CONSULTA 4: Búsqueda flexible de clientes",
                "descripcion": "Clientes con letra 'a' en nombre o apellidos",
                "query": """
                    SELECT
                        ruc,
                        CONCAT(nombres, ' ', apellido_paterno, ' ', apellido_materno) AS nombre_completo,
                        correo_electronico,
                        telefono,
                        pagina_web
                    FROM cliente
                    WHERE nombres LIKE '%a%'
                       OR apellido_paterno LIKE '%a%'
                       OR apellido_materno LIKE '%a%'
                    ORDER BY apellido_paterno
                """,
                "columnas": ["RUC", "Nombre Completo", "Correo Electrónico", "Teléfono", "Página Web"]
            },
            4: {
                "nombre": "CONSULTA 5: Conteo de clientes por apellido paterno",
                "descripcion": "Agrupa clientes por apellido paterno",
                "query": """
                    SELECT
                        apellido_paterno,
                        COUNT(*) AS total_clientes,
                        GROUP_CONCAT(CONCAT(nombres, ' ', apellido_materno) ORDER BY nombres SEPARATOR ', ') AS clientes
                    FROM cliente
                    GROUP BY apellido_paterno
                    ORDER BY total_clientes DESC, apellido_paterno
                """,
                "columnas": ["Apellido Paterno", "Total Clientes", "Clientes"]
            },
            5: {
                "nombre": "CONSULTA 6: Clientes asignados a empleados (JOIN)",
                "descripcion": "Relación empleado-cliente mediante JOIN",
                "query": """
                    SELECT
                        e.codigo,
                        CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
                        e.cargo,
                        e.sexo,
                        c.ruc,
                        CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS cliente,
                        c.telefono,
                        c.correo_electronico
                    FROM empleado e
                    INNER JOIN cliente c ON e.ruc_cliente = c.ruc
                    ORDER BY e.codigo
                """,
                "columnas": ["Código Emp.", "Empleado", "Cargo", "Sexo", "RUC Cliente", "Cliente", "Teléfono", "Correo"]
            },
            6: {
                "nombre": "CONSULTA 7: Estadísticas de empleados por cargo",
                "descripcion": "Análisis demográfico de empleados por cargo",
                "query": """
                    SELECT
                        cargo,
                        COUNT(*) AS total_empleados,
                        SUM(CASE WHEN sexo = 'Masculino' THEN 1 ELSE 0 END) AS hombres,
                        SUM(CASE WHEN sexo = 'Femenino' THEN 1 ELSE 0 END) AS mujeres,
                        MIN(fecha_nacimiento) AS empleado_mas_antiguo,
                        MAX(fecha_nacimiento) AS empleado_mas_joven
                    FROM empleado
                    GROUP BY cargo
                    ORDER BY total_empleados DESC
                """,
                "columnas": ["Cargo", "Total", "Hombres", "Mujeres", "Más Antiguo", "Más Joven"]
            },
            7: {
                "nombre": "CONSULTA 8: Empleados sin clientes asignados",
                "descripcion": "Empleados que no tienen clientes asignados",
                "query": """
                    SELECT
                        e.codigo,
                        CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
                        e.cargo,
                        e.sexo,
                        e.fecha_nacimiento,
                        TIMESTAMPDIFF(YEAR, e.fecha_nacimiento, CURDATE()) AS edad
                    FROM empleado e
                    WHERE e.ruc_cliente IS NULL
                    ORDER BY e.codigo
                """,
                "columnas": ["Código", "Empleado", "Cargo", "Sexo", "Fecha Nacimiento", "Edad"]
            },
            8: {
                "nombre": "CONSULTA 9: Historial completo de consultas SUNAT (JOIN)",
                "descripcion": "Todas las consultas SUNAT con empleado responsable",
                "query": """
                    SELECT
                        cs.nro_consultado,
                        cs.razon_social,
                        cs.estado,
                        cs.condicion,
                        cs.codigo_empleado,
                        CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
                        e.cargo
                    FROM consulta_sunat cs
                    INNER JOIN empleado e ON cs.codigo_empleado = e.codigo
                    ORDER BY cs.nro_consultado
                """,
                "columnas": ["Nro. Consultado", "Razón Social", "Estado", "Condición", "Código Emp.", "Empleado", "Cargo"]
            },
            9: {
                "nombre": "CONSULTA 10: Clientes con problemas en SUNAT",
                "descripcion": "Clientes con estado SUNAT no activo o no habido",
                "query": """
                    SELECT
                        c.ruc,
                        CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS cliente,
                        c.correo_electronico,
                        c.telefono,
                        cs.razon_social,
                        cs.estado,
                        cs.condicion,
                        CASE
                            WHEN cs.estado != 'ACTIVO' THEN 'URGENTE - Estado inactivo'
                            WHEN cs.condicion != 'HABIDO' THEN 'IMPORTANTE - No habido'
                            ELSE 'REVISAR'
                        END AS prioridad
                    FROM cliente c
                    LEFT JOIN consulta_sunat cs ON c.ruc = cs.nro_consultado
                    WHERE cs.estado IS NOT NULL
                      AND (cs.estado != 'ACTIVO' OR cs.condicion != 'HABIDO')
                    ORDER BY
                        CASE
                            WHEN cs.estado != 'ACTIVO' THEN 1
                            WHEN cs.condicion != 'HABIDO' THEN 2
                            ELSE 3
                        END
                """,
                "columnas": ["RUC", "Cliente", "Correo", "Teléfono", "Razón Social", "Estado", "Condición", "Prioridad"]
            },
            10: {
                "nombre": "CONSULTA 11: Productividad de consultas SUNAT por empleado",
                "descripcion": "Estadísticas de consultas SUNAT por empleado",
                "query": """
                    SELECT
                        e.codigo,
                        CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado,
                        e.cargo,
                        COUNT(cs.nro_consultado) AS total_consultas,
                        SUM(CASE WHEN cs.estado = 'ACTIVO' THEN 1 ELSE 0 END) AS consultas_activas,
                        SUM(CASE WHEN cs.condicion = 'HABIDO' THEN 1 ELSE 0 END) AS consultas_habidas
                    FROM empleado e
                    LEFT JOIN consulta_sunat cs ON e.codigo = cs.codigo_empleado
                    GROUP BY e.codigo, empleado, e.cargo
                    ORDER BY total_consultas DESC
                """,
                "columnas": ["Código", "Empleado", "Cargo", "Total Consultas", "Activas", "Habidas"]
            },
            11: {
                "nombre": "CONSULTA 12: Análisis de archivos Excel",
                "descripcion": "Estado y antigüedad de archivos Excel del sistema",
                "query": """
                    SELECT
                        nombre,
                        DATE_FORMAT(fecha_creacion, '%Y-%m-%d %H:%i') AS fecha_creacion,
                        DATE_FORMAT(fecha_modificacion, '%Y-%m-%d %H:%i') AS fecha_modificacion,
                        TIMESTAMPDIFF(DAY, fecha_creacion, fecha_modificacion) AS dias_entre_modificaciones,
                        TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) AS dias_desde_ultima_modificacion,
                        CASE
                            WHEN TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) > 180 THEN 'Archivo antiguo'
                            WHEN TIMESTAMPDIFF(DAY, fecha_modificacion, NOW()) > 90 THEN 'Archivo desactualizado'
                            ELSE 'Archivo reciente'
                        END AS estado_archivo
                    FROM archivo_excel_gestion_clientes
                    ORDER BY fecha_modificacion DESC
                """,
                "columnas": ["Nombre", "Fecha Creación", "Fecha Modificación", "Días Entre Mod.", "Días Desde Última Mod.", "Estado"]
            },
            12: {
                "nombre": "CONSULTA 13: Reporte consolidado Cliente-Empleado-SUNAT (JOIN múltiple)",
                "descripcion": "Vista completa con relaciones Cliente-Empleado-SUNAT",
                "query": """
                    SELECT
                        c.ruc,
                        CONCAT(c.nombres, ' ', c.apellido_paterno, ' ', c.apellido_materno) AS cliente,
                        c.correo_electronico,
                        c.telefono,
                        c.pagina_web,
                        e.codigo AS empleado_codigo,
                        CONCAT(e.nombres, ' ', e.apellido_paterno, ' ', e.apellido_materno) AS empleado_asignado,
                        e.cargo,
                        e.sexo,
                        cs.razon_social,
                        cs.estado AS estado_sunat,
                        cs.condicion AS condicion_sunat,
                        CASE
                            WHEN cs.estado = 'ACTIVO' AND cs.condicion = 'HABIDO' THEN 'VALIDADO'
                            WHEN cs.estado != 'ACTIVO' THEN 'ALERTA - Inactivo'
                            WHEN cs.condicion != 'HABIDO' THEN 'ALERTA - No habido'
                            ELSE 'REVISAR'
                        END AS clasificacion
                    FROM cliente c
                    LEFT JOIN empleado e ON c.ruc = e.ruc_cliente
                    LEFT JOIN consulta_sunat cs ON c.ruc = cs.nro_consultado
                    ORDER BY c.apellido_paterno, c.apellido_materno
                """,
                "columnas": ["RUC", "Cliente", "Correo", "Teléfono", "Página Web", "Cód. Emp.",
                           "Empleado", "Cargo", "Sexo", "Razón Social", "Estado SUNAT",
                           "Condición SUNAT", "Clasificación"]
            }
        }

        self.crear_interfaz()

    def crear_interfaz(self):
        # Header
        header = tk.Frame(self.ventana, bg="#6F42C1", height=70)
        header.pack(fill=tk.X)

        titulo = tk.Label(
            header,
            text="REPORTES Y ANÁLISIS",
            font=("Segoe UI", 16, "bold"),
            bg="#6F42C1",
            fg="white"
        )
        titulo.pack(pady=20)

        # Contenedor principal
        main_container = tk.Frame(self.ventana, bg="#F5F5F5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Panel izquierdo - Lista de reportes
        panel_izq = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), ipadx=10)

        tk.Label(
            panel_izq,
            text="Reportes Disponibles",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#6F42C1"
        ).pack(pady=15)

        # Frame para lista con scrollbar
        list_frame = tk.Frame(panel_izq, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)

        # Lista de reportes
        self.reportes_listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 9),
            bg="#F8F9FA",
            selectbackground="#6F42C1",
            selectforeground="white",
            width=45,
            height=25,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.reportes_listbox.yview)

        self.reportes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Agregar reportes a la lista
        for i in range(13):
            self.reportes_listbox.insert(tk.END, self.reportes[i]["nombre"])

        # Bind para mostrar descripción al seleccionar
        self.reportes_listbox.bind('<<ListboxSelect>>', self.mostrar_descripcion)

        # Frame para descripción
        desc_frame = tk.Frame(panel_izq, bg="#E9ECEF", relief=tk.SUNKEN, bd=1)
        desc_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(
            desc_frame,
            text="Descripción:",
            font=("Segoe UI", 9, "bold"),
            bg="#E9ECEF",
            fg="#495057"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.lbl_descripcion = tk.Label(
            desc_frame,
            text="Seleccione un reporte para ver su descripción",
            font=("Segoe UI", 9),
            bg="#E9ECEF",
            fg="#495057",
            wraplength=380,
            justify="left"
        )
        self.lbl_descripcion.pack(anchor="w", padx=10, pady=(0, 10))

        # Botón generar
        btn_generar = tk.Button(
            panel_izq,
            text="Generar Reporte",
            font=("Segoe UI", 11, "bold"),
            bg="#6F42C1",
            fg="white",
            command=self.generar_reporte,
            cursor="hand2",
            width=20,
            height=2,
            bd=0,
            relief="flat"
        )
        btn_generar.pack(pady=15)

        # Panel derecho - Visualización
        panel_der = tk.Frame(main_container, bg="white", relief=tk.RAISED, bd=2)
        panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            panel_der,
            text="Resultado del Reporte",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#6F42C1"
        ).pack(pady=15)

        # Frame para tabla
        tree_frame = tk.Frame(panel_der, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

        # Treeview para mostrar resultados
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=25
        )

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Info panel
        info_frame = tk.Frame(panel_der, bg="#E9ECEF", height=60)
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        info_frame.pack_propagate(False)

        self.lbl_info = tk.Label(
            info_frame,
            text="Seleccione un reporte de la lista y haga clic en 'Generar Reporte'",
            font=("Segoe UI", 10),
            bg="#E9ECEF",
            fg="#495057"
        )
        self.lbl_info.pack(pady=20)

    def mostrar_descripcion(self, event=None):
        """Muestra la descripción del reporte seleccionado"""
        seleccion = self.reportes_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.lbl_descripcion.config(text=self.reportes[indice]["descripcion"])

    def generar_reporte(self):
        """Genera el reporte seleccionado"""
        seleccion = self.reportes_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un reporte de la lista")
            return

        indice = seleccion[0]
        reporte = self.reportes[indice]

        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Ejecutar query del reporte
            cursor.execute(reporte["query"])
            resultados = cursor.fetchall()

            # Configurar columnas
            self.configurar_columnas(reporte["columnas"])

            # Insertar datos en el tree
            for fila in resultados:
                self.tree.insert("", tk.END, values=fila)

            cursor.close()

            # Actualizar info
            self.lbl_info.config(
                text=f"Reporte generado exitosamente: {len(resultados)} registros encontrados",
                fg="#28A745"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")
            self.lbl_info.config(
                text=f"Error al generar reporte: {str(e)}",
                fg="#DC3545"
            )

    def configurar_columnas(self, columnas):
        """Configura las columnas del treeview"""
        self.tree["columns"] = columnas
        self.tree["show"] = "headings"

        for col in columnas:
            self.tree.heading(col, text=col)
            # Ajustar ancho según el nombre de la columna
            if len(col) > 20:
                ancho = 200
            elif len(col) > 15:
                ancho = 150
            else:
                ancho = 120
            self.tree.column(col, width=ancho, anchor="w")
