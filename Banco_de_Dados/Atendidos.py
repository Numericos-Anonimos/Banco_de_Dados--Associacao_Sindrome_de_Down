import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)
metadata = sqlalchemy.MetaData()
metadata.create_all(engine)
table = sqlalchemy.Table('ASIN', metadata)

# Conectando ao banco e executando a consulta
with engine.connect() as con:
    result = con.execute(sqlalchemy.text('SELECT * FROM Atendidos'))
    # Exibindo os resultados
    for row in result:
        print(row)
