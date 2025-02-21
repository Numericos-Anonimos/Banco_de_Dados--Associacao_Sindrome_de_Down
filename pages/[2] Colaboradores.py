import streamlit as st
from datetime import date
from time import sleep
import textwrap
from Banco_de_Dados.Colaboradores import *
import pandas as pd
import uuid
from st_aggrid import AgGrid, GridOptionsBuilder
from datetime import datetime
from babel.dates import format_date 
import requests


st.session_state['current_page'] = "Home"

dados_funcionarios = listar_funcionarios()

def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

# Função para formatar CPF e RG
def formatar_cpf(cpf):
    return f"{cpf:011d}"[:3] + '.' + f"{cpf:011d}"[3:6] + '.' + f"{cpf:011d}"[6:9] + '-' + f"{cpf:011d}"[9:]

def formatar_cep(cep):
    return f"{cep:08d}"[:5] + '-' + f"{cep:08d}"[5:]

def formatar_telefone(telefone):
    telefone = "".join(filter(str.isdigit, telefone))  # Remove caracteres não numéricos
    telefone = telefone.zfill(11)  # Garante que tenha 11 dígitos, preenchendo com zeros à esquerda se necessário
    return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

def endereco_por_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        endereco = response.json()
        return endereco
    else:
        return {'logradouro': 'Não encontrado', 'bairro': 'Não encontrado', 'localidade': 'Não encontrado', 'uf': 'Não encontrado'}
    


def imprimir_colaborador(funcionario_selecionado):
        st.empty()
        nome_completo = funcionario_selecionado['Nome']
        primeiros_nomes = " ".join(nome_completo.split()[:2])  # Pega os dois primeiros nomes

        st.markdown(f"<h1 style='font-size: 60px;'>Perfil:  {primeiros_nomes}</h1>", unsafe_allow_html=True)

    
        # Exibindo os detalhes do funcionário
        col1_detalhes, col2_detalhes =st.columns(2)
        col1_detalhes.write(f"**Nome Completo:** {funcionario_selecionado['Nome']}")
        col2_detalhes.write(f"**CPF:** {funcionario_selecionado['CPF']}")

        #st.write(f"Endereço: {funcionario_selecionado['Endereço']}")
        if(funcionario_selecionado['Salario']):
            st.write(f"Salário: {funcionario_selecionado['Salario']}")
        else:
            st.write(f"Salário: não inserido")
        
        if(funcionario_selecionado['Observacoes']):
            st.write(f"Observações: {funcionario_selecionado['Observacoes']}")
        else:
            st.write(f"Observações: não inserido")

        # Endereço
        def formatar_cep(cep):
            """ Formata o CEP no padrão XXXXX-XXX """
            return f"{cep[:5]}-{cep[5:]}"

        endereco = endereco_por_cep(funcionario_selecionado['CEP'])
        
        
        col1, col2, col3 = st.columns(3)

        col1.write(f"**Logradouro:** {endereco.get('logradouro', 'Não informado')}")
        col2.write(f"**CEP:** {formatar_cep(funcionario_selecionado['CEP'])}")
        col3.write(f"**Número:** {funcionario_selecionado.get('Numero', 'Não informado')}")

        col1.write(f"**Bairro:** {endereco.get('bairro', 'Não informado')}")
        col2.write(f"**Cidade:** {endereco.get('localidade', 'Não informado')}")
        col3.write(f"**Estado:** {endereco.get('uf', 'Não informado')}")









        st.markdown("---")
        # Contatos
        funcionario_selecionado_contatos = funcionario_contatos(funcionario_selecionado["Cod_Funcionario"])
        cols = st.columns(3)

        contatos = funcionario_selecionado_contatos

        st.subheader("📞 **Contatos**")
        cols = st.columns(3)  # Criar colunas para organizar os contatos

        # Iterar sobre os contatos e exibir na interface
        for idx, contato in enumerate(contatos):
            if isinstance(contato, tuple) and len(contato) == 2:  # Verificar se o formato da tupla está correto
                telefone, descricao = contato
                formatted_telefone = formatar_telefone(telefone)  # Formatar o telefone corretamente
                
                with cols[idx % 3].container(border=True):
                    st.markdown(f"**{descricao}:**")
                    st.write(formatted_telefone)
                    
        st.markdown("---")  # Linha separadora para organização

        funcionario_selecionado_oficinas = funcionario_oficinas(funcionario_selecionado["Cod_Funcionario"])

        st.subheader("**Oficinas**")

        # Extrai os dias disponíveis dos horários
        dias_disponiveis = ["Todos"] + sorted(set(horario.split(" - ")[0] for horario in funcionario_selecionado_oficinas.keys()))

        # Caixa de seleção para escolher o dia
        dia_escolhido = st.selectbox("Escolha o dia da semana:", dias_disponiveis)

        # Exibe as oficinas filtradas
        for horario, oficina in funcionario_selecionado_oficinas.items():
            if dia_escolhido == "Todos" or horario.startswith(dia_escolhido):
                st.write(f"- **{horario}**: {oficina}")
        
        st.markdown("---")
        funcionario_selecionado_pontos = funcionario_ponto(funcionario_selecionado["Cod_Funcionario"])

        # Verifica se há registros antes de processar os dados
        if funcionario_selecionado_pontos:
            # Presenças
            pontos_formatados = [
                (datetime.strptime(data, "%Y-%m-%d"), entrada, saida)
                for data, entrada, saida in funcionario_selecionado_pontos
            ]

            # Encontrar a menor e maior data
            min_date = min(pontos_formatados, key=lambda x: x[0])[0]
            max_date = max(pontos_formatados, key=lambda x: x[0])[0]

            # Filtro de datas pelo usuário
            st.subheader("📊 **Filtro de Período**")
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input("Selecione a data inicial", min_date)
            with col2:
                data_fim = st.date_input("Selecione a data final", max_date)

            # Garantir que a data de fim seja posterior à de início
            if data_inicio > data_fim:
                st.warning("⚠️ A data inicial não pode ser maior que a data final.")
            else:
                # Converter as datas do usuário para datetime
                data_inicio = datetime.combine(data_inicio, datetime.min.time())
                data_fim = datetime.combine(data_fim, datetime.max.time())

                # Filtrar os pontos dentro do intervalo selecionado
                pontos_no_intervalo = [
                    (data, entrada, saida) for data, entrada, saida in pontos_formatados
                    if data_inicio <= data <= data_fim
                ]

                st.write(f"Pontos no intervalo selecionado: {len(pontos_no_intervalo)}")

                # Expansor para mostrar as datas no intervalo formatadas
                with st.expander("📅 **Datas de Presença**"):
                    for data, entrada, saida in pontos_no_intervalo:
                        st.write(f"📅 **{format_date(data, 'dd/MM/yyyy', locale='pt_BR')}** → 🕘 {entrada} - 🕛 {saida}")


        else:
            st.subheader("📊 **Pontos**")
            st.write("⚠️ Nenhum registro de ponto encontrado para este funcionário.")



