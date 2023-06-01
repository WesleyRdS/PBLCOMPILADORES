import sys
sys.path.insert(1,'./FP')
sys.path.insert(1,'./bloco_var')
sys.path.insert(1,'./estrutura_de_dados')
sys.path.insert(1,'./exp')
sys.path.insert(1,'./if_while')
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
import func

class printar:
    def __init__(self, lista, linha, arquivo, classe):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe


    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.token) > 0:
            if self.list[0] == "print":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'print'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'print'\n")

    def E1(self):
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
                        self.E2()
                    elif self.token[0] == "CAC" or self.token[0] == "NRO" or self.list[0] == "true" or self.list == "false":
                        self.list.pop(0)
                        self.token.pop(0)
                        self.n.pop(0)
                        self.E2()
                    elif self.token[0] == "IDE":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token)
                        iniciar_automato.E0()
                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'int', 'real', 'string', 'vetor' or 'function'\n")
                else:
                    self.erro.append("ERROR: Line-final Expected: ')'\n")
            elif self.list[0] == ")":
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                self.E2()        
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected: '('\n")

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ",":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ','\n")
                self.E3()
        else:
            self.erro.append("ERROR: Line-final Expected: ','\n")

    def E3(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ")":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ')'\n")
        else:
            self.erro.append("ERROR: Line-final Expected: ')'\n")