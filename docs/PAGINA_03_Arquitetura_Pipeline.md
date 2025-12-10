# Arquitetura Completa do Pipeline

## 🏗️ Visão Geral da Arquitetura

### Diagrama de Componentes
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│   Dados CSV     │───▶│   Ingestão       │───▶│   Processamento │───▶│   Armazenamento  │
│   (Fonte)       │    │   (Python)       │    │   (Spark)       │    │   (MinIO S3)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └──────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Dashboards    │◀───│   PostgreSQL     │◀───│   Exportação    │
│   (Metabase)    │    │   (OLAP)         │    │   (Pipeline)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Fluxo de Dados Detalhado
```
[CSV Files] 
    ↓ (Python Pandas)
[Validation & Cleaning]
    ↓ (Spark ETL)
[Raw Layer - MinIO]
    ↓ (Spark Transformations)
[Bronze Layer - MinIO]
    ↓ (Spark Aggregations)
[Silver Layer - MinIO]
    ↓ (Spark KPIs)
[Gold Layer - MinIO]
    ↓ (JDBC Export)
[PostgreSQL OLAP]
    ↓ (SQL Queries)
[Metabase Dashboards]
```

---

## 🔄 Camadas do Pipeline

### 1. Camada de Ingestão

#### Componente: Python + Pandas
**Responsabilidades:**
- **Leitura de arquivos CSV** com encoding automático
- **Validação inicial** de schema e tipos de dados
- **Limpeza básica** de dados inconsistentes
- **Conversão para Parquet** para otimização de storage

**Validações Implementadas:**
- **Campos obrigatórios**: Verificação de valores nulos
- **Tipos de dados**: Conversão e validação automática
- **Ranges válidos**: Preços > 0, quantidades > 0, ratings 1-5
- **Consistência**: total_amount = price × quantity

**Código de Exemplo:**
```python
def validate_sales_data(df):
    # Validar campos obrigatórios
    required_fields = ['order_id', 'customer_id', 'price', 'quantity']
    for field in required_fields:
        if df[field].isnull().any():
            raise ValueError(f"Campo {field} tem valores nulos")
    
    # Validar ranges
    if (df['price'] <= 0).any():
        raise ValueError("Preços devem ser positivos")
    
    # Validar consistência
    calculated_total = df['price'] * df['quantity']
    if not np.allclose(df['total_amount'], calculated_total):
        raise ValueError("Inconsistência no cálculo de total_amount")
```

### 2. Camada de Processamento

#### Componente: Apache Spark
**Configuração:**
- **Spark Master**: Coordenador de jobs e recursos
- **Spark Worker**: Executor de tarefas distribuídas
- **Memory**: 1GB por worker configurado
- **Cores**: 1 core por worker para paralelização

**Otimizações Implementadas:**
- **Cache de DataFrames**: Para reutilização em múltiplas operações
- **Broadcast Joins**: Para tabelas pequenas (lookup tables)
- **Particionamento**: Por data para otimizar consultas temporais
- **Catalyst Optimizer**: Otimização automática de queries

**Transformações por Camada:**

#### Raw → Bronze
```python
def process_bronze_layer(spark, raw_path):
    df = spark.read.parquet(raw_path)
    
    # Filtros de qualidade
    df_clean = df.filter(
        (col("price") > 0) & 
        (col("quantity") > 0) & 
        (col("rating").between(1, 5))
    )
    
    # Padronização de tipos
    df_clean = df_clean.withColumn("sale_date", to_date(col("sale_date")))
    df_clean = df_clean.withColumn("processed_at", current_timestamp())
    
    return df_clean
```

#### Bronze → Silver
```python
def process_silver_layer(spark, bronze_path):
    df = spark.read.parquet(bronze_path)
    
    # Agregações por categoria
    category_metrics = df.groupBy("category") \
        .agg(
            sum("total_amount").alias("total_revenue"),
            count("order_id").alias("total_orders"),
            avg("rating").alias("avg_rating"),
            sum("quantity").alias("units_sold")
        )
    
    # Métricas de clientes
    customer_metrics = df.groupBy("customer_id", "customer_segment") \
        .agg(
            sum("total_amount").alias("customer_ltv"),
            count("order_id").alias("total_orders"),
            max("sale_date").alias("last_purchase")
        )
    
    return category_metrics, customer_metrics
```

#### Silver → Gold
```python
def process_gold_layer(spark, silver_path):
    # KPIs principais para dashboards
    df = spark.read.parquet(silver_path)
    
    # Top produtos por receita
    top_products = df.groupBy("product_name") \
        .agg(sum("total_amount").alias("revenue")) \
        .orderBy(desc("revenue")) \
        .limit(20)
    
    # Vendas por mês
    monthly_sales = df.groupBy(
        date_trunc("month", col("sale_date")).alias("month")
    ).agg(
        sum("total_amount").alias("monthly_revenue"),
        countDistinct("customer_id").alias("unique_customers")
    )
    
    return top_products, monthly_sales
```

