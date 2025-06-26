from datetime import datetime
try:
    from app.database import db
except ImportError:
    try:
        from app import db
    except ImportError:
        try:
            from database import db
        except ImportError:
            from flask_sqlalchemy import SQLAlchemy
            db = SQLAlchemy()

class ProductCouponApplication(db.Model):
    """Modelo para aplicação de cupons em produtos"""
    
    __tablename__ = 'product_coupon_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=True)  # NULLABLE para descontos diretos
    discount_amount = db.Column(db.Float, nullable=False)
    applied_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    discount_percentage = db.Column(db.Float, default=0.0)
    

    
    # Relacionamentos
    product = db.relationship('Product', backref='coupon_applications', lazy=True)
    coupon = db.relationship('Coupon', backref='product_applications', lazy=True)
    
    # Índices para otimização
    __table_args__ = (
        db.Index('idx_product_coupon_active', 'product_id', 'is_active'),
        db.Index('idx_coupon_product_active', 'coupon_id', 'is_active'),
        # Removido o índice único problemático por enquanto
    )
    
    def __init__(self, product_id, coupon_id=None, discount_amount=0.0, discount_percentage=0.0):
        """
        Construtor flexível que aceita cupom ou desconto direto
        """
        self.product_id = product_id
        self.coupon_id = coupon_id  # Pode ser None para descontos diretos
        self.discount_amount = discount_amount
        self.discount_percentage = discount_percentage
        self.is_active = True
    
    def save(self):
        """Salva o registro no banco de dados"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar ProductCouponApplication: {e}")
            return False
    
    def update(self):
        """Atualiza o registro no banco de dados"""
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar ProductCouponApplication: {e}")
            return False
    
    def delete(self):
        """Remove o registro do banco de dados"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar ProductCouponApplication: {e}")
            return False
    
    def __repr__(self):
        coupon_info = f"Coupon:{self.coupon_id}" if self.coupon_id else "Direct Discount"
        return f'<ProductCouponApplication Product:{self.product_id} {coupon_info}>'
    
    def deactivate(self):
        """Desativa a aplicação do cupom"""
        self.is_active = False
        return self.update()
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'coupon_id': self.coupon_id,
            'discount_amount': float(self.discount_amount),
            'discount_percentage': float(self.discount_percentage),
            'applied_at': self.applied_at.isoformat() + 'Z' if self.applied_at else None,
            'is_active': self.is_active,
            'is_coupon_discount': self.coupon_id is not None
        }
    
    @staticmethod
    def create_application(product_id, coupon_id=None, discount_amount=0.0, discount_percentage=0.0):
        """Método estático para criar nova aplicação"""
        # Verificar se já existe aplicação ativa para o produto
        existing = ProductCouponApplication.get_active_discount_for_product(product_id)
        if existing:
            existing.deactivate()  # Desativa o anterior
        
        # Criar nova aplicação
        new_application = ProductCouponApplication(
            product_id=product_id,
            coupon_id=coupon_id,
            discount_amount=discount_amount,
            discount_percentage=discount_percentage
        )
        
        if new_application.save():
            return new_application
        return None
    
    @staticmethod
    def get_active_discount_for_product(product_id):
        """Busca desconto ativo para um produto específico"""
        return ProductCouponApplication.query.filter_by(
            product_id=product_id,
            is_active=True
        ).first()
    
    @staticmethod
    def has_active_discount(product_id):
        """Verifica se produto tem desconto ativo"""
        return ProductCouponApplication.query.filter_by(
            product_id=product_id,
            is_active=True
        ).count() > 0
    
    @staticmethod
    def get_all_active():
        """Retorna todas as aplicações ativas"""
        return ProductCouponApplication.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_by_coupon(coupon_id):
        """Retorna todas as aplicações de um cupom específico"""
        return ProductCouponApplication.query.filter_by(coupon_id=coupon_id).all()