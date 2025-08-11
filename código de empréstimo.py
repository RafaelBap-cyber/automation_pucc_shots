#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Processamento de Relatório de Empréstimos
==================================================

Este script processa relatórios de empréstimos de bibliotecas, realizando:
- Limpeza e formatação de dados
- Filtragem de registros inválidos
- Separação por unidades/bibliotecas
- Geração de planilhas organizadas

Autor: Sistema de Automação
Data: 2025
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processamento_emprestimos.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProcessadorEmprestimos:
    """Classe para processamento de relatórios de empréstimos."""
    
    def __init__(self, arquivo_entrada: str = "Relatório de Empréstimos 30.06.2025.xlsx"):
        """
        Inicializa o processador.
        
        Args:
            arquivo_entrada: Nome do arquivo Excel de entrada
        """
        self.arquivo_entrada = arquivo_entrada
        self.arquivo_saida = "Relatório de Empréstimos.xlsx"
        self.df = None
        
        # Configurações de colunas
        self.colunas_selecionadas = [
            'Nome da pessoa',
            'Gênero', 
            'Nome da biblioteca',
            'Email',
            'Nome pessoa empréstimo'
        ]
        
        # Mapeamento de gêneros
        self.mapeamento_genero = {"M": "o", "F": "a"}
        
        # Configurações de bibliotecas
        self.bibliotecas = {
            "Unidade 1": "Biblioteca Campus I - Unid. 1",
            "Unidade 2": "Biblioteca Campus I - Unid. 2", 
            "Campus II": "Biblioteca Campus II"
        }
    
    def carregar_dados(self) -> bool:
        """
        Carrega os dados do arquivo Excel.
        
        Returns:
            bool: True se carregado com sucesso, False caso contrário
        """
        try:
            if not Path(self.arquivo_entrada).exists():
                logger.error(f"Arquivo não encontrado: {self.arquivo_entrada}")
                return False
                
            logger.info(f"Carregando dados de: {self.arquivo_entrada}")
            self.df = pd.read_excel(self.arquivo_entrada)
            logger.info(f"Dados carregados: {len(self.df)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            return False
    
    def validar_colunas(self) -> bool:
        """
        Valida se as colunas necessárias existem no DataFrame.
        
        Returns:
            bool: True se todas as colunas existem, False caso contrário
        """
        colunas_faltantes = [col for col in self.colunas_selecionadas if col not in self.df.columns]
        
        if colunas_faltantes:
            logger.error(f"Colunas faltantes: {colunas_faltantes}")
            logger.info(f"Colunas disponíveis: {list(self.df.columns)}")
            return False
            
        logger.info("Todas as colunas necessárias estão presentes")
        return True
    
    def selecionar_colunas(self) -> None:
        """Seleciona apenas as colunas necessárias."""
        logger.info("Selecionando colunas relevantes")
        self.df = self.df[self.colunas_selecionadas]
    
    def limpar_dados(self) -> None:
        """Realiza a limpeza dos dados."""
        registros_iniciais = len(self.df)
        
        # Remover emails em branco (incluindo NaN, None, strings vazias)
        self.df = self.df[
            (self.df["Email"].notna()) & 
            (self.df["Email"].astype(str).str.strip() != "") &
            (self.df["Email"].astype(str).str.strip() != "nan")
        ]
        logger.info(f"Removidos {registros_iniciais - len(self.df)} registros sem email")
        
        # Remover Bibinternet
        self.df = self.df[self.df["Nome pessoa empréstimo"] != "Bibinternet"]
        
        # Remover coluna desnecessária
        self.df = self.df.drop(columns=["Nome pessoa empréstimo"])
        
        # Remover duplicatas
        duplicatas_removidas = len(self.df) - len(self.df.drop_duplicates())
        self.df = self.df.drop_duplicates()
        logger.info(f"Removidas {duplicatas_removidas} duplicatas")
    
    def formatar_dados(self) -> None:
        """Formata os dados para o padrão desejado."""
        # Ordenar por nome
        self.df = self.df.sort_values(by="Nome da pessoa")
        
        # Formatar nomes (primeira letra maiúscula e apenas primeiro nome)
        self.df["Nome da pessoa"] = self.df["Nome da pessoa"].str.title()
        self.df["Nome da pessoa"] = self.df["Nome da pessoa"].str.split().str[0]
        
        # Substituir valores de gênero
        self.df["Gênero"] = self.df["Gênero"].replace(self.mapeamento_genero)
        
        # Formatar emails (substituir vírgulas por ponto e vírgula)
        self.df["Email"] = self.df["Email"].str.replace(",", "; ", regex=False)
        
        logger.info("Dados formatados com sucesso")
    
    def separar_por_biblioteca(self) -> Dict[str, pd.DataFrame]:
        """
        Separa os dados por biblioteca.
        
        Returns:
            Dict com DataFrames separados por biblioteca
        """
        planilhas = {"Base": self.df}
        
        for nome_planilha, nome_biblioteca in self.bibliotecas.items():
            planilhas[nome_planilha] = self.df[
                self.df["Nome da biblioteca"] == nome_biblioteca
            ]
            logger.info(f"{nome_planilha}: {len(planilhas[nome_planilha])} registros")
        
        return planilhas
    
    def salvar_planilhas(self, planilhas: Dict[str, pd.DataFrame]) -> bool:
        """
        Salva as planilhas processadas em arquivo Excel.
        
        Args:
            planilhas: Dicionário com DataFrames por biblioteca
            
        Returns:
            bool: True se salvo com sucesso, False caso contrário
        """
        try:
            logger.info(f"Salvando planilhas em: {self.arquivo_saida}")
            
            with pd.ExcelWriter(self.arquivo_saida, engine="openpyxl") as writer:
                for nome_planilha, df_planilha in planilhas.items():
                    df_planilha.to_excel(writer, sheet_name=nome_planilha, index=False)
                    logger.info(f"Planilha '{nome_planilha}' salva com {len(df_planilha)} registros")
            
            logger.info("Processamento concluído com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar planilhas: {e}")
            return False
    
    def processar(self) -> bool:
        """
        Executa todo o processo de processamento.
        
        Returns:
            bool: True se processamento bem-sucedido, False caso contrário
        """
        logger.info("Iniciando processamento de empréstimos")
        
        # Carregar dados
        if not self.carregar_dados():
            return False
        
        # Validar colunas
        if not self.validar_colunas():
            return False
        
        # Processar dados
        self.selecionar_colunas()
        self.limpar_dados()
        self.formatar_dados()
        
        # Separar por biblioteca
        planilhas = self.separar_por_biblioteca()
        
        # Salvar resultados
        return self.salvar_planilhas(planilhas)


def main():
    """Função principal do script."""
    try:
        processador = ProcessadorEmprestimos()
        sucesso = processador.processar()
        
        if sucesso:
            logger.info("Script executado com sucesso!")
            return 0
        else:
            logger.error("Falha na execução do script")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Processamento interrompido pelo usuário")
        return 1
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
        

        