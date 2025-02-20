import streamlit as st
import pandas as pd
from datetime import datetime, time, date
import os


#st.set_page_config(page_title="Oficinas", layout="wide")






def apresentar_oficinas1(oficinas):
    if "oficina_selecionada" in st.session_state and st.session_state["oficina_selecionada"]:
        oficina_selecionada = st.session_state["oficina_selecionada"]
        dados = oficina_selecionada.copy()
        
        edit_mode = st.session_state.get('edit_mode', False)
        
        if not st.session_state.edit_mode:
            cols = st.columns([2.5, 1])
            cols[0].title(f'{dados["Nome"]}')
            cols[1].header(f'Status: {"✅" if dados["Data_Fim"] is None else "❌"}')
            st.markdown("<br>",unsafe_allow_html=True)

            cols = st.columns(3)
            cols[0].write(f'**Categoria**: {dados["Categoria"]}')
            cols[1].write(f'**Projeto**: {dados["Projeto"]}')
            cols[2].write(f'**Data de Cadastro**: {dados["Data_Cadastro"].strftime("%d/%m/%Y")}{"" if dados["Data_Fim"] is None else f" - {dados["Data_Fim"].strftime("%d/%m/%Y")}" }')

            cols = st.columns(3)
            cols[0].write(f'**Dia da Semana**: {dados["Dia_Semana"]}')
            cols[1].write(f'**Horário**: {dados["Horario_Inicio"].strftime("%H:%M")} às {dados["Horario_Fim"].strftime("%H:%M")} ({sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"])} minutos)')
            cols[2].write(f'**Usuários**: {len(dados["Participantes"])} / {dados["Max_Participantes"]}')

            cols = st.columns(3)
            cols[0].write(f'**Oficineiro**: {dados["Oficineiro"]}')
            cols[1].write(f'**Valor por Hora**: R$ {dados["Valor_Hora"]:.2f}')
            cols[2].write(f'**Total**: R$ {len(dados["Houve_Oficina"]) * sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"]) * dados["Valor_Hora"] / 60:.2f}')
            
            st.write(f'**Descrição**: {dados["Descricao"]}')

            if st.button("Editar"):
                st.session_state.edit_mode = True
                st.rerun()

            st.markdown("---")
            st.header("Presenças")
            min_date, max_date = min(dados['Houve_Oficina']), max(dados['Houve_Oficina'])
            cols = st.columns(2)

            selected_dates = [cols[0].date_input("Data Inicial", min_date, min_value=min_date, max_value=max_date, format="DD/MM/YYYY")]
            selected_dates.append(cols[1].date_input("Data Final", max_date, min_value=selected_dates[0], max_value=max_date, format="DD/MM/YYYY"))

            show_all_dates = st.checkbox("Mostrar todas as datas")

            if show_all_dates:
                all_dates = pd.date_range(selected_dates[0], selected_dates[1])
                date_list = [d.date() for d in all_dates]
            else:
                date_list = [d for d in dados['Houve_Oficina'] if selected_dates[0] <= d <= selected_dates[1]]

            date_strings = [d.strftime("%d/%m/%Y") for d in date_list]
            df = pd.DataFrame(index=dados['Participantes'].keys(), columns=date_strings, dtype=str)

            for participante, presencas in dados['Participantes'].items():
                for data in date_list:
                    data_str = data.strftime("%d/%m/%Y")
                    df.loc[participante, data_str] = "✅" if data in presencas else "❌" if data in dados['Houve_Oficina'] else "⬜"

            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.subheader("Fotos")
            if st.checkbox("Mostrar Fotos"):
                cols = st.columns(3)
                for idx, foto in enumerate(dados['Fotos']):
                    if os.path.exists(foto):
                        cols[idx % 3].image(foto, use_column_width=True)
                    else:
                        st.error(f"Imagem não encontrada: {foto}")
            if st.button("Voltar"):
                st.session_state["oficina_selecionada"] = None
                st.rerun()

        else:
            novos_dados = dados.copy()
            novos_dados["Nome"] = st.text_input("Nome", value=dados["Nome"])
            novos_dados["Categoria"] = st.text_input("Categoria", value=dados["Categoria"])
            novos_dados["Max_Participantes"] = st.number_input("Máximo de Participantes", value=dados["Max_Participantes"], min_value=1, max_value=100)
            novos_dados["Valor_Hora"] = st.number_input("Valor por Hora", value=dados["Valor_Hora"], min_value=0.01, format="%.2f", step=1.0)
            novos_dados["Descricao"] = st.text_area("Descrição", value=dados["Descricao"])
            
            cols = st.columns(2)
            if cols[0].button("Salvar", use_container_width=True):
                dados.update(novos_dados)
                st.session_state.edit_mode = False
                st.rerun()
            if cols[1].button("Cancelar", use_container_width=True):
                st.session_state.edit_mode = False
                st.rerun()
            st.info("Modo de edição ativado. Altere os campos e clique em 'Salvar alterações'.")
    else:
        st.title("Nossas Oficinas")
        oficinas_unicas = {oficina['Nome']: oficina for oficina in oficinas}.values()
        num_oficinas = len(oficinas_unicas)
        st.markdown("<br>",unsafe_allow_html=True)
        
        for i in range(0, num_oficinas, 3):
            cols = st.columns(3)
            for j, oficina in enumerate(list(oficinas_unicas)[i:i+3]):
                with cols[j]:
                    with st.container(border=True):
                        if st.button(oficina["Nome"], use_container_width=True, key=f"btn_{oficina['Cod_Oficina']}"):
                            st.session_state["oficina_selecionada"] = oficina
                            st.rerun()
                        st.markdown(f'<div style="text-align: center; font-size: 12px; color: gray;">{oficina["Descricao"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")











# Oficial após a mudança do componente para a página de atendidos:


oficinas = [{
    'Cod_Oficina': 1,
    'Nome': "Informática",
    'Categoria': "Tecnologia",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "TER",
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
    'Nome': "Clinica",
    'Categoria': "Esporte",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "QUA",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Clinica",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
    },
    {
    'Cod_Oficina': 3,
    'Nome': "Esporte",
    'Categoria': "Esporte",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(11, 0),
    'Horario_Fim': time(12, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Esporte",
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
    'Descricao': "Oficina de Esporte",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/Sem título.jpg']
    },
    {
    'Cod_Oficina': 5,
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
    'Cod_Oficina': 6,
    'Nome': "Hip Hop",
    'Categoria': "Dança",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Dança",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png', 'Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
    },{
    'Cod_Oficina':7,
    'Nome': "Jazz",
    'Categoria': "Dança",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Dança",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png', 'Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
    },{
    'Cod_Oficina': 8,
    'Nome': "Zumba",
    'Categoria': "Dança",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Dança",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png', 'Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
    },{
    'Cod_Oficina': 9,
    'Nome': "Fisioterapia",
    'Categoria': "Clinica",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "SEG",
    'Horario_Inicio': time(8, 0),
    'Horario_Fim': time(10, 0),
    'Max_Participantes': 10,
    'Valor_Hora': 10.00,
    'Descricao': "Oficina de Clinica",
    'Oficineiro': "João Victor Assaoka Ribeiro",
    'Houve_Oficina': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)],
    'Participantes': {'Thomas Pires': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)], 'Lucas Molinari': [date(2024, 2, 3), date(2024, 2, 17), date(2024, 2, 24)], 'Miguel': [date(2024, 2, 3), date(2024, 2, 10), date(2024, 2, 17), date(2024, 2, 24)]},
    'Fotos': ['Imagens/Outras/octocat-1692375072300.png', 'Imagens/Outras/roxo.jpg', 'Imagens/Outras/Sem título.jpg']
    }
]


