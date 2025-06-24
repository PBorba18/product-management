from app.models.product import Product
from app.models.coupon import Coupon
from app.models.product_coupon_application import ProductCouponApplication  # se existir

from app.database import db

class ProductService:
    """Serviço para operações com produtos (implementação real)"""

    @staticmethod
    def list_products(filters):
        query = Product.query

        if 'name' in filters:
            query = query.filter(Product.name.ilike(f"%{filters['name']}%"))
        if 'min_price' in filters:
            # Assumindo que você tem um campo final_price na tabela ou calculamos baseado no price
            # Se não tiver final_price, use Product.price
            query = query.filter(Product.price >= filters['min_price'])
        if 'max_price' in filters:
            query = query.filter(Product.price <= filters['max_price'])

        page = filters.get('page', 1)
        limit = filters.get('limit', 10)
        pagination = query.paginate(page=page, per_page=limit, error_out=False)

        return {
            'products': [product.to_dict() for product in pagination.items],
            'meta': {
                'page': pagination.page,
                'limit': limit,
                'total': pagination.total,
                'totalPages': pagination.pages,
                'hasNext': pagination.has_next,
                'hasPrev': pagination.has_prev
            }
        }

    @staticmethod
    def create_product(data):
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict()

    @staticmethod
    def get_product_by_id(product_id):
        product = Product.query.get(product_id)
        return product.to_dict() if product else None

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return None

        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()
        return product.to_dict()

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return False

        db.session.delete(product)
        db.session.commit()
        return True

    @staticmethod
    def apply_percentage_discount(product_id, percentage):
        if not (1 <= percentage <= 80):
            raise ValueError("Desconto deve estar entre 1% e 80%")

        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")

        # Usar o preço original do produto
        original_price = float(product.price)
        discount_value = original_price * (percentage / 100)
        final_price = round(original_price - discount_value, 2)
        
        # Se você tiver um campo final_price na tabela, use:
        # product.final_price = final_price
        # Se não tiver, você pode adicionar um campo discount_percentage:
        product.discount_percentage = percentage
        
        db.session.commit()
        return True

    @staticmethod
    def apply_coupon_discount(product_id, coupon_code):
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")

        coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
        if not coupon:
            raise ValueError("Cupom inválido ou inativo")

        # Usar o preço original do produto
        original_price = float(product.price)
        # Assumindo que o cupom tem um campo discount_percentage
        discount_value = original_price * (coupon.discount_percentage / 100)
        final_price = round(original_price - discount_value, 2)
        
        # Se você tiver campos específicos na tabela:
        # product.final_price = final_price
        product.discount_percentage = coupon.discount_percentage
        product.has_coupon_applied = True
        
        db.session.commit()
        return True

    @staticmethod
    def remove_discount(product_id):
        product = Product.query.get(product_id)
        if not product:
            return False

        # Remover desconto - voltar ao preço original
        # product.final_price = product.price  # se tiver campo final_price
        product.discount_percentage = 0
        product.has_coupon_applied = False
        
        db.session.commit()
        return True

    @staticmethod
    def calculate_final_price(product):
        """
        Método auxiliar para calcular o preço final de um produto
        considerando descontos aplicados
        """
        original_price = float(product.price)
        discount_percentage = getattr(product, 'discount_percentage', 0) or 0
        
        if discount_percentage > 0:
            discount_value = original_price * (discount_percentage / 100)
            return round(original_price - discount_value, 2)
        
        return original_price