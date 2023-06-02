import sys
sys.path.insert(1,'./bloco_const')
sys.path.insert(1,'./bloco_var')
sys.path.insert(1,'./estrutura_de_dados')
sys.path.insert(1,'./exp')
sys.path.insert(1,'./if_while')
import automato_bloco_const
import automato_bloco_var
import vetor
import struct
import struct_exp
import exp_aritimetica
import exp_logica
import atribuir_valor
import ifthen
import while_a
import func
import procedu
import analizador_lexico

#vetor_lista = ["var",   '{', "int",  "i",  "=",  "2",   ",",   "j",  "=",   "7",   ",",   "k",   "=", "5.65",   ";", "boolean",   "h",   "=" ,"true", ";","}"]
#vetor_token = ["PRE", "DEL", "PRE","IDE","REL","NRO", "DEL", "IDE","REL", "NRO", "DEL", "IDE", "REL",  "NRO", "DEL",     "PRE", "IDE",  "REL", "PRE", "DEL", "DEL"]
#vetor_linha = ["1"  ,   "1",   "2",  "2",  "2",  "2",   "2",   "2",  "2",   "2",   "2",   "2",   "2",    "2",   "2",       "3",   "3",    "3",   "3", "3", "4"]


teste = analizador_lexico.analizador_lexico("teste.txt")
teste.E0()
escrever = open("saida.txt", "a")
for lin in teste.simbolos:
  escrever.write(str(lin[0]) + ", " + lin[1] + ", " + lin[2] + "\n")