### 3. Camada de Armazenamento

#### Componente: MinIO (S3-Compatible)
**Configuração:**
- **Endpoint**: http://localhost:9000 (API)
- **Console**: http://localhost:9001 (Web UI)
- **Credenciais**: admin/password123
- **Buckets**: raw-data, bronze-data, silver-data, gold-data

**Estrutura de Buckets:**
```
minio/
├── raw-data/
│   └── sales_data_20241201.parquet
├── bronze-data/
│   └── year=2024/month=12/day=01/
│       └── part-00000.parquet
├── silver-data/
│   ├── category_metrics/
│   └── customer_metrics/
└── gold-data/
    ├── top_products/
    └── monthly_sales/
```

**Otimizações de Storage:**
- **Formato Parquet**: Compressão Snappy (~70% redução)
- **Particionamento**: Por data para consultas eficientes
- **Schema Evolution**: Suporte a mudanças de schema
- **Versionamento**: Controle de versões automático

### 4. Camada OLAP

#### Componente: PostgreSQL
**Configuração:**
- **Versão**: PostgreSQL 13
- **Database**: sales_db
- **Usuário**: postgres/postgres123
- **Porta**: 5432

**Schema Otimizado:**
```sql
-- Tabela principal de vendas
CREATE TABLE sales_summary (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id INTEGER,
    customer_segment VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    quantity INTEGER,
    total_amount DECIMAL(12,2),
    sale_date DATE,
    rating DECIMAL(3,1)
);

-- Índices para performance
CREATE INDEX idx_sales_date ON sales_summary(sale_date);
CREATE INDEX idx_sales_category ON sales_summary(category);
CREATE INDEX idx_sales_customer ON sales_summary(customer_id);
CREATE INDEX idx_sales_segment ON sales_summary(customer_segment);

-- Tabela de métricas de clientes
CREATE TABLE customer_metrics (
    customer_id INTEGER PRIMARY KEY,
    customer_segment VARCHAR(20),
    total_orders INTEGER,
    total_revenue DECIMAL(12,2),
    avg_order_value DECIMAL(10,2),
    last_purchase_date DATE
);

-- Tabela de performance de produtos
CREATE TABLE product_performance (
    product_name VARCHAR(100) PRIMARY KEY,
    category VARCHAR(50),
    total_revenue DECIMAL(12,2),
    total_orders INTEGER,
    avg_rating DECIMAL(3,1),
    units_sold INTEGER
);
```

### 5. Camada de Visualização

#### Componente: Metabase
**Configuração:**
- **URL**: http://localhost:3000
- **Database**: PostgreSQL (sales_db)
- **Conexão**: Automática via Docker network

**Dashboards Implementados:**
1. **Visão Executiva**: KPIs principais e tendências
2. **Análise de Produtos**: Performance e rankings
3. **Segmentação de Clientes**: Comportamento e valor
4. **Análise Temporal**: Sazonalidade e crescimento

---

## 🔧 Infraestrutura e Orquestração

### Docker Compose
**Arquivo de Configuração:**
```yaml
version: '3.8'
services:
  minio:
    image: minio/minio:latest
    ports: ["9000:9000", "9001:9001"]
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: password123
    command: server /data --console-address ":9001"
    volumes: [minio_data:/data]

  spark-master:
    image: apache/spark:3.4.0
    container_name: spark-master
    command: /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
    environment:
      - SPARK_MASTER_HOST=0.0.0.0
      - SPARK_MASTER_PORT=7077
      - SPARK_MASTER_WEBUI_PORT=8080
    ports:
      - "8080:8080"
      - "7077:7077"

  spark-worker:
    image: apache/spark:3.4.0
    container_name: spark-worker
    command: /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
    environment:
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_MEMORY=1g

  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: sales_db
      POSTGRES_PASSWORD: postgres123
    ports: ["5432:5432"]
    volumes: [postgres_data:/var/lib/postgresql/data]

  metabase:
    image: metabase/metabase:latest
    container_name: metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: h2
      MB_DB_FILE: /metabase-data/metabase.db
    volumes:
      - metabase_data:/metabase-data
    depends_on:
      - postgres
```

### Rede e Comunicação
- **Rede Docker**: Isolamento e comunicação segura
- **Service Discovery**: Resolução automática de nomes
- **Health Checks**: Verificação de saúde dos serviços
- **Volumes Persistentes**: Dados mantidos entre restarts

### Monitoramento
- **Logs Centralizados**: Docker logs para todos os serviços
- **Métricas de Performance**: Tempo de execução do pipeline
- **Spark UI**: Monitoramento de jobs e recursos
- **MinIO Console**: Monitoramento de storage e objetos