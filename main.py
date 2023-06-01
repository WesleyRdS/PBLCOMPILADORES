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
#vetor_lista = ["var",   '{', "int",  "i",  "=",  "2",   ",",   "j",  "=",   "7",   ",",   "k",   "=", "5.65",   ";", "boolean",   "h",   "=" ,"true", ";","}"]
#vetor_token = ["PRE", "DEL", "PRE","IDE","REL","NRO", "DEL", "IDE","REL", "NRO", "DEL", "IDE", "REL",  "NRO", "DEL",     "PRE", "IDE",  "REL", "PRE", "DEL", "DEL"]
#vetor_linha = ["1"  ,   "1",   "2",  "2",  "2",  "2",   "2",   "2",  "2",   "2",   "2",   "2",   "2",    "2",   "2",       "3",   "3",    "3",   "3", "3", "4"]


vetor_lista = ["if",
               "(",
               "c",
               ">",
               "b",
               ")",
               "then",

               "{",
               "b",
               "==",
                "c",
                "+",
                "2",
                ";",

               "}"
               

                 ]
vetor_token = [ "PRE",
                "DEL",
                "IDE",
                "REL",
                "IDE",
                "DEL",
                "PRE",

              "DEL",
              "IDE",
                "REL",
                "IDE",
                "ART",
                "NRO",
                "DEL",

                "DEL"
               
               ]
vetor_linha = ["1",  
                "2",   
                "3",  
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15"

                ]


arquivo = []
teste = ifthen.ifthen(vetor_lista,vetor_linha,arquivo,vetor_token)
teste.E0()

saida = open("teste.txt", "a")
for i in teste.erro:
    saida.write(i)
print(teste.erro)