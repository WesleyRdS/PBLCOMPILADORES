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
import if_while.while_a


class parenteses:
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
                case "(":
                    self.list.pop(0)
                    self.n.pop(0)
                    self.token.pop(0)
                    self.remetente.insert(0,"par")
                    iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                    iniciar_automato.E0()
                case _:
                    self.erro.append("ERROR: Line-"+self.n[0]+" Read "+self.list[0]+  " Expected '('\n")
                    self.E0()
        else:
            self.erro.append("ERROR: Line-final Expected '('\n")
    

    def E1(self):
        print(self.list)
        print(self.n)
        print(self.token)
        if len(self.list) > 0 and len(self.remetente) > 0:
            self.list.pop(0)
            self.n.pop(0)
            self.token.pop(0)
            print(self.list[0]+"---------------aquiiiiiiiiiiiiiiiiiiiiiiiiiii-------------------"+self.remetente[0])
            if self.list[0] == "{" and self.remetente[0] == "while":
                self.remetente.pop(0)
                iniciar_automato = if_while.while_a.while_a(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            elif self.list[0] == "then" and self.remetente[0] == "if":
                self.remetente.pop(0)
                iniciar_automato = if_while.ifthen.ifthen(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            elif self.list[0] != ";" and self.remetente[0] == "art":
                self.remetente.pop(0)
                iniciar_automato = exp.exp_aritimetica.exp_aritimetica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            elif self.list[0] == ";" and self.remetente[0] == "art":
                self.remetente.pop(0)
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E8()
            elif self.list[0] == ";" and self.remetente[0] == "art_v":
                self.remetente.pop(0)
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E8()
            elif self.list[0] != ";" and self.remetente[0] == "log":
                self.remetente.pop(0)
                iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            elif self.list[0] == ";" and self.remetente[0] == "log":
                self.remetente.pop(0)
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E8()
            elif self.list[0] == ")" and self.remetente[0] != "par":
                self.erro.append("ERROR: Line-"+self.n[0]+" '(' referring to ')' not found \n")
                self.E1()
            elif self.list[0] == ")" and self.remetente[0] == "par":
                self.remetente.pop(0)
                self.E1()
            else:
                self.E2()

        elif len(self.list) > 0 and len(self.remetente) == 0:
            if self.list[0] == ")": 
                self.list.pop(0)
                self.n.pop(0)
                self.token.pop(0)
                self.E1()
            else:
                self.E2()
        else:
            return self.list
    
    def E2(self):
        if len(self.list) > 0:
            if self.token[0] == "ART":
                iniciar_automato = exp.exp_aritimetica.exp_aritimetica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            elif self.list[0] == "=":
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E1()
            elif self.token[0] == "REL":
                iniciar_automato = exp.exp_logica.exp_logica(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E3()
            else:
                iniciar_automato = atribuir_valor.atribuir_valor(self.list,self.n, self.erro,self.token,self.remetente)
                iniciar_automato.E8()
        else:
            self.erro.append("ERROR: Line-Final expected 'ART' ,'REL' or 'DEL' \n")
           


        
            
        


