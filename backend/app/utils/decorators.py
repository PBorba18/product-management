from functools import wraps
from flask import jsonify
import logging
import traceback

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print(f"=== EXECUTANDO {func.__name__} ===")
            result = func(*args, **kwargs)
            print(f"=== RESULTADO: {type(result)} ===")
            print(f"=== CONTEÚDO: {result} ===")
            return result
        except Exception as e:
            print(f"=== ERRO CAPTURADO: {str(e)} ===")
            print(f"=== TRACEBACK: {traceback.format_exc()} ===")
            logging.error(f"Erro em {func.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            return jsonify({'error': str(e)}), 500
    return wrapper