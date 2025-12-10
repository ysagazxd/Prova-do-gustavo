import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import boto3
from botocore.exceptions import ClientError
import psycopg2
from datetime import datetime
import os

class DataPipeline:
    def __init__(self):
        self.spark = self._create_spark_session()
        self.minio_client = self._create_minio_client()
        
    def _create_spark_session(self):
        """Cria sessão Spark com configurações para MinIO"""
        return SparkSession.builder \
            .appName("SalesDataPipeline") \
            .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
            .config("spark.hadoop.fs.s3a.access.key", "admin") \
            .config("spark.hadoop.fs.s3a.secret.key", "password123") \
            .config("spark.hadoop.fs.s3a.path.style.access", "true") \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .getOrCreate()
    
    def _create_minio_client(self):
        """Cria cliente MinIO"""
        return boto3.client(
            's3',
            endpoint_url='http://localhost:9000',
            aws_access_key_id='admin',
            aws_secret_access_key='password123'
        )
    
    def create_buckets(self):
        """Cria buckets no MinIO para as camadas do Data Lake"""
        buckets = ['raw-data', 'bronze-data', 'silver-data', 'gold-data']
        
        for bucket in buckets:
            try:
                self.minio_client.create_bucket(Bucket=bucket)
                print(f"Bucket '{bucket}' criado com sucesso")
            except ClientError as e:
                if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                    print(f"Bucket '{bucket}' já existe")
                else:
                    print(f"Erro ao criar bucket '{bucket}': {e}")
    
    def ingest_raw_data(self, csv_path):
        """Camada RAW: Ingestão dos dados brutos"""
        print("Iniciando ingestão de dados...")
        
        # Ler CSV com Pandas primeiro para validação
        df_pandas = pd.read_csv(csv_path)
        print(f"Dados carregados: {len(df_pandas)} registros")
        
        # Carregar no Spark
        df_spark = self.spark.read.csv(csv_path, header=True, inferSchema=True)
        
        # Salvar na camada RAW (formato original)
        df_spark.write.mode("overwrite").parquet("s3a://raw-data/sales/")
        print("Dados salvos na camada RAW")
        
        return df_spark
    
    def process_bronze_layer(self, df_raw):
        """Camada BRONZE: Limpeza e padronização básica"""
        print("Processando camada Bronze...")
        
        df_bronze = df_raw \
            .filter(col("total_amount") > 0) \
            .filter(col("quantity") > 0) \
            .withColumn("sale_date", to_date(col("sale_date"), "yyyy-MM-dd")) \
            .withColumn("processed_at", current_timestamp())
        
        # Salvar na camada Bronze
        df_bronze.write.mode("overwrite").parquet("s3a://bronze-data/sales/")
        print("Dados processados na camada Bronze")
        
        return df_bronze
    
    def process_silver_layer(self, df_bronze):
        """Camada SILVER: Transformações e agregações"""
        print("Processando camada Silver...")
        
        # Agregações por categoria e data
        sales_by_category = df_bronze.groupBy("category", "sale_date") \
            .agg(
                sum("total_amount").alias("total_sales"),
                sum("quantity").alias("total_quantity"),
                avg("price").alias("avg_price"),
                count("order_id").alias("order_count")
            )
        
        # Métricas de clientes
        customer_metrics = df_bronze.groupBy("customer_segment") \
            .agg(
                countDistinct("customer_id").alias("total_customers"),
                avg("total_amount").alias("avg_order_value"),
                sum("total_amount").alias("total_revenue")
            )
        
        # Performance de produtos
        product_performance = df_bronze.groupBy("product_name", "category") \
            .agg(
                sum("quantity").alias("total_sold"),
                sum("total_amount").alias("revenue"),
                avg("rating").alias("avg_rating")
            )
        
        # Salvar agregações na camada Silver
        sales_by_category.write.mode("overwrite").parquet("s3a://silver-data/sales_summary/")
        customer_metrics.write.mode("overwrite").parquet("s3a://silver-data/customer_metrics/")
        product_performance.write.mode("overwrite").parquet("s3a://silver-data/product_performance/")
        
        print("Dados processados na camada Silver")
        
        return {
            'sales_summary': sales_by_category,
            'customer_metrics': customer_metrics,
            'product_performance': product_performance
        }
    
    def process_gold_layer(self, silver_data):
        """Camada GOLD: Dados prontos para consumo"""
        print("Processando camada Gold...")
        
        # KPIs principais
        sales_summary = silver_data['sales_summary']
        
        # Top 10 produtos por receita
        top_products = silver_data['product_performance'] \
            .orderBy(desc("revenue")) \
            .limit(10)
        
        # Tendência mensal de vendas
        monthly_trend = sales_summary \
            .withColumn("year_month", date_format(col("sale_date"), "yyyy-MM")) \
            .groupBy("year_month") \
            .agg(sum("total_sales").alias("monthly_sales"))
        
        # Salvar na camada Gold
        top_products.write.mode("overwrite").parquet("s3a://gold-data/top_products/")
        monthly_trend.write.mode("overwrite").parquet("s3a://gold-data/monthly_trend/")
        
        print("Dados processados na camada Gold")
        
        return {
            'top_products': top_products,
            'monthly_trend': monthly_trend
        }
    
    def export_to_postgres(self, silver_data):
        """Exporta dados processados para PostgreSQL"""
        print("Exportando dados para PostgreSQL...")
        
        # Configuração de conexão
        conn_params = {
            'host': 'localhost',
            'port': 5432,
            'database': 'sales_db',
            'user': 'postgres',
            'password': 'postgres123'
        }
        
        try:
            # Converter Spark DataFrames para Pandas para inserção
            sales_df = silver_data['sales_summary'].toPandas()
            customer_df = silver_data['customer_metrics'].toPandas()
            product_df = silver_data['product_performance'].toPandas()
            
            # Conectar ao PostgreSQL
            conn = psycopg2.connect(**conn_params)
            
            # Inserir dados (usando pandas to_sql seria mais eficiente, mas vamos usar psycopg2)
            cursor = conn.cursor()
            
            # Limpar tabelas existentes
            cursor.execute("TRUNCATE TABLE sales_summary, customer_metrics, product_performance")
            
            # Inserir sales_summary
            for _, row in sales_df.iterrows():
                cursor.execute("""
                    INSERT INTO sales_summary (product_category, total_sales, total_quantity, avg_price, sales_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row['category'], row['total_sales'], row['total_quantity'], row['avg_price'], row['sale_date']))
            
            # Inserir customer_metrics
            for _, row in customer_df.iterrows():
                cursor.execute("""
                    INSERT INTO customer_metrics (customer_segment, total_customers, avg_order_value, total_revenue)
                    VALUES (%s, %s, %s, %s)
                """, (row['customer_segment'], row['total_customers'], row['avg_order_value'], row['total_revenue']))
            
            # Inserir product_performance
            for _, row in product_df.iterrows():
                cursor.execute("""
                    INSERT INTO product_performance (product_name, category, total_sold, revenue, avg_rating)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row['product_name'], row['category'], row['total_sold'], row['revenue'], row['avg_rating']))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("Dados exportados para PostgreSQL com sucesso")
            
        except Exception as e:
            print(f"Erro ao exportar para PostgreSQL: {e}")
    
    def run_pipeline(self, csv_path):
        """Executa o pipeline completo"""
        print("=== Iniciando Pipeline de Dados ===")
        
        # 1. Criar buckets
        self.create_buckets()
        
        # 2. Ingestão (RAW)
        df_raw = self.ingest_raw_data(csv_path)
        
        # 3. Processamento Bronze
        df_bronze = self.process_bronze_layer(df_raw)
        
        # 4. Processamento Silver
        silver_data = self.process_silver_layer(df_bronze)
        
        # 5. Processamento Gold
        gold_data = self.process_gold_layer(silver_data)
        
        # 6. Exportar para PostgreSQL
        self.export_to_postgres(silver_data)
        
        print("=== Pipeline executado com sucesso! ===")
        
        # Mostrar algumas estatísticas
        print("\nEstatísticas do processamento:")
        print(f"Total de registros processados: {df_bronze.count()}")
        print(f"Categorias únicas: {df_bronze.select('category').distinct().count()}")
        print(f"Período dos dados: {df_bronze.agg(min('sale_date'), max('sale_date')).collect()[0]}")

if __name__ == "__main__":
    # Executar pipeline
    pipeline = DataPipeline()
    pipeline.run_pipeline("datasets/sales_data.csv")