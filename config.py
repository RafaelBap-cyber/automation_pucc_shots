#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações Centralizadas para Processamento de Relatórios
===========================================================

Este módulo contém todas as configurações utilizadas pelos scripts
de processamento de empréstimos e pendências.
"""

from typing import Dict, List

# Configurações de arquivos
ARQUIVOS_CONFIG = {
    "emprestimos": {
        "entrada": "Entrada/Processados/Empréstimos_Teste.xlsx",
        "saida": "Relatório de Empréstimos.xlsx"
    },
    "pendencias": {
        "entrada": "Entrada/Processados/Pendência_Teste.xlsx", 
        "saida": "Relatório de Pendência.xlsx"
    }
}

# Configurações de colunas para empréstimos
COLUNAS_EMPRESTIMOS = [
    'Nome da pessoa',
    'Gênero', 
    'Nome da biblioteca',
    'Email',
    'Nome pessoa empréstimo'
]

# Configurações de colunas para pendências
COLUNAS_PENDENCIAS = [
    "Nome da pessoa",
    "Email",
    "Data de empréstimo",
    "Data devolução prevista",
    "Título",
    "Nome da biblioteca"
]

# Nova ordem das colunas para pendências
ORDEM_COLUNAS_PENDENCIAS = [
    "Nome da pessoa",
    "Email", 
    "Título",
    "Data de empréstimo",
    "Data devolução prevista",
    "Nome da biblioteca"
]

# Mapeamento de gêneros
MAPEAMENTO_GENERO = {"M": "o", "F": "a"}

# Configurações de bibliotecas
BIBLIOTECAS = {
    "Unidade 1": "Biblioteca Campus I - Unid. 1",
    "Unidade 2": "Biblioteca Campus I - Unid. 2",
    "Campus II": "Biblioteca Campus II"
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "encoding": "utf-8"
}

# Configurações de processamento
PROCESSAMENTO_CONFIG = {
    "remover_duplicatas": True,
    "ordenar_por_nome": True,
    "formatar_nomes": True,
    "validar_emails": True
} 