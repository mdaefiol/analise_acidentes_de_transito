import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_processing import consolidate_data

# Carrega os dados
st.title("Análise de Acidentes de Trânsito")
st.subheader("Carregando os dados...")

data, null_info_before, null_info_after = consolidate_data()

if data is None:
    st.error("Erro ao carregar os dados consolidados.")
else:
    st.success("Dados carregados com sucesso.")
    st.dataframe(data.head())  # Exibe os dados

    # Exibir as informações sobre valores nulos antes e depois do tratamento
    st.subheader("Informações sobre Valores Nulos")
    st.write("### Valores nulos antes do tratamento")
    st.dataframe(null_info_before)

    st.write("### Valores nulos depois do tratamento")
    st.dataframe(null_info_after)

    # Filtros para as categorias
    st.subheader("Filtros")
    ano_filtro = st.selectbox("Escolha o ano", data['ano'].unique())
    uf_filtro = st.selectbox("Escolha a UF", data['uf'].unique())
    tipo_acidente_filtro = st.selectbox("Escolha o tipo de acidente", data['tipo_acidente'].unique())

    # Filtra os dados com base nas escolhas
    data_filtrada = data[
        (data['ano'] == ano_filtro) & 
        (data['uf'] == uf_filtro) & 
        (data['tipo_acidente'] == tipo_acidente_filtro)
    ]

    # Graficos e visualizações
    st.subheader("Visualizações")
    visual_option = st.selectbox("Escolha uma visualização", ["Nenhum", "Distribuição", "Gráfico de Dispersão", "Análise Temporal", "Boxplot", "Histograma"])

    if visual_option == "Distribuição":
        column = st.selectbox("Escolha uma coluna numérica", data.select_dtypes(include=["int", "float"]).columns)
        st.write(f"Distribuição de densidade da coluna {column}")
        fig, ax = plt.subplots()
        data_filtrada[column].dropna().plot(kind='density', ax=ax)
        ax.set_title(f"Densidade de {column}")
        st.pyplot(fig)

    elif visual_option == "Gráfico de Dispersão":
        col1 = st.selectbox("Escolha a primeira coluna numérica", data.select_dtypes(include=["int", "float"]).columns)
        col2 = st.selectbox("Escolha a segunda coluna numérica", data.select_dtypes(include=["int", "float"]).columns)
        st.write(f"Gráfico de Dispersão entre {col1} e {col2}")
        fig, ax = plt.subplots()
        ax.scatter(data_filtrada[col1], data_filtrada[col2], color='blue', alpha=0.5)
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.set_title(f"Gráfico de Dispersão entre {col1} e {col2}")
        st.pyplot(fig)

    elif visual_option == "Boxplot":
        column = st.selectbox("Escolha uma coluna numérica para o Boxplot", data.select_dtypes(include=["int", "float"]).columns)
        st.write(f"Boxplot da coluna {column}")
        fig, ax = plt.subplots()
        sns.boxplot(x=data_filtrada[column], ax=ax)
        ax.set_title(f"Boxplot de {column}")
        st.pyplot(fig)

    elif visual_option == "Histograma":
        column = st.selectbox("Escolha uma coluna numérica para o Histograma", data.select_dtypes(include=["int", "float"]).columns)
        st.write(f"Histograma da coluna {column}")
        fig, ax = plt.subplots()
        data_filtrada[column].dropna().plot(kind='hist', bins=30, ax=ax, color='skyblue', edgecolor='black')
        ax.set_title(f"Histograma de {column}")
        st.pyplot(fig)

    elif visual_option == "Análise Temporal":
        column = st.selectbox("Escolha uma coluna para análise temporal", data.select_dtypes(include=["int", "float"]).columns)
        st.write(f"Análise Temporal da coluna {column}")
        data_filtrada['data_inversa'] = pd.to_datetime(data_filtrada['data_inversa'], errors='coerce')
        temporal_data = data_filtrada.groupby(data_filtrada['data_inversa'].dt.to_period("M"))[column].mean()
        st.line_chart(temporal_data)

    # Verificação/remoção de duplicatas
    st.subheader("Verificação e Remoção de Duplicatas")
    
    # Mostra quantas duplicatas existem
    duplicatas = data.duplicated(subset=None, keep=False)
    num_duplicatas = duplicatas.sum()
    
    st.write(f"Total de registros duplicados: {num_duplicatas}")

    if num_duplicatas > 0:
        # Remove as duplicatas
        data_limpa = data.drop_duplicates(keep='first')
        st.write("Duplicatas removidas com sucesso.")
    else:
        data_limpa = data
        st.write("Nenhuma duplicata encontrada para remoção.")
    
    # Exibe o dataframe sem duplicatas
    st.dataframe(data_limpa.head())