if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

def sub_hora(ini:time, fim:time):
    return (fim.hour - ini.hour) * 60 + (fim.minute - ini.minute)



from datetime import datetime, time
import streamlit as st

def apresentar_oficinas2(oficinas):
    if 'oficina_selecionada' in st.session_state and st.session_state['oficina_selecionada']:
        oficina_selecionada = st.session_state["oficina_selecionada"]
    
        # Verifique o tipo do objeto antes de tentar fazer a cópia
        if isinstance(oficina_selecionada, dict):
            dados = oficina_selecionada.copy()  # Só chama copy() se for um dicionário
        else:
            st.error("A oficina selecionada não é um dicionário!")
            return  # Encerra a execução da função ou faz outra ação apropriada
        
        edit_mode = st.session_state.get('edit_mode', False)
        
        if not st.session_state.edit_mode:
            cols = st.columns([2.5, 1])
            cols[0].title(f'{dados["Nome"]}')
            cols[1].header(f'Status: {"✅" if dados["Data_Fim"] is None else "❌"}')
            st.markdown("<br>", unsafe_allow_html=True)

            cols = st.columns(3)
            cols[0].write(f'**Categoria**: {dados["Categoria"]}')
            cols[1].write(f'**Projeto**: {dados["Projeto"]}')
            cols[2].write(f'**Data de Cadastro**: {dados["Data_Cadastro"].strftime("%d/%m/%Y")}{"" if dados["Data_Fim"] is None else f" - {dados['Data_Fim'].strftime('%d/%m/%Y')}" }')

            cols = st.columns(3)
            cols[0].write(f'**Dia da Semana**: {dados["Dia_Semana"]}')
            cols[1].write(f'**Horário**: {dados["Horario_Inicio"].strftime("%H:%M")} às {dados["Horario_Fim"].strftime("%H:%M")} ({sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"])} minutos)')
            cols[2].write(f'**Usuários**: {len(dados["Participantes"])} / {dados["Max_Participantes"]}')

            cols = st.columns(3)
            cols[0].write(f'**Oficineiro**: {dados["Oficineiro"]}')
            cols[1].write(f'**Valor por Hora**: R$ {dados["Valor_Hora"]:.2f}')
            cols[2].write(f'**Total**: R$ {len(dados["Houve_Oficina"]) * sub_hora(dados["Horario_Inicio"], dados["Horario_Fim"]) * dados["Valor_Hora"] / 60:.2f}')
            
            st.write(f'**Descrição**: {dados["Descricao"]}')

            if st.button("Editar"):
                st.session_state.edit_mode = True
                st.rerun()

            st.markdown("---")
            st.header("Presenças")
            min_date, max_date = min(dados['Houve_Oficina']), max(dados['Houve_Oficina'])
            cols = st.columns(2)

            selected_dates = [cols[0].date_input("Data Inicial", min_date, min_value=min_date, max_value=max_date, format="DD/MM/YYYY")]
            selected_dates.append(cols[1].date_input("Data Final", max_date, min_value=selected_dates[0], max_value=max_date, format="DD/MM/YYYY"))

            show_all_dates = st.checkbox("Mostrar todas as datas")

            if show_all_dates:
                all_dates = pd.date_range(selected_dates[0], selected_dates[1])
                date_list = [d.date() for d in all_dates]
            else:
                date_list = [d for d in dados['Houve_Oficina'] if selected_dates[0] <= d <= selected_dates[1]]

            date_strings = [d.strftime("%d/%m/%Y") for d in date_list]
            df = pd.DataFrame(index=dados['Participantes'].keys(), columns=date_strings, dtype=str)

            for participante, presencas in dados['Participantes'].items():
                for data in date_list:
                    data_str = data.strftime("%d/%m/%Y")
                    df.loc[participante, data_str] = "✅" if data in presencas else "❌" if data in dados['Houve_Oficina'] else "⬜"

            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.subheader("Fotos")
            if st.checkbox("Mostrar Fotos"):
                cols = st.columns(3)
                for idx, foto in enumerate(dados['Fotos']):
                    if os.path.exists(foto):
                        cols[idx % 3].image(foto, use_column_width=True)
                    else:
                        st.error(f"Imagem não encontrada: {foto}")
            if st.button("Voltar", key=f"voltar_{dados['Cod_Oficina']}"):
                st.session_state["oficina_selecionada"] = None
                st.session_state["oficina_nome_selecionada"] = None
                st.rerun()

        else:
            novos_dados = dados.copy()
            novos_dados["Nome"] = st.text_input("Nome", value=dados["Nome"])
            novos_dados["Categoria"] = st.text_input("Categoria", value=dados["Categoria"])
            novos_dados["Max_Participantes"] = st.number_input("Máximo de Participantes", value=dados["Max_Participantes"], min_value=1, max_value=100)
            novos_dados["Valor_Hora"] = st.number_input("Valor por Hora", value=dados["Valor_Hora"], min_value=0.01, format="%.2f", step=1.0)
            novos_dados["Descricao"] = st.text_area("Descrição", value=dados["Descricao"])
            
            cols = st.columns(2)
            if cols[0].button("Salvar", use_container_width=True):
                dados.update(novos_dados)
                st.session_state.edit_mode = False
                st.rerun()
            if cols[1].button("Cancelar", use_container_width=True):
                st.session_state.edit_mode = False
                st.rerun()
            st.info("Modo de edição ativado. Altere os campos e clique em 'Salvar alterações'.")

    elif "oficina_nome_selecionado" in st.session_state and st.session_state["oficina_nome_selecionado"]:
        oficina_nome_selecionado = st.session_state["oficina_nome_selecionado"]
        
        st.title(f"Oficinas Selecionadas: {oficina_nome_selecionado}")
        st.markdown("<br>", unsafe_allow_html=True)

        # Filtro por dias da semana dentro do primeiro if, usando multiselect
        dias_semana = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]
        dias_selecionados = st.multiselect("Selecione os dias da semana:", dias_semana)

        st.markdown("---")
        # Filtrando oficinas com o nome igual ao selecionado
        oficinas_filtradas = [oficina for oficina in oficinas if oficina["Nome"] == oficina_nome_selecionado]

        # Se houver dias selecionados, aplica o filtro
        if dias_selecionados:
            oficinas_filtradas = [oficina for oficina in oficinas_filtradas if oficina['Dia_Semana'] in dias_selecionados]

        for oficina in oficinas_filtradas:
            # Convertendo Horário de Início e Fim para string
            horario_inicio = oficina['Horario_Inicio'].strftime("%H:%M")
            horario_fim = oficina['Horario_Fim'].strftime("%H:%M")
            # Exibindo a data de início e fim
            data_inicio = oficina['Data_Cadastro'].strftime("%d/%m/%Y")
            dia_semana_inicio = oficina['Dia_Semana']
            dia_semana_fim = oficina['Dia_Semana']  # Presumindo que o fim ocorre no mesmo dia da semana
            
            # Criando a estrutura para exibição
            with st.container(border=True):
                # Definindo as colunas para layout: uma para informações e outra para o botão
                cols = st.columns([4, 1])  # A primeira coluna é maior para as informações, a segunda é menor para o botão
                with cols[0]:
                    st.markdown(f"### {oficina['Nome']}")
                    st.markdown(f"**Categoria:** {oficina['Categoria']}")
                    st.markdown(f"**Oficineiro:** {oficina['Oficineiro']}")
                    st.markdown(f"**Horário:** {horario_inicio} - {horario_fim}")
                    st.markdown(f"**Data:** {data_inicio} ({dia_semana_inicio})")
                
                with cols[1]:
                    st.markdown("""
                        <style>
                            .button-container {
                                display: flex;
                                flex-direction: column;
                                justify-content: flex-end;
                                height: 100%;  /* Garantir que o container ocupe toda a altura */
                                margin-top: auto;  /* Posiciona o botão na parte inferior */
                            }
                        </style>
                    """, unsafe_allow_html=True)

                    with st.container():
                        st.markdown('<div class="button-container">', unsafe_allow_html=True)
                        if st.button("Ver Mais", key=f"ver_mais_{oficina['Cod_Oficina']}"):
                            st.session_state["oficina_selecionada"] = oficina
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")

        
        # Botão de voltar para a lista de oficinas
        if st.button("Voltar"):
            # Limpa o estado da oficina selecionada
            st.session_state["oficina_nome_selecionado"] = None
            st.rerun()  # Reinicia a página para exibir a lista inicial de oficinas
    else:
        st.title("Nossas Oficinas")
        st.markdown("<br>", unsafe_allow_html=True)

        # Filtrando categorias únicas
        categorias_unicas = sorted(set(oficina['Categoria'] for oficina in oficinas))

        # Select box para escolher a categoria
        categoria_selecionada = st.selectbox("Selecione uma categoria:", ["Todas"] + categorias_unicas)

        # Filtrando as oficinas com base na categoria selecionada
        if categoria_selecionada != "Todas":
            oficinas_filtradas = [oficina for oficina in oficinas if oficina['Categoria'] == categoria_selecionada]
        else:
            oficinas_filtradas = oficinas

        st.markdown("---")

        # Obtendo oficinas únicas
        oficinas_unicas = {oficina['Nome']: oficina for oficina in oficinas_filtradas}.values()
        num_oficinas = len(oficinas_unicas)

        # Inserindo espaçamento
        st.markdown("<br>", unsafe_allow_html=True)

        # Exibindo as oficinas
        for i in range(0, num_oficinas, 3):
            cols = st.columns(3)
            for j, oficina in enumerate(list(oficinas_unicas)[i:i+3]):
                with cols[j]:
                    with st.container(border=True):
                        if st.button(oficina["Nome"], use_container_width=True, key=f"btn_{oficina['Cod_Oficina']}"):
                            st.session_state["oficina_nome_selecionado"] = oficina["Nome"]
                            st.rerun()
                        st.markdown(f'<div style="text-align: center; font-size: 12px; color: gray;">{oficina["Descricao"]}</div>', unsafe_allow_html=True)











apresentar_oficinas2(oficinas)



with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)
