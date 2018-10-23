from sys import getsizeof

class Package:

    #Construtor da classe Package
    def __init__(self, message):

        #Define a lista de cabeçalhos
        self._headers = []

        #Carga útil do pacote
        self._data = message

        #Duração da mensagem em unidades de tempo
        self._duration = len(message)

    #Função que adiciona novos cabeçalhos na lista
    def addHeader(self, header):
        self._headers.append(header)

    #Função estática que retorna um pacote criado
    @staticmethod
    def createPackage(message):
        return Package(message)