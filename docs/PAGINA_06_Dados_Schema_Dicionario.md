# Descrição dos Dados: Origem, Formato, Schema e Dicionário

## 📊 Origem e Características dos Dados

### Fonte dos Dados

#### Dados Sintéticos Gerados
- **Tipo**: Dados artificiais gerados programaticamente
- **Propósito**: Simular transações reais de e-commerce para demonstração
- **Gerador**: Script Python utilizando biblioteca Faker
- **Realismo**: Padrões baseados em dados reais de mercado

#### Justificativa para Dados Sintéticos
- **Privacidade**: Evita uso de dados pessoais reais
- **Disponibilidade**: Não depende de acesso a sistemas externos
- **Controle**: Permite ajustar volume e características conforme necessário
- **Reprodutibilidade**: Mesmos dados podem ser gerados consistentemente

### Características do Dataset

#### Volume e Escala
- **Registros**: 10.000 transações de vendas
- **Período**: Janeiro 2023 a Dezembro 2024 (24 meses)
- **Clientes**: 2.000 clientes únicos (5 transações por cliente em média)
- **Produtos**: 30 produtos diferentes distribuídos em 6 categorias
- **Tamanho do arquivo**: ~2.5MB (CSV) / ~800KB (Parquet comprimido)

#### Distribuição Temporal
```python
# Distribuição por mês (exemplo)
2023-01: 380 transações
2023-02: 420 transações
...
2023-11: 580 transações (Black Friday)
2023-12: 650 transações (Natal)
2024-01: 400 transações
...
```

#### Distribuição por Categoria
```python
# Percentual de vendas por categoria
Eletrônicos: 35% (R$ 5.3M)
Casa & Jardim: 22% (R$ 3.4M)
Roupas: 18% (R$ 2.7M)
Livros: 15% (R$ 2.3M)
Esportes: 10% (R$ 1.5M)
Beleza: 8% (R$ 1.2M)
```

---

## 📋 Formato e Estrutura dos Dados

### Formato de Entrada (CSV)

#### Estrutura do Arquivo
```csv
order_id,customer_id,customer_segment,product_name,category,price,quantity,total_amount,sale_date,rating
ORD_000001,1001,Premium,Smartphone Samsung Galaxy,Eletrônicos,899.99,1,899.99,2023-01-15,4.5
ORD_000002,1002,Regular,Camiseta Polo,Roupas,79.90,2,159.80,2023-01-15,4.2
ORD_000003,1003,Básico,Livro Python Programming,Livros,45.50,1,45.50,2023-01-16,4.8
```

#### Características do CSV
- **Encoding**: UTF-8
- **Separador**: Vírgula (,)
- **Header**: Primeira linha contém nomes das colunas
- **Aspas**: Campos com vírgulas são delimitados por aspas duplas
- **Valores nulos**: Representados como campos vazios

### Formatos de Armazenamento

#### Raw Layer (Parquet Original)
```python
# Estrutura mantida igual ao CSV
Schema: 
├── order_id: string
├── customer_id: int64
├── customer_segment: string
├── product_name: string
├── category: string
├── price: double
├── quantity: int64
├── total_amount: double
├── sale_date: date
└── rating: double
```

#### Bronze Layer (Dados Limpos)
```python
# Adicionados campos de controle
Schema:
├── [campos originais]
├── processed_at: timestamp
├── data_quality_score: double
└── validation_flags: string
```

#### Silver Layer (Agregações)
```python
# Múltiplas tabelas especializadas
category_metrics:
├── category: string
├── total_revenue: double
├── total_orders: int64
├── avg_rating: double
└── units_sold: int64

customer_metrics:
├── customer_id: int64
├── customer_segment: string
├── total_orders: int64
├── customer_ltv: double
└── last_purchase: date
```

#### Gold Layer (KPIs Finais)
```python
# Dados otimizados para BI
sales_summary:
├── [todos os campos originais]
├── month_year: string
├── quarter: string
└── year: int64

top_products:
├── product_name: string
├── category: string
├── total_revenue: double
├── total_orders: int64
└── rank_position: int64
```

---

## 🗂️ Schema Detalhado

### Tabela Principal: sales_data

