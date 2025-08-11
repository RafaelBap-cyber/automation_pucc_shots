# Sistema de Automação de Relatórios de Biblioteca

Este projeto contém scripts para processamento automatizado de relatórios de empréstimos e pendências de bibliotecas.

## 📋 Funcionalidades

- **Processamento de Empréstimos**: Limpeza e formatação de dados de empréstimos
- **Processamento de Pendências**: Limpeza e formatação de dados de pendências
- **Separação por Biblioteca**: Geração de planilhas separadas por unidade/biblioteca
- **Logging Detalhado**: Registro completo de todas as operações
- **Tratamento de Erros**: Validação e tratamento robusto de erros
- **Arquitetura Modular**: Código reutilizável e bem estruturado

## 🚀 Instalação

1. **Clone ou baixe o projeto**
2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Estrutura do Projeto

```
Automação Serviço/
├── código de empréstimo.py          # Script original de empréstimos
├── código de pendência.py           # Script original de pendências
├── processador_base.py              # Classe base para processamento
├── processador_unificado.py         # Script unificado melhorado
├── config.py                        # Configurações centralizadas
├── requirements.txt                 # Dependências do projeto
├── README.md                        # Esta documentação
├── Relatório de Empréstimos.xlsx    # Arquivo de saída de empréstimos
└── Relatório de Pendência.xlsx      # Arquivo de saída de pendências
```

## 🎯 Como Usar

### Script Unificado (Recomendado)

```bash
# Processar apenas empréstimos
python processador_unificado.py emprestimos

# Processar apenas pendências
python processador_unificado.py pendencias

# Processar ambos os relatórios
python processador_unificado.py todos
```

### Scripts Originais

```bash
# Processar empréstimos
python "código de empréstimo.py"

# Processar pendências
python "código de pendência.py"
```

## 📊 Arquivos de Entrada Esperados

### Para Empréstimos
- **Arquivo**: `Relatório de Empréstimos 30.06.2025.xlsx`
- **Colunas necessárias**:
  - Nome da pessoa
  - Gênero
  - Nome da biblioteca
  - Email
  - Nome pessoa empréstimo

### Para Pendências
- **Arquivo**: `Relatório de Pendência 30.06.2025.xlsx`
- **Colunas necessárias**:
  - Nome da pessoa
  - Email
  - Data de empréstimo
  - Data devolução prevista
  - Título
  - Nome da biblioteca

## 📤 Arquivos de Saída

### Empréstimos
- **Arquivo**: `Relatório de Empréstimos.xlsx`
- **Planilhas geradas**:
  - Base (todos os dados)
  - Unidade 1
  - Unidade 2
  - Campus II

### Pendências
- **Arquivo**: `Relatório de Pendência.xlsx`
- **Planilhas geradas**:
  - Unidade 1
  - Unidade 2
  - Campus II

## 🔧 Melhorias Implementadas

### 1. **Tratamento de Erros**
- Validação de arquivos de entrada
- Verificação de colunas necessárias
- Tratamento de exceções com logging detalhado

### 2. **Arquitetura Modular**
- Classe base reutilizável (`ProcessadorBase`)
- Classes específicas para cada tipo de relatório
- Configurações centralizadas (`config.py`)

### 3. **Logging Avançado**
- Logs salvos em arquivos separados
- Níveis de log configuráveis
- Informações detalhadas sobre o processamento

### 4. **Validação de Dados**
- Verificação de colunas existentes
- Validação de emails
- Tratamento de dados ausentes

### 5. **Código Limpo**
- Documentação completa (docstrings)
- Nomes de variáveis descritivos
- Estrutura de código organizada

### 6. **Flexibilidade**
- Configurações centralizadas
- Fácil modificação de parâmetros
- Script unificado para ambos os tipos

## 📝 Logs

Os logs são salvos em arquivos separados:
- `processamento_processadoremprestimos.log` - Logs de empréstimos
- `processamento_processadorpendencias.log` - Logs de pendências

## ⚙️ Configuração

As configurações podem ser modificadas no arquivo `config.py`:

- Nomes de arquivos de entrada/saída
- Lista de colunas necessárias
- Mapeamento de bibliotecas
- Configurações de logging

## 🐛 Solução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique se o arquivo de entrada existe no diretório
- Confirme o nome exato do arquivo

### Erro: "Colunas faltantes"
- Verifique se o arquivo Excel contém todas as colunas necessárias
- Consulte a seção "Arquivos de Entrada Esperados"

### Erro: "openpyxl não encontrado"
- Execute: `pip install openpyxl`

## 📈 Próximas Melhorias Sugeridas

1. **Interface Gráfica**: Criar uma GUI para facilitar o uso
2. **Processamento em Lote**: Processar múltiplos arquivos de uma vez
3. **Validação de Datas**: Verificar formatos de data
4. **Backup Automático**: Criar backup dos arquivos originais
5. **Relatórios Estatísticos**: Gerar relatórios de qualidade dos dados
6. **Configuração via Arquivo**: Permitir configuração via arquivo JSON/YAML

## 👥 Contribuição

Para contribuir com melhorias:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Implemente as melhorias
4. Teste adequadamente
5. Envie um pull request

## 📄 Licença

Este projeto é de uso interno para automação de relatórios de biblioteca. 