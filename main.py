class analisador_lexico:

    def __init__(self, arquivo):
        self.LinhaAtual = [] #vetor com todas as letras da linha lida
        self.linha_lida = 0 #numero da linha lida
        self.simboloAtual = '' #simbolo lidos(junção das letras)
        self.reservada = [] #vetor que retorna o simbolo e a linha lida
        self.linha = '' #linha lida
        self.arq = arquivo #arquivo lido
        self.delimI = ""
        self.delimF = ""
        self.alfabeto = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.digito = set("0123456789")
        self.inicioCadeia = []
        self.fimCadeia = []
        self.simbolos = [] #tabela com simbolos lido
        self._arquivo = open(arquivo, "r", encoding="UTF-8") #abertura de arquivo no modo leitura

    def verificarSubset(self,simbolo): #função que recebe um simbolo qualquer
        simb = set((simbolo)) #comando para setar esse simbolo como um conjunto
        if(simb.issubset(self.digito)): #verifica se esse simbolo faz parte do conjunto de digitos definidos
            return True
        elif(simb.issubset(self.alfabeto)):#se não verifica se faz parte do conjunto de letras
            return "letra"
        else: #caso nenhuma das duas se prove verdadeiro retorna falso
            return False

    def pularProximoSimbolo(self):
        if len(self.linha) >= 1:
            while self.linha[0] == " ": #verifica se o proximo termo é um espaço em branco
                self.linha.pop(0) #enquanto o termo lido no vetor for um espaço em branco esse espaço é descartado

    def resetSimbAtual(self):
        self.simboloAtual = '' #apaga o simbolo

    def resetReservada(self):
        self.reservada = [] #apaga a palavra reservada atual do vetor

    def attlinha(self):
        self.linha_lida += 1 # atualiza o numero da linha lida

    def estadoAtual(self):
        return self.estado
#função para ler linha do arquivo
    def lerLinha(self):
        self.linhaAtual = self._arquivo.readline()
        self.linha = list(self.linhaAtual) #transfora a linha lida em uma lista
        self.attlinha() #atualiza o numero da linha que foi lida
        return self.linha #retorna a linha lida

#Função que ignora linha em branco.
    def ignoraBranco(self):
        if len(self.linha) >= 1: #verifica se o vetor linha esta vazio
            self.E1() #Se sim, manda para o estado de analise do simbolo
        else:
            self.E0() #Se não manda para o estado de leitura para ler proxima linha

#estado de leitura de arquivo
    def E0(self):
        self.lerLinha()
        if(len(self.linha) >= 1): #se a linha não esta vazia manda para o estado de analise de simbolo
            self.E1()

