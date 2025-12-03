# 📚 Índice Geral da Documentação

## 🎯 Navegação Rápida por Objetivo

### 🚀 **Quero executar o projeto**
1. **[Guia de Execução](guia_execucao.md)** - Passo a passo completo
2. **[RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)** - 3 comandos para rodar tudo
3. **[setup.bat](../setup.bat)** - Script automático de instalação

### 📖 **Quero entender a arquitetura**
1. **[Arquitetura](arquitetura.md)** - Diagramas e componentes detalhados
2. **[Documentação Completa](documentacao_completa.md)** - Visão técnica completa
3. **[README.md](../README.md)** - Visão geral do projeto

### 🎤 **Quero me preparar para apresentação**
1. **[RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)** - Pontos principais
2. **[Documentação Completa](documentacao_completa.md)** - Base técnica

### 📊 **Quero ver análises dos dados**
1. **[Notebook de Análise](../notebooks/exploratory_analysis.ipynb)** - Jupyter com gráficos
2. **[Dados Gerados](../datasets/sales_data.csv)** - 10k registros sintéticos
3. **[Pipeline de Processamento](../src/pipeline.py)** - Código principal

---

## 📁 Estrutura Completa dos Documentos

### 📋 **Documentação Principal**
- **[README.md](../README.md)** - Porta de entrada do projeto
- **[RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)** - Visão executiva para apresentação
- **[Documentação Completa](documentacao_completa.md)** - Documento técnico principal

### 🏗️ **Documentação Técnica**
- **[Arquitetura](arquitetura.md)** - Design do sistema e componentes
- **[Guia de Execução](guia_execucao.md)** - Como rodar o projeto


### 💻 **Código e Configurações**
- **[Pipeline Principal](../src/pipeline.py)** - ETL completo com Spark
- **[Gerador de Dados](../src/generate_data.py)** - Criação de dados sintéticos
- **[Docker Compose](../infra/docker-compose.yml)** - Infraestrutura completa
- **[Requirements](../requirements.txt)** - Dependências Python

### 📊 **Análises e Dados**
- **[Análise Exploratória](../notebooks/exploratory_analysis.ipynb)** - Jupyter notebook
- **[Dados de Exemplo](../datasets/sales_data.csv)** - Dataset sintético
- **[Script SQL](../infra/init.sql)** - Inicialização do banco

### 🛠️ **Utilitários**
- **[Setup Automático](../setup.bat)** - Instalação com 1 comando
- **[Este Índice](INDICE.md)** - Navegação da documentação

---

## 🎯 Fluxo de Leitura Recomendado

### 👨‍🎓 **Para Estudar (1ª vez)**
1. **[README.md](../README.md)** - Entender o projeto
2. **[Documentação Completa](documentacao_completa.md)** - Base técnica
3. **[Arquitetura](arquitetura.md)** - Design detalhado
4. **[Guia de Execução](guia_execucao.md)** - Como funciona

### 🚀 **Para Executar**
1. **[RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)** - Checklist rápido
2. **[Guia de Execução](guia_execucao.md)** - Passo a passo
3. **[Troubleshooting](guia_execucao.md#6-troubleshooting)** - Se algo der errado

### 🎤 **Para Apresentar**
1. **[RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)** - Pontos principais
2. **[Documentação Completa](documentacao_completa.md)** - Referência técnica

---

## 🔍 Busca Rápida por Tópico

### 🏗️ **Arquitetura e Design**
- [Diagrama de Componentes](arquitetura.md#1-visão-geral-da-arquitetura)
- [Camadas do Data Lake](arquitetura.md#23-camada-de-armazenamento-data-lake)
- [Fluxo de Dados](arquitetura.md#4-fluxo-de-dados)
- [Decisões Técnicas](documentacao_completa.md#53-decisões-técnicas)

### 💻 **Implementação**
- [Pipeline Spark](../src/pipeline.py)
- [Configuração Docker](../infra/docker-compose.yml)
- [Processamento de Dados](documentacao_completa.md#43-fluxo-de-dados-detalhado)
- [Tecnologias Utilizadas](documentacao_completa.md#5-tecnologias-e-ferramentas)

### 📊 **Dados e Análises**
- [Schema dos Dados](documentacao_completa.md#62-schema-dos-dados)
- [Qualidade dos Dados](documentacao_completa.md#63-qualidade-dos-dados)
- [Análise Exploratória](../notebooks/exploratory_analysis.ipynb)
- [KPIs e Métricas](documentacao_completa.md#43-fluxo-de-dados-detalhado)

### 🛠️ **Operação**
- [Como Executar](guia_execucao.md#3-execução-passo-a-passo)
- [Troubleshooting](guia_execucao.md#6-troubleshooting)
- [Monitoramento](arquitetura.md#7-monitoramento)
- [Backup e Recovery](arquitetura.md#8-disaster-recovery)

### 🎓 **Apresentação**
- [Pontos Fortes](RESUMO_EXECUTIVO.md#diferenciais-do-projeto)
- [Resumo Executivo](../RESUMO_EXECUTIVO.md)
- [Documentação Técnica](documentacao_completa.md)

---

## 📞 Links Úteis Durante Execução

### 🌐 **Interfaces Web**
- **MinIO Console**: http://localhost:9001 (admin/password123)
- **Spark UI**: http://localhost:8080
- **Metabase**: http://localhost:3000
- **PostgreSQL**: localhost:5432 (postgres/postgres123)

### 🔧 **Comandos Essenciais**
```bash
# Status dos containers
docker-compose ps

# Executar pipeline
python src/pipeline.py

# Logs de troubleshooting
docker-compose logs

# Jupyter notebook
jupyter notebook notebooks/
```

### 📋 **Checklist de Validação**
- [ ] Containers rodando: `docker-compose ps`
- [ ] Dados gerados: `ls datasets/`
- [ ] Pipeline executado: `python src/pipeline.py`
- [ ] MinIO acessível: http://localhost:9001
- [ ] PostgreSQL com dados: `docker exec -it postgres psql -U postgres -d sales_db`

---

## 🎯 **Mensagem Final**

Esta documentação foi estruturada para ser **autoexplicativa** e **navegável**. Cada documento tem links para os outros, facilitando o estudo e a preparação.

**Para sua prova:**
1. **Execute** o projeto seguindo o [RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)
2. **Estude** a [Documentação Completa](documentacao_completa.md)
3. **Prepare-se** com o [Resumo Executivo](../RESUMO_EXECUTIVO.md)

**Você tem um projeto completo, funcional e bem documentado! 🚀**