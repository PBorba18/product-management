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

class Coupon(db.Model):
    """Modelo para cupons de desconto"""
    
    __tablename__ = 'coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200))
    discount_percentage = db.Column(db.Float, nullable=False)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, nullable=False, default=1)
    usage_count = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Índices para otimização
    __table_args__ = (
        db.Index('idx_coupon_code_active', 'code', 'is_active'),
        db.Index('idx_coupon_validity', 'valid_from', 'valid_until'),
        db.Index('idx_coupon_active', 'is_active'),
    )
    
    def __init__(self, code, discount_percentage, valid_from, valid_until, 
                 description='', usage_limit=1, usage_count=0, is_active=True):
        self.code = code.upper()
        self.description = description
        self.discount_percentage = discount_percentage
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.usage_limit = usage_limit
        self.usage_count = usage_count
        self.is_active = is_active
    
    def __repr__(self):
        return f'<Coupon {self.code}>'
    
    @property
    def is_valid(self):
        """Verifica se o cupom está válido"""
        now = datetime.utcnow()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            self.usage_count < self.usage_limit
        )
    
    @property
    def is_expired(self):
        """Verifica se o cupom expirou"""
        return datetime.utcnow() > self.valid_until
    
    @property
    def is_not_started(self):
        """Verifica se o cupom ainda não iniciou"""
        return datetime.utcnow() < self.valid_from
    
    @property
    def is_limit_reached(self):
        """Verifica se atingiu o limite de uso"""
        return self.usage_count >= self.usage_limit
    
    @property
    def remaining_uses(self):
        """Retorna usos restantes"""
        return max(0, self.usage_limit - self.usage_count)
    
    def can_be_used(self):
        """Verifica se pode ser usado e retorna motivo se não puder"""
        if not self.is_active:
            return False, "Cupom inativo"
        
        now = datetime.utcnow()
        
        if now < self.valid_from:
            return False, "Cupom ainda não é válido"
        
        if now > self.valid_until:
            return False, "Cupom expirado"
        
        if self.usage_count >= self.usage_limit:
            return False, "Limite de uso atingido"
        
        return True, "Cupom válido"
    
    def use(self):
        """Incrementa o uso do cupom"""
        can_use, message = self.can_be_used()
        if not can_use:
            raise ValueError(message)
        
        self.usage_count += 1
        self.updated_at = datetime.utcnow()
    
    def to_dict(self, include_validity=True):
        """Converte para dicionário"""
        data = {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'discount_percentage': self.discount_percentage,
            'valid_from': self.valid_from.isoformat() + 'Z',
            'valid_until': self.valid_until.isoformat() + 'Z',
            'usage_limit': self.usage_limit,
            'usage_count': self.usage_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }
        
        if include_validity:
            data.update({
                'is_valid': self.is_valid,
                'is_expired': self.is_expired,
                'is_not_started': self.is_not_started,
                'is_limit_reached': self.is_limit_reached,
                'remaining_uses': self.remaining_uses
            })
        
        return data