#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador Unificado de Relatórios de Biblioteca
================================================

Este script unifica o processamento de relatórios de empréstimos e pendências,
utilizando uma arquitetura modular e reutilizável.

Autor: Sistema de Automação
Data: 2025
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Importar módulos locais
from processador_base import ProcessadorBase
from config import (
    ARQUIVOS_CONFIG, 
    COLUNAS_EMPRESTIMOS, 
    COLUNAS_PENDENCIAS,
    ORDEM_COLUNAS_PENDENCIAS,
    MAPEAMENTO_GENERO,
    BIBLIOTECAS
)

class ProcessadorEmprestimos(ProcessadorBase):
    """Processador específico para relatórios de empréstimos."""
    
    def __init__(self):
        """Inicializa o processador de empréstimos."""
        config = ARQUIVOS_CONFIG["emprestimos"]
        super().__init__(config["entrada"], config["saida"])
    
    def processar_dados_especificos(self) -> None:
        """Processa dados específicos de empréstimos."""
        # Validar colunas
        if not self.validar_colunas(COLUNAS_EMPRESTIMOS):
            raise ValueError("Colunas necessárias não encontradas")
        
        # Selecionar colunas
        self.logger.info("Selecionando colunas relevantes")
        self.df = self.df[COLUNAS_EMPRESTIMOS]
        
        # Limpar dados
        self._limpar_dados_emprestimos()
        
        # Formatar dados
        self._formatar_dados_emprestimos()
        
        # Separar por biblioteca
        planilhas = self.separar_por_biblioteca(BIBLIOTECAS)
        planilhas["Base"] = self.df  # Adicionar planilha base
        
        # Gerar relatório
        self.gerar_relatorio(BIBLIOTECAS)
        
        # Salvar resultados
        if not self.salvar_planilhas(planilhas):
            raise RuntimeError("Falha ao salvar planilhas")
    
    def _limpar_dados_emprestimos(self) -> None:
        """Limpa dados específicos de empréstimos."""
        registros_iniciais = len(self.df)
        
        # Remover emails em branco (incluindo NaN, None, strings vazias)
        self.df = self.df[
            (self.df["Email"].notna()) & 
            (self.df["Email"].astype(str).str.strip() != "") &
            (self.df["Email"].astype(str).str.strip() != "nan")
        ]
        self.logger.info(f"Removidos {registros_iniciais - len(self.df)} registros sem email")
        
        # Remover Bibinternet
        self.df = self.df[self.df["Nome pessoa empréstimo"] != "Bibinternet"]
        
        # Remover coluna desnecessária
        self.df = self.df.drop(columns=["Nome pessoa empréstimo"])
        
        # Remover duplicatas
        self.remover_duplicatas()
    
    def _formatar_dados_emprestimos(self) -> None:
        """Formata dados específicos de empréstimos."""
        # Ordenar por nome
        self.ordenar_por_nome()
        
        # Formatar nomes
        self.formatar_nomes()
        
        # Substituir valores de gênero
        self.df["Gênero"] = self.df["Gênero"].replace(MAPEAMENTO_GENERO)
        
        # Formatar emails
        self.formatar_emails()
        
        self.logger.info("Dados de empréstimos formatados com sucesso")


