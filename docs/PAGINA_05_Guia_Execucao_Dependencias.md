# Guia de Execução e Dependências

## 🛠️ **REQUISITOS OBRIGATÓRIOS PARA RODAR O PROJETO**

### **✅ DEVE TER INSTALADO:**
- **Docker** (versão 20.10.0 ou superior)
- **Docker Compose** (versão 2.0.0 ou superior) 
- **Python** (versão 3.9.0 ou superior)

### **⚠️ OPCIONAL (para pipeline Spark completo):**
- **Java 17+** (se não tiver, use pipeline simplificado)

### **🔍 VERIFICAR SE TEM:**
```bash
docker --version          # Precisa: 20.10.0+
docker-compose --version  # Precisa: 2.0.0+
python --version          # Precisa: 3.9.0+
java -version             # Opcional: 17+ (para Spark)
```

### **📦 INSTALAÇÃO AUTOMÁTICA:**
```bash
# Execute apenas este comando (instala tudo automaticamente):
setup.bat
```

### **📦 INSTALAÇÃO MANUAL:**
```bash
# 1. Instalar dependências Python
pip install pandas numpy boto3 psycopg2-binary matplotlib seaborn python-dotenv

# 2. Subir containers Docker
cd infra && docker-compose up -d

# 3. Executar pipeline
python src/pipeline_simple.py
```

---

## 🚀 Guia de Execução: Como Rodar do Zero

### Pré-requisitos Detalhados

#### Software Necessário
```bash
# Verificar se está instalado
docker --version          # Mínimo: 20.10.0
docker-compose --version  # Mínimo: 2.0.0
python --version          # Mínimo: 3.9.0
git --version             # Qualquer versão recente
```

#### Recursos de Hardware
- **RAM**: 8GB mínimo (16GB recomendado)
- **CPU**: 4 cores mínimo (8 cores recomendado)
- **Storage**: 10GB livres (SSD preferível)
- **Rede**: Conexão para download de imagens Docker

#### Portas Necessárias
```bash
# Verificar se as portas estão livres
netstat -an | findstr "3000 5432 7077 8080 9000 9001"
# Se alguma porta estiver ocupada, parar o serviço correspondente
```

### Método 1: Execução Automática (Recomendado)

#### Passo Único
```bash
# Executar script de setup completo
setup.bat
```

**O que o script faz:**
1. Verifica pré-requisitos
2. Instala dependências Python
3. Sobe infraestrutura Docker
4. Aguarda inicialização dos serviços
5. Executa pipeline de dados
6. Valida resultados

### Método 2: Execução Manual Passo a Passo

#### Passo 1: Preparação do Ambiente
```bash
# 1. Clonar repositório (se necessário)
git clone https://github.com/ysagazxd/Prova-do-gustavo.git
cd Prova-do-gustavo

# 2. Criar ambiente virtual Python
python -m venv venv

# 3. Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt
```

#### Passo 2: Configuração de Variáveis (Opcional)
```bash
# Criar arquivo .env para customizações
echo MINIO_ROOT_USER=admin > .env
echo MINIO_ROOT_PASSWORD=password123 >> .env
echo POSTGRES_PASSWORD=postgres123 >> .env
echo SPARK_WORKER_MEMORY=2g >> .env
echo SPARK_WORKER_CORES=2 >> .env
```

#### Passo 3: Subir Infraestrutura
```bash
# Navegar para diretório de infraestrutura
cd infra

# Subir todos os serviços em background
docker-compose up -d

# Verificar se todos os containers subiram
docker-compose ps
```

**Saída Esperada:**
```
NAME                IMAGE                     STATUS
minio               minio/minio:latest        Up
metabase            metabase/metabase:latest  Up
postgres            postgres:13               Up
spark-master        bitnami/spark:3.4         Up
spark-worker        bitnami/spark:3.4         Up
```

#### Passo 4: Aguardar Inicialização
```bash
# Aguardar 2-3 minutos para todos os serviços iniciarem
# Verificar logs se necessário
docker-compose logs -f metabase

# Testar conectividade
curl -I http://localhost:9001  # MinIO Console
curl -I http://localhost:8080  # Spark UI
curl -I http://localhost:3000  # Metabase
```

