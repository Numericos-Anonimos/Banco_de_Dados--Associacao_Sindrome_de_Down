import sqlalchemy
import streamlit as st
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)

def transformar_dicionario(result):
    dicionario = {}
    for row in result:
        dicionario[row[0]] = row[1]
    return dicionario

def auxiliares():
    with engine.connect() as con:
        atendidos = transformar_dicionario(
                        con.execute(sqlalchemy.text("""
                            SELECT Cod_Atendido, Nome
                            FROM Atendidos""")))
        
        eventos = transformar_dicionario(
                        con.execute(sqlalchemy.text("""
                            SELECT Cod_Evento, concat(Nome, " (", strftime('%d/%m/%Y', Data), ")")
                            FROM Eventos""")))
        
        funcionarios = transformar_dicionario(
                        con.execute(sqlalchemy.text("""
                            SELECT Cod_Funcionario, Nome
                            FROM Funcionarios""")))
        
        oficinas = transformar_dicionario(
                        con.execute(sqlalchemy.text("""
                            SELECT Cod_Oficina, concat(Nome, ' - ', Hora_Inicio)
                            FROM Oficinas""")))
        
        return atendidos, eventos, funcionarios, oficinas
        
if 'Atendidos' not in st.session_state:
    st.session_state['Atendidos'], st.session_state['Eventos'], st.session_state['Funcionarios'], st.session_state['Oficinas'] = auxiliares()
st.session_state['Atendidos'], st.session_state['Eventos'], st.session_state['Funcionarios'], st.session_state['Oficinas'] = auxiliares()

def realizar_busca():
    atendidos = ', '.join(str(i) for i in st.session_state['Atendidos_selecionados'])
    eventos = ', '.join(str(i) for i in st.session_state['Eventos_selecionados'])
    funcionarios = ', '.join(str(i) for i in st.session_state['Funcionarios_selecionados'])
    oficinas = ', '.join(str(i) for i in st.session_state['Oficinas_selecionadas'])
    
    with engine.connect() as con:
        query = f"""
                    SELECT f.Caminho
                    FROM Fotos f
        """
        if atendidos or eventos or funcionarios or oficinas:
            query += 'WHERE\n'
            if atendidos:
                query += f'f.Cod_Foto IN (\nSELECT Cod_Foto FROM Atendido_Fotos\nWHERE Cod_Atendido IN ({atendidos}))\n'
            if eventos:
                query += f'{"" if query[-6::] == "WHERE\n" else "AND"} f.Cod_Foto IN (\nSELECT Cod_Foto FROM Evento_Fotos\nWHERE Cod_Evento IN ({eventos}))\n'
            if funcionarios:
                query += f'{"" if query[-6::] == "WHERE\n" else "AND"} f.Cod_Foto IN (\nSELECT Cod_Foto FROM Funcionario_Fotos\nWHERE Cod_Funcionario IN ({funcionarios}))\n'
            if oficinas:
                query += f'{"" if query[-6::] == "WHERE\n" else "AND"} f.Cod_Foto IN (\nSELECT Cod_Foto FROM Oficina_Fotos\nWHERE Cod_Oficina IN ({oficinas}))\n'
        result = con.execute(sqlalchemy.text(query))
        return result.fetchall()
