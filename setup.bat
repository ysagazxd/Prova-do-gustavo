@echo off
echo ========================================
echo    Setup do Projeto de Ciencia de Dados
echo ========================================

echo.
echo [1/6] Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Docker nao encontrado. Instale o Docker Desktop primeiro.
    pause
    exit /b 1
)
echo Docker OK

echo.
echo [2/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado. Instale Python 3.9+ primeiro.
    pause
    exit /b 1
)
echo Python OK

echo.
echo [3/6] Instalando dependencias Python...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha na instalacao das dependencias.
    pause
    exit /b 1
)

echo.
echo [4/6] Subindo infraestrutura Docker...
cd infra
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERRO: Falha ao subir containers Docker.
    pause
    exit /b 1
)
cd ..

echo.
echo [5/6] Aguardando servicos iniciarem...
timeout /t 30 /nobreak >nul

echo.
echo [6/6] Gerando dados de exemplo...
python src\generate_data.py
if %errorlevel% neq 0 (
    echo ERRO: Falha na geracao de dados.
    pause
    exit /b 1
)

echo.
echo ========================================
echo           SETUP CONCLUIDO!
echo ========================================
echo.
echo Servicos disponiveis:
echo - MinIO Console: http://localhost:9001
echo - Spark UI: http://localhost:8080  
echo - Metabase: http://localhost:3000
echo.
echo Para executar o pipeline:
echo   python src\pipeline.py
echo.
echo Para abrir notebook:
echo   jupyter notebook notebooks\
echo.
pause