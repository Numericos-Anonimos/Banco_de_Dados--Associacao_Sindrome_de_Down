import streamlit as st
from datetime import datetime, date

# Configuração da página
st.set_page_config(page_title="Projetos", layout="wide")


# Dados simulados da tabela Projetos
dados_projetos = [
    {
        "Cod_Projetos": 1,
        "Nome": "Projeto A",
        "Verba": 1000.0,
        "Data_Inicio": "2023-01-01",
        "Data_Fim": "2023-06-30",
        "Descricao": "Projeto focado em A"
    },
    {
        "Cod_Projetos": 2,
        "Nome": "Projeto B",
        "Verba": 1500.0,
        "Data_Inicio": "2023-02-01",
        "Data_Fim": "2023-07-31",
        "Descricao": "Projeto focado em B"
    },
    {
        "Cod_Projetos": 3,
        "Nome": "Projeto C",
        "Verba": 2000.0,
        "Data_Inicio": "2023-03-01",
        "Data_Fim": None,
        "Descricao": "Projeto em andamento"
    },
    {
        "Cod_Projetos": 4,
        "Nome": "Projeto D",
        "Verba": 2500.0,
        "Data_Inicio": "2023-03-01",
        "Data_Fim": None,
        "Descricao": "Projeto em andamento"
    }
]

if "alterar_projeto" not in st.session_state:
    st.session_state["alterar_projeto"] = None
if "ver_projeto" not in st.session_state:
    st.session_state["ver_projeto"] = None

def ver_callback(cod):
    st.session_state["ver_projeto"] = cod

def alterar_callback(cod):
    st.session_state["alterar_projeto"] = cod

def listar_projetos(dados):
    st.title("Projetos")

    st.markdown("""
        <style>
            .card {
                border: 1px solid #00aeef;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0);
                background: #005f88;
            }
            .card h3 {
                margin-top: 0;
                color: #ffffff; /* Cor branca para o título */
            }
            .card p {
                margin: 5px 0;
                color: #ffffff; /* Cor branca para o texto */
            }
        </style>
    """, unsafe_allow_html=True)
    
    num_colunas = 3
    for i in range(0, len(dados), num_colunas):
        linha = dados[i:i+num_colunas]
        cols = st.columns(num_colunas)
        
        for j, projeto in enumerate(linha):
            with cols[j]:
                st.markdown(f"""
                <div class="card">
                    <h3>{projeto['Nome']}</h3>
                    <p><b>Código:</b> {projeto['Cod_Projetos']}</p>
                    <p><b>Verba:</b> R$ {projeto['Verba']:.2f}</p>
                    <p><b>Início:</b> {projeto['Data_Inicio']}</p>
                    <p><b>Fim:</b> {projeto['Data_Fim'] if projeto['Data_Fim'] else 'Em andamento'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button(
                        "Ver", 
                        key=f"ver_{projeto['Cod_Projetos']}",
                        on_click=ver_callback, 
                        args=(projeto['Cod_Projetos'],)
                    )
                with col2:
                    st.button(
                        "Alterar",
                        key=f"alterar_{projeto['Cod_Projetos']}",
                        on_click=alterar_callback,
                        args=(projeto['Cod_Projetos'],)
                    )

def ver_projeto(dados, cod):
    projeto = next(p for p in dados if p["Cod_Projetos"] == cod)
    st.markdown(f"<h1 style='font-size: 40px;'>{projeto['Nome']}</h1>", unsafe_allow_html=True)
    st.write(f"**Código:** {projeto['Cod_Projetos']}")
    st.write(f"**Verba:** R$ {projeto['Verba']}")
    st.write(f"**Data de Início:** {projeto['Data_Inicio']}")
    st.write(f"**Data de Fim:** {projeto['Data_Fim'] if projeto['Data_Fim'] else 'Em andamento'}")
    st.write(f"**Descrição:** {projeto['Descricao']}")
    if st.button("Voltar"):
        st.session_state["ver_projeto"] = None
        st.rerun()

def alterar_projeto(dados, cod):
    projeto = next(p for p in dados if p["Cod_Projetos"] == cod)
    st.header(f"Alterando dados de: {projeto['Nome']}")
    with st.form(key=f"alterar_{cod}"):
        nome = st.text_input("Nome", value=projeto["Nome"])
        verba = st.number_input("Verba", value=projeto["Verba"], step=100.0)
        data_inicio = st.date_input("Data de Início", datetime.strptime(projeto["Data_Inicio"], "%Y-%m-%d").date())
        data_fim = st.date_input("Data de Fim", datetime.strptime(projeto["Data_Fim"], "%Y-%m-%d").date()) if projeto["Data_Fim"] else st.date_input("Data de Fim", date.today())
        descricao = st.text_area("Descrição", value=projeto["Descricao"])
        
        if st.form_submit_button("Salvar"):
            projeto.update({
                "Nome": nome,
                "Verba": verba,
                "Data_Inicio": data_inicio.strftime("%Y-%m-%d"),
                "Data_Fim": data_fim.strftime("%Y-%m-%d") if data_fim else None,
                "Descricao": descricao
            })
            st.success("Alterações salvas!")
            st.session_state["alterar_projeto"] = None
            st.rerun()

if st.session_state["ver_projeto"]:
    ver_projeto(dados_projetos, st.session_state["ver_projeto"])
elif st.session_state["alterar_projeto"]:
    alterar_projeto(dados_projetos, st.session_state["alterar_projeto"])
else:
    listar_projetos(dados_projetos)

with st.sidebar:
    st.image("Imagens/BannerASIN.png", use_container_width=True)



