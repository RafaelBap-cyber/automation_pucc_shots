#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe Base para Processamento de Relatórios
============================================

Esta classe fornece funcionalidades comuns para processamento
de relatórios de bibliotecas.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys
from abc import ABC, abstractmethod

class ProcessadorBase(ABC):
    """Classe base abstrata para processamento de relatórios."""
    
    def __init__(self, arquivo_entrada: str, arquivo_saida: str):
        """
        Inicializa o processador base.
        
        Args:
            arquivo_entrada: Nome do arquivo Excel de entrada
            arquivo_saida: Nome do arquivo Excel de saída
        """
        self.arquivo_entrada = arquivo_entrada
        self.arquivo_saida = arquivo_saida
        self.df = None
        
        # Configurar logging específico para cada tipo de processamento
        self._configurar_logging()
    
    def _configurar_logging(self):
        """Configura o sistema de logging."""
        nome_classe = self.__class__.__name__.lower()
        log_file = f'processamento_{nome_classe}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def carregar_dados(self) -> bool:
        """
        Carrega os dados do arquivo Excel.
        
        Returns:
            bool: True se carregado com sucesso, False caso contrário
        """
        try:
            if not Path(self.arquivo_entrada).exists():
                self.logger.error(f"Arquivo não encontrado: {self.arquivo_entrada}")
                return False
                
            self.logger.info(f"Carregando dados de: {self.arquivo_entrada}")
            self.df = pd.read_excel(self.arquivo_entrada)
            self.logger.info(f"Dados carregados: {len(self.df)} registros")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {e}")
            return False
    
    def validar_colunas(self, colunas_necessarias: List[str]) -> bool:
        """
        Valida se as colunas necessárias existem no DataFrame.
        
        Args:
            colunas_necessarias: Lista de colunas que devem existir
            
        Returns:
            bool: True se todas as colunas existem, False caso contrário
        """
        colunas_faltantes = [col for col in colunas_necessarias if col not in self.df.columns]
        
        if colunas_faltantes:
            self.logger.error(f"Colunas faltantes: {colunas_faltantes}")
            self.logger.info(f"Colunas disponíveis: {list(self.df.columns)}")
            return False
            
        self.logger.info("Todas as colunas necessárias estão presentes")
        return True
    
    def formatar_nomes(self) -> None:
        """Formata os nomes das pessoas (primeira letra maiúscula e apenas primeiro nome)."""
        if "Nome da pessoa" in self.df.columns:
            # Primeiro aplicar title() para capitalizar
            self.df["Nome da pessoa"] = self.df["Nome da pessoa"].str.title()
            # Depois extrair apenas o primeiro nome
            self.df["Nome da pessoa"] = self.df["Nome da pessoa"].str.split().str[0]
            self.logger.info("Nomes formatados com sucesso (apenas primeiro nome)")
    
    def ordenar_por_nome(self) -> None:
        """Ordena os dados por nome da pessoa."""
        if "Nome da pessoa" in self.df.columns:
            self.df = self.df.sort_values(by="Nome da pessoa")
            self.logger.info("Dados ordenados por nome")
    
    def remover_duplicatas(self) -> None:
        """Remove registros duplicados."""
        registros_antes = len(self.df)
        self.df = self.df.drop_duplicates()
        registros_removidos = registros_antes - len(self.df)
        
        if registros_removidos > 0:
            self.logger.info(f"Removidas {registros_removidos} duplicatas")
    
    def formatar_emails(self) -> None:
        """Formata os emails (substitui vírgulas por ponto e vírgula)."""
        if "Email" in self.df.columns:
            self.df["Email"] = self.df["Email"].str.replace(",", "; ", regex=False)
            self.logger.info("Emails formatados com sucesso")
    
    def separar_por_biblioteca(self, bibliotecas: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        """
        Separa os dados por biblioteca.
        
        Args:
            bibliotecas: Dicionário com mapeamento de nomes de planilha para nomes de biblioteca
            
        Returns:
            Dict com DataFrames separados por biblioteca
        """
        planilhas = {}
        
        for nome_planilha, nome_biblioteca in bibliotecas.items():
            planilhas[nome_planilha] = self.df[
                self.df["Nome da biblioteca"] == nome_biblioteca
            ]
            self.logger.info(f"{nome_planilha}: {len(planilhas[nome_planilha])} registros")
        
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
            self.logger.info(f"Salvando planilhas em: {self.arquivo_saida}")
            
            with pd.ExcelWriter(self.arquivo_saida, engine="openpyxl") as writer:
                for nome_planilha, df_planilha in planilhas.items():
                    df_planilha.to_excel(writer, sheet_name=nome_planilha, index=False)
                    self.logger.info(f"Planilha '{nome_planilha}' salva com {len(df_planilha)} registros")
            
            self.logger.info("Processamento concluído com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar planilhas: {e}")
            return False
    
    def gerar_relatorio(self, bibliotecas: Dict[str, str]) -> None:
        """
        Gera um relatório resumido do processamento.
        
        Args:
            bibliotecas: Dicionário com mapeamento de bibliotecas
        """
        self.logger.info("=== RELATÓRIO DE PROCESSAMENTO ===")
        self.logger.info(f"Total de registros processados: {len(self.df)}")
        self.logger.info(f"Colunas no dataset: {list(self.df.columns)}")
        
        # Estatísticas por biblioteca
        for nome_biblioteca in bibliotecas.values():
            count = len(self.df[self.df["Nome da biblioteca"] == nome_biblioteca])
            self.logger.info(f"{nome_biblioteca}: {count} registros")
    
    @abstractmethod
    def processar_dados_especificos(self) -> None:
        """
        Método abstrato que deve ser implementado pelas classes filhas
        para processar dados específicos de cada tipo de relatório.
        """
        pass
    
    def processar(self) -> bool:
        """
        Executa todo o processo de processamento.
        
        Returns:
            bool: True se processamento bem-sucedido, False caso contrário
        """
        self.logger.info("Iniciando processamento")
        
        # Carregar dados
        if not self.carregar_dados():
            return False
        
        # Processar dados específicos (implementado pelas classes filhas)
        self.processar_dados_especificos()
        
        # Salvar resultados
        return True 