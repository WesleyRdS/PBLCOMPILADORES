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
import FP.procedu
import bloco_start
import constante.automato_bloco_const


class func:
    def __init__(self, lista, linha, arquivo, classe, remetente):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe
        self.remetente = remetente

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "function":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E1()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'function'\n")
                self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected: 'function'\n")


    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "int" or self.list[0] == "real" or self.list[0] == "string" or self.list[0] == "boolean" or self.token[0] == "IDE":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E2()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'int', 'real', 'string' or 'IDE'\n")
                self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected: 'int', 'real', 'string' or 'IDE'\n")

    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
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
            if self.list[0] == "(":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                if len(self.list) > 0:
                    if self.list[0] == ")":
                        self.E4()
                    else:
                        self.remetente.insert(0,"func")
                        iniciar_automato = FP.parametro_functionD.parametro_functionD(self.list,self.n, self.erro,self.token,self.remetente)
                        iniciar_automato.E0()
                else:
                    self.erro.append("ERROR: Line-final Expected: ')'\n")
            elif self.list[0] == ")":
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                self.E4()        
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '('\n")
                self.remetente.insert(0,"func")
                iniciar_automato = FP.parametro_functionD.parametro_functionD(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
        else:
            self.erro.append("ERROR: Line-final Expected: '('\n")


    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == ")":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                self.E5()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: ')'\n")
                self.E5()
        else:
            self.erro.append("ERROR: Line-final Expected: ')'\n")

    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "{":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E6()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '{'\n")
                    self.E6()
        else:
            self.erro.append("ERROR: Line-final Expected '{'\n")


    def E6(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "var":
                self.remetente.insert(0,"func")
                iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0() 
            elif self.token[0] == "IDE":
                self.remetente.insert(0,"func")
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "if":
                self.remetente.insert(0,"func")
                iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "while":
                self.remetente.insert(0,"func")
                iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "struct":
                self.remetente.insert(0,"func")
                iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "procedure":
                self.remetente.insert(0,"func")
                iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "function":
                self.remetente.insert(0,"func")
                self.E0()
            elif self.list[0] == "print":
                self.remetente.insert(0,"func")
                iniciar_automato = PR.printar.printar(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "read":
                self.remetente.insert(0,"func")
                iniciar_automato = PR.reader.reader(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            else:
                self.E7()
        else:
            self.erro.append("ERROR: Line-final Expected 'return'\n")

    def E7(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "return":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E8()
            else:
               self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'return'\n")
               self.E8()
        else:
            self.erro.append("ERROR: Line-final Expected 'return'\n")

    def E8(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.token[0] == "NRO" or self.token[0] == "IDE" or self.list[0] == "true" or self.list[0] == "false" or self.token[0] == "CAC":
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E9()
            else:
               self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'IDE', 'int', 'real', 'true', 'false' or 'string'\n")
               self.E9()
        else:
            self.erro.append("ERROR: Line-final Expected 'IDE', 'int', 'real', 'true', 'false' or 'string'\n")

    def E9(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case ";":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E10()
                    
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ';'\n")
                    self.E10()
                 
        else:
            self.erro.append("ERROR: Line-final Expected ';'\n")


    def E10(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "}":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    if len(self.remetente) > 0 and len(self.list)>0:
                        if self.remetente[0] == "func":
                            self.remetente.pop(0)
                            self.E6()
                        elif self.remetente[0] == "proc":
                            self.remetente.pop(0)
                            iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E5()
                        elif self.remetente[0] == "start":
                            self.remetente.pop(0)
                            iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E2()
                        elif self.remetente[0] == "if":
                            self.remetente.pop(0)
                            iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E5()
                        elif self.remetente[0] == "while":
                            self.remetente.pop(0)
                            iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E4()
                        elif self.remetente[0] == "struct":
                            self.remetente.pop(0)
                            iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E5()
                        

                        elif self.list[0] == "var":
                            iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "const":
                            iniciar_automato = constante.automato_bloco_const.bloco_const(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "procedure":
                            iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "function":
                            self.E0()
                        elif self.list[0] == "struct":
                            iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        else:
                            iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()

                    else:
                        if len(self.list)>0:
                            if self.list[0] == "var":
                                iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "procedure":
                                iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "function":
                                self.E0()
                            elif self.list[0] == "struct":
                                iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "const":
                                iniciar_automato = constante.automato_bloco_const.bloco_const(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            else:
                                iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '}'\n")
                    if self.list[0] == "var":
                        iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "procedure":
                        iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "function":
                        self.E0()
                    elif self.list[0] == "struct":
                        iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "const":
                        iniciar_automato = constante.automato_bloco_const.bloco_const(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    else:
                        iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                 
        else:
            self.erro.append("ERROR: Line-final Expected '}'\n")

