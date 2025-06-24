from flask_restx import fields, Model

# Modelo para entrada (criação/atualização)
product_input_model = Model('ProductInput', {
    'name': fields.String(required=True, min_length=3, max_length=100,
                         description='Nome único do produto'),
    'description': fields.String(max_length=300, 
                                description='Descrição do produto'),
    'price': fields.Float(required=True, min=0.01, max=1000000,
                         description='Preço do produto (mín: R$ 0,01)'),
    'stock': fields.Integer(required=True, min=0, max=999999,
                           description='Quantidade em estoque')
})

# Modelo para saída (resposta)
product_output_model = Model('ProductOutput', {
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

# Modelo para listagem
product_list_model = Model('ProductList', {
    'data': fields.List(fields.Nested(product_output_model)),
    'meta': fields.Raw(description='Metadados da paginação')
})

# Modelo para aplicação de desconto
discount_input_model = Model('DiscountInput', {
    'percentage': fields.Float(required=True, min=1, max=80,
                              description='Percentual de desconto (1-80)')
})