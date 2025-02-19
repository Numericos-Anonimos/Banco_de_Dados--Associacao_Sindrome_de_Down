Chat, preciso que voce me ajude a criar um banco de dados no SQL. Vou te mandar as tabelas e algumas informações sobre elas. Sua tarefa é criar o banco de dados e as tabelas no SQL.

# Atendidos
Cod_Atendido: Chave primária, inteiro, autoincremento
Nome: Texto, 60 caracteres
Status: Categoria (Ativo, Inativo)
Data_Nascimento: Data
RG: Texto, 20 caracteres
CPF: Numero, 11 digitos
Convênio: Texto, 15 caracteres
Nome_Mãe: Texto, 60 caracteres
Nome_Pai: Texto, 60 caracteres (opcional)
Nome_Responsável: Texto, 60 caracteres (opcional)
Data_Cadastro: Data
CEP: Numero, 8 digitos
Numero: Numero, 6 digitos
Complemento: Texto, 30 caracteres
Observações: Texto, 255 caracteres

# Atendido_Presenças
Cod_Atendido: Chave primária estrangeira (Atendidos), inteiro
Data: Chave primária, Data

# Atendido_Contatos
Cod_Atendido: Chave primária estrangeira (Atendidos), inteiro
Cod_Contato: Chave primária estrangeira (Contatos), inteiro

# Atendido_Oficinas
Cod_Atendido: Chave primária estrangeira (Atendidos), inteiro
Cod_Oficina: Chave primária estrangeira (Oficinas), inteiro
Data_Inicio: Data
Data_Fim: Data, opcional

# Atendido_Fotos
Cod_Atendido: Chave primária estrangeira (Atendidos), inteiro
Cod_Foto: Chave primária estrangeira (Fotos), inteiro

# Atendido_Eventos
Cod_Atendido: Chave primária estrangeira (Atendidos), inteiro
Cod_Evento: Chave primária estrangeira (Eventos), inteiro

# Contatos
Cod_Contato: Chave primária, inteiro, autoincremento
Telefone: Numero, 11 digitos
Descricao: Texto, 100 caracteres


# Funcionários
Cod_Funcionario: Chave primária, inteiro, autoincremento
Nome: Texto, 60 caracteres
CPF: Numero, 11 digitos
CEP: Numero, 8 digitos
Numero: Numero, 6 digitos
Complemento: Texto, 30 caracteres
Observações: Texto, 255 caracteres
Salário: Float, 2 casas decimais (opcional)

# Funcionário_Presenças
Cod_Funcionario: Chave primária estrangeira (Funcionários), inteiro
Data: Chave primária, Data
Entrada: Hora
Saída: Hora

# Funcionário_Contatos
Cod_Funcionario: Chave primária estrangeira (Funcionários), inteiro
Cod_Contato: Chave primária estrangeira (Contatos), inteiro

# Funcionário_Fotos
Cod_Funcionario: Chave primária estrangeira (Funcionários), inteiro
Cod_Foto: Chave primária estrangeira (Fotos), inteiro

# Funcionário_Eventos
Cod_Funcionario: Chave primária estrangeira (Funcionários), inteiro
Cod_Evento: Chave primária estrangeira (Eventos), inteiro

# Fotos
Cod_Foto: Chave primária, inteiro, autoincremento
Caminho: Texto, 255 caracteres
Descrição: Texto, 255 caracteres

# Oficinas
Cod_Oficina: Chave primária, inteiro, autoincremento
Nome: Texto, 60 caracteres
Cod_Projeto: Chave estrangeira (Projetos), inteiro
Data_Inicio: Data
Data_Fim: Data, opcional
Dia_Semana: Categoria (Segunda, Terça, Quarta, Quinta, Sexta)
Hora_Inicio: Hora
Hora_Fim: Hora
Vagas: Inteiro
Cod_Funcionario: Chave estrangeira (Funcionários), inteiro, opcional
Valor_Hora: Float, 2 casas decimais
Descrição: Texto, 255 caracteres



# Oficina_Fotos
Cod_Oficina: Chave primária estrangeira (Oficinas), inteiro
Cod_Foto: Chave primária estrangeira (Fotos), inteiro

# Projetos
Cod_Projeto: Chave primária, inteiro, autoincremento
Nome: Texto, 60 caracteres
Verba: Float, 2 casas decimais
Data_Inicio: Data
Data_Fim: Data, opcional
Descrição: Texto, 255 caracteres

