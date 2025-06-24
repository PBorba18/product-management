# Importações dos modelos
try:
    from .product import Product
except ImportError as e:
    print(f"Erro ao importar Product: {e}")
    Product = None

try:
    from .coupon import Coupon
except ImportError as e:
    print(f"Erro ao importar Coupon: {e}")
    Coupon = None

try:
    from .product_coupon_application import ProductCouponApplication
except ImportError as e:
    print(f"Erro ao importar ProductCouponApplication: {e}")
    ProductCouponApplication = None

# Exportar apenas os modelos que foram importados com sucesso
__all__ = []

if Product:
    __all__.append('Product')
if Coupon:
    __all__.append('Coupon')
if ProductCouponApplication:
    __all__.append('ProductCouponApplication')