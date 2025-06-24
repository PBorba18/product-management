import requests
import json
from datetime import datetime, timedelta

# Configuração
BASE_URL = "http://localhost:5000/api"

def print_response(response, description):
    """Função auxiliar para imprimir respostas"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTE: {description}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_coupon_api():
    """Teste completo da API de cupons"""
    
    print("🚀 INICIANDO TESTES DA API DE CUPONS")
    print("="*60)
    
    # 1. Health Check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Check")
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return
    
    # 2. Criar cupom percentual
    coupon_data = {
        "code": "TESTE20",
        "discount_type": "percentage",
        "discount_value": 20.0,
        "description": "Cupom de teste - 20% de desconto",
        "valid_until": (datetime.now() + timedelta(days=30)).isoformat(),
        "usage_limit": 10,
        "min_purchase_amount": 100.0,
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/coupons", json=coupon_data)
    print_response(response, "Criar Cupom Percentual")
    
    # 3. Criar cupom de valor fixo
    coupon_fixed_data = {
        "code": "GANHE50",
        "discount_type": "fixed",
        "discount_value": 50.0,
        "description": "Cupom de teste - R$ 50 de desconto",
        "valid_until": (datetime.now() + timedelta(days=15)).isoformat(),
        "usage_limit": 5,
        "min_purchase_amount": 200.0,
        "is_active": True
    }
    
    response = requests.post(f"{BASE_URL}/coupons", json=coupon_fixed_data)
    print_response(response, "Criar Cupom Valor Fixo")
    
    # 4. Listar cupons
    response = requests.get(f"{BASE_URL}/coupons")
    print_response(response, "Listar Todos os Cupons")
    
    # 5. Buscar cupom específico
    response = requests.get(f"{BASE_URL}/coupons/TESTE20")
    print_response(response, "Buscar Cupom Específico")
    
    # 6. Validar cupom
    validate_data = {
        "code": "TESTE20",
        "amount": 500.0
    }
    
    response = requests.post(f"{BASE_URL}/coupons/TESTE20/validate", json=validate_data)
    print_response(response, "Validar Cupom")
    
    # 7. Tentar validar com valor insuficiente
    validate_data_low = {
        "code": "TESTE20",
        "amount": 50.0  # Menor que min_purchase_amount
    }
    
    response = requests.post(f"{BASE_URL}/coupons/TESTE20/validate", json=validate_data_low)
    print_response(response, "Validar Cupom - Valor Insuficiente")
    
    # 8. Criar produto para teste (assumindo que existe endpoint)
    product_data = {
        "name": "Produto de Teste",
        "description": "Produto para testar cupons",
        "price": 299.99,
        "category": "Teste",
        "stock_quantity": 100
    }
    
    # Tentar criar produto
    try:
        response = requests.post(f"{BASE_URL}/products", json=product_data)
        print_response(response, "Criar Produto de Teste")
        product_id = response.json().get('product', {}).get('id', 1)
    except:
        print("⚠️  Endpoint de produtos não encontrado, usando ID 1")
        product_id = 1
    
    # 9. Calcular desconto (preview)
    calculate_data = {
        "coupon_code": "TESTE20"
    }
    
    response = requests.post(f"{BASE_URL}/products/{product_id}/calculate-discount", json=calculate_data)
    print_response(response, "Calcular Desconto (Preview)")
    
    # 10. Aplicar cupom no produto
    apply_data = {
        "coupon_code": "TESTE20"
    }
    
    response = requests.post(f"{BASE_URL}/products/{product_id}/apply-coupon", json=apply_data)
    print_response(response, "Aplicar Cupom no Produto")
    
    # 11. Histórico do cupom
    response = requests.get(f"{BASE_URL}/coupons/TESTE20/usage-history")
    print_response(response, "Histórico de Uso do Cupom")
    
    # 12. Histórico do produto
    response = requests.get(f"{BASE_URL}/products/{product_id}/coupon-history")
    print_response(response, "Histórico de Cupons do Produto")
    
    # 13. Aplicar cupom em múltiplos produtos
    batch_data = {
        "coupon_code": "GANHE50",
        "product_ids": [product_id, product_id + 1, product_id + 2]
    }
    
    response = requests.post(f"{BASE_URL}/products/apply-coupon-batch", json=batch_data)
    print_response(response, "Aplicar Cupom em Múltiplos Produtos")
    
    # 14. Atualizar cupom
    update_data = {
        "description": "Cupom atualizado via API",
        "is_active": True
    }
    
    response = requests.put(f"{BASE_URL}/coupons/TESTE20", json=update_data)
    print_response(response, "Atualizar Cupom")
    
    # 15. Tentar criar cupom com código duplicado
    duplicate_coupon = {
        "code": "TESTE20",  # Código já existe
        "discount_type": "percentage",
        "discount_value": 10.0,
        "valid_until": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/coupons", json=duplicate_coupon)
    print_response(response, "Tentar Criar Cupom Duplicado")
    
    # 16. Listar rotas disponíveis
    response = requests.get(f"{BASE_URL}/routes")
    print_response(response, "Listar Rotas Disponíveis")
    
    # 17. Desativar cupom
    response = requests.delete(f"{BASE_URL}/coupons/GANHE50")
    print_response(response, "Desativar Cupom")
    
    # 18. Listar cupons com filtro
    response = requests.get(f"{BASE_URL}/coupons?is_active=true&discount_type=percentage")
    print_response(response, "Listar Cupons Filtrados")
    
    print("\n🎉 TESTES CONCLUÍDOS!")
    print("="*60)

def test_error_scenarios():
    """Testar cenários de erro"""
    
    print("\n🚨 TESTANDO CENÁRIOS DE ERRO")
    print("="*60)
    
    # 1. Cupom não encontrado
    response = requests.get(f"{BASE_URL}/coupons/NAOEXISTE")
    print_response(response, "Cupom Não Encontrado")
    
    # 2. Dados inválidos para criação
    invalid_data = {
        "code": "",  # Código vazio
        "discount_type": "invalid",  # Tipo inválido
        "discount_value": -10  # Valor negativo
    }
    
    response = requests.post(f"{BASE_URL}/coupons", json=invalid_data)
    print_response(response, "Dados Inválidos para Criação")
    
    # 3. Desconto percentual inválido
    invalid_percentage = {
        "code": "INVALID",
        "discount_type": "percentage",
        "discount_value": 150,  # Maior que 100%
        "valid_until": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/coupons", json=invalid_percentage)
    print_response(response, "Desconto Percentual Inválido")
    
    # 4. Data inválida
    invalid_date = {
        "code": "DATETEST",
        "discount_type": "percentage",
        "discount_value": 10,
        "valid_until": "data-invalida"
    }
    
    response = requests.post(f"{BASE_URL}/coupons", json=invalid_date)
    print_response(response, "Data Inválida")

if __name__ == "__main__":
    print("🔧 CONFIGURAÇÃO")
    print(f"Base URL: {BASE_URL}")
    print("Certifique-se de que o servidor Flask está rodando!")
    
    input("\nPressione ENTER para iniciar os testes...")
    
    try:
        test_coupon_api()
        test_error_scenarios()
    except KeyboardInterrupt:
        print("\n\n❌ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n\n💥 Erro durante os testes: {e}")
    
    print("\n👋 Fim dos testes!")