import streamlit as st

memoria = st.session_state

if 'cad_pessoa' not in st.session_state:
    memoria.cad_pessoa = {}


if 'cpf' not in st.session_state:
    st.session_state.cpf = {}
    st.session_state.nome = {}

st.title('Cadastro de Pessoas')

cpf = st.text_input('CPF')
nome = st.text_input('Nome')

esq, col1, col2, dir = st.columns([0.4, 0.1, 0.1, 0.4])

adicionar = col1.button('➕')
buscar = col2.button('🔎')

if adicionar:
    memoria.cad_pessoa[cpf] = nome
    st.success('Pessoa cadastrada com sucesso')
elif buscar:
    nome = memoria.cad_pessoa.get(cpf)

    if nome:
        st.success(f'Nome: {nome} CPF: {cpf}')
    else:
        st.error('CPF não encontrado')

st.table(memoria.cad_pessoa)
