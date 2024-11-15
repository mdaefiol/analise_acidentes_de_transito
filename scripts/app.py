import streamlit as st
from data_processing import load_data, check_files  # para usar o data processing, funcoes especificas

# Verificar arquivos disponíveis
missing_files = check_files()

if missing_files:
    st.error(f"Arquivos de dados faltando: {', '.join(missing_files)}")
else:
    st.success("Arquivos de dados foram encontrados.")
    
    # Select para escolher o .csv
    selected_file = st.selectbox("Escolha o arquivo de dados", ["2021.csv", "2022.csv", "2023.csv", "2024.csv"])
    
    # Caminho dos arquivos
    file_path = f"/home/hub/Documents/analise_acidentes_de_transito/data/{selected_file}"
    
    # Carrega e exibe os dados
    st.subheader(f"Dados de {selected_file}")
    data = load_data(file_path)
    if isinstance(data, str):  # Se existir erro
        st.error(data)
    else:
        st.dataframe(data)  # Exibe normalmente

