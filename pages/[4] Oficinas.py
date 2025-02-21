import streamlit as st
import pandas as pd
from datetime import datetime, time, date
from st_aggrid import AgGrid, GridOptionsBuilder
import os
import uuid
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

    st.markdown(
        """
        <style>
        .ag-theme-alpine {
            --ag-secondary-background-color: #005f88;
        }
        .small-button button {
            width: 100px;  
            font-size: 8px;
            padding: 0px;
            background-color: #ff4b4b;
            color: white;
            border-radius: 0px;
            border: none;
            cursor: pointer;
        }
        .small-button button:hover {
            background-color: #ff1f1f;
        }
        .spaced-button {
            margin-top: 28px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Inicializando estado da sessão
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = None
    if "nome_funcionario" not in st.session_state:
        st.session_state.nome_funcionario = ""
    if "grid_key" not in st.session_state:
        st.session_state.grid_key = str(uuid.uuid4())

    # Layout do input e botão limpar
    col_input, col_button = st.columns([9, 1])
    with col_input:
        nome_funcionario = st.text_input(
            "Digite o nome do atendido:",
            key=f"search_input_{st.session_state.grid_key}",
            value=st.session_state.nome_funcionario
        )
    with col_button:
        st.markdown('<div class="spaced-button">', unsafe_allow_html=True)
        if st.button("Limpar", key="clear_button"):
            st.session_state.nome_funcionario = ""  # Limpa o campo de entrada
            st.session_state.grid_key = str(uuid.uuid4())  # Atualiza a chave para forçar a atualização
            st.session_state.selected_user = None 
            st.rerun()  # Recarrega a página para aplicar mudanças
        st.markdown('</div>', unsafe_allow_html=True)

    # Filtra oficinas com base no input
    oficinas_filtradas = oficinas[oficinas["Oficina"].str.contains(nome_funcionario, case=False, na=False)] if nome_funcionario else oficinas

    # Criando grid interativa
    gb = GridOptionsBuilder.from_dataframe(oficinas_filtradas)
    gb.configure_default_column(resizable=True, minColumnWidth=200, flex=1)
    gb.configure_selection('single', use_checkbox=False)
    gridOptions = gb.build()
    gridOptions["domLayout"] = "autoHeight"

    grid_response = AgGrid(
        oficinas_filtradas,
        gridOptions=gridOptions,
        use_container_width=True,
        height=500,
        update_mode='SELECTION_CHANGED',
        fit_columns_on_grid_load=True,
        rowHeight=30,
        key=st.session_state.grid_key  # Atualiza a chave para forçar re-renderização
    )

    st.markdown("---")

    selected = grid_response.get("selected_rows")

    if isinstance(selected, pd.DataFrame):  
        selected = selected.to_dict(orient="records")  # Converte DataFrame para lista de dicionários

    if selected and len(selected) > 0:
        cod_oficina = selected[0].get("Código")
        if cod_oficina is not None:
            oficina = bd.buscar_oficina(cod_oficina)
            exibir_dados(oficina)
        else:
            st.warning("A oficina selecionada não contém um código válido.")
    else:
        st.info("Nenhuma oficina selecionada.")






apresentar_oficinas2(oficinas_bd)



with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)
