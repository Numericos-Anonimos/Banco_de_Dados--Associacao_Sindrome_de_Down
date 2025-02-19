import streamlit as st
import pandas as pd
from datetime import datetime, time, date
import os

st.set_page_config(page_title="Oficinas", layout="wide")

# Dados das oficinas
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




def filtrar_oficinas(nome):
    return [oficina for oficina in oficinas if nome.lower() in oficina['Nome'].lower()]





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

        st.markdown("""
            <style>
            .container {
                width: 100%;
                height: 260px; /* Altura fixa para garantir o tamanho igual */
                border-radius: 10px; /* Bordas arredondadas */
                padding: 7px;
                margin-bottom: 15px; /* Espaço inferior */
                text-align: justify; /* Alinhamento do texto */
            }
            .stButton > button {
                width: 100%; /* Botões de categoria ocupando toda a largura do container */
            }
            </style>
        """, unsafe_allow_html=True)

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



with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)
