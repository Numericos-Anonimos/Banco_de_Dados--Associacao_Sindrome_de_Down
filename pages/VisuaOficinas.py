import streamlit as st
import pandas as pd
from datetime import datetime, time, date
import os


st.set_page_config(page_title="VisuaOficinas", layout="wide")


if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

def sub_hora(ini:time, fim:time):
    return (fim.hour - ini.hour) * 60 + (fim.minute - ini.minute)

dados = {
    'Cod_Oficina': 1,
    'Nome': "Informática",
    'Categoria': "Tecnologia",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Informática",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png', 'Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
}


st.title("Oficinas")

if not st.session_state['edit_mode']:
    cols = st.columns([2.5,1])
    cols[0].header(f'{dados["Nome"]}')
    cols[1].header(f'Status: {"✅" if dados["Data_Fim"] is None else "❌"}')
else:
    novos_dados = dados.copy()
    novos_dados["Nome"] = st.text_input("Nome", value=dados["Nome"])


if not st.session_state['edit_mode']:
    cols = st.columns(3)
    cols[0].write(f'**Categoria**: {dados["Categoria"]}')
    cols[1].write(f'**Projeto**: {dados["Projeto"]}')
    cols[2].write(f'**Data de Cadastro**: {dados["Data_Cadastro"].strftime("%d/%m/%Y")}{"" if dados["Data_Fim"] is None else f" - {dados['Data_Fim'].strftime('%d/%m/%Y')}" }')
else:
    cols = st.columns([3, 1, 1])
    cols[0].write(f'**Categoria**: {dados["Categoria"]}')
    cols[0].write(f'**Projeto**: {dados["Projeto"]}')
    cols[1].write(f'**Data de Cadastro**: {dados["Data_Cadastro"].strftime("%d/%m/%Y")}')
    novos_dados["Data_Fim"] = cols[2].date_input("Data de Encerramento", value=dados["Data_Fim"], min_value=dados["Data_Cadastro"], max_value=date(2100, 12, 31), format="DD/MM/YYYY")

if not st.session_state['edit_mode']:
    cols = st.columns(3)        
    cols[0].write(f'**Dia da Semana**: {dados["Dia_Semana"]}')
    cols[1].write(f'**Horário**: {dados["Horario_Inicio"].strftime("%H:%M")} às {dados["Horario_Fim"].strftime("%H:%M")} ({sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"])} minutos)')
    cols[2].write(f'**Usuários**: {len(dados["Participantes"])} / {dados["Max_Participantes"]}')
else:
    cols = st.columns([2, 1])
    cols[0].write(f'**Dia da Semana**: {dados["Dia_Semana"]}')
    cols[0].write(f'**Horário**: {dados["Horario_Inicio"].strftime("%H:%M")} às {dados["Horario_Fim"].strftime("%H:%M")} ({sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"])} minutos)')
    novos_dados["Max_Participantes"] = cols[1].number_input("Máximo de Participantes", value=dados["Max_Participantes"], min_value=1, max_value=100)


if not st.session_state['edit_mode']:
    cols = st.columns(3)
    cols[0].write(f'**Oficineiro**: {dados["Oficineiro"]}')
    cols[1].write(f'**Valor por Hora**: R$ {dados["Valor_Hora"]:.2f}')
    cols[2].write(f'**Total**: R$ {len(dados["Houve_Oficina"]) * sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"]) * dados["Valor_Hora"]/60:.2f}')
    st.write(f'**Descrição**: {dados["Descricao"]}')
else:
    cols = st.columns([2, 1])
    cols[0].write(f'**Oficineiro**: {dados["Oficineiro"]}')
    novos_dados["Valor_Hora"] = cols[1].number_input("Valor por Hora", value=dados["Valor_Hora"], min_value=0.01, format="%.2f", step=1.0)
    cols[0].write(f'**Total**: R$ {len(dados["Houve_Oficina"]) * sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"]) * novos_dados["Valor_Hora"]/60:.2f}')
    novos_dados["Descricao"] = st.text_area("Descrição", value=dados["Descricao"])

