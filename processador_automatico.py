#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador Automático de Relatórios de Biblioteca
==================================================

Este script monitora uma pasta de entrada, processa automaticamente
os relatórios de empréstimos e pendências, e salva os resultados
em uma pasta de saída organizada.

Autor: Sistema de Automação
Data: 2025
"""

import os
import sys
import time
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

# Importar módulos locais
from processador_unificado import ProcessadorUnificado
from config import ARQUIVOS_CONFIG

class ProcessadorAutomatico:
    """Processador automático que monitora pastas e processa arquivos."""
    
    def __init__(self, pasta_entrada: str = "Entrada", pasta_saida: str = "Saida"):
        """
        Inicializa o processador automático.
        
        Args:
            pasta_entrada: Pasta onde colocar arquivos para processamento
            pasta_saida: Pasta onde salvar arquivos processados
        """
        self.pasta_entrada = Path(pasta_entrada)
        self.pasta_saida = Path(pasta_saida)
        self.pasta_processados = self.pasta_entrada / "Processados"
        self.pasta_erros = self.pasta_entrada / "Erros"
        
        # Configurar logging
        self._configurar_logging()
        
        # Criar pastas necessárias
        self._criar_pastas()
        
        # Processador unificado
        self.processador = ProcessadorUnificado()
        
        # Arquivos já processados (para evitar reprocessamento)
        self.arquivos_processados = set()
    
    def _configurar_logging(self):
        """Configura o sistema de logging."""
        log_file = f'processador_automatico_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _criar_pastas(self):
        """Cria as pastas necessárias para o funcionamento."""
        pastas = [
            self.pasta_entrada,
            self.pasta_saida,
            self.pasta_processados,
            self.pasta_erros
        ]
        
        for pasta in pastas:
            pasta.mkdir(exist_ok=True)
            self.logger.info(f"Pasta criada/verificada: {pasta}")
    
    def _identificar_tipo_arquivo(self, arquivo: Path) -> Optional[str]:
        """
        Identifica o tipo de arquivo baseado no nome.
        
        Args:
            arquivo: Caminho do arquivo
            
        Returns:
            Tipo do arquivo ("emprestimos", "pendencias" ou None)
        """
        nome_arquivo = arquivo.name.lower()
        
        # Padrões para identificar tipos de arquivo
        padroes_emprestimos = [
            "emprestimo", "emprestimos", "empréstimo", "empréstimos",
            "loan", "loans", "emprestimo"
        ]
        
        padroes_pendencias = [
            "pendencia", "pendencias", "pendência", "pendências",
            "pending", "overdue", "pendencia"
        ]
        
        # Verificar padrões
        for padrao in padroes_emprestimos:
            if padrao in nome_arquivo:
                return "emprestimos"
        
        for padrao in padroes_pendencias:
            if padrao in nome_arquivo:
                return "pendencias"
        
        return None
    
    def _validar_arquivo_excel(self, arquivo: Path) -> bool:
        """
        Valida se o arquivo é um Excel válido.
        
        Args:
            arquivo: Caminho do arquivo
            
        Returns:
            True se válido, False caso contrário
        """
        try:
            # Verificar extensão
            if arquivo.suffix.lower() not in ['.xlsx', '.xls']:
                return False
            
            # Tentar abrir o arquivo
            df = pd.read_excel(arquivo, nrows=5)  # Ler apenas 5 linhas para teste
            return True
            
        except Exception as e:
            self.logger.warning(f"Arquivo inválido {arquivo}: {e}")
            return False
    
    def _mover_arquivo(self, origem: Path, destino: Path, sucesso: bool = True):
        """
        Move um arquivo para a pasta apropriada.
        
        Args:
            origem: Arquivo de origem
            destino: Destino do arquivo
            sucesso: Se o processamento foi bem-sucedido
        """
        try:
            if sucesso:
                # Mover para pasta de processados
                destino_final = self.pasta_processados / origem.name
            else:
                # Mover para pasta de erros
                destino_final = self.pasta_erros / origem.name
            
            shutil.move(str(origem), str(destino_final))
            self.logger.info(f"Arquivo movido: {origem.name} -> {destino_final}")
            
        except Exception as e:
            self.logger.error(f"Erro ao mover arquivo {origem}: {e}")
    
    def _processar_arquivo(self, arquivo: Path) -> bool:
        """
        Processa um arquivo específico.
        
        Args:
            arquivo: Caminho do arquivo
            
        Returns:
            True se processado com sucesso, False caso contrário
        """
        try:
            self.logger.info(f"Iniciando processamento: {arquivo.name}")
            
            # Identificar tipo do arquivo
            tipo = self._identificar_tipo_arquivo(arquivo)
            
            if not tipo:
                self.logger.warning(f"Não foi possível identificar o tipo do arquivo: {arquivo.name}")
                return False
            
            # Copiar arquivo para processamento temporário
            arquivo_temp = Path(f"temp_{arquivo.name}")
            shutil.copy2(arquivo, arquivo_temp)
            
            # Modificar configuração temporariamente
            config_original = ARQUIVOS_CONFIG[tipo]["entrada"]
            ARQUIVOS_CONFIG[tipo]["entrada"] = arquivo_temp.name
            
            # Processar arquivo
            sucesso = self.processador.processar_tipo(tipo)
            
            # Restaurar configuração
            ARQUIVOS_CONFIG[tipo]["entrada"] = config_original
            
            # Remover arquivo temporário
            if arquivo_temp.exists():
                arquivo_temp.unlink()
            
            if sucesso:
                # Mover arquivo processado para pasta de saída
                arquivo_saida = ARQUIVOS_CONFIG[tipo]["saida"]
                if Path(arquivo_saida).exists():
                    destino_final = self.pasta_saida / f"{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{arquivo_saida}"
                    shutil.move(arquivo_saida, destino_final)
                    self.logger.info(f"Arquivo processado salvo: {destino_final}")
                
                # Mover arquivo original para pasta de processados
                self._mover_arquivo(arquivo, self.pasta_processados, sucesso=True)
                return True
            else:
                # Mover arquivo para pasta de erros
                self._mover_arquivo(arquivo, self.pasta_erros, sucesso=False)
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao processar {arquivo}: {e}")
            self._mover_arquivo(arquivo, self.pasta_erros, sucesso=False)
            return False
    
    def _encontrar_arquivos_novos(self) -> List[Path]:
        """
        Encontra arquivos novos na pasta de entrada.
        
        Returns:
            Lista de arquivos novos para processar
        """
        arquivos_novos = []
        
        for arquivo in self.pasta_entrada.glob("*"):
            # Ignorar pastas e arquivos já processados
            if (arquivo.is_file() and 
                arquivo not in self.arquivos_processados and
                self._validar_arquivo_excel(arquivo)):
                
                arquivos_novos.append(arquivo)
        
        return arquivos_novos
    
    def processar_pasta(self):
        """Processa todos os arquivos novos na pasta de entrada."""
        self.logger.info("Verificando pasta de entrada...")
        
        arquivos_novos = self._encontrar_arquivos_novos()
        
        if not arquivos_novos:
            self.logger.info("Nenhum arquivo novo encontrado.")
            return
        
        self.logger.info(f"Encontrados {len(arquivos_novos)} arquivos novos para processar.")
        
        for arquivo in arquivos_novos:
            self.logger.info(f"Processando: {arquivo.name}")
            
            sucesso = self._processar_arquivo(arquivo)
            
            if sucesso:
                self.arquivos_processados.add(arquivo)
                self.logger.info(f"✅ {arquivo.name} processado com sucesso!")
            else:
                self.logger.error(f"❌ Falha no processamento de {arquivo.name}")
    
    def monitorar_pasta(self, intervalo: int = 30):
        """
        Monitora continuamente a pasta de entrada.
        
        Args:
            intervalo: Intervalo em segundos entre verificações
        """
        self.logger.info(f"Iniciando monitoramento da pasta: {self.pasta_entrada}")
        self.logger.info(f"Arquivos processados serão salvos em: {self.pasta_saida}")
        self.logger.info(f"Pressione Ctrl+C para parar o monitoramento")
        
        try:
            while True:
                self.processar_pasta()
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoramento interrompido pelo usuário.")
    
    def processar_uma_vez(self):
        """Processa a pasta uma única vez."""
        self.logger.info("Processamento único iniciado...")
        self.processar_pasta()
        self.logger.info("Processamento único concluído.")


def main():
    """Função principal do script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Processador Automático de Relatórios de Biblioteca",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python processador_automatico.py                    # Monitoramento contínuo
  python processador_automatico.py --uma-vez         # Processamento único
  python processador_automatico.py --entrada "Dados" --saida "Resultados"
        """
    )
    
    parser.add_argument(
        "--entrada", 
        default="Entrada",
        help="Pasta de entrada (padrão: Entrada)"
    )
    
    parser.add_argument(
        "--saida", 
        default="Saida",
        help="Pasta de saída (padrão: Saida)"
    )
    
    parser.add_argument(
        "--intervalo", 
        type=int, 
        default=30,
        help="Intervalo de verificação em segundos (padrão: 30)"
    )
    
    parser.add_argument(
        "--uma-vez", 
        action="store_true",
        help="Processar apenas uma vez e sair"
    )
    
    args = parser.parse_args()
    
    try:
        processador = ProcessadorAutomatico(args.entrada, args.saida)
        
        if args.uma_vez:
            processador.processar_uma_vez()
        else:
            processador.monitorar_pasta(args.intervalo)
            
    except Exception as e:
        print(f"Erro: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 