| Cod_Projetos | Nome | Verba | Data_Inicio | Data_Fim | Descrição |
|--------------|------|-------|-------------|----------|-----------|
| 1 | Verba Interna | NULL | 2010-01-01 | NULL | Oficinas financiadas com verba interna |
| 2 | SASC | 10000.00 | 2024-01-01 | 2024-12-31 | Oficinas de dança e cultura |
| 3 | Emenda Parlamentar | 5000.00 | 2024-01-01 | NULL | Oficinas financiadas pelo governo |
| 4 | Clinica | 20000.00 | 2024-01-01 | NULL | Oficinas de saúde |
| 5 | SASC | 15000.00 | 2025-01-01 | NULL | Renovação do projeto |





# Eventos
Cod_Evento: Chave primária, inteiro, autoincremento
Nome: Texto, 60 caracteres
Data: Data
Observações: Texto, 255 caracteres
Quantidade_Externos: Inteiro, opcional

# Evento_Fotos
Cod_Evento: Chave primária estrangeira (Eventos), inteiro
Cod_Foto: Chave primária estrangeira (Fotos), inteiro

# Criando Tabelas:
~~~SQL
-- Tabela de Projetos (base para Categorias)
CREATE TABLE Projetos (
  Cod_Projetos INTEGER PRIMARY KEY AUTOINCREMENT,
  Nome TEXT NOT NULL,
  Verba REAL NOT NULL,
  Data_Inicio DATE NOT NULL,
  Data_Fim DATE,
  Descricao TEXT
);

-- Tabela de Categorias (relacionada a Projetos)
CREATE TABLE Categorias (
  Cod_Categoria INTEGER PRIMARY KEY AUTOINCREMENT,
  Nome TEXT NOT NULL,
  Cod_Projetos INTEGER,
  FOREIGN KEY (Cod_Projetos) REFERENCES Projetos(Cod_Projetos)
);

-- Tabela de Contatos
CREATE TABLE Contatos (
  Cod_Contato INTEGER PRIMARY KEY AUTOINCREMENT,
  Telefone TEXT NOT NULL,
  Descricao TEXT
);

-- Tabela de Funcionários
CREATE TABLE Funcionarios (
  Cod_Funcionario INTEGER PRIMARY KEY AUTOINCREMENT,
  Nome TEXT NOT NULL,
  CPF TEXT NOT NULL,
  CEP TEXT NOT NULL,
  Numero INTEGER NOT NULL,
  Complemento TEXT,
  Observacoes TEXT,
  Salario REAL
);

-- Tabela de Fotos
CREATE TABLE Fotos (
  Cod_Foto INTEGER PRIMARY KEY AUTOINCREMENT,
  Caminho TEXT NOT NULL,
  Descricao TEXT
);

-- Tabela de Atendidos
CREATE TABLE Atendidos (
  Cod_Atendido INTEGER PRIMARY KEY AUTOINCREMENT,
  Nome TEXT NOT NULL,
  Status TEXT NOT NULL CHECK (Status IN ('Ativo','Inativo')),
  Data_Nascimento DATE NOT NULL,
  RG TEXT NOT NULL,
  CPF TEXT NOT NULL,
  Convenio TEXT NOT NULL,
  Nome_Mae TEXT NOT NULL,
  Nome_Pai TEXT,
  Nome_Responsavel TEXT,
  Data_Cadastro DATE NOT NULL,
  CEP TEXT NOT NULL,
  Numero INTEGER NOT NULL,
  Complemento TEXT,
  Observacoes TEXT
);

-- Tabela de Eventos
CREATE TABLE Eventos (
  Cod_Evento INTEGER PRIMARY KEY AUTOINCREMENT,
  Nome TEXT NOT NULL,
  Data DATE NOT NULL,
  Observacoes TEXT,
  Quantidade_Externos INTEGER
);

-- Tabela de Oficinas
CREATE TABLE Oficinas (
  Cod_Oficina INTEGER PRIMARY KEY AUTOINCREMENT,
  Nome TEXT NOT NULL,
  Cod_Categoria INTEGER NOT NULL,
  Data_Inicio DATE NOT NULL,
  Data_Fim DATE,
  Dia_Semana TEXT NOT NULL CHECK (Dia_Semana IN ('Segunda','Terça','Quarta','Quinta','Sexta')),
  Hora_Inicio TIME NOT NULL,
  Hora_Fim TIME NOT NULL,
  Vagas INTEGER NOT NULL,
  Cod_Funcionario INTEGER,
  Valor_Hora REAL NOT NULL,
  Descricao TEXT,
  FOREIGN KEY (Cod_Categoria) REFERENCES Categorias(Cod_Categoria),
  FOREIGN KEY (Cod_Funcionario) REFERENCES Funcionarios(Cod_Funcionario)
);

-- Tabelas de relacionamento

