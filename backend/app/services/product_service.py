from datetime import datetime
from app.models.product import Product
from app.models.coupon import Coupon
from app.models.product_coupon_application import ProductCouponApplication  # se existir
from app.database import db

class ProductService:
    """Serviço para operações com produtos"""

    @staticmethod
    def list_products(filters):
        query = Product.query

        if 'name' in filters and filters['name']:
            query = query.filter(Product.name.ilike(f"%{filters['name']}%"))

        if 'min_price' in filters and filters['min_price'] is not None:
            query = query.filter(Product.price >= filters['min_price'])

        if 'max_price' in filters and filters['max_price'] is not None:
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
            raise ValueError("O desconto deve estar entre 1% e 80%")

        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")

        # Aplica o desconto no modelo
        product.apply_percentage_discount(percentage)

        # Cria o registro no histórico de aplicação
        ProductCouponApplication.create_application(
            product_id=product.id,
            coupon_id=None,
            discount_amount=product.discount_amount,
            discount_percentage=percentage
        )

        db.session.commit()
        return product.to_dict()

    @staticmethod
    def apply_coupon_discount(product_id, coupon_code):
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")

        coupon = Coupon.query.filter_by(code=coupon_code.upper()).first()
        if not coupon:
            raise ValueError("Cupom não encontrado")

        can_use, reason = coupon.can_be_used()
        if not can_use:
            raise ValueError(reason)

        # Marca como usado
        coupon.use()

        # Aplica desconto no produto
        product.apply_percentage_discount(coupon.discount_percentage)

        # Cria registro da aplicação
        ProductCouponApplication.create_application(
            product_id=product.id,
            coupon_id=coupon.id,
            discount_amount=product.discount_amount,
            discount_percentage=coupon.discount_percentage
        )

        db.session.commit()
        return product.to_dict()

    @staticmethod
    def remove_discount(product_id):
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")

        active_application = ProductCouponApplication.get_active_discount_for_product(product_id)

        if not active_application:
            raise ValueError("Nenhum desconto ativo encontrado para este produto")

        active_application.deactivate()

        # Atualiza o produto para refletir a remoção do desconto
        product.discount_percentage = 0
        product.has_active_discount = False
        product.discount_end_date = datetime.utcnow()

        db.session.commit()

        return {
            'success': True,
            'message': 'Desconto removido com sucesso',
            'final_price': float(product.price),
            'removed_application_id': active_application.id
        }

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

    @staticmethod
    def get_product_discount_details(product_id):
        """Retorna detalhes completos do desconto aplicado ao produto"""
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Produto não encontrado")

        active_application = ProductCouponApplication.get_active_discount_for_product(product_id)

        result = {
            'product_id': product_id,
            'original_price': float(product.price),
            'current_final_price': ProductService.calculate_final_price(product),
            'has_discount': active_application is not None
        }

        if active_application:
            result.update({
                'discount_details': active_application.to_dict(),
                'discount_type': 'coupon' if active_application.coupon_id else 'direct',
                'savings': active_application.discount_amount
            })

            # Se for cupom, buscar dados do cupom
            if active_application.coupon_id:
                coupon = Coupon.query.get(active_application.coupon_id)
                if coupon:
                    result['coupon_info'] = {
                        'code': coupon.code,
                        'name': getattr(coupon, 'name', ''),
                        'description': getattr(coupon, 'description', '')
                    }

        return result

    @staticmethod
    def list_products_with_discount_info(filters=None):
        """Lista produtos com informações detalhadas de desconto"""
        if filters is None:
            filters = {}

        query = Product.query

        # Aplicar filtros básicos
        if 'name' in filters and filters['name']:
            query = query.filter(Product.name.ilike(f"%{filters['name']}%"))

        # Filtros de preço considerando desconto
        if 'min_price' in filters and filters['min_price'] is not None:
            if hasattr(Product, 'final_price'):
                query = query.filter(
                    db.or_(
                        Product.final_price >= filters['min_price'],
                        db.and_(Product.final_price.is_(None), Product.price >= filters['min_price'])
                    )
                )
            else:
                query = query.filter(Product.price >= filters['min_price'])

        if 'max_price' in filters and filters['max_price'] is not None:
            if hasattr(Product, 'final_price'):
                query = query.filter(
                    db.or_(
                        Product.final_price <= filters['max_price'],
                        db.and_(Product.final_price.is_(None), Product.price <= filters['max_price'])
                    )
                )
            else:
                query = query.filter(Product.price <= filters['max_price'])

        # Filtro por produtos com desconto
        if 'has_discount' in filters:
            active_product_ids = db.session.query(ProductCouponApplication.product_id).filter_by(is_active=True).subquery()
            if filters['has_discount']:
                # Produtos com aplicação ativa
                query = query.filter(Product.id.in_(active_product_ids))
            else:
                # Produtos sem aplicação ativa
                query = query.filter(~Product.id.in_(active_product_ids))

        # Paginação
        page = filters.get('page', 1)
        limit = filters.get('limit', 10)
        pagination = query.paginate(page=page, per_page=limit, error_out=False)

        # Enriquecer dados dos produtos
        enriched_products = []
        for product in pagination.items:
            product_dict = product.to_dict()

            # Buscar informações de desconto
            active_application = ProductCouponApplication.get_active_discount_for_product(product.id)

            if active_application:
                product_dict['discount_info'] = active_application.to_dict()
                product_dict['has_active_discount'] = True
                product_dict['savings'] = active_application.discount_amount
            else:
                product_dict['discount_info'] = None
                product_dict['has_active_discount'] = False
                product_dict['savings'] = 0.0

            # Garantir que sempre temos um preço final
            product_dict['calculated_final_price'] = ProductService.calculate_final_price(product)

            enriched_products.append(product_dict)

        return {
            'products': enriched_products,
            'meta': {
                'page': pagination.page,
                'limit': limit,
                'total': pagination.total,
                'totalPages': pagination.pages,
                'hasNext': pagination.has_next,
                'hasPrev': pagination.has_prev
            }
        }
