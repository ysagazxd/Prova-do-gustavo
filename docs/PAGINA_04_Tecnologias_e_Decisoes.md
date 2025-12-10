# Tecnologias Utilizadas e Decisões Técnicas

## 🛠️ Detalhes das Ferramentas e Tecnologias

### Stack Tecnológico Completo

| Camada | Tecnologia | Versão | Função | Justificativa |
|--------|------------|--------|--------|---------------|
| **Linguagem** | Python | 3.9+ | Desenvolvimento principal | Ecossistema rico para data science |
| **Processamento** | Apache Spark | 3.4.0 | ETL distribuído | Escalabilidade e performance |
| **Storage** | MinIO | Latest | Data Lake S3-compatible | Compatibilidade cloud + open source |
| **Database** | PostgreSQL | 13 | OLAP analytics | Performance para consultas complexas |
| **BI/Visualização** | Metabase | Latest | Dashboards interativos | Interface intuitiva + open source |
| **Orquestração** | Docker Compose | 2.0+ | Containerização | Portabilidade e isolamento |
| **Análise** | Jupyter | 1.0.0 | Exploração interativa | Prototipagem e análise ad-hoc |

### Bibliotecas Python Detalhadas

#### Core Data Processing
```python
# requirements.txt
pandas==2.1.4              # Manipulação de dados estruturados
numpy==1.24.3              # Computação numérica otimizada
pyspark==3.4.1             # Interface Python para Spark
```

#### Storage e Conectividade
```python
boto3==1.34.0              # Cliente AWS S3 (MinIO compatible)
psycopg2-binary==2.9.9     # Driver PostgreSQL otimizado
minio==7.2.0               # Cliente MinIO nativo
```

#### Visualização e Análise
```python
matplotlib==3.7.2          # Gráficos estáticos
seaborn==0.12.2            # Visualizações estatísticas
jupyter==1.0.0             # Ambiente de análise
notebook==7.0.6            # Interface Jupyter
```

#### Utilitários
```python
python-dotenv==1.0.0       # Gerenciamento de variáveis de ambiente
requests==2.31.0           # Cliente HTTP
pytest==7.4.3              # Framework de testes
black==23.11.0             # Formatação de código
```

---

## ⚖️ Decisões Técnicas e Trade-offs

### 1. Apache Spark vs Alternativas

#### Decisão: Apache Spark
**Alternativas Consideradas:**
- **Pandas**: Limitado à memória de uma máquina
- **Dask**: Menos maduro, comunidade menor
- **Ray**: Foco em ML, não em ETL tradicional
- **Polars**: Muito novo, ecossistema limitado

**Justificativas:**
✅ **Escalabilidade Horizontal**: Distribui processamento entre múltiplos workers
✅ **Otimizações Automáticas**: Catalyst optimizer e Tungsten execution engine
✅ **Ecossistema Maduro**: Ampla compatibilidade com formatos e sistemas
✅ **Performance**: Processamento in-memory com spill para disco quando necessário
✅ **SQL Support**: Spark SQL para consultas complexas

**Trade-offs Aceitos:**
❌ **Complexidade**: Overhead de configuração e debugging
❌ **Recursos**: Consome mais memória que soluções single-machine
❌ **Latência**: Startup time maior para jobs pequenos

**Código de Configuração:**
```python
spark = SparkSession.builder \
    .appName("SalesAnalytics") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()
```

### 2. MinIO vs Alternativas de Storage

#### Decisão: MinIO
**Alternativas Consideradas:**
- **HDFS**: Complexidade de setup e manutenção
- **Local FileSystem**: Não escalável, sem redundância
- **AWS S3**: Vendor lock-in, custos variáveis
- **Azure Blob**: Mesmas limitações do S3

**Justificativas:**
✅ **S3 Compatibility**: API compatível com AWS S3
✅ **Open Source**: Sem custos de licenciamento
✅ **Performance**: Alta throughput para operações paralelas
✅ **Portabilidade**: Funciona on-premise e cloud
✅ **Simplicidade**: Setup e configuração straightforward

**Trade-offs Aceitos:**
❌ **Features**: Menos recursos que AWS S3 nativo
❌ **Managed Services**: Sem serviços gerenciados como S3 Glacier
❌ **Integração**: Menos integrações nativas que soluções cloud

**Configuração Docker:**
```yaml
minio:
  image: minio/minio:latest
  ports: ["9000:9000", "9001:9001"]
  environment:
    MINIO_ROOT_USER: admin
    MINIO_ROOT_PASSWORD: password123
  command: server /data --console-address ":9001"
  volumes: [minio_data:/data]
```

### 3. PostgreSQL vs Alternativas OLAP

#### Decisão: PostgreSQL
**Alternativas Consideradas:**
- **ClickHouse**: Melhor performance, mas menos conhecido
- **Apache Druid**: Complexo para casos de uso simples
- **BigQuery**: Cloud-only, custos variáveis
- **Snowflake**: Proprietário, custos altos

