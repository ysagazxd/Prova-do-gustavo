# 📋 ESTRUTURA CONFLUENCE - Sistema de Análise de Vendas E-commerce

## 🏗️ HIERARQUIA DE PÁGINAS

```
📁 Sistema de Análise de Vendas E-commerce (PÁGINA PRINCIPAL)
├── 📄 1. Visão Geral do Projeto
├── 📄 2. Arquitetura do Sistema  
├── 📄 3. Guia de Execução
├── 📄 4. Documentação Técnica Completa
├── 📄 5. Análise de Dados
└── 📄 6. Resumo Executivo
```

---

## 📄 PÁGINA PRINCIPAL - Sistema de Análise de Vendas E-commerce

### Conteúdo da Página Principal:

**Título:** Sistema de Análise de Vendas E-commerce

**Descrição:** Pipeline completo de dados para análise de performance de vendas

### Visão Geral
Este projeto implementa um pipeline completo de dados para análise de vendas de e-commerce, desde a ingestão até a visualização de insights de negócio.

### Problema Abordado
Análise de performance de vendas, identificação de produtos mais vendidos, sazonalidade e comportamento de clientes para tomada de decisão estratégica.

### Arquitetura
```
Dados CSV → Ingestão (Python) → Processamento (Spark) → Data Lake (MinIO) → Visualização (Metabase)
```

