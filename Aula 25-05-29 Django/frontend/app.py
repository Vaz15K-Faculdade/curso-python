import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from frontend.backend import *

if "produtos_venda" not in st.session_state:
    st.session_state.produtos_venda = []

st.title("Sistema PDV")

produtos = get_produtos()

def formatar_produto(produto):
    return f"{produto['descricao']} - R$ {produto['valor']:.2f}"

produto_selecionado = st.selectbox("Produto", produtos, format_func=formatar_produto)
quantidade = st.number_input("Quantidade", min_value=0)
st.button("Adicionar ao Carrinho", use_container_width=True)

if st.button("Adicionar ao Carrinho", use_container_width=True):
    produto = {
        "id": produto_selecionado['id'],
        "descricao": produto_selecionado['descricao'],
        "quantidade": quantidade
    }
    st.session_state.produtos_venda.append(produto)
    st.success(f"Produto {produto['descricao']} adicionado ao carrinho.")