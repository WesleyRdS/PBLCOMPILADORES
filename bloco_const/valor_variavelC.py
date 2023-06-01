import parametro_const

class valor_variavelC:

    def __init__(self,lista,linha, arquivo,classe):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.token)>0):
            if self.token[0] == 'NRO' or self.token[0] == 'CAC' or self.token[0] == 'IDE' or self.list[0] == 'true' or self.list[0] == 'false' :
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                iniciar_automato = parametro_const.parametro_const(self.list,self.n, self.erro,self.token)
                iniciar_automato.E3()
            
            elif self.list[0] == '[':
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E1()

            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'int', 'real', 'string', 'boolean', 'ide' or '['\n")
                self.E1()
        else:
             self.erro.append("ERROR: Line-final Expected 'int', 'real', 'string', 'boolean', 'ide' or '['\n")

           
           

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
                iniciar_automato = parametro_const.parametro_const(self.list,self.n, self.erro,self.token)
                iniciar_automato.E3()

            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ',' or ']'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected ',' or ']'\n")
