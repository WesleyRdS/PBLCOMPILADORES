import exp_logica
import atribuir_valor
class exp_aritimetica:

    def __init__(self,lista,linha, arquivo,classe):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe
        self.pilha = []


    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            if self.token[0] == "NRO" or self.token[0] == "IDE":
                self.E2()
            elif self.list[0] == "(":
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real' 'ide' or '('\n")
                self.E3()
        else:
            self.erro.append("ERROR: Line-final Expected 'int', 'real' 'ide' or '('\n")

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            if self.list[0] == "(":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.pilha.append(")")
                self.E2()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '('\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected '('\n")

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            if self.token[0] == "NRO" or self.token[0] == "IDE":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == ")" and len(self.pilha) > 0:
                        self.pilha.pop(0)
                        self.E5()

                    elif self.list[0] == ";":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token)
                        iniciar_automato.E8() 
                    else: 
                        self.E3()
                else:
                    self.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real' 'ide'\n")
                self.E3()

        else:
            self.erro.append("ERROR: Line-final Expected 'int', 'real' 'ide' or '('\n")
    
    
    def E3(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            if self.token[0] == "ART":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                if(len(self.list)>0):
                    if self.token[0] == "NRO" or self.token[0] == "IDE":
                        self.E4()
                    elif self.list[0] == "(": 
                        self.E1()
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real' 'ide' or '('\n")
                        self.E4()
                else:
                    return self.list      
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/' or '*'\n")
                self.E4()
        else:
            self.erro.append("ERROR: Line-final Expected '+', '-', '/' or '*'\n")

    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            if self.token[0] == "NRO" or self.token[0] == "IDE":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                if(len(self.list)>0):
                    if self.token[0] == "ART":
                        self.E3()
                    elif self.list[0] == ")" and len(self.pilha) > 0: 
                        self.pilha.pop(0)
                        self.E5()

                    elif self.list[0] == ";":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token)
                        iniciar_automato.E8() 
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/', '*' or ')'\n")
                        self.E6()
                else:
                    return self.list
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real' 'ide'\n")
                self.E3()

        else:
            self.erro.append("ERROR: Line-final Expected 'int', 'real' 'ide' or '('\n")
    
    

    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            if self.list[0] == ")":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                if(len(self.list)>0):
                    if self.list[0] == "ART":
                        self.E6()
                    elif self.list[0] == ")" and len(self.pilha)> 0:
                        self.pilha.pop(0)
                        self.E5()
                    elif self.list[0] == ")" and len(self.pilha) == 0:
                        self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
                        self.token.pop(0)
                        self.list.pop(0)
                        self.n.pop(0)
                        self.E6()

                    elif self.token[0] == "REL": 
                        iniciar_automato = exp_logica.exp_logica(self.list,self.n, self.erro,self.token)
                        iniciar_automato.E3()
                    
                    elif self.list[0] == ";":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token)
                        iniciar_automato.E8() 
                    else: 
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/' or '*'\n")
                        self.E6()
                else:
                    return self.list
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ')'\n")
        else:
            self.erro.append("ERROR: Line-final Expected ')'\n")

        
    def E6(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            if self.list[0] == "ART":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E0()
            else: 
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/' or '*'\n")
                self.E0()
        else:
            self.erro.append("ERROR: Line-final Expected '+', '-', '/' or '*'\n")





