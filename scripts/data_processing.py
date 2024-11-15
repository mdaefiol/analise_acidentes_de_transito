import pandas as pd
import os

data_path = "/home/hub/Documents/analise_acidentes_de_transito/data"
files_2021_2023 = ["2021.csv", "2023.csv"]
files_2022_2024 = ["2022.csv", "2024.csv"]

def consolidate_data():
    try:
        # Verifica se o diretório existe
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"O diretório {data_path} não foi encontrado.")

        # Verifica se os arquivos existem
        missing_files = [file for file in files_2021_2023 + files_2022_2024 if not os.path.exists(os.path.join(data_path, file))]
        if missing_files:
            raise FileNotFoundError(f"Os arquivos estão faltando: {', '.join(missing_files)}")

        # Carrega dados de 2021 e 2023 separados por ;
        dataframes_2021_2023 = [
            pd.read_csv(
                os.path.join(data_path, file), encoding="latin1", sep=";", on_bad_lines="skip"
            )
            for file in files_2021_2023
        ]
        df_2021_2023 = pd.concat(dataframes_2021_2023, axis=0, ignore_index=True)

        # Carrega dados de 2022 e 2024 separados por ,
        dataframes_2022_2024 = [
            pd.read_csv(
                os.path.join(data_path, file), encoding="latin1", sep=",", on_bad_lines="skip"
            )
            for file in files_2022_2024
        ]
        df_2022_2024 = pd.concat(dataframes_2022_2024, axis=0, ignore_index=True)

        # Juntar todos os dados
        df_completo = pd.concat([df_2021_2023, df_2022_2024], axis=0, ignore_index=True)

        # Verificar e converter a coluna de data
        if 'data_inversa' in df_completo.columns:
            print("Tentando converter 'data_inversa' para datetime...")

            # Datas convertidas para o formato datetime YYYY-MM-DD
            df_completo['data_inversa'] = pd.to_datetime(df_completo['data_inversa'], errors='coerce')

            # Verificar se há valores nat após conversao
            if df_completo['data_inversa'].isnull().sum() > 0:
                print(f"Warning: {df_completo['data_inversa'].isnull().sum()} datas não foram convertidas corretamente.")
            
            # Criar a coluna 'ano'
            df_completo['ano'] = df_completo['data_inversa'].dt.year

        else:
            print("Coluna 'data_inversa' não encontrada para extrair o ano.")

        # Tratar valores nulos e obter informações sobre nulos
        null_info_before, null_info_after = tratar_valores_nulos(df_completo)

        # Remover duplicatas
        df_completo = df_completo.drop_duplicates()
        print(f"Removidas {df_completo.duplicated().sum()} duplicatas.")

        # Identificar/remover registros incoerentes
        df_completo = remover_registros_incoerentes(df_completo)

        # Salvar o DataFrame consolidado
        output_path = os.path.join(data_path, "dados_consolidados.csv")
        df_completo.to_csv(output_path, index=False, encoding="utf-8")
        print("Dados consolidados salvos em:", output_path)
        
        return df_completo, null_info_before, null_info_after

    except Exception as e:
        print(f"Erro ao consolidar os dados: {e}")
        return None, None, None

def tratar_valores_nulos(df):
    # Armazenar número de valores nulos antes do tratamento
    null_info_before = df.isnull().sum()

    # Substitui valores nulos de numéricos pela mediana
    for coluna in df.select_dtypes(include=["float64", "int64"]).columns:
        if df[coluna].isnull().sum() > 0:
            df[coluna] = df[coluna].fillna(df[coluna].median())  # mediana
            print(f"Valores nulos na coluna {coluna} foram substituídos pela mediana.")

    # Substitui valores nulos categórias pela moda
    for coluna in df.select_dtypes(include=["object"]).columns:
        if df[coluna].isnull().sum() > 0:
            df[coluna] = df[coluna].fillna(df[coluna].mode()[0])  # moda
            print(f"Valores nulos na coluna {coluna} foram substituídos pela moda.")

    # Armazenar número de valores nulos após tratamento
    null_info_after = df.isnull().sum()

    return null_info_before, null_info_after

# TODO: adicionar mais casos de tratativas de casos incorentes
def remover_registros_incoerentes(df):
    # Remover registros onde a data é nula
    df = df[df['data_inversa'].notnull()]

    return df
