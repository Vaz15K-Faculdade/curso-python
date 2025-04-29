# app.py  
import streamlit as st  
import plotly.express as px
import pandas as pd
import numpy as np

st.title('Meu Dashboard')  
df = px.data.tips()  
st.write("Visualização de Dados: Dataset Tips")  

# Widgets  
opcao = st.selectbox('Selecione a coluna para cor:', ['sex', 'smoker', 'day'])  

# Atualizar gráfico com base na seleção  
fig = px.scatter(df, x='total_bill', y='tip', color=opcao)  
st.plotly_chart(fig)


col1, col2 = st.columns(2)  
with col1:  
    st.header("Gráfico 1")  
    fig1 = px.histogram(df, x='total_bill')  
    st.plotly_chart(fig1)  

with col2:  
    st.header("Gráfico 2")  
    fig2 = px.box(df, x='day', y='total_bill')  
    st.plotly_chart(fig2)  

# Gráfico de Pizza
df = px.data.tips()
fig = px.pie(df, values='tip', names='day')
st.plotly_chart(fig)


# Gráfico interativo de uma api externa
import requests  
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=brl&days=30'  
response = requests.get(url).json()  
prices = pd.DataFrame(response['prices'], columns=['timestamp', 'price'])  
prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')  
fig = px.line(prices, x='date', y='price', title='Preço do Bitcoin (Últimos 30 dias)')  
st.plotly_chart(fig)  


st.header("Visualização 3D")

# Dataset do Gapminder
df_gapminder = px.data.gapminder().query("year == 2007")

# Gráfico 3D Interativo
fig3d = px.scatter_3d(df_gapminder, x='gdpPercap', y='lifeExp', z='pop',
                        color='continent', size='pop', 
                        hover_name='country', log_x=True,
                        title="GDP vs Expectativa de Vida vs População (2007)")
st.plotly_chart(fig3d, use_container_width=True)







st.header("Anomalia de Temperatura Global")
try:
    url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    df = pd.read_csv(url, skiprows=1)[['Year', 'J-D']]
    df = df.rename(columns={'Year': 'Ano', 'J-D': 'Temperatura'})

    ano_min = int(df['Ano'].min())
    ano_max = int(df['Ano'].max())

    ano_slider = st.slider('Ano', ano_min, ano_max, (ano_min, ano_max))
    df_filtered = df[df['Ano'].between(ano_slider[0], ano_slider[1])]

    
    fig = px.line(df_filtered, x='Ano', y='Temperatura', 
                    title="Anomalia de Temperatura Global (°C)",
                    markers=True)
    fig.add_hline(y=0, line_dash="dash")
    st.plotly_chart(fig, use_container_width=True)
except:
    st.error("Dados climáticos indisponíveis")



st.header('Outros exemplos de componentes streamlit')


url = "https://streamlit.io"
data = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])


st.checkbox("I agree")
st.feedback("thumbs")
st.pills("Tags", ["Sports", "Politics"])
st.radio("Pick one", ["cats", "dogs"])
st.segmented_control("Filter", ["Open", "Closed"])
st.toggle("Enable")
st.selectbox("Pick one", ["cats", "dogs"])
st.multiselect("Buy", ["milk", "apples", "potatoes"])
st.slider("Pick a number", 0, 100)
st.select_slider("Pick a size", ["S", "M", "L"])
st.date_input("Your birthday")
st.time_input("Meeting time")


for i in range(int(st.number_input("Num:"))):
    st.write(i)
if st.sidebar.selectbox("Teste:",["f", "g"]) == "f":
    st.write('teste')