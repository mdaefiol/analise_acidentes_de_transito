import time
import streamlit as st
import pandas as pd
import plotly.express as px
from data_processing import consolidate_data

# Função para carregamento dos dados e atualizar a barra de progresso


def load_data_with_progress():
    st.title("Análise de Acidentes de Trânsito")
    # Barra de progresso
    progress_bar = st.progress(0)
    progress_text = st.empty()

    # Simulação de carregamento de dados
    progress_text.text("Iniciando o carregamento dos dados...")
    for i in range(101):
        time.sleep(0.05)
        progress_bar.progress(i)

        # Atualiza o texto com a porcentagem
        progress_text.text(f"Carregando dados... {i}%")
    data, null_info_before, null_info_after = consolidate_data()

    if data is None:
        st.error("Erro ao carregar os dados consolidados.")
    else:
        st.success("Dados carregados com sucesso.")
        progress_bar.progress(100)

    return data


# Carregar os dados
data = load_data_with_progress()

if data is not None:
    ano_filtro = st.selectbox("Escolha o ano", data["ano"].unique())
    uf_filtro = st.selectbox("Escolha a UF", data["uf"].unique())
    tipo_acidente_filtro = st.selectbox(
        "Escolha o tipo de acidente", data["tipo_acidente"].unique()
    )

    # Filtra os dados com base nas escolhas
    data_filtrada = data[(
        data["ano"] == ano_filtro) &
        (data["uf"] == uf_filtro) &
        (data["tipo_acidente"] == tipo_acidente_filtro)
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
        progress_bar = st.progress(0)
        column = st.selectbox(
            "Escolha uma coluna numérica",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Distribuição de densidade da coluna {column}")
        fig = px.histogram(data_filtrada, x=column,
                           histnorm='density', nbins=30)
        fig.update_layout(title=f"Densidade de {column}")
        st.plotly_chart(fig)

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
            fig = px.scatter(data_filtrada, x=col1, y=col2)
            st.plotly_chart(fig)

    elif visual_option == "Boxplot":
        column = st.selectbox(
            "Escolha uma coluna numérica para o Boxplot",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Boxplot da coluna {column}")
        fig = px.box(data_filtrada, y=column)
        st.plotly_chart(fig)

    elif visual_option == "Histograma":
        column = st.selectbox(
            "Escolha uma coluna numérica para o Histograma",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Histograma da coluna {column}")
        fig = px.histogram(data_filtrada, x=column, nbins=30)
        st.plotly_chart(fig)

    elif visual_option == "Análise Temporal":
        column = st.selectbox(
            "Escolha uma coluna para análise temporal",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Análise Temporal da coluna {column}")

        data_filtrada["data_inversa"] = pd.to_datetime(
            data_filtrada["data_inversa"], errors="coerce")

        temporal_data = data_filtrada.groupby(
            data_filtrada["data_inversa"].dt.to_period("M"))[column].mean()

        fig = px.line(temporal_data, y=column,
                      title=f"Análise Temporal de {column}")
        st.plotly_chart(fig)

    # Gráfico de barras Top 5 Causas mais comuns
    top_5_causas = data["causa_acidente"].value_counts().nlargest(5)
    top_5_causas = top_5_causas.sort_values(ascending=True)

    st.header("Top 5 Causas Mais Comuns dos Acidentes")
    fig_causas = px.bar(
        top_5_causas,
        x=top_5_causas.values,
        y=top_5_causas.index,
        labels={"x": "Número de Acidentes", "y": "Causas dos Acidentes"},
        color=top_5_causas.values,
        text=top_5_causas.values,
        color_continuous_scale="Blues",
    )
    fig_causas.update_traces(
        hoverinfo="text",
        texttemplate="%{text}",
        textfont=dict(color="black"),
    )
    st.plotly_chart(fig_causas)

    # Top 5 Tipos mais comuns
    top_5_tipos = data["tipo_acidente"].value_counts().nlargest(5)
    top_5_tipos = top_5_tipos.sort_values(ascending=True)

    st.header("Top 5 Tipos Mais Comuns de Acidentes")
    fig_tipos = px.bar(
        top_5_tipos,
        x=top_5_tipos.values,
        y=top_5_tipos.index,
        labels={"x": "Número de Acidentes", "y": "Tipos de Acidentes"},
        color=top_5_tipos.values,
        text=top_5_tipos.values,
        color_continuous_scale="Greens",
    )
    st.plotly_chart(fig_tipos)

    # Gráfico de dispersão entre número de vítimas e condições meteorológicas
    st.header("Relação entre Número de Vítimas e Condições Meteorológicas")
    acidentes_com_mortos = data.groupby("condicao_metereologica")[
        "mortos"].sum().reset_index()
    fig = px.scatter(
        acidentes_com_mortos,
        x="condicao_metereologica",
        y="mortos",
        color="condicao_metereologica",
        labels={"condicao_metereologica": "Condição Meteorológica",
                "mortos": "Número Vítimas"},
    )
    st.plotly_chart(fig)

    # Mapa interativo
    data["latitude"] = pd.to_numeric(data["latitude"], errors="coerce")
    data["longitude"] = pd.to_numeric(data["longitude"], errors="coerce")
    data = data.dropna(subset=["latitude", "longitude"])

    acidentes_por_municipio = data.groupby(
        ["municipio"])["id"].count().reset_index(name="quantidade_acidentes")
    df_map = data.merge(acidentes_por_municipio, on="municipio", how="left")

    fig = px.scatter_mapbox(
        df_map,
        lat="latitude",
        lon="longitude",
        hover_name="municipio",
        hover_data={"quantidade_acidentes": True},
        size="quantidade_acidentes",
        color="quantidade_acidentes",
        color_continuous_scale="Blues",
        template="plotly",
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": df_map["latitude"].mean(
        ), "lon": df_map["longitude"].mean()},
        mapbox_zoom=5,
    )
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
