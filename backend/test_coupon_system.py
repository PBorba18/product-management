# test_coupon_system.py
# Arquivo para testar o sistema de cupons

from app import create_app, db
from app.models.product import Product
from app.models.coupon import Coupon
from app.models.product_coupon_application import ProductCouponApplication
from datetime import datetime, timedelta

def test_coupon_system():
    """Teste completo do sistema de cupons"""
    
    # Configuração do app para teste
    app = create_app('config.DevelopmentConfig')  # ou sua classe de config
    
    with app.app_context():
        # 1. Criar produtos de teste
        print("=== Criando produtos de teste ===")
        
        produto1 = Product(
            name="Smartphone Samsung",
            description="Smartphone Galaxy A54",
            price=1299.99,
            category="Eletrônicos",
            stock_quantity=50
        )
        
        produto2 = Product(
            name="Notebook Dell",
            description="Notebook Inspiron 15",
            price=2499.99,
            category="Informática",
            stock_quantity=20
        )
        
        db.session.add(produto1)
        db.session.add(produto2)
        db.session.commit()
        
        print(f"✓ Produto 1 criado: {produto1.name} - R$ {produto1.price}")
        print(f"✓ Produto 2 criado: {produto2.name} - R$ {produto2.price}")
        
        # 2. Criar cupons de teste
        print("\n=== Criando cupons de teste ===")
        
        # Cupom percentual
        cupom_percent = Coupon(
            code="DESCONTO20",
            discount_type="percentage",
            discount_value=20.0,
            valid_from=datetime.now(),
            valid_until=datetime.now() + timedelta(days=30),
            usage_limit=100,
            min_purchase_amount=100.0,
            is_active=True
        )
        
        # Cupom valor fixo
        cupom_fixed = Coupon(
            code="GANHE50",
            discount_type="fixed",
            discount_value=50.0,
            valid_from=datetime.now(),
            valid_until=datetime.now() + timedelta(days=15),
            usage_limit=50,
            min_purchase_amount=200.0,
            is_active=True
        )
        
        db.session.add(cupom_percent)
        db.session.add(cupom_fixed)
        db.session.commit()
        
        print(f"✓ Cupom criado: {cupom_percent.code} - {cupom_percent.discount_value}% desconto")
        print(f"✓ Cupom criado: {cupom_fixed.code} - R$ {cupom_fixed.discount_value} desconto")
        
        # 3. Testar aplicação de cupons
        print("\n=== Testando aplicação de cupons ===")
        
        # Teste 1: Aplicar cupom percentual no produto 1
        print(f"\nTeste 1: Aplicar {cupom_percent.code} em {produto1.name}")
        print(f"Preço original: R$ {produto1.price}")
        
        if cupom_percent.can_be_applied_to_amount(produto1.price):
            discount_amount = cupom_percent.calculate_discount(produto1.price)
            final_price = produto1.price - discount_amount
            
            print(f"Desconto aplicado: R$ {discount_amount:.2f}")
            print(f"Preço final: R$ {final_price:.2f}")
            
            # Registrar aplicação do cupom
            application = ProductCouponApplication(
                product_id=produto1.id,
                coupon_id=cupom_percent.id,
                original_price=produto1.price,
                discount_amount=discount_amount,
                final_price=final_price
            )
            db.session.add(application)
            
            # Atualizar uso do cupom
            cupom_percent.times_used += 1
            print("✓ Cupom aplicado com sucesso!")
        else:
            print("✗ Cupom não pode ser aplicado")
        
        # Teste 2: Aplicar cupom fixo no produto 2
        print(f"\nTeste 2: Aplicar {cupom_fixed.code} em {produto2.name}")
        print(f"Preço original: R$ {produto2.price}")
        
        if cupom_fixed.can_be_applied_to_amount(produto2.price):
            discount_amount = cupom_fixed.calculate_discount(produto2.price)
            final_price = produto2.price - discount_amount
            
            print(f"Desconto aplicado: R$ {discount_amount:.2f}")
            print(f"Preço final: R$ {final_price:.2f}")
            
            # Registrar aplicação do cupom
            application = ProductCouponApplication(
                product_id=produto2.id,
                coupon_id=cupom_fixed.id,
                original_price=produto2.price,
                discount_amount=discount_amount,
                final_price=final_price
            )
            db.session.add(application)
            
            # Atualizar uso do cupom
            cupom_fixed.times_used += 1
            print("✓ Cupom aplicado com sucesso!")
        else:
            print("✗ Cupom não pode ser aplicado")
        
        db.session.commit()
        
        # 4. Verificar histórico de aplicações
        print("\n=== Histórico de aplicações ===")
        
        applications = ProductCouponApplication.query.all()
        for app in applications:
            print(f"Produto: {app.product.name}")
            print(f"Cupom: {app.coupon.code}")
            print(f"Desconto: R$ {app.discount_amount:.2f}")
            print(f"Preço final: R$ {app.final_price:.2f}")
            print(f"Data: {app.applied_at}")
            print("-" * 40)
        
        # 5. Verificar status dos cupons
        print("\n=== Status dos cupons ===")
        
        cupons = Coupon.query.all()
        for cupom in cupons:
            print(f"Cupom: {cupom.code}")
            print(f"Usado: {cupom.times_used}/{cupom.usage_limit} vezes")
            print(f"Status: {'Ativo' if cupom.is_active else 'Inativo'}")
            print(f"Válido até: {cupom.valid_until}")
            print("-" * 40)
        
        print("\n🎉 Teste concluído com sucesso!")

if __name__ == "__main__":
    test_coupon_system()