#estado de comentario(Só é possivel chegar nesse estado a partir de um estado anterior do analisador de simbolos E1)
    def coment_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]: #lendo primeira letra da pilha
                case "/": #Neste ponto ele esta lendo a segunda / depois de ler a primeira então identifica como comentario
                    self.resetSimbAtual() #apaga o simbolo guardado ignorando a linha por ser comentario
                    self.E0 #manda ler a proxima linha
                #Os dois casos a seguir é se o termo da pilha for vazio ou quebra de linha
                case " ":
                    self.div_state() #ele identifica como uma divisão e manda para o estado que trata disso
                case "\n":
                    self.div_state()
                # aqui ele identificou um comentario em bloco então manda para o estado do operado de multiplicação
                case "*":
                    self.blockComent_State() #esse estado É onde verifica o comentario em bloco

    def blockComent_State(self):#estado que so chega a partir do estado de comentario(previamente foi lido uma /)
        if len(self.linha) >= 1: #Verificando se a algo na linha
            match self.linha[0]:#A partir daqui ele para de guardar as informações até o comentario ser fechado
                case "*": #identifica o segundo item que correspnde ao comentario em bloco
                    self.simboloAtual += self.linha.pop(0)#adiciona o asterisco a simbolo
                    print(self.simboloAtual)
                    if self.simboloAtual == "/*":
                        self.inicioCadeia.append(self.simboloAtual)
                        self.percorrerCadeias()
                        if self.delimI == "CoMF" or self.delimF == "CoMF":
                            self.reservada.append(self.linha_lida)
                            self.reservada.append(self.delimI)
                            self.reservada.append(self.simboloAtual)
                            self.simbolos.append(self.reservada)
                            self.resetReservada()
                    self.blockComent_State() #volta para o estado inicial

                case "/": #identificou o fim do comentario em bloco
                    self.simboloAtual += self.linha.pop(0) #adiciona ao simbolo atualmente lindo
                    if self.simboloAtual == "*/": #verifica o fechamento do comentario em bloco
                        self.fimCadeia.append(self.simboloAtual)
                        self.percorrerCadeias()
                        if self.delimI == "CoMF" or self.delimF == "CoMF":
                            self.reservada.append(self.linha_lida)
                            self.reservada.append(self.delimI)
                            self.reservada.append(self.simboloAtual)
                            self.simbolos.append(self.reservada)
                            self.resetReservada()
                        self.resetSimbAtual() # reseta o simbolo para identificar o proximo
                        self.E1() #volta a fazer a analize de simbolos normalmente
                    else: # se não identificar continua a / apos o * continua a procurar
                        self.resetSimbAtual()
                        self.linha.pop(0) #elimina o que ja foi lido
                        self.blockComent_State()

                case "\n":#chegou a quebra de linha sem identificar o fechamento do comentario
                    self.resetSimbAtual()
                    self.linha = self.lerLinha() #ler a proxima linha
                    self.blockComent_State()

                case _:
                    self.linha.pop(0)
                    self.resetSimbAtual()
                    self.blockComent_State()

    def percorrerCadeias(self):
        if len(self.inicioCadeia) >= 1 or len(self.fimCadeia) >=1:
            for i in range( 0, len(self.inicioCadeia)-1):
                for j in range( 0, len(self.fimCadeia)-1):
                    if self.inicioCadeia[i] == "/*":
                        if self.fimCadeia[j] == "*/":
                            self.inicioCadeia.pop(i)
                            self.fimCadeia.pop(j)
                    elif self.inicioCadeia[i] == "(":
                        if self.fimCadeia[j] == ")":
                            self.inicioCadeia.pop(i)
                            self.fimCadeia.pop(j)


            for k in range(0, len(self.fimCadeia)):
                if len(self.fimCadeia) >= 1:
                    if self.fimCadeia[k] != "*/":
                        self.delimF = "CoMF"
                    else:
                        self.delimF ="TMF"
            for l in range(0, len(self.inicioCadeia)):
                if len(self.inicioCadeia) >= 1:
                    if self.inicioCadeia[l] != "/*":
                        self.delimI = "CoMF"
                    else:
                        self.delimI ="TMF"

        self.inicioCadeia = []
        self.fimCadeia = []


#operadores aritimeticos
    def div_state(self): #estado depois da / ser lida no E1(Divisão)
        if len(self.linha) >= 1:
            match self.linha[0]: #verifica proxima letra da pilha
                #caso da quebra de linha
                case "\n":
                    if (self.simboloAtual != ''): #verifica se o simbolo realmente existe
                        #adiciona no vetor o numero da linha, o simbolo lido e seu tipo
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART") #atribuiu o valor que representa a divisão
                        self.reservada.append(self.simboloAtual)
                        #adiciona a tabela de simbolos
                        self.simbolos.append(self.reservada)
                    self.resetReservada() #apaga os dados lidos do vetor temporario
                    self.resetSimbAtual() #apaga o simbolo temporario
                    self.E0() #manda ler uma proxima linha

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _: #para todos os outros casos ele repete o processo mas sem mandar ler a proxima linha
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo() #ele continua na mesma e vai para o proximo simbolo a ser lido
                    self.ignoraBranco() #E aqui ele vai chegar se ainda tem alguma coisa e caso tenha ele manda pro estado E1

    def plus_state(self): #estado de soma. Após o operador + ser lido no E1
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "\n": #no caso da quebra de linha
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART") # o valor soma sera atribuido ao simbolo
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0() #E uma nova linha sera lida

                case "+": #Para o caso especial do simbolo lido após o primeiro + for ele mesmo
                    self.simboloAtual += self.linha.pop(0) #o simbolo é retirado da pilha e incrementado no simbolo
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART") # Em vez de ser identificado como soma vai ser um incremento
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _: #para todos os outros caso o valor atribuido sera soma
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo() #E a leitura dos simbolos da linha prossiguira
                    self.ignoraBranco()

    def mini_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case "-":
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def mult_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "/":
                    self.blockComent_State()
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("ART")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

