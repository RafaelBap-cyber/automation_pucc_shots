# Sistema de Processamento de Relatórios de Biblioteca

## Arquivos Essenciais

### Processadores Principais
- **`processador_unificado.py`** - Processador principal (recomendado)
- **`processador_automatico.py`** - Processamento automático
- **`processador_simples.py`** - Processador simples
- **`código de empréstimo.py`** - Processador original de empréstimos
- **`código de pendência.py`** - Processador original de pendências

### Arquivos de Suporte
- **`processador_base.py`** - Classe base para processadores
- **`config.py`** - Configurações centralizadas
- **`requirements.txt`** - Dependências Python

### Executáveis e Scripts
- **`ProcessadorBiblioteca.exe`** - Executável Windows
- **`Executar_Processador.bat`** - Script de execução
- **`criar_executavel.py`** - Script para criar executável

## Como Usar

### 1. Processamento Manual (Recomendado)
```bash
# Processar empréstimos
python processador_unificado.py emprestimos

# Processar pendências
python processador_unificado.py pendencias

# Processar ambos
python processador_unificado.py todos
```

### 2. Processamento Automático
```bash
# Executar uma vez
python processador_automatico.py

# Ou usar o executável
ProcessadorBiblioteca.exe
```

### 3. Scripts Originais
```bash
# Empréstimos
python "código de empréstimo.py"

# Pendências
python "código de pendência.py"
```

## Estrutura de Pastas

```
Automation/
├── Entrada/           # Arquivos para processar
│   ├── Processados/   # Arquivos já processados
│   └── Erros/         # Arquivos com erro
├── Saida/             # Arquivos processados
└── [arquivos Python]  # Scripts de processamento
```

## Melhorias Implementadas

✅ **Limpeza robusta de emails**: Remove linhas sem email (vazio, NaN, None)
✅ **Aba "Base" em pendências**: Planilha de pendências agora tem aba "Base"
✅ **Processamento unificado**: Um script para ambos os tipos
✅ **Logs detalhados**: Rastreamento completo das operações
✅ **Primeiro nome apenas**: Coluna "Nome da pessoa" fica apenas com o primeiro nome

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Edite `config.py` para modificar:
- Nomes de arquivos
- Colunas
- Bibliotecas
- Configurações de processamento 