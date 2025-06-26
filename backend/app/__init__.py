from flask import Flask
from flask_cors import CORS
from flask_restx import Api
import logging
from app.database import db, migrate

def create_app(config_class=None):
    """Factory pattern para criar a aplicação Flask"""
    
    app = Flask(__name__)
    
    # Carregar configuração
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object('config.DevelopmentConfig')
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar CORS para liberar o Vite (5173), React (3000) e variações localhost
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://localhost:3000",
                "http://127.0.0.1:5173",
                "http://127.0.0.1:3000"
            ],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configurar logging
    if not app.debug and not app.testing:
        logging.basicConfig(level=logging.INFO)
    
    # Configurar API com Swagger
    api = Api(
        app,
        version='1.0',
        title='Product Management API',
        description='API para gerenciamento de produtos com sistema de descontos',
        doc='/api/docs/',  # URL da documentação Swagger
        prefix='/api'
    )
    
    # Registrar blueprints (ou namespaces) - ajuste para sua estrutura real!
    from app.api import register_blueprints
    register_blueprints(api)
    
    # Importar modelos (importante para migrations)
    from app.models import product, coupon, product_coupon_application
    
    # Criar tabelas no contexto da aplicação (opcional, só para dev/teste)
    with app.app_context():
        db.create_all()
    
    # Handler de erro global
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Recurso não encontrado'}, 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return {'message': 'Erro interno do servidor'}, 500
    
    return app
