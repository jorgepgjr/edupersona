--
-- 1. CRIAÇÃO DA TABELA ALUNO
--
CREATE TABLE Aluno (
    ID_Aluno INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Sobrenome VARCHAR(100) NOT NULL,
    DataNascimento DATE,
    Email VARCHAR(150) UNIQUE NOT NULL,
    Telefone VARCHAR(20),
    Endereco VARCHAR(255)
);

--
-- 2. CRIAÇÃO DA TABELA PROFESSOR
--
CREATE TABLE Professor (
    ID_Professor INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(100) NOT NULL,
    Sobrenome VARCHAR(100) NOT NULL,
    Email VARCHAR(150) UNIQUE NOT NULL,
    Departamento VARCHAR(100)
);

--
-- 3. CRIAÇÃO DA TABELA DISCIPLINA
--
CREATE TABLE Disciplina (
    ID_Disciplina INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(150) NOT NULL,
    CodigoDisciplina VARCHAR(10) UNIQUE NOT NULL,
    CargaHoraria INT,
    Ementa TEXT
);

--
-- 4. CRIAÇÃO DA TABELA TURMA
-- (Relaciona Disciplina e Professor)
--
CREATE TABLE Turma (
    ID_Turma INT PRIMARY KEY AUTO_INCREMENT,
    ID_Disciplina INT NOT NULL,
    ID_Professor INT NOT NULL,
    Ano YEAR NOT NULL,
    Semestre INT NOT NULL,
    Local VARCHAR(50),
    Horario VARCHAR(100),
    
    -- Definição das Chaves Estrangeiras (FK)
    FOREIGN KEY (ID_Disciplina) REFERENCES Disciplina(ID_Disciplina),
    FOREIGN KEY (ID_Professor) REFERENCES Professor(ID_Professor)
);

--
-- 5. CRIAÇÃO DA TABELA MATRÍCULA
-- (Tabela de Junção Principal: Aluno e Turma. Armazena o resultado final.)
--
CREATE TABLE Matricula (
    ID_Matricula INT PRIMARY KEY AUTO_INCREMENT,
    ID_Aluno INT NOT NULL,
    ID_Turma INT NOT NULL,
    DataMatricula DATE NOT NULL,
    Status ENUM('Ativa', 'Concluída', 'Trancada', 'Reprovada') DEFAULT 'Ativa',
    NotaFinal DECIMAL(4, 2) DEFAULT NULL, -- Exemplo: 0.00 a 10.00
    Frequencia DECIMAL(5, 2) DEFAULT NULL, -- Exemplo: 0.00% a 100.00%
    
    -- Definição das Chaves Estrangeiras (FK)
    FOREIGN KEY (ID_Aluno) REFERENCES Aluno(ID_Aluno),
    FOREIGN KEY (ID_Turma) REFERENCES Turma(ID_Turma),
    
    -- Restrição de unicidade: um aluno só pode se matricular uma vez na mesma turma
    UNIQUE KEY (ID_Aluno, ID_Turma) 
);

--
-- 6. CRIAÇÃO DA TABELA AVALIAÇÃO
-- (Armazena as notas parciais. Relaciona-se com a Matrícula.)
--
CREATE TABLE Avaliacao (
    ID_Avaliacao INT PRIMARY KEY AUTO_INCREMENT,
    ID_Matricula INT NOT NULL,
    Tipo VARCHAR(50) NOT NULL, -- Ex: 'Prova 1', 'Trabalho Final', 'Participação'
    Peso DECIMAL(5, 2) NOT NULL, -- Peso percentual (ex: 40.00)
    Data DATE,
    ValorNota DECIMAL(4, 2), -- A nota obtida (ex: 8.50)
    
    -- Definição da Chave Estrangeira (FK)
    FOREIGN KEY (ID_Matricula) REFERENCES Matricula(ID_Matricula)
);