#Operadores lógicos:
    def negate_State(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case "=":
                    self.simboloAtual += self.linha.pop(0);
                    self.equals_State()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def and_State(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "&":
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def or_State(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "|":
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()


                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()


                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def equals_State(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "=":
                    self.simboloAtual += self.linha.pop(0);
                    self.equals_State()
                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "!=":
                                self.reservada.append("REL")
                            case ">=":
                                self.reservada.append("REL")
                            case "<=":
                                self.reservada.append("REL")
                            case "==":
                                self.reservada.append("REL")
                            case _:
                                self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()


                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "!=":
                                self.reservada.append("REL")
                            case ">=":
                                self.reservada.append("REL")
                            case "<=":
                                self.reservada.append("REL")
                            case "==":
                                self.reservada.append("REL")
                            case _:
                                self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def maiorQ_State(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "=":
                    self.simboloAtual += self.linha.pop(0);
                    self.equals_State()
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def menorQ_State(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "=":
                    self.simboloAtual += self.linha.pop(0);
                    self.equals_State()
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("REL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def colchetes_state(self):
        if len(self.linha) >= 1:
            if self.simboloAtual == "[":
                self.inicioCadeia.append(self.simboloAtual)
            elif self.simboloAtual == "]":
                self.fimCadeia.append(self.simboloAtual)
            else:
                self.resetSimbAtual()
            match self.linha[0]:
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def parenteses_state(self):
        if len(self.linha) >= 1:
            if self.simboloAtual == "(":
                self.inicioCadeia.append(self.simboloAtual)
            elif self.simboloAtual == ")":
                self.fimCadeia.append(self.simboloAtual)
            else:
                self.resetSimbAtual()
            match self.linha[0]:
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

    def chaves_state(self):
        if len(self.linha) >= 1:
            if self.simboloAtual == "{":
                self.inicioCadeia.append(self.simboloAtual)
            elif self.simboloAtual == "}":
                self.fimCadeia.append(self.simboloAtual)
            else:
                self.resetSimbAtual()
            match self.linha[0]:
                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()


    def string_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case '"':
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("CAC")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    if len(self.linha) >= 1:
                        match self.linha[0]:
                            case " ":
                                self.pularProximoSimbolo()
                                self.ignoraBranco()
                                self.string_state()
                            case "\n":
                                self.lerLinha()
                                if len(self.linha) >= 1:
                                    self.simboloAtual += self.linha.pop(0)
                                self.string_state()

                case "\n":
                    self.lerLinha()
                    if len(self.linha) >= 1:
                        self.simboloAtual += self.linha.pop(0)
                    self.string_state()


                case _:
                    self.simboloAtual += self.linha.pop(0)
                    self.string_state()


    def E1(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case '"':
                    self.simboloAtual += self.linha.pop(0)
                    self.string_state()
                case ".":
                    self.ponto_state()
                case ";":
                    self.ponto_state()
                case ",":
                    self.ponto_state()
                case "(":
                    self.simboloAtual += self.linha.pop(0)
                    self.chaves_state()
                case ")":
                    self.simboloAtual += self.linha.pop(0)
                    self.parenteses_state()
                case "{":
                    self.simboloAtual += self.linha.pop(0)
                    self.chaves_state()
                case "}":
                    self.simboloAtual += self.linha.pop(0)
                    self.chaves_state()
                case "[":
                    self.simboloAtual += self.linha.pop(0)
                    self.colchetes_state()
                case "]":
                    self.simboloAtual += self.linha.pop(0)
                    self.colchetes_state()
                case "_":
                    self.simboloAtual += self.linha.pop(0)
                    self.erro_state()
                case ">":
                    self.simboloAtual += self.linha.pop(0)
                    self.maiorQ_State()
                case "<":
                    self.simboloAtual += self.linha.pop(0)
                    self.menorQ_State()
                case "=":
                    self.simboloAtual += self.linha.pop(0)
                    self.equals_State()
                case "|":
                    self.simboloAtual += self.linha.pop(0)
                    self.or_State()

                case "&":
                    self.simboloAtual += self.linha.pop(0)
                    self.and_State()

                case "!":
                    self.simboloAtual += self.linha.pop(0);
                    self.negate_State()

                case "/":
                    self.simboloAtual += self.linha.pop(0)
                    self.coment_state()

                case "+":
                    self.simboloAtual += self.linha.pop(0)
                    self.plus_state()

                case "-":
                    self.simboloAtual += self.linha.pop(0)
                    self.mini_state()

                case "*":
                    self.simboloAtual += self.linha.pop(0)
                    self.mult_state()

                case "i":
                    self.simboloAtual += self.linha.pop(0)
                    self.i_state()

                case "v":
                    self.simboloAtual += self.linha.pop(0)
                    self.v_state()

                case "c":
                    self.simboloAtual += self.linha.pop(0)
                    self.c_state()

                case "s":
                    self.simboloAtual += self.linha.pop(0)
                    self.s_state()

                case "p":
                    self.simboloAtual += self.linha.pop(0)
                    self.p_state()

                case "f":
                    self.simboloAtual += self.linha.pop(0)
                    self.f_state()

                case "r":
                    self.simboloAtual += self.linha.pop(0)
                    self.r_state()

                case "e":
                    self.simboloAtual += self.linha.pop(0)
                    self.e_state()

                case "t":
                    self.simboloAtual += self.linha.pop(0)
                    self.t_state()

                case "w":
                    self.simboloAtual += self.linha.pop(0)
                    self.w_state()

                case "b":
                    self.simboloAtual += self.linha.pop(0)
                    self.b_state()

                case "f":
                    self.simboloAtual += self.linha.pop(0)
                    self.f_state()

                case " ":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if(self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case ".":
                    self.simboloAtual += self.linha.pop(0)
                    self.ponto_state()
                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def i_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "f":
                    self.simboloAtual += self.linha.pop(0)
                    self.f_state()

                case "o":
                    self.simboloAtual += self.linha.pop(0)
                    self.o_state()

                case "l":
                    self.simboloAtual += self.linha.pop(0)
                    self.l_state()

                case "n":
                    self.simboloAtual += self.linha.pop(0)
                    self.n_state()

                case " ":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def f_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "u":
                    self.simboloAtual += self.linha.pop(0)
                    self.u_state()

                case "a":
                    self.simboloAtual += self.linha.pop(0)
                    self.a_state()

                case " ":
                    self.reservada.append(self.linha_lida)
                    if (self.simboloAtual == "if"):
                        self.reservada.append("PRE")
                    else:
                        self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    if (self.simboloAtual == "if"):
                        self.reservada.append("PRE")
                    else:
                        self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()

                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        if (self.simboloAtual == "if"):
                            self.reservada.append("PRE")
                        else:
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

    def v_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "a":
                    self.simboloAtual += self.linha.pop(0)
                    self.a_state()

                case " ":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def a_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "r":
                    self.simboloAtual += self.linha.pop(0)
                    self.r_state()

                case "d":
                    self.simboloAtual += self.linha.pop(0)
                    self.d_state()

                case "l":
                    self.simboloAtual += self.linha.pop(0)
                    self.l_state()

                case "n":
                    self.simboloAtual += self.linha.pop(0)
                    self.n_state()

                case " ":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def r_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "u":
                    self.simboloAtual += self.linha.pop(0)
                    self.u_state()

                case "o":
                    self.simboloAtual += self.linha.pop(0)
                    self.o_state()

                case "e":
                    self.simboloAtual += self.linha.pop(0)
                    self.e_state()

                case "t":
                    self.simboloAtual += self.linha.pop(0)
                    self.t_state()

                case "n":
                    self.simboloAtual += self.linha.pop(0)
                    self.n_state()

                case "i":
                    self.simboloAtual += self.linha.pop(0)
                    self.i_state()


                case " ":
                    self.reservada.append(self.linha_lida)
                    if(self.simboloAtual == "var"):
                        self.reservada.append("PRE")
                    else:
                        self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    if (self.simboloAtual == "var"):
                        self.reservada.append("PRE")
                    else:
                        self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()

                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        if (self.simboloAtual == "var"):
                            self.reservada.append("PRE")
                        else:
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()


    def c_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "o":
                    self.simboloAtual += self.linha.pop(0)
                    self.o_state()

                case "t":
                    self.simboloAtual += self.linha.pop(0)
                    self.t_state()

                case "e":
                    self.simboloAtual += self.linha.pop(0)
                    self.e_state()

                case " ":

                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def o_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "n":
                    self.simboloAtual += self.linha.pop(0)
                    self.n_state()

                case "c":
                    self.simboloAtual += self.linha.pop(0)
                    self.c_state()

                case "o":
                    self.simboloAtual += self.linha.pop(0)
                    self.o_state()

                case "l":
                    self.simboloAtual += self.linha.pop(0)
                    self.l_state()

                case " ":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def n_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "s":
                    self.simboloAtual += self.linha.pop(0)
                    self.s_state()

                case "c":
                    self.simboloAtual += self.linha.pop(0)
                    self.c_state()

                case "t":
                    self.simboloAtual += self.linha.pop(0)
                    self.t_state()

                case "g":
                    self.simboloAtual += self.linha.pop(0)
                    self.g_state()

                case " ":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "function" | "return" | "then" | "boolean":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "function" | "return" | "then" | "boolean":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "function" | "return" | "then" | "boolean":
                                self.reservada.append("PRE")
                            case _:
                                self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

    def s_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "t":
                    self.simboloAtual += self.linha.pop(0)
                    self.t_state()

                case "e":
                    self.simboloAtual += self.linha.pop(0)
                    self.e_state()

                case " ":

                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":

                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def t_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "r":
                    self.simboloAtual += self.linha.pop(0)
                    self.r_state()

                case "i":
                    self.simboloAtual += self.linha.pop(0)
                    self.i_state()

                case "a":
                    self.simboloAtual += self.linha.pop(0)
                    self.a_state()

                case "u":
                    self.simboloAtual += self.linha.pop(0)
                    self.u_state()

                case "h":
                    self.simboloAtual += self.linha.pop(0)
                    self.h_state()

                case " ":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "const" | "struct" | "start" | "print" | "int":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "const" | "struct" | "start" | "print" | "int":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "const" | "struct" | "start" | "print" | "int":
                                self.reservada.append("PRE")
                            case _:
                                self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

    def u_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "c":
                    self.simboloAtual += self.linha.pop(0)
                    self.c_state()

                case "r":
                    self.simboloAtual += self.linha.pop(0)
                    self.r_state()

                case "n":
                    self.simboloAtual += self.linha.pop(0)
                    self.n_state()

                case "e":
                    self.simboloAtual += self.linha.pop(0)
                    self.e_state()

                case " ":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def p_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "r":
                    self.simboloAtual += self.linha.pop(0)
                    self.r_state()

                case " ":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def e_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "d":
                    self.simboloAtual += self.linha.pop(0)
                    self.d_state()

                case "t":
                    self.simboloAtual += self.linha.pop(0)
                    self.t_state()

                case "l":
                    self.simboloAtual += self.linha.pop(0)
                    self.l_state()

                case "n":
                    self.simboloAtual += self.linha.pop(0)
                    self.n_state()

                case "a":
                    self.simboloAtual += self.linha.pop(0)
                    self.a_state()

                case " ":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "procedure" | "else" | "while" | "true" | "false":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "procedure" | "else" | "while" | "true" | "false":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "procedure" | "else" | "while" | "true" | "false":
                                self.reservada.append("PRE")
                            case _:
                                self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

    def d_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "u":
                    self.simboloAtual += self.linha.pop(0)
                    self.u_state()

                case " ":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "read":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "read":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "read":
                                self.reservada.append("PRE")
                            case _:
                                self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

    def l_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "s":
                    self.simboloAtual += self.linha.pop(0)
                    self.s_state()

                case "e":
                    self.simboloAtual += self.linha.pop(0)
                    self.e_state()

                case " ":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "real":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "real":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "real":
                                self.reservada.append("PRE")
                            case _:
                                self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

    def h_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "e":
                    self.simboloAtual += self.linha.pop(0)
                    self.e_state()

                case "i":
                    self.simboloAtual += self.linha.pop(0)
                    self.i_state()

                case " ":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def w_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "h":
                    self.simboloAtual += self.linha.pop(0)
                    self.h_state()

                case " ":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    if ():
                        self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def b_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "o":
                    self.simboloAtual += self.linha.pop(0)
                    self.o_state()

                case " ":

                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    else:
                        self.id_state()

    def g_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:
                case " ":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "string":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n":
                    self.reservada.append(self.linha_lida)
                    match self.simboloAtual:
                        case "string":
                            self.reservada.append("PRE")
                        case _:
                            self.reservada.append("IDE")
                    self.reservada.append(self.simboloAtual)
                    self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                case _:
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual:
                            case "string":
                                self.reservada.append("PRE")
                            case _:
                                self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

    def id_state(self):
        if len(self.linha) >= 1:#se a linha não tiver vazia
            match self.linha[0]:
                case " ": # se o proximo termo é um espaço em branco
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE") #classifica como identificador
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo() #pula pro proximo simbolo a ser lido
                    self.ignoraBranco() #volta para o estado E1

                #a quebra de linha vai classificar o simbolo como identificador
                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0() #voltara para o estado de leitura


                case _: #caso contrario fara uma chamada recursiva
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()

                    elif self.verificarSubset(self.linha[0]) == "letra":
                        self.simboloAtual += self.linha.pop(0)
                        self.id_state()
                    else:
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()



    def numero_State(self): #Estado iniciado após verificar a ocorrencia de um digito no E1
        if len(self.linha) >= 1:
            match self.linha[0]:#Lê o proximo termo
                case " ": #Se for um espaço em branco
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(self.simboloAtual) == True: #verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else: # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case '"':
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case ";":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case ",":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case ")":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "}":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "[":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "]":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "_":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case ">":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "<":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "=":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "|":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "&":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "!":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "/":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "+":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "-":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "*":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(
                                self.simboloAtual) == True:  # verifica se o simbolo guardado é formado so por inteiros
                            self.reservada.append("NRO")  # identifica como numero
                        else:  # se não atribui como identificador
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "\n": #identificado quebra de linha
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        if self.verificarSubset(self.simboloAtual) == True:
                            self.reservada.append("NRO") #identifica como numero
                        else:
                            self.reservada.append("IDE")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()#vai para o estado de leitura

                case ".": # se encontrar um ponto flutuante
                    self.simboloAtual += self.linha.pop(0) #adiciona o termo ao simbolo
                    self.decimal_State() #manda para o estado que identifica decimais
                case _: # qualquer outro caso
                    if self.verificarSubset(self.linha[0]) == True: #chama a função que verifica se o termo é um digito
                        self.simboloAtual += self.linha.pop(0) #adiciona o simbolo
                        self.numero_State() #faz chamada recursivo ddela memo
                    else: #se não for um nume classifica como um erro de identificador
                        self.simboloAtual += self.linha.pop(0)  # adiciona o simbolo
                        self.erro_state()  # faz chamada recursivo ddela memo


    def erro_state(self):
        if len(self.linha) >= 1:
            match self.linha[0]:  # Lê o proximo termo
                case " ":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "\n":
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()  # vai para o estado de leitura
                case _:
                    self.simboloAtual += self.linha.pop(0)  # adiciona o simbolo
                    self.erro_state()

    def decimal_State(self): #estado após identificar um numero seguido de ponto flutuante
        if len(self.linha) >= 1:
            match self.linha[0]:
                case ".":
                    self.simboloAtual += self.linha.pop(0)
                    self.decimal_State()  # volta para propria função
                case _:
                    if self.verificarSubset(self.linha[0]) == True: #verificar se o proximo termo é o numero
                        self.simboloAtual += self.linha.pop(0)
                        self.decimal_State() #volta para propria função
                    else: #se não verifica se a palavra lida é uma letra
                        if (self.simboloAtual != ""):
                            self.reservada.append(self.linha_lida)
                            lkl = self.simboloAtual.split(".");
                            if len(lkl) == 2:
                                if lkl[0].isnumeric() == True and lkl[1].isnumeric() == True:
                                    self.reservada.append("NRO")
                                else:
                                    self.reservada.append("NMF") #se sim apresenta erro de ponto flutuante
                            else:
                                self.reservada.append("NMF")  # se sim apresenta erro de ponto flutuante
                            self.reservada.append(self.simboloAtual)
                            self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo() #vai para o proximo simbolo
                        self.ignoraBranco()

    def ponto_state(self): #se o ponto for lido no estado E1 esse estado é chamado
        if len(self.linha) >= 1:
            match self.linha[0]:
                case ".":
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case ",":
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case ";":
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "\n": #se o proximo termo é uma quebra de linha ele reconhece o ponto como um delimitador
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("DEL")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()
                case _: #para todos os outros casos ele vai verificar se é um numero
                    if self.verificarSubset(self.linha[0]) == True:
                        self.simboloAtual += self.linha.pop(0)
                        self.decimal_State() #se sim vai mandar para o estado decimal
                    else:#Se não vai para o erro de ponto flutuante
                        if (self.simboloAtual != ""):
                            self.reservada.append(self.linha_lida)
                            self.reservada.append("NMF")
                            self.reservada.append(self.simboloAtual)
                            self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()






teste = analisador_lexico("teste2.txt")
teste.E0()
teste.E0()
teste.E0()
teste.E0()
arquivo0 = open("saida.txt", "a")
for lin in teste.simbolos:
    arquivo0.write(str(lin)+"\n")
print(teste.simbolos)