import streamlit as st
st.set_page_config(page_title="Sistema ASIN", page_icon="Imagens/LogoASIN.png", layout="wide")
st.html('''<style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;} 
        </style>''')



with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_column_width=True)
    st.write("Ferramentas: ")
    
    # Adicionar asin no final

