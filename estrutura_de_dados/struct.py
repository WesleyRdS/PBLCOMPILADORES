import estrutura_de_dados.struct_var


class struct:
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
            if self.list[0] == "struct":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'struct'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'struct'\n")

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
        if len(self.list) > 0:
            if self.list[0] == "{":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E3()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '{'\n")
                self.E3()
        else:
            self.erro.append("ERROR: Line-final Expected: '{'\n")

    def E3(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "int" or self.list[0] == "real" or self.list[0] == "string" or self.list[0] == "boolean" or self.list[0] == "true" or self.list[0] == "false" or self.token[0] == "NRO" or self.token[0] == "IDE":
                iniciar_automato = estrutura_de_dados.struct_var.struct_var(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            else:
                self.E4()
        else:
            self.E4()
    
    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "}":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '}'\n")
        else:
            self.erro.append("ERROR: Line-final Expected: '}'\n")