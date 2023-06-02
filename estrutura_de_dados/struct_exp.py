import sys
sys.path.insert(1,'./FP')

import FP.parametro_function
class struct_exp:
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
            if self.token[0] == "IDE":
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
        if len(self.list) > 0:
            if self.list[0] == ".":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E2()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '.'\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected: '.'\n")

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.token) > 0:
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
            if self.list[0] == ";":
                self.E4()
            if self.list[0] == "(":
                self.E7()
            else:
                self.E5()
        else:
            self.erro.append("ERROR: Line-final Expected: ';' or '='\n")

    
    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ";":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ';'\n")
        else:
            self.erro.append("ERROR: Line-final Expected: ';'\n")

    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "=":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E6()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '='\n")
                self.E6()
        else:
            self.erro.append("ERROR: Line-final Expected: '='\n")

    def E6(self):
        if len(self.list) > 0:
            if self.token[0] == 'NRO' or self.token[0] == 'CAC' or self.token[0] == 'IDE' or self.list[0] == 'true' or self.list[0] == 'false':
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E4()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'int', 'real', 'string' or boolean\n")
                self.E4()
        else:
            self.erro.append("ERROR: Line-final Expected: 'int', 'real', 'string' or boolean\n")


    def E7(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "(":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                iniciar_automato = FP.parametro_function.parametro_function(self.list,self.n, self.erro,self.token,"struct_func")
                iniciar_automato.E0()
            else:
                self.E3()
        else:
            self.E4()
    
    
    def E8(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ")":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E4()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ')'\n")
                self.E4()
        else:
            self.erro.append("ERROR: Line-final Expected: ')'\n")
            










