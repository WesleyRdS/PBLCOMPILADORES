import analizador_lexico

try:
    n_arquivos = int(input("(Somente numeros interios) - digite quantos arquivos de entrada você deseja ler: "))
    for i in range(0,n_arquivos):
        try:
            nome_aquivoE = str(input("Digite o nome do arquivo a ser lido a seguir(Com a extensão do arquivo): "))
            teste = analizador_lexico.analisador_lexico(nome_aquivoE)
            teste.E0()
            teste.E0()
            teste.E0()
            teste.E0()
            teste.checarErroComent()
            teste.checarErroCadeia()
            nome_aquivoS = str(input("Digite como você quer que seja o nome do arquivo de saida referente ao arquivo anterior(Com a extensão do arquivo): "))
            arquivo0 = open(nome_aquivoS, "a")
            for lin in teste.simbolos:
                arquivo0.write(str(lin[0]) + ", " + lin[1] + ", " + lin[2] + "\n")
            print(teste.simbolos)
        except:
            print("Arquivo não encontrado!!!")
except:
    print("Você não digitou um numero inteiro valido")