#### Passo 5: Gerar Dados de Exemplo
```bash
# Voltar para diretório raiz
cd ..

# Executar geração de dados sintéticos
python src/generate_data.py
```

**Saída Esperada:**
```
Gerando dados sintéticos de vendas...
Dados gerados: 10000 registros
Período: 2023-01-01 a 2024-12-31
Categorias: 6 (Eletrônicos, Roupas, Casa & Jardim, Livros, Esportes, Beleza)
Clientes únicos: 2000
Produtos únicos: 30
Total de vendas: R$ 15,234,567.89
Arquivo salvo: datasets/sales_data.csv
```

#### Passo 6: Executar Pipeline Principal
```bash
# Executar pipeline completo de ETL
python src/pipeline.py
```

**Saída Esperada:**
```
=== Sistema de Análise de Vendas E-commerce ===
=== Iniciando Pipeline de Dados ===

[INFO] Configurando conexões...
[INFO] MinIO conectado: http://localhost:9000
[INFO] Spark Session iniciada: SalesAnalytics
[INFO] PostgreSQL conectado: sales_db

[INFO] Criando buckets no Data Lake...
✓ Bucket 'raw-data' criado
✓ Bucket 'bronze-data' criado  
✓ Bucket 'silver-data' criado
✓ Bucket 'gold-data' criado

[INFO] Processando camada RAW...
✓ Dados carregados: 10000 registros
✓ Validações executadas: 100% válidos
✓ Dados salvos: raw-data/sales_data_20241201.parquet

[INFO] Processando camada BRONZE...
✓ Filtros de qualidade aplicados
✓ Padronização de tipos concluída
✓ Dados salvos: bronze-data/year=2024/month=12/

[INFO] Processando camada SILVER...
✓ Agregações por categoria calculadas
✓ Métricas de clientes processadas
✓ Dados salvos: silver-data/

[INFO] Processando camada GOLD...
✓ KPIs principais calculados
✓ Top produtos identificados
✓ Dados salvos: gold-data/

[INFO] Exportando para PostgreSQL...
✓ Tabela sales_summary: 10000 registros
✓ Tabela customer_metrics: 2000 registros
✓ Tabela product_performance: 30 registros

=== Pipeline executado com sucesso! ===
Tempo total: 2m 34s
```

### Verificação de Resultados

#### Acessar Interfaces Web
```bash
# MinIO Console (Data Lake)
# URL: http://localhost:9001
# User: admin / Pass: password123

# Spark UI (Monitoramento)
# URL: http://localhost:8080

# Metabase (Dashboards)
# URL: http://localhost:3000
# Configurar conexão PostgreSQL na primeira vez
```

#### Verificar Dados no PostgreSQL
```bash
# Conectar via linha de comando
docker exec -it postgres psql -U postgres -d sales_db

# Verificar tabelas criadas
\dt

# Contar registros
SELECT 'sales_summary' as tabela, COUNT(*) as registros FROM sales_summary
UNION ALL
SELECT 'customer_metrics' as tabela, COUNT(*) as registros FROM customer_metrics
UNION ALL  
SELECT 'product_performance' as tabela, COUNT(*) as registros FROM product_performance;

# Sair do PostgreSQL
\q
```

#### Executar Análise Exploratória
```bash
# Iniciar Jupyter Notebook
jupyter notebook notebooks/

# Abrir e executar: exploratory_analysis.ipynb
# Verificar gráficos e estatísticas geradas
```

---

## 📦 Guia Completo de Dependências

### Dependências Python (requirements.txt)

#### Core Data Processing
```txt
# Manipulação de dados
pandas==2.1.4
numpy==1.24.3
pyspark==3.4.1

# Conectividade
boto3==1.34.0              # Cliente S3/MinIO
psycopg2-binary==2.9.9     # Driver PostgreSQL
sqlalchemy==2.0.23         # ORM database

# Visualização
matplotlib==3.7.2
seaborn==0.12.2
plotly==5.17.0

# Análise interativa
jupyter==1.0.0
ipykernel==6.25.0
notebook==7.0.6

# Utilitários
python-dotenv==1.0.0       # Variáveis de ambiente
faker==20.1.0              # Dados sintéticos
tqdm==4.66.1               # Progress bars
loguru==0.7.2              # Logging avançado
```

