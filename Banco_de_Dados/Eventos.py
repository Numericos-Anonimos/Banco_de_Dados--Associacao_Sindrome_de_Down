import sqlalchemy

# Criando a engine e conectando ao banco
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)

def listar_eventos():
    with engine.connect() as con:
        result = con.execute(sqlalchemy.text('SELECT * From Eventos'))
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

#print (listar_eventos())
#print (imagens_evento(2))