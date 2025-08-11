#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Criar Executável do Processador Automático
=====================================================

Este script cria um executável do processador automático
usando PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def instalar_pyinstaller():
    """Instala o PyInstaller se não estiver instalado."""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller instalado com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar PyInstaller")
            return False

def criar_executavel():
    """Cria o executável do processador automático."""
    print("🔨 Criando executável...")
    
    # Configuração do PyInstaller
    comando = [
        "pyinstaller",
        "--onefile",                    # Criar um único arquivo executável
        "--console",                    # Mostrar console para logs
        "--name=ProcessadorBiblioteca", # Nome do executável
        "--hidden-import=pandas",       # Incluir pandas
        "--hidden-import=openpyxl",     # Incluir openpyxl
        "--hidden-import=xlrd",         # Incluir xlrd
        "processador_simples.py"        # Script principal
    ]
    
    try:
        subprocess.check_call(comando)
        print("✅ Executável criado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")
        return False

def criar_estrutura_pastas():
    """Cria a estrutura de pastas necessária."""
    print("📁 Criando estrutura de pastas...")
    
    pastas = ["Entrada", "Saida", "Entrada/Processados", "Entrada/Erros"]
    
    for pasta in pastas:
        Path(pasta).mkdir(exist_ok=True)
        print(f"  ✅ {pasta}")
    
    # Criar arquivo README na pasta de entrada
    readme_entrada = """# Pasta de Entrada

Coloque aqui os arquivos Excel de empréstimos e pendências para processamento.

## Tipos de arquivo aceitos:
- Relatórios de empréstimos (.xlsx, .xls)
- Relatórios de pendências (.xlsx, .xls)

## Como funciona:
1. Coloque os arquivos nesta pasta
2. Execute o ProcessadorBiblioteca.exe
3. Os arquivos processados aparecerão na pasta "Saida"
4. Os arquivos originais serão movidos para "Entrada/Processados"

## Nomenclatura dos arquivos:
O sistema identifica automaticamente o tipo de arquivo baseado no nome:
- Arquivos com "emprestimo", "empréstimo", "loan" → Processados como empréstimos
- Arquivos com "pendencia", "pendência", "pending" → Processados como pendências
"""
    
    with open("Entrada/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_entrada)
    
    print("  ✅ README.txt criado na pasta Entrada")

def criar_arquivo_batch():
    """Cria um arquivo .bat para facilitar a execução."""
    print("📝 Criando arquivo .bat...")
    
    conteudo_batch = """@echo off
echo ========================================
echo  Processador de Relatorios de Biblioteca
echo ========================================
echo.
echo Iniciando processamento automatico...
echo.
echo Pasta de entrada: Entrada
echo Pasta de saida: Saida
echo.
echo Pressione qualquer tecla para parar...
echo.

ProcessadorBiblioteca.exe

echo.
echo Processamento concluido!
pause
"""
    
    with open("Executar_Processador.bat", "w", encoding="utf-8") as f:
        f.write(conteudo_batch)
    
    print("✅ Executar_Processador.bat criado")

def criar_instrucoes():
    """Cria arquivo com instruções de uso."""
    print("📋 Criando instruções de uso...")
    
    instrucoes = """# INSTRUÇÕES DE USO - PROCESSADOR DE BIBLIOTECA

## 🚀 Como usar:

### Método 1 - Arquivo .bat (Recomendado):
1. Clique duas vezes em "Executar_Processador.bat"
2. O processador iniciará automaticamente
3. Coloque os arquivos Excel na pasta "Entrada"
4. Os resultados aparecerão na pasta "Saida"

### Método 2 - Executável direto:
1. Clique duas vezes em "ProcessadorBiblioteca.exe"
2. Siga as instruções na tela

## 📁 Estrutura de pastas:

```
📂 Pasta do Projeto/
├── 📄 ProcessadorBiblioteca.exe     # Executável principal
├── 📄 Executar_Processador.bat      # Arquivo para execução fácil
├── 📂 Entrada/                      # Coloque arquivos aqui
│   ├── 📄 README.txt               # Instruções
│   ├── 📂 Processados/             # Arquivos já processados
│   └── 📂 Erros/                   # Arquivos com erro
└── 📂 Saida/                       # Resultados processados
```

## 📊 Tipos de arquivo aceitos:

### Empréstimos:
- Arquivos com "emprestimo", "empréstimo", "loan" no nome
- Formatos: .xlsx, .xls

### Pendências:
- Arquivos com "pendencia", "pendência", "pending" no nome
- Formatos: .xlsx, .xls

## ⚙️ Configuração:

O sistema funciona automaticamente, mas você pode:
- Modificar o intervalo de verificação
- Alterar nomes de pastas
- Personalizar configurações no arquivo config.py

## 🐛 Solução de problemas:

### Erro: "Arquivo não encontrado"
- Verifique se o arquivo Excel está na pasta "Entrada"
- Confirme se o arquivo não está corrompido

### Erro: "Tipo não identificado"
- Verifique se o nome do arquivo contém palavras-chave
- Consulte a seção "Tipos de arquivo aceitos"

### Arquivo movido para "Erros"
- Verifique o log para detalhes do erro
- Confirme se o arquivo tem o formato correto

## 📞 Suporte:

Para problemas ou dúvidas, consulte:
- Arquivo de log gerado automaticamente
- README.txt na pasta Entrada
- Documentação completa no README.md

---
Desenvolvido para automação de relatórios de biblioteca
"""
    
    with open("INSTRUCOES_USO.txt", "w", encoding="utf-8") as f:
        f.write(instrucoes)
    
    print("✅ INSTRUCOES_USO.txt criado")

def limpar_arquivos_temporarios():
    """Remove arquivos temporários do PyInstaller."""
    print("🧹 Limpando arquivos temporários...")
    
    pastas_para_remover = ["build", "__pycache__"]
    arquivos_para_remover = ["ProcessadorBiblioteca.spec"]
    
    for pasta in pastas_para_remover:
        if Path(pasta).exists():
            shutil.rmtree(pasta)
            print(f"  ✅ {pasta} removida")
    
    for arquivo in arquivos_para_remover:
        if Path(arquivo).exists():
            Path(arquivo).unlink()
            print(f"  ✅ {arquivo} removido")

def main():
    """Função principal."""
    print("🔨 CRIADOR DE EXECUTÁVEL - PROCESSADOR DE BIBLIOTECA")
    print("=" * 60)
    
    # Verificar se os arquivos necessários existem
    arquivos_necessarios = [
        "processador_simples.py"
    ]
    
    for arquivo in arquivos_necessarios:
        if not Path(arquivo).exists():
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return 1
    
    print("✅ Todos os arquivos necessários encontrados")
    
    # Instalar PyInstaller
    if not instalar_pyinstaller():
        return 1
    
    # Criar executável
    if not criar_executavel():
        return 1
    
    # Criar estrutura de pastas
    criar_estrutura_pastas()
    
    # Criar arquivo .bat
    criar_arquivo_batch()
    
    # Criar instruções
    criar_instrucoes()
    
    # Limpar arquivos temporários
    limpar_arquivos_temporarios()
    
    print("\n🎉 EXECUTÁVEL CRIADO COM SUCESSO!")
    print("=" * 60)
    print("📁 Arquivos criados:")
    print("  ✅ ProcessadorBiblioteca.exe")
    print("  ✅ Executar_Processador.bat")
    print("  ✅ INSTRUCOES_USO.txt")
    print("  ✅ Pasta Entrada/ com README.txt")
    print("  ✅ Pasta Saida/")
    print("\n🚀 Para usar:")
    print("  1. Clique em 'Executar_Processador.bat'")
    print("  2. Coloque arquivos Excel na pasta 'Entrada'")
    print("  3. Os resultados aparecerão na pasta 'Saida'")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 