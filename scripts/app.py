import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
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
    #st.subheader("Informações sobre Valores Nulos")
    #st.write("### Valores nulos antes do tratamento")
    #st.dataframe(null_info_before)

    #st.write("### Valores nulos depois do tratamento")
    #st.dataframe(null_info_after)

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

    # GRÁFICO DE BARRAS
    # 1. Top 5 causas mais comuns
    top_5_causas = data["causa_acidente"].value_counts().nlargest(5)

    top_5_causas = top_5_causas.sort_values(ascending=True)

    # Configuração do Streamlit
    st.title("Análise de Acidentes")

    # Gráfico de barras para as top 5 causas mais comuns
    st.header("Top 5 Causas Mais Comuns dos Acidentes")

    # Criando o gráfico de barras com Plotly
    fig_causas = px.bar(
        top_5_causas,
        x=top_5_causas.values,
        y=top_5_causas.index,
        labels={"x": "Número de Acidentes", "y": "Causas dos Acidentes"},
        color=top_5_causas.values,
        text=top_5_causas.values,
        color_continuous_scale="Blues",
    )

    # Adiciona tooltips (informações ao passar o mouse sobre as barras)
    fig_causas.update_traces(
        hoverinfo="text",
        texttemplate="%{text}",
        textfont=dict(color="black"),
    )

    # Ajustar o layout para garantir boa apresentação
    fig_causas.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        xaxis_title="Número de Acidentes",
        yaxis_title="Causas dos Acidentes",
        font=dict(color="black"),
        # Cor dos títulos dos eixos
        xaxis_title_font=dict(color="white"),
        yaxis_title_font=dict(color="white"),
        # Cor dos valores dos eixos (ticks)
        xaxis_tickfont=dict(color="white"),
        yaxis_tickfont=dict(color="white"),
        # Cor da legenda
        legend_title_font=dict(color="white"),
        legend_font=dict(color="white"),
        # Alterando a cor da escala de cores
        coloraxis_colorbar_tickfont=dict(color="white"),
        coloraxis_colorbar_title_font=dict(color="white"),
    )

    # Exibir o gráfico interativo no Streamlit
    st.plotly_chart(fig_causas)

    # 2. Top 5 tipos mais comuns
    top_5_tipos = data["tipo_acidente"].value_counts().nlargest(5)

    top_5_tipos = top_5_tipos.sort_values(ascending=True)

    # Gráfico de barras para os top 5 tipos mais comuns de acidentes
    st.header("Top 5 Tipos Mais Comuns de Acidentes")

    # Criando o gráfico de barras com Plotly
    fig_tipos = px.bar(
        top_5_tipos,
        x=top_5_tipos.values,
        y=top_5_tipos.index,
        labels={"x": "Número de Acidentes", "y": "Tipos de Acidentes"},
        color=top_5_tipos.values,
        text=top_5_tipos.values,
        color_continuous_scale="Greens",
    )

    # Ajustar o layout para garantir boa apresentação
    fig_tipos.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        xaxis_title="Número de Acidentes",
        yaxis_title="Tipos de Acidentes",
        font=dict(color="black"),
        # Cor dos títulos dos eixos
        xaxis_title_font=dict(color="white"),
        yaxis_title_font=dict(color="white"),
        # Cor dos valores dos eixos (ticks)
        xaxis_tickfont=dict(color="white"),
        yaxis_tickfont=dict(color="white"),
        # Cor da legenda
        legend_title_font=dict(color="white"),
        legend_font=dict(color="white"),
        # Alterando a cor da escala de cores
        coloraxis_colorbar_tickfont=dict(color="white"),
        coloraxis_colorbar_title_font=dict(color="white"),
    )

    # Exibir o gráfico interativo no Streamlit
    st.plotly_chart(fig_tipos)

    # GRÁFICO DE DISPERSÃO
    # Configurar texto do Streamlit
    st.header("Relação entre Número de Vítimas e Condições Meteorológicas")
    st.write(
        "Este gráfico mostra a relação entre o número de vítimas e as condições meteorológicas nos acidentes."
    )

    # Contar o número de acidentes com mortos para cada condição meteorológica
    acidentes_com_mortos = (
        data.groupby("condicao_metereologica")["mortos"].sum().reset_index()
    )

    # Criar gráfico de dispersão com Plotly
    fig = px.scatter(
        acidentes_com_mortos,
        x="condicao_metereologica",
        y="mortos",
        color="condicao_metereologica",
        labels={
            "condicao_metereologica": "Condição Meteorológica",
            "mortos": "Número Vítimas",
        },
        hover_data=["condicao_metereologica", "mortos"],
    )

    # Definir o fundo branco para o gráfico
    fig.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        font=dict(color="black"),
        xaxis_title_font=dict(color="white"),
        yaxis_title_font=dict(color="white"),
        xaxis_tickfont=dict(color="white"),
        yaxis_tickfont=dict(color="white"),
        legend_title_font=dict(color="white"),
        legend_font=dict(color="white"),
    )

    # Exibir o gráfico interativo no Streamlit
    st.plotly_chart(fig)

    # MAPA INTERATIVO
    # Garantir que as colunas de latitude e longitude sejam convertidas para float
    data["latitude"] = pd.to_numeric(data["latitude"], errors="coerce")
    data["longitude"] = pd.to_numeric(data["longitude"], errors="coerce")

    # Passo 2: Filtrar as linhas com NaN nas colunas de latitude ou longitude
    data = data.dropna(subset=["latitude", "longitude"])

    # Contar o número de acidentes por município ou UF
    acidentes_por_municipio = (
        data.groupby(["municipio"])["id"]
        .count()
        .reset_index(name="quantidade_acidentes")
    )

    # Unir os dados de acidentes com o dataframe original para que possamos acessar a quantidade de acidentes por município
    df_map = data.merge(acidentes_por_municipio, on="municipio", how="left")

    # Criar o mapa interativo com Plotly
    fig = px.scatter_mapbox(
        df_map,
        lat="latitude",
        lon="longitude",
        hover_name="municipio",
        hover_data={
            "quantidade_acidentes": True,
        },
        size="quantidade_acidentes",
        color="quantidade_acidentes",
        color_continuous_scale="Blues",
        template="plotly",
    )

    # Configurar o mapa com a API do Mapbox
    fig.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        mapbox_style="carto-positron",
        mapbox_center={
            "lat": df_map["latitude"].mean(),
            "lon": df_map["longitude"].mean(),
        },
        mapbox_zoom=5,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )

    # Exibir o mapa no Streamlit
    st.header("Distribuição Geográfica dos Acidentes")
    st.plotly_chart(fig)

    # MAPA DE CALOR
    # Exibir título no Streamlit
    st.subheader("Relação entre dia da semana e período do dia")

    # Garantir que os dias da semana sigam a ordem correta
    dias_da_semana_ordem = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    data["dia_semana"] = pd.Categorical(
        data["dia_semana"], categories=dias_da_semana_ordem, ordered=True
    )

    # Garantir que os períodos do dia sigam a ordem correta
    periodos_dia_ordem = ["Madrugada", "Manhã", "Tarde", "Noite"]
    data["periodo_dia"] = pd.Categorical(
        data["periodo_dia"], categories=periodos_dia_ordem, ordered=True
    )

    # Agrupando por dia da semana e período do dia, contando IDs únicos
    heatmap_data = (
        data.groupby(["dia_semana", "periodo_dia"])["id"]
        .nunique()
        .reset_index(name="contagem_ids")
    )

    # Criando o gráfico de calor interativo
    fig = px.imshow(
        heatmap_data.pivot(
            index="periodo_dia", columns="dia_semana", values="contagem_ids"
        ),
        labels={
            "x": "Dia da Semana",
            "y": "Período do Dia",
            "color": "Número de acidentes",
        },
        color_continuous_scale="YlGnBu",
    )

    # Personalizando o layout do gráfico
    fig.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        font=dict(family="Arial", size=12, color="white"),
        xaxis=dict(
            title="Dia da Semana",
            tickfont=dict(family="Arial", size=10, color="white"),
        ),
        yaxis=dict(
            title="Período do Dia",
            tickfont=dict(family="Arial", size=10, color="white"),
        ),
        coloraxis_colorbar=dict(
            title="Contagem de IDs",
            tickfont=dict(family="Arial", size=10, color="white"),
        ),
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)

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
