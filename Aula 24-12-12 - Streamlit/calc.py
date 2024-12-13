import streamlit as st

memoria = st.session_state
# cria uma variavel de sessão chamada memoria que nao muda de valor

st.title('Calculadora')

op_a = st.number_input('Digite o primeiro número')
op_b = st.number_input('Digite o segundo número')

col1, col2, col3, col4 = st.columns(4)

if 'res' not in memoria:
    memoria.res = 0

def somar(a, b):
    memoria.res = a + b

def subtrair(a, b):
    memoria.res = a - b

def multiplicar(a, b):
    memoria.res = a * b

def dividir(a, b):
    if b == 0:
        st.error('Não é possível dividir por zero')
    else:
        memoria.res = a / b

som = col1.button('➕ Somar', use_container_width=True, on_click=somar, args=(op_a, op_b))
sub = col2.button('➖ Subtrair', use_container_width=True, on_click=subtrair, args=(op_a, op_b))
mul = col3.button('✖️ Multiplicar', use_container_width=True, on_click=multiplicar, args=(op_a, op_b))
div = col4.button('➗ Dividir', use_container_width=True, on_click=dividir, args=(op_a, op_b))

st.write('Resultado:', memoria.res)
