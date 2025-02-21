import streamlit as st

if "filtros" not in st.session_state:
    st.session_state["filtros"] = []

st.title("🔍 Busca de Imagens")

def imprimir_filtro(filtro):
    pass
    

for i in st.session_state["filtros"]:
    st.write(i)
