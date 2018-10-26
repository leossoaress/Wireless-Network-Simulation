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
        #Pacotes esperando para mandarem
        self._waitingPackages = []
        #Pacotes lidos
        self._readedPackages = []
        #Pacote enviando
        self._sending = False
        #Pacote recebendo
        self._receiving = False
        #Pacote recebido com sucesso
        self._received = False
    


    #Função responsável a enviar a um vizinho especifico
    def sendPackage(self):
    
        self._mediumacess = self.mediumAcess()

        #Testa se o meio está livre e se o host não está em backoff 
        if(self._sending == False and self._receiving == False and self._mediumacess == True and self._phyLayer._sendPackages != [] and self._backoff == 0):
            print("ID",self._phyLayer._id,": Inicio do envio do pacote!")
            package = self._phyLayer._sendPackages[0]
            self._sendDuration = package._duration
            self._phyLayer.sendPackage()
            self._sending = True

        #Caso o meio estiver ocupado o host entrará em backoff
        elif(self._backoff == 0 and self._phyLayer._sendPackages != []):
            self._waitingPackages.append(self._phyLayer._sendPackages[0])
            self._backoff = randint(self._phyLayer._sendPackages[-1]._duration, self._phyLayer._sendPackages[-1]._duration + 5)
            print("ID",self._phyLayer._id,": Host sofreu backoff de ", self._backoff)

        elif(self._backoff > 0):
            self._backoff -= 1
            
        elif(self._sending == True):
            self._sendDuration -= 1
            if(self._sendDuration == 0):
                self._sending = False
                print("ID",self._phyLayer._id,": Pacote enviado!")
            else:
                print("ID",self._phyLayer._id,": Enviando pacote!")




    #Função responsável para descartar os pacotes que não são para o host
    def receivePackage(self, id):
        
        if(self._phyLayer._receivePackages != [] and self._sending == False and self._receiving == False):
            package = self._phyLayer._receivePackages.pop(0)
            self._receiveDuration = package._duration
            self._receiving = True
            print("ID",self._phyLayer._id,": Inicio do recebimento do pacote!")

            if(package._headers[0]._idDest == id):
                self._readedPackages.append(package)
            elif(package._headers[0]._idDest == -1):
                self._readedPackages.append(package)
        
        elif(self._receiving == True):
            self._receiveDuration -= 1
            if(self._receiveDuration == 0):
                self._receiving = False
                print("ID",self._phyLayer._id,": Pacote recebido!")
            else:
                print("ID",self._phyLayer._id,": Recebendo pacote!")

    #Funcação responsável para detectar o meio
    def mediumAcess(self):
        if(self._phyLayer._receivePackages == []):
            return True
        return False 
