import streamlit as st
from datetime import datetime, date
from babel.dates import format_date
import os

# Dados fornecidos
dados = {
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
    'Presenças': [datetime(2021, 5, 4), datetime(2021, 5, 11), datetime(2021, 5, 18), datetime(2021, 5, 25)],
    'Contatos': [(31999999999, 'WhatsApp da mãe'), (12222222222, 'Telefone fixo do trabalho do pai')],
    'Oficinas': {'SEG - 09:00 ÁS 10:00': 'Informática', 
                 'QUA - 09:00 ÁS 10:00': 'Música'},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png',
              'Imagens/Outras/roxo.jpg', 
              'Imagens/Outras/Sem título.jpg'],
    'Eventos': [('Feira de Ciências', datetime(2021, 5, 4), 'Descrição da Feira de Ciências'),
                ('Festa Junina', datetime(2021, 6, 4), 'Descrição da Festa Junina')]
}

# Função para calcular idade
def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

# Função para formatar CPF e RG
def formatar_cpf(cpf):
    return f"{cpf:011d}"[:3] + '.' + f"{cpf:011d}"[3:6] + '.' + f"{cpf:011d}"[6:9] + '-' + f"{cpf:011d}"[9:]

def formatar_cep(cep):
    return f"{cep:08d}"[:5] + '-' + f"{cep:08d}"[5:]

def formatar_telefone(telefone):
    telefone = f"{telefone:011d}"
    return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

def endereco_por_cep(cep, dados):
    import requests
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        endereco = response.json()
        dados['Logradouro'] = endereco['logradouro']
        dados['Bairro'] = endereco['bairro']
        dados['Cidade'] = endereco['localidade']
        dados['Estado'] = endereco['uf']
    else:
        dados['Logradouro'] = 'Não encontrado'
        dados['Bairro'] = 'Não encontrado'
        dados['Cidade'] = 'Não encontrado'
        dados['Estado'] = 'Não encontrado'

if st.session_state.get('Editando') is None:
    st.session_state['Editando'] = False

# Início da interface com Streamlit
st.set_page_config(page_title="Detalhes do Atendido", layout="wide")
st.title("Perfil do Atendido")

# Header com nome e status
col1, col2 = st.columns([3, 1])
col1.header(dados['Nome'])
if st.session_state['Editando'] == False:
    status_emoji = "✅" if dados['Status'] else "❌"
    col2.markdown(f"### Status: {status_emoji}")
else:
    novos_dados = dados.copy()
    novos_dados['Status'] = col2.checkbox("**Status**",  value=novos_dados['Status'])


# Dados pessoais
st.subheader("Dados Pessoais")
col1, col2, col3, col4 = st.columns(4)
if st.session_state['Editando'] == False:
    col1.write(f"**Data de Nascimento:** {format_date(dados['Data de Nascimento'], 'dd/MM/yyyy', locale='pt_BR')} ({calcular_idade(dados['Data de Nascimento'])} anos)")
    col2.write(f"**RG:** {dados['RG']}")
    col3.write(f"**CPF:** {formatar_cpf(dados['CPF'])}")
    col4.write(f"**Convênio:** {dados['Convênio']}")
else:
    novos_dados['Data de Nascimento'] = col1.date_input("Data de Nascimento", value=dados['Data de Nascimento'], format="DD/MM/YYYY")
    novos_dados['RG'] = col2.text_input("RG", value=dados['RG'])
    novos_dados['CPF'] = int(col3.text_input("CPF", value=dados['CPF']))
    novos_dados['Convênio'] = col4.text_input("Convênio", value=dados['Convênio'])

# Endereço
endereco_por_cep(dados['CEP'], dados)
if st.session_state['Editando'] == False:
    col1, col2, col3 = st.columns(3)
    col1.write(f"**Logradouro:** {dados['Logradouro']}")
    col2.write(f"**CEP:** {formatar_cep(dados['CEP'])}")
    col3.write(f"**Número:** {dados['Número']}")
    col1.write(f"**Bairro:** {dados['Bairro']}")
    col2.write(f"**Cidade:** {dados['Cidade']}")
    col3.write(f"**Estado:** {dados['Estado']}")
