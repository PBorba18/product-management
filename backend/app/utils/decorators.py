from functools import wraps
from flask import jsonify
import logging

def handle_exceptions(f):
    """Decorator para tratamento padronizado de exceções"""
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logging.warning(f"Erro de validação: {str(e)}")
            return {'message': str(e)}, 400
        except PermissionError as e:
            logging.warning(f"Erro de permissão: {str(e)}")
            return {'message': str(e)}, 403
        except FileNotFoundError as e:
            logging.warning(f"Recurso não encontrado: {str(e)}")
            return {'message': 'Recurso não encontrado'}, 404
        except Exception as e:
            logging.error(f"Erro interno: {str(e)}")
            return {'message': 'Erro interno do servidor'}, 500
    
    return decorated_function