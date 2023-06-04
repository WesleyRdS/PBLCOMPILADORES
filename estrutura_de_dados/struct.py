import estrutura_de_dados.struct_var
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
import bloco_start
import estrutura_de_dados.struct

import FP.func
import FP.procedu

import bloco_start
import analizador_lexico
import analizador_sintatico

class struct:
    def __init__(self, lista, linha, arquivo, classe,remetente):
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
                iniciar_automato = estrutura_de_dados.struct_var.struct_var(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            else:
                if len(self.list) > 0:
                    if self.list[0] == "function" or self.list[0] == "procedure":
                        self.E5()
                    else:
                        self.E4()
                else:
                    self.E4()
        
        else:
            self.erro.append("ERROR: Line-final Expected: '}'\n")
    
    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "}":
                self.list.pop(0)
                self.token.pop(0)
                self.n.pop(0)
                if len(self.remetente) > 0:
                    if self.remetente[0] == "func" and len(self.list)>0:
                        self.remetente.pop(0)
                        iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E6()
                    elif self.remetente[0] == "proc":
                        self.remetente.pop(0)
                        iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E5()
                    elif self.remetente[0] == "start":
                        self.remetente.pop(0)
                        iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E2()
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
                        iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "struct":
                        self.E0()
                    else:
                        iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()

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
                    iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                    iniciar_automato.E0()
                elif self.list[0] == "struct":
                    self.E0()
                else:
                    iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                    iniciar_automato.E0()


            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: '}'\n")
                if len(self.list)>0:
                    if self.list[0] == "var":
                        iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token, self.remetente)
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
                    elif self.list[0] == "const":
                        iniciar_automato = constante.automato_bloco_const.bloco_const(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    else:
                        iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
        else:
            self.erro.append("ERROR: Line-final Expected: '}'\n")

    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0:
            if self.list[0] == "procedure":
                self.remetente.insert(0,"struct")
                iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "function":
                self.remetente.insert(0,"struct")
                iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            else:
                self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected: 'function' or 'procedure'\n")
                self.E4()
        else:
            self.erro.append("ERROR: Line-final Expected: 'function' or 'procedure'\n")