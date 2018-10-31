from physicallayer import PhysicalLayer
from package import Package
from headers import Header
from random import randint

class LinkLayer:

    #Construtor da classe LinkLayer
    def __init__(self, phyLayer):
        #Qunatidade de tempo que o host tem que esperar caso o meio esteja ocupado
        self._backoff = 0
        #Duração que o meio físico estará ocupado enviando
        self._sendDuration = 0
         #Duração que o meio físico estará ocupado recebenfo
        self._receiveDuration = 0
        #Flag para informar se o meio está livre
        self._mediumacess = True
        #Inicializa a cama física
        self._phyLayer = phyLayer
        #Pacotes lidos
        self._readedPackages = []
        #Pacote enviando
        self._sending = False
        #Pacote recebendo
        self._receiving = False
        #Pacote recebido com sucesso
        self._received = False
        self._receivingPackage = []
        self._counter = 0
        self._free = False


    #Função responsável a enviar a um vizinho especifico
    def sendPackage(self):
    
        self._mediumacess = self.mediumAcess()

        #Testa se o meio está livre e se o host não está em backoff 
        if(self._mediumacess == True):
            
            if(self._phyLayer._sendPackages != []):

                if(self._backoff == 0):
                    print("ID",self._phyLayer._id,": Host envia para os vizinhos")
                    self._phyLayer.sendPackage()
                
                else:
                    self._backoff -= 1

        #Caso o meio estiver ocupado o host entrará em backoff
        elif(self._phyLayer._sendPackages != []):
    
            if(self._backoff == 0):
                self._backoff = randint(self._sendDuration, self._sendDuration + 5)
                print("ID",self._phyLayer._id,": Host sofreu backoff de ", self._backoff)


    #Função responsável para descartar os pacotes que não são para o host
    def receivePackage(self):

        if(len(self._phyLayer._receivePackages) > 1):
            self._phyLayer._receivePackages.clear()
            print("ID",self._phyLayer._id,": Colisão neste host")
        
        elif(len(self._phyLayer._receivePackages) == 1):

                package = self._phyLayer._receivePackages.pop(0)
                header = package.getLinkHeader()

                if(header._macDestiny == self._phyLayer._id):    
                    self._readedPackages.append(package)
                elif(header._macDestiny  == -1):
                    self._readedPackages.append(package)

    #Funcação responsável para detectar o meio
    def mediumAcess(self):
        if(self._phyLayer._receivePackages == []):
            return True
        return False 


    def addPackage(self, package, macDestiny):
        
        header = Header("LINK", self._phyLayer._id, macDestiny, self._counter, -1, -1, -1)
        package.addHeader(header)

        self._phyLayer._sendPackages.append(package)