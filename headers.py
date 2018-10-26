class Header:

    #Construtor da classe Header
    def __init__(self, type, idSource, idDest):

        #Define o tipo de cabeçalho (enlace ou rede)
        self._type = type

        #Define o destino para a camada correspondente
        self._idDest = idDest

        #Define o remetente do pacote
        self._idSource = idSource