-- Atendido_Presencas
CREATE TABLE Atendido_Presencas (
  Cod_Atendido INTEGER NOT NULL,
  Data DATE NOT NULL,
  PRIMARY KEY (Cod_Atendido, Data),
  FOREIGN KEY (Cod_Atendido) REFERENCES Atendidos(Cod_Atendido)
);

-- Atendido_Contatos
CREATE TABLE Atendido_Contatos (
  Cod_Atendido INTEGER NOT NULL,
  Cod_Contato INTEGER NOT NULL,
  PRIMARY KEY (Cod_Atendido, Cod_Contato),
  FOREIGN KEY (Cod_Atendido) REFERENCES Atendidos(Cod_Atendido),
  FOREIGN KEY (Cod_Contato) REFERENCES Contatos(Cod_Contato)
);

-- Atendido_Oficinas
CREATE TABLE Atendido_Oficinas (
  Cod_Atendido INTEGER NOT NULL,
  Cod_Oficina INTEGER NOT NULL,
  Data_Inicio DATE NOT NULL,
  Data_Fim DATE,
  PRIMARY KEY (Cod_Atendido, Cod_Oficina),
  FOREIGN KEY (Cod_Atendido) REFERENCES Atendidos(Cod_Atendido),
  FOREIGN KEY (Cod_Oficina) REFERENCES Oficinas(Cod_Oficina)
);

-- Atendido_Fotos
CREATE TABLE Atendido_Fotos (
  Cod_Atendido INTEGER NOT NULL,
  Cod_Foto INTEGER NOT NULL,
  PRIMARY KEY (Cod_Atendido, Cod_Foto),
  FOREIGN KEY (Cod_Atendido) REFERENCES Atendidos(Cod_Atendido),
  FOREIGN KEY (Cod_Foto) REFERENCES Fotos(Cod_Foto)
);

-- Atendido_Eventos
CREATE TABLE Atendido_Eventos (
  Cod_Atendido INTEGER NOT NULL,
  Cod_Evento INTEGER NOT NULL,
  PRIMARY KEY (Cod_Atendido, Cod_Evento),
  FOREIGN KEY (Cod_Atendido) REFERENCES Atendidos(Cod_Atendido),
  FOREIGN KEY (Cod_Evento) REFERENCES Eventos(Cod_Evento)
);

-- Funcionario_Presencas
CREATE TABLE Funcionario_Presencas (
  Cod_Funcionario INTEGER NOT NULL,
  Data DATE NOT NULL,
  Entrada TIME NOT NULL,
  Saida TIME NOT NULL,
  PRIMARY KEY (Cod_Funcionario, Data),
  FOREIGN KEY (Cod_Funcionario) REFERENCES Funcionarios(Cod_Funcionario)
);

-- Funcionario_Contatos
CREATE TABLE Funcionario_Contatos (
  Cod_Funcionario INTEGER NOT NULL,
  Cod_Contato INTEGER NOT NULL,
  PRIMARY KEY (Cod_Funcionario, Cod_Contato),
  FOREIGN KEY (Cod_Funcionario) REFERENCES Funcionarios(Cod_Funcionario),
  FOREIGN KEY (Cod_Contato) REFERENCES Contatos(Cod_Contato)
);

-- Funcionario_Fotos
CREATE TABLE Funcionario_Fotos (
  Cod_Funcionario INTEGER NOT NULL,
  Cod_Foto INTEGER NOT NULL,
  PRIMARY KEY (Cod_Funcionario, Cod_Foto),
  FOREIGN KEY (Cod_Funcionario) REFERENCES Funcionarios(Cod_Funcionario),
  FOREIGN KEY (Cod_Foto) REFERENCES Fotos(Cod_Foto)
);

-- Funcionario_Eventos
CREATE TABLE Funcionario_Eventos (
  Cod_Funcionario INTEGER NOT NULL,
  Cod_Evento INTEGER NOT NULL,
  PRIMARY KEY (Cod_Funcionario, Cod_Evento),
  FOREIGN KEY (Cod_Funcionario) REFERENCES Funcionarios(Cod_Funcionario),
  FOREIGN KEY (Cod_Evento) REFERENCES Eventos(Cod_Evento)
);

-- Oficina_Fotos
CREATE TABLE Oficina_Fotos (
  Cod_Oficina INTEGER NOT NULL,
  Cod_Foto INTEGER NOT NULL,
  PRIMARY KEY (Cod_Oficina, Cod_Foto),
  FOREIGN KEY (Cod_Oficina) REFERENCES Oficinas(Cod_Oficina),
  FOREIGN KEY (Cod_Foto) REFERENCES Fotos(Cod_Foto)
);

