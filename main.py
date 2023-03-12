import analizador_lexico


teste = analizador_lexico.analisador_lexico("teste.txt")
teste.E0()
teste.E0()
teste.E0()
teste.E0()
teste.checarErroComent()
arquivo0 = open("saida.txt", "a")
for lin in teste.simbolos:
    arquivo0.write(str(lin)+"\n")
print(teste.simbolos)
