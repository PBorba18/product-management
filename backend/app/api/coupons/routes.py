from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.coupon_service import CouponService


coupons_ns = Namespace('coupons', description='Operações com cupons promocionais')

# Modelo para criação de cupom
coupon_input_model = coupons_ns.model('CouponInput', {
    'code': fields.String(required=True, description='Código do cupom (será convertido para maiúscula)', example='DESCONTO20'),
    'description': fields.String(required=False, description='Descrição do cupom', example='Desconto de 20% para novos clientes'),
    'discount_percentage': fields.Float(required=True, description='Percentual de desconto (0-100)', example=20.0, min=0, max=100),
    'valid_from': fields.String(required=True, description='Data de início da validade (ISO format)', example='2025-06-24T00:00:00Z'),
    'valid_until': fields.String(required=True, description='Data de fim da validade (ISO format)', example='2025-12-31T23:59:59Z'),
    'usage_limit': fields.Integer(required=False, description='Limite de uso do cupom', example=100, default=1, min=1)
})

# Modelo para atualização de cupom
coupon_update_model = coupons_ns.model('CouponUpdate', {
    'code': fields.String(required=False, description='Código do cupom'),
    'description': fields.String(required=False, description='Descrição do cupom'),
    'discount_percentage': fields.Float(required=False, description='Percentual de desconto (0-100)', min=0, max=100),
    'valid_from': fields.String(required=False, description='Data de início da validade (ISO format)'),
    'valid_until': fields.String(required=False, description='Data de fim da validade (ISO format)'),
    'usage_limit': fields.Integer(required=False, description='Limite de uso do cupom', min=1)
})

# Modelo de resposta de cupom
coupon_response_model = coupons_ns.model('CouponResponse', {
    'id': fields.Integer(description='ID do cupom'),
    'code': fields.String(description='Código do cupom'),
    'description': fields.String(description='Descrição do cupom'),
    'discount_percentage': fields.Float(description='Percentual de desconto'),
    'valid_from': fields.String(description='Data de início da validade'),
    'valid_until': fields.String(description='Data de fim da validade'),
    'usage_limit': fields.Integer(description='Limite de uso'),
    'usage_count': fields.Integer(description='Quantidade de usos'),
    'is_active': fields.Boolean(description='Se o cupom está ativo'),
    'is_valid': fields.Boolean(description='Se o cupom está válido'),
    'is_expired': fields.Boolean(description='Se o cupom está expirado'),
    'remaining_uses': fields.Integer(description='Usos restantes'),
    'created_at': fields.String(description='Data de criação'),
    'updated_at': fields.String(description='Data de atualização')
})

@coupons_ns.route('/')
class CouponListResource(Resource):
    """Listagem e criação de cupons"""
    
    @coupons_ns.doc('list_coupons')
    @coupons_ns.marshal_list_with(coupon_response_model, envelope='data')
    def get(self):
        """Lista cupons disponíveis"""
        try:
            # Pegar filtros da query string
            filters = {
                'search': request.args.get('search'),
                'min_discount': request.args.get('min_discount', type=float),
                'max_discount': request.args.get('max_discount', type=float),
                'is_valid': request.args.get('is_valid', type=bool),
                'page': request.args.get('page', 1, type=int),
                'limit': request.args.get('limit', 10, type=int),
                'sort_by': request.args.get('sort_by', 'created_at'),
                'sort_order': request.args.get('sort_order', 'desc')
            }
            # Remover filtros None
            filters = {k: v for k, v in filters.items() if v is not None}
            
            result = CouponService.list_coupons(filters)
            return result
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')
    
    @coupons_ns.doc('create_coupon')
    @coupons_ns.expect(coupon_input_model, validate=True)
    @coupons_ns.marshal_with(coupon_response_model, code=201)
    def post(self):
        """Cria novo cupom promocional"""
        try:
            data = request.get_json()
            
            # Validações básicas
            if not data:
                coupons_ns.abort(400, 'Dados não fornecidos')
            
            required_fields = ['code', 'discount_percentage', 'valid_from', 'valid_until']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                coupons_ns.abort(400, f'Campos obrigatórios ausentes: {", ".join(missing_fields)}')
            
            # Validar percentual de desconto
            if not 0 <= data['discount_percentage'] <= 100:
                coupons_ns.abort(400, 'Percentual de desconto deve estar entre 0 e 100')
            
            coupon = CouponService.create_coupon(data)
            return coupon, 201
            
        except ValueError as e:
            coupons_ns.abort(400, str(e))
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')

