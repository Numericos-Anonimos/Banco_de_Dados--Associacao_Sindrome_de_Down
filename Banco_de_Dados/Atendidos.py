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

def atendidos_oficina (Cod_Atendido):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT o.Dia_Semana, o.Hora_Inicio, o.Hora_Fim, o.Nome
            FROM Oficinas o
            JOIN Atendido_Oficinas A ON A.Cod_Oficina = o.Cod_Oficina
            WHERE A.Cod_Atendido = :cod;
        """)

        oficinas = con.execute(query, {"cod": Cod_Atendido})

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


def atendido_foto(Cod_Atendido):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT f.Caminho
            FROM Fotos f
            JOIN Atendido_Fotos A ON A.Cod_Foto = f.Cod_Foto
            WHERE A.Cod_Atendido = :cod;
        """)

        fotos = con.execute(query, {"cod": Cod_Atendido})

        
        fotos =  [row[0] for row in fotos]

    return fotos

def atendido_eventos (Cod_Atendido):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT e.nome, e.data, e.Observacoes
            FROM Eventos e
            JOIN Atendido_Eventos A ON A.Cod_Evento = e.Cod_Evento
            WHERE A.Cod_Atendido = :cod;
        """)

        eventos = con.execute(query, {"cod": Cod_Atendido})

        # Retornando uma lista de tuplas (Telefone, Descrição)
        eventos = [(row[0], row[1], row[2]) for row in eventos]

    return eventos


print(atendidos_oficina(1))