import pandas as pd
import numpy as np
from datetime import datetime
import os

class SimpleDataPipeline:
    def __init__(self):
        self.data_path = "../datasets/sales_data.csv"
        
    def run_pipeline(self):
        """Executa pipeline simplificado usando apenas pandas"""
        print("=== Iniciando Pipeline Simplificado ===")
        
        # 1. Ingestão de dados
        print("1. Carregando dados...")
        df = pd.read_csv(self.data_path)
        print(f"   Dados carregados: {len(df)} registros")
        
        # 2. Limpeza básica (Bronze)
        print("2. Processando camada Bronze...")
        df_bronze = df[
            (df['total_amount'] > 0) & 
            (df['quantity'] > 0)
        ].copy()
        df_bronze['processed_at'] = datetime.now()
        print(f"   Registros após limpeza: {len(df_bronze)}")
        
        # 3. Agregações (Silver)
        print("3. Processando camada Silver...")
        
        # Vendas por categoria
        sales_by_category = df_bronze.groupby('category').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'price': 'mean',
            'order_id': 'count'
        }).round(2)
        
        # Métricas de clientes
        customer_metrics = df_bronze.groupby('customer_segment').agg({
            'customer_id': 'nunique',
            'total_amount': ['mean', 'sum']
        }).round(2)
        
        # Performance de produtos
        product_performance = df_bronze.groupby(['product_name', 'category']).agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'rating': 'mean'
        }).round(2)
        
        # 4. KPIs principais (Gold)
        print("4. Processando camada Gold...")
        
        # Top 10 produtos por receita
        top_products = product_performance.sort_values('total_amount', ascending=False).head(10)
        
        # Estatísticas gerais
        total_revenue = df_bronze['total_amount'].sum()
        total_orders = len(df_bronze)
        avg_order_value = df_bronze['total_amount'].mean()
        unique_customers = df_bronze['customer_id'].nunique()
        
        # 5. Exibir resultados
        print("\n=== RESULTADOS DO PIPELINE ===")
        print(f"Total de Receita: R$ {total_revenue:,.2f}")
        print(f"Total de Pedidos: {total_orders:,}")
        print(f"Valor Medio por Pedido: R$ {avg_order_value:.2f}")
        print(f"Clientes Unicos: {unique_customers:,}")
        
        print("\nVENDAS POR CATEGORIA:")
        print(sales_by_category.to_string())
        
        print("\nMETRICAS POR SEGMENTO:")
        print(customer_metrics.to_string())
        
        print("\nTOP 5 PRODUTOS POR RECEITA:")
        print(top_products.head().to_string())
        
        # 6. Salvar resultados
        print("\n6. Salvando resultados...")
        
        # Criar diretório de saída se não existir
        output_dir = "../output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Salvar CSVs
        sales_by_category.to_csv(f"{output_dir}/sales_by_category.csv")
        customer_metrics.to_csv(f"{output_dir}/customer_metrics.csv")
        product_performance.to_csv(f"{output_dir}/product_performance.csv")
        top_products.to_csv(f"{output_dir}/top_products.csv")
        
        print(f"   Resultados salvos em: {output_dir}/")
        
        print("\n=== Pipeline executado com sucesso! ===")
        
        return {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'avg_order_value': avg_order_value,
            'unique_customers': unique_customers,
            'sales_by_category': sales_by_category,
            'customer_metrics': customer_metrics,
            'top_products': top_products
        }

if __name__ == "__main__":
    # Executar pipeline simplificado
    pipeline = SimpleDataPipeline()
    results = pipeline.run_pipeline()