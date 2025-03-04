import streamlit as st
import sqlalchemy
import pandas as pd

import Banco_de_Dados.Imagens as Imagens

with st.container(border=True):
    st.multiselect('Atendidos', key='Atendidos_selecionados', 
                   options=st.session_state['Atendidos'].keys(),
                   format_func=lambda x: st.session_state['Atendidos'][x])
    st.multiselect('Eventos', key='Eventos_selecionados',
                   options=st.session_state['Eventos'].keys(),
                   format_func=lambda x: st.session_state['Eventos'][x])
    st.multiselect('Funcionarios', key='Funcionarios_selecionados',
                   options=st.session_state['Funcionarios'].keys(),
                   format_func=lambda x: st.session_state['Funcionarios'][x])
    st.multiselect('Oficinas', key='Oficinas_selecionadas',
                   options=st.session_state['Oficinas'].keys(),
                   format_func=lambda x: st.session_state['Oficinas'][x])

    st.button('Buscar', key='button_buscar_imagens')

if st.session_state['button_buscar_imagens']:
    st.session_state['fotos'] = Imagens.realizar_busca()

if 'fotos' in st.session_state:
    fotos = st.session_state['fotos']
    cols = st.columns(3)
    for i in range (len(fotos)):
        with cols[i % 3]:
            st.image(f'Banco de Imagens/{fotos[i][0]}')