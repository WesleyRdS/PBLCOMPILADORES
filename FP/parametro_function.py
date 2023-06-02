import sys
sys.path.insert(1,'./estrutura_de_dados')
import estrutura_de_dados.struct_exp
import atribuir_valor

class parametro_function:
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
            if self.token[0] == "IDE" or self.token[0] == "NRO" or self.token[0] == "CAC" or self.list[0] == "true" or self.list[0] == "false":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'IDE'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'IDE'\n")

    def E1(self):
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
                if self.destino == "struct_func":
                    iniciar_automato = estrutura_de_dados.struct_exp.struct_exp(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E8()
                elif self.destino == "atr_v":
                    self.list.pop(0)
                    self.token.pop(0)
                    self.n.pop(0)
                    iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E8()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ',' or ')'\n")
                self.E0()
        else:
            self.erro.append("ERROR: Line-final Expected: ',' or ')'\n")