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
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.id'), nullable=False)
    discount_amount = db.Column(db.Float, nullable=False)
    applied_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relacionamentos
    product = db.relationship('Product', backref='coupon_applications', lazy=True)
    coupon = db.relationship('Coupon', backref='product_applications', lazy=True)
    
    # Índices para otimização
    __table_args__ = (
        db.Index('idx_product_coupon_active', 'product_id', 'is_active'),
        db.Index('idx_coupon_product_active', 'coupon_id', 'is_active'),
        db.UniqueConstraint('product_id', 'coupon_id', name='unique_product_coupon_active'),
    )
    
    def __init__(self, product_id, coupon_id, discount_amount):
        self.product_id = product_id
        self.coupon_id = coupon_id
        self.discount_amount = discount_amount
        self.is_active = True
    
    def __repr__(self):
        return f'<ProductCouponApplication Product:{self.product_id} Coupon:{self.coupon_id}>'
    
    def deactivate(self):
        """Desativa a aplicação do cupom"""
        self.is_active = False
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'coupon_id': self.coupon_id,
            'discount_amount': self.discount_amount,
            'applied_at': self.applied_at.isoformat() + 'Z',
            'is_active': self.is_active
        }