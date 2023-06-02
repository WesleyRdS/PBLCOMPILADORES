import variavel.parametro_var

class bloco_var:
    def __init__(self, lista, linha, arquivo,classe):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "var":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E1()  
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'var'\n")
                    self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected 'var'\n")

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "{":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E2()  
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '{'\n")
                    self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected '{'\n")


    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "}":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    return self.list
                case _:
                    #se tiver declaração de inteiro, real, booleano ou string ou o proprio valor vai para o automato de paramatros das variaveis
                    #La checara se a forma sintatica do parametro do bloco esta correta 
                    if self.list[0] == 'true' or self.list[0] == 'false' or self.token[0] == "IDE" or self.token == "NRO" or self.list[0] == 'int' or self.list[0] == 'boolean' or self.list[0] == 'string' or self.list[0] == 'real':
                        iniciar_automato = variavel.parametro_var.parametro_var(self.list, self.n, self.erro, self.token)
                        iniciar_automato.E0()

                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '}'\n")
        else:
            self.erro.append("ERROR: Line-final Expected '}'\n")
                        


