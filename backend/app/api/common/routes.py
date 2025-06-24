from flask_restx import Namespace, Resource
from flask import jsonify

common_ns = Namespace('health', description='Endpoints de saúde da API')

@common_ns.route('/')
class HealthCheckResource(Resource):
    """Health check da aplicação"""
    
    @common_ns.doc('health_check')
    def get(self):
        """Verifica se a API está funcionando"""
        return {
            'status': 'healthy',
            'message': 'Product Management API está rodando',
            'version': '1.0'
        }
common_ns = Namespace('common', description='Operações comuns')

@common_ns.route('/')
class APIRoot(Resource):
    def get(self):
        """Endpoint raiz da API"""
        return {
            'message': 'Product Management API v1.0',
            'version': '1.0',
            'endpoints': {
                'products': '/api/v1/products/',
                'coupons': '/api/v1/coupons/',
                'health': '/api/v1/health/',
                'docs': '/api/docs/'
            }
        }