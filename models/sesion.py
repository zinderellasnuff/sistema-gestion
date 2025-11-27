"""
Módulo de Sesión de Usuario
Sistema de Gestión de Clientes JP
Maneja la sesión activa del usuario autenticado
"""

class SesionUsuario:
    """
    Clase Singleton para manejar la sesión del usuario actual
    """
    _instancia = None
    _usuario_actual = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(SesionUsuario, cls).__new__(cls)
        return cls._instancia

    @classmethod
    def iniciar_sesion(cls, usuario_data):
        """
        Inicia la sesión con los datos del usuario

        Args:
            usuario_data (dict): Diccionario con datos del usuario
                - id: ID del usuario
                - usuario: Nombre de usuario
                - rol: Rol del usuario (Administrador/Contabilidad)
                - nombre_completo: Nombre completo
                - email: Email
        """
        cls._usuario_actual = {
            'id': usuario_data.get('id'),
            'usuario': usuario_data.get('usuario'),
            'rol': usuario_data.get('rol'),
            'nombre_completo': usuario_data.get('nombre_completo'),
            'email': usuario_data.get('email')
        }
        print(f"✓ Sesión iniciada: {cls._usuario_actual['usuario']} ({cls._usuario_actual['rol']})")

    @classmethod
    def cerrar_sesion(cls):
        """Cierra la sesión actual"""
        if cls._usuario_actual:
            print(f"✓ Sesión cerrada: {cls._usuario_actual['usuario']}")
        cls._usuario_actual = None

    @classmethod
    def obtener_usuario(cls):
        """Retorna los datos del usuario actual"""
        return cls._usuario_actual

    @classmethod
    def esta_autenticado(cls):
        """Verifica si hay un usuario autenticado"""
        return cls._usuario_actual is not None

    @classmethod
    def es_administrador(cls):
        """Verifica si el usuario actual es administrador"""
        if not cls._usuario_actual:
            return False
        return cls._usuario_actual.get('rol') == 'Administrador'

    @classmethod
    def es_contabilidad(cls):
        """Verifica si el usuario actual es de contabilidad"""
        if not cls._usuario_actual:
            return False
        return cls._usuario_actual.get('rol') == 'Contabilidad'

    @classmethod
    def puede_eliminar(cls):
        """Verifica si el usuario puede eliminar registros"""
        # Solo administrador puede eliminar
        return cls.es_administrador()

    @classmethod
    def obtener_nombre(cls):
        """Retorna el nombre del usuario actual"""
        if cls._usuario_actual:
            return cls._usuario_actual.get('nombre_completo', 'Usuario')
        return 'No autenticado'

    @classmethod
    def obtener_rol(cls):
        """Retorna el rol del usuario actual"""
        if cls._usuario_actual:
            return cls._usuario_actual.get('rol', 'Sin rol')
        return 'Sin rol'

    @classmethod
    def obtener_id(cls):
        """Retorna el ID del usuario actual"""
        if cls._usuario_actual:
            return cls._usuario_actual.get('id')
        return None