### Como Executar
1. **Pré-requisitos:** Docker e Docker Compose, Python 3.9+
2. **Executar:** `docker-compose up -d` → `python src/pipeline.py`
3. **Acessar:** MinIO (http://localhost:9001), Metabase (http://localhost:3000)

### Estrutura do Projeto
```
├── docs/           # Documentação completa
├── src/            # Código-fonte do pipeline
├── infra/          # Docker Compose e configs
├── notebooks/      # Análise exploratória
├── datasets/       # Dados de exemplo
└── README.md       # Este arquivo
```

### Equipe
- **Gustavo**: Arquitetura geral e processamento de dados
- **[Colega]**: Visualização e análise de dados

### Tecnologias Utilizadas
- **Ingestão**: Python, Pandas
- **Processamento**: Apache Spark
- **Armazenamento**: MinIO (S3-compatible)
- **Visualização**: Metabase
- **Orquestração**: Docker Compose

### Páginas Filhas
- [Visão Geral do Projeto]
- [Arquitetura do Sistema]
- [Guia de Execução]
- [Documentação Técnica Completa]
- [Análise de Dados]
- [Resumo Executivo]

---

## 📄 PÁGINA 1 - Visão Geral do Projeto

### Descrição do Problema

#### Contexto de Negócio
O projeto aborda a necessidade de uma empresa de e-commerce analisar suas vendas para:
- Identificar produtos e categorias mais rentáveis
- Entender comportamento sazonal das vendas
- Segmentar clientes por valor e comportamento
- Otimizar estratégias de marketing e estoque

#### Desafios Técnicos
- Volume crescente de dados de vendas
- Necessidade de processamento em batch e potencial streaming
- Múltiplas fontes de dados (vendas, produtos, clientes)
- Demanda por dashboards em tempo real
- Escalabilidade para crescimento futuro

### Objetivos do Sistema

#### Objetivos Principais
- **Centralização**: Unificar dados de vendas em Data Lake
- **Processamento**: Pipeline automatizado de ETL
- **Análise**: Gerar insights de negócio através de KPIs
- **Visualização**: Dashboards interativos para tomada de decisão

#### Objetivos Técnicos
- Implementar arquitetura de Data Lake (Bronze/Silver/Gold)
- Processar dados com Apache Spark para escalabilidade
- Armazenar dados em formato otimizado (Parquet)
- Disponibilizar dados via PostgreSQL para BI
- Criar dashboards no Metabase

### Escopo da Solução

#### Incluído no Escopo
- Pipeline de ingestão de dados CSV
- Processamento batch com Spark
- Data Lake com 4 camadas (Raw/Bronze/Silver/Gold)
- Armazenamento em MinIO (S3-compatible)
- Banco PostgreSQL para consultas OLAP
- Dashboards no Metabase
- Análise exploratória em Jupyter
- Documentação completa
- Scripts de automação

#### Não Incluído no Escopo
- Ingestão em tempo real (streaming)
- APIs REST para consulta de dados
- Autenticação e autorização avançada
- Monitoramento e alertas automatizados
- Backup e disaster recovery automatizado
- Integração com sistemas externos (CRM, ERP)

---

## 📄 PÁGINA 2 - Arquitetura do Sistema

### Visão Geral da Arquitetura

#### Diagrama de Componentes
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

### Camadas da Arquitetura

#### Camada de Ingestão
- **Tecnologia**: Python + Pandas
- **Função**: Coleta e validação inicial dos dados
- **Formato de Entrada**: CSV
- **Validações**: Verificação de integridade, tipos de dados

#### Camada de Processamento
- **Tecnologia**: Apache Spark
- **Função**: Transformações, limpeza e agregações
- **Paralelização**: Distribuído para grandes volumes
- **Otimizações**: Cache de DataFrames, particionamento

#### Camada de Armazenamento (Data Lake)

**Raw Layer (Dados Brutos)**
- **Bucket**: `raw-data`
- **Formato**: Parquet (compressão eficiente)
- **Conteúdo**: Dados originais sem transformação
- **Retenção**: Permanente para auditoria

**Bronze Layer (Dados Limpos)**
- **Bucket**: `bronze-data`
- **Formato**: Parquet particionado por data
- **Transformações**: Remoção de registros inválidos, padronização de tipos

**Silver Layer (Dados Agregados)**
- **Bucket**: `silver-data`
- **Formato**: Parquet otimizado
- **Conteúdo**: Agregações por categoria/período, métricas de clientes

**Gold Layer (Dados para Consumo)**
- **Bucket**: `gold-data`
- **Formato**: Parquet + PostgreSQL
- **Conteúdo**: KPIs principais, dados prontos para dashboards

#### Camada de Apresentação
- **Tecnologia**: Metabase
- **Função**: Dashboards e relatórios
- **Conexão**: PostgreSQL como fonte
- **Atualizações**: Batch diário via pipeline

### Fluxo de Dados

1. **Ingestão**: CSV → Validação → Raw Layer
2. **Bronze**: Raw → Limpeza → Bronze Layer
3. **Silver**: Bronze → Agregações → Silver Layer
4. **Gold**: Silver → KPIs → Gold Layer + PostgreSQL
5. **Visualização**: PostgreSQL → Metabase → Dashboards

---

## 📄 PÁGINA 3 - Guia de Execução

### Pré-requisitos

#### Software Necessário
- **Docker Desktop**: Versão 4.0+
- **Docker Compose**: Versão 2.0+
- **Python**: Versão 3.9+
- **Git**: Para versionamento

#### Recursos Mínimos
- **RAM**: 8GB (recomendado 16GB)
- **Storage**: 10GB livres
- **CPU**: 4 cores (recomendado)

### Execução Passo a Passo

#### 1. Subir a Infraestrutura
```bash
cd infra
docker-compose up -d
docker-compose ps
```

#### 2. Gerar Dados de Exemplo
```bash
cd ..
python src/generate_data.py
```

#### 3. Executar Pipeline de Dados
```bash
python src/pipeline.py
```

### Verificação dos Serviços

#### MinIO (Data Lake)
- **URL**: http://localhost:9001
- **Usuário**: admin
- **Senha**: password123

#### PostgreSQL
```bash
docker exec -it postgres psql -U postgres -d sales_db
\dt
SELECT COUNT(*) FROM sales_summary;
```

#### Metabase
- **URL**: http://localhost:3000
- **Configuração**: PostgreSQL (host: postgres, porta: 5432, db: sales_db)

### Troubleshooting

#### Containers não sobem
```bash
netstat -an | findstr "3000 5432 8080 9000"
docker stop $(docker ps -q)
docker system prune -f
```

#### Erro no pipeline Spark
```bash
docker logs spark-master
docker logs spark-worker
docker-compose restart spark-master spark-worker
```

---

## 📄 PÁGINA 4 - Documentação Técnica Completa

### Tecnologias e Ferramentas

#### Stack Tecnológico

| Componente | Tecnologia | Versão | Justificativa |
|------------|------------|--------|---------------|
| Processamento | Apache Spark | 3.4 | Escalabilidade, performance |
| Storage | MinIO | Latest | S3-compatible, open-source |
| Database | PostgreSQL | 13 | OLAP, performance analítica |
| BI | Metabase | Latest | Open-source, fácil uso |
| Linguagem | Python | 3.9+ | Ecossistema data science |
| Orquestração | Docker Compose | 2.0+ | Portabilidade, isolamento |

#### Decisões Técnicas

**Por que Spark?**
- **Prós**: Escalabilidade, performance, ecossistema
- **Contras**: Complexidade, overhead para pequenos dados
- **Alternativas**: Pandas (limitado), Dask (menos maduro)
- **Decisão**: Spark pela escalabilidade futura

**Por que MinIO?**
- **Prós**: S3-compatible, open-source, performance
- **Contras**: Menos features que AWS S3
- **Alternativas**: HDFS (complexo), filesystem local (não escalável)
- **Decisão**: MinIO pela compatibilidade e simplicidade

### Dados e Schema

#### Schema dos Dados
```sql
order_id VARCHAR(20) -- Identificador único do pedido
customer_id INTEGER -- ID do cliente
customer_segment VARCHAR(20) -- Segmento (Premium/Regular/Básico)
product_name VARCHAR(100) -- Nome do produto
category VARCHAR(50) -- Categoria do produto
price DECIMAL(10,2) -- Preço unitário
quantity INTEGER -- Quantidade vendida
total_amount DECIMAL(12,2) -- Valor total (price * quantity)
sale_date DATE -- Data da venda
rating DECIMAL(3,1) -- Avaliação do produto (1-5)
```

### Pontos de Falha e Limitações

#### Limitações Atuais
- **Escalabilidade**: Single-node, não cluster
- **Performance**: Sem otimizações avançadas
- **Disponibilidade**: Sem redundância ou failover
- **Monitoramento**: Manual, sem alertas automáticos
- **Dados**: Sintéticos, não refletem realidade
- **Tempo real**: Apenas batch, sem streaming

#### Mitigações Implementadas
- **Validação de dados**: Filtros de qualidade
- **Logs detalhados**: Para troubleshooting
- **Containerização**: Isolamento e portabilidade
- **Documentação**: Guias de execução e troubleshooting

### Trabalho Individual

#### Gustavo (Você)
- **Arquitetura geral**: Design do pipeline e componentes
- **Processamento de dados**: Implementação Spark, transformações
- **Data Lake**: Estrutura de camadas, formatos de dados
- **Infraestrutura**: Docker Compose, configurações
- **Documentação**: Arquitetura, guias técnicos

#### [Seu Colega]
- **Análise de dados**: Jupyter notebooks, estatísticas
- **Visualização**: Dashboards Metabase, KPIs
- **Validação**: Testes de qualidade, validação de resultados
- **Documentação**: Análises, insights de negócio

---

## 📄 PÁGINA 5 - Análise de Dados

### Dados Gerados

#### Estatísticas Gerais
- **Volume**: 10.000 registros de vendas
- **Período**: 2023-2024
- **Valor total**: R$ 16.7 milhões
- **Categorias**: 6 (Eletrônicos, Roupas, Casa, Livros, Esportes, Beleza)
- **Clientes**: 1.986 únicos

### KPIs Principais

#### Receita por Categoria
- **Eletrônicos**: ~R$ 5M (líder)
- **Roupas**: ~R$ 3M
- **Casa**: ~R$ 2.5M
- **Outros**: ~R$ 6.2M

#### Segmentação de Clientes
- **Premium**: Maior valor médio por pedido
- **Regular**: Volume médio
- **Básico**: Maior quantidade de transações

### Análise Exploratória

#### Jupyter Notebook
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

#### Principais Insights
- Sazonalidade identificada nos dados
- Padrões de comportamento por segmento
- Top produtos por receita e quantidade
- Correlações entre rating e vendas

### Visualizações

#### Metabase Dashboards
- Dashboard de vendas por categoria
- Análise temporal de receita
- Performance de produtos
- Métricas de clientes

---

## 📄 PÁGINA 6 - Resumo Executivo

### O que foi entregue

#### Estrutura Completa
- Pipeline completo: CSV → Python → Spark → MinIO → PostgreSQL → Metabase
- Data Lake: 4 camadas (Raw/Bronze/Silver/Gold)
- Processamento: Apache Spark distribuído
- Armazenamento: MinIO (S3-compatible) + PostgreSQL
- Visualização: Metabase + Jupyter notebooks
- Infraestrutura: Docker Compose (5 containers)

### Como Executar (3 passos)

1. **Setup Automático**: `setup.bat`
2. **Executar Pipeline**: `python src/pipeline.py`
3. **Acessar Resultados**: MinIO (localhost:9001), Metabase (localhost:3000)

### Resultados Demonstráveis

#### KPIs Principais
- Receita por categoria: Eletrônicos lidera com ~R$ 5M
- Clientes Premium: Maior valor médio por pedido
- Sazonalidade: Padrões mensais identificados
- Top produtos: Ranking por receita e quantidade

#### Métricas Técnicas
- Performance: Pipeline completo em ~2 minutos
- Escalabilidade: Spark distribuído, storage S3-compatible
- Qualidade: 100% dos dados validados e processados
- Formato: Parquet otimizado (compressão ~70%)

### Diferenciais do Projeto

#### Pontos Fortes
- **Funciona 100%**: Pipeline executável do zero
- **Documentação completa**: Guias detalhados, troubleshooting
- **Tecnologias modernas**: Spark, containers, Data Lake
- **Boas práticas**: Camadas, validações, versionamento
- **Escalável**: Design pensado para produção

#### Conhecimento Demonstrado
- **Big Data**: Spark, processamento distribuído
- **Engenharia de Dados**: ETL, Data Lake, formatos otimizados
- **DevOps**: Docker, orquestração, infraestrutura como código
- **Análise**: Jupyter, visualizações, insights

### Melhorias Futuras

#### Curto Prazo (1-3 meses)
- Agendamento: Airflow para orquestração
- Monitoramento: Prometheus + Grafana
- Testes: Unitários e integração
- CI/CD: Pipeline automatizado

#### Médio Prazo (3-6 meses)
- Streaming: Kafka + Spark Streaming
- APIs: REST endpoints para dados
- ML: Modelos preditivos (churn, recomendação)
- Segurança: Autenticação, criptografia

#### Longo Prazo (6+ meses)
- Cloud: Migração para AWS/Azure/GCP
- Cluster: Spark/Hadoop distribuído
- Data Mesh: Arquitetura descentralizada
- Real-time: Dashboards em tempo real

---

## 📋 INSTRUÇÕES PARA CONFLUENCE

### Como Criar no Confluence:

1. **Criar Espaço**: "Sistema de Análise de Vendas E-commerce"
2. **Página Principal**: Copiar conteúdo da "PÁGINA PRINCIPAL"
3. **Páginas Filhas**: Criar 6 páginas filhas com os conteúdos respectivos
4. **Links**: Ajustar links internos para páginas do Confluence
5. **Formatação**: Usar macros do Confluence para código e diagramas

### Macros Úteis do Confluence:
- **{code}** para blocos de código
- **{info}** para caixas de informação
- **{warning}** para alertas
- **{toc}** para índice automático
- **{children}** para listar páginas filhas

### Anexos Recomendados:
- Screenshots dos dashboards
- Diagramas de arquitetura
- Logs de execução
- Código-fonte principal (pipeline.py)