import sys
sys.path.insert(1,'./FP')
sys.path.insert(1,'./bloco_var')
sys.path.insert(1,'./estrutura_de_dados')
sys.path.insert(1,'./exp')
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
import FP.func
import FP.procedu
import bloco_start


class while_a:
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
        if(len(self.list)>0):
            match self.list[0]:
                case "while":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E1()  
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected 'while'\n")
                    self.E1()
        else:
            self.erro.append("ERROR: Line-final Expected 'while'\n")

    
    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "(":
                    self.remetente.insert(0,'while')
                    iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                    iniciar_automato.E0()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '('\n")
                    self.E2()
        else:
            self.erro.append("ERROR: Line-final Expected '('\n")


    def E2(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case ")":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E3()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected ')'\n")
                    self.E3()
        else:
            self.erro.append("ERROR: Line-final Expected ')'\n")


  

    def E3(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            match self.list[0]:
                case "{":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.E4()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '{'\n")
                    self.E4()
        else:
            self.erro.append("ERROR: Line-final Expected '{'\n")


    def E4(self):
        print(self.list)
        print(self.n)
        print(self.token)

        if len(self.list) > 0:
            if self.list[0] == "var":
                self.remetente.insert(0,"while")
                iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token)
                iniciar_automato.E0() 
            elif self.token[0] == "IDE":
                self.remetente.insert(0,"while")
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "if":
                self.remetente.insert(0,"while")
                iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "while":
                self.remetente.insert(0,"while")
                self.E0()
            elif self.list[0] == "procedure":
                self.remetente.insert(0,"while")
                iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "function":
                self.remetente.insert(0,"while")
                iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "print":
                self.remetente.insert(0,"while")
                iniciar_automato = PR.printar.printar(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            elif self.list[0] == "read":
                self.remetente.insert(0,"while")
                iniciar_automato = PR.reader.reader(self.list,self.n, self.erro,self.token, self.remetente)
                iniciar_automato.E0()
            else:
                self.E5()

    def E5(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if(len(self.list)>0):
            print("aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii--"+self.list[0])
            match self.list[0]:
                case "}":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    if len(self.remetente) > 0 and len(self.list)>0:
                        print("olhaaaaaaaaaaaaaaaaaaaaaaaaaa------"+self.remetente[0])
                        if self.remetente[0] == "func":
                            self.remetente.pop(0)
                            iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                            self.E6()
                        elif self.remetente[0] == "proc":
                            self.remetente.pop(0)
                            iniciar_automato = FP.procedu.procedu(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E5()
                        elif self.remetente[0] == "if":
                            self.remetente.pop(0)
                            iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E5()
                        elif self.remetente[0] == "start":
                            self.remetente.pop(0)
                            iniciar_automato = bloco_start.bloco_start(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E2()
                        elif self.remetente[0] == "while":
                            self.remetente.pop(0)
                            self.E4()

                        elif self.list[0] == "var":
                            iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "procedure":
                            self.E0()
                        elif self.list[0] == "function":
                            iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "struct":
                            iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "print":
                            iniciar_automato = PR.printar.printar(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "read":
                            iniciar_automato = PR.reader.reader(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "IDE":
                            iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "if":
                            iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token, self.remetente)
                            iniciar_automato.E0()
                        elif self.list[0] == "while":
                            self.E0()
                        
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '{'\n")
                    if self.list[0] == "var":
                        iniciar_automato = variavel.automato_bloco_var.bloco_var(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "procedure":
                        self.E0()
                    elif self.list[0] == "function":
                        iniciar_automato = FP.func.func(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "struct":
                        iniciar_automato = estrutura_de_dados.struct.struct(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "print":
                        iniciar_automato = PR.printar.printar(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "read":
                        iniciar_automato = PR.reader.reader(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "IDE":
                        iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "if":
                        iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token, self.remetente)
                        iniciar_automato.E0()
                    elif self.list[0] == "while":
                        self.E0()
        else:
            self.erro.append("ERROR: Line-final Expected '{'\n")

                    



    
