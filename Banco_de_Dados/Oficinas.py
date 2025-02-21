import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)
metadata = sqlalchemy.MetaData()
metadata.create_all(engine)
table = sqlalchemy.Table('ASIN', metadata)

import pandas as pd
dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
convert_dias = lambda x: dias_semana[x-1]

from datetime import datetime, date, time
def consultar(sql):
    with engine.connect() as con:
        return con.execute(sqlalchemy.text(sql))

def listar_oficinas():
    rs = consultar("""
        SELECT 
            o.Cod_Oficina AS "Código", o.Nome AS "Oficina", p.Nome AS "Projeto",
            o.Data_Inicio AS "Data de Início", o.Data_Fim AS "Data de Término",
            o.Dia_Semana AS "Dia da Semana", o.Hora_Inicio AS "Hora de Início", 
            o.Hora_Fim AS "Hora de Término", o.Vagas, count(DISTINCT ao.Cod_Atendido) AS "Participantes",
            f.Nome AS "Responsável", o.Valor_Hora AS "Preço", o.Descricao
        FROM Oficinas o
        INNER JOIN Funcionarios f ON o.Cod_Funcionario = f.Cod_Funcionario
        INNER JOIN Projetos p ON o.Cod_Projeto = p.Cod_Projeto
        LEFT JOIN Atendido_Oficinas ao ON 
            ao.Cod_Oficina = o.Cod_Oficina
            AND ao.Data_Fim IS NULL
        GROUP BY o.Cod_Oficina
        """)
    
    df = pd.DataFrame([list(row) for row in rs], columns=rs.keys())
    df['Projeto'] = df['Projeto'].astype('category')
    df['Dia da Semana'] = df['Dia da Semana'].apply(convert_dias).astype('category')
    return df

print(listar_oficinas()['Participantes'])
    
def buscar_oficina(cod_oficina):
    # Pegando dados gerais da oficina
    rs = consultar(f"""
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
        """)
    row = rs.fetchone()
    if row is None:
        raise ValueError('Oficina não encontrada')
    oficina = {key: val for key, val in zip(rs.keys(), row)}
        
    oficina['Hora de Início'] = time()
    oficina['Hora de Término'] = time(*map(int, oficina['Hora de Término'].split(':')))    
    rs = consultar(f"""
        SELECT Data, Entrada, Saida
        FROM Funcionario_Presencas
        WHERE 
            Cod_Funcionario = {oficina['Código do Responsável']} 
            AND strftime('%w', Data) = '{oficina['Dia da Semana']}' 
            AND Entrada <= '{oficina['Hora de Início']}' 
            AND Saida >= TIME('{oficina['Hora de Término']}')
        ORDER BY Data;
        """)
    oficina['Houve_Oficina'] = [date(*map(int, data.split('-'))) for data, _, _ in rs]

    # Participantes da oficina e dias que participaram
    rs = consultar(f"""
        SELECT a.Nome, data
        FROM Atendidos a
        INNER JOIN Atendido_Oficinas ao ON 
            a.Cod_Atendido = ao.Cod_Atendido
            and ao.Cod_Oficina = {cod_oficina}       
        INNER JOIN Atendido_Presencas ap ON 
            a.Cod_Atendido = ap.Cod_Atendido
            and strftime('%w', ap.Data) = '{oficina['Dia da Semana']}'
        """)
    presencas = {}
    for nome, data in rs:
        if nome not in presencas:
            presencas[nome] = []
        presencas[nome].append(date(*map(int, data.split('-'))))
    oficina['Presenças'] = presencas

    # Fotos
    rs = consultar(f"""
        SELECT f.Caminho
        FROM Fotos f
        INNER JOIN Oficina_Fotos of ON
            f.Cod_Foto = of.Cod_Foto
            AND of.Cod_Oficina = {cod_oficina}
        """)
    oficina['Fotos'] = [caminho for caminho, in rs]

    
    return oficina

print(listar_oficinas())



        