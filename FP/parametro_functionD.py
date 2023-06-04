import sys
sys.path.insert(1,'./estrutura_de_dados')

import FP.func
import FP.procedu

class parametro_functionD:
    def __init__(self, lista, linha, arquivo, classe, local):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe
        self.destino = local

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.token) > 0:
            if self.token[0] == "IDE" or self.list[0] == "int" or self.list[0] == "real" or self.list[0] == "string" or self.list[0] == "boolean":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'IDE','int', 'real' or 'boolean'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'IDE','int', 'real' or 'boolean'\n")
    

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.token) > 0:
            if self.token[0] == "IDE":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E2()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'IDE'\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected: 'IDE'\n")

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.token) > 0:
            if self.list[0] == ",":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E0()
            elif self.list[0] == ")":
                if len(self.destino) > 0:
                    if self.destino[0] == "func":
                        self.destino.pop(0)
                        iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token,self.destino)
                        iniciar_automato.E4()
                    elif self.destino[0] == "proc":
                        self.destino.pop(0)
                        iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token,self.destino)
                        iniciar_automato.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ',' or ')'\n")
                
        else:
            self.erro.append("ERROR: Line-final Expected: ',' or ')'\n")