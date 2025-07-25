from app import create_app
# Importa a configuração de desenvolvimento para definir variáveis específicas do ambiente
from config import DevelopmentConfig
import os

# Criar aplicação
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    # Configurações de desenvolvimento
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
    Product Management API iniciando...
    
    
    
    
          Endpoints disponíveis:
    • API Base: http://localhost:{port}/api/
    • Swagger UI: http://localhost:{port}/api/docs/
    • Health Check: http://localhost:{port}/api/health/
    
    Recursos:
    • Produtos: /api/products/
    • Cupons: /api/coupons/
    """)
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port,
        threaded=True
    )