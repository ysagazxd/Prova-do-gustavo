import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data():
    """Gera dados sintéticos de vendas para demonstração"""
    
    # Configurações
    n_records = 10000
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Listas de dados
    categories = ['Eletrônicos', 'Roupas', 'Casa', 'Livros', 'Esportes', 'Beleza']
    products = {
        'Eletrônicos': ['Smartphone', 'Laptop', 'Tablet', 'Fone de Ouvido', 'Smart TV'],
        'Roupas': ['Camiseta', 'Calça Jeans', 'Vestido', 'Tênis', 'Jaqueta'],
        'Casa': ['Sofá', 'Mesa', 'Cadeira', 'Luminária', 'Tapete'],
        'Livros': ['Romance', 'Ficção Científica', 'Biografia', 'Técnico', 'Infantil'],
        'Esportes': ['Bola de Futebol', 'Raquete', 'Bicicleta', 'Tênis Esportivo', 'Equipamento Gym'],
        'Beleza': ['Perfume', 'Maquiagem', 'Creme', 'Shampoo', 'Protetor Solar']
    }
    
    customer_segments = ['Premium', 'Regular', 'Básico']
    
    # Geração dos dados
    data = []
    
    for _ in range(n_records):
        category = random.choice(categories)
        product = random.choice(products[category])
        
        # Preços baseados na categoria
        price_ranges = {
            'Eletrônicos': (200, 3000),
            'Roupas': (30, 300),
            'Casa': (100, 2000),
            'Livros': (15, 80),
            'Esportes': (50, 500),
            'Beleza': (20, 200)
        }
        
        min_price, max_price = price_ranges[category]
        price = round(random.uniform(min_price, max_price), 2)
        quantity = random.randint(1, 5)
        
        # Data aleatória
        random_days = random.randint(0, (end_date - start_date).days)
        sale_date = start_date + timedelta(days=random_days)
        
        # Customer ID e segmento
        customer_id = random.randint(1, 2000)
        segment = random.choice(customer_segments)
        
        # Rating
        rating = round(random.uniform(3.0, 5.0), 1)
        
        data.append({
            'order_id': f'ORD_{_+1:06d}',
            'customer_id': customer_id,
            'customer_segment': segment,
            'product_name': product,
            'category': category,
            'price': price,
            'quantity': quantity,
            'total_amount': price * quantity,
            'sale_date': sale_date.strftime('%Y-%m-%d'),
            'rating': rating
        })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Gerar dados
    sales_df = generate_sales_data()
    
    # Salvar em CSV
    sales_df.to_csv('datasets/sales_data.csv', index=False)
    print(f"Dados gerados: {len(sales_df)} registros salvos em datasets/sales_data.csv")
    
    # Mostrar estatísticas básicas
    print("\nEstatísticas dos dados gerados:")
    print(f"Período: {sales_df['sale_date'].min()} a {sales_df['sale_date'].max()}")
    print(f"Total de vendas: R$ {sales_df['total_amount'].sum():,.2f}")
    print(f"Categorias: {sales_df['category'].nunique()}")
    print(f"Produtos únicos: {sales_df['product_name'].nunique()}")
    print(f"Clientes únicos: {sales_df['customer_id'].nunique()}")