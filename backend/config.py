import os
from datetime import timedelta

class Config:
    """Configuração base da aplicação"""
    
    # Chave secreta para sessões e CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Configurações do Flask-RESTX (Swagger)
    RESTX_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTX_VALIDATE = True
    RESTX_JSON = {
        'ensure_ascii': False,
        'indent': 2
    }
    
    # Configurações de CORS
    WTF_CSRF_ENABLED = False  # Desabilitar CSRF para API
    
    # Configurações de logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    # Configurações de performance
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento"""
    
    DEBUG = True
    TESTING = False
    
    # Usar SQLite em arquivo para persistir dados durante desenvolvimento
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dev.db')
    
    # Configurações mais verbosas para desenvolvimento
    SQLALCHEMY_ECHO = True  # Log de queries SQL
    
    # Hot reload para templates
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    """Configuração para testes"""
    
    TESTING = True
    DEBUG = False
    
    # Banco em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Desabilitar proteção CSRF nos testes
    WTF_CSRF_ENABLED = False
    
    # Acelerar testes
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    """Configuração para produção"""
    
    DEBUG = False
    TESTING = False
    
    # Banco de dados de produção (deve ser configurado via variável de ambiente)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prod.db')
    
    # Configurações de segurança
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Logging em produção
    SQLALCHEMY_ECHO = False
    
    # Configurações otimizadas para produção
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True,
        'max_overflow': 20
    }

# Dicionário para facilitar a seleção da configuração
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}