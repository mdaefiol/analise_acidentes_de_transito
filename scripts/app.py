import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
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
    ano_filtro = st.selectbox("Escolha o ano", data["ano"].unique())
    uf_filtro = st.selectbox("Escolha a UF", data["uf"].unique())
    tipo_acidente_filtro = st.selectbox(
        "Escolha o tipo de acidente", data["tipo_acidente"].unique()
    )

    # Filtra os dados com base nas escolhas
    data_filtrada = data[
        (data["ano"] == ano_filtro)
        & (data["uf"] == uf_filtro)
        & (data["tipo_acidente"] == tipo_acidente_filtro)
    ]

    # Graficos e visualizações
    st.subheader("Visualizações")
    visual_option = st.selectbox(
        "Escolha uma visualização",
        [
            "Nenhum",
            "Distribuição",
            "Gráfico de Dispersão",
            "Análise Temporal",
            "Boxplot",
            "Histograma",
        ],
    )

    if visual_option == "Distribuição":
        column = st.selectbox(
            "Escolha uma coluna numérica",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Distribuição de densidade da coluna {column}")
        fig, ax = plt.subplots()
        data_filtrada[column].dropna().plot(kind="density", ax=ax)
        ax.set_title(f"Densidade de {column}")
        st.pyplot(fig)

    elif visual_option == "Gráfico de Dispersão":
        col1 = st.selectbox(
            "Escolha a primeira coluna numérica",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        col2 = st.selectbox(
            "Escolha a segunda coluna numérica",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        # Verifica se as colunas selecionadas são diferentes
        if col1 == col2:
            st.error("As colunas selecionadas devem ser diferentes!")
        else:
            st.write(f"Gráfico de Dispersão entre {col1} e {col2}")
            fig, ax = plt.subplots()
            ax.scatter(
                data_filtrada[col1], data_filtrada[col2], color="blue", alpha=0.5
            )
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            ax.set_title(f"Gráfico de Dispersão entre {col1} e {col2}")
            st.pyplot(fig)

    elif visual_option == "Boxplot":
        column = st.selectbox(
            "Escolha uma coluna numérica para o Boxplot",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Boxplot da coluna {column}")
        fig, ax = plt.subplots()
        sns.boxplot(x=data_filtrada[column], ax=ax)
        ax.set_title(f"Boxplot de {column}")
        st.pyplot(fig)

    elif visual_option == "Histograma":
        column = st.selectbox(
            "Escolha uma coluna numérica para o Histograma",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Histograma da coluna {column}")
        fig, ax = plt.subplots()
        data_filtrada[column].dropna().plot(
            kind="hist", bins=30, ax=ax, color="skyblue", edgecolor="black"
        )
        ax.set_title(f"Histograma de {column}")
        st.pyplot(fig)

    elif visual_option == "Análise Temporal":
        column = st.selectbox(
            "Escolha uma coluna para análise temporal",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Análise Temporal da coluna {column}")
        data_filtrada["data_inversa"] = pd.to_datetime(
            data_filtrada["data_inversa"], errors="coerce"
        )
        temporal_data = data_filtrada.groupby(
            data_filtrada["data_inversa"].dt.to_period("M")
        )[column].mean()
        st.line_chart(temporal_data)
    
    # 1. Top 5 causas mais comuns
    top_5_causas = data['causa_acidente'].value_counts().nlargest(5)

    # 2. Top 5 tipos mais comuns
    top_5_tipos = data['tipo_acidente'].value_counts().nlargest(5)

    # Configuração do Streamlit
    st.title("Análise de Acidentes")

    # Gráfico de barras para as top 5 causas mais comuns
    st.header('Top 5 Causas Mais Comuns dos Acidentes')
    fig_causas, ax_causas = plt.subplots()
    sns.barplot(x=top_5_causas.values, y=top_5_causas.index, ax=ax_causas, palette='Blues_d')
    ax_causas.set_xlabel('Número de Acidentes')
    ax_causas.set_ylabel('Causas')
    ax_causas.set_title('Top 5 Causas Mais Comuns')

    # Exibir o gráfico de causas
    st.pyplot(fig_causas)

    # Gráfico de barras para os top 5 tipos mais comuns de acidentes
    st.header('Top 5 Tipos Mais Comuns de Acidentes')
    fig_tipos, ax_tipos = plt.subplots()
    sns.barplot(x=top_5_tipos.values, y=top_5_tipos.index, ax=ax_tipos, palette='Greens_d')
    ax_tipos.set_xlabel('Número de Acidentes')
    ax_tipos.set_ylabel('Tipos de Acidentes')
    ax_tipos.set_title('Top 5 Tipos Mais Comuns de Acidentes')

    # Exibir o gráfico de tipos
    st.pyplot(fig_tipos)

    # Configurar o Streamlit
    st.title("Relação entre Número de Vítimas e Condições Meteorológicas")
    st.write("Este gráfico mostra a relação entre o número de vítimas e as condições meteorológicas nos acidentes.")

    # Contar o número de acidentes com mortos para cada condição meteorológica
    acidentes_com_mortos = data.groupby('condicao_metereologica')['mortos'].sum().reset_index()

    # Criar gráfico de dispersão (número de acidentes com mortos vs condições meteorológicas)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=acidentes_com_mortos, x='condicao_metereologica', y='mortos', hue='condicao_metereologica', palette='Set2', s=100, ax=ax, legend=False)

    # Adicionar título e rótulos aos eixos
    ax.set_title('Número de Acidentes com Mortos por Condição Meteorológica', fontsize=16)
    ax.set_xlabel('Condição Meteorológica', fontsize=12)
    ax.set_ylabel('Número de Acidentes com Mortos', fontsize=12)

    # Exibir o gráfico
    st.pyplot(fig)

    # Garantir que as colunas de latitude e longitude sejam convertidas para float
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    # Passo 2: Filtrar as linhas com NaN nas colunas de latitude ou longitude
    data = data.dropna(subset=['latitude', 'longitude'])

    # Função para criar o mapa
    def create_map(df):
        # Inicializando o mapa com uma coordenada média
        mapa = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=5)
        
        # Adicionando marcadores ao mapa
        for index, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"<b>{row['municipio']}</b><br>{row['tipo_acidente']}<br><i>{row['causa_acidente']}</i>",
                icon=folium.Icon(color='blue')
            ).add_to(mapa)
        
        # Retornando o mapa gerado
        return mapa

    # Streamlit interface
    st.title('Distribuição Geográfica dos Acidentes')

    # Exibindo o mapa interativo
    mapa = create_map(data)

    # Para exibir o mapa interativo no Streamlit, precisamos usar o folium integrada ao streamlit
    # Streamlit renderiza o mapa com folium através do st.components.v1
    from streamlit.components.v1 import iframe

    # Salvar o mapa como um HTML temporário
    mapa.save("mapa_acidentes.html")

    # Exibir o mapa no Streamlit
    with open("mapa_acidentes.html", "r") as f:
        mapa_html = f.read()

    # Renderizando o mapa dentro do Streamlit
    st.components.v1.html(mapa_html, width=700, height=500)

    # Verificação/remoção de duplicatas
    st.subheader("Verificação e Remoção de Duplicatas")

    # Mostra quantas duplicatas existem
    num_duplicatas = data.duplicated(subset=None, keep=False).sum()

    st.write(f"Total de registros duplicados: {num_duplicatas}")

    if num_duplicatas > 0:
        # Remove as duplicatas
        data_limpa = data.drop_duplicates(keep="first")
        st.write("Duplicatas removidas com sucesso.")
    else:
        data_limpa = data
        st.write("Nenhuma duplicata encontrada para remoção.")

    # Exibe o dataframe sem duplicatas
    st.dataframe(data_limpa.head())
