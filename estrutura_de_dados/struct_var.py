
import struct

class struct_var:
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
            if self.list[0] == "int" or self.list[0] == "real" or self.list[0] == "string" or self.list[0] == "boolean" or self.token[0] == "IDE":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                 self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'int', 'real', 'string', 'boolean' or IDE\n")
                 self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'int', 'real', 'string', 'boolean' or IDE\n")


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
            if self.list[0] == ";":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                if self.list[0] ==  "int" or self.list[0] == "real" or self.list[0] == "string" or self.list[0] == "boolean" or self.token[0] == "IDE":
                    self.E0()
                else:
                    iniciar_automato = struct.struct(self.list,self.n, self.erro,self.token)
                    iniciar_automato.E4()
            elif self.list[0] == "[":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E3()
            
            elif self.list[0] == ',':
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ',', '[' or ';'\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected: ',', '[' or ';'\n")
    
    def E3(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.token) > 0:
            if self.token[0] == "NRO" or self.token[0] == "IDE":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E4()
            
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'NRO' or 'IDE' \n")
                self.E4()
        else:
            self.erro.append("ERROR: Line-final Expected: 'NRO' or 'IDE'\n")

    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "]":
                self.token.pop(0)
                self.list.pop(0)
                self.n.pop(0)
                self.E2()
            
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ']'\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected: ']'\n")
        

