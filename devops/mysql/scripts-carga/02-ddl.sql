--
-- CARGA NA TABELA ALUNO
--
INSERT INTO Aluno (Nome, Sobrenome, DataNascimento, Email, Telefone, Endereco) VALUES
('João', 'Silva', '2000-05-15', 'joao.silva@email.com', '79988881234', 'Rua A, 101'),
('Maria', 'Santos', '1999-08-22', 'maria.santos@email.com', '79977775678', 'Av. B, 202'),
('Pedro', 'Oliveira', '2001-01-10', 'pedro.oliver@email.com', '79966669012', 'Trav. C, 303'),
('Ana', 'Souza', '2002-04-01', 'ana.souza@email.com', '79955553456', 'Rua D, 404');


--
-- CARGA NA TABELA PROFESSOR
--
INSERT INTO Professor (Nome, Sobrenome, Email, Departamento) VALUES
('Carlos', 'Ferreira', 'carlos.ferreira@inst.com', 'Ciência da Computação'),
('Juliana', 'Almeida', 'juliana.almeida@inst.com', 'Matemática');


--
-- CARGA NA TABELA DISCIPLINA
--
INSERT INTO Disciplina (Nome, CodigoDisciplina, CargaHoraria, Ementa) VALUES
('Banco de Dados I', 'BDI-101', 60, 'Modelagem e Linguagem SQL.'),
('Algoritmos e Estruturas de Dados', 'AED-205', 80, 'Implementação de estruturas de dados e algoritmos de busca/ordenação.');


--
-- CARGA NA TABELA TURMA
--
INSERT INTO Turma (ID_Disciplina, ID_Professor, Ano, Semestre, Local, Horario) VALUES
(1, 1, 2025, 1, 'Sala B10', 'Segunda e Quarta - 19:00h'),
(2, 2, 2025, 1, 'Lab 2', 'Terça e Quinta - 14:00h');


--
-- CARGA NA TABELA MATRÍCULA
--
INSERT INTO Matricula (ID_Aluno, ID_Turma, DataMatricula, Status, NotaFinal, Frequencia) VALUES
(1, 1, '2025-02-10', 'Concluída', 8.50, 90.00), -- João em BDI-101
(2, 1, '2025-02-10', 'Ativa', NULL, NULL), -- Maria em BDI-101
(3, 2, '2025-02-12', 'Ativa', NULL, 85.00), -- Pedro em AED-205
(4, 2, '2025-02-12', 'Reprovada', 4.50, 70.00); -- Ana em AED-205

--
-- CARGA NA TABELA AVALIAÇÃO
--
INSERT INTO Avaliacao (ID_Matricula, Tipo, Peso, Data, ValorNota) VALUES
-- Notas de João (Matrícula ID 1) em BDI-101
(1, 'Prova 1', 40.00, '2025-04-15', 7.00),
(1, 'Trabalho Final', 60.00, '2025-06-20', 9.50),

-- Notas de Maria (Matrícula ID 2) em BDI-101
(2, 'Prova 1', 40.00, '2025-04-15', 6.00),

-- Notas de Pedro (Matrícula ID 3) em AED-205
(3, 'Trabalho 1', 30.00, '2025-05-01', 9.00),

-- Notas de Ana (Matrícula ID 4) em AED-205 - Reprovada
(4, 'Prova 1', 50.00, '2025-04-20', 5.00),
(4, 'Prova 2', 50.00, '2025-06-01', 4.00);

--
-- CARGA NA TABELA ALUNO (Mais 4 alunos)
--
INSERT INTO Aluno (Nome, Sobrenome, DataNascimento, Email, Telefone, Endereco) VALUES
('Felipe', 'Costa', '2000-11-05', 'felipe.costa@email.com', '79944440001', 'Rua E, 505'),
('Mariana', 'Pereira', '1998-03-17', 'mariana.pereira@email.com', '79933330002', 'Av. F, 606'),
('Guilherme', 'Rodrigues', '2003-09-28', 'gui.rodrigues@email.com', '79922220003', 'Rua G, 707'),
('Laura', 'Martins', '2001-06-19', 'laura.martins@email.com', '79911110004', 'Trav. H, 808');
-- IDs de 1 a 8

--
-- CARGA NA TABELA PROFESSOR (Mais 1 professor)
--
INSERT INTO Professor (Nome, Sobrenome, Email, Departamento) VALUES
('Patrícia', 'Gomes', 'patricia.gomes@inst.com', 'Engenharia de Software');
-- IDs de 1 a 3

--
-- CARGA NA TABELA DISCIPLINA (Mais 1 disciplina)
--
INSERT INTO Disciplina (Nome, CodigoDisciplina, CargaHoraria, Ementa) VALUES
('Programação Orientada a Objetos', 'POO-302', 60, 'Conceitos avançados de POO com Java/C#.');
-- IDs de 1 a 3

--
-- CARGA NA TABELA TURMA (Mais 1 Turma)
--
INSERT INTO Turma (ID_Disciplina, ID_Professor, Ano, Semestre, Local, Horario) VALUES
(3, 3, 2025, 1, 'Sala C15', 'Segunda e Quarta - 17:00h');
-- IDs de 1 a 3

--
-- CARGA NA TABELA MATRÍCULA (Mais 6 Matrículas)
--
INSERT INTO Matricula (ID_Aluno, ID_Turma, DataMatricula, Status, NotaFinal, Frequencia) VALUES
(5, 1, '2025-02-10', 'Ativa', NULL, 95.00),         -- Felipe em BDI-101
(6, 1, '2025-02-10', 'Reprovada', 3.20, 92.00),    -- Mariana em BDI-101
(7, 2, '2025-02-12', 'Concluída', 9.80, 100.00),   -- Guilherme em AED-205
(8, 2, '2025-02-12', 'Trancada', NULL, 60.00),     -- Laura em AED-205 (Trancada)
(5, 3, '2025-02-15', 'Ativa', NULL, 90.00),         -- Felipe em POO-302
(6, 3, '2025-02-15', 'Concluída', 7.00, 78.00);    -- Mariana em POO-302
-- IDs de Matrícula de 5 a 10 (continuando os 4 anteriores)

--
-- CARGA NA TABELA AVALIAÇÃO (Notas adicionais)
--
INSERT INTO Avaliacao (ID_Matricula, Tipo, Peso, Data, ValorNota) VALUES
-- Notas de Mariana (Matrícula ID 6) em BDI-101 - Reprovada
(6, 'Prova 1', 40.00, '2025-04-15', 3.00),
(6, 'Trabalho Final', 60.00, '2025-06-20', 3.30), -- Média (3.0*0.4 + 3.3*0.6) = 3.18 (arredondado para 3.20 na Matricula)

-- Notas de Guilherme (Matrícula ID 7) em AED-205 - Aprovado
(7, 'Projeto 1', 50.00, '2025-05-01', 10.00),
(7, 'Prova Final', 50.00, '2025-06-25', 9.60), -- Média = 9.80

-- Notas de Felipe (Matrícula ID 5) em BDI-101 - Ativa
(5, 'Quiz 1', 10.00, '2025-03-01', 8.00),
(5, 'Trabalho Intermediário', 30.00, '2025-05-05', 7.50),

-- Notas de Felipe (Matrícula ID 9) em POO-302 - Ativa
(9, 'Exercício POO', 20.00, '2025-04-10', 9.00),

-- Notas de Mariana (Matrícula ID 10) em POO-302 - Aprovada
(10, 'Prova POO', 60.00, '2025-06-10', 6.50),
(10, 'Projeto POO', 40.00, '2025-06-25', 7.75); -- Média = 7.00