#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador Simples de Relatórios de Biblioteca
==============================================

Versão simplificada para executável que processa arquivos
automaticamente na pasta de entrada.
"""

import os
import sys
import time
import shutil
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'processador_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProcessadorSimples:
    """Processador simples para executável."""
    
    def __init__(self):
        """Inicializa o processador."""
        self.pasta_entrada = Path("Entrada")
        self.pasta_saida = Path("Saida")
        self.pasta_processados = self.pasta_entrada / "Processados"
        self.pasta_erros = self.pasta_entrada / "Erros"
        
        # Criar pastas se não existirem
        self._criar_pastas()
        
        # Configurações
        self.bibliotecas = {
            "Unidade 1": "Biblioteca Campus I - Unid. 1",
            "Unidade 2": "Biblioteca Campus I - Unid. 2",
            "Campus II": "Biblioteca Campus II"
        }
    
    def _criar_pastas(self):
        """Cria as pastas necessárias."""
        pastas = [self.pasta_entrada, self.pasta_saida, self.pasta_processados, self.pasta_erros]
        for pasta in pastas:
            pasta.mkdir(exist_ok=True)
            logger.info(f"Pasta verificada: {pasta}")
    
    def _identificar_tipo(self, arquivo: Path) -> str:
        """Identifica o tipo do arquivo."""
        nome = arquivo.name.lower()
        
        if any(palavra in nome for palavra in ["emprestimo", "empréstimo", "loan"]):
            return "emprestimos"
        elif any(palavra in nome for palavra in ["pendencia", "pendência", "pending"]):
            return "pendencias"
        else:
            return "desconhecido"
    
    def _processar_emprestimos(self, arquivo: Path) -> bool:
        """Processa arquivo de empréstimos."""
        try:
            logger.info(f"Processando empréstimos: {arquivo.name}")
            
            # Carregar dados
            df = pd.read_excel(arquivo)
            
            # Colunas necessárias
            colunas = ['Nome da pessoa', 'Gênero', 'Nome da biblioteca', 'Email', 'Nome pessoa empréstimo']
            
            # Verificar colunas
            colunas_faltantes = [col for col in colunas if col not in df.columns]
            if colunas_faltantes:
                logger.error(f"Colunas faltantes: {colunas_faltantes}")
                return False
            
            # Selecionar colunas
            df = df[colunas]
            
            # Limpar dados
            df = df[
                (df["Email"].notna()) & 
                (df["Email"].astype(str).str.strip() != "") &
                (df["Email"].astype(str).str.strip() != "nan")
            ]
            df = df[df["Nome pessoa empréstimo"] != "Bibinternet"]
            df = df.drop(columns=["Nome pessoa empréstimo"])
            df = df.drop_duplicates()
            
            # Formatar dados
            df = df.sort_values(by="Nome da pessoa")
            # Converter para minúsculo primeiro, depois aplicar title() para pegar apenas primeira letra maiúscula
            df["Nome da pessoa"] = df["Nome da pessoa"].str.lower().str.title()
            df["Nome da pessoa"] = df["Nome da pessoa"].str.split().str[0]
            df["Gênero"] = df["Gênero"].replace({"M": "o", "F": "a"})
            df["Email"] = df["Email"].str.replace(",", "; ", regex=False)
            
            # Separar por biblioteca
            planilhas = {"Base": df}
            for nome_planilha, nome_biblioteca in self.bibliotecas.items():
                planilhas[nome_planilha] = df[df["Nome da biblioteca"] == nome_biblioteca]
            
            # Salvar resultados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = self.pasta_saida / f"emprestimos_{timestamp}.xlsx"
            
            with pd.ExcelWriter(arquivo_saida, engine="openpyxl") as writer:
                for nome_planilha, df_planilha in planilhas.items():
                    df_planilha.to_excel(writer, sheet_name=nome_planilha, index=False)
            
            logger.info(f"Empréstimos processados: {arquivo_saida}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar empréstimos: {e}")
            return False
    
    def _processar_pendencias(self, arquivo: Path) -> bool:
        """Processa arquivo de pendências."""
        try:
            logger.info(f"Processando pendências: {arquivo.name}")
            
            # Carregar dados
            df = pd.read_excel(arquivo)
            
            # Colunas necessárias
            colunas = ["Nome da pessoa", "Email", "Data de empréstimo", 
                      "Data devolução prevista", "Título", "Nome da biblioteca"]
            
            # Verificar colunas
            colunas_existentes = [col for col in colunas if col in df.columns]
            if len(colunas_existentes) < 4:  # Mínimo de colunas necessárias
                logger.error("Colunas insuficientes para processamento")
                return False
            
            # Selecionar colunas
            df = df[colunas_existentes]
            
            # Limpar dados (incluindo NaN, None, strings vazias)
            df = df[
                (df["Email"].notna()) & 
                (df["Email"].astype(str).str.strip() != "") &
                (df["Email"].astype(str).str.strip() != "nan")
            ]
            
            # Formatar dados
            df = df.sort_values(by="Nome da pessoa")
            # Converter para minúsculo primeiro, depois aplicar title() para pegar apenas primeira letra maiúscula
            df["Nome da pessoa"] = df["Nome da pessoa"].str.lower().str.title()
            df["Nome da pessoa"] = df["Nome da pessoa"].str.split().str[0]
            df["Email"] = df["Email"].str.replace(",", "; ", regex=False)
            
            # Reordenar colunas se possível
            nova_ordem = ["Nome da pessoa", "Email", "Título", "Data de empréstimo", 
                         "Data devolução prevista", "Nome da biblioteca"]
            colunas_disponiveis = [col for col in nova_ordem if col in df.columns]
            if colunas_disponiveis:
                df = df[colunas_disponiveis]
            
            # Separar por biblioteca
            planilhas = {"Base": df}  # Adicionar planilha base
            for nome_planilha, nome_biblioteca in self.bibliotecas.items():
                planilhas[nome_planilha] = df[df["Nome da biblioteca"] == nome_biblioteca]
            
            # Salvar resultados
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_saida = self.pasta_saida / f"pendencias_{timestamp}.xlsx"
            
            with pd.ExcelWriter(arquivo_saida, engine="openpyxl") as writer:
                for nome_planilha, df_planilha in planilhas.items():
                    df_planilha.to_excel(writer, sheet_name=nome_planilha, index=False)
            
            logger.info(f"Pendências processadas: {arquivo_saida}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar pendências: {e}")
            return False
    
    def _mover_arquivo(self, arquivo: Path, sucesso: bool):
        """Move arquivo para pasta apropriada."""
        try:
            if sucesso:
                destino = self.pasta_processados / arquivo.name
            else:
                destino = self.pasta_erros / arquivo.name
            
            shutil.move(str(arquivo), str(destino))
            logger.info(f"Arquivo movido: {arquivo.name} -> {destino}")
            
        except Exception as e:
            logger.error(f"Erro ao mover arquivo {arquivo}: {e}")
    
    def processar_arquivo(self, arquivo: Path) -> bool:
        """Processa um arquivo específico."""
        try:
            # Verificar se é arquivo Excel
            if arquivo.suffix.lower() not in ['.xlsx', '.xls']:
                logger.warning(f"Arquivo não é Excel: {arquivo.name}")
                return False
            
            # Identificar tipo
            tipo = self._identificar_tipo(arquivo)
            
            if tipo == "desconhecido":
                logger.warning(f"Tipo não identificado: {arquivo.name}")
                return False
            
            # Processar baseado no tipo
            if tipo == "emprestimos":
                sucesso = self._processar_emprestimos(arquivo)
            else:  # pendencias
                sucesso = self._processar_pendencias(arquivo)
            
            # Mover arquivo
            self._mover_arquivo(arquivo, sucesso)
            
            return sucesso
            
        except Exception as e:
            logger.error(f"Erro ao processar {arquivo}: {e}")
            self._mover_arquivo(arquivo, False)
            return False
    
    def processar_pasta(self):
        """Processa todos os arquivos na pasta de entrada."""
        logger.info("Verificando pasta de entrada...")
        
        # Encontrar arquivos Excel
        arquivos_excel = list(self.pasta_entrada.glob("*.xlsx")) + list(self.pasta_entrada.glob("*.xls"))
        
        # Filtrar arquivos que não estão nas subpastas
        arquivos_para_processar = [
            arquivo for arquivo in arquivos_excel 
            if arquivo.parent == self.pasta_entrada
        ]
        
        if not arquivos_para_processar:
            logger.info("Nenhum arquivo novo encontrado.")
            return
        
        logger.info(f"Encontrados {len(arquivos_para_processar)} arquivos para processar.")
        
        for arquivo in arquivos_para_processar:
            logger.info(f"Processando: {arquivo.name}")
            
            sucesso = self.processar_arquivo(arquivo)
            
            if sucesso:
                logger.info(f"✅ {arquivo.name} processado com sucesso!")
            else:
                logger.error(f"❌ Falha no processamento de {arquivo.name}")
    
    def executar(self):
        """Executa o processamento."""
        print("🚀 PROCESSADOR DE RELATÓRIOS DE BIBLIOTECA")
        print("=" * 50)
        print(f"📁 Pasta de entrada: {self.pasta_entrada}")
        print(f"📁 Pasta de saída: {self.pasta_saida}")
        print("=" * 50)
        
        try:
            self.processar_pasta()
            print("\n✅ Processamento concluído!")
            print("📊 Verifique a pasta 'Saida' para os resultados.")
            
        except Exception as e:
            logger.error(f"Erro durante execução: {e}")
            print(f"\n❌ Erro: {e}")
        
        input("\nPressione Enter para sair...")


def main():
    """Função principal."""
    try:
        processador = ProcessadorSimples()
        processador.executar()
        return 0
    except Exception as e:
        print(f"Erro fatal: {e}")
        input("Pressione Enter para sair...")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 