import streamlit as st
from datetime import datetime, date

# Configuração da página
st.set_page_config(page_title="Projetos", layout="wide")
st.title("Projetos")

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
    }
]

# Inicializa as variáveis de sessão para controlar o fluxo
if "alterar_projeto" not in st.session_state:
    st.session_state["alterar_projeto"] = None
if "ver_projeto" not in st.session_state:
    st.session_state["ver_projeto"] = None

# Funções de callback para os botões
def ver_callback(cod):
    st.session_state["ver_projeto"] = cod

def alterar_callback(cod):
    st.session_state["alterar_projeto"] = cod

def listar_projetos(dados):
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Cabeçalho da tabela
    colunas = st.columns([1, 3, 2, 2, 3, 1, 1])
    campos = ["Nº", "Nome", "Verba", "Data Início", "Data Fim", "Ver", "Alterar"]
    for col, campo in zip(colunas, campos):
        col.write(campo)
    
    # Exibição dos projetos na tabela
    for item in dados:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 2, 3, 1, 1])
        col1.write(item["Cod_Projetos"])
        col2.write(item["Nome"])
        col3.write(f"R$ {item['Verba']}")
        col4.write(item["Data_Inicio"])
        col5.write(item["Data_Fim"] if item["Data_Fim"] else "Em andamento")
        
        # Usando callbacks para atualizar o estado imediatamente
        col6.button("Ver", key="ver"+str(item["Cod_Projetos"]),
                    on_click=ver_callback, args=(item["Cod_Projetos"],))
        col7.button("Alterar", key="alterar"+str(item["Cod_Projetos"]),
                    on_click=alterar_callback, args=(item["Cod_Projetos"],))

def ver_projeto(dados, cod):
    projeto_selecionado = next(item for item in dados if item["Cod_Projetos"] == cod)
    st.markdown(f"<h1 style='font-size: 40px;'>{projeto_selecionado['Nome']}</h1>", unsafe_allow_html=True)
    st.write(f"**Código:** {projeto_selecionado['Cod_Projetos']}")
    st.write(f"**Verba:** R$ {projeto_selecionado['Verba']}")
    st.write(f"**Data de Início:** {projeto_selecionado['Data_Inicio']}")
    st.write(f"**Data de Fim:** {projeto_selecionado['Data_Fim'] if projeto_selecionado['Data_Fim'] else 'Em andamento'}")
    st.write(f"**Descrição:** {projeto_selecionado['Descricao']}")
    if st.button("Voltar"):
        st.session_state["ver_projeto"] = None

def alterar_projeto(dados, cod):
    projeto_selecionado = next(item for item in dados if item["Cod_Projetos"] == cod)
    st.header(f"Alterando dados de: {projeto_selecionado['Nome']}")
    with st.form(key=f"alterar_{projeto_selecionado['Cod_Projetos']}"):
        nome = st.text_input("Nome", value=projeto_selecionado["Nome"])
        verba = st.number_input("Verba", value=projeto_selecionado["Verba"], step=100.0)
        data_inicio = st.date_input("Data de Início", datetime.strptime(projeto_selecionado["Data_Inicio"], "%Y-%m-%d").date())
        if projeto_selecionado["Data_Fim"]:
            data_fim = st.date_input("Data de Fim", datetime.strptime(projeto_selecionado["Data_Fim"], "%Y-%m-%d").date())
        else:
            data_fim = st.date_input("Data de Fim", date.today())
        descricao = st.text_area("Descrição", value=projeto_selecionado["Descricao"])
        
        submit_button = st.form_submit_button(label="Salvar Alterações")
        if submit_button:
            projeto_selecionado["Nome"] = nome
            projeto_selecionado["Verba"] = verba
            projeto_selecionado["Data_Inicio"] = data_inicio.strftime("%Y-%m-%d")
            projeto_selecionado["Data_Fim"] = data_fim.strftime("%Y-%m-%d")
            projeto_selecionado["Descricao"] = descricao
            st.success(f"Alterações salvas para {nome}!")
            st.session_state["alterar_projeto"] = None

# Fluxo da aplicação
if st.session_state["ver_projeto"] is not None:
    ver_projeto(dados_projetos, st.session_state["ver_projeto"])
elif st.session_state["alterar_projeto"] is not None:
    alterar_projeto(dados_projetos, st.session_state["alterar_projeto"])
else:
    listar_projetos(dados_projetos)

with st.sidebar:
    st.image("Imagens/BannerASIN.png", use_container_width=True)