#### Definição SQL
```sql
CREATE TABLE sales_data (
    order_id VARCHAR(20) NOT NULL,
    customer_id INTEGER NOT NULL,
    customer_segment VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_amount DECIMAL(12,2) NOT NULL,
    sale_date DATE NOT NULL,
    rating DECIMAL(3,1) CHECK (rating >= 1.0 AND rating <= 5.0),
    
    -- Constraints
    PRIMARY KEY (order_id),
    CONSTRAINT chk_total_amount CHECK (total_amount = price * quantity)
);
```

#### Índices para Performance
```sql
-- Índices principais
CREATE INDEX idx_sales_date ON sales_data(sale_date);
CREATE INDEX idx_sales_category ON sales_data(category);
CREATE INDEX idx_sales_customer ON sales_data(customer_id);
CREATE INDEX idx_sales_segment ON sales_data(customer_segment);

-- Índices compostos
CREATE INDEX idx_sales_date_category ON sales_data(sale_date, category);
CREATE INDEX idx_sales_customer_date ON sales_data(customer_id, sale_date);
```

### Tabelas Derivadas

#### customer_metrics
```sql
CREATE TABLE customer_metrics (
    customer_id INTEGER PRIMARY KEY,
    customer_segment VARCHAR(20) NOT NULL,
    total_orders INTEGER NOT NULL,
    total_revenue DECIMAL(12,2) NOT NULL,
    avg_order_value DECIMAL(10,2) NOT NULL,
    first_purchase_date DATE NOT NULL,
    last_purchase_date DATE NOT NULL,
    days_since_last_purchase INTEGER,
    avg_rating DECIMAL(3,1)
);
```

#### product_performance
```sql
CREATE TABLE product_performance (
    product_name VARCHAR(100) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    total_revenue DECIMAL(12,2) NOT NULL,
    total_orders INTEGER NOT NULL,
    total_units_sold INTEGER NOT NULL,
    avg_price DECIMAL(10,2) NOT NULL,
    avg_rating DECIMAL(3,1),
    revenue_rank INTEGER,
    units_rank INTEGER
);
```

#### category_summary
```sql
CREATE TABLE category_summary (
    category VARCHAR(50) PRIMARY KEY,
    total_revenue DECIMAL(12,2) NOT NULL,
    total_orders INTEGER NOT NULL,
    total_units_sold INTEGER NOT NULL,
    avg_order_value DECIMAL(10,2) NOT NULL,
    avg_rating DECIMAL(3,1),
    unique_products INTEGER,
    revenue_percentage DECIMAL(5,2)
);
```

---

## 📖 Dicionário de Dados Completo

### Campos Principais

| Campo | Tipo | Tamanho | Obrigatório | Descrição | Exemplo | Validações |
|-------|------|---------|-------------|-----------|---------|------------|
| **order_id** | VARCHAR | 20 | Sim | Identificador único do pedido | ORD_000001 | Formato: ORD_XXXXXX |
| **customer_id** | INTEGER | - | Sim | ID numérico do cliente | 1001 | Range: 1001-3000 |
| **customer_segment** | VARCHAR | 20 | Sim | Segmento do cliente | Premium | Valores: Premium, Regular, Básico |
| **product_name** | VARCHAR | 100 | Sim | Nome completo do produto | Smartphone Samsung Galaxy | Texto livre |
| **category** | VARCHAR | 50 | Sim | Categoria do produto | Eletrônicos | 6 categorias válidas |
| **price** | DECIMAL | 10,2 | Sim | Preço unitário em R$ | 899.99 | Valor > 0 |
| **quantity** | INTEGER | - | Sim | Quantidade comprada | 2 | Valor > 0, máximo 10 |
| **total_amount** | DECIMAL | 12,2 | Sim | Valor total da linha | 1799.98 | price × quantity |
| **sale_date** | DATE | - | Sim | Data da transação | 2023-01-15 | Range: 2023-2024 |
| **rating** | DECIMAL | 3,1 | Não | Avaliação do produto | 4.5 | Range: 1.0-5.0 |

### Domínios de Valores

#### customer_segment
```python
VALID_SEGMENTS = {
    'Premium': 'Clientes de alto valor (>R$ 2000/mês)',
    'Regular': 'Clientes médios (R$ 500-2000/mês)', 
    'Básico': 'Clientes de baixo valor (<R$ 500/mês)'
}
```