class ProcessadorPendencias(ProcessadorBase):
    """Processador específico para relatórios de pendências."""
    
    def __init__(self):
        """Inicializa o processador de pendências."""
        config = ARQUIVOS_CONFIG["pendencias"]
        super().__init__(config["entrada"], config["saida"])
    
    def processar_dados_especificos(self) -> None:
        """Processa dados específicos de pendências."""
        # Selecionar colunas
        self._selecionar_colunas_pendencias()
        
        # Limpar dados
        self._limpar_dados_pendencias()
        
        # Formatar dados
        self._formatar_dados_pendencias()
        
        # Reordenar colunas
        self._reordenar_colunas()
        
        # Separar por biblioteca
        planilhas = self.separar_por_biblioteca(BIBLIOTECAS)
        planilhas["Base"] = self.df  # Adicionar planilha base
        
        # Gerar relatório
        self.gerar_relatorio(BIBLIOTECAS)
        
        # Salvar resultados
        if not self.salvar_planilhas(planilhas):
            raise RuntimeError("Falha ao salvar planilhas")
    
    def _selecionar_colunas_pendencias(self) -> None:
        """Seleciona colunas específicas para pendências."""
        self.logger.info("Selecionando colunas relevantes")
        
        # Verificar quais colunas existem no DataFrame
        colunas_existentes = [col for col in COLUNAS_PENDENCIAS if col in self.df.columns]
        colunas_faltantes = [col for col in COLUNAS_PENDENCIAS if col not in self.df.columns]
        
        if colunas_faltantes:
            self.logger.warning(f"Colunas não encontradas: {colunas_faltantes}")
        
        # Manter apenas as colunas desejadas que existem
        self.df = self.df[colunas_existentes]
        self.logger.info(f"Selecionadas {len(colunas_existentes)} colunas")
    
    def _limpar_dados_pendencias(self) -> None:
        """Limpa dados específicos de pendências."""
        registros_iniciais = len(self.df)
        
        # Filtrar registros sem email (incluindo NaN, None, strings vazias)
        registros_sem_email = self.df[
            (self.df["Email"].isna()) | 
            (self.df["Email"].astype(str).str.strip() == "") |
            (self.df["Email"].astype(str).str.strip() == "nan")
        ]
        self.logger.info(f"Encontrados {len(registros_sem_email)} registros sem email")
        
        # Remover registros sem email
        self.df = self.df[
            (self.df["Email"].notna()) & 
            (self.df["Email"].astype(str).str.strip() != "") &
            (self.df["Email"].astype(str).str.strip() != "nan")
        ]
        self.logger.info(f"Removidos {registros_iniciais - len(self.df)} registros sem email")
    
    def _formatar_dados_pendencias(self) -> None:
        """Formata dados específicos de pendências."""
        # Ordenar por nome
        self.ordenar_por_nome()
        
        # Formatar nomes
        self.formatar_nomes()
        
        # Formatar emails
        self.formatar_emails()
        
        self.logger.info("Dados de pendências formatados com sucesso")
    
    def _reordenar_colunas(self) -> None:
        """Reordena as colunas na ordem especificada."""
        # Verificar quais colunas da nova ordem existem
        colunas_disponiveis = [col for col in ORDEM_COLUNAS_PENDENCIAS if col in self.df.columns]
        
        if colunas_disponiveis:
            self.df = self.df[colunas_disponiveis]
            self.logger.info("Colunas reordenadas com sucesso")
        else:
            self.logger.warning("Nenhuma coluna da nova ordem encontrada")


class ProcessadorUnificado:
    """Classe unificada para processar ambos os tipos de relatório."""
    
    def __init__(self):
        """Inicializa o processador unificado."""
        self.processadores = {
            "emprestimos": ProcessadorEmprestimos(),
            "pendencias": ProcessadorPendencias()
        }
    
    def processar_tipo(self, tipo: str) -> bool:
        """
        Processa um tipo específico de relatório.
        
        Args:
            tipo: Tipo de relatório ("emprestimos" ou "pendencias")
            
        Returns:
            bool: True se processamento bem-sucedido, False caso contrário
        """
        if tipo not in self.processadores:
            print(f"Tipo de relatório inválido: {tipo}")
            print("Tipos válidos: emprestimos, pendencias")
            return False
        
        try:
            print(f"Processando relatório de {tipo}...")
            return self.processadores[tipo].processar()
            
        except Exception as e:
            print(f"Erro ao processar {tipo}: {e}")
            return False
    
    def processar_todos(self) -> Dict[str, bool]:
        """
        Processa todos os tipos de relatório.
        
        Returns:
            Dict com resultados de cada processamento
        """
        resultados = {}
        
        for tipo in self.processadores.keys():
            print(f"\n{'='*50}")
            print(f"PROCESSANDO: {tipo.upper()}")
            print(f"{'='*50}")
            
            resultados[tipo] = self.processar_tipo(tipo)
            
            if resultados[tipo]:
                print(f"✅ {tipo} processado com sucesso!")
            else:
                print(f"❌ Falha no processamento de {tipo}")
        
        return resultados


def main():
    """Função principal do script."""
    if len(sys.argv) < 2:
        print("Uso: python processador_unificado.py <tipo>")
        print("Tipos disponíveis:")
        print("  emprestimos - Processa relatório de empréstimos")
        print("  pendencias  - Processa relatório de pendências")
        print("  todos       - Processa ambos os relatórios")
        return 1
    
    tipo = sys.argv[1].lower()
    
    try:
        processador = ProcessadorUnificado()
        
        if tipo == "todos":
            resultados = processador.processar_todos()
            
            print(f"\n{'='*50}")
            print("RESUMO DOS RESULTADOS")
            print(f"{'='*50}")
            
            for tipo_relatorio, sucesso in resultados.items():
                status = "✅ SUCESSO" if sucesso else "❌ FALHA"
                print(f"{tipo_relatorio}: {status}")
            
            return 0 if all(resultados.values()) else 1
            
        else:
            sucesso = processador.processar_tipo(tipo)
            return 0 if sucesso else 1
            
    except KeyboardInterrupt:
        print("\nProcessamento interrompido pelo usuário")
        return 1
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 