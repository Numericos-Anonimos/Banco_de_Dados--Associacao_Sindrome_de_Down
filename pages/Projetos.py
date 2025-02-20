import streamlit as st


st.set_page_config(page_title="Projetos", layout="wide")


st.title("Projetos")


with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)
    st.write("Ferramentas: ")