#### category
```python
VALID_CATEGORIES = {
    'Eletrônicos': 'Smartphones, laptops, tablets, acessórios',
    'Roupas': 'Camisetas, calças, vestidos, acessórios',
    'Casa & Jardim': 'Móveis, decoração, utensílios domésticos',
    'Livros': 'Livros físicos e digitais, revistas',
    'Esportes': 'Equipamentos esportivos, roupas fitness',
    'Beleza': 'Cosméticos, perfumes, cuidados pessoais'
}
```

#### Produtos por Categoria
```python
PRODUCTS_BY_CATEGORY = {
    'Eletrônicos': [
        'Smartphone Samsung Galaxy', 'iPhone 14 Pro',
        'Laptop Dell Inspiron', 'Tablet iPad Air',
        'Fone Bluetooth Sony', 'Smartwatch Apple'
    ],
    'Roupas': [
        'Camiseta Polo', 'Calça Jeans Levi\'s',
        'Vestido Floral', 'Tênis Nike Air',
        'Jaqueta de Couro', 'Blusa de Tricot'
    ],
    # ... outras categorias
}
```

### Regras de Negócio

#### Cálculos Derivados
```python
# Total amount deve sempre ser price × quantity
total_amount = price * quantity

# Customer LTV (Lifetime Value)
customer_ltv = SUM(total_amount) GROUP BY customer_id

# Average Order Value por segmento
aov_segment = AVG(total_amount) GROUP BY customer_segment

# Revenue rank por produto
revenue_rank = RANK() OVER (ORDER BY SUM(total_amount) DESC)
```

#### Validações de Qualidade
```python
# Completude - campos obrigatórios
completeness = COUNT(non_null_fields) / COUNT(total_fields) * 100

# Validade - valores dentro dos ranges esperados
validity = COUNT(valid_records) / COUNT(total_records) * 100

# Consistência - cálculos matemáticos corretos
consistency = COUNT(correct_calculations) / COUNT(total_records) * 100

# Unicidade - IDs únicos
uniqueness = COUNT(DISTINCT order_id) / COUNT(order_id) * 100
```

### Padrões de Dados

#### Distribuições Estatísticas
```python
# Preços por categoria (médias)
price_ranges = {
    'Eletrônicos': (200, 3000),    # R$ 200 - R$ 3.000
    'Roupas': (30, 300),           # R$ 30 - R$ 300
    'Casa & Jardim': (50, 800),    # R$ 50 - R$ 800
    'Livros': (20, 150),           # R$ 20 - R$ 150
    'Esportes': (40, 500),         # R$ 40 - R$ 500
    'Beleza': (25, 200)            # R$ 25 - R$ 200
}

# Distribuição de ratings (normal)
rating_distribution = {
    'mean': 4.2,
    'std_dev': 0.8,
    'min': 1.0,
    'max': 5.0
}

# Sazonalidade (multiplicadores mensais)
seasonal_multipliers = {
    'Jan': 0.9, 'Feb': 0.8, 'Mar': 0.9,
    'Apr': 1.0, 'May': 1.1, 'Jun': 1.0,
    'Jul': 0.9, 'Aug': 1.0, 'Sep': 1.1,
    'Oct': 1.2, 'Nov': 1.4, 'Dec': 1.5  # Black Friday/Natal
}
```

### Metadados Técnicos

#### Informações de Processamento
```python
metadata = {
    'created_at': '2024-12-01T10:00:00Z',
    'created_by': 'generate_data.py',
    'version': '1.0',
    'total_records': 10000,
    'file_size_csv': '2.5MB',
    'file_size_parquet': '800KB',
    'compression_ratio': '68%',
    'processing_time': '45 seconds',
    'data_quality_score': 98.5
}
```

#### Linhagem de Dados
```python
data_lineage = {
    'source': 'synthetic_generator',
    'transformations': [
        'csv_to_parquet',
        'data_validation',
        'quality_scoring',
        'aggregation_silver',
        'kpi_calculation_gold'
    ],
    'destinations': [
        'minio_data_lake',
        'postgresql_olap',
        'metabase_dashboards'
    ]
}
```