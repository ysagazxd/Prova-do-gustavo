# Arquitetura do Sistema

## 1. Visão Geral da Arquitetura

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

## 2. Camadas da Arquitetura

### 2.1 Camada de Ingestão
- **Tecnologia**: Python + Pandas
- **Função**: Coleta e validação inicial dos dados
- **Formato de Entrada**: CSV
- **Validações**: Verificação de integridade, tipos de dados

### 2.2 Camada de Processamento
- **Tecnologia**: Apache Spark
- **Função**: Transformações, limpeza e agregações
- **Paralelização**: Distribuído para grandes volumes
- **Otimizações**: Cache de DataFrames, particionamento

### 2.3 Camada de Armazenamento (Data Lake)

#### Raw Layer (Dados Brutos)
- **Bucket**: `raw-data`
- **Formato**: Parquet (compressão eficiente)
- **Conteúdo**: Dados originais sem transformação
- **Retenção**: Permanente para auditoria

#### Bronze Layer (Dados Limpos)
- **Bucket**: `bronze-data`
- **Formato**: Parquet particionado por data
- **Transformações**: 
  - Remoção de registros inválidos
  - Padronização de tipos
  - Adição de timestamp de processamento

#### Silver Layer (Dados Agregados)
- **Bucket**: `silver-data`
- **Formato**: Parquet otimizado
- **Conteúdo**: 
  - Agregações por categoria/período
  - Métricas de clientes
  - Performance de produtos

#### Gold Layer (Dados para Consumo)
- **Bucket**: `gold-data`
- **Formato**: Parquet + PostgreSQL
- **Conteúdo**: 
  - KPIs principais
  - Dados prontos para dashboards
  - Métricas de negócio

### 2.4 Camada de Apresentação
- **Tecnologia**: Metabase
- **Função**: Dashboards e relatórios
- **Conexão**: PostgreSQL como fonte
- **Atualizações**: Batch diário via pipeline

## 3. Infraestrutura

### 3.1 Containerização
- **Docker Compose**: Orquestração de serviços
- **Serviços**:
  - MinIO (S3-compatible storage)
  - Spark Master/Worker
  - PostgreSQL
  - Metabase

### 3.2 Rede e Comunicação
- **Rede Docker**: `data_network`
- **Portas Expostas**:
  - MinIO: 9000 (API), 9001 (Console)
  - Spark: 8080 (UI), 7077 (Master)
  - PostgreSQL: 5432
  - Metabase: 3000

### 3.3 Volumes Persistentes
- `minio_data`: Armazenamento do Data Lake
- `postgres_data`: Banco de dados OLAP
- `metabase_data`: Configurações do Metabase

## 4. Fluxo de Dados

### 4.1 Pipeline de Processamento
1. **Ingestão**: CSV → Validação → Raw Layer
2. **Bronze**: Raw → Limpeza → Bronze Layer
3. **Silver**: Bronze → Agregações → Silver Layer
4. **Gold**: Silver → KPIs → Gold Layer + PostgreSQL
5. **Visualização**: PostgreSQL → Metabase → Dashboards

### 4.2 Frequência de Execução
- **Batch Diário**: Processamento completo
- **Incremental**: Apenas novos dados (futuro)
- **Real-time**: Streaming com Kafka (futuro)

## 5. Governança de Dados

### 5.1 Qualidade de Dados
- **Validações**: Tipos, ranges, obrigatoriedade
- **Monitoramento**: Logs de pipeline, métricas de qualidade
- **Alertas**: Falhas de processamento, dados inconsistentes

### 5.2 Catalogação
- **Metadados**: Schema, linhagem, documentação
- **Versionamento**: Controle de mudanças no schema
- **Descoberta**: Tags e classificações

### 5.3 Segurança
- **Acesso**: Credenciais por serviço
- **Criptografia**: Dados em trânsito e repouso
- **Auditoria**: Logs de acesso e modificações

## 6. Escalabilidade

### 6.1 Horizontal
- **Spark**: Adicionar workers conforme demanda
- **MinIO**: Cluster distribuído
- **PostgreSQL**: Read replicas

### 6.2 Vertical
- **Recursos**: CPU, memória por container
- **Storage**: SSD para melhor performance
- **Rede**: Bandwidth adequada

## 7. Monitoramento

### 7.1 Métricas Técnicas
- **Performance**: Tempo de processamento, throughput
- **Recursos**: CPU, memória, storage
- **Disponibilidade**: Uptime dos serviços

### 7.2 Métricas de Negócio
- **Qualidade**: Completude, precisão dos dados
- **SLA**: Tempo de disponibilização dos dados
- **Uso**: Dashboards mais acessados

## 8. Disaster Recovery

### 8.1 Backup
- **Frequência**: Diário para dados críticos
- **Retenção**: 30 dias para dados operacionais
- **Localização**: Storage externo/nuvem

### 8.2 Recuperação
- **RTO**: 4 horas para restauração completa
- **RPO**: Máximo 24 horas de perda de dados
- **Testes**: Mensais de recuperação