from app.api.products.routes import products_ns

def register_blueprints(api):
    """Registra todos os blueprints na API"""

    # Importar e registrar blueprint de produtos
    from app.api.products.routes import products_ns
    api.add_namespace(products_ns, path='/products')

    # Importar e registrar blueprint de cupons
    from app.api.coupons.routes import coupons_ns
    api.add_namespace(coupons_ns, path='/coupons')

    # Blueprint para health check
    from app.api.common.routes import common_ns
    api.add_namespace(common_ns, path='/health')
