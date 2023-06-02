import string


class analizador_lexico:

    def __init__(self, arquivo):
        self.LinhaAtual = [] #vetor com todas as letras da linha lida
        self.linha_lida = 0 #numero da linha lida
        self.simboloAtual = '' #simbolo lidos(junção das letras)
        self.erros = []
        self.reservada = [] #vetor que retorna o simbolo e a linha lida
        self.linha = '' #linha lida
        self.arq = arquivo #arquivo lido
        self.alfabeto = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_") #alfabeto valido
        self.digito = set("0123456789-") #numeros
        self.simblosEspeciais = set("'\!#$%?@^`~") #simbolos validos
        self.simbolos = [] #tabela com simbolos lido
        self.comentario = [] #lista auxiliar temporario para guardar inicio e fim de comentario em bloco
        self.erro_comentario = [] #lista principal onde fica localizado a linha e o comentario em bloco mal formado
        self.erro_caract = [] #lista auxiliar temporaria para guardar simbolos de caracter
        self.caract = [] #lista principal que contera a linha e o comentario mal formado
        self._arquivo = open(arquivo, "r", encoding="UTF-8") #abertura de arquivo no modo leitura

    def verificarSubset(self,simbolo): #função que recebe um simbolo qualquer
        simb = set((simbolo)) #comando para setar esse simbolo como um conjunto
        if(simb.issubset(self.digito)): #verifica se esse simbolo faz parte do conjunto de digitos definidos
            return True
        elif simb.issubset(self.simblosEspeciais): #verifica se é um simbolo especial da tabela ascii
            return "simbolo"
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
                case "*":
                    self.blockComent_State() #esse estado É onde verifica o comentario em bloco
                case _:
                    self.div_state()


    def blockComent_State(self):#estado que so chega a partir do estado de comentario(previamente foi lido uma /)
        if len(self.linha) >= 1: #verifica se existe algo na linha
            match self.linha[0]:
                case '/': #caso leia uma barra
                    if len(self.linha) >= 1:
                        self.simboloAtual += self.linha.pop(0) #Retira o caractere da linha e adiciona a string do simbolo
                        if self.simboloAtual == "*/": #verifica se o simbolo atual é final de comentario
                            self.comentario.append(self.linha_lida) #se sim adiciona a  linha lida lista temporaria de comentarios
                            self.comentario.append(self.simboloAtual) # adiciona tambe o proprio simbolo lido
                            #essa lista abaixo sera usada em outra função para verificar se o comentario foi formado de forma correta
                            self.erro_comentario.append(self.comentario) # e coloca a lista dentro da lista de erros de comentario
                            self.comentario = [] #esvazia a lista temporaria
                            match self.linha[0]:
                                case " ": #caso o proximo caractere seja uma linha em branco
                                    self.pularProximoSimbolo() #esse caractere é ignorado
                                    self.resetSimbAtual() # o simbolo é resetado
                                    self.E1() #e o programa retorna para o estado E1
                                case "\n": #caso seja quebra de linha
                                    self.resetSimbAtual()
                                    self.ignoraBranco() #ele vai ou ir para o estado E1 ou E0 de acordo com a condição da função
                        else: #se não for fim de comentario
                            self.resetSimbAtual()
                            self.pularProximoSimbolo() # o proximo simbolo sera lido
                            self.blockComent_State() # e ira continuar no mesmo estado

                case '*': # caso leia asterisco identifica que é um comentario em bloco
                    if len(self.linha) >= 1:
                        self.simboloAtual += self.linha.pop(0) #adiciona ao simbolo
                        if self.simboloAtual == "/*": # se for identificado o inicio do comentario em bloco guardara a informação
                            self.comentario.append(self.linha_lida)
                            self.comentario.append(self.simboloAtual)
                            self.erro_comentario.append(self.comentario)
                            self.comentario = []
                        self.pularProximoSimbolo()
                        self.blockComent_State() #continuara no mesmo estado

                case "\n": #caso ocorra quebra de linha
                    self.resetSimbAtual()
                    self.lerLinha() #ler a proxima linha
                    self.blockComent_State() # continua no mesmo estado

                case _: # caso qualquer outra coisa significa que ainda esta no comentario
                    self.linha.pop(0) #então o caractere sera simplismente descartada
                    self.resetSimbAtual()
                    self.blockComent_State() # continua no mesmo estado

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

                #para os proximo casos caso encontre um delimitador o simbolo sera reconhecido como operador aritimetico e voltara para o estado E1
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

                # para os proximo casos caso encontre um delimitador o simbolo sera reconhecido como operador aritimetico e voltara para o estado E1
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

    def mini_state(self): # segue a mesma logica do plus state so que para o operador de subtração
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
                        if (self.verificarSubset(self.linha[0]) == True):
                            self.simboloAtual += self.linha.pop(0)
                            self.numero_State()
                        else:
                            self.reservada.append(self.linha_lida)
                            self.reservada.append("ART")
                            self.reservada.append(self.simboloAtual)
                            self.simbolos.append(self.reservada)
                            self.resetReservada()
                            self.resetSimbAtual()
                            self.pularProximoSimbolo()
                            self.ignoraBranco()

    def mult_state(self): #estado de multiplicação
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "/": #caso especial onde após o * vem uma barra indicando fim de bloco de comentario
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("CoMF") #identifica automaticamente como comentario mal formado
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                # os outros casos seguem a mesma logica do div state
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
    def negate_State(self): #estado que identifica a !
        if len(self.linha) >= 1:
            match self.linha[0]:#lendo primeira letra da linha
                case "\n": #no caso da quebra de linha
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG") #identifica como operador logico
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0() #após resetar todas as variaveis temporarias vai para o estado de leitura da proxima linha

                case "=": # caso leia o simbolo de igual
                    self.simboloAtual += self.linha.pop(0); #adiciona o simbolo, retira da linha
                    self.equals_State() # manda para o estado que processa o simbolo =

                #para todos os delimitadores lidos apos o proximo simbolo funciona da mesma forma dos operadores aritimeticos
                case "[":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG") #mas o simbolo sera identificado como operador logico
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

                case _: #para qualquer outro caso definira como operador logico
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()#ira ler o proximo simbolo
                    self.ignoraBranco() #e a função decidira o proximo estado

    def and_State(self): # estado que processa o simbolo &
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "&": # caso em que após o & ser lido outro & é lido
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG") #identifica como operador logico
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                #para todos os outros caso sera identificado como um token mal formado pois a linguagem não reconhece o simbolo & isolado apesar de ser capaz de processa-lo
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
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
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

    def or_State(self): #caso que processa o simbolo |
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "|": # caso identifique outro
                    self.simboloAtual += self.linha.pop(0)
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("LOG") #identifica como operador logico
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                #para todos os outros caso identifica como token mal formado
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
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "]":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()

                case "{":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case "}":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()


                case "(":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()
                    self.ignoraBranco()
                case ")":
                    if (self.simboloAtual != ''):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("TMF")
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

    def equals_State(self): #estado que processa o simbolo =
        if len(self.linha) >= 1:
            match self.linha[0]:
                case "=": # caso leia um segundo simbolo =
                    self.simboloAtual += self.linha.pop(0); #adiciona ao simbolo atual
                    self.equals_State() #continua no mesmo estado
                case "\n": #caso haja uma quebra de linha
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        match self.simboloAtual: # se a palavra for um dos simbolos validos ele identifica como relacional
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
                    self.E0() # volta pro estado E0

                #Ao se deparar com um delimitador tambem atribui o valor relacional
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

    #Os dois proximos estados seguem a mesma logica do equals state
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

    #Os 3 estados a seguir são delimitadores
    #ao chegar nesse estado a palavra que esta no simboloAtual automaticamente sera identificada como delimitador
    def colchetes_state(self):
        if len(self.linha) >= 1:
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
        if len(self.linha) > 0:
            match self.linha[0]:
                case "\n":
                    if (self.simboloAtual != ""):
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
        else:
           if (self.simboloAtual != ""):
                self.reservada.append(self.linha_lida)
                self.reservada.append("DEL")
                self.reservada.append(self.simboloAtual)
                self.simbolos.append(self.reservada) 

    #Só é possivel chegar nesse estado a partir da leitura previa de aspas duplas
    def string_state(self): # estado de cadeia de caracteres
        if len(self.linha) >= 1:
            match self.linha[0]:
                case '"': #identificou novas aspas duplas
                    if len(self.erro_caract) -1 >= 1:
                        self.erro_caract.pop()
                    if (self.simboloAtual != ""):
                        self.simboloAtual += self.linha.pop(0)
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("CAC") #identifica como cadeia de caractere
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.ignoraBranco()

                case "\n": #caso identifique uma quebra de linha
                    if(self.simboloAtual != ""):
                        self.simboloAtual += self.linha.pop(0)
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("CAC")  # identifica como cadeia de caractere
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.lerLinha() # le uma nova linha
                    self.string_state() #continua no mesmo estado

                case _:
                    self.simboloAtual += self.linha.pop(0)
                    self.string_state()



    def E1(self): #estado responsavel por processar a primeira leta de cada novo simbolo lido
        if len(self.linha) >= 1:
            match self.linha[0]:
                case '"': #identifica que sera uma string
                    self.simboloAtual += self.linha.pop(0)
                    #guardando informação de cadeia de caracteres
                    self.caract.append(self.linha_lida) #linha
                    self.caract.append(self.simboloAtual) #aspoas
                    self.erro_caract.append(self.caract) #ambos juntos
                    self.caract = [] #resetando vetor temporario
                    self.string_state()
                #caso dos delimitadores
                case ".":
                    self.ponto_state()
                case ";":
                    self.ponto_state()
                case ",":
                    self.ponto_state()
                case "(":
                    self.simboloAtual += self.linha.pop(0)
                    self.parenteses_state()
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

                #começando variavel por underline manda para o estado de erro
                case "_":
                    self.simboloAtual += self.linha.pop(0)
                    self.erro_state()

                #operadores relacionais
                case ">":
                    self.simboloAtual += self.linha.pop(0)
                    self.maiorQ_State()
                case "<":
                    self.simboloAtual += self.linha.pop(0)
                    self.menorQ_State()
                case "=":
                    self.simboloAtual += self.linha.pop(0)
                    self.equals_State()

                #operadores logicos
                case "|":
                    self.simboloAtual += self.linha.pop(0)
                    self.or_State()

                case "&":
                    self.simboloAtual += self.linha.pop(0)
                    self.and_State()

                case "!":
                    self.simboloAtual += self.linha.pop(0);
                    self.negate_State()

                #operadores aritimeticos
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

                #vogais validas para palavras reservadas
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

                #outros delimitadores
                case ".":
                    self.simboloAtual += self.linha.pop(0)
                    self.ponto_state()

                case " ":
                    self.simboloAtual += self.linha.pop(0)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E1()

                case "\n":
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()

                #qualquer outro caso
                case _:
                    if self.verificarSubset(self.linha[0]) == True: #se numero for processado
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State()
                    elif self.verificarSubset(self.linha[0]) == "simbolo": #se simbolos ascii fora do escopo valido predefinido for processado
                        self.erro_state()
                    else: #toda outra possibilidade é um identificador
                        self.id_state()

    #Sequência de estados que identificam palavras reservadas. Processo:
    #1 -Chegou no estado. Identifica o proximo caractere lido.
    #2 -É estado de letras predefinidas: Ele retira o caractere da linha e concatena com o sibmolo
    #3a- É estado final e após ele é um delimitador, espaço vazio, ou quebra de linha: Identifica como reservada
    #3a - Reseta as variaveis temporarias e volta para o Estado E1 ou E0.
    #3b - É estado final mas após ele tem mais letras
    #3ba - Letra predefinida: volta para o ponto 2.
    #3bb - Letra não predefinida, numero ou _ vai para o estado de identificador
    #3c - Não é estado final mas após ele é um delimitador, espaço vazio, ou quebra de linha: Vai para o estado de identificador


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

    def id_state(self): #estado de identificador
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

                case " ":  # se o proximo termo é um espaço em branco
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IDE")  # classifica como identificador
                        self.reservada.append(self.simboloAtual)
                        self.simbolos.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.pularProximoSimbolo()  # pula pro proximo simbolo a ser lido
                    self.ignoraBranco()  # volta para o estado E1

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


                case _: #caso contrario
                    if self.verificarSubset(self.linha[0]) == True: #verifica se é numero
                        self.simboloAtual += self.linha.pop(0)
                        self.numero_State() # vai para o estado que processa numero

                    elif self.verificarSubset(self.linha[0]) == "letra": # se for letra
                        self.simboloAtual += self.linha.pop(0)
                        self.id_state() # continua no estado de IDE
                    elif  self.verificarSubset(self.linha[0]) == "simbolo":
                        self.erro_state()
                    else: # qualquer outra coisa vai para o estado de erro
                        if (self.simboloAtual != ""):
                            self.reservada.append(self.linha_lida)
                            self.reservada.append("IDE")
                            self.reservada.append(self.simboloAtual)
                            self.simbolos.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.E1()  # voltara para o estado de leitura



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
                case '"': #identificou inicio de comentario
                    match self.verificarSubset(self.simboloAtual):
                        case "simbolo": #no caso de ser simbolo do ascii não predefinido
                            if (self.simboloAtual != ""):
                                self.reservada.append(self.linha_lida)
                                self.reservada.append("TMF") # token mal formado
                                self.reservada.append(self.simboloAtual)
                                self.erros.append(self.reservada)
                            self.resetReservada()
                            self.resetSimbAtual()
                            self.pularProximoSimbolo()
                            self.ignoraBranco()
                        case _: # qualquer outro caso
                            if (self.simboloAtual != ""):
                                self.reservada.append(self.linha_lida)
                                self.reservada.append("IMF") #reconhece como um identificador mal formado
                                self.reservada.append(self.simboloAtual)
                                self.erros.append(self.reservada)
                            self.resetReservada()
                            self.resetSimbAtual()
                            self.pularProximoSimbolo()
                            self.ignoraBranco()
                case " ": #caso da linha branco
                    match self.verificarSubset(self.simboloAtual):
                        case "simbolo": # se for simbolo
                            if (self.simboloAtual != ""):
                                self.reservada.append(self.linha_lida)
                                self.reservada.append("TMF") #identifica como token mal formado
                                self.reservada.append(self.simboloAtual)
                                self.erros.append(self.reservada)
                            self.resetReservada()
                            self.resetSimbAtual()
                            self.pularProximoSimbolo()
                            self.ignoraBranco()
                        case _: #caso contrario como identificador mal formado
                            if (self.simboloAtual != ""):
                                self.reservada.append(self.linha_lida)
                                self.reservada.append("IMF")
                                self.reservada.append(self.simboloAtual)
                                self.erros.append(self.reservada)
                            self.resetReservada()
                            self.resetSimbAtual()
                            self.pularProximoSimbolo()
                            self.ignoraBranco()
                case "\n": #caso quebra de linha
                    if (self.simboloAtual != ""):
                        self.reservada.append(self.linha_lida)
                        self.reservada.append("IMF")
                        self.reservada.append(self.simboloAtual)
                        self.erros.append(self.reservada)
                    self.resetReservada()
                    self.resetSimbAtual()
                    self.E0()  # vai para o estado de leitura

                case _: #qualquer outra coisa
                    self.simboloAtual += self.linha.pop(0)  # adiciona o simbolo
                    if self.verificarSubset(self.linha[0]) == True: #identificando um numero
                        if (self.simboloAtual != ""):
                            self.reservada.append(self.linha_lida)
                            self.reservada.append("TMF") #identifica como um token mal formado
                            self.reservada.append(self.simboloAtual)
                            self.erros.append(self.reservada)
                        self.resetReservada()
                        self.resetSimbAtual()
                        self.pularProximoSimbolo()
                        self.ignoraBranco()

                        
                    else: #caso contrario so le o proximo simbolo e fica no mesmo estado
                        self.pularProximoSimbolo()
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

    def checarErroComent(self): #estado que verifica erro de comentario
        if len(self.erro_comentario) >= 1: #verifica se a lista de comentario tem pelo menos um item
           self.simbolos.append(self.erro_comentario[0])
           self.simbolos[-1].insert(1, "CoMF")

    def checarErroCadeia(self):
        if len(self.erro_caract) >= 1:
            self.simbolos.append(self.erro_caract[0])
            self.simbolos[-1].insert(1, "CMF")






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






