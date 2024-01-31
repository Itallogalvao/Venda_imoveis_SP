# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Apartamentos à venda na cidade de Sao Paulo, SP

# <h2>Projeto de Visualização de Dados de Imóveis em São Paulo</h2>
#
# Bem-vindo ao nosso projeto de visualização de dados de imóveis em São Paulo! Neste trabalho, exploramos uma análise geoespacial de vendas de imóveis na cidade de São Paulo, apresentando informações detalhadas sobre localização, valores, bairros e características dos imóveis.
#
# <h3> Objetivo: </h3>
#
# O objetivo principal deste projeto é proporcionar uma visualização interativa e informativa sobre as vendas de imóveis na região. Utilizamos bibliotecas populares como Folium, Geopandas e Plotly para criar mapas interativos, gráficos informativos e proporcionar uma experiência envolvente para quem estiver explorando os dados.
#
# <h3>Principais Componentes:</h3>
#
# 1. **Mapas Interativos:** Utilizamos Folium para criar mapas interativos que destacam a localização exata de cada venda de imóvel, permitindo uma visão espacial clara.
#
# 2. **Análise de Bairros:** Apresentamos uma análise detalhada dos bairros de São Paulo, destacando limites geográficos, cores personalizadas e informações específicas.
#
# 3. **Visualização de Dados:** Utilizando gráficos do Plotly, apresentamos comparações úteis, proporcionando uma visão mais aprofundada sobre características como valores totais, número de quartos e proximidade de estações.
#
# <h3>Como Explorar:</h3>
#
# Clique nos marcadores no mapa para obter detalhes sobre cada venda de imóvel.
# Utilize os gráficos interativos para comparar diferentes métricas.
# Acesse informações específicas sobre bairros ao passar o mouse sobre os limites no mapa.
# Esperamos que esta visualização forneça insights valiosos sobre o mercado imobiliário em São Paulo e torne a exploração dos dados uma experiência informativa e interessante.
#
# Vamos começar a explorar a cidade de São Paulo de uma maneira totalmente nova!
#
# Esse dataset foi encontrado no site do kaggle
# link: https://www.kaggle.com/datasets/jlgrego/apartamentos-venda-na-cidade-de-sao-paulo-sp
#
#
#

# +
# Este trecho de código utiliza diferentes bibliotecas para criar um ambiente integrado para visualização e análise de dados geoespaciais.
# Aqui estão as principais funções de cada biblioteca:

# - pandas: Manipulação de dados em formato tabular, incluindo a leitura e escrita de arquivos Excel e a criação de DataFrames.
# - numpy: Biblioteca para operações numéricas e manipulação de arrays, utilizada aqui para calcular a média das coordenadas.
# - folium: Criação de mapas interativos.
# - geopandas: Manipulação de dados geoespaciais, como leitura e escrita de arquivos shapefile e realização de operações espaciais.
# - shapely.geometry: Representação de geometrias, sendo utilizada aqui para criar pontos a partir de coordenadas de latitude e longitude.
# - plotly.express: Criação de visualizações de dados interativas, sendo usada aqui para criar gráficos de barras e mapa coroplético.

import pandas as pd
import numpy as np
import folium
import geopandas as gpd
from shapely.geometry import Point
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

# -

# Carregar DataFrame de imóveis a partir do Excel
imoveis_df = pd.read_excel('dados_wgs.xlsx')
# Exibir as primeiras 10 linhas do DataFrame
imoveis_df.head(10)

# Exibir informações sobre o DataFrame
imoveis_df.info()

# Exibir estatísticas descritivas transpostas do DataFrame
imoveis_df.describe().T

# Ordenar o DataFrame por valor total
imoveis_df_sorted = imoveis_df.sort_values(by='valor_total', ascending=False)

