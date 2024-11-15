import os
import pandas as pd

# Init dos arquivos
data_path = "/home/hub/Documents/analise_acidentes_de_transito/data"
files = ["2021.csv", "2022.csv", "2023.csv", "2024.csv"]

# Carregar dados
def load_data(file_path):
    try:
        # Carregar os dados com 'latin1' e ';'
        df = pd.read_csv(file_path, encoding='latin1', sep=';', on_bad_lines='skip', errors='ignore')

        # Verifica se existe dados faltando 
        if df.isnull().values.any():
            df = df.dropna()  # remoção de linhas com dados faltando, como tratar de outra forma? 
# TODO: remover isso
        return df.head(20)  # Retorna as linhas
    

    except Exception as e:
        return f"Erro ao carregar os dados de {file_path}: {e}"

# Verifica se os arquivos existem
def check_files():
    missing_files = [file for file in files if not os.path.exists(os.path.join(data_path, file))]
    return missing_files

