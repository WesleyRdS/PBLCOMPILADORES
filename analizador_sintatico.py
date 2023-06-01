class analizador_sintatico:
    def __init__(self,arquivo):
        self.LinhaAtual = [] #vetor com linha dos respectivos toks
        self.linha = [] #vetor com os tokens lidos
        self.identificacao = []
        self.arq = arquivo #arquivo lido
        self._arquivo = open(arquivo, "r", encoding="UTF-8") #abertura de arquivo no modo leitura

    def lerArquivo(self):
        self.linhaAtual = self._arquivo.read()
        linha_reserva = self.linhaAtual.split("\n") #transfora o arquivo em uma lista
        while len(linha_reserva) > 0: 
            vetor_reserva = linha_reserva[0].split() #separa as saidas do analisador lexico
            del linha_reserva[0] #remove a linha da saida ja lida
            self.linha.append(vetor_reserva[2]) #Obtem so os tokens
            self.identificacao.append(vetor_reserva[1])
            self.LinhaAtual.append(vetor_reserva[0]) #obtem a linha do token obtido 
            vetor_reserva.clear()
        return self.linha #retorna todos os tokens


 
                        


teste = analizador_sintatico("teste.txt")
teste.lerArquivo()
print(teste.linha)
print(teste.LinhaAtual)
print(teste.identificacao)