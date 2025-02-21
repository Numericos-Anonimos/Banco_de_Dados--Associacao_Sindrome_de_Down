import sqlalchemy

# Criando a engine e conectando ao banco
engine = sqlalchemy.create_engine('sqlite:///ASIN.db', echo=False)

def listar_projetos():
    with engine.connect() as con:
        result = con.execute(sqlalchemy.text('SELECT * From Projetos'))
        columns = result.keys()

        projetos = [dict(zip(columns, row)) for row in result]
    
    return projetos

#print (listar_projetos())