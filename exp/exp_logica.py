import sys

import exp.exp_aritimetica
import atribuir_valor
sys.path.insert(1,'./if_while')
import if_while.ifthen
import if_while.while_a
class exp_logica:

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
            if self.token[0] == "NRO" or self.token[0] == "IDE" or self.list[0] == "true" or self.list[0] == "false" :
                self.E2()
            elif self.list[0] == "(":
                self.E1()
            elif self.list[0] == ")":
                self.E5()
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
            if self.token[0] == "NRO" or self.token[0] == "IDE" or self.list[0] == "true" or self.list[0] == "false":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == ")":
                        self.E5()
                    elif self.list[0] == ";":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8() 

                    else: 
                        self.E3()
                else:
                    self.E3()
            elif self.list[0] == ")":
                self.E5()   
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
            if self.token[0] == "REL":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E4()

            elif self.token[0] == "ART":
                iniciar_automato = exp.exp_aritimetica.exp_aritimetica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            
            elif self.list[0] == ")":
                self.E5()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+ " Expected '==', '>=' '<=' or '!='\n")
                self.E4()
        else:
            self.erro.append("ERROR: Line-final Expected '==', '>=' '<=' or '!='\n")

    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            if self.list[0] == "true" or self.list[0] == "false" or self.token[0] == "NRO" or self.token[0] == "IDE":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                if len(self.list)> 0:
                    if self.token[0] == "REL":
                        self.list.pop(0)
                        self.n.pop(0)
                        self.token.pop(0)
                        self.E0()
                    elif self.token[0] == "ART":
                        iniciar_automato = exp.exp_aritimetica.exp_aritimetica(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E3()
                    elif self.list[0] == ")":
                        self.E5()
                    
                    elif self.list[0] == ";":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8() 

                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+ " Expected '==', '>=' '<=' or '!='\n")
                        self.E0()
                else:
                    return self.list
                
            elif self.token[0] == "ART":
                iniciar_automato = exp.exp_aritimetica.exp_aritimetica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()

            elif self.list == ";":
                    iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                    iniciar_automato.E8()
           
            
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+ " Expected 'true', 'false' 'int' or 'real'\n")
          
        else:
            self.erro.append("ERROR: Line-final Expected 'true', 'false' 'int' or 'real'\n")




    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.token)>0:
            if self.list[0] == ")" and len(self.pilha) > 0:
                self.pilha.pop(0)
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E5()
            elif self.list[0] == ")" and len(self.pilha) == 0:
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                if len(self.token)>0:
                    if self.token[0] == "REL":
                        self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
                        self.E3()
            
                    elif self.list[0] == "then":
                        if len(self.remetente) > 0:
                            if self.remetente[0] == "if":
                                self.remetente.pop(0)
                                iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                            else:
                                iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                        else:
                            iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E3()

                    elif self.list[0] == "{":
                        if len(self.remetente) > 0:
                            if self.remetente[0] == "while":
                                self.remetente.pop(0)
                                iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                            else:
                                iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                        else:
                            iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E3()
                    elif self.token[0] == "ART":
                        self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
                        iniciar_automato = exp.exp_aritimetica.exp_aritimetica(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E3()
                        
                    elif self.list[0] == ";":
                        self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8() 
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
                        self.E0()
                else:
                    self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
               

            else:
                if len(self.token)>0:
                    if self.token[0] == "REL":
                        self.E3()
            
                    elif self.list[0] == "then":
                        if len(self.remetente) > 0:
                            if self.remetente[0] == "if":
                                self.remetente.pop(0)
                                iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                            else:
                                iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                        else:
                            iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E3()

                    elif self.list[0] == "{":
                        if len(self.remetente) > 0:
                            if self.remetente[0] == "while":
                                self.remetente.pop(0)
                                iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                            else:
                                iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                                iniciar_automato.E3()
                        else:
                            iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                            iniciar_automato.E3()
                    elif self.token[0] == "ART":
                        iniciar_automato = exp.exp_aritimetica.exp_aritimetica(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E3()
                        
                    elif self.list[0] == ";":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E8() 
                    
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ';', '==', '>=' '<=', '!=', '+', '-', '*' or '/' \n")
                        self.E0()
                else:
                    return self.list
                    
     
        else:
            return self.list
