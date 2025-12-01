"""
Controlador para consultas SUNAT
Versión: 5.0 - API Decolecta (FUNCIONAL)
Sistema de Gestión Empresarial
"""

import requests
import re
from typing import Dict, Optional

class SUNATController:
    """Controlador para interactuar con API de consulta RUC"""

    # ✅ API DECOLECTA - Configuración
    API_URL = 'https://api.decolecta.com/v1/sunat/ruc/full'
    
    # 🔑 TOKEN DE API (Válido hasta: November de 2026)
    API_TOKEN = 'sk_11946.XqCed7qtXxj0tVWCQNcqhnZoMpAIScaS'

    @staticmethod
    def validar_ruc(ruc: str) -> bool:
        """
        Valida que el RUC tenga el formato correcto (11 dígitos)

        Args:
            ruc: Número de RUC a validar

        Returns:
            bool: True si es válido, False si no
        """
        if not ruc:
            return False
        
        ruc = ruc.strip()
        
        # Validar formato: 11 dígitos numéricos
        if not re.match(r'^\d{11}$', ruc):
            return False
        
        # El RUC debe empezar con 10, 15, 17 o 20
        if ruc[0:2] not in ['10', '15', '17', '20']:
            return False
        
        return True

    @staticmethod
    def consultar_ruc(ruc: str) -> Dict[str, Optional[str]]:
        """
        Consulta un RUC usando la API de Decolecta

        Args:
            ruc: Número de RUC a consultar

        Returns:
            dict: Información del RUC
        """
        # Validar formato
        if not SUNATController.validar_ruc(ruc):
            return {
                'success': False,
                'error': 'RUC inválido.\n\n'
                        '✓ Debe contener 11 dígitos numéricos\n'
                        '✓ Debe comenzar con: 10, 15, 17 o 20\n\n'
                        'Ejemplo: 20100070970',
                'razon_social': None,
                'estado': None,
                'condicion': None,
                'direccion': None,
                'ubigeo': None,
                'api_used': None
            }

        ruc = ruc.strip()

        try:
            # ✅ CONSULTAR API DECOLECTA
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {SUNATController.API_TOKEN}'
            }
            
            params = {'numero': ruc}
            
            print(f"🔍 Consultando RUC {ruc} en API Decolecta...")
            
            response = requests.get(
                SUNATController.API_URL,
                headers=headers,
                params=params,
                timeout=15
            )

            print(f"📡 Respuesta API: Status {response.status_code}")

            # Verificar respuesta
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Datos recibidos: {data}")
                
                # ✅ CORRECCIÓN: Buscar razon_social primero (con guion bajo)
                razon_social = (
                    data.get('razon_social') or 
                    data.get('razonSocial') or 
                    data.get('nombre') or 
                    ''
                ).strip()
                
                # Extraer datos según estructura de Decolecta
                return {
                    'success': True,
                    'razon_social': razon_social,
                    'estado': data.get('estado', 'ACTIVO').upper(),
                    'condicion': data.get('condicion', 'HABIDO').upper(),
                    'direccion': data.get('direccion', '').strip(),
                    'ubigeo': data.get('ubigeo', '').strip(),
                    'error': None,
                    'api_used': 'API Decolecta'
                }
            
            elif response.status_code == 401:
                return {
                    'success': False,
                    'error': '❌ Token de API inválido o expirado.\n\n'
                            'Verifica tu token en:\n'
                            'https://decolecta.com/dashboard\n\n'
                            'Por ahora, completa los datos manualmente.',
                    'razon_social': None,
                    'estado': None,
                    'condicion': None,
                    'direccion': None,
                    'ubigeo': None,
                    'api_used': 'API Decolecta'
                }
            
            elif response.status_code == 404:
                return {
                    'success': False,
                    'error': f'RUC {ruc} no encontrado en SUNAT.\n\n'
                            'Verifique que el RUC sea correcto.',
                    'razon_social': None,
                    'estado': None,
                    'condicion': None,
                    'direccion': None,
                    'ubigeo': None,
                    'api_used': 'API Decolecta'
                }
            
            else:
                error_detail = response.text[:200] if response.text else 'Sin detalles'
                print(f"❌ Error {response.status_code}: {error_detail}")
                return {
                    'success': False,
                    'error': f'Error al consultar: Código {response.status_code}\n\n'
                            'Complete los datos manualmente.',
                    'razon_social': None,
                    'estado': None,
                    'condicion': None,
                    'direccion': None,
                    'ubigeo': None,
                    'api_used': 'API Decolecta'
                }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Tiempo de espera agotado.\n\n'
                        'La API está tardando mucho en responder.\n'
                        'Intente nuevamente o complete los datos manualmente.',
                'razon_social': None,
                'estado': None,
                'condicion': None,
                'direccion': None,
                'ubigeo': None,
                'api_used': None
            }
        
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Sin conexión a Internet.\n\n'
                        'Verifique su conexión de red.\n'
                        'Complete los datos manualmente.',
                'razon_social': None,
                'estado': None,
                'condicion': None,
                'direccion': None,
                'ubigeo': None,
                'api_used': None
            }
        
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}\n\n'
                        'Complete los datos manualmente.',
                'razon_social': None,
                'estado': None,
                'condicion': None,
                'direccion': None,
                'ubigeo': None,
                'api_used': None
            }

    @staticmethod
    def normalizar_estado(estado: str) -> str:
        """Normaliza el estado SUNAT"""
        estado = estado.upper().strip() if estado else 'ACTIVO'
        
        mapeo = {
            'ACTIVO': 'ACTIVO',
            'ACTIVE': 'ACTIVO',
            'BAJA': 'BAJA DE OFICIO',
            'BAJA DE OFICIO': 'BAJA DE OFICIO',
            'BAJA PROVISIONAL': 'BAJA PROVISIONAL',
            'SUSPENSION': 'SUSPENSION TEMPORAL',
            'SUSPENDIDO': 'SUSPENSION TEMPORAL',
            'SUSPENSION TEMPORAL': 'SUSPENSION TEMPORAL',
            'INHABILITADO': 'INHABILITADO'
        }
        
        return mapeo.get(estado, 'ACTIVO')

    @staticmethod
    def normalizar_condicion(condicion: str) -> str:
        """Normaliza la condición del contribuyente"""
        condicion = condicion.upper().strip() if condicion else 'HABIDO'
        
        mapeo = {
            'HABIDO': 'HABIDO',
            'NO HABIDO': 'NO HABIDO',
            'NO HALLADO': 'NO HALLADO',
            'PENDIENTE': 'PENDIENTE',
            'NO VERIFICADO': 'NO VERIFICADO'
        }
        
        return mapeo.get(condicion, 'HABIDO')