if st.session_state['edit_mode']:
    cols = st.columns(2)
    if cols[0].button("Salvar", use_container_width=True):
        dados = novos_dados
        st.session_state.edit_mode = False
        st.rerun()
    if cols[1].button("Cancelar", use_container_width=True):
        st.session_state.edit_mode = False
        st.rerun()
    st.info("Modo de edição ativado. Altere os campos e clique em 'Salvar alterações'.")
else:
    if st.button("Editar"):
        st.session_state.edit_mode = True
        st.rerun()
        

st.header("Presenças")
min_date, max_date = min(dados['Houve_Oficina']), max(dados['Houve_Oficina'])
cols = st.columns(2)

selected_dates = [cols[0].date_input("Data Inicial", min_date, min_value=min_date, max_value=max_date, format="DD/MM/YYYY")]
selected_dates.append(cols[1].date_input("Data Final", max_date, min_value=selected_dates[0], max_value=max_date, format="DD/MM/YYYY"))

show_all_dates = st.checkbox("Mostrar todas as datas")

# Criando lista de datas conforme opção do usuário
if show_all_dates:
    all_dates = pd.date_range(selected_dates[0], selected_dates[1])
    date_list = [d.date() for d in all_dates]
else:
    date_list = [d for d in dados['Houve_Oficina'] if selected_dates[0] <= d <= selected_dates[1]]

date_strings = [d.strftime("%d/%m/%Y") for d in date_list]

# Criando DataFrame com presenças
df = pd.DataFrame(index=dados['Participantes'].keys(), columns=date_strings, dtype=str)

for participante, presencas in dados['Participantes'].items():
    for data in date_list:
        data_str = data.strftime("%d/%m/%Y")
        if data in presencas:
            df.loc[participante, data_str] = "✅"
        elif data in dados['Houve_Oficina']:
            df.loc[participante, data_str] = "❌"
        else:
            df.loc[participante, data_str] = "⬜"

st.dataframe(df, use_container_width=True)

st.subheader("Fotos")
if st.checkbox("Mostrar Fotos"):
    cols = st.columns(3)
    for idx, foto in enumerate(dados['Fotos']):
        if os.path.exists(foto):
            cols[idx % 3].image(foto, use_column_width=True)
        else:
            st.error(f"Imagem não encontrada: {foto}")


























oficinas = [{
    'Cod_Oficina': 1,
    'Nome': "Informática",
    'Categoria': "Tecnologia",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Informática",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png', 'Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
    },
    {
    'Cod_Oficina': 2,
    'Nome': "Informática",
    'Categoria': "Esporte",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Futebol",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
    },
    {
    'Cod_Oficina': 3,
    'Nome': "Informática",
    'Categoria': "Esporte",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Futebol",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png']
    },
    {
    'Cod_Oficina': 4,
    'Nome': "Arte",
    'Categoria': "Esporte",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Futebol",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/Sem título.jpg']
    }
]

