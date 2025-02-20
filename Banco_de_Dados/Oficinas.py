import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)
metadata = sqlalchemy.MetaData()
metadata.create_all(engine)
table = sqlalchemy.Table('ASIN', metadata)

import pandas as pd
dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
convert_dias = lambda x: dias_semana[x-1]

from datetime import datetime, date, time

def listar_oficinas():
    with engine.connect() as con:
        rs = con.execute(sqlalchemy.text("""
        SELECT 
            o.Cod_Oficina AS "Código", o.Nome AS "Oficina", p.Nome AS "Projeto",
            o.Data_Inicio AS "Data de Início", o.Data_Fim AS "Data de Término",
            o.Dia_Semana AS "Dia da Semana", o.Hora_Inicio AS "Hora de Início", 
            o.Hora_Fim AS "Hora de Término", o.Vagas, f.Nome AS "Responsável", 
            o.Valor_Hora AS "Preço", o.Descricao
        FROM Oficinas o
        INNER JOIN Funcionarios f ON o.Cod_Funcionario = f.Cod_Funcionario
        INNER JOIN Projetos p ON o.Cod_Projeto = p.Cod_Projeto
        """))
    
    df = pd.DataFrame([list(row) for row in rs], columns=rs.keys())
    df['Projeto'] = df['Projeto'].astype('category')
    df['Dia da Semana'] = df['Dia da Semana'].apply(convert_dias).astype('category')
    return df
    
def buscar_oficina(cod_oficina):
    # Pegando dados gerais da oficina
    with engine.connect() as con:
        rs = con.execute(sqlalchemy.text(f"""
        SELECT 
            o.Cod_Oficina AS "Código", o.Nome AS "Oficina", p.Nome AS "Projeto",
            o.Data_Inicio AS "Data de Início", o.Data_Fim AS "Data de Término",
            o.Dia_Semana AS "Dia da Semana", o.Hora_Inicio AS "Hora de Início", 
            o.Hora_Fim AS "Hora de Término", o.Vagas, f.Nome AS "Responsável", 
            f.Cod_Funcionario AS "Código do Responsável", o.Valor_Hora AS "Preço", 
            o.Descricao
        FROM Oficinas o
        INNER JOIN Funcionarios f ON o.Cod_Funcionario = f.Cod_Funcionario
        INNER JOIN Projetos p ON o.Cod_Projeto = p.Cod_Projeto
        WHERE o.Cod_Oficina = {cod_oficina}
        """))
    row = rs.fetchone()
    if row is None:
        raise ValueError('Oficina não encontrada')
    oficina = {key: val for key, val in zip(rs.keys(), row)}
    
    # Pegando dias que a oficina ocorreu (dias que o funcionário responsável estava presente no horário da oficina)
    with engine.connect() as con:
        rs = con.execute(sqlalchemy.text(f"""
        SELECT Data, Entrada, Saida
        FROM Funcionario_Presencas
        WHERE 
            Cod_Funcionario = {oficina['Código do Responsável']} 
            AND strftime('%w', Data) = '{oficina['Dia da Semana']}' 
            AND Entrada <= '{oficina['Hora de Início']}' 
            AND Saida >= '{oficina['Hora de Término']}'
        ORDER BY Data;
        """))

    return oficina, list(rs)
    

# print(buscar_oficina(1))



        