import subprocess
import sys

def install_package(package):
    """Instala um pacote Python usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[OK] {package} instalado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Erro ao instalar {package}: {e}")
        return False

def main():
    """Instala dependências essenciais uma por vez"""
    print("=== Instalando Dependências Essenciais ===")
    
    # Lista de pacotes essenciais (sem Spark por enquanto)
    essential_packages = [
        "pandas",
        "numpy", 
        "boto3",
        "psycopg2-binary"
    ]
    
    success_count = 0
    
    for package in essential_packages:
        print(f"\nInstalando {package}...")
        if install_package(package):
            success_count += 1
    
    print(f"\n=== Resultado ===")
    print(f"Pacotes instalados: {success_count}/{len(essential_packages)}")
    
    if success_count == len(essential_packages):
        print("[OK] Todas as dependencias essenciais foram instaladas!")
        print("Voce pode executar: python pipeline_simple.py")
    else:
        print("[AVISO] Algumas dependencias falharam. Tente instalar manualmente.")
    
    # Tentar instalar PySpark separadamente (opcional)
    print("\n=== Tentando instalar PySpark (opcional) ===")
    if install_package("pyspark"):
        print("[OK] PySpark instalado! Voce pode usar o pipeline completo.")
    else:
        print("[ERRO] PySpark falhou. Use o pipeline_simple.py por enquanto.")

if __name__ == "__main__":
    main()