def colaborador():
    st.title("Gestão de Funcionários")

    # Injetando CSS customizado para alterar a cor secundária de fundo do grid (tema Alpine)
    st.markdown(
        """
        <style>
        .ag-theme-alpine {
            --ag-secondary-background-color: #005f88;
        }
        .small-button button {
            width: 100px;  /* Tamanho menor */
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

    # Inicializa o estado da sessão
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = None
    if "nome_atendido" not in st.session_state:
        st.session_state.nome_atendido = ""
    if "grid_key" not in st.session_state:
        st.session_state.grid_key = str(uuid.uuid4())

    # Cria duas colunas para o campo de texto e o botão de limpar
    col_input, col_button = st.columns([9, 1])
    with col_input:
        nome_atendido = st.text_input(
            "Digite o nome do colaborador:",
            key=f"search_input_{st.session_state.grid_key}",
            value=st.session_state.nome_atendido
        )
    with col_button:
        st.markdown('<div class="spaced-button">', unsafe_allow_html=True)
        if st.button("Limpar", key="clear_button"):
            st.session_state.nome_atendido = ""             # Limpa o filtro
            st.session_state.grid_key = str(uuid.uuid4())     # Gera nova chave para reinicializar grid e input
            st.session_state.selected_user = None             # Remove o usuário selecionado
            st.rerun()                                        # Reexecuta o script
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtrando os dados conforme a pesquisa
    if nome_atendido:
        dados_filtrados = [item for item in dados_funcionarios if nome_atendido.lower() in item['Nome'].lower()]
    else:
        dados_filtrados = dados_funcionarios  # Exibe todos os dados quando não há pesquisa

    # Se o filtro não retornar nenhum resultado, exibe uma mensagem e encerra a função
    if not dados_filtrados:
        st.info("Nenhum atendido encontrado com este filtro.")
        return

    # Criando DataFrame e filtrando apenas os atributos necessários
    df = pd.DataFrame(dados_filtrados)
    df = df[["Cod_Funcionario","Nome", "CPF","Salario"]]
    df["Salario"] = df["Salario"].fillna("---")

    # Configurando o AgGrid para seleção única e para as colunas se expandirem
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, minColumnWidth=200, flex=1)
    gb.configure_selection('single', use_checkbox=False)
    gridOptions = gb.build()
    gridOptions["domLayout"] = "autoHeight"

    # Exibe o grid interativo usando a chave armazenada
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        use_container_width=True,
        height=500,       # Garante que o grid ocupe toda a largura disponível
        update_mode="SELECTION_CHANGED",
        fit_columns_on_grid_load=True,
        rowHeight=60,
        key=st.session_state.grid_key
    )

    # Recupera as linhas selecionadas
    selected_rows = grid_response.get('selected_rows', [])
    if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
        selected_row = selected_rows.iloc[0].to_dict()
        st.session_state.selected_user = selected_row['Cod_Funcionario']

    # Exibe as informações do usuário selecionado, se houver
    if st.session_state.selected_user is not None:
        selected_user_data = next((item for item in dados_funcionarios if item['Cod_Funcionario'] == st.session_state.selected_user), None)
        if selected_user_data:
            st.markdown("---")
            imprimir_colaborador(selected_user_data)

colaborador()

with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)