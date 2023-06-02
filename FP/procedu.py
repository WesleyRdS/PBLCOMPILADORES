import sys
sys.path.insert(1,'./FP')
sys.path.insert(1,'./bloco_var')
sys.path.insert(1,'./estrutura_de_dados')
sys.path.insert(1,'./exp')
sys.path.insert(1,'./if_while')
sys.path.insert(1,'./PR')
import PR.printar
import PR.reader
import variavel.automato_bloco_var
import estrutura_de_dados.vetor
import estrutura_de_dados.struct
import estrutura_de_dados.struct_exp
import exp.exp_aritimetica
import exp.exp_logica
import atribuir_valor
import if_while.ifthen
import if_while.while_a
import FP.parametro_functionD
import FP.func

class procedu:
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
            if self.list[0] == "procedure":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'procedure'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'procedure'\n")



    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
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
            if self.list[0] == "(":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == ")":
                        self.E3()
                    else:
                        iniciar_automato = FP.parametro_functionD.parametro_functionD(self.list,self.n, self.erro,self.token,"proc")
                        iniciar_automato.E0()
                else:
                    self.erro.append("ERROR: Line-final Expected: ')'\n")
            elif self.list[0] == ")":
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                self.E3()        
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                iniciar_automato = FP.parametro_functionD.parametro_functionD(self.list,self.n, self.erro,self.token,"proc")
                iniciar_automato.E0()
        else:
            self.erro.append("ERROR: Line-final Expected: '('\n")


    def E3(self):
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

    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "{":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E5()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '{'\n")
                    self.E5()
        else:
            self.erro.append("ERROR: Line-final Expected '{'\n")


    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "var":
                iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0() 
            elif self.token[0] == "IDE":
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,"proc")
                iniciar_automato.E0()
            elif self.list[0] == "if":
                iniciar_automato = if_while.ifthen(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "while":
                iniciar_automato = if_while.while_a(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "struct":
                iniciar_automato = estrutura_de_dados.struct(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "procedure":
                iniciar_automato = procedu(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "function":
                iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "print":
                iniciar_automato = PR.printar(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            elif self.list[0] == "read":
                iniciar_automato = PR.reader(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0()
            else:
                self.E6()
        else:
            self.erro.append("ERROR: Line-final Expected '}'\n")

    
    def E6(self):
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