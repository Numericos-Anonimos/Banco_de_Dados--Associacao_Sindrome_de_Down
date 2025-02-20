import streamlit as st
from datetime import datetime, date
from babel.dates import format_date
import pandas as pd
import os
import requests
from st_aggrid import AgGrid, GridOptionsBuilder

# Configuração da página deve ser a primeira linha no script
st.set_page_config(page_title="Detalhes do Atendido", layout="wide")

# Dados de exemplo
dados = [{
    "Cod": 1,
    'Nome': 'João Victor Assaoka Ribeiro',
    'Status': True,
    'Data de Nascimento': datetime(2005, 5, 4),
    'RG': '98680418X',
    'CPF': 31997000405,
    'Convênio': 'Unimed',
    'Pai': 'José',
    'Mãe': 'Maria',
    'Responsável': None,
    'CEP': 12221580,
    'Número': 123,
    'Observações': None,
    'Presenças': [date(2021, 5, 4), date(2021, 5, 11), date(2021, 5, 18), date(2021, 5, 25)],
    'Contatos': [(31999999999, 'WhatsApp da mãe'), (12222222222, 'Telefone fixo do trabalho do pai')],
    'Oficinas': {'SEG - 09:00 ÁS 10:00': 'Informática', 
                 'QUA - 09:00 ÁS 10:00': 'Música'},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png',
              'Imagens/Outras/roxo.jpg', 
              'Imagens/Outras/Sem título.jpg'],
    'Eventos': [('Feira de Ciências', date(2021, 5, 4), 'Descrição da Feira de Ciências'),
                ('Festa Junina', date(2021, 6, 4), 'Descrição da Festa Junina')]
},
    {
    "Cod": 2,
    'Nome': 'João Ferreira da Silva Pereira',
    'Status': True,
    'Data de Nascimento': datetime(2005, 5, 4),
    'RG': '98680418X',
    'CPF': 31997000405,
    'Convênio': 'Unimed',
    'Pai': 'José',
    'Mãe': 'Maria',
    'Responsável': None,
    'CEP': 12221580,
    'Número': 123,
    'Observações': None,
    'Presenças': [date(2021, 5, 4), date(2021, 5, 11), date(2021, 5, 18), date(2021, 5, 25)],
    'Contatos': [(31999999999, 'WhatsApp da mãe'), (12222222222, 'Telefone fixo do trabalho do pai')],
    'Oficinas': {'SEG - 09:00 ÁS 10:00': 'Informática', 
                 'QUA - 09:00 ÁS 10:00': 'Música'},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png',
              'Imagens/Outras/roxo.jpg', 
              'Imagens/Outras/Sem título.jpg'],
    'Eventos': [('Feira de Ciências', date(2021, 5, 4), 'Descrição da Feira de Ciências'),
                ('Festa Junina', date(2021, 6, 4), 'Descrição da Festa Junina')]
},
{
    "Cod": 3,
    'Nome': 'Thomas Pires Correia',
    'Status': True,
    'Data de Nascimento': datetime(2005, 5, 4),
    'RG': '98680418X',
    'CPF': 31997000405,
    'Convênio': 'Unimed',
    'Pai': 'José',
    'Mãe': 'Maria',
    'Responsável': None,
    'CEP': 12221580,
    'Número': 123,
    'Observações': None,
    'Presenças': [date(2021, 5, 4), date(2021, 5, 11), date(2021, 5, 18), date(2021, 5, 25)],
    'Contatos': [(31999999999, 'WhatsApp da mãe'), (12222222222, 'Telefone fixo do trabalho do pai')],
    'Oficinas': {'SEG - 09:00 ÁS 10:00': 'Informática', 
                 'QUA - 09:00 ÁS 10:00': 'Música'},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png',
              'Imagens/Outras/roxo.jpg', 
              'Imagens/Outras/Sem título.jpg'],
    'Eventos': [('Feira de Ciências', date(2021, 5, 4), 'Descrição da Feira de Ciências'),
                ('Festa Junina', date(2021, 6, 4), 'Descrição da Festa Junina')]
},
{
    "Cod": 4,
    'Nome': 'Matheus Kaua',
    'Status': False,
    'Data de Nascimento': datetime(2005, 5, 4),
    'RG': '98680418X',
    'CPF': 31997000405,
    'Convênio': 'Unimed',
    'Pai': 'José',
    'Mãe': 'Maria',
    'Responsável': None,
    'CEP': 12221580,
    'Número': 123,
    'Observações': None,
    'Presenças': [date(2021, 5, 4), date(2021, 5, 11), date(2021, 5, 18), date(2021, 5, 25)],
    'Contatos': [(31999999999, 'WhatsApp da mãe'), (12222222222, 'Telefone fixo do trabalho do pai')],
    'Oficinas': {'SEG - 09:00 ÁS 10:00': 'Informática', 
                 'QUA - 09:00 ÁS 10:00': 'Música'},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png',
              'Imagens/Outras/roxo.jpg', 
              'Imagens/Outras/Sem título.jpg'],
    'Eventos': [('Feira de Ciências', date(2021, 5, 4), 'Descrição da Feira de Ciências'),
                ('Festa Junina', date(2021, 6, 4), 'Descrição da Festa Junina')]
},
{
    "Cod": 5,
    'Nome': 'Reginaldo da Silva',
    'Status': True,
    'Data de Nascimento': datetime(2005, 5, 4),
    'RG': '98680418X',
    'CPF': 31997000405,
    'Convênio': 'Unimed',
    'Pai': 'José',
    'Mãe': 'Maria',
    'Responsável': None,
    'CEP': 12221580,
    'Número': 123,
    'Observações': None,
    'Presenças': [date(2021, 5, 4), date(2021, 5, 11), date(2021, 5, 18), date(2021, 5, 25)],
    'Contatos': [(31999999999, 'WhatsApp da mãe'), (12222222222, 'Telefone fixo do trabalho do pai')],
    'Oficinas': {'SEG - 09:00 ÁS 10:00': 'Informática', 
                 'QUA - 09:00 ÁS 10:00': 'Música'},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png',
              'Imagens/Outras/roxo.jpg', 
              'Imagens/Outras/Sem título.jpg'],
    'Eventos': [('Feira de Ciências', date(2021, 5, 4), 'Descrição da Feira de Ciências'),
                ('Festa Junina', date(2021, 6, 4), 'Descrição da Festa Junina')]
},
{
    "Cod": 6,
    'Nome': 'Carlos Rodrigues da Silva Carvalho',
    'Status': False,
    'Data de Nascimento': datetime(2005, 5, 4),
    'RG': '98680418X',
    'CPF': 31997000405,
    'Convênio': 'Unimed',
    'Pai': 'José',
    'Mãe': 'Maria',
    'Responsável': None,
    'CEP': 12221580,
    'Número': 123,
    'Observações': None,
    'Presenças': [date(2021, 5, 4), date(2021, 5, 11), date(2021, 5, 18), date(2021, 5, 25)],
    'Contatos': [(31999999999, 'WhatsApp da mãe'), (12222222222, 'Telefone fixo do trabalho do pai')],
    'Oficinas': {'SEG - 09:00 ÁS 10:00': 'Informática', 
                 'QUA - 09:00 ÁS 10:00': 'Música'},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png',
              'Imagens/Outras/roxo.jpg', 
              'Imagens/Outras/Sem título.jpg'],
    'Eventos': [('Feira de Ciências', date(2021, 5, 4), 'Descrição da Feira de Ciências'),
                ('Festa Junina', date(2021, 6, 4), 'Descrição da Festa Junina')]
}


]


