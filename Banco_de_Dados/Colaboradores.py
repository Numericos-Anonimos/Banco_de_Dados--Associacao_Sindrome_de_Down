import sqlalchemy

# Criando a engine e conectando ao banco
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)

def listar_funcionarios():
    with engine.connect() as con:
        result = con.execute(sqlalchemy.text("""
            SELECT 
                f.Cod_Funcionario AS "Cod_Funcionario", f.Nome AS "Nome", f.Status AS "Status",
                f.CPF AS "CPF", f.CEP AS "CEP", f.Numero AS "Numero", f.Complemento AS "Complemento",
                f.Observacoes AS "Observacoes", f.Salario + 10 AS "Salario"
            FROM Funcionarios f
            LEFT JOIN Oficinas o ON o.Cod_Funcionario = f.Cod_Funcionario
        """))
        columns = result.keys()

        funcionarios = [dict(zip(columns, row)) for row in result]
    
    return funcionarios

def funcionario_contatos (Cod_Funcionario):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT C.Telefone, C.Descricao
            FROM Contatos C
            JOIN Funcionario_Contatos F ON F.Cod_Contato = C.Cod_Contato
            WHERE F.Cod_Funcionario = :cod;
        """)

        telefones = con.execute(query, {"cod": Cod_Funcionario})

        # Retornando uma lista de tuplas (Telefone, Descrição)
        telefone_list = [(row[0], row[1]) for row in telefones]

    return telefone_list

def funcionario_oficinas (Cod_Funcionario):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT o.Dia_Semana, o.Hora_Inicio, o.Hora_Fim, o.Nome
            FROM Oficinas o
            WHERE o.Cod_Funcionario = :cod;
        """)

        oficinas = con.execute(query, {"cod": Cod_Funcionario})

        # Mapeamento de números para dias da semana
        dias_semana = {
            1: "SEG", 2: "TER", 3: "QUA", 4: "QUI", 5: "SEX", 6: "SÁB", 7: "DOM"
        }

        oficina_dict = {
            f"{dias_semana.get(row[0], 'DIA INVÁLIDO')} - {row[1]} ÀS {row[2]}": 
            [dias_semana.get(row[0], None)] + [i for i in row[1:]]
            for row in oficinas
        }

    return oficina_dict

def funcionario_ponto (Cod_Funcionario):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT P.Data, P.Entrada, P.Saida
            FROM Funcionario_Presencas P
            WHERE P.Cod_Funcionario = :cod
        """)

        result = con.execute(query, {"cod": Cod_Funcionario})

        # Retornando apenas uma lista de datas
        datas = [(row[0], row[1], row[2]) for row in result]

    return datas

#print (funcionario_ponto(1))
#print (funcionario_oficinas(1))
print (listar_funcionarios())
#print (funcionario_contatos(1))