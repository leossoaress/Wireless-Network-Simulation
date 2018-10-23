from physicallayer import PhysicalLayer
from package import Package
from header import Header
from random import randint

class LinkLayer:

    #Construtor da classe LinkLayer
    def __init__(self, phyLayer):
        #Qunatidade de tempo que o host tem que esperar caso o meio esteja ocupado
        self._backoff = 0
        #Flag que informa se o host está recebendo dados
        self._receiving = False
        #Flag que informa se o host está enviando dados
        self._sending = False
        #Duração que o meio físico estará ocupado
        self._sendDuration = 0
        #Flag para informar se o meio está livre
        self._mediumacess = True
        #Inicializa a cama física
        self._phyLayer = phyLayer

    #Função responsável a enviar a um vizinho especifico
    def sendPackage(self, package, idSource, idDest):
        #Testa se o meio está livre e se o host não está em backoff 
        if(self._mediumacess == True and self._backoff == 0):
            self._sending = True
            self._phyLayer.getMediumAcess()
            self._phyLayer._package.append(package)
            self._phyLayer._package[-1].addHeader(Header(1, idSource, idDest))
            self._phyLayer.sendPackage()
            self._sendDuration = package._duration
        #Caso o meio estiver ocupado o host entrará em backoff
        elif(self._backoff == 0):
            self._backoff = randint(self._phyLayer._package[-1]._duration, self._phyLayer._package[-1]._duration + 5)

    #Função responsável para descartar os pacotes que não são para o host
    def receivePackage(self, id):
        if(self._phyLayer._package[-1]._headers[0]._idDest != id):
            self._phyLayer._package.remove(self._phyLayer._package[-1])
        else:
            self._receiving = True
            self._sendDuration = self._phyLayer._package[-1]._duration

    #Função que atualiza as informações do host por unidade de tempo
    def update(self):
        if(self._phyLayer._package != [] or self._sending == True):  
            self._sendDuration = self._sendDuration - 1
            if(self._sendDuration < 0):
                self._receiving = False
                self._sending = False

        if(self._backoff > 0):
            self._backoff = self._backoff - 1