# Criar intervalos de cores
intervalos = [0,300000,500000,700000, 1000000, 2000000, 4000000, float('inf')]  # Defina seus próprios intervalos
cores = ['rgb(255, 0, 0)', 'rgb(255, 165, 0)', 'rgb(255, 255, 0)', 'rgb(0, 255, 0)', 'rgb(0, 255, 255)', 'rgb(0, 0, 255)', 'rgb(128, 0, 128)']

# Criar gráfico interativo de barras usando plotly
fig = px.bar(imoveis_df_sorted, y='bairro', x='valor_total', title='Comparação de Valores Totais por Bairro',
             labels={'valor_total': 'Valor Total (R$)'},
             color='valor_total',  # Adicionando cor com base no valor total
             color_continuous_scale=cores,  # Utilizando cores discretas
             color_discrete_map={str(intervalo): cor for intervalo, cor in zip(intervalos, cores)})

# +
# Adicionar interatividade ao gráfico

fig.update_traces(hovertemplate='<b>Bairro:</b> %{y}<br><b>Valor Total:</b> R$ %{x:,.2f}')
# Ajustar layout do gráfico
fig.update_layout(
    yaxis=dict(tickmode='array', tickvals=imoveis_df_sorted['bairro'], ticktext=imoveis_df_sorted['bairro']),
    xaxis=dict(title='Valor Total (R$)'),  # Adicione esta linha
    yaxis_title='Bairro',  # Corrija esta linha removendo "dict"
    paper_bgcolor='rgb(14,17,23)',  # Cor do fundo do gráfico
    plot_bgcolor='rgb(14,17,23)',   # Cor do fundo da área do gráfico
    font=dict(family='Arial, sans-serif', size=12, color='rgb(64, 64, 64)'),  # Estilo da fonte
    margin=dict(l=80, r=80, t=80, b=60)  # Margens ao redor do gráfico
)

# Ajustar tamanho do gráfico
fig.update_layout(height=1800, width=1000)

# Exibir o gráfico interativo
st.plotly_chart(fig, use_container_width=True)


# -

# Carregar arquivo GeoJSON com os limites dos distritos de São Paulo
arquivo_geojson_bairros = 'SAD69-96_SHP_distrito.geojson' 
bairros_sp = gpd.read_file(arquivo_geojson_bairros)

# Criar um mapa centrado na cidade de São Paulo
mapa = folium.Map(location=[-23.5505, -46.6333], zoom_start=11)

# Adicionar a geometria dos bairros de São Paulo ao mapa
folium.GeoJson(
    bairros_sp,
    name='Bairros SP',
    style_function=lambda feature: {
        'fillColor': 'green',   # Cor do preenchimento
        'color': 'black',       # Cor da borda
        'weight': 1,            # Largura da borda
        'fillOpacity': 0.2      # Opacidade do preenchimento
    }
).add_to(mapa)

# Adicionar marcadores para cada venda de imóvel dentro dos limites dos bairros
for index, row in imoveis_df.iterrows():
    popup_text = f"""
    <div style="max-width: 200px; text-align: center; font-family: Arial, sans-serif;">
        <h3 style="color: #3498db; margin-bottom: 5px;">Imóvel à Venda</h3>
        <p style="margin-bottom: 5px;"><b>Valor Total:</b> R$ {row['valor_total']:,.2f}</p>
        <p style="margin-bottom: 5px;"><b>Bairro:</b> {row['bairro']}</p>
        <p style="margin-bottom: 5px;"><b>Quartos:</b> {row['quartos']}</p>
        <p style="margin-bottom: 5px;"><b>Estação Próxima:</b> {row['estacao_prox']}</p>
    </div>
    """
     # Adicionar um marcador circular ao mapa com o pop-up
    folium.CircleMarker(
    location=[row['lat'], row['lon']],
    popup=popup_text,
    radius=2,
    color='black',         # Cor da borda
    fill=True,
    fill_color='green',    # Cor de preenchimento
    fill_opacity=1,      # Opacidade do preenchimento
    weight=1              # Largura da borda
    ).add_to(mapa)

st.title("Mapa Interativo com Streamlit")
st_mapa = st_folium(mapa, width = 750)