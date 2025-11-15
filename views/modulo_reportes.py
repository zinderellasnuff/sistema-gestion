"""
Módulo de Reportes y Análisis
Sistema JP Business Solutions
Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from models.config_db import Database

class ModuloReportes:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Reportes y Análisis - JP Business Solutions")
        self.ventana.geometry("1400x800")
        self.ventana.configure(bg="#F5F5F5")

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
        ).pack(pady=10)

        # Lista de reportes
        self.reportes_listbox = tk.Listbox(
            panel_izq,
            font=("Arial", 10),
            bg="#F8F9FA",
            selectbackground="#6F42C1",
            selectforeground="white",
            width=40
        )
        self.reportes_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Agregar reportes
        reportes = [
            "1. Clientes Activos por Departamento",
            "2. Empleados por Área con Salarios",
            "3. Consultas SUNAT por Tipo",
            "4. Archivos Excel Procesados",
            "5. Auditoría de Clientes (últimas 30)",
            "6. Clientes con Información Completa",
            "7. Clientes con Información Incompleta",
            "8. Búsqueda Flexible de Clientes",
            "9. Conteo por Tipo de Empresa",
            "10. Clientes Asignados a Empleados",
            "11. Estadísticas de Empleados por Cargo",
            "12. Empleados sin Clientes Asignados",
            "13. Historial Completo SUNAT",
            "─" * 35,
            "📊 Dashboard Principal",
            "⚠️ Clientes con Problemas SUNAT",
            "📈 Productividad SUNAT por Empleado",
            "📁 Análisis de Archivos Excel"
        ]

        for reporte in reportes:
            self.reportes_listbox.insert(tk.END, reporte)

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
            height=2
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
        ).pack(pady=10)

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
            font=("Arial", 10),
            bg="#E9ECEF",
            fg="#495057"
        )
        self.lbl_info.pack(pady=20)

    def generar_reporte(self):
        """Genera el reporte seleccionado"""
        seleccion = self.reportes_listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un reporte")
            return

        indice = seleccion[0]

        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            conn = Database.conectar()
            cursor = conn.cursor()

            # Mapeo de reportes a consultas SQL
            if indice == 0:  # Reporte 1
                query = """
                    SELECT departamento, COUNT(*) AS total_clientes
                    FROM cliente WHERE estado = 'ACTIVO'
                    GROUP BY departamento ORDER BY total_clientes DESC
                """
                self.configurar_columnas(["Departamento", "Total Clientes"])

            elif indice == 1:  # Reporte 2
                query = """
                    SELECT area, cargo, COUNT(*) AS total_empleados,
                           CONCAT('S/ ', FORMAT(AVG(salario), 2)) AS salario_promedio
                    FROM empleado WHERE estado = 'ACTIVO'
                    GROUP BY area, cargo ORDER BY area
                """
                self.configurar_columnas(["Área", "Cargo", "Total Empleados", "Salario Promedio"])

            elif indice == 2:  # Reporte 3
                query = """
                    SELECT tipo_consulta, COUNT(*) AS total,
                           estado_sunat, condicion_sunat
                    FROM consulta_sunat
                    GROUP BY tipo_consulta, estado_sunat, condicion_sunat
                """
                self.configurar_columnas(["Tipo", "Total", "Estado SUNAT", "Condición"])

            elif indice == 3:  # Reporte 4
                query = """
                    SELECT tipo_operacion, COUNT(*) AS total_archivos,
                           SUM(registros_procesados) AS total_registros,
                           ROUND((SUM(registros_exitosos)/SUM(registros_procesados))*100, 2) AS porcentaje_exito
                    FROM archivo_excel_gestion_clientes
                    GROUP BY tipo_operacion
                """
                self.configurar_columnas(["Tipo Operación", "Total Archivos", "Total Registros", "% Éxito"])

            elif indice == 4:  # Reporte 5
                query = """
                    SELECT a.id_auditoria, c.razon_social, a.tipo_operacion,
                           DATE_FORMAT(a.fecha_operacion, '%Y-%m-%d %H:%i') AS fecha
                    FROM auditoria_cliente a
                    LEFT JOIN cliente c ON a.id_cliente = c.id_cliente
                    ORDER BY a.fecha_operacion DESC LIMIT 30
                """
                self.configurar_columnas(["ID", "Cliente", "Operación", "Fecha"])

            elif indice == 5:  # Reporte 6
                query = """
                    SELECT ruc, razon_social, telefono, email, contacto_nombre
                    FROM cliente
                    WHERE telefono IS NOT NULL AND email IS NOT NULL
                      AND contacto_nombre IS NOT NULL AND estado = 'ACTIVO'
                    ORDER BY razon_social
                """
                self.configurar_columnas(["RUC", "Razón Social", "Teléfono", "Email", "Contacto"])

            elif indice == 6:  # Reporte 7
                query = """
                    SELECT ruc, razon_social,
                    CASE
                        WHEN telefono IS NULL THEN 'Falta teléfono'
                        WHEN email IS NULL THEN 'Falta email'
                        WHEN contacto_nombre IS NULL THEN 'Falta contacto'
                        ELSE 'Datos incompletos'
                    END AS dato_faltante
                    FROM cliente
                    WHERE telefono IS NULL OR email IS NULL OR contacto_nombre IS NULL
                """
                self.configurar_columnas(["RUC", "Razón Social", "Dato Faltante"])

            elif indice == 8:  # Reporte 9
                query = """
                    SELECT
                        CASE
                            WHEN razon_social LIKE '%SAC%' THEN 'SAC'
                            WHEN razon_social LIKE '%SRL%' THEN 'SRL'
                            WHEN razon_social LIKE '%EIRL%' THEN 'EIRL'
                            WHEN razon_social LIKE '%SA%' THEN 'SA'
                            ELSE 'OTRO'
                        END AS tipo_empresa,
                        COUNT(*) AS total_clientes
                    FROM cliente WHERE estado = 'ACTIVO'
                    GROUP BY tipo_empresa ORDER BY total_clientes DESC
                """
                self.configurar_columnas(["Tipo Empresa", "Total Clientes"])

            elif indice == 10:  # Reporte 11
                query = """
                    SELECT cargo, area, COUNT(*) AS total,
                           CONCAT('S/ ', FORMAT(AVG(salario), 2)) AS salario_prom,
                           MIN(fecha_ingreso) AS mas_antiguo
                    FROM empleado WHERE estado = 'ACTIVO'
                    GROUP BY cargo, area ORDER BY total DESC
                """
                self.configurar_columnas(["Cargo", "Área", "Total", "Salario Prom", "Más Antiguo"])

            elif indice == 12:  # Reporte 13
                query = """
                    SELECT cs.id_consulta, cs.ruc_consultado, c.razon_social,
                           cs.estado_sunat, cs.condicion_sunat,
                           DATE_FORMAT(cs.fecha_consulta, '%Y-%m-%d') AS fecha
                    FROM consulta_sunat cs
                    LEFT JOIN cliente c ON cs.id_cliente = c.id_cliente
                    ORDER BY cs.fecha_consulta DESC LIMIT 100
                """
                self.configurar_columnas(["ID", "RUC", "Cliente", "Estado SUNAT", "Condición", "Fecha"])

            elif indice == 14:  # Dashboard
                query = """
                    SELECT
                        (SELECT COUNT(*) FROM cliente WHERE estado = 'ACTIVO') AS clientes_activos,
                        (SELECT COUNT(*) FROM empleado WHERE estado = 'ACTIVO') AS empleados_activos,
                        (SELECT COUNT(*) FROM consulta_sunat) AS total_consultas_sunat,
                        (SELECT SUM(salario) FROM empleado WHERE estado = 'ACTIVO') AS nomina_total
                """
                self.configurar_columnas(["Clientes Activos", "Empleados Activos", "Consultas SUNAT", "Nómina Total"])

            else:
                messagebox.showinfo("Info", "Reporte seleccionado en desarrollo")
                return

            cursor.execute(query)
            resultados = cursor.fetchall()

            # Insertar datos en el tree
            for fila in resultados:
                self.tree.insert("", tk.END, values=fila)

            cursor.close()

            self.lbl_info.config(
                text=f"✓ Reporte generado: {len(resultados)} registros encontrados"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            self.lbl_info.config(text=f"✗ Error al generar reporte")

    def configurar_columnas(self, columnas):
        """Configura las columnas del treeview"""
        self.tree["columns"] = columnas
        self.tree["show"] = "headings"

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="w")
