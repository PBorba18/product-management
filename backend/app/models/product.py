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

class Product(db.Model):
    """Modelo para produtos"""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.String(300))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Campos para desconto
    discount_percentage = db.Column(db.Float, default=0.0)
    discount_start_date = db.Column(db.DateTime)
    discount_end_date = db.Column(db.DateTime)
    has_active_discount = db.Column(db.Boolean, default=False)
    
    # Índices para otimização
    __table_args__ = (
        db.Index('idx_product_name_active', 'name', 'is_active'),
        db.Index('idx_product_price', 'price'),
        db.Index('idx_product_stock', 'stock'),
        db.Index('idx_product_active', 'is_active'),
        db.Index('idx_product_discount', 'has_active_discount'),
    )
    
    def __init__(self, name, price, stock=0, description=''):
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.is_active = True
        self.discount_percentage = 0.0
        self.has_active_discount = False
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    @property
    def final_price(self):
        """Calcula o preço final com desconto"""
        if self.has_active_discount and self.discount_percentage > 0:
            discount_amount = self.price * (self.discount_percentage / 100)
            return round(self.price - discount_amount, 2)
        return self.price
    
    @property
    def is_out_of_stock(self):
        """Verifica se está sem estoque"""
        return self.stock <= 0
    
    @property
    def discount_amount(self):
        """Calcula o valor do desconto"""
        if self.has_active_discount and self.discount_percentage > 0:
            return round(self.price * (self.discount_percentage / 100), 2)
        return 0.0
    
    def apply_percentage_discount(self, percentage):
        """Aplica desconto percentual"""
        if not 1 <= percentage <= 80:
            raise ValueError("Percentual deve estar entre 1% e 80%")
        
        self.discount_percentage = percentage
        self.has_active_discount = True
        self.discount_start_date = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def remove_discount(self):
        """Remove desconto ativo"""
        self.discount_percentage = 0.0
        self.has_active_discount = False
        self.discount_start_date = None
        self.discount_end_date = None
        self.updated_at = datetime.utcnow()
    
    def update_stock(self, quantity):
        """Atualiza estoque"""
        self.stock = max(0, quantity)
        self.updated_at = datetime.utcnow()
    
    def add_stock(self, quantity):
        """Adiciona ao estoque"""
        if quantity > 0:
            self.stock += quantity
            self.updated_at = datetime.utcnow()
    
    def reduce_stock(self, quantity):
        """Reduz do estoque"""
        if quantity > 0:
            self.stock = max(0, self.stock - quantity)
            self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Inativa o produto (soft delete)"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self):
        """Ativa o produto"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_discount_info=True):
        """Converte para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'finalPrice': self.final_price,
            'isOutOfStock': self.is_out_of_stock,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
        
        if include_discount_info:
            discount_info = None
            if self.has_active_discount:
                discount_info = {
                    'percentage': self.discount_percentage,
                    'amount': self.discount_amount,
                    'start_date': self.discount_start_date.isoformat() + 'Z' if self.discount_start_date else None,
                    'end_date': self.discount_end_date.isoformat() + 'Z' if self.discount_end_date else None
                }
            
            data.update({
                'discount': discount_info,
                'hasCouponApplied': False  # Será atualizado pelo service se houver cupom
            })
        
        return data