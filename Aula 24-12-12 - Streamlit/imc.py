import streamlit as st

st.title('calculadora de IMC')

peso = st.number_input('Digite seu peso')
altura = st.number_input('Digite sua altura')

if altura != 0:
    imc = peso / altura ** 2
    st.write(f'O IMC é {imc:.2f}')

    if imc < 18.5:
        st.write('Abaixo do peso')
    elif imc < 25:
        st.write('Peso normal')
    elif imc < 30:
        st.write('Sobrepeso')
    else:
        st.write('Obesidade')