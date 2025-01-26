import streamlit as st
from datetime import datetime, date
from babel.dates import format_date
from collections import Counter
import os

# Dados fornecidos
dados = {
    'Nome': 'João Victor Assaoka Ribeiro',
    'Status': 'Ativo',
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

def calcular_presencas_por_mes(presencas):
    contagem = Counter(presenca.strftime('%m/%Y') for presenca in presencas)
    return sorted(contagem.items(), key=lambda x: datetime.strptime(x[0], '%m/%Y'))

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

# Início da interface com Streamlit
st.set_page_config(page_title="Detalhes do Usuário", layout="wide")
st.title("Perfil do Usuário")

# Header com nome e status
col1, col2 = st.columns([3, 1])
col1.header(dados['Nome'])
status_emoji = "✅" if dados['Status'] == "Ativo" else "❌"
col2.markdown(f"### Status: {status_emoji}")

# Dados pessoais
st.subheader("Dados Pessoais")
col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
col1.write(f"**Data de Nascimento:** {format_date(dados['Data de Nascimento'], 'dd/MM/yyyy', locale='pt_BR')} ({calcular_idade(dados['Data de Nascimento'])} anos)")
col2.write(f"**RG:** {dados['RG']}")
col3.write(f"**CPF:** {formatar_cpf(dados['CPF'])}")
col4.write(f"**Convênio:** {dados['Convênio']}")

col1, col2, col3 = st.columns(3)
endereco_por_cep(dados['CEP'], dados)
col1.write(f"**Logradouro:** {dados['Logradouro']}")
col2.write(f"**Número:** {dados['Número']}")
col3.write(f"**CEP:** {formatar_cep(dados['CEP'])}")
col1.write(f"**Bairro:** {dados['Bairro']}")
col2.write(f"**Cidade:** {dados['Cidade']}")
col3.write(f"**Estado:** {dados['Estado']}")

col1, col2, col3 = st.columns(3)
col1.write(f"**Pai:** {dados['Pai']}")
col2.write(f"**Mãe:** {dados['Mãe']}")
if dados['Responsável']: col3.write(f"**Responsável:** {dados['Responsável']}")

# Responsáveis

# Endereço
# Vamos pegar o cep pra pegar endereço, bairro, cidade e estado

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

# Botão para modo de edição
if st.button("Entrar no modo de edição"):
    with st.form("edit_form"):
        novo_nome = st.text_input("Nome", value=dados['Nome'])
        novo_status = st.selectbox("Status", ["Ativo", "Inativo"], index=0 if dados['Status'] == "Ativo" else 1)
        nova_data_nascimento = st.date_input("Data de Nascimento", value=dados['Data de Nascimento'].date())
        novo_rg = st.text_input("RG", value=str(dados['RG']))
        novo_cpf = st.text_input("CPF", value=formatar_cpf(dados['CPF']))
        novo_endereco = st.text_input("Endereço", value=dados['Endereço'])
        novo_cep = st.text_input("CEP", value=formatar_cep(dados['CEP']))

        st.form_submit_button("Salvar alterações")
