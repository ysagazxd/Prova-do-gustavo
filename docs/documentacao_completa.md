# Documentação Completa - Sistema de Análise de Vendas E-commerce

## 1. Descrição do Problema

### 1.1 Contexto de Negócio
O projeto aborda a necessidade de uma empresa de e-commerce analisar suas vendas para:
- Identificar produtos e categorias mais rentáveis
- Entender comportamento sazonal das vendas
- Segmentar clientes por valor e comportamento
- Otimizar estratégias de marketing e estoque

### 1.2 Desafios Técnicos
- Volume crescente de dados de vendas
- Necessidade de processamento em batch e potencial streaming
- Múltiplas fontes de dados (vendas, produtos, clientes)
- Demanda por dashboards em tempo real
- Escalabilidade para crescimento futuro

> 📋 **Para mais detalhes sobre como resolvemos estes desafios, veja a seção [4. Arquitetura Detalhada](#4-arquitetura-detalhada)**

## 2. Objetivos do Sistema

### 2.1 Objetivos Principais
- **Centralização**: Unificar dados de vendas em Data Lake
- **Processamento**: Pipeline automatizado de ETL
- **Análise**: Gerar insights de negócio através de KPIs
- **Visualização**: Dashboards interativos para tomada de decisão

### 2.2 Objetivos Técnicos
- Implementar arquitetura de Data Lake (Bronze/Silver/Gold)
- Processar dados com Apache Spark para escalabilidade
- Armazenar dados em formato otimizado (Parquet)
- Disponibilizar dados via PostgreSQL para BI
- Criar dashboards no Metabase

### 2.3 Justificativa Técnica
- **Spark**: Processamento distribuído para grandes volumes
- **MinIO**: Storage S3-compatible, escalável e econômico
- **PostgreSQL**: OLAP otimizado para consultas analíticas
- **Metabase**: BI open-source com interface intuitiva
- **Docker**: Containerização para portabilidade e escalabilidade

> 🔧 **Para detalhes completos das tecnologias e decisões técnicas, consulte [5. Tecnologias e Ferramentas](#5-tecnologias-e-ferramentas)**

## 3. Escopo da Solução

### 3.1 Incluído no Escopo
- Pipeline de ingestão de dados CSV
- Processamento batch com Spark
- Data Lake com 4 camadas (Raw/Bronze/Silver/Gold)
- Armazenamento em MinIO (S3-compatible)
- Banco PostgreSQL para consultas OLAP
- Dashboards no Metabase
- Análise exploratória em Jupyter
- Documentação completa
- Scripts de automação

### 3.2 Não Incluído no Escopo
- Ingestão em tempo real (streaming)
- APIs REST para consulta de dados
- Autenticação e autorização avançada
- Monitoramento e alertas automatizados
- Backup e disaster recovery automatizado
- Integração com sistemas externos (CRM, ERP)

### 3.3 Limitações Conhecidas
- Processamento apenas batch (não streaming)
- Dados sintéticos (não reais)
- Ambiente single-node (não cluster)
- Sem alta disponibilidade
- Segurança básica (desenvolvimento)

> ⚠️ **Para informações sobre pontos de falha e mitigações, veja [8. Pontos de Falha e Limitações](#8-pontos-de-falha-e-limitações)**

## 4. Arquitetura Detalhada

### 4.1 Visão Geral
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    CSV      │─▶│   Python    │─▶│    Spark    │─▶│   MinIO     │
│  (Fonte)    │  │ (Ingestão)  │  │(Processam.) │  │(Data Lake)  │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
                                                           │
┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  Metabase   │◀─│ PostgreSQL  │◀─│ Exportação  │◀────────┘
│(Dashboards) │  │   (OLAP)    │  │ (Pipeline)  │
└─────────────┘  └─────────────┘  └─────────────┘
```

### 4.2 Componentes Principais

#### Ingestão (Python + Pandas)
- **Função**: Coleta e validação inicial
- **Entrada**: Arquivos CSV
- **Validações**: Tipos, integridade, completude
- **Saída**: Dados validados para processamento

#### Processamento (Apache Spark)
- **Função**: ETL distribuído
- **Transformações**: Limpeza, agregações, cálculos
- **Otimizações**: Cache, particionamento, broadcast joins
- **Paralelização**: Multi-core processing

#### Armazenamento (MinIO Data Lake)
- **Raw**: Dados originais (backup/auditoria)
- **Bronze**: Dados limpos e padronizados
- **Silver**: Agregações e métricas intermediárias
- **Gold**: KPIs e dados para consumo final

#### Análise (PostgreSQL + Metabase)
- **PostgreSQL**: OLAP para consultas rápidas
- **Metabase**: Dashboards e relatórios visuais
- **Jupyter**: Análise exploratória e prototipagem

### 4.3 Fluxo de Dados Detalhado

1. **Ingestão Raw**:
   - Leitura de CSV com validação
   - Conversão para Parquet
   - Armazenamento em `raw-data/`

2. **Processamento Bronze**:
   - Filtros de qualidade (valores válidos)
   - Padronização de tipos de dados
   - Adição de metadados (timestamp)
   - Armazenamento em `bronze-data/`

3. **Processamento Silver**:
   - Agregações por categoria/período
   - Cálculo de métricas de clientes
   - Performance de produtos
   - Armazenamento em `silver-data/`

4. **Processamento Gold**:
   - KPIs principais de negócio
   - Top produtos/categorias
   - Tendências temporais
   - Armazenamento em `gold-data/` + PostgreSQL

5. **Visualização**:
   - Consultas otimizadas no PostgreSQL
   - Dashboards interativos no Metabase
   - Análises ad-hoc no Jupyter

> 🚀 **Para executar este pipeline, siga o [Guia de Execução](guia_execucao.md)**

## 5. Tecnologias e Ferramentas

### 5.1 Stack Tecnológico

| Componente | Tecnologia | Versão | Justificativa |
|------------|------------|--------|---------------|
| Processamento | Apache Spark | 3.4 | Escalabilidade, performance |
| Storage | MinIO | Latest | S3-compatible, open-source |
| Database | PostgreSQL | 13 | OLAP, performance analítica |
| BI | Metabase | Latest | Open-source, fácil uso |
| Linguagem | Python | 3.9+ | Ecossistema data science |
| Orquestração | Docker Compose | 2.0+ | Portabilidade, isolamento |

### 5.2 Bibliotecas Python

| Biblioteca | Versão | Uso |
|------------|--------|-----|
| pandas | 2.1.4 | Manipulação de dados |
| pyspark | 3.4.1 | Processamento distribuído |
| boto3 | 1.34.0 | Integração com MinIO/S3 |
| psycopg2 | 2.9.9 | Conexão PostgreSQL |
| matplotlib | 3.7.2 | Visualizações |
| seaborn | 0.12.2 | Gráficos estatísticos |
| jupyter | 1.0.0 | Análise interativa |

### 5.3 Decisões Técnicas

#### Por que Spark?
- **Prós**: Escalabilidade, performance, ecossistema
- **Contras**: Complexidade, overhead para pequenos dados
- **Alternativas**: Pandas (limitado), Dask (menos maduro)
- **Decisão**: Spark pela escalabilidade futura

#### Por que MinIO?
- **Prós**: S3-compatible, open-source, performance
- **Contras**: Menos features que AWS S3
- **Alternativas**: HDFS (complexo), filesystem local (não escalável)
- **Decisão**: MinIO pela compatibilidade e simplicidade

#### Por que PostgreSQL?
- **Prós**: Performance OLAP, SQL padrão, confiabilidade
- **Contras**: Não é columnar nativo
- **Alternativas**: ClickHouse (menos conhecido), BigQuery (cloud-only)
- **Decisão**: PostgreSQL pela maturidade e facilidade

#### Por que Metabase?
- **Prós**: Open-source, interface intuitiva, fácil setup
- **Contras**: Menos features que Power BI/Tableau
- **Alternativas**: Grafana (mais técnico), Superset (mais complexo)
- **Decisão**: Metabase pelo equilíbrio simplicidade/funcionalidade

> 🏗️ **Para ver a arquitetura completa do sistema, consulte [arquitetura.md](arquitetura.md)**

## 6. Dados e Schema

### 6.1 Fonte de Dados
- **Formato**: CSV
- **Volume**: 10.000 registros (exemplo)
- **Período**: 2023-2024
- **Atualização**: Batch diário (simulado)

### 6.2 Schema dos Dados

#### Tabela Principal (sales_data)
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

#### Dicionário de Dados

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| order_id | String | ID único do pedido | ORD_000001 |
| customer_id | Integer | Identificador do cliente | 1001 |
| customer_segment | String | Categoria do cliente | Premium |
| product_name | String | Nome do produto | Smartphone |
| category | String | Categoria do produto | Eletrônicos |
| price | Decimal | Preço unitário em R$ | 899.99 |
| quantity | Integer | Quantidade comprada | 2 |
| total_amount | Decimal | Valor total da linha | 1799.98 |
| sale_date | Date | Data da transação | 2024-01-15 |
| rating | Decimal | Avaliação 1-5 | 4.5 |

### 6.3 Qualidade dos Dados

#### Validações Implementadas
- **Valores obrigatórios**: Todos os campos são required
- **Tipos de dados**: Validação de tipos numéricos e datas
- **Ranges**: Preços > 0, Quantity > 0, Rating 1-5
- **Consistência**: total_amount = price * quantity

#### Métricas de Qualidade
- **Completude**: % de campos preenchidos
- **Validade**: % de registros que passam nas validações
- **Consistência**: % de registros com cálculos corretos
- **Unicidade**: % de order_ids únicos

> 📊 **Para ver análises dos dados gerados, execute o notebook [exploratory_analysis.ipynb](../notebooks/exploratory_analysis.ipynb)**

## 7. Governança e Qualidade

### 7.1 Catalogação de Dados
- **Metadados**: Schema, tipos, descrições
- **Linhagem**: Origem → Transformações → Destino
- **Documentação**: Este documento + comentários no código
- **Versionamento**: Git para código, schema evolution para dados

### 7.2 Controle de Qualidade
- **Validação na ingestão**: Tipos, ranges, obrigatoriedade
- **Monitoramento**: Logs de pipeline, métricas de execução
- **Alertas**: Falhas de processamento (manual por enquanto)
- **Auditoria**: Logs de transformações, timestamps

> 🔍 **Para troubleshooting e resolução de problemas, consulte [guia_execucao.md](guia_execucao.md#6-troubleshooting)**

### 7.3 Segurança
- **Acesso**: Credenciais básicas por serviço
- **Rede**: Isolamento via Docker network
- **Dados**: Sem dados sensíveis (sintéticos)
- **Logs**: Não exposição de credenciais

> 🔒 **Para melhorias de segurança em produção, veja [10. Melhorias Futuras](#10-melhorias-futuras)**

## 8. Pontos de Falha e Limitações

### 8.1 Pontos de Falha Identificados

#### Infraestrutura
- **Docker**: Falha de containers, recursos insuficientes
- **Rede**: Perda de conectividade entre serviços
- **Storage**: Espaço em disco insuficiente
- **Memória**: OOM em processamento de grandes volumes

#### Pipeline
- **Dados corrompidos**: CSV malformado, encoding incorreto
- **Schema changes**: Mudanças na estrutura dos dados
- **Dependências**: Falha em bibliotecas Python/Spark
- **Conectividade**: Falha de conexão com MinIO/PostgreSQL

### 8.2 Limitações Atuais

#### Técnicas
- **Escalabilidade**: Single-node, não cluster
- **Performance**: Sem otimizações avançadas (índices, particionamento)
- **Disponibilidade**: Sem redundância ou failover
- **Monitoramento**: Manual, sem alertas automáticos

#### Funcionais
- **Dados**: Sintéticos, não refletem realidade
- **Tempo real**: Apenas batch, sem streaming
- **Integração**: Sem APIs ou conectores externos
- **Segurança**: Básica, não adequada para produção

### 8.3 Mitigações Implementadas
- **Validação de dados**: Filtros de qualidade
- **Logs detalhados**: Para troubleshooting
- **Containerização**: Isolamento e portabilidade
- **Documentação**: Guias de execução e troubleshooting

> 🛠️ **Para soluções de problemas comuns, consulte [guia_execucao.md](guia_execucao.md#6-troubleshooting)**

## 9. Trabalho Individual

### 9.1 Responsabilidades por Integrante

#### Bruno Rocha
- **Arquitetura geral**: Design do pipeline e componentes
- **Processamento de dados**: Implementação Spark, transformações
- **Data Lake**: Estrutura de camadas, formatos de dados
- **Infraestrutura**: Docker Compose, configurações
- **Documentação**: Arquitetura, guias técnicos

#### Allison Henrique
- **Análise de dados**: Jupyter notebooks, estatísticas
- **Visualização**: Dashboards Metabase, KPIs
- **Validação**: Testes de qualidade, validação de resultados
- **Documentação**: Análises, insights de negócio

### 9.2 Conhecimentos Demonstrados
- **Big Data**: Spark, Data Lake, processamento distribuído
- **Engenharia de Dados**: ETL, pipeline design, formatos otimizados
- **Infraestrutura**: Docker, orquestração de serviços
- **Arquitetura**: Design de sistemas, trade-offs técnicos

#### Preparação para Perguntas Individuais
1. **Spark**: Por que usar? Como funciona? Otimizações?
2. **Data Lake**: Camadas, formatos, governança
3. **Pipeline**: Fluxo de dados, tratamento de erros
4. **Arquitetura**: Componentes, comunicação, escalabilidade
5. **Decisões técnicas**: Trade-offs, alternativas consideradas



## 10. Melhorias Futuras

### 10.1 Curto Prazo (1-3 meses)
- **Agendamento**: Airflow para orquestração
- **Monitoramento**: Prometheus + Grafana
- **Testes**: Unitários e integração
- **CI/CD**: Pipeline automatizado

### 10.2 Médio Prazo (3-6 meses)
- **Streaming**: Kafka + Spark Streaming
- **APIs**: REST endpoints para dados
- **ML**: Modelos preditivos (churn, recomendação)
- **Segurança**: Autenticação, criptografia

### 10.3 Longo Prazo (6+ meses)
- **Cloud**: Migração para AWS/Azure/GCP
- **Cluster**: Spark/Hadoop distribuído
- **Data Mesh**: Arquitetura descentralizada
- **Real-time**: Dashboards em tempo real

> 🚀 **Para roadmap detalhado de evolução, consulte [RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md#evolução-futura)**

## 11. Conclusão

Este projeto demonstra uma implementação completa de pipeline de dados moderno, seguindo boas práticas de Engenharia de Dados e arquitetura de Data Lake. A solução é escalável, bem documentada e serve como base sólida para evolução futura.

Os principais diferenciais são:
- Arquitetura em camadas bem definida
- Uso de tecnologias modernas e escaláveis
- Documentação completa e executável
- Código limpo e bem estruturado
- Consideração de aspectos de produção (governança, qualidade, monitoramento)

A implementação demonstra domínio técnico em Big Data, Ciência de Dados e Engenharia de Software, preparando para cenários reais de mercado.

> 🏆 **Para visão geral executiva e checklist final, consulte [RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)**

---

## 🗺️ Navegação Rápida

- **🏠 Início**: [README.md](../README.md)
- **🏗️ Arquitetura**: [arquitetura.md](arquitetura.md)
- **🚀 Execução**: [guia_execucao.md](guia_execucao.md)

- **📊 Análise**: [../notebooks/exploratory_analysis.ipynb](../notebooks/exploratory_analysis.ipynb)
- **💼 Resumo**: [../RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)ões, timestamps

### 7.3 Segurança
- **Acesso**: Credenciais básicas por serviço
- **Rede**: Isolamento via Docker network
- **Dados**: Sem dados sensíveis (sintéticos)
- **Logs**: Não exposição de credenciais

## 8. Pontos de Falha e Limitações

### 8.1 Pontos de Falha Identificados

#### Infraestrutura
- **Docker**: Falha de containers, recursos insuficientes
- **Rede**: Perda de conectividade entre serviços
- **Storage**: Espaço em disco insuficiente
- **Memória**: OOM em processamento de grandes volumes

#### Pipeline
- **Dados corrompidos**: CSV malformado, encoding incorreto
- **Schema changes**: Mudanças na estrutura dos dados
- **Dependências**: Falha em bibliotecas Python/Spark
- **Conectividade**: Falha de conexão com MinIO/PostgreSQL

### 8.2 Limitações Atuais

#### Técnicas
- **Escalabilidade**: Single-node, não cluster
- **Performance**: Sem otimizações avançadas (índices, particionamento)
- **Disponibilidade**: Sem redundância ou failover
- **Monitoramento**: Manual, sem alertas automáticos

#### Funcionais
- **Dados**: Sintéticos, não refletem realidade
- **Tempo real**: Apenas batch, sem streaming
- **Integração**: Sem APIs ou conectores externos
- **Segurança**: Básica, não adequada para produção

### 8.3 Mitigações Implementadas
- **Validação de dados**: Filtros de qualidade
- **Logs detalhados**: Para troubleshooting
- **Containerização**: Isolamento e portabilidade
- **Documentação**: Guias de execução e troubleshooting

## 9. Trabalho Individual

### 9.1 Responsabilidades por Integrante

####  Bruno Rocha
- **Arquitetura geral**: Design do pipeline e componentes
- **Processamento de dados**: Implementação Spark, transformações
- **Data Lake**: Estrutura de camadas, formatos de dados
- **Infraestrutura**: Docker Compose, configurações
- **Documentação**: Arquitetura, guias técnicos

#### Allison Henrique
- **Análise de dados**: Jupyter notebooks, estatísticas
- **Visualização**: Dashboards Metabase, KPIs
- **Validação**: Testes de qualidade, validação de resultados
- **Documentação**: Análises, insights de negócio

### 9.2 Conhecimentos Demonstrados

#### Bruno Rocha
- **Big Data**: Spark, Data Lake, processamento distribuído
- **Engenharia de Dados**: ETL, pipeline design, formatos otimizados
- **Infraestrutura**: Docker, orquestração de serviços
- **Arquitetura**: Design de sistemas, trade-offs técnicos

#### Preparação para Perguntas Individuais
1. **Spark**: Por que usar? Como funciona? Otimizações?
2. **Data Lake**: Camadas, formatos, governança
3. **Pipeline**: Fluxo de dados, tratamento de erros
4. **Arquitetura**: Componentes, comunicação, escalabilidade
5. **Decisões técnicas**: Trade-offs, alternativas consideradas

## 10. Melhorias Futuras

### 10.1 Curto Prazo (1-3 meses)
- **Agendamento**: Airflow para orquestração
- **Monitoramento**: Prometheus + Grafana
- **Testes**: Unitários e integração
- **CI/CD**: Pipeline automatizado

### 10.2 Médio Prazo (3-6 meses)
- **Streaming**: Kafka + Spark Streaming
- **APIs**: REST endpoints para dados
- **ML**: Modelos preditivos (churn, recomendação)
- **Segurança**: Autenticação, criptografia

### 10.3 Longo Prazo (6+ meses)
- **Cloud**: Migração para AWS/Azure/GCP
- **Cluster**: Spark/Hadoop distribuído
- **Data Mesh**: Arquitetura descentralizada
- **Real-time**: Dashboards em tempo real

## 11. Conclusão

Este projeto demonstra uma implementação completa de pipeline de dados moderno, seguindo boas práticas de Engenharia de Dados e arquitetura de Data Lake. A solução é escalável, bem documentada e serve como base sólida para evolução futura.

Os principais diferenciais são:
- Arquitetura em camadas bem definida
- Uso de tecnologias modernas e escaláveis
- Documentação completa e executável
- Código limpo e bem estruturado
- Consideração de aspectos de produção (governança, qualidade, monitoramento)

A implementação demonstra domínio técnico em Big Data, Ciência de Dados e Engenharia de Software, preparando para cenários reais de mercado.