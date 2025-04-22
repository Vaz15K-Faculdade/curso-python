import pandas as pandinha

framezao = pandinha.read_csv("Aula 25-04-11/historico_escolar.csv")

frame_pessoas = framezao.groupby(["id_aluno", "nome_aluno"])[["nota", "faltas"]].mean()
frame_pessoas["aprovado"] = frame_pessoas["nota"] >= 5

frame_disciplinas = framezao.groupby(["ano_letivo", "disciplina"])[["nota", "faltas"]].mean()
frame_disciplinas["aprovado"] = frame_disciplinas["nota"] >= 5

indice_rep = frame_disciplinas.groupby(["ano_letivo", "disciplina"])["aprovado"].mean()

print("Médias por aluno:")
print(frame_pessoas)
print("\nMédias por disciplina:")
print(frame_disciplinas)
print("\nÍndice de aprovação:")
print(indice_rep)
