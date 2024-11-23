import pandas as pd
import os
import holidays

data_path = "/home/hub/Documents/analise_acidentes_de_transito/data"
files_2021_2023 = ["2021.csv", "2023.csv"]
files_2022_2024 = ["2022.csv", "2024.csv"]


import os
import pandas as pd


def load_and_concat_files(file_list, sep, data_path):
    # Função para carregar e concatenar arquivos CSV com diferentes codificações
    dataframes = []

    # Define um dicionário de codificação para os arquivos específicos
    encoding_dict = {
        "2021": "latin1",
        "2023": "latin1",
        "2022": "utf-8",
        "2024": "utf-8",
    }

    for file in file_list:
        file_path = os.path.join(data_path, file)
        if os.path.exists(file_path):
            try:
                # Obtém o encoding com base no nome do arquivo
                year = file.split(".")[
                    0
                ]  # Assuming file name format is like '2021.csv'
                encoding = encoding_dict.get(
                    year, "utf-8"
                )  # Default to "utf-8" if year not found

                df = pd.read_csv(
                    file_path, encoding=encoding, sep=sep, on_bad_lines="skip"
                )
                dataframes.append(df)
            except Exception as e:
                print(f"Erro ao ler o arquivo {file}: {e}")
        else:
            print(f"Arquivo {file} não encontrado em {data_path}.")

    return (
        pd.concat(dataframes, axis=0, ignore_index=True)
        if dataframes
        else pd.DataFrame()
    )


def consolidate_data():
    # Função para consolidar os dados
    try:
        # Verifica se o diretório existe
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"O diretório {data_path} não foi encontrado.")

        # Verifica se os arquivos existem
        missing_files = [
            file
            for file in files_2021_2023 + files_2022_2024
            if not os.path.exists(os.path.join(data_path, file))
        ]
        if missing_files:
            raise FileNotFoundError(
                f"Os arquivos estão faltando: {', '.join(missing_files)}"
            )

        # Carregar e concatenar os dados
        df_2021_2023 = load_and_concat_files(
            files_2021_2023, sep=";", data_path=data_path
        )
        df_2022_2024 = load_and_concat_files(
            files_2022_2024, sep=",", data_path=data_path
        )

        if df_2021_2023.empty and df_2022_2024.empty:
            raise ValueError("Nenhum dado foi carregado. Verifique os arquivos.")

        # Juntar todos os dados
        df_completo = pd.concat([df_2021_2023, df_2022_2024], axis=0, ignore_index=True)

        # Verificar e converter a coluna de data
        if "data_inversa" in df_completo.columns:
            print("Tentando converter 'data_inversa' para datetime...")

            # Datas convertidas para o formato datetime YYYY-MM-DD
            df_completo["data_inversa"] = pd.to_datetime(
                df_completo["data_inversa"], errors="coerce"
            )

            # Verificar se há valores nat após conversao
            if df_completo["data_inversa"].isnull().sum() > 0:
                print(
                    f"Warning: {df_completo['data_inversa'].isnull().sum()} datas não foram convertidas corretamente."
                )

            # Criar a coluna 'ano'
            df_completo["ano"] = df_completo["data_inversa"].dt.year

        else:
            print("Coluna 'data_inversa' não encontrada para extrair o ano.")

        # Tratar valores nulos e obter informações sobre nulos
        null_info_before, null_info_after = tratar_valores_nulos(df_completo)

        # Remover duplicatas
        df_completo = df_completo.drop_duplicates()
        print(f"Removidas {df_completo.duplicated().sum()} duplicatas.")

        # Identificar/remover registros incoerentes
        df_completo = remover_registros_incoerentes(df_completo)

        # Adicionar informações adicionais - Engenharia de Atributos
        df_completo = adicionar_informacoes(df_completo)

        # Salvar o DataFrame consolidado
        output_path = os.path.join(data_path, "dados_consolidados.csv")
        df_completo.to_csv(output_path, index=False, encoding="utf-8")
        print("Dados consolidados salvos em:", output_path)

        return df_completo, null_info_before, null_info_after

    except Exception as e:
        print(f"Erro ao consolidar os dados: {e}")
        return None, None, None


def tratar_valores_nulos(df):
    # Função para tratar valores nulos no DataFrame: numéricos com a mediana e categóricos com a moda
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