#### Instalação das Dependências
```bash
# Método 1: Via requirements.txt
pip install -r requirements.txt

# Método 2: Instalação individual
pip install pandas==2.1.4 numpy==1.24.3 pyspark==3.4.1
pip install boto3==1.34.0 psycopg2-binary==2.9.9
pip install matplotlib==3.7.2 seaborn==0.12.2
pip install jupyter==1.0.0 faker==20.1.0
```

### Imagens Docker Utilizadas

#### Serviços Principais
```yaml
# MinIO - Object Storage
minio/minio:latest
# Tamanho: ~50MB
# Função: Data Lake S3-compatible

# Apache Spark - Processamento
bitnami/spark:3.4
# Tamanho: ~800MB  
# Função: Master e Worker nodes

# PostgreSQL - Database OLAP
postgres:13
# Tamanho: ~150MB
# Função: Armazenamento estruturado

# Metabase - Business Intelligence
metabase/metabase:latest
# Tamanho: ~300MB
# Função: Dashboards e visualização
```

#### Download das Imagens
```bash
# Download manual (opcional)
docker pull minio/minio:latest
docker pull bitnami/spark:3.4
docker pull postgres:13
docker pull metabase/metabase:latest

# Verificar imagens baixadas
docker images
```

### Configurações de Sistema

#### Docker Compose (infra/docker-compose.yml)
```yaml
version: '3.8'

services:
  minio:
    image: minio/minio:latest
    container_name: minio
    ports:
      - "9000:9000"    # API
      - "9001:9001"    # Console
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: password123
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    networks:
      - data_network

  spark-master:
    image: bitnami/spark:3.4
    container_name: spark-master
    ports:
      - "8080:8080"    # Web UI
      - "7077:7077"    # Master port
    environment:
      - SPARK_MODE=master
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
    networks:
      - data_network

  spark-worker:
    image: bitnami/spark:3.4
    container_name: spark-worker
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=2G
      - SPARK_WORKER_CORES=2
    depends_on:
      - spark-master
    networks:
      - data_network

  postgres:
    image: postgres:13
    container_name: postgres
    environment:
      POSTGRES_DB: sales_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - data_network

  metabase:
    image: metabase/metabase:latest
    container_name: metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: metabase
      MB_DB_PORT: 5432
      MB_DB_USER: postgres
      MB_DB_PASS: postgres123
      MB_DB_HOST: postgres
    depends_on:
      - postgres
    volumes:
      - metabase_data:/metabase-data
    networks:
      - data_network

volumes:
  minio_data:
  postgres_data:
  metabase_data:

networks:
  data_network:
    driver: bridge
```

#### Configuração PostgreSQL (infra/init.sql)
```sql
-- Criar database para dados de vendas
CREATE DATABASE sales_db;

-- Conectar ao database
\c sales_db;

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Configurações de performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;

-- Recarregar configurações
SELECT pg_reload_conf();
```

### Versões e Compatibilidade

#### Matriz de Compatibilidade
| Componente | Versão Testada | Versão Mínima | Versão Máxima |
|------------|----------------|---------------|---------------|
| Python | 3.9.18 | 3.9.0 | 3.11.x |
| Docker | 24.0.7 | 20.10.0 | Latest |
| Docker Compose | 2.23.3 | 2.0.0 | Latest |
| Spark | 3.4.1 | 3.3.0 | 3.5.x |
| PostgreSQL | 13.13 | 13.0 | 15.x |
| MinIO | RELEASE.2024-01-16 | 2023.x | Latest |

#### Verificação de Versões
```bash
# Script de verificação completa
python --version
docker --version
docker-compose --version
pip list | grep -E "(pandas|pyspark|boto3)"

# Verificar containers em execução
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
```