def format_status(status):
    return "✅" if status else "❌"

def format_data(data):
    return data.strftime('%d/%m/%Y') if isinstance(data, (datetime, date)) else data

def format_list(lista):
    return ", ".join([format_data(item) for item in lista]) if isinstance(lista, list) else lista

def format_dict(dicionario):
    return "; ".join([f"{key}: {value}" for key, value in dicionario.items()]) if isinstance(dicionario, dict) else dicionario

def format_contatos(contatos):
    return "; ".join([f"{tel} ({desc})" for tel, desc in contatos]) if isinstance(contatos, list) else contatos

def format_eventos(eventos):
    return "; ".join([f"{nome} ({format_data(data)}): {desc}" for nome, data, desc in eventos]) if isinstance(eventos, list) else eventos











# Função para calcular idade
def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

# Função para formatar CPF
def formatar_cpf(cpf):
    return f"{cpf:011d}"[:3] + '.' + f"{cpf:011d}"[3:6] + '.' + f"{cpf:011d}"[6:9] + '-' + f"{cpf:011d}"[9:]  

def formatar_cep(cep):
    return f"{cep:08d}"[:5] + '-' + f"{cep:08d}"[5:]

# Função para formatar telefone
def formatar_telefone(telefone):
    telefone = f"{telefone:011d}"
    return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"


