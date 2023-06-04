import variavel.parametro_var


class parametro_vetor:
    def __init__(self,lista,linha, arquivo,classe, remetente):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe
        self.remetente = remetente

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            match self.token[0]:
                case 'NRO' | 'IDE':
                    self.list.pop(0)
                    self.token.pop(0)
                    self.n.pop(0)
                    self.E1()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real', or 'ide'\n")
                    self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected 'int', 'real', or 'ide'\n")

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case ']':
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    iniciar_automato = variavel.parametro_var.parametro_var(self.list,self.n, self.erro,self.token,self.remetente)
                    iniciar_automato.E2()
                
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ']' \n")
                    iniciar_automato = variavel.parametro_var.parametro_var(self.list,self.n, self.erro,self.token,self.remetente)
                    iniciar_automato.E2()
        else:
            self.erro.append("ERROR: Line-final Expected ']' \n")
             