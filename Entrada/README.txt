# Pasta de Entrada

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
