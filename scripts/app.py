import time
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
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
    # Total de acidentes sem filtro aplicado
    all_total_acidentes = len(data)

    # Ordenar labels dos meses no filtro
    meses_ordenados = sorted(
        data[["mes", "nome_mes"]].drop_duplicates().values, key=lambda x: x[0]
    )
    meses_ordenados = [mes[1] for mes in meses_ordenados]

    # Definição dos filtros
    ano_filtro = st.selectbox("Escolha o ano", ["Todos"] + sorted(data["ano"].unique()))
    mes_filtro = st.selectbox("Escolha o mês", ["Todos"] + meses_ordenados)
    uf_filtro = st.selectbox("Escolha a UF", ["Todos"] + sorted(data["uf"].unique()))
    tipo_acidente_filtro = st.selectbox(
        "Escolha o tipo de acidente", ["Todos"] + sorted(data["tipo_acidente"].unique())
    )

    # Filtra os dados com base nas escolhas
    if ano_filtro != "Todos":
        data = data[data["ano"] == ano_filtro]

    if mes_filtro != "Todos":
        data = data[data["nome_mes"] == mes_filtro]

    if uf_filtro != "Todos":
        data = data[data["uf"] == uf_filtro]

    if tipo_acidente_filtro != "Todos":
        data = data[data["tipo_acidente"] == tipo_acidente_filtro]

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
        fig = px.histogram(data, x=column, histnorm="density", nbins=30)
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
            fig = px.scatter(data, x=col1, y=col2)
            st.plotly_chart(fig)

    elif visual_option == "Boxplot":
        column = st.selectbox(
            "Escolha uma coluna numérica para o Boxplot",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Boxplot da coluna {column}")
        fig = px.box(data, y=column)
        st.plotly_chart(fig)

    elif visual_option == "Histograma":
        column = st.selectbox(
            "Escolha uma coluna numérica para o Histograma",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Histograma da coluna {column}")
        fig = px.histogram(data, x=column, nbins=30)
        st.plotly_chart(fig)

    elif visual_option == "Análise Temporal":
        column = st.selectbox(
            "Escolha uma coluna para análise temporal",
            data.select_dtypes(include=["int", "float"]).columns,
        )
        st.write(f"Análise Temporal da coluna {column}")

        data["data_inversa"] = pd.to_datetime(data["data_inversa"], errors="coerce")

        temporal_data = data.groupby(data["data_inversa"].dt.to_period("M"))[
            column
        ].mean()

        fig = px.line(temporal_data, y=column, title=f"Análise Temporal de {column}")
        st.plotly_chart(fig)

    # Gráfico de barras Top 5 Causas mais comuns
    top_5_causas = data["causa_acidente"].value_counts().nlargest(5)
    top_5_causas = top_5_causas.sort_values(ascending=True)
    top_5_causas = top_5_causas.reset_index()
    top_5_causas.columns = ["Causa do Acidente", "Número de Acidentes"]

    st.subheader("Top 5 Causas Mais Comuns dos Acidentes")

    fig_causas = px.bar(
        top_5_causas,
        x="Número de Acidentes",
        y="Causa do Acidente",
        labels={
            "Número de Acidentes": "Número de Acidentes",
            "Causa do Acidente": "Causa do Acidente",
        },
        color="Número de Acidentes",
        text="Número de Acidentes",
        color_continuous_scale="Blues",
        hover_data={"Número de Acidentes": True, "Causa do Acidente": True},
    )

    fig_causas.update_layout(
        xaxis_visible=False,
        xaxis_showticklabels=False,
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        font=dict(family="Arial", size=12, color="white"),
        yaxis=dict(
            title="",
        ),
        coloraxis_showscale=False,
    )

    st.plotly_chart(fig_causas)

    # Insights
    total_acidentes = len(data)
    causa_mais_comum = top_5_causas.iloc[4]
    causa_mais_comum_nome = causa_mais_comum["Causa do Acidente"]
    causa_mais_comum_acidentes = causa_mais_comum["Número de Acidentes"]
    causa_mais_comum_percentual = (causa_mais_comum_acidentes / total_acidentes) * 100

    st.write(
        f"A causa mais comum de acidente é **{causa_mais_comum_nome}**, com um total de **{causa_mais_comum_acidentes}** acidentes, "
        f"representando **{causa_mais_comum_percentual:.1f}%** do total de acidentes."
    )

    # Top 5 Tipos mais comuns
    top_5_tipos = data["tipo_acidente"].value_counts().nlargest(5)
    top_5_tipos = top_5_tipos.sort_values(ascending=True)
    top_5_tipos = top_5_tipos.reset_index()
    top_5_tipos.columns = ["Tipo do Acidente", "Número de Acidentes"]

    st.subheader("Top 5 Tipos Mais Comuns de Acidentes")

    fig_tipos = px.bar(
        top_5_tipos,
        x="Número de Acidentes",
        y="Tipo do Acidente",
        labels={
            "Número de Acidentes": "Número de Acidentes",
            "Tipo do Acidente": "Tipo de Acidente",
        },
        color="Número de Acidentes",
        text="Número de Acidentes",
        color_continuous_scale="Greens",
        hover_data={"Número de Acidentes": True, "Tipo do Acidente": True},
    )

    fig_tipos.update_layout(
        xaxis_visible=False,
        xaxis_showticklabels=False,
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        font=dict(family="Arial", size=12, color="white"),
        yaxis=dict(
            title="",
        ),
        coloraxis_showscale=False,
    )

    st.plotly_chart(fig_tipos)

    # Insights
    tipo_mais_comum = top_5_tipos.iloc[4]
    tipo_mais_comum_nome = tipo_mais_comum["Tipo do Acidente"]
    tipo_mais_comum_acidentes = tipo_mais_comum["Número de Acidentes"]
    tipo_mais_comum_percentual = (tipo_mais_comum_acidentes / total_acidentes) * 100

    st.write(
        f"O tipo mais comum de acidente é **{tipo_mais_comum_nome}**, com um total de **{tipo_mais_comum_acidentes}** acidentes, "
        f"representando **{tipo_mais_comum_percentual:.1f}%** do total de acidentes."
    )

    # Gráfico de dispersão entre número de vítimas e condições meteorológicas
    st.subheader("Relação entre Número de Vítimas e Condições Meteorológicas")

    acidentes_com_mortos = (
        data.groupby("condicao_metereologica")["mortos"].sum().reset_index()
    )

    fig = px.scatter(
        acidentes_com_mortos,
        x="condicao_metereologica",
        y="mortos",
        color="condicao_metereologica",
        labels={
            "condicao_metereologica": "Condição Meteorológica",
            "mortos": "Número de Vítimas",
        },
    )

    fig.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
    )

    st.plotly_chart(fig)

    # Insights
    total_mortos = data["mortos"].sum()
    maior_valor = acidentes_com_mortos["mortos"].max()
    condicao_com_maior_ocorrencia = acidentes_com_mortos.loc[
        acidentes_com_mortos["mortos"] == maior_valor, "condicao_metereologica"
    ].iloc[0]
    condicao_percentual = (maior_valor / total_mortos) * 100

    st.write(
        f"A condição meteorológica com mais registros de vítimas fatais é **{condicao_com_maior_ocorrencia}**, com um total de **{maior_valor}** vítimas, "
        f"representando **{condicao_percentual:.1f}%** do total de vítimas fatais."
    )

    # Mapa interativo
    st.subheader("Ditribuição Geográfica dos Acidentes")

    data["latitude"] = data["latitude"].str.replace(",", ".").astype(float)
    data["longitude"] = data["longitude"].str.replace(",", ".").astype(float)
    data["latitude"] = data["latitude"].round().astype(int)
    data["longitude"] = data["longitude"].round().astype(int)

    group = (
        data.groupby(["municipio", "latitude", "longitude"])["id"]
        .size()
        .reset_index(name="quantidade_acidentes")
    )

    # Arredondamento latitude e longitude
    acidentes_por_municipio = (
        group.groupby("municipio")
        .agg(
            {
                "latitude": "mean",
                "longitude": "mean",
                "quantidade_acidentes": "sum",
            }
        )
        .reset_index()
    )

    fig = px.scatter_mapbox(
        acidentes_por_municipio,
        lat="latitude",
        lon="longitude",
        hover_name="municipio",
        hover_data={
            "quantidade_acidentes": True,
            "latitude": False,
            "longitude": False,
        },
        size="quantidade_acidentes",
        color="quantidade_acidentes",
        color_continuous_scale="Inferno",
        template="plotly",
    )
    fig.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        mapbox_style="carto-positron",
        mapbox_center={
            "lat": acidentes_por_municipio["latitude"].mean(),
            "lon": acidentes_por_municipio["longitude"].mean(),
        },
        coloraxis_showscale=False,
        mapbox_zoom=3,
        height=500,
    )

    st.plotly_chart(fig)

    # Insights
    acidentes_por_municipio_sorted = acidentes_por_municipio.sort_values(
        by="quantidade_acidentes", ascending=False
    )

    if uf_filtro == "Todos":
        st.write(
            f"A cidade com mais registros de acidentes é **{acidentes_por_municipio_sorted.iloc[0]["municipio"]}**, com um total de **{acidentes_por_municipio_sorted.iloc[0]["quantidade_acidentes"]}** acidentes, "
            f"representando **{(acidentes_por_municipio_sorted.iloc[0]["quantidade_acidentes"] / total_acidentes) * 100:.1f}%** do total de acidentes no Brasil."
        )
    else:
        st.write(
            f"A cidade com mais registros de acidentes é **{acidentes_por_municipio_sorted.iloc[0]["municipio"]}**, com um total de **{acidentes_por_municipio_sorted.iloc[0]["quantidade_acidentes"]}** acidentes, "
            f"representando **{(acidentes_por_municipio_sorted.iloc[0]["quantidade_acidentes"] / total_acidentes) * 100:.1f}%** do total de acidentes no estado de **{uf_filtro}**."
        )

    # MAPA DE CALOR
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
            title="Número de Acidentes",
            tickfont=dict(family="Arial", size=10, color="white"),
        ),
    )

    st.plotly_chart(fig)

    # GRÁFICO DE COLUNAS
    # Analisar número de acidentes por UF
    st.subheader("Número de Acidentes por Estado")

    acidentes_uf = data.groupby("uf")["id"].nunique().reset_index(name="acidentes")

    fig = px.bar(
        acidentes_uf,
        x="uf",
        y="acidentes",
        labels={
            "uf": "UF",
            "acidentes": "Número de Acidentes",
        },
        text="acidentes",
    )

    fig.update_traces(texttemplate="%{text}", textposition="inside")

    fig.update_layout(
        yaxis_visible=False,
        yaxis_showticklabels=False,
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
    )

    fig.update_traces(marker_color="#1f77b4")

    st.plotly_chart(fig)

    # Insights
    acidentes_uf_sorted = acidentes_uf.sort_values(by="acidentes", ascending=False)

    acidentes_uf_sorted_ascending = acidentes_uf.sort_values(
        by="acidentes", ascending=True
    )

    if uf_filtro == "Todos":
        st.write(
            f"O estado com mais registros de acidentes é **{acidentes_uf_sorted.iloc[0]["uf"]}**, com um total de **{acidentes_uf_sorted.iloc[0]["acidentes"]}** acidentes, "
            f"representando **{(acidentes_uf_sorted.iloc[0]["acidentes"] / total_acidentes) * 100:.1f}%** do total de acidentes no Brasil, seguido de **{acidentes_uf_sorted.iloc[1]["uf"]}** "
            f"com **{acidentes_uf_sorted.iloc[1]["acidentes"]}** acidentes. Por outro lado, o estado com menor registro de acidentes é **{acidentes_uf_sorted_ascending.iloc[0]["uf"]}** com **{acidentes_uf_sorted_ascending.iloc[0]["acidentes"]}** acidentes."
        )
    else:
        st.write(
            f"O estado de **{(uf_filtro)}** registrou um total de **{(acidentes_uf_sorted.iloc[0]["acidentes"])}** acidentes, "
            f"representando **{(acidentes_uf_sorted.iloc[0]["acidentes"] / all_total_acidentes) * 100:.1f}%** do total de acidentes no Brasil."
        )

    # GRÁFICO DE ROSCA
    # Acidentes em feriados ou não
    st.subheader("Número de acidentes em feriados")

    pie_data = data.groupby("feriado")["id"].nunique().reset_index(name="acidentes")

    fig = px.pie(pie_data, names="feriado", values="acidentes", hole=0.4)
    fig.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        legend=dict(
            orientation="v",
            x=1,
            y=0.5,
            xanchor="left",
            yanchor="middle",
            font=dict(color="white"),
        ),
    )

    st.plotly_chart(fig)

    # Insights
    pie_data_sorted = pie_data.sort_values(by="acidentes", ascending=False)

    if pie_data_sorted.iloc[0]["feriado"] == "Sim":
        st.write(
            f"A maioria dos acidentes (**{(pie_data_sorted.iloc[0]["acidentes"])}** - **{(pie_data_sorted.iloc[0]["acidentes"] / total_acidentes) * 100:.1f}%**) aconteceram em feriados."
        )
    else:
        st.write(
            f"A maioria dos acidentes (**{(pie_data_sorted.iloc[0]["acidentes"])}** - **{(pie_data_sorted.iloc[0]["acidentes"] / total_acidentes) * 100:.1f}%**) aconteceram quando não era feriado."
        )

    # GRÁFICO TEMPORAL
    st.subheader("Análise de acidentes ao longo do tempo")

    # Periodicidade dinâmica
    period_map = {"Dia": "D", "Mês": "M", "Ano": "Y"}  # Diário  # Mensal  # Anual

    if mes_filtro == "Todos":
        idx = 1
    else:
        idx = 0

    analise = st.selectbox(
        "Escolha a periodicidade da análise", ["Dia", "Mês", "Ano"], index=idx
    )

    selected_period = period_map[analise]

    df_agrupado = (
        data.groupby([data["data_inversa"].dt.to_period(selected_period)])["id"]
        .nunique()
        .reset_index(name="quantidade_acidentes")
    )

    df_agrupado["data_inversa"] = df_agrupado["data_inversa"].dt.to_timestamp()

    # Criando gráfico de linha interativo
    fig = px.line(
        df_agrupado,
        x="data_inversa",
        y="quantidade_acidentes",
        labels={
            "data_inversa": "Data",
            "quantidade_acidentes": "Número de Acidentes",
        },
    )

    fig.update_layout(
        plot_bgcolor="#26292e",
        paper_bgcolor="#26292e",
        xaxis=dict(
            title="",
        ),
        yaxis=dict(
            title="",
        ),
    )

    fig.update_traces(line=dict(color="#1f77b4"))

    st.plotly_chart(fig)
