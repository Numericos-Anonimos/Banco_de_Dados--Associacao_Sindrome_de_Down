import streamlit as st
from datetime import date

#st.set_page_config(page_title="Eventos", layout="wide")

import streamlit as st
from datetime import date

eventos = [
    {"Cod_Evento": 1, "Nome": "Festa Junina", "Data": date(2021, 5, 4), "Observacao": "", "Quantidade_Externos": 40,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
    {"Cod_Evento": 2, "Nome": "Natal Solidário", "Data": date(2021, 12, 20), "Observacao": "Distribuição de presentes", "Quantidade_Externos": 60,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
    {"Cod_Evento": 3, "Nome": "Palestra Motivacional", "Data": date(2022, 3, 15), "Observacao": "Convidado especial", "Quantidade_Externos": 25,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
    {"Cod_Evento": 4, "Nome": "Dia da Família", "Data": date(2022, 6, 10), "Observacao": "Atividades recreativas", "Quantidade_Externos": 50},
    {"Cod_Evento": 5, "Nome": "Semana Cultural", "Data": date(2022, 9, 5), "Observacao": "Exposições e apresentações", "Quantidade_Externos": 80,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
    {"Cod_Evento": 6, "Nome": "Workshop de Tecnologia", "Data": date(2023, 2, 18), "Observacao": "Demonstrações de IA", "Quantidade_Externos": 30,"Imagem":["Imagens/Outras/competição de natação.jpeg"]}
]



def apresentando_eventos():
    st.title("Eventos Realizados")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .small-button button {
            width: 100px;
            font-size: 10px;
            padding: 5px;
            background-color: #ff4b4b;
            color: white;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .small-button button:hover {
            background-color: #ff1f1f;
        }
        .spaced-button {
            margin-top: 28px;
        }
        .evento-container {
            min-height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .evento-info {
            text-align: center;
        }
        .evento-img {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }
        .evento-img img {
            max-width: 100%;
            border-radius: 8px;
            padding-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Colunas para input do nome e botão Limpar
    col_input, col_button = st.columns([9, 1])
    with col_input:
        nome_evento = st.text_input(
            "Digite o nome do evento:",
            value="" if "nome_evento" not in st.session_state else st.session_state["nome_evento"]
        )
    with col_button:
        st.markdown('<div class="spaced-button">', unsafe_allow_html=True)
        if st.button("Limpar", key="clear_button"):
            for key in ["nome_evento", "data_inicio", "data_fim"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])

    data_inicio_default = min(evento["Data"] for evento in eventos)
    data_fim_default = max(evento["Data"] for evento in eventos)

    with col1:
        data_inicio = st.date_input(
            "Data Inicial", 
            value=(st.session_state.get("data_inicio") or data_inicio_default)
        )
    with col2:
        data_fim = st.date_input(
            "Data Final", 
            value=(st.session_state.get("data_fim") or data_fim_default)
        )

    st.session_state["data_inicio"] = data_inicio
    st.session_state["data_fim"] = data_fim
    st.session_state["nome_evento"] = nome_evento

    st.markdown("---")

    if data_inicio is None:
        data_inicio = data_inicio_default
    if data_fim is None:
        data_fim = data_fim_default

    eventos_filtrados = [
        evento for evento in eventos
        if data_inicio <= evento["Data"] <= data_fim and
           (nome_evento.lower() in evento["Nome"].lower() if nome_evento else True)
    ]

    if not eventos_filtrados:
        st.warning("Nenhum evento encontrado para os filtros aplicados.")

    for evento in eventos_filtrados:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(evento["Nome"])
                st.write(f"**Data:** {evento['Data'].strftime('%d/%m/%Y')}")
                st.write(f"**Observação:** {evento['Observacao'] if evento['Observacao'] else 'Nenhuma'}")
                st.write(f"**Quantidade de Externos:** {evento['Quantidade_Externos']}")

            with col2:
                if 'Imagem' in evento and evento['Imagem']:
                    st.markdown(
                        f"""
                        <div class="evento-img">
                            <img src="{evento['Imagem'][0]}" width="300, height=300">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    st.markdown("---")














# Chamando a função principal:
apresentando_eventos()


with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)