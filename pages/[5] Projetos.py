import streamlit as st
from datetime import datetime, date
from Banco_de_Dados.Projetos import *

# Configuração da página
#st.set_page_config(page_title="Projetos", layout="wide")

# Dados simulados da tabela Projetos
dados_projetos = listar_projetos()

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
                padding: 10px;
                margin: 10px 10px 10px 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                background: #005f88;
                text-align: center;
                width: 310px;
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

    
    def formatar_data(data_str):
        """ Formata uma string de data no formato 'YYYY-MM-DD HH:MM:SS' para 'DD/MM/YYYY'. """
        if data_str:
            return datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
        return "Em andamento"

    for i in range(0, len(dados), num_colunas):
        linha = dados[i:i + num_colunas]
        cols = st.columns(num_colunas)

        for j, projeto in enumerate(linha):
            with cols[j]:
                st.markdown(f"""
                <div class="card">
                    <h3>{projeto['Nome']}</h3>
                    <p><b>Código:</b> {projeto['Cod_Projeto']}</p>
                    <p><b>Verba:</b> R$ {projeto['Verba']:,.2f}</p>
                    <p><b>Início:</b> {formatar_data(projeto['Data_Inicio'])}</p>
                    <p><b>Fim:</b> {formatar_data(projeto['Data_Fim'])}</p>
                    <p><b>Descrição:</b> {projeto['Descricao']}</p>
                    <hr>
                </div>
                """, unsafe_allow_html=True)

# Controle de navegação
listar_projetos(dados_projetos)

# Sidebar
with st.sidebar:
    st.image("Imagens/BannerASIN.png", use_container_width=True)