**Justificativas:**
✅ **SQL Padrão**: Familiar para analistas e desenvolvedores
✅ **OLAP Performance**: Otimizado para consultas analíticas
✅ **ACID Compliance**: Consistência transacional garantida
✅ **Extensibilidade**: Suporte a extensões e tipos customizados
✅ **Integração**: Compatibilidade nativa com ferramentas de BI

**Trade-offs Aceitos:**
❌ **Columnar Storage**: Não é columnar nativo como ClickHouse
❌ **Distributed**: Single-node por padrão
❌ **Compression**: Compressão menos eficiente que soluções especializadas

**Otimizações Implementadas:**
```sql
-- Índices para performance
CREATE INDEX CONCURRENTLY idx_sales_date_category 
ON sales_summary(sale_date, category);

-- Particionamento por data (futuro)
CREATE TABLE sales_summary_2024 PARTITION OF sales_summary
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Configurações de performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET random_page_cost = 1.1;
```

### 4. Metabase vs Alternativas de BI

#### Decisão: Metabase
**Alternativas Consideradas:**
- **Apache Superset**: Mais complexo, setup mais difícil
- **Grafana**: Foco em métricas, não em BI tradicional
- **Power BI**: Proprietário, custos de licença
- **Tableau**: Muito caro para uso acadêmico

**Justificativas:**
✅ **Facilidade de Uso**: Interface intuitiva para usuários não-técnicos
✅ **Open Source**: Sem custos de licenciamento
✅ **Setup Rápido**: Configuração em minutos via Docker
✅ **SQL Support**: Consultas SQL nativas suportadas
✅ **Dashboards**: Criação drag-and-drop de visualizações

**Trade-offs Aceitos:**
❌ **Features Avançadas**: Menos recursos que Power BI/Tableau
❌ **Performance**: Pode ser lento com datasets muito grandes
❌ **Customização**: Menos opções de customização visual

**Configuração de Conexão:**
```yaml
metabase:
  image: metabase/metabase:latest
  ports: ["3000:3000"]
  environment:
    MB_DB_TYPE: postgres
    MB_DB_DBNAME: sales_db
    MB_DB_PORT: 5432
    MB_DB_USER: postgres
    MB_DB_PASS: postgres123
    MB_DB_HOST: postgres
```

### 5. Docker Compose vs Alternativas de Orquestração

#### Decisão: Docker Compose
**Alternativas Consideradas:**
- **Kubernetes**: Over-engineering para ambiente local
- **Docker Swarm**: Menos features que Kubernetes
- **Vagrant**: VMs são mais pesadas que containers
- **Manual Setup**: Muito trabalhoso e propenso a erros

**Justificativas:**
✅ **Simplicidade**: Configuração declarativa em YAML
✅ **Portabilidade**: Funciona em qualquer ambiente com Docker
✅ **Isolamento**: Cada serviço em container separado
✅ **Networking**: Rede isolada com service discovery automático
✅ **Volumes**: Persistência de dados entre restarts

**Trade-offs Aceitos:**
❌ **Escalabilidade**: Limitado a single-host
❌ **High Availability**: Sem failover automático
❌ **Load Balancing**: Sem distribuição de carga nativa
❌ **Service Mesh**: Sem recursos avançados de rede

---

## 🔍 Análise de Alternativas Não Escolhidas

### Por que NÃO escolhemos certas tecnologias?

#### Hadoop/HDFS
**Motivos:**
- **Complexidade**: Setup e manutenção muito complexos
- **Overhead**: Recursos excessivos para volume de dados atual
- **Legacy**: Tecnologia mais antiga, sendo substituída por soluções cloud-native

#### NoSQL (MongoDB, Cassandra)
**Motivos:**
- **Consultas**: SQL é mais familiar para analistas
- **ACID**: Necessidade de consistência transacional
- **BI Tools**: Melhor integração com ferramentas de BI tradicionais

#### Kafka para Streaming
**Motivos:**
- **Escopo**: Projeto focado em batch processing
- **Complexidade**: Adiciona complexidade desnecessária
- **Recursos**: Overhead de infraestrutura significativo

#### Cloud Services (AWS, Azure, GCP)
**Motivos:**
- **Custos**: Evitar custos variáveis em ambiente acadêmico
- **Portabilidade**: Solução deve funcionar em qualquer ambiente
- **Aprendizado**: Foco em tecnologias open-source

---

## 📈 Benefícios das Escolhas Feitas

### Técnicos
- **Escalabilidade**: Arquitetura preparada para crescimento 100x
- **Performance**: Pipeline processa 10K registros em <3 minutos
- **Manutenibilidade**: Código limpo e bem documentado
- **Portabilidade**: Funciona em qualquer ambiente com Docker

### Operacionais
- **Setup Simples**: Execução com 3 comandos
- **Troubleshooting**: Logs centralizados e debugging facilitado
- **Monitoramento**: UIs web para todos os componentes
- **Backup**: Volumes Docker para persistência

### Econômicos
- **Custo Zero**: Todas as tecnologias são open-source
- **Recursos**: Otimizado para hardware modesto (8GB RAM)
- **Cloud Ready**: Migração futura para cloud sem reescrita
- **ROI**: Base sólida para expansão com investimento mínimo