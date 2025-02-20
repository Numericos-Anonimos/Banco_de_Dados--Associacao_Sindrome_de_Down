from timetable_canvas import timetable_canvas_generator
import streamlit as st
import pandas as pd
from datetime import time

def convert_to_timetable(cursos):
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

# Dados de exemplo no novo formato
cursos = [
    {
        'Cod_Oficina': 1,
        'Nome': "Informática",
        'Dia_Semana': "SEG",
        'Horario_Inicio': time(8, 0),
        'Horario_Fim': time(10, 0),
    },
    {
        'Cod_Oficina': 2,
        'Nome': "Matemática",
        'Dia_Semana': "TER",
        'Horario_Inicio': time(10, 0),
        'Horario_Fim': time(12, 0),
    }
]

# Converter para grade
timetable = convert_to_timetable(cursos)

# Gerar componente visual
updated_timetable = timetable_canvas_generator(
    timetable,
    timetableType=['08:00', '09:00', '10:00', '11:00', '12:00', 
                  '13:00', '14:00', '15:00', '16:00', '17:00'],
    Gheight=100
)

st.write(updated_timetable)