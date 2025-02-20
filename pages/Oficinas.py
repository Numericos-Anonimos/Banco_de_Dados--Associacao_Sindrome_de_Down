import streamlit as st
import pandas as pd
from datetime import datetime, time, date
import os

from timetable_canvas import timetable_canvas_generator


st.set_page_config(page_title="Oficinas", layout="wide")

def convert_to_timetable(cursos): # Para plotar o componente baseado no array de dicionários do banco de dados
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
    
    # Grade inicializada com horários vazios
    timetable = [['' for _ in time_slots] for _ in day_map.values()]
    
    for curso in cursos:
        dia = day_map.get(curso['Dia_Semana'].upper())
        inicio = curso['Horario_Inicio'].strftime('%H:%M')
        fim = curso['Horario_Fim'].strftime('%H:%M')
        
        try:
            idx_dia = list(day_map.values()).index(dia)
            idx_inicio = time_slots.index(inicio)
            idx_fim = time_slots.index(fim)
        except (ValueError, KeyError):
            continue
        
        # Cria um item para cada horário individual
        for slot in range(idx_inicio, idx_fim):
            horario = time_slots[slot]
            timetable[idx_dia][slot] = f"{curso['Nome']} ({horario})"  # Item único por horário

    return timetable

# Dados das oficinas
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
    'Nome': "Teste",
    'Categoria': "Esporte",
    'Projeto': "Projeto 1",
    'Data_Cadastro': date(2005, 5, 4),
    'Data_Fim': None,
    'Dia_Semana': "QUA",
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

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

def sub_hora(ini:time, fim:time):
    return (fim.hour - ini.hour) * 60 + (fim.minute - ini.minute)

def apresentar_oficinas1(oficinas):
    if "oficina_selecionada" in st.session_state and st.session_state["oficina_selecionada"]:
        oficina_selecionada = st.session_state["oficina_selecionada"]
        dados = oficina_selecionada.copy()
        
        edit_mode = st.session_state.get('edit_mode', False)
        
        if not edit_mode:
            cols = st.columns([2.5, 1])
            cols[0].header(dados["Nome"])
            cols[1].header(f"Status: {'✅' if dados['Data_Fim'] is None else '❌'}")
        
            cols = st.columns(3)
            cols[0].write(f'**Categoria**: {dados["Categoria"]}')
            cols[1].write(f'**Projeto**: {dados["Projeto"]}')
            data_fim = f" - {dados['Data_Fim'].strftime('%d/%m/%Y')}" if dados["Data_Fim"] else ""
            cols[2].write(f'**Data de Cadastro**: {dados["Data_Cadastro"].strftime("%d/%m/%Y")}{data_fim}')
        
        if edit_mode:
            novos_dados = dados.copy()
            novos_dados["Nome"] = st.text_input("Nome", value=dados["Nome"])
            novos_dados["Data_Fim"] = st.date_input("Data de Encerramento", value=dados["Data_Fim"], min_value=dados["Data_Cadastro"], max_value=date(2100, 12, 31))
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
            if st.button("Editar"):
                st.session_state.edit_mode = True
                st.rerun()
                
        st.header("Presenças")
        min_date, max_date = min(dados['Houve_Oficina']), max(dados['Houve_Oficina'])
        cols = st.columns(2)
        
        selected_dates = [cols[0].date_input("Data Inicial", min_date, min_value=min_date, max_value=max_date)]
        selected_dates.append(cols[1].date_input("Data Final", max_date, min_value=selected_dates[0], max_value=max_date))
        
        show_all_dates = st.checkbox("Mostrar todas as datas")
        date_list = [d.date() for d in pd.date_range(selected_dates[0], selected_dates[1])] if show_all_dates else [d for d in dados['Houve_Oficina'] if selected_dates[0] <= d <= selected_dates[1]]
        
        date_strings = [d.strftime("%d/%m/%Y") for d in date_list]
        df = pd.DataFrame(index=dados['Participantes'].keys(), columns=date_strings, dtype=str)
        
        for participante, presencas in dados['Participantes'].items():
            for data in date_list:
                df.loc[participante, data.strftime("%d/%m/%Y")] = "✅" if data in presencas else "❌" if data in dados['Houve_Oficina'] else "⬜"
        
        st.dataframe(df, use_container_width=True)
        
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
        st.title("Nossas Oficinas")
        oficinas_unicas = {oficina['Nome']: oficina for oficina in oficinas}.values()
        num_oficinas = len(oficinas_unicas)
        
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
        # Converter para grade
        timetable = convert_to_timetable(oficinas)

        # Gerar componente visual
        updated_timetable = timetable_canvas_generator(
            timetable,
            timetableType=['08:00', '09:00', '10:00', '11:00', '12:00', 
                        '13:00', '14:00', '15:00', '16:00', '17:00'],
            Gheight=100
        )

        st.write(updated_timetable)

apresentar_oficinas1(oficinas)



with st.sidebar:
    #st.logo("Imagens/BannerASIN.png", icon_image="Imagens/LogoASIN.png")
    st.image("Imagens/BannerASIN.png", use_container_width=True)