# Função para buscar endereço por CEP
def endereco_por_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        endereco = response.json()
        return endereco
    else:
        return {'logradouro': 'Não encontrado', 'bairro': 'Não encontrado', 'localidade': 'Não encontrado', 'uf': 'Não encontrado'}

def imprime_colaborador(atendido_info):
        # Header com nome e status
        col1, col2 = st.columns([2.5, 1])
        col1.title(atendido_info['Nome'])
        status_emoji = "✅" if atendido_info['Status'] else "❌"
        col2.header(f"Status: {status_emoji}")

        # Dados pessoais
        st.subheader("**Dados Pessoais**")
        col1, col2, col3, col4 = st.columns(4)
        col1.write(f"**Data de Nascimento:** {format_date(atendido_info['Data de Nascimento'], 'dd/MM/yyyy', locale='pt_BR')} ({calcular_idade(atendido_info['Data de Nascimento'])} anos)")
        col2.write(f"**RG:** {atendido_info['RG']}")
        col3.write(f"**CPF:** {formatar_cpf(atendido_info['CPF'])}")
        col4.write(f"**Convênio:** {atendido_info['Convênio']}")

        # Endereço
        endereco = endereco_por_cep(atendido_info['CEP'])
        col1, col2, col3 = st.columns(3)
        col1.write(f"**Logradouro:** {endereco['logradouro']}")
        col2.write(f"**CEP:** {formatar_cep(atendido_info['CEP'])}")
        col3.write(f"**Número:** {atendido_info['Número']}")
        col1.write(f"**Bairro:** {endereco['bairro']}")
        col2.write(f"**Cidade:** {endereco['localidade']}")
        col3.write(f"**Estado:** {endereco['uf']}")

        st.markdown("---")
        st.subheader("**Contatos**")
        cols = st.columns(3)
        for idx, (telefone, descricao) in enumerate(atendido_info['Contatos']):
            formatted_telefone = formatar_telefone(telefone)
            with cols[idx % 3].container(border=True):
                st.markdown(f"**{descricao}:**")
                st.write(formatted_telefone)

        st.markdown("---")

        # Oficinas
        st.subheader("**Oficinas**")
        for horario, oficina in atendido_info['Oficinas'].items():
            st.write(f"- **{horario}**: {oficina}")
            
        st.markdown("---")
        # Presenças
        st.subheader("**Presenças**")
        min_date, max_date = min(atendido_info['Presenças']), max(atendido_info['Presenças'])

        cols = st.columns(2)
        intervalo_datas = [cols[0].date_input("Data Inicial", min_date, min_value=min_date, max_value=max_date, format="DD/MM/YYYY")]
        intervalo_datas.append(cols[1].date_input("Data Final", max_date, min_value=intervalo_datas[0], max_value=max_date, format="DD/MM/YYYY"))

        st.write(f"Presenças no intervalo selecionado: {len([i for i in atendido_info['Presenças'] if intervalo_datas[0] <= i <= intervalo_datas[1]])}")

        with st.expander("Datas de presença"):
            for i in atendido_info['Presenças']:
                if intervalo_datas[0] <= i <= intervalo_datas[1]:
                    st.write(format_date(i, 'dd/MM/yyyy', locale='pt_BR'))

        st.markdown("---")

        # Eventos
        st.subheader("**Eventos**")
        col1, col2 = st.columns(2)
        for idx, (nome, data, descricao) in enumerate(atendido_info['Eventos']):
            label = f"{nome} ({format_date(data, 'dd/MM/yyyy', locale='pt_BR')})"
            if idx % 2 == 0:
                with col1.expander(label):
                    st.write(descricao)
            else:
                with col2.expander(label):
                    st.write(descricao)
                    
        st.markdown("---")

        st.subheader("**Fotos**")
        if st.checkbox("Mostrar Fotos"):
            cols = st.columns(3)
            for idx, foto in enumerate(atendido_info['Fotos']):
                if os.path.exists(foto):
                    cols[idx % 3].image(foto, use_column_width=True)
                else:
                    st.error(f"Imagem não encontrada: {foto}")



