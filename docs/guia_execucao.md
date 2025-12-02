# Guia de Execução do Projeto

## 1. Pré-requisitos

### 1.1 Software Necessário
- **Docker Desktop**: Versão 4.0+
- **Docker Compose**: Versão 2.0+
- **Python**: Versão 3.9+
- **Git**: Para versionamento

### 1.2 Recursos Mínimos
- **RAM**: 8GB (recomendado 16GB)
- **Storage**: 10GB livres
- **CPU**: 4 cores (recomendado)

### 1.3 Verificação do Ambiente
```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Python
python --version
pip --version

# Verificar portas disponíveis
netstat -an | findstr "3000 5432 8080 9000 9001"
```

> 📋 **Para detalhes sobre as tecnologias utilizadas, consulte [documentacao_completa.md](documentacao_completa.md#5-tecnologias-e-ferramentas)**

## 2. Instalação e Configuração

### 2.1 Clone do Repositório
```bash
git clone <url-do-repositorio>
cd prova-ciencia-dados
```

### 2.2 Instalação de Dependências Python
```bash
# Criar ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install pandas numpy pyspark boto3 psycopg2-binary jupyter matplotlib seaborn
```

### 2.3 Configuração de Variáveis de Ambiente
```bash
# Criar arquivo .env (opcional)
echo MINIO_ROOT_USER=admin > .env
echo MINIO_ROOT_PASSWORD=password123 >> .env
echo POSTGRES_PASSWORD=postgres123 >> .env
```

> 🔒 **Para informações sobre segurança e credenciais, veja [documentacao_completa.md](documentacao_completa.md#73-segurança)**

## 3. Execução Passo a Passo

### 3.1 Subir a Infraestrutura
```bash
# Navegar para o diretório de infraestrutura
cd infra

# Subir todos os serviços
docker-compose up -d

# Verificar se todos os containers estão rodando
docker-compose ps
```

**Saída esperada:**
```
NAME                IMAGE                     STATUS
minio               minio/minio:latest        Up
metabase            metabase/metabase:latest  Up
postgres            postgres:13               Up
spark-master        bitnami/spark:3.4         Up
spark-worker        bitnami/spark:3.4         Up
```

### 3.2 Aguardar Inicialização dos Serviços
```bash
# Aguardar ~2-3 minutos para todos os serviços iniciarem
# Verificar logs se necessário
docker-compose logs -f metabase
```

### 3.3 Gerar Dados de Exemplo
```bash
# Voltar para o diretório raiz
cd ..

# Executar geração de dados
python src/generate_data.py
```

**Saída esperada:**
```
Dados gerados: 10000 registros salvos em datasets/sales_data.csv
Estatísticas dos dados gerados:
Período: 2023-01-01 a 2024-12-31
Total de vendas: R$ 15,234,567.89
Categorias: 6
Produtos únicos: 30
Clientes únicos: 2000
```

### 3.4 Executar Pipeline de Dados
```bash
# Executar pipeline completo
python src/pipeline.py
```

**Saída esperada:**
```
=== Iniciando Pipeline de Dados ===
Bucket 'raw-data' criado com sucesso
Bucket 'bronze-data' criado com sucesso
Bucket 'silver-data' criado com sucesso
Bucket 'gold-data' criado com sucesso
Iniciando ingestão de dados...
Dados carregados: 10000 registros
Dados salvos na camada RAW
Processando camada Bronze...
Dados processados na camada Bronze
Processando camada Silver...
Dados processados na camada Silver
Processando camada Gold...
Dados processados na camada Gold
Exportando dados para PostgreSQL...
Dados exportados para PostgreSQL com sucesso
=== Pipeline executado com sucesso! ===
```

## 4. Verificação e Acesso aos Serviços

### 4.1 MinIO (Data Lake)
- **URL**: http://localhost:9001
- **Usuário**: admin
- **Senha**: password123

**Verificações:**
- Buckets criados: raw-data, bronze-data, silver-data, gold-data
- Arquivos Parquet em cada bucket

### 4.2 Spark UI
- **URL**: http://localhost:8080
- **Verificações**: Jobs executados, workers ativos

### 4.3 PostgreSQL
```bash
# Conectar via linha de comando
docker exec -it postgres psql -U postgres -d sales_db

# Verificar tabelas
\dt

# Verificar dados
SELECT COUNT(*) FROM sales_summary;
SELECT COUNT(*) FROM customer_metrics;
SELECT COUNT(*) FROM product_performance;
```

### 4.4 Metabase
- **URL**: http://localhost:3000
- **Configuração inicial**: Seguir wizard de setup
- **Banco**: PostgreSQL (host: postgres, porta: 5432, db: sales_db)

> 📊 **Para análises detalhadas dos dados, execute [../notebooks/exploratory_analysis.ipynb](../notebooks/exploratory_analysis.ipynb)**

## 5. Análise Exploratória

### 5.1 Jupyter Notebook
```bash
# Instalar Jupyter se não instalado
pip install jupyter

# Iniciar Jupyter
jupyter notebook notebooks/

# Abrir: exploratory_analysis.ipynb
```

### 5.2 Executar Análises
- Executar todas as células do notebook
- Verificar gráficos e estatísticas geradas
- Salvar resultados

## 6. Troubleshooting

### 6.1 Problemas Comuns

#### Containers não sobem
```bash
# Verificar portas em uso
netstat -an | findstr "3000 5432 8080 9000"

# Parar containers conflitantes
docker stop $(docker ps -q)

# Limpar recursos Docker
docker system prune -f
```

#### Erro de conexão com MinIO
```bash
# Verificar se MinIO está rodando
docker logs minio

# Recriar buckets manualmente
docker exec -it minio mc mb /data/raw-data
```

#### Erro no pipeline Spark
```bash
# Verificar logs do Spark
docker logs spark-master
docker logs spark-worker

# Reiniciar serviços Spark
docker-compose restart spark-master spark-worker
```

#### PostgreSQL não aceita conexões
```bash
# Verificar logs
docker logs postgres

# Verificar se banco foi criado
docker exec -it postgres psql -U postgres -l
```

### 6.2 Logs Úteis
```bash
# Logs de todos os serviços
docker-compose logs

# Logs específicos
docker-compose logs minio
docker-compose logs postgres
docker-compose logs metabase
```

### 6.3 Reinicialização Completa
```bash
# Parar todos os serviços
docker-compose down

# Remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Subir novamente
docker-compose up -d
```

## 7. Validação Final

### 7.1 Checklist de Verificação
- [ ] Todos os containers estão rodando
- [ ] Buckets MinIO criados com dados
- [ ] Tabelas PostgreSQL populadas
- [ ] Metabase acessível e configurado
- [ ] Notebook executado sem erros
- [ ] Pipeline completo executado

### 7.2 Testes de Funcionalidade
```bash
# Teste 1: Verificar dados no MinIO
curl -X GET "http://admin:password123@localhost:9000/raw-data/"

# Teste 2: Verificar dados no PostgreSQL
docker exec -it postgres psql -U postgres -d sales_db -c "SELECT COUNT(*) FROM sales_summary;"

# Teste 3: Verificar Metabase
curl -I http://localhost:3000
```

> ✅ **Para checklist completo de validação, consulte [../RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md#checklist-final)**

## 8. Parada do Sistema

### 8.1 Parada Controlada
```bash
# Parar serviços mantendo dados
docker-compose stop

# Parar e remover containers (mantém volumes)
docker-compose down
```

### 8.2 Limpeza Completa
```bash
# Remover tudo (containers, volumes, redes)
docker-compose down -v --remove-orphans

# Limpar imagens não utilizadas
docker image prune -f
```

## 9. Próximos Passos

### 9.1 Melhorias Sugeridas
- Implementar agendamento com Airflow
- Adicionar monitoramento com Prometheus
- Configurar alertas automáticos
- Implementar testes automatizados

### 9.2 Produção
- Configurar backup automático
- Implementar alta disponibilidade
- Configurar SSL/TLS
- Implementar autenticação robusta

> 🚀 **Para roadmap completo de melhorias, veja [documentacao_completa.md](documentacao_completa.md#10-melhorias-futuras)**

---

## 🗺️ Navegação

- **🏠 Voltar ao Início**: [../README.md](../README.md)
- **📋 Documentação Completa**: [documentacao_completa.md](documentacao_completa.md)
- **🏗️ Arquitetura**: [arquitetura.md](arquitetura.md)
- **🎓 Dicas de Apresentação**: [dicas_apresentacao.md](dicas_apresentacao.md)
- **📈 Resumo Executivo**: [../RESUMO_EXECUTIVO.md](../RESUMO_EXECUTIVO.md)