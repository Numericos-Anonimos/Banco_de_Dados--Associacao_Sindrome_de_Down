import streamlit as st
import pandas as pd
from datetime import datetime, time, date
import os

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
    'Nome': "Futebol",
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
    'Nome': "Futebol",
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
    'Nome': "Desenho",
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
    st.title("Nossas Oficinas")

    # Layout com colunas para exibir as oficinas
    col1, col2, col3 = st.columns(3, gap='small')

    # Usando colunas para organizar as oficinas
    for i, oficina in enumerate(oficinas):
        # Definir qual coluna usar
        col = [col1, col2, col3][i % 3]
        with col:
            # Criando um container estilizado
            with st.container():
                # Aplicando estilo CSS para tornar clicável
                st.markdown(
                    f"""
                    <div style="
                        border: 1px solid #ddd; 
                        padding: 10px; 
                        border-radius: 8px; 
                        text-align: center; 
                        background-color: #f9f9f9; 
                        cursor: pointer;
                    " onclick="window.location.href='https://example.com/detalhes/{oficina['Nome'].replace(' ', '_')}'">
                        <h4 style="margin: 0;">{oficina['Nome']}</h4>
                        <p style="font-size: 12px; margin: 5px 0;">{oficina['Categoria']}</p>
                        <p style="font-size: 12px; margin: 5px 0;">{oficina['Dia_Semana']} {oficina['Horario_Inicio']} - {oficina['Horario_Fim']}</p>
                        <p style="font-size: 12px; margin: 5px 0;"><b>Oficineiro:</b> {oficina['Oficineiro']}</p>
                        <img src="{oficina['Fotos'][0]}" width="50">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Chama a função para apresentar as oficinas
Apresentando_Oficinas()
