#!/usr/bin/env python3
import pandas as pd
import os
import glob

def verificar_arquivo(arquivo_path, nome_arquivo):
    print(f"\n=== VERIFICANDO {nome_arquivo} ===")
    
    if not os.path.exists(arquivo_path):
        print(f"Arquivo não encontrado: {arquivo_path}")
        return
    
    try:
        # Ler todas as planilhas do arquivo
        df_dict = pd.read_excel(arquivo_path, sheet_name=None)
        
        print(f"Planilhas encontradas: {list(df_dict.keys())}")
        
        for sheet_name, df in df_dict.items():
            print(f"\n--- Planilha: {sheet_name} ---")
            print(f"Colunas: {list(df.columns)}")
            print(f"Total de registros: {len(df)}")
            
            if "Nome da pessoa" in df.columns:
                print("Primeiros 5 nomes:")
                for i, nome in enumerate(df["Nome da pessoa"].head(5)):
                    print(f"  {i+1}. '{nome}' (tipo: {type(nome)})")
                
                # Verificar se há nomes com espaços (nomes completos)
                nomes_completos = df[df["Nome da pessoa"].str.contains(" ", na=False)]
                if len(nomes_completos) > 0:
                    print(f"\n⚠️  ENCONTRADOS {len(nomes_completos)} registros com nomes completos:")
                    for i, nome in enumerate(nomes_completos["Nome da pessoa"].head(3)):
                        print(f"  {i+1}. '{nome}'")
                else:
                    print("✅ Todos os nomes estão apenas com o primeiro nome")
            
            if "Email" in df.columns:
                emails_vazios = df[df["Email"].isna() | (df["Email"].astype(str).str.strip() == "")]
                print(f"Registros sem email: {len(emails_vazios)}")
    
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

# Verificar o arquivo mais recente gerado pelo executável
arquivos_emprestimos = glob.glob("Saida/emprestimos_*.xlsx")
if arquivos_emprestimos:
    arquivo_mais_recente = max(arquivos_emprestimos, key=os.path.getctime)
    verificar_arquivo(arquivo_mais_recente, "ARQUIVO GERADO PELO EXECUTÁVEL CORRIGIDO")
else:
    print("Nenhum arquivo de empréstimos encontrado na pasta Saida")
