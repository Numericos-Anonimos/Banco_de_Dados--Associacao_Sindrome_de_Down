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


def listar_projetos(dados):
    st.title("Projetos da Associação")

    # Filtro de status do projeto
    status_filtro = st.selectbox("Status do projeto", ["Todos", "Em andamento", "Finalizados"])

    st.markdown("---")
    # Aplicando filtro
    if status_filtro == "Em andamento":
        dados = [p for p in dados if not p["Data_Fim"]]
    elif status_filtro == "Finalizados":
        dados = [p for p in dados if p["Data_Fim"]]

    st.markdown("""
        <style>
            .card {
                border: 1px solid #00aeef;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0 10px 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                background: #005f88;
                text-align: center;
                width: 280px;
            }
            .card h3, .card p {
                color: #ffffff;
            }
            .button-container {
                display: flex;
                justify-content: center;
                margin-top: 10px;
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
                    <hr>
                </div>
                """, unsafe_allow_html=True)

# Controle de navegação
listar_projetos(dados_projetos)

# Sidebar
with st.sidebar:
    st.image("Imagens/BannerASIN.png", use_container_width=True)
