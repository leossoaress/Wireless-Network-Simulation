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