# 🚗 Análise de Acidentes de Trânsito no Brasil
Este projeto tem como objetivo analisar dados de acidentes de trânsito ocorridos no Brasil entre os anos de 2021 e 2024, utilizando técnicas de manipulação e visualização de dados. A análise fornece insights sobre os padrões de acidentes no Brasil, destacando aspectos como ano, localização geográfica (estado), tipo de acidente e outros fatores relevantes.

## 🛠️ Tecnologias Utilizadas
- Python: Linguagem principal.
- Pandas: Manipulação e limpeza de dados.
- Seaborn & Matplotlib: Visualização de dados.
- Streamlit: Desenvolvimento da interface interativa.

## 📂 Estrutura do Projeto
- Dados: Arquivos CSV contendo informações dos acidentes, organizados por ano.
- Processamento de Dados: Consolidação e limpeza dos dados para garantir consistência e qualidade.
- Aplicação Interativa: Interface desenvolvida com Streamlit para exploração dinâmica dos dados e visualização dos resultados.

## 📊 Visualizações
A aplicação permite explorar os dados por meio de diferentes gráficos interativos. Exemplos incluem:

- Distribuição de densidade para variáveis numéricas.
- Gráficos de dispersão para correlação entre variáveis.
- Boxplots para análise de outliers.
- Histograma para distribuição de frequências.

## 🚀 Como Executar
Clone o repositório:

```bash
git clone https://github.com/mdaefiol/analise_acidentes_de_transito.git
cd analise_acidentes_de_transito/scripts
```
- Para atualizar os requirements do projeto: `pip freeze > requirements.txt`
- Para instalar as dependencias do projeto: `pip install -r requirements.txt`
- Para rodar o app no terminal: 
```bash
cd analise_acidentes_de_transito/scripts
streamlit run app.py`
```

## 🔗 Aquisição dos Dados
Os dados utilizados neste projeto devem ser obtidos diretamente do portal da Polícia Rodoviária Federal (PRF). Acesse o link abaixo para realizar o download:

🌐 Portal de Dados Abertos da PRF (https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf).

Certifique-se de baixar os arquivos para os anos necessários e salvá-los no diretório data/ antes de executar os scripts.


## 🗂️ Estrutura de Pastas  
A estrutura de pastas do projeto é organizada da seguinte maneira:

```plaintext
📂 analise_acidentes_de_transito/
│
├── 📂 data/                       # Pasta para armazenar os dados (arquivos CSV)
│   ├── 2021.csv                   # Dados de acidentes de 2021
│   ├── 2022.csv                   # Dados de acidentes de 2022
│   ├── 2023.csv                   # Dados de acidentes de 2023
│   └── 2024.csv                   # Dados de acidentes de 2024
│
├── 📂 scripts/                    # Scripts principais de processamento de dados e análises
│   ├── requirements.txt           # Dependências do projeto
│   ├── app.py                     # Aplicação principal em Streamlit
│   └── data_processing.py         # Processamento e limpeza de dados
│
├── .gitignore                     # Arquivo para ignorar arquivos temporários
└── README.md                      # Arquivo de documentação do projeto
```

## 💡 Insights
Com base na análise dos dados sobre acidentes de trânsito no Brasil entre 2021 e 2024, foram identificados alguns insights importantes:

- **Principais Causas dos Acidentes**:
   - A reação tardia ou ineficiente do condutor é a principal causa dos acidentes, representando cerca de 14% dos casos. A ausência de reação do condutor é a segunda causa mais comum, com 13% dos acidentes.

- **Principais Tipos dos Acidentes**:
   - A colisão transeira é o principal tipo dos acidentes, representando cerca de 20% dos casos. A saída de leito carroçável é o segundo tipo mais comum, com 15% dos acidentes.

- **Fatalidades**:
   - 67% das fatalidades ocorreram quando a condição metereológica estava com céu claro.

- **Distribuição Geográfica**:
   - O município de Guarulhos registrou o maior número de acidentes com um total de 2504 acidentes, representando 2% do total de acidentes no Brasil e 21% do total de acidentes no estado de São Paulo.

   - O estado com mais registros de acidentes é o Rio de Janeiro, representando 11% do total de acidentes no Brasil. Por outro lado, o Amazonas é o estado com menor registro de acidentes, representando 0,2% dos casos no país.

- **Período**:
   - 29% dos acidentes aconteceram no período da noite, entre 18h e 00h. Além disso, 17% dos acidentes aconteceram no sábado e 5% dos acidentes aconteceram no sábado a noite.

- **Análise Temporal**:
   - O maior número de acidentes entre 2021-2024 ocorreu em 2023, 7% a mais do que o número registrado em 2022. Além disso, entre 2021 e 2024, o mês de julho registrou mais ocorrências, 49% a mais do que no mês de novembro.
