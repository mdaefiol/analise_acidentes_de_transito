import streamlit as st
import sweetviz as sv
import pandas as pd
from data_processing import check_files, load_data 


# Função para carregar os dados
@st.cache_data
def load_data(file_path):
    try:
        # Codificação 'ISO-8859-1' (ou 'latin1')
        data = pd.read_csv(file_path, encoding='ISO-8859-1')
        return data
    except Exception as e:
        return str(e)

# Verificar arquivos disponíveis
missing_files = check_files()

if missing_files:
    st.error(f"Arquivos de dados faltando: {', '.join(missing_files)}")
else:
    st.success("Arquivos de dados foram encontrados.")
    
    # Select para escolher o .csv
    selected_file = st.selectbox("Escolha o arquivo de dados", ["2021.csv", "2022.csv", "2023.csv", "2024.csv"])

    # Caminho do arquivo
    file_path = f"/home/hub/Documents/analise_acidentes_de_transito/data/{selected_file}"
    
    # Carregar os dados
    st.subheader(f"Dados de {selected_file}")
    data = load_data(file_path)
    
    if isinstance(data, str):  # Se existir erro
        st.error(data)
    else:
        # Gerar o relatório com Sweetviz
        report = sv.analyze(data)
        
        # Exibir o relatório no Streamlit
        st.write(report.show_html(), unsafe_allow_html=True)
