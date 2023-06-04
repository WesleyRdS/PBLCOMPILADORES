import sys
sys.path.insert(1,'./if_while')
sys.path.insert(1,'./PR')
sys.path.insert(1,'./FP')
import exp.exp_logica
import atribuir_valor
import FP.func
import FP.procedu
import if_while.ifthen
import if_while.while_a
import PR.printar
import PR.reader

class exp_aritimetica:

    def __init__(self,lista,linha, arquivo,classe,remetente):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe
        self.pilha = []
        self.remetente = remetente


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
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
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
                x = self.list.pop(0)
                self.n.pop(0)
                if(len(self.list)>0):
                    if self.token[0] == "NRO" or self.token[0] == "IDE":
                        self.E4()
                    elif self.list[0] == "(": 
                        self.E1()
                    elif x == "++" or x == "--":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8() 

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
                    
                    elif self.list[0] == ")" and len(self.pilha) == 0: 
                        self.E5()
                    
                    elif self.list[0] == "=":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E1() 

                    elif self.list[0] == ";":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8() 
                    
                    elif self.token[0] == "REL":
                        iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E3()
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
            if self.list[0] == ")" and len(self.pilha)> 0:
                self.pilha.pop(0)
                self.E5()
            elif self.list[0] == ")" and len(self.pilha) == 0:
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                if self.list[0] == "{":
                    if len(self.remetente) > 0:
                        if self.remetente[0] == "while":
                            self.remetente.pop(0)
                            iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E3()
                        else:
                            self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/' or '*'\n")
                            self.E6()
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/' or '*'\n")
                        self.E6()
                elif self.list[0] == "then":
                    if len(self.remetente) > 0:
                        if self.remetente[0] == "if":
                            self.remetente.pop(0)
                            iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E3()
                        else:
                            self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/' or '*'\n")
                            self.E6()
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '+', '-', '/' or '*'\n")
                        self.E6()
                elif self.list[0] == ";":
                    if len(self.remetente) > 0:
                        if self.remetente[0] == "print":
                            self.remetente.pop(0)
                            iniciar_automato = PR.printar.printar(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E0()
                        else:
                            iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E8()
                    else:
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8()  
                else:
                    self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
                    self.E6()
               
            elif self.list[0] == "ART":
                self.E6()
                    
            elif self.list[0] == ";":
                if len(self.remetente) > 0:
                    if self.remetente[0] == "print":
                        self.remetente.pop(0)
                        iniciar_automato = PR.printar.printar(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E0()
                    else:
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8()
                else:
                    iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                    iniciar_automato.E8()  
            

            elif self.token[0] == "REL": 
                iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            
            elif self.list[0] == ";":
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E8() 

            
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





