import sys
sys.path.insert(1,'./exp')
import exp.exp_logica
sys.path.insert(1,'./FP')
import FP.func
import FP.procedu
import if_while.ifthen
import if_while.while_a
import bloco_start
import FP.parametro_function

class atribuir_valor:
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
        if len(self.list) > 0:
            if self.token[0] == "IDE":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == "=":
                        self.E1()
                    elif self.list[0] == ".":
                        self.E2()
                    elif self.list[0] == "[":
                        self.E3()
                    elif self.token[0] == "REL":
                        iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: IDE\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: IDE\n")

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "=":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E7()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '='\n")
                self.E7()
        else:
            self.erro.append("ERROR: Line-final Expected: '='\n") 


    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ".":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E6()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '.'\n")
                self.E6()
        else:
            self.erro.append("ERROR: Line-final   Expected: '.'\n")

    def E3(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "[":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E4()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '['\n")
                self.E4()
        else:
            self.erro.append("ERROR: Line-final   Expected: '['\n")
        
    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.token[0] == "IDE" or self.token[0] == "NRO":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E5()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'int' or IDE\n")
                self.E5()
        else:
            self.erro.append("ERROR: Line-final   Expected: 'int' or IDE\n")

    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "]":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == "=":
                        self.E1()
                    elif self.list[0] == "[":
                        self.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ']'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final   Expected: ']'\n")



    
    def E6(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.token[0] == "IDE":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == "=":
                        self.E1()
                    elif self.list[0] == "[":
                        self.E3()
            elif self.list[0] == "[":
                        self.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: IDE\n")
                self.E1()


    def E7(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.token[0] == "IDE" or self.token[0] == "NRO":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                if len(self.list) > 0:
                    if self.token[0] == "ART" or self.token[0] == 'REL':
                        iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E3()
                    elif self.list[0] == "(":
                        self.list.pop(0)
                        self.token.pop(0)
                        self.n.pop(0)
                        iniciar_automato = FP.parametro_function.parametro_function(self.list,self.n, self.erro,self.token,"atr_v")
                        iniciar_automato.E0()
                    else:
                        self.E8()
                else:
                    self.E8()
            elif self.list[0] == "(":
                iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'IDE','int', 'real or boolean\n")
                self.E8()
        else:
            self.erro.append("ERROR: Line-final Read "+self.list[0]+  " Expected: 'IDE','int', 'real or boolean\n")


        
    def E8(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ";":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                if self.remetente == "func":
                    iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E6()
                elif self.remetente == "proc":
                    iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E5()
                elif self.remetente == "if":
                    iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E5()
                elif self.remetente == "while":
                    iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E4()
                elif self.remetente == "start":
                    iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E2()


            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ';'\n")
                return self.list
        else:
           
            self.erro.append("ERROR: Line-final   Expected: ';'\n")


