from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker

# Conectando ao banco de dados
# Aqui você deve substituir 'sqlite:///example.db' pela URL do seu banco de dados
engine = create_engine('sqlite:///example.db', echo=True)

# Criando uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Carregar metadados da tabela
metadata = MetaData()
metadata.reflect(bind=engine)


# Tabela que retorna as tuplas da tabela Atendidos:
def acessar_tabela_atendidos():
    # Acessar a tabela 'Atendidos'
    atendidos = Table('Atendidos', metadata, autoload_with=engine)

    result = session.execute(atendidos.select()).fetchall()

    return result

# Tabela que retorna as tuplas da tabela Funcionarios:
def acessar_funcionarios():
    funcionarios = Table('Funcionarios', metadata, autoload_with=engine)

    result = session.execute(funcionarios.select()).fetchall()

    return result

# Tabela que retorna as tuplas da tabela Oficinas:
def acessar_oficinas():
    oficinas = Table('Oficinas', metadata, autoload_with=engine)

    result = session.execute(oficinas.select()).fetchall()

    return result

# Tabela que retorna as tuplas da tabela Eventos:
def acessar_oficinas():
    eventos = Table('Eventos', metadata, autoload_with=engine)

    result = session.execute(eventos.select()).fetchall()

    return result


# Tabela que retorna as tuplas da tabela Projetos:
def acessar_oficinas():
    projetos = Table('Projetos', metadata, autoload_with=engine)

    result = session.execute(projetos.select()).fetchall()

    return result

