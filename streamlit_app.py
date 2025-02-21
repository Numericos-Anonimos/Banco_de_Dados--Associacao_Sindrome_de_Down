import streamlit as st

st.set_page_config(page_title="Sistema ASIN", page_icon="Imagens/LogoASIN.png", layout="wide")
st.html('''<style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;} 
        </style>''')

pg = st.navigation([
    st.Page("pages/[0] Home.py", title="Home", icon="🏡"),
    st.Page("pages/[1] Atendidos.py", title="Atendidos", icon="📋"),
    st.Page("pages/[2] Colaboradores.py", title="Colaboradores", icon="👥"),
    st.Page("pages/[3] Eventos.py", title="Eventos", icon="🎉"),
    st.Page("pages/[4] Oficinas.py", title="Oficinas", icon="🛠️"),
    st.Page("pages/[5] Projetos.py", title="Projetos", icon="📊"),
    st.Page("pages/[6] Busca_Imagens.py", title="Busca de Imagens", icon="🔍"),
])

pg.run()