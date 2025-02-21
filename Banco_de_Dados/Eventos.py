import sqlalchemy

# Criando a engine e conectando ao banco
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)

def listar_eventos():
    with engine.connect() as con:
        result = con.execute(sqlalchemy.text('''
            SELECT
                e.Cod_Evento AS "Código",
                e.Nome AS "Evento",
                e.Data AS "Data",
                e.Observacoes AS "Observações",
                e.Quantidade_Externos AS "Externos",
                COUNT(DISTINCT a.Cod_Atendido) AS "Atendidos",
                COUNT(DISTINCT f.Cod_Funcionario) AS "Funcionários"
            FROM Eventos e
            LEFT JOIN Atendido_Eventos a ON a.Cod_Evento = e.Cod_Evento
            LEFT JOIN Funcionario_Eventos f ON f.Cod_Evento = e.Cod_Evento
            GROUP BY e.Cod_Evento;
        '''))
        columns = result.keys()

        eventos = [dict(zip(columns, row)) for row in result]
    
    return eventos

def imagens_evento (Cod_Evento):
    with engine.connect() as con:
        query = sqlalchemy.text("""
            SELECT f.Caminho
            FROM Fotos f
            JOIN Evento_Fotos e ON e.Cod_Foto = f.Cod_Foto
            WHERE e.Cod_Evento = :cod;
        """)

        fotos = con.execute(query, {"cod": Cod_Evento})
  
        fotos =  [row[0] for row in fotos]

    return fotos


#print(listar_eventos())