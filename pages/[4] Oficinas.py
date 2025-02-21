import streamlit as st
import pandas as pd
from datetime import datetime, time, date
from st_aggrid import AgGrid, GridOptionsBuilder
import os

import Banco_de_Dados.Oficinas as bd


#st.set_page_config(page_title="Oficinas", layout="wide")


oficinas_bd = bd.listar_oficinas() 

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

def sub_hora(ini:time, fim:time):
    return (fim.hour - ini.hour) * 60 + (fim.minute - ini.minute)

def exibir_imagem(foto):
    """
    Exibe a imagem localizada dentro da pasta "Banco de Imagens".
    Se o arquivo não existir, exibe uma mensagem de erro.
    """
    caminho_imagem = os.path.join("Banco de Imagens", foto)
    
    if not os.path.exists(caminho_imagem):
        st.error(f"Imagem não encontrada: {foto}")
    else:
        try:
            st.image(caminho_imagem, caption=foto, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao exibir a imagem: {foto}\n{str(e)}")

def exibir_dados(dados: dict):
    st.title("Detalhes da Oficina")

    # Informações básicas
    with st.expander("📌 Informações Básicas"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Código:** {dados.get('Código')}")
            st.write(f"**Oficina:** {dados.get('Oficina')}")
            st.write(f"**Projeto:** {dados.get('Projeto')}")
            st.write(f"**Data de Início:** {dados.get('Data de Início')}")
            st.write(f"**Data de Término:** {dados.get('Data de Término', 'Não definida')}")
        with col2:
            st.write(f"**Dia da Semana:** {dados.get('Dia da Semana')}")
            st.write(f"**Hora de Início:** {dados.get('Hora de Início')}")
            st.write(f"**Hora de Término:** {dados.get('Hora de Término')}")
            st.write(f"**Vagas:** {dados.get('Vagas')}")
            st.write(f"**Preço:** R$ {dados.get('Preço')}")

    # Responsável
    with st.expander("👤 Responsável"):
        st.write(f"**Nome:** {dados.get('Responsável')}")
        st.write(f"**Código do Responsável:** {dados.get('Código do Responsável')}")
        st.write(f"**Descrição:** {dados.get('Descricao')}")

    # Houve Oficina
    if "Houve_Oficina" in dados:
        with st.expander("📅 Datas das Oficinas"):
            for data in dados["Houve_Oficina"]:
                st.write(f"- {data}")

    # Presenças
    if "Presenças" in dados:
        with st.expander("✅ Presenças"):
            for nome, datas in dados["Presenças"].items():
                st.write(f"**{nome}:**")
                for data in datas:
                    st.write(f"- {data}")

    # Fotos
    if "Fotos" in dados:
        with st.expander("📸 Fotos da Oficina"):
            fotos = dados["Fotos"]
            num_colunas = 2
            for i in range(0, len(fotos), num_colunas):
                cols = st.columns(num_colunas)
                for j, foto in enumerate(fotos[i:i+num_colunas]):
                    with cols[j]:
                        exibir_imagem(foto)



def apresentar_oficinas2(oficinas):
        st.title("Oficinas")
        st.markdown("<br>", unsafe_allow_html=True)

        gb = GridOptionsBuilder.from_dataframe(oficinas)
        gb.configure_default_column(resizable=True, minColumnWidth=200, flex=1)
        gb.configure_selection('single', use_checkbox=False)
        gridOptions = gb.build()
        gridOptions["domLayout"] = "autoHeight"

        grid_response = AgGrid(
            oficinas,
            gridOptions=gridOptions,
            use_container_width=True,
            height=500,
            update_mode='SELECTION_CHANGED',
            fit_columns_on_grid_load=True,
            rowHeight=30,
            key='grid_oficinas'
        )

        st.markdown("---")

        selected = grid_response.get("selected_rows")
        if selected is None or selected.empty:
            st.info("Nenhuma oficina selecionada.")
        else:
            cod_oficina = selected.iloc[0]["Código"]
            oficina = bd.buscar_oficina(cod_oficina)
            exibir_dados(oficina)
        




apresentar_oficinas2(oficinas_bd)



with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)
