import streamlit as st
from datetime import datetime, date
from babel.dates import format_date
import pandas as pd
import os
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
from timetable_canvas import timetable_canvas_generator

# Configuração da página deve ser a primeira linha no script
#st.set_page_config(page_title="Detalhes do Atendido", layout="wide")


def convert_to_timetable(dados, nome_pessoa):
    day_map = {
        "SEG": "Segunda",
        "TER": "Terça",
        "QUA": "Quarta",
        "QUI": "Quinta",
        "SEX": "Sexta"
    }
    
    time_slots = [
        '08:00', '09:00', '10:00', '11:00', '12:00',
        '13:00', '14:00', '15:00', '16:00', '17:00'
    ]
    
    timetable = [['' for _ in time_slots] for _ in day_map.values()]
    
    for pessoa in dados:
        if pessoa['Nome'] == nome_pessoa:
            oficinas = pessoa.get('Oficinas', {})
            
            for horario_key, nome_oficina in oficinas.items():
                try:
                    # Extrair dia e horários da chave
                    dia_part, tempo_part = horario_key.split(' - ')
                    inicio_str, fim_str = tempo_part.split(' ÁS ')
                    
                    # Converter para formatos padrão
                    dia = day_map[dia_part.strip().upper()]
                    idx_dia = list(day_map.values()).index(dia)
                    
                    # Encontrar índices dos horários
                    idx_inicio = time_slots.index(inicio_str.strip())
                    idx_fim = time_slots.index(fim_str.strip())
                    
                    # Preencher a grade
                    for slot in range(idx_inicio, idx_fim):
                        timetable[idx_dia][slot] = f"{nome_oficina} ({time_slots[slot]})"
                        
                except (KeyError, ValueError, AttributeError):
                    continue
                    
    return timetable

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
                try:
                    # Usando caminho absoluto para melhor controle
                    caminho_imagem = os.path.abspath(os.path.join("Imagens/Outras", os.path.basename(foto)))
                    
                    with cols[idx % 3]:
                        if os.path.exists(caminho_imagem):
                            st.image(caminho_imagem, use_column_width=True)
                        else:
                            st.warning(f"Arquivo não encontrado: {os.path.basename(foto)}")
                except Exception as e:
                    st.error(f"Erro ao carregar imagem: {str(e)}")
                    continue  # Continua para próxima imagem mesmo com erro

        # Garantindo que o timetable sempre será renderizado
        try:
            timetable = convert_to_timetable(dados, atendido_info['Nome'])
            updated_timetable = timetable_canvas_generator(
                timetable,
                timetableType=['08:00', '09:00', '10:00', '11:00', '12:00', 
                            '13:00', '14:00', '15:00', '16:00', '17:00'],
                Gheight=100
            )
            st.write(updated_timetable)
        except Exception as e:
            st.error("Erro ao gerar a grade horária:")
            st.exception(e)  # Mostra detalhes do erro sem quebrar o app



# Função para procurar atendido
import uuid

def Atendidos():
    st.title("📋 Procurar Atendidos")

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
            "Digite o nome do atendido:",
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
        dados_filtrados = [item for item in dados if nome_atendido.lower() in item['Nome'].lower()]
    else:
        dados_filtrados = dados  # Exibe todos os dados quando não há pesquisa

    # Se o filtro não retornar nenhum resultado, exibe uma mensagem e encerra a função
    if not dados_filtrados:
        st.info("Nenhum atendido encontrado com este filtro.")
        return

    # Criando DataFrame e filtrando apenas os atributos necessários
    df = pd.DataFrame(dados_filtrados)
    df = df[["Cod", "Nome", "CPF", "Data de Nascimento", "Status", "Convênio"]]
    df["Data de Nascimento"] = pd.to_datetime(df["Data de Nascimento"]).dt.strftime('%d/%m/%Y')

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

    st.markdown("---")
    # Recupera as linhas selecionadas
    selected_rows = grid_response.get('selected_rows', [])
    if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
        selected_row = selected_rows.iloc[0].to_dict()
        st.session_state.selected_user = selected_row['Cod']

    # Exibe as informações do usuário selecionado, se houver
    if st.session_state.selected_user is not None:
        selected_user_data = next((item for item in dados if item['Cod'] == st.session_state.selected_user), None)
        if selected_user_data:
            imprime_colaborador(selected_user_data)














# Chama a função principal
Atendidos()

with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)