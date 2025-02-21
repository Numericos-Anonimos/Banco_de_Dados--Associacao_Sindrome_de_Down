import streamlit as st
from datetime import date
import streamlit as st
from datetime import date
from Banco_de_Dados.Eventos import *
from datetime import datetime
import uuid

eventos = listar_eventos()


def apresentando_eventos():
    st.title("Eventos Realizados")
    st.markdown("<br>", unsafe_allow_html=True)

    # Estilização customizada
    st.markdown(
        """
        <style>
        .spaced-button { margin-top: 28px; }
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
        .evento-info { text-align: center; }
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

    # Seção de Filtros
    col_input, col_button = st.columns([9, 1])
    with col_input:
        nome_evento = st.text_input("Digite o nome do evento:", st.session_state.get("nome_evento", ""))

    with col_button:
        st.markdown('<div class="spaced-button">', unsafe_allow_html=True)
        if st.button("Limpar", key="clear_button"):
            st.session_state.nome_evento = ""  # Limpa o nome do evento
            st.session_state.data_inicio = date(2024, 1, 1)  # Reseta data inicial
            st.session_state.data_fim = date.today()  # Reseta data final
            st.session_state.grid_key = str(uuid.uuid4())  # Gera nova chave para reinicializar a interface
            st.rerun()  # Recarrega a página
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input("Data Inicial", st.session_state.get("data_inicio", date(2024, 1, 1)))
    with col2:
        data_fim = st.date_input("Data Final", st.session_state.get("data_fim", date.today()))

    # Atualizando session state com os novos valores
    st.session_state["data_inicio"] = data_inicio
    st.session_state["data_fim"] = data_fim
    st.session_state["nome_evento"] = nome_evento

    st.markdown("---")

    # Filtrar eventos com base nos filtros aplicados
    eventos_filtrados = [
        evento for evento in eventos
        if data_inicio <= datetime.strptime(evento["Data"], "%Y-%m-%d %H:%M:%S").date() <= data_fim and
        (nome_evento.lower() in evento["Evento"].lower() if nome_evento else True)
    ]

    if not eventos_filtrados:
        st.warning("Nenhum evento encontrado para os filtros aplicados.")

    for evento in eventos_filtrados:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(evento["Evento"])
                data_evento = datetime.strptime(evento["Data"], "%Y-%m-%d %H:%M:%S")
                st.write(f"**Data:** {data_evento.strftime('%d/%m/%Y %H:%M')}")  # Inclui horário no formato correto
                st.write(f"**Observação:** {evento['Observações'] if evento['Observações'] else 'Nenhuma'}")
                st.write(f"**Quantidade de Externos:** {evento['Externos']}")
                st.write(f"**Quantidade de Funcionários:** {evento['Funcionários']}")

            with col2:
                if evento.get('Imagem'):
                    st.image(evento['Imagem'][0], use_column_width=True)

    st.markdown("---")

# Chamada da função principal
apresentando_eventos()



# Sidebar
with st.sidebar:
   st.image("Imagens/BannerASIN.png", use_container_width=True)
