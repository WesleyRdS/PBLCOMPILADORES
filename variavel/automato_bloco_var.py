import variavel.parametro_var
import sys 
sys.path.insert(1,'./constante')
sys.path.insert(1,'./bloco_var')
sys.path.insert(1,'./estrutura_de_dados')
sys.path.insert(1,'./exp')
sys.path.insert(1,'./if_while')
sys.path.insert(1,'./PR')
sys.path.insert(1,'./FP')
import constante.automato_bloco_const

import variavel.automato_bloco_var

import estrutura_de_dados.struct
import if_while.ifthen
import if_while.while_a
import FP.func
import FP.procedu

import bloco_start
import analizador_lexico
import analizador_sintatico

class bloco_var:
    def __init__(self, lista, linha, arquivo,classe,remetente):
        self.list = lista
        self.erro = arquivo
        self.n = linha
        self.token = classe
        self.remetente = remetente

    def E0(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "var":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E1()  
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'var'\n")
                    self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected 'var'\n")

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "{":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E2()  
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '{'\n")
                    self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected '{'\n")


    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "}":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    if len(self.list) > 0 and len(self.remetente) > 0:
                        if self.remetente[0] == "func":
                            self.remetente.pop(0)
                            iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
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
                        elif self.list[0] == "const":
                            iniciar_automato = constante.automato_bloco_const.bloco_const(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "procedure":
                            iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "function":
                            iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "struct":
                            iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        else:
                            iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                    else:
                        if len(self.list) > 0:
                            if self.list[0] == "const":
                                iniciar_automato =constante.automato_bloco_const.bloco_const(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "procedure":
                                iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "function":
                                iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "struct":
                                iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            else:
                                iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()

                case _:
                    #se tiver declaração de inteiro, real, booleano ou string ou o proprio valor vai para o automato de paramatros das variaveis
                    #La checara se a forma sintatica do parametro do bloco esta correta 
                    if self.list[0] == 'true' or self.list[0] == 'false' or self.token[0] == "IDE" or self.token == "NRO" or self.list[0] == 'int' or self.list[0] == 'boolean' or self.list[0] == 'string' or self.list[0] == 'real':
                        iniciar_automato = variavel.parametro_var.parametro_var(self.list, self.n, self.erro, self.token,self.remetente)
                        iniciar_automato.E0()

                    else:
                        self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '}'\n")
                        if len(self.list) > 0:
                            if self.list[0] == "const":
                                iniciar_automato =constante.automato_bloco_const.bloco_const(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "procedure":
                                iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "function":
                                iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            elif self.list[0] == "struct":
                                iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
                            else:
                                iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                                iniciar_automato.E0()
        else:
            self.erro.append("ERROR: Line-final Expected '}'\n")
                        


