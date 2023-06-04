import constante.automato_bloco_const
import constante.valor_variavelC
import constante.parametro_vetorC

class parametro_const:
    def __init__(self, lista, linha, arquivo, classe, remetente):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe
        self.remetente = remetente

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            if self.list[0] == 'int' or self.list[0] == 'boolean' or self.list[0] == 'string' or  self.list[0] == 'real' or self.token[0] == "IDE" :
                self.n.pop(0)
                self.list.pop(0)
                self.token.pop(0)
                self.E1()  
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real', 'boolean' or 'ide(struct)'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected 'int', 'real', 'boolean' or 'ide(struct)'\n")

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            match self.token[0]:
                case 'IDE':
                    self.n.pop(0)
                    self.token.pop(0)
                    self.list.pop(0)
                    self.E2()  
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'ide'\n")
                    self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected 'ide'\n")
                    

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):  
            match self.list[0]:
                case ',':
                    self.n.pop(0)
                    self.list.pop(0)
                    self.token.pop(0)
                    self.E1()
                case '=':
                    self.n.pop(0)
                    self.list.pop(0)
                    self.token.pop(0)
                    iniciar_automato = constante.valor_variavelC.valor_variavelC(self.list,self.n, self.erro,self.token,self.remetente)
                    iniciar_automato.E0()
                case '[':
                    self.n.pop(0)
                    self.list.pop(0)
                    self.token.pop(0)
                    iniciar_automato = constante.parametro_vetorC.parametro_vetorC(self.list, self.n, self.erro, self.token,self.remetente)
                    iniciar_automato.E0()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ',', '=' or '['\n")

                    if self.token[0] == 'NRO' or self.token[0] == 'CAC' or self.token[0] == 'IDE' or self.list[0] == 'true' or self.list[0] == 'false':
                        iniciar_automato = constante.valor_variavelC.valor_variavelC(self.list, self.n, self.erro, self.token,self.remetente)
                        iniciar_automato.E0()
                    else:
                        self.E3()
        else:
             self.erro.append("ERROR: Line-final Expected ',', '=' or '['\n")
                

    def E3(self):
        if(len(self.token)>0):  
            match self.list[0]:
                case ';':
                    self.n.pop(0)
                    self.list.pop(0)
                    self.token.pop(0)
                    if(len(self.list)> 0):
                        if self.list[0] == 'true' or self.list[0] == 'false' or self.token[0] == "IDE" or self.token == "NRO" or self.list[0] == 'int' or self.list[0] == 'boolean' or self.list[0] == 'string' or self.list[0] == 'real' or self.token[0] == "CAC":
                            self.E0()
                        else:
                            iniciar_automato = constante.automato_bloco_const.bloco_const(self.list, self.n, self.erro, self.token,self.remetente)
                            iniciar_automato.E2()
                    else:
                        iniciar_automato = constante.automato_bloco_const.bloco_const(self.list, self.n, self.erro, self.token,self.remetente)
                        iniciar_automato.E2()
                case _:
                    if self.list[0] == "real" or self.list[0] == "int" or self.list[0] == 'boolean' or self.list[0] == "string" or self.token[0] == "IDE":
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ';'\n")
                        self.E0()
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0] +" Read "+self.list[0]+  "Expected ';' \n")
                        iniciar_automato = constante.automato_bloco_const.bloco_const(self.list, self.n, self.erro, self.token,self.remetente)
                        iniciar_automato.E2()
        else:
            self.erro.append("ERROR: Line-final Expected ';' \n")

                        