def remover_registros_incoerentes(df):
    # Função para remover registros incoerentes
    # Remover registros onde a data é nula
    if "data_inversa" in df.columns:
        df = df[df["data_inversa"].notnull()]

    # Remover registros onde o id é nulo
    if "id" in df.columns:
        df = df[df["id"].notnull()]

    # Validar 'uf' (deve ser uma sigla de estado válida no Brasil)
    valid_ufs = [
        "AC",
        "AL",
        "AP",
        "AM",
        "BA",
        "CE",
        "DF",
        "ES",
        "GO",
        "MA",
        "MT",
        "MS",
        "MG",
        "PA",
        "PB",
        "PR",
        "PE",
        "PI",
        "RJ",
        "RN",
        "RS",
        "RO",
        "RR",
        "SC",
        "SP",
        "SE",
        "TO",
    ]
    if "uf" in df.columns:
        df = df[df["uf"].isin(valid_ufs)]

    # Validar 'km' (deve ser maior ou igual a 0)
    if "km" in df.columns:
        df["km"] = pd.to_numeric(df["km"], errors="coerce")
        df = df[df["km"].notna() & (df["km"] >= 0)]

    # Validar campos numéricos (não podem ser negativos)
    numeric_columns = [
        "pessoas",
        "mortos",
        "feridos_leves",
        "feridos_graves",
        "ilesos",
        "ignorados",
        "feridos",
        "veiculos",
    ]
    for col in numeric_columns:
        if col in df.columns:
            df = df[df[col] >= 0]

    # Verificar consistência entre os campos numéricos
    if "pessoas" in df.columns and "mortos" in df.columns:
        df = df[df["mortos"] <= df["pessoas"]]

    if "feridos" in df.columns and "pessoas" in df.columns:
        df = df[df["feridos"] <= df["pessoas"]]

    # Verificar se 'feridos' é igual à soma de 'feridos_leves' e 'feridos_graves'
    if (
        "feridos" in df.columns
        and "feridos_leves" in df.columns
        and "feridos_graves" in df.columns
    ):
        df = df[df["feridos"] == df["feridos_leves"] + df["feridos_graves"]]

    return df


# Engenharia de Atributos
def adicionar_informacoes(df):
    # Adiciona novas colunas relevantes para a análise

    # Garantir que a coluna 'data_inversa' está no formato datetime
    if "data_inversa" in df.columns:
        df["data_inversa"] = pd.to_datetime(df["data_inversa"], errors="coerce")

        # Criar coluna 'dia_semana' (Dia da semana)
        df["dia_semana"] = df["data_inversa"].dt.day_name()

        # Criar coluna 'mes' (Número do mês)
        df["mes"] = df["data_inversa"].dt.month

        # Criar coluna 'nome_mes' (Nome do mês)
        df["nome_mes"] = df["data_inversa"].dt.strftime("%B")

        # Criar coluna 'ano' (Ano)
        df["ano"] = df["data_inversa"].dt.year

        # Criar uma lista de feriados para cada ano presente no DataFrame
        df["feriado"] = df["ano"].apply(lambda x: holidays.Brazil(years=x))

        # Verificar se cada data está em um feriado
        df["feriado"] = df["data_inversa"].apply(
            lambda x: "Sim" if x in df.loc[x.year == df["ano"], "feriado"].iloc[0] else "Não"
        )

    # Verificar se a coluna 'horario' existe e está no formato correto
    if "horario" in df.columns:
        # Converter 'horario' para o formato datetime (extrair a parte da hora)
        df["hora"] = pd.to_datetime(
            df["horario"], format="%H:%M:%S", errors="coerce"
        ).dt.hour

        # Classificar o horário em categorias
        df["periodo_dia"] = pd.cut(
            df["hora"],
            bins=[-1, 5, 11, 17, 23],  # Definir os intervalos de horas
            labels=[
                "Madrugada",
                "Manhã",
                "Tarde",
                "Noite",
            ],  # Rótulos para as categorias
            right=True,
        )

        # Remover a coluna auxiliar
        df = df.drop(columns=["hora"])

    # Criar categoria para pessoas envolvidas nos acidentes
    df["faixa_pessoas"] = pd.cut(
        df["pessoas"],
        bins=[-1, 5, 20, float("inf")],
        labels=["Baixo envolvimento", "Médio envolvimento", "Alto envolvimento"],
        right=True,
    )

    return df
