from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.product_service import ProductService
from app.utils.decorators import handle_exceptions
import logging

# Criar namespace para produtos
products_ns = Namespace('products', description='Operações com produtos')

# Modelos para Swagger
product_input_model = products_ns.model('ProductInput', {
    'name': fields.String(required=True, min_length=3, max_length=100,
                         description='Nome único do produto'),
    'description': fields.String(max_length=300, 
                                description='Descrição do produto'),
    'price': fields.Float(required=True, min=0.01, max=1000000,
                         description='Preço do produto (mín: R$ 0,01)'),
    'stock': fields.Integer(required=True, min=0, max=999999,
                           description='Quantidade em estoque')
})

product_output_model = products_ns.model('ProductOutput', {
    'id': fields.Integer(description='ID único do produto'),
    'name': fields.String(description='Nome do produto'),
    'description': fields.String(description='Descrição do produto'),
    'price': fields.Float(description='Preço original'),
    'stock': fields.Integer(description='Estoque atual'),
    'finalPrice': fields.Float(description='Preço com desconto (se aplicável)'),
    'isOutOfStock': fields.Boolean(description='Produto sem estoque'),
    'discount': fields.Raw(description='Informações do desconto ativo'),
    'hasCouponApplied': fields.Boolean(description='Possui cupom aplicado'),
    'createdAt': fields.DateTime(description='Data de criação'),
    'updatedAt': fields.DateTime(description='Data de atualização')
})

product_list_model = products_ns.model('ProductList', {
    'data': fields.List(fields.Nested(product_output_model)),
    'meta': fields.Raw(description='Metadados da paginação')
})

discount_input_model = products_ns.model('DiscountInput', {
    'percentage': fields.Float(required=True, min=1, max=80,
                              description='Percentual de desconto (1-80)')
})

coupon_input_model = products_ns.model('CouponApplication', {
    'code': fields.String(required=True, description='Código do cupom')
})

@products_ns.route('/')
class ProductListResource(Resource):
    """Recurso para listagem e criação de produtos"""
    
    @products_ns.doc('list_products')
    @products_ns.param('page', 'Número da página', type=int, default=1)
    @products_ns.param('limit', 'Itens por página (1-50)', type=int, default=10)
    @products_ns.param('search', 'Busca por nome ou descrição', type=str)
    @products_ns.param('minPrice', 'Preço mínimo', type=float)
    @products_ns.param('maxPrice', 'Preço máximo', type=float)
    @products_ns.param('hasDiscount', 'Filtrar produtos com desconto', type=bool)
    @products_ns.param('sortBy', 'Campo para ordenação', type=str, 
                      enum=['name', 'price', 'stock', 'created_at'])
    @products_ns.param('sortOrder', 'Direção da ordenação', type=str, 
                      enum=['asc', 'desc'], default='asc')
    @products_ns.param('onlyOutOfStock', 'Apenas produtos sem estoque', type=bool)
    @products_ns.marshal_with(product_list_model)
    @handle_exceptions
    def get(self):
        """Lista produtos com filtros avançados e paginação"""
        
        # Extrair e validar parâmetros
        filters = {
            'page': request.args.get('page', 1, type=int),
            'limit': min(request.args.get('limit', 10, type=int), 50),
            'search': request.args.get('search', '').strip(),
            'min_price': request.args.get('minPrice', type=float),
            'max_price': request.args.get('maxPrice', type=float),
            'has_discount': request.args.get('hasDiscount', type=bool),
            'sort_by': request.args.get('sortBy', 'name'),
            'sort_order': request.args.get('sortOrder', 'asc'),
            'only_out_of_stock': request.args.get('onlyOutOfStock', type=bool)
        }
        
        logging.info(f"Listando produtos com filtros: {filters}")
        
        # Chamar service
        result = ProductService.list_products(filters)
        
        return {
            'data': result['products'],
            'meta': result['meta']
        }
    
    @products_ns.doc('create_product')
    @products_ns.expect(product_input_model, validate=True)
    @products_ns.marshal_with(product_output_model, code=201)
    @handle_exceptions
    def post(self):
        """Cria um novo produto"""
        
        data = request.get_json()
        logging.info(f"Criando produto: {data.get('name')}")
        
        # Chamar service
        product = ProductService.create_product(data)
        
        return product, 201

@products_ns.route('/<int:product_id>')
class ProductResource(Resource):
    """Recurso para operações em produto específico"""
    
    @products_ns.doc('get_product')
    @products_ns.marshal_with(product_output_model)
    @handle_exceptions
    def get(self, product_id):
        """Obtém detalhes de um produto específico"""
        
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            products_ns.abort(404, 'Produto não encontrado')
        
        return product
    
    @products_ns.doc('update_product')
    @products_ns.expect(product_input_model, validate=True)
    @products_ns.marshal_with(product_output_model)
    @handle_exceptions
    def patch(self, product_id):
        """Atualiza parcialmente um produto"""
        
        data = request.get_json()
        logging.info(f"Atualizando produto {product_id}: {data}")
        
        product = ProductService.update_product(product_id, data)
        
        if not product:
            products_ns.abort(404, 'Produto não encontrado')
        
        return product
    
    @products_ns.doc('delete_product')
    @handle_exceptions
    def delete(self, product_id):
        """Inativa um produto (soft delete)"""
        
        success = ProductService.delete_product(product_id)
        
        if not success:
            products_ns.abort(404, 'Produto não encontrado')
        
        return '', 204

@products_ns.route('/<int:product_id>/discount/percent')
class ProductPercentDiscountResource(Resource):
    """Aplicar desconto percentual"""
    
    @products_ns.doc('apply_percent_discount')
    @products_ns.expect(discount_input_model, validate=True)
    @handle_exceptions
    def post(self, product_id):
        """Aplica desconto percentual ao produto"""
        
        data = request.get_json()
        percentage = data.get('percentage')
        
        logging.info(f"Aplicando desconto {percentage}% ao produto {product_id}")
        
        try:
            ProductService.apply_percentage_discount(product_id, percentage)
            return {'message': 'Desconto aplicado com sucesso'}, 200
        except ValueError as e:
            products_ns.abort(400, str(e))
        except Exception as e:
            products_ns.abort(422, str(e))

@products_ns.route('/<int:product_id>/discount/coupon')
class ProductCouponDiscountResource(Resource):
    """Aplicar cupom promocional"""
    
    @products_ns.doc('apply_coupon_discount')
    @products_ns.expect(coupon_input_model, validate=True)
    @handle_exceptions
    def post(self, product_id):
        """Aplica cupom promocional ao produto"""
        
        data = request.get_json()
        coupon_code = data.get('code')
        
        logging.info(f"Aplicando cupom {coupon_code} ao produto {product_id}")
        
        try:
            ProductService.apply_coupon_discount(product_id, coupon_code)  
            return {'message': 'Cupom aplicado com sucesso'}, 200
        except ValueError as e:
            products_ns.abort(400, str(e))
        except Exception as e:
            products_ns.abort(422, str(e))

@products_ns.route('/<int:product_id>/discount')
class ProductDiscountResource(Resource):
    """Remover desconto"""
    
    @products_ns.doc('remove_discount')
    @handle_exceptions
    def delete(self, product_id):
        """Remove desconto ativo do produto"""
        
        logging.info(f"Removendo desconto do produto {product_id}")
        
        success = ProductService.remove_discount(product_id)
        
        if not success:
            products_ns.abort(404, 'Produto não encontrado ou sem desconto ativo')
        
        return '', 204