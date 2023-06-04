import variavel.parametro_var

class valor_variavel:

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
            if self.token[0] == 'NRO' or self.token[0] == 'CAC' or self.token[0] == 'IDE' or self.list[0] == 'true' or self.list[0] == 'false' :
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                iniciar_automato = variavel.parametro_var.parametro_var(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E2()
            
            elif self.list[0] == '[':
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E1()

            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real', 'boolean', 'ide', 'string' or '['\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected 'int', 'real', 'boolean', 'ide', 'string' or '['\n")

           
           

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            if (self.token[0] == 'NRO') or (self.token[0] == 'CAC') or (self.token[0] == 'IDE') or (self.list[0] == 'true') or (self.list[0] == 'false'):
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E2()
            
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real', 'string', 'boolean', or 'ide'\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected 'int', 'real', 'string', 'boolean', or 'ide'\n")

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            if self.list[0] == ',':
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E1()
            
            elif self.list[0] == ']':
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                iniciar_automato = variavel.parametro_var.parametro_var(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E2()
            
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ',' or ']'\n")
                self.E1()
        
        else:
            self.erro.append("ERROR: Line-final Expected ',' or ']'\n")
