from datetime import datetime
import logging
from sqlalchemy import and_
from datetime import datetime, timezone
import pytz

try:
    from app.models.coupon import Coupon
except ImportError:
    from models.coupon import Coupon

try:
    from app.database import db
except ImportError:
    try:
        from app import db
    except ImportError:
        from database import db

class CouponService:
    """Serviço para gerenciamento de cupons (implementação real)"""

    

    @staticmethod
    def list_coupons(filters=None):
        if filters is None:
            filters = {}

        try:
            query = Coupon.query.filter(Coupon.is_active == True)

            if filters.get('search'):
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    Coupon.code.ilike(search_term) |
                    Coupon.description.ilike(search_term)
                )

            if filters.get('min_discount'):
                query = query.filter(Coupon.discount_percentage >= filters['min_discount'])

            if filters.get('max_discount'):
                query = query.filter(Coupon.discount_percentage <= filters['max_discount'])

            if filters.get('is_valid') is not None:
                now = datetime.utcnow()
                if filters['is_valid']:
                    query = query.filter(
                        and_(
                            Coupon.valid_from <= now,
                            Coupon.valid_until >= now,
                            Coupon.usage_count < Coupon.usage_limit
                        )
                    )
                else:
                    query = query.filter(
                        (Coupon.valid_from > now) |
                        (Coupon.valid_until < now) |
                        (Coupon.usage_count >= Coupon.usage_limit)
                    )

            sort_by = filters.get('sort_by', 'created_at')
            sort_order = filters.get('sort_order', 'desc')

            if hasattr(Coupon, sort_by):
                order_column = getattr(Coupon, sort_by)
                query = query.order_by(order_column.desc() if sort_order == 'desc' else order_column.asc())

            page = max(filters.get('page', 1), 1)
            limit = min(max(filters.get('limit', 10), 1), 50)

            paginated = query.paginate(page=page, per_page=limit, error_out=False)

            coupons = [CouponService._serialize_coupon(c) for c in paginated.items]

            return {
                'coupons': coupons,
                'meta': {
                    'page': page,
                    'pages': paginated.pages,
                    'per_page': limit,
                    'total': paginated.total,
                    'has_next': paginated.has_next,
                    'has_prev': paginated.has_prev
                }
            }

        except Exception as e:
            logging.error(f"Erro ao listar cupons: {str(e)}")
            raise

    @staticmethod
    def get_coupon_by_id(coupon_id):
        try:
            coupon = Coupon.query.filter(Coupon.id == coupon_id, Coupon.is_active == True).first()
            return CouponService._serialize_coupon(coupon) if coupon else None
        except Exception as e:
            logging.error(f"Erro ao buscar cupom {coupon_id}: {str(e)}")
            raise

    @staticmethod
    def get_coupon_by_code(code):
        try:
            coupon = Coupon.query.filter(Coupon.code == code.upper(), Coupon.is_active == True).first()
            return CouponService._serialize_coupon(coupon) if coupon else None
        except Exception as e:
            logging.error(f"Erro ao buscar cupom por código {code}: {str(e)}")
            raise

    @staticmethod
    def create_coupon(data):
        try:
            existing = Coupon.query.filter(Coupon.code == data['code'].upper(), Coupon.is_active == True).first()
            if existing:
                raise ValueError(f"Cupom com código '{data['code']}' já existe")

            # Corrigir parsing de datas para garantir timezone
            def parse_datetime(date_str):
                # Remove 'Z' e adiciona timezone UTC explicitamente
                if date_str.endswith('Z'):
                    date_str = date_str[:-1] + '+00:00'
                dt = datetime.fromisoformat(date_str)
                # Se não tem timezone, assume UTC
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt

            valid_from = parse_datetime(data['valid_from'])
            valid_until = parse_datetime(data['valid_until'])

            if valid_from >= valid_until:
                raise ValueError("Data de início deve ser anterior à data de fim")
        
            # Comparar com datetime com timezone
            now = datetime.now(timezone.utc)
            if valid_until <= now:
                raise ValueError("Data de fim deve ser futura")

            coupon = Coupon(
                code=data['code'].upper(),
                description=data.get('description', ''),
                discount_percentage=data['discount_percentage'],
                valid_from=valid_from,
                valid_until=valid_until,
                usage_limit=data.get('usage_limit', 1),
                usage_count=0,
                is_active=True
            )

            db.session.add(coupon)
            db.session.commit()
            logging.info(f"Cupom criado: {coupon.code}")
            return CouponService._serialize_coupon(coupon)

        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao criar cupom: {str(e)}")
            raise

    @staticmethod
    def update_coupon(coupon_id, data):
        try:
            coupon = Coupon.query.filter(Coupon.id == coupon_id, Coupon.is_active == True).first()
            if not coupon:
                return None

            if 'code' in data and data['code'].upper() != coupon.code:
                existing = Coupon.query.filter(
                    Coupon.code == data['code'].upper(),
                    Coupon.is_active == True,
                    Coupon.id != coupon_id
                ).first()
                if existing:
                    raise ValueError(f"Cupom com código '{data['code']}' já existe")
                coupon.code = data['code'].upper()

            if 'description' in data:
                coupon.description = data['description']

            if 'discount_percentage' in data:
                coupon.discount_percentage = data['discount_percentage']

            if 'valid_from' in data:
                valid_from = datetime.fromisoformat(data['valid_from'].replace('Z', '+00:00'))
                if valid_from >= coupon.valid_until:
                    raise ValueError("Data de início deve ser anterior à data de fim")
                coupon.valid_from = valid_from

            if 'valid_until' in data:
                valid_until = datetime.fromisoformat(data['valid_until'].replace('Z', '+00:00'))
                if valid_until <= coupon.valid_from:
                    raise ValueError("Data de fim deve ser posterior à data de início")
                coupon.valid_until = valid_until

            if 'usage_limit' in data:
                if data['usage_limit'] < coupon.usage_count:
                    raise ValueError("Limite de uso não pode ser menor que o uso atual")
                coupon.usage_limit = data['usage_limit']

            coupon.updated_at = datetime.utcnow()
            db.session.commit()
            logging.info(f"Cupom atualizado: {coupon.code}")
            return CouponService._serialize_coupon(coupon)

        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao atualizar cupom {coupon_id}: {str(e)}")
            raise

    @staticmethod
    def delete_coupon(coupon_id):
        try:
            coupon = Coupon.query.filter(Coupon.id == coupon_id, Coupon.is_active == True).first()
            if not coupon:
                return False
            coupon.is_active = False
            coupon.updated_at = datetime.utcnow()
            db.session.commit()
            logging.info(f"Cupom inativado: {coupon.code}")
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao deletar cupom {coupon_id}: {str(e)}")
            raise

    @staticmethod
    def validate_coupon(code):
        try:
            coupon = Coupon.query.filter(Coupon.code == code.upper(), Coupon.is_active == True).first()
            if not coupon:
                return {'valid': False, 'message': 'Cupom não encontrado', 'coupon': None}

            # Garantir timezone nas comparações
            now = datetime.now(timezone.utc)
            
            def make_aware(dt):
                if dt.tzinfo is None:
                    return dt.replace(tzinfo=timezone.utc)
                return dt
            
            valid_from = make_aware(coupon.valid_from)
            valid_until = make_aware(coupon.valid_until)
            
            if now < valid_from:
                return {'valid': False, 'message': 'Cupom ainda não é válido', 'coupon': CouponService._serialize_coupon(coupon)}
            if now > valid_until:
                return {'valid': False, 'message': 'Cupom expirado', 'coupon': CouponService._serialize_coupon(coupon)}
            if coupon.usage_count >= coupon.usage_limit:
                return {'valid': False, 'message': 'Cupom atingiu limite de uso', 'coupon': CouponService._serialize_coupon(coupon)}

            return {'valid': True, 'message': 'Cupom válido', 'coupon': CouponService._serialize_coupon(coupon)}

        except Exception as e:
            logging.error(f"Erro ao validar cupom {code}: {str(e)}")
            raise

    @staticmethod
    def use_coupon(code):
        try:
            coupon = Coupon.query.filter(Coupon.code == code.upper(), Coupon.is_active == True).first()
            if not coupon:
                raise ValueError("Cupom não encontrado")

            validation = CouponService.validate_coupon(code)
            if not validation['valid']:
                raise ValueError(validation['message'])

            coupon.usage_count += 1
            coupon.updated_at = datetime.utcnow()
            db.session.commit()
            logging.info(f"Cupom usado: {coupon.code} (uso {coupon.usage_count}/{coupon.usage_limit})")
            return CouponService._serialize_coupon(coupon)

        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao usar cupom {code}: {str(e)}")
            raise

    @staticmethod
    def _serialize_coupon(coupon):
        now = datetime.utcnow()
        is_valid = (coupon.is_active and coupon.valid_from <= now <= coupon.valid_until and coupon.usage_count < coupon.usage_limit)
        return {
            'id': coupon.id,
            'code': coupon.code,
            'description': coupon.description,
            'discount_percentage': coupon.discount_percentage,
            'valid_from': coupon.valid_from.isoformat() + 'Z',
            'valid_until': coupon.valid_until.isoformat() + 'Z',
            'usage_limit': coupon.usage_limit,
            'usage_count': coupon.usage_count,
            'is_active': coupon.is_active,
            'is_valid': is_valid,
            'is_expired': now > coupon.valid_until,
            'is_not_started': now < coupon.valid_from,
            'is_limit_reached': coupon.usage_count >= coupon.usage_limit,
            'remaining_uses': max(0, coupon.usage_limit - coupon.usage_count),
            'created_at': coupon.created_at.isoformat() + 'Z',
            'updated_at': coupon.updated_at.isoformat() + 'Z' if coupon.updated_at else None
        }
    
        
          