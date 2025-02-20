import sqlalchemy

# Criando a engine e conectando ao banco
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)


def listar_atendidos():
    # Conectando e executando a consulta
    with engine.connect() as con:
        result = con.execute(sqlalchemy.text('SELECT * FROM Atendidos'))
        # Obtendo os nomes das colunas
        columns = result.keys()

        # Transformando em lista de dicionários
        atendidos = [dict(zip(columns, row)) for row in result]
    
    return atendidos

def atendido_presencas(Cod_Atendido):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT P.Data
            FROM Atendido_Presencas P
            WHERE P.Cod_Atendido = :cod
        """)

        presenca = con.execute(query, {"cod": Cod_Atendido})

        # Retornando apenas uma lista de datas
        datas = [row[0] for row in presenca]

    return datas    

def atendido_contatos (Cod_Atendido):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT C.Telefone, C.Descricao
            FROM Contatos C
            JOIN Atendido_Contatos A ON A.Cod_Contato = C.Cod_Contato
            WHERE A.Cod_Atendido = :cod;
        """)

        telefones = con.execute(query, {"cod": Cod_Atendido})

        # Retornando uma lista de tuplas (Telefone, Descrição)
        telefone_list = [(row[0], row[1]) for row in telefones]

    return telefone_list

#print (atendido_contatos(3))
#print (listar_atendidos())
#print (atendido_presencas(2))