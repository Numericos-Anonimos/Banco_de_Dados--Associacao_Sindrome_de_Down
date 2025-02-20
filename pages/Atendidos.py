import streamlit as st
from datetime import datetime, date
from babel.dates import format_date
import pandas as pd
import os
import requests

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
}


]

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

# Função para procurar atendido
def Atendidos():

    if 'selected_atendido' in st.session_state:
        st.empty()
        atendido_selecionado = st.session_state.selected_atendido

        # Buscar o atendido na lista de dados com base no nome
        atendido_info = next((item for item in dados if item['Nome'] == atendido_selecionado), None)

        if atendido_info is None:
            st.error("Atendido não encontrado!")
            return

        # Início da interface com Streamlit
        st.title("**Perfil do Atendido**")

        # Header com nome e status
        col1, col2 = st.columns([2.5, 1])
        col1.header(atendido_selecionado)
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

        st.subheader("**Contatos**")
        cols = st.columns(3)
        for idx, (telefone, descricao) in enumerate(atendido_info['Contatos']):
            formatted_telefone = formatar_telefone(telefone)
            with cols[idx % 3].container(border=True):
                st.markdown(f"**{descricao}:**")
                st.write(formatted_telefone)

        # Oficinas
        st.subheader("**Oficinas**")
        for horario, oficina in atendido_info['Oficinas'].items():
            st.write(f"- **{horario}**: {oficina}")

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

        st.subheader("**Fotos**")
        if st.checkbox("Mostrar Fotos"):
            cols = st.columns(3)
            for idx, foto in enumerate(atendido_info['Fotos']):
                if os.path.exists(foto):
                    cols[idx % 3].image(foto, use_column_width=True)
                else:
                    st.error(f"Imagem não encontrada: {foto}")
        
        submit_button = st.button("Voltar")

        if submit_button:
            del st.session_state['selected_atendido']  # Limpar o estado de visualização para voltar à lista
            st.rerun()

    else:
        st.markdown(f"<h1 style='font-size: 40px;'>Procurar Atendido</h1>", unsafe_allow_html=True)
        nome_atendido = st.text_input("Digite o nome do atendido:")
        
        # Espaçamento (opcional)
        st.write("\n" * 5)  

        # Cabeçalho da tabela
        columns = st.columns([1, 3, 2, 1.5, 1.5, 1, 1.5])
        campos = ["**Nº**", "**Nome**", "**Data de Nascimento**", "**Status**", "**Convênio**", "**Ver**", "**Alterar**"]
        for col, campo_nome in zip(columns, campos):
            col.write(campo_nome)

        if nome_atendido:
            sugestões = [item['Nome'] for item in dados if nome_atendido.lower() in item['Nome'].lower()]
            
            if sugestões:
                for sugestao in sugestões:
                    if st.button(sugestao):
                        st.session_state.selected_atendido = sugestao
                        st.rerun()  # Atualiza imediatamente para a visualização detalhada
                        break
            else:
                st.error("Atendido não encontrado!")
        else:
            # Exibe todos os atendidos apenas se não houver pesquisa
            for item in dados:
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 2, 1.5, 1.5, 1, 1.5])
                
                col1.write(item['Cod'])
                col2.write(item["Nome"])
                col3.write(format_date(item["Data de Nascimento"], 'dd/MM/yyyy', locale='pt_BR'))
                col4.write("✅" if item["Status"] else "❌")
                col5.write(item["Convênio"])

                if col6.button("Ver", key=f"ver_{item['Cod']}"):
                    st.session_state.selected_atendido = item["Nome"]
                    st.rerun()
                
                if col7.button("Alterar", key=f"alt_{item['Cod']}"):
                    st.session_state.alterar_atendido = item["Cod"]
                    st.rerun()








# Chama a função principal
Atendidos()

with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)