def Apresentando_Oficinas():



    if st.session_state.get('categoria_selecionada') == 'Informática':
        # Filtro para encontrar oficinas com o nome "Informática"
        oficinas_informatica = [oficina for oficina in oficinas if oficina["Nome"] == "Informática"]
        
        if oficinas_informatica:
            for oficina in oficinas_informatica:
                st.write(f"Nome: {oficina['Nome']}")
                st.write(f"Categoria: {oficina['Categoria']}")
                st.write(f"Descrição: {oficina['Descricao']}")
                st.write(f"Oficineiro: {oficina['Oficineiro']}")
                st.write("----------")
        else:
            st.success(f"Não existe nenhum horário da categoria selecionada: {st.session_state.get('categoria_selecionada')}")

        if st.button("Voltar"):
            st.session_state['categoria_selecionada'] = None
            st.empty()
            st.rerun()
    elif st.session_state.get('categoria_selecionada') == 'Arte':

        # Filtro para encontrar oficinas com o nome "Informática"
        oficinas_informatica = [oficina for oficina in oficinas if oficina["Nome"] == "Arte"]
        
        if oficinas_informatica:
            for oficina in oficinas_informatica:
                st.write(f"Nome: {oficina['Nome']}")
                st.write(f"Categoria: {oficina['Categoria']}")
                st.write(f"Descrição: {oficina['Descricao']}")
                st.write(f"Oficineiro: {oficina['Oficineiro']}")
                st.write("----------")
        else:
            st.success(f"Não existe nenhum horário da categoria selecionada: {st.session_state.get('categoria_selecionada')}")

        if st.button("Voltar"):
            st.session_state['categoria_selecionada'] = None
            st.empty()
            st.rerun()
    elif st.session_state.get('categoria_selecionada') == 'Jazz':

        # Filtro para encontrar oficinas com o nome "Informática"
        oficinas_informatica = [oficina for oficina in oficinas if oficina["Nome"] == "Jazz"]
        
        if oficinas_informatica:
            for oficina in oficinas_informatica:
                st.write(f"Nome: {oficina['Nome']}")
                st.write(f"Categoria: {oficina['Categoria']}")
                st.write(f"Descrição: {oficina['Descricao']}")
                st.write(f"Oficineiro: {oficina['Oficineiro']}")
                st.write("----------")
        else:
            st.success(f"Não existe nenhum horário da categoria selecionada: {st.session_state.get('categoria_selecionada')}")

        if st.button("Voltar"):
            st.session_state['categoria_selecionada'] = None
            st.empty()
            st.rerun()
    elif st.session_state.get('categoria_selecionada') == 'Zumba':
        
         # Filtro para encontrar oficinas com o nome "Informática"
        oficinas_informatica = [oficina for oficina in oficinas if oficina["Nome"] == "Zumba"]
        
        if oficinas_informatica:
            for oficina in oficinas_informatica:
                st.write(f"Nome: {oficina['Nome']}")
                st.write(f"Categoria: {oficina['Categoria']}")
                st.write(f"Descrição: {oficina['Descricao']}")
                st.write(f"Oficineiro: {oficina['Oficineiro']}")
                st.write("----------")
        else:
            st.success(f"Não existe nenhum horário da categoria selecionada: {st.session_state.get('categoria_selecionada')}")

        if st.button("Voltar"):
            st.session_state['categoria_selecionada'] = None
            st.empty()
            st.rerun()
    elif st.session_state.get('categoria_selecionada') == 'Fisioterapia':

        # Filtro para encontrar oficinas com o nome "Informática"
        oficinas_informatica = [oficina for oficina in oficinas if oficina["Nome"] == "Fisioterapia"]
        
        if oficinas_informatica:
            for oficina in oficinas_informatica:
                st.write(f"Nome: {oficina['Nome']}")
                st.write(f"Categoria: {oficina['Categoria']}")
                st.write(f"Descrição: {oficina['Descricao']}")
                st.write(f"Oficineiro: {oficina['Oficineiro']}")
                st.write("----------")
        else:
            st.success(f"Não existe nenhum horário da categoria selecionada: {st.session_state.get('categoria_selecionada')}")

        if st.button("Voltar"):
            st.session_state['categoria_selecionada'] = None
            st.empty()
            st.rerun()
    elif st.session_state.get('categoria_selecionada') == 'Hip Hop':


         # Filtro para encontrar oficinas com o nome "Informática"
        oficinas_informatica = [oficina for oficina in oficinas if oficina["Nome"] == "Hip Hop"]
        
        if oficinas_informatica:
            for oficina in oficinas_informatica:
                st.write(f"Nome: {oficina['Nome']}")
                st.write(f"Categoria: {oficina['Categoria']}")
                st.write(f"Descrição: {oficina['Descricao']}")
                st.write(f"Oficineiro: {oficina['Oficineiro']}")
                st.write("----------")
        else:
            st.success(f"Não existe nenhum horário da categoria selecionada: {st.session_state.get('categoria_selecionada')}")

        if st.button("Voltar"):
            st.session_state['categoria_selecionada'] = None
            st.empty()
            st.rerun()

    else:

        st.title("Nossas Oficinas")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Definindo as categorias e suas descrições
        categorias = {
        'Informática': 'Aprenda a dominar as ferramentas digitais e programe para o futuro. Nossa oficina oferece uma base sólida em linguagens de programação essenciais como Python, JavaScript e muito mais. Desde o básico até tópicos avançados, como inteligência artificial e desenvolvimento de software, você adquirirá a confiança para criar aplicativos e sistemas inovadores com um excelente desempenho.',
        'Arte': 'Explore sua criatividade e se expresse por meio de diversas formas artísticas. Pintura, escultura, desenho e arte digital são algumas das possibilidades oferecidas nesta oficina. Você aprimorará suas habilidades artísticas, experimentará novas técnicas e estilos, e criará obras que transmitam suas emoções e pensamentos de forma única.',
        'Jazz': 'Sinta a liberdade e improvisação do jazz nesta oficina musical. Aqui, você aprenderá a tocar e se expressar musicalmente com fluidez e naturalidade. A oficina abrange aspectos como as bases rítmicas, harmônicas e a improvisação em tempo real, desenvolvendo sua musicalidade e percepção artística.',
        'Fisioterapia': 'Melhore seu bem-estar físico com técnicas de recuperação e prevenção. Esta oficina oferece uma abordagem prática e teórica, com foco no alívio de dores, recuperação de lesões e manutenção da saúde corporal. Você conhecerá diferentes tipos de fisioterapia, como ortopédica, neurológica e respiratória, e aprenderá a aplicar essas técnicas no dia a dia.',
        'Zumba': 'Divirta-se e queime calorias em uma aula cheia de energia e ritmo. Zumba mistura dança e exercícios aeróbicos de forma descontraída e contagiante. Nessa oficina, você aprenderá coreografias para músicas envolventes, realizando movimentos simples que trabalham todo o corpo e proporcionam uma experiência divertida e intensa.',
        'Hip Hop': 'Mergulhe no mundo da dança de rua e aprenda os passos do hip hop. Esta oficina ensina os movimentos e técnicas do hip hop, do básico às coreografias mais avançadas. Você terá a chance de explorar o estilo de dança mais popular do mundo, entender sua história e criar suas próprias rotinas de dança, desenvolvendo expressão corporal única.'
    }


        # Layout com 3 colunas para exibir as categorias, com equal width
        col1, col2, col3 = st.columns(3, gap='small')

        # Verificando se uma categoria foi selecionada
        categoria_selecionada = st.session_state.get('categoria_selecionada', None)

        

        # Criando blocos clicáveis para cada categoria
        with col1:
            with st.container(border=True):  # Adicionando borda
                if st.button("Informática", use_container_width=True):
                    st.session_state["categoria_selecionada"] = 'Informática'
                    st.empty()
                    st.rerun()
                st.markdown(f'<div class="container">{categorias["Informática"]}</div>', unsafe_allow_html=True)

            with st.container(border=True):  # Adicionando borda
                if st.button("Arte", use_container_width=True):
                    st.session_state["categoria_selecionada"] = 'Arte'
                    st.empty()
                    st.rerun()
                st.markdown(f'<div class="container">{categorias["Arte"]}</div>', unsafe_allow_html=True)

        with col2:
            with st.container(border=True):  # Adicionando borda
                if st.button("Jazz", use_container_width=True):
                    st.session_state["categoria_selecionada"] = 'Jazz'
                    st.empty()
                    st.rerun()
                st.markdown(f'<div class="container">{categorias["Jazz"]}</div>', unsafe_allow_html=True)

            with st.container(border=True):  # Adicionando borda
                if st.button("Fisioterapia", use_container_width=True):
                    st.session_state["categoria_selecionada"] = 'Fisioterapia'
                    st.empty()
                    st.rerun()
                st.markdown(f'<div class="container">{categorias["Fisioterapia"]}</div>', unsafe_allow_html=True)

        with col3:
            with st.container(border=True):  # Adicionando borda
                if st.button("Zumba", use_container_width=True):
                    st.session_state["categoria_selecionada"] = 'Zumba'
                    st.empty()
                    st.rerun()
                st.markdown(f'<div class="container">{categorias["Zumba"]}</div>', unsafe_allow_html=True)

            with st.container(border=True):  # Adicionando borda
                if st.button("Hip Hop", use_container_width=True):
                    st.session_state["categoria_selecionada"] = 'Hip Hop'
                    st.empty()
                    st.rerun()
                st.markdown(f'<div class="container">{categorias["Hip Hop"]}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Exibir a categoria selecionada
        if categoria_selecionada:
            st.success(f"Categoria selecionada: {categoria_selecionada}")

# Chama a função para apresentar as categorias
Apresentando_Oficinas()