@coupons_ns.route('/<string:coupon_code>')
class CouponResource(Resource):
    """Operações em cupom específico"""
    
    @coupons_ns.doc('get_coupon')
    @coupons_ns.marshal_with(coupon_response_model)
    def get(self, coupon_code):
        """Detalhes de um cupom pelo código"""
        try:
            coupon = CouponService.get_coupon_by_code(coupon_code)
            if not coupon:
                coupons_ns.abort(404, 'Cupom não encontrado')
            return coupon
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')
    
    @coupons_ns.doc('update_coupon')
    @coupons_ns.expect(coupon_update_model, validate=True)
    @coupons_ns.marshal_with(coupon_response_model)
    def put(self, coupon_code):
        """Atualiza um cupom pelo código"""
        try:
            # Primeiro buscar o cupom pelo código para pegar o ID
            existing_coupon = CouponService.get_coupon_by_code(coupon_code)
            if not existing_coupon:
                coupons_ns.abort(404, 'Cupom não encontrado')
            
            data = request.get_json()
            if not data:
                coupons_ns.abort(400, 'Dados não fornecidos')
            
            # Validar percentual de desconto se fornecido
            if 'discount_percentage' in data and not 0 <= data['discount_percentage'] <= 100:
                coupons_ns.abort(400, 'Percentual de desconto deve estar entre 0 e 100')
            
            updated_coupon = CouponService.update_coupon(existing_coupon['id'], data)
            if not updated_coupon:
                coupons_ns.abort(404, 'Cupom não encontrado')
            
            return updated_coupon
            
        except ValueError as e:
            coupons_ns.abort(400, str(e))
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')
    
    @coupons_ns.doc('delete_coupon')
    def delete(self, coupon_code):
        """Remove um cupom pelo código (soft delete)"""
        try:
            # Primeiro buscar o cupom pelo código para pegar o ID
            existing_coupon = CouponService.get_coupon_by_code(coupon_code)
            if not existing_coupon:
                coupons_ns.abort(404, 'Cupom não encontrado')
            
            success = CouponService.delete_coupon(existing_coupon['id'])
            if not success:
                coupons_ns.abort(404, 'Cupom não encontrado')
            
            return {'message': 'Cupom removido com sucesso'}, 200
            
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')

@coupons_ns.route('/<int:coupon_id>')
class CouponByIdResource(Resource):
    """Operações em cupom específico por ID"""
    
    @coupons_ns.doc('get_coupon_by_id')
    @coupons_ns.marshal_with(coupon_response_model)
    def get(self, coupon_id):
        """Detalhes de um cupom pelo ID"""
        try:
            coupon = CouponService.get_coupon_by_id(coupon_id)
            if not coupon:
                coupons_ns.abort(404, 'Cupom não encontrado')
            return coupon
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')

@coupons_ns.route('/validate/<string:coupon_code>')
class CouponValidationResource(Resource):
    """Validação de cupons"""
    
    @coupons_ns.doc('validate_coupon')
    def get(self, coupon_code):
        """Valida se um cupom pode ser usado"""
        try:
            validation = CouponService.validate_coupon(coupon_code)
            return validation
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')

@coupons_ns.route('/use/<string:coupon_code>')
class CouponUsageResource(Resource):
    """Uso de cupons"""
    
    @coupons_ns.doc('use_coupon')
    @coupons_ns.marshal_with(coupon_response_model)
    def post(self, coupon_code):
        """Marca um cupom como usado"""
        try:
            coupon = CouponService.use_coupon(coupon_code)
            return coupon
        except ValueError as e:
            coupons_ns.abort(400, str(e))
        except Exception as e:
            coupons_ns.abort(500, f'Erro interno: {str(e)}')