import streamlit as st
from datetime import date
import streamlit as st
from datetime import date
from Banco_de_Dados.Eventos import *
from datetime import datetime

# """
# eventos = [
#     {"Cod_Evento": 1, "Nome": "Festa Junina", "Data": date(2021, 5, 4), "Observacao": "", "Quantidade_Externos": 40,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
#     {"Cod_Evento": 2, "Nome": "Natal Solidário", "Data": date(2021, 12, 20), "Observacao": "Distribuição de presentes", "Quantidade_Externos": 60,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
#     {"Cod_Evento": 3, "Nome": "Palestra Motivacional", "Data": date(2022, 3, 15), "Observacao": "Convidado especial", "Quantidade_Externos": 25,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
#     {"Cod_Evento": 4, "Nome": "Dia da Família", "Data": date(2022, 6, 10), "Observacao": "Atividades recreativas", "Quantidade_Externos": 50},
#     {"Cod_Evento": 5, "Nome": "Semana Cultural", "Data": date(2022, 9, 5), "Observacao": "Exposições e apresentações", "Quantidade_Externos": 80,"Imagem":["Imagens/Outras/competição de natação.jpeg"]},
#     {"Cod_Evento": 6, "Nome": "Workshop de Tecnologia", "Data": date(2023, 2, 18), "Observacao": "Demonstrações de IA", "Quantidade_Externos": 30,"Imagem":["Imagens/Outras/competição de natação.jpeg"]}
# ]
# """
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
    
    # Filtros
    col_input, col_button = st.columns([9, 1])
    with col_input:
        nome_evento = st.text_input("Digite o nome do evento:", st.session_state.get("nome_evento", ""))
    with col_button:
        st.markdown('<div class="spaced-button">', unsafe_allow_html=True)
        if st.button("Limpar", key="clear_button"):
            for key in ["nome_evento", "data_inicio", "data_fim"]:
                st.session_state.pop(key, None)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    #data_inicio_default = min(evento["Data"] for evento in eventos)
    #data_fim_default = max(evento["Data"] for evento in eventos)
    
    with col1:
        data_inicio = st.date_input("Data Inicial", st.session_state.get("data_inicio", date(2024, 1, 1)))
    with col2:
        data_fim = st.date_input("Data Final", st.session_state.get("data_fim", date.today()))
    
    # Atualizando session state
    st.session_state.update({
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "nome_evento": nome_evento
    })
    
    st.markdown("---")
    
    # Filtro dos eventos
    eventos_filtrados = [
        evento for evento in eventos
        if data_inicio <= datetime.strptime(evento["Data"], "%Y-%m-%d %H:%M:%S").date() <= data_fim and
        (nome_evento.lower() in evento["Nome"].lower() if nome_evento else True)
    ]
    
    if not eventos_filtrados:
        st.warning("Nenhum evento encontrado para os filtros aplicados.")
    
    for evento in eventos_filtrados:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(evento["Nome"])
                data_evento = datetime.strptime(evento["Data"], "%Y-%m-%d %H:%M:%S")
                st.write(f"**Data:** {data_evento.strftime('%d/%m/%Y')}")
                st.write(f"**Observação:** {evento['Observacoes'] if evento['Observacoes'] else 'Nenhuma'}")
                st.write(f"**Quantidade de Externos:** {evento['Quantidade_Externos']}")
            
            with col2:
                if evento.get('Imagem'):
                    st.image(evento['Imagem'][0], use_column_width=True)
    
    st.markdown("---")

# Chamando a função principal
apresentando_eventos()

# Sidebar
with st.sidebar:
   st.image("Imagens/BannerASIN.png", use_container_width=True)
