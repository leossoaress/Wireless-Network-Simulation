from headers import Header

class Package:

    #Construtor da classe Package
    def __init__(self, message, duration):

        #Identificador do pacote
        self._id = -1

        #Define a lista de cabeçalhos
        self._headers = []

        #Carga útil do pacote
        self._data = message

        #Duração da mensagem em unidades de tempo
        self._duration = duration

    #Função que adiciona novos cabeçalhos na lista
    def addHeader(self, header):
        self._headers.append(header)

    #Função estática que retorna um pacote criado
    @staticmethod
    def createPackage(message, duration):
        return Package(message, duration)

    #Função que exibe as informações do pacote
    def printPackage(self):
        print("Data: ", self._data)

    
    def getLinkHeader(self):
        for header in self._headers:
            if(header._type == "LINK"):
                return header

    def getNetworkHeader(self):
        for header in self._headers:
            if(header._type == "NETWORK"):
                return header

    def updateSequence(self, sequence):
        for header in self._headers:
            if(header._type == "NETWORK"):
                header._sequenceList = sequence
