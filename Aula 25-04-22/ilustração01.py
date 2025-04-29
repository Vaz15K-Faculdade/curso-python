import streamlit as st
import pandas as pd

import plotly.express as px

def carregar_dados(path = None):
    if path:
        df = pd.read_csv(path)
    else:
        df = pd.read_csv('Aula 25-04-22/vgsales.csv')
    return df

def obter_datas(df):
    return int(df['Year'].min()), int(df['Year'].max())

df = carregar_dados()

with st.sidebar:
    ano_minimo, ano_maximo = st.slider(
        'Selecione o intervalo de tempo',
        min_value = int(df['Year'].min()),
        max_value = int(df['Year'].max()),
        value = (int(df['Year'].min()), int(df['Year'].max()))
    )

    plataformas = st.multiselect(
        'Selecione as plataformas',
        options=df['Platform'].unique(),
        default=[]
    )

    generos = st.multiselect(
        'Selecione os gêneros',
        options=df['Genre'].unique(),
        default=[]
    )

    publishers = st.multiselect(
        'Selecione as editoras',
        options=df['Publisher'].unique(),
        default=[]
    )

df_filtrado = df[
    (df['Year'] >= ano_minimo) & (df['Year'] <= ano_maximo) &
    (df['Platform'].isin(plataformas) if plataformas else True) &
    (df['Genre'].isin(generos) if generos else True) &
    (df['Publisher'].isin(publishers) if publishers else True) 
]

st.header('Análise de Vendas de Video Games')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label='Total de jogos', value = len(df_filtrado))
with col2:
    st.metric(label='Ano Jogo mais Antigo', value=int(df_filtrado['Year'].min()))
with col3:
    st.metric(label='Ano Jogo mais Novo', value=int(df_filtrado['Year'].max()))
with col4:
    st.metric(label='Media de vendas', value=f"${df_filtrado['Global_Sales'].mean():.2f}M")
with col5:
    st.metric(label='Editora com mais jogos', value=df_filtrado['Publisher'].value_counts().idxmax())

# https://drive.google.com/drive/folders/1oXLtJfn4PJIJtqjCg0T1FZaHSXDgb_EI?usp=sharing
