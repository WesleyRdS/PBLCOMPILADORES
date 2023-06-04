import os
caminho = r""+os.path.dirname(os.path.realpath(__file__))+"\\files"
os.chdir(caminho)
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

import FP.func
import FP.procedu

import bloco_start
import analizador_lexico
import analizador_sintatico


#vetor_lista = ["var",   '{', "int",  "i",  "=",  "2",   ",",   "j",  "=",   "7",   ",",   "k",   "=", "5.65",   ";", "boolean",   "h",   "=" ,"true", ";","}"]
#vetor_token = ["PRE", "DEL", "PRE","IDE","REL","NRO", "DEL", "IDE","REL", "NRO", "DEL", "IDE", "REL",  "NRO", "DEL",     "PRE", "IDE",  "REL", "PRE", "DEL", "DEL"]
#vetor_linha = ["1"  ,   "1",   "2",  "2",  "2",  "2",   "2",   "2",  "2",   "2",   "2",   "2",   "2",    "2",   "2",       "3",   "3",    "3",   "3", "3", "4"]


termo = []
identificador = []
l = []

for arq in os.listdir():
  if arq.endswith(".txt") and not(arq.endswith("-saida.txt")) and not(arq.endswith("-saida_sintatica.txt")):
    caminho_lido = f"{caminho}\{arq}"
    teste = analizador_lexico.analizador_lexico(caminho_lido)
    teste.E0()
    arq = arq.replace(".txt","-saida.txt")
    caminho_saida = f"{caminho}\{arq}"
    with open(caminho_saida, "a") as escrever:
      for lin in teste.simbolos:
        escrever.write(str(lin[0]) + ", " + lin[1] + ", " + lin[2] + "\n")

for arq in os.listdir():
  saida_erros = []
  if arq.endswith("-saida.txt") and not(arq.endswith("-saida_sintatica.txt")):
    caminho_saida = f"{caminho}\{arq}"
    sintaxe = analizador_sintatico.analizador_sintatico(caminho_saida)
    sintaxe.lerArquivo()
    arq = arq.replace("-saida.txt","-saida_sintatica.txt")
    caminho_saida = f"{caminho}\{arq}"
    saida = []
    termo = sintaxe.linha
    identificador = sintaxe.identificacao
    remetente = []
    l = sintaxe.LinhaAtual
    if len(termo) > 0:
      if termo[0] == "var":
        automato = variavel.automato_bloco_var.bloco_var(termo, l, saida, identificador,remetente)
        automato.E0()
        termo = automato.list
        l = automato.n
        saida = automato.erro
        identificador = automato.token
        saida_erros = automato.erro
      elif termo[0] == "const":
        automato = constante.automato_bloco_const.bloco_const(termo, l, saida, identificador,remetente)
        automato.E0()
        termo = automato.list
        l = automato.n
        saida = automato.erro
        identificador = automato.token
        saida_erros = automato.erro
      elif termo[0] == "procedure":
        automato = FP.procedu.procedu(termo, l, saida, identificador,remetente)
        automato.E0()
        termo = automato.list
        l = automato.n
        saida = automato.erro
        identificador = automato.token
        saida_erros = automato.erro
      elif termo[0] == "function":
        automato = FP.func.func(termo, l, saida, identificador,remetente)
        automato.E0()
        termo = automato.list
        l = automato.n
        saida = automato.erro
        identificador = automato.token
        saida_erros = automato.erro
      elif termo[0] == "struct":
        automato = estrutura_de_dados.struct.struct(termo, l, saida, identificador,remetente)
        automato.E0()
        termo = automato.list
        l = automato.n
        saida = automato.erro
        identificador = automato.token
        saida_erros = automato.erro
      else:
        automato = bloco_start.bloco_start(termo, l, saida, identificador,remetente)
        automato.E0()
        termo = automato.list
        l = automato.n
        saida = automato.erro
        identificador = automato.token
        saida_erros = automato.erro
      with open(caminho_saida, "a") as escrever:
        if len(saida_erros) == 0:
          escrever.write("Compilation success: No errors")
        else:
          escrever.write("Errors found: \n")
        for i in saida_erros:
          escrever.write(i)


  


  



    
  

        

    







