# Sistema de Análise de Vendas E-commerce
## Pipeline de Dados para Análise de Performance de Vendas

### 📋 Visão Geral
Este projeto implementa um pipeline completo de dados para análise de vendas de e-commerce, desde a ingestão até a visualização de insights de negócio.

### 🎯 Problema Abordado
Análise de performance de vendas, identificação de produtos mais vendidos, sazonalidade e comportamento de clientes para tomada de decisão estratégica.

> 📋 **Para detalhes completos do problema e objetivos, veja [docs/documentacao_completa.md](docs/documentacao_completa.md#1-descrição-do-problema)**

### 🏗️ Arquitetura
```
Dados CSV → Ingestão (Python) → Processamento (Spark) → Data Lake (MinIO) → Visualização (Metabase)
```

> 🏛️ **Para arquitetura detalhada com diagramas e justificativas, consulte [docs/arquitetura.md](docs/arquitetura.md)**

### 🚀 Como Executar

1. **Pré-requisitos:**
   - Docker e Docker Compose
   - Python 3.9+

2. **Executar o projeto:**
   ```bash
   # Subir infraestrutura
   docker-compose up -d
   
   # Executar pipeline
   python src/pipeline.py
   
   # Acessar dashboards
   # Metabase: http://localhost:3000
   # MinIO: http://localhost:9001
   ```

> 📖 **Para guia completo passo a passo, veja [docs/guia_execucao.md](docs/guia_execucao.md)**

### 📁 Estrutura do Projeto
```
├── docs/           # Documentação completa
├── src/            # Código-fonte do pipeline
├── infra/          # Docker Compose e configs
├── notebooks/      # Análise exploratória
├── datasets/       # Dados de exemplo
└── README.md       # Este arquivo
```

### 👥 Equipe
- **BRUNO**: Arquitetura geral e processamento de dados
- **ALLISON**: Visualização e análise de dados

> 👨‍💼 **Para detalhes das responsabilidades individuais, consulte [docs/documentacao_completa.md](docs/documentacao_completa.md#9-trabalho-individual)**

### 🔧 Tecnologias Utilizadas
- **Ingestão**: Python, Pandas
- **Processamento**: Apache Spark
- **Armazenamento**: MinIO (S3-compatible)
- **Visualização**: Metabase
- **Orquestração**: Docker Compose

> 🛠️ **Para justificativas técnicas e alternativas consideradas, veja [docs/documentacao_completa.md](docs/documentacao_completa.md#5-tecnologias-e-ferramentas)**

---

## 📚 Documentação Completa

- 📋 **[Documentação Completa](docs/documentacao_completa.md)** - Visão geral técnica e de negócio
- 🏛️ **[Arquitetura](docs/arquitetura.md)** - Diagramas e componentes detalhados
- 🚀 **[Guia de Execução](docs/guia_execucao.md)** - Passo a passo para rodar o projeto
- 📊 **[Análise Exploratória](notebooks/exploratory_analysis.ipynb)** - Jupyter notebook com insights
- 📈 **[Resumo Executivo](RESUMO_EXECUTIVO.md)** - Visão geral para apresentação

## 🚀 Início Rápido

```bash
# 1. Execute o setup automático
setup.bat

# 2. Execute o pipeline
python src/pipeline.py

# 3. Acesse os resultados
# MinIO: http://localhost:9001 (admin/password123)
# Metabase: http://localhost:3000
```

> ⚡ **Para troubleshooting, consulte [docs/guia_execucao.md](docs/guia_execucao.md#6-troubleshooting)**