import sys
sys.path.insert(1,'./FP')
sys.path.insert(1,'./bloco_var')
sys.path.insert(1,'./estrutura_de_dados')
sys.path.insert(1,'./exp')
sys.path.insert(1,'./if_while')
sys.path.insert(1,'./PR')
import printar
import reader
import automato_bloco_var
import vetor
import struct
import struct_exp
import exp_aritimetica
import exp_logica
import atribuir_valor
import ifthen
import while_a
import parametro_functionD
import procedu


class func:
    def __init__(self, lista, linha, arquivo, classe):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "function":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'function'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'function'\n")


    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "int" and self.list[0] == "real" and self.list[0] == "string" and self.list[0] == "boolean" and self.token[0] == "IDE":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E2()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'int', 'real', 'string' or 'IDE'\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected: 'int', 'real', 'string' or 'IDE'\n")

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.token[0] == "IDE":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'IDE'\n")
                self.E3()
        else:
            self.erro.append("ERROR: Line-final Expected: 'IDE'\n")


    def E3(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "(":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == ")":
                        self.E4()
                    else:
                        iniciar_automato = parametro_functionD.parametro_functionD(self.list,self.n, self.erro,self.token,"func")
                        iniciar_automato.E0()
                else:
                    self.erro.append("ERROR: Line-final Expected: ')'\n")
            elif self.list[0] == ")":
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                self.E4()        
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                iniciar_automato = parametro_functionD.parametro_functionD(self.list,self.n, self.erro,self.token,"func")
                iniciar_automato.E0()
        else:
            self.erro.append("ERROR: Line-final Expected: '('\n")


    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ")":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E5()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ')'\n")
                self.E5()
        else:
            self.erro.append("ERROR: Line-final Expected: ')'\n")

    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "{":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E6()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '{'\n")
                    self.E6()
        else:
            self.erro.append("ERROR: Line-final Expected '{'\n")


    def E6(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "var":
                iniciar_automato = automato_bloco_var.automato_bloco_var(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0() 
            elif self.token[0] == "IDE":
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "if":
                iniciar_automato = ifthen.ifthen(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "while":
                iniciar_automato =while_a.while_a(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "struct":
                iniciar_automato = struct.struct(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "procedure":
                iniciar_automato = procedu.procedu(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list == "function":
                iniciar_automato = func.func(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list == "print":
                iniciar_automato = printar.printar(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list == "read":
                iniciar_automato = reader.reader(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            else:
                self.E7()
        else:
            self.erro.append("ERROR: Line-final Expected 'return'\n")

    def E7(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "return":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E8()
            else:
               self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'return'\n")
               self.E8()
        else:
            self.erro.append("ERROR: Line-final Expected 'return'\n")

    def E8(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.token[0] == "NRO" or self.token[0] == "IDE" or self.list[0] == "true" or self.list[0] == "false" or self.token[0] == "CAC":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E9()
            else:
               self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'IDE', 'int', 'real', 'true', 'false' or 'string'\n")
               self.E9()
        else:
            self.erro.append("ERROR: Line-final Expected 'IDE', 'int', 'real', 'true', 'false' or 'string'\n")

    
    def E9(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "}":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '}'\n")
                 
        else:
            self.erro.append("ERROR: Line-final Expected '}'\n")

