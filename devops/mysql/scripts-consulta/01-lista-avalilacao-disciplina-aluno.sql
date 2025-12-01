SELECT d.Nome, a.Tipo, a.Peso, a.ValorNota, al.Nome, al.Sobrenome, m.Status, m.NotaFinal, m.Frequencia from Avaliacao a
INNER JOIN Matricula m on a.ID_Matricula = m.ID_Matricula
INNER JOIN Aluno al on al.ID_Aluno = al.ID_Aluno
INNER JOIN Turma t on t.ID_Turma = m.ID_Turma
INNER JOIN Disciplina d on d.ID_Disciplina= t.ID_Disciplina