else:
    col1, col2 = st.columns(2)
    novos_dados['CEP'] = int(col1.text_input("CEP", value=novos_dados['CEP']))
    novos_dados['Número'] = int(col2.text_input("Número", value=novos_dados['Número']))
    with st.expander("Endereço (Antigo / Novo)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Logradouro:** {dados['Logradouro']}")
            st.write(f"**Bairro:** {dados['Bairro']}")
            st.write(f"**Cidade:** {dados['Cidade']}")
            st.write(f"**Estado:** {dados['Estado']}")
        with col2:
            endereco_por_cep(novos_dados['CEP'], novos_dados)
            st.write(f"**Logradouro:** {novos_dados['Logradouro']}")
            st.write(f"**Bairro:** {novos_dados['Bairro']}")
            st.write(f"**Cidade:** {novos_dados['Cidade']}")
            st.write(f"**Estado:** {novos_dados['Estado']}")
 
col1, col2, col3 = st.columns(3)
if st.session_state['Editando'] == False:
    col1.write(f"**Pai:** {dados['Pai']}")
    col2.write(f"**Mãe:** {dados['Mãe']}")
    if dados['Responsável']: col3.write(f"**Responsável:** {dados['Responsável']}")
else:
    novos_dados['Pai'] = col1.text_input("Pai", value=dados['Pai'])
    novos_dados['Mãe'] = col2.text_input("Mãe", value=dados['Mãe'])
    novos_dados['Responsável'] = col3.text_input("Responsável", value=dados['Responsável'])

if st.session_state['Editando'] == False:
    if st.button("Editar Dados Pessoais"):
        st.session_state['Editando'] = True
        st.rerun()
elif st.button("Salvar Dados Pessoais"):
    st.session_state['Editando'] = False
    st.rerun()

# Contatos
st.subheader("Contatos")
cols = st.columns(3)
for idx, (telefone, descricao) in enumerate(dados['Contatos']):
    formatted_telefone = formatar_telefone(telefone)
    with cols[idx % 3].container(border=True):
        st.markdown(f"**{descricao}:**")
        st.write(formatted_telefone)

# Oficinas
st.subheader("Oficinas")
st.write("Aqui teremos a tabela de horários e oficinas")
for horario, oficina in dados['Oficinas'].items():
    st.write(f"- **{horario}**: {oficina}")

# Presenças
st.subheader("Presenças")
# Cria um intervalo de data entre o maximo e minimo
min_date = min(dados['Presenças'])
max_date = max(dados['Presenças'])
# Cria um intervalo de datas com slider
intervalo_datas = st.slider("Selecione o intervalo de datas", min_date, max_date, (min_date, max_date), format="DD/MM/YYYY")
# Imprime ordenado as datas que ele foi

st.write(f"Presenças no intervalo selecionado: {len([i for i in dados['Presenças'] if intervalo_datas[0] <= i <= intervalo_datas[1]])}")

with st.expander("Datas de presença"):
    for i in dados['Presenças']:
        if intervalo_datas[0] <= i <= intervalo_datas[1]:
            st.write(format_date(i, 'dd/MM/yyyy', locale='pt_BR'))

# Eventos
st.subheader("Eventos")
col1, col2 = st.columns(2)
for idx, (nome, data, descricao) in enumerate(dados['Eventos']):
    label = f"{nome} ({format_date(data, 'dd/MM/yyyy', locale='pt_BR')})"
    if idx % 2 == 0:
        with col1.expander(label):
            st.write(descricao)
    else:
        with col2.expander(label):
            st.write(descricao)

# Fotos
st.subheader("Fotos")
col1, col2, col3 = st.columns(3)
for idx, foto in enumerate(dados['Fotos']):
    if os.path.exists(foto):
        if idx % 3 == 0:
            col1.image(foto, use_column_width=True)
        elif idx % 3 == 1:
            col2.image(foto, use_column_width=True)
        else:
            col3.image(foto, use_column_width=True)
    else:
        st.error(f"Imagem não encontrada: {foto}")
