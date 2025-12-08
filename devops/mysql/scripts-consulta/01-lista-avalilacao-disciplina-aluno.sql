SELECT concat(al.Nome," ",al.Sobrenome) as name, 
 d.Nome as discipline,
 a.Tipo, 
 a.Peso, 
 a.ValorNota,
 m.Frequencia
from Avaliacao a	
INNER JOIN Matricula m on a.ID_Matricula = m.ID_Matricula
INNER JOIN Aluno al on al.ID_Aluno = m.ID_Aluno
INNER JOIN Turma t on t.ID_Turma = m.ID_Turma
INNER JOIN Disciplina d on d.ID_Disciplina= t.ID_Disciplina
WHERE al.ID_Aluno = 6-- and d.ID_Disciplina = 1
order by t.ID_Turma