# Função para procurar atendido
def Atendidos():
        st.title("📋 Procurar Atendidos")

        # Injetando CSS customizado para alterar a cor secundária de fundo do grid (tema Alpine)
        st.markdown(
            """
            <style>
            .ag-theme-alpine {
                --ag-secondary-background-color: #005f88;
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

        # Campo de texto para busca
        nome_atendido = st.text_input("Digite o nome do atendido:", key="search_input", value=st.session_state.nome_atendido)
        st.markdown("<br>", unsafe_allow_html=True)

        # Filtrando os dados conforme a pesquisa
        if nome_atendido:
            dados_filtrados = [item for item in dados if nome_atendido.lower() in item['Nome'].lower()]
        else:
            dados_filtrados = dados  # Exibe todos os dados quando não há pesquisa

        # Criando DataFrame e filtrando apenas os atributos necessários
        df = pd.DataFrame(dados_filtrados)[["Cod", "Nome", "CPF","Data de Nascimento", "Status", "Convênio"]]
        df["Data de Nascimento"] = pd.to_datetime(df["Data de Nascimento"]).dt.strftime('%d/%m/%Y')

        # Configurando o AgGrid para seleção única e para as colunas se expandirem
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(resizable=True, minColumnWidth=200, flex=1)
        gb.configure_selection('single', use_checkbox=False)
        gridOptions = gb.build()

        # Define o layout do grid para autoHeight, para que ele se ajuste ao conteúdo
        gridOptions["domLayout"] = "autoHeight"

        # Exibe o grid interativo
        grid_response = AgGrid(
            df,
            gridOptions=gridOptions,
            use_container_width=True,
            height=500,       # Garante que o grid ocupe toda a largura disponível
            update_mode="SELECTION_CHANGED",
            fit_columns_on_grid_load=True,  # Ajusta as colunas para preencher o grid
            rowHeight=60
        )



        if st.button('Limpar Tabela e Campo de Texto'):
            # Limpa os dados filtrados e o campo de texto
            dados_filtrados = []
            st.session_state.nome_atendido = ""  # Limpa o campo de texto
            st.rerun()   # Isso reinicia a execução do script e limpa a tabela
        
        st.markdown("---")
        # Recupera as linhas selecionadas
        selected_rows = grid_response.get('selected_rows', [])

        # Se o retorno for um DataFrame, converte a primeira linha para dicionário
        if isinstance(selected_rows, pd.DataFrame):
            if not selected_rows.empty:
                selected_row = selected_rows.iloc[0].to_dict()
                st.session_state.selected_user = selected_row['Cod']
                
                # Filtra os dados para encontrar a linha com o 'Cod' selecionado
                selected_user_data = next((item for item in dados if item['Cod'] == selected_row['Cod']), None)
                
                # Imprime as informações do usuário selecionado
                if selected_user_data:
                    imprime_colaborador(selected_user_data)
        











# Chama a função principal
Atendidos()

with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)