-- Evento_Fotos
CREATE TABLE Evento_Fotos (
  Cod_Evento INTEGER NOT NULL,
  Cod_Foto INTEGER NOT NULL,
  PRIMARY KEY (Cod_Evento, Cod_Foto),
  FOREIGN KEY (Cod_Evento) REFERENCES Eventos(Cod_Evento),
  FOREIGN KEY (Cod_Foto) REFERENCES Fotos(Cod_Foto)
);
~~~

# Dados
~~~SQL
-- Inserindo dados na tabela Projetos
INSERT INTO Projetos (Nome, Verba, Data_Inicio, Data_Fim, Descricao) VALUES
('Verba Interna', NULL, '2010-01-01', NULL, 'Oficinas financiadas com verba interna'),
('SASC', 10000.00, '2024-01-01', '2024-12-31', 'Oficinas de dança e cultura'),
('Emenda Parlamentar', 5000.00, '2024-01-01', NULL, 'Oficinas financiadas pelo governo'),
('Clinica', 20000.00, '2024-01-01', NULL, 'Oficinas de saúde'),
('SASC', 15000.00, '2025-01-01', NULL, 'Renovação do projeto');

-- Inserindo dados na tabela Categorias
INSERT INTO Categorias (Nome, Cod_Projetos) VALUES
('Informática', 1),
('Estimulação Cognitiva', 1),
('Cultura', 2),
('Danças e Ritmos', 2),
('Atividades Físicas', 2),
('Danças e Ritmos', 3),
('Estimulação Cognitiva', 3),
('Terapia', 4),
('Pedagogia', 4),
('Danças e Ritmos', 5);
('Cultura', 5),
('Danças e Ritmos', 5),
('Atividades Físicas', 5),

-- Inserindo dados na tabela Atendidos
INSERT INTO Atendidos (Nome, Status, Data_Nascimento, RG, CPF, Convenio, Nome_Mae, Nome_Pai, Nome_Responsavel, Data_Cadastro, CEP, Numero, Complemento, Observacoes) VALUES
('Alice Ferreira', 'Ativo', '1992-05-12', 'MG1234567', '12345678901', 'Unimed', 'Mariana Ferreira', 'Carlos Ferreira', NULL, '2023-01-15', '30140000', 100, 'Apto 101', 'Sem observações'),
('Bruno Souza', 'Ativo', '1988-08-22', 'SP2345678', '23456789012', 'Amil', 'Lucia Souza', 'Roberto Souza', NULL, '2023-02-10', '04001000', 200, 'Casa', 'Alergia a penicilina'),
('Carla Mendes', 'Inativo', '1995-11-03', 'RJ3456789', '34567890123', 'Bradesco', 'Sandra Mendes', NULL, 'Fernando Mendes', '2023-03-05', '20040000', 300, 'Sem complemento', 'Histórico de atendimento irregular'),
('Daniel Costa', 'Ativo', '1980-07-18', 'PR4567890', '45678901234', 'SulAmérica', 'Patricia Costa', 'Antonio Costa', NULL, '2023-04-20', '80010000', 400, 'Apto 202', 'Sem observações'),
('Elisa Pereira', 'Ativo', '1978-03-30', 'RS5678901', '56789012345', 'Hapvida', 'Rita Pereira', 'Carlos Pereira', NULL, '2023-05-15', '90020000', 500, 'Casa', 'Sem observações'),
('Fernando Lima', 'Ativo', '1985-12-25', 'SC6789012', '67890123456', 'Unimed', 'Sandra Lima', 'Miguel Lima', NULL, '2023-06-10', '70030000', 600, 'Apto 303', 'Pendências documentais'),
('Gabriela Santos', 'Inativo', '1990-04-05', 'BA7890123', '78901234567', 'Amil', 'Eva Santos', 'João Santos', NULL, '2023-07-25', '60040000', 700, 'Casa', 'Sem observações'),
('Henrique Almeida', 'Ativo', '1993-09-17', 'CE8901234', '89012345678', 'Bradesco', 'Sonia Almeida', NULL, 'Fernando Almeida', '2023-08-30', '50050000', 800, 'Apto 404', 'Sem observações'),
('Isabela Rocha', 'Ativo', '1987-02-11', 'PE9012345', '90123456789', 'SulAmérica', 'Marta Rocha', 'José Rocha', NULL, '2023-09-12', '40060000', 900, 'Casa', 'Sem observações'),
('João Martins', 'Ativo', '1999-06-21', 'GO0123456', '01234567890', 'Hapvida', 'Lucia Martins', 'Ricardo Martins', NULL, '2023-10-05', '30070000', 1000, 'Apto 505', 'Sem observações'),
('Karina Silva', 'Ativo', '1996-12-30', 'MG1122334', '11223344556', 'Unimed', 'Maria Silva', 'José Silva', NULL, '2023-11-20', '20080000', 1100, 'Casa', 'Necessita acompanhamento regular');

