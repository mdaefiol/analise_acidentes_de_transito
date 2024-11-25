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
cd analise_acidentes_de_transito
```

### Para desenvolvedores:
- Para atualizar os requirements do projeto: `pip freeze > requirements.txt`
- Para rodar o app no terminal: `streamlit run app.py`

### Para o usuario:
- Para instalar as dependencias do projeto: `pip install -r requirements.txt`

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
├── 📂 documentation/               # Documentação adicional
│   └── Exercicio.pdf              # Exercício ou explicação do projeto
│
├── 📂 scripts/                     # Scripts principais de processamento de dados e análises
│   ├── app.py                     # Aplicação principal em Streamlit
│   └── data_processing.py         # Processamento e limpeza de dados
│
├── .gitignore                     # Arquivo para ignorar arquivos temporários
├── requirements.txt               # Dependências do projeto
└── README.md                      # Arquivo de documentação do projeto
```
