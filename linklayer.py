from physicallayer import PhysicalLayer
from lists import indicesToSend, nextTosend
from package import Package
from headers import Header
from random import randint

class LinkLayer:

    #Construtor da classe LinkLayer
    def __init__(self, phyLayer):
        #Qunatidade de tempo que o host tem que esperar caso o meio esteja ocupado
        self._backoff = 0
        #Flag para informar se o meio está livre
        self._mediumacess = True
        #Inicializa a cama física
        self._phyLayer = phyLayer
        #Pacotes lidos
        self._readedPackages = []


    #Função que envia os pacotes da camada de enlace
    def sendPackage(self):
        
        self._mediumacess = self.mediumAcess()

        #Testa se o meio está livre 
        if(self._mediumacess == True):
            
            #Verifica se host não está em backoff 
            if(self._phyLayer._sendPackages != []):

                if(self._backoff == 0):
                    self._phyLayer.sendPackage()
                
                else:
                    nextTosend.append(self._phyLayer._id)
                    self._backoff -= 1

        #Caso o meio estiver ocupado o host entrará em backoff
        elif(self._phyLayer._sendPackages != []):
            
            if(self._backoff == 0):
                self._backoff = randint(2, 7)
                print("ID",self._phyLayer._id,": Host sofreu backoff de ", self._backoff)
                nextTosend.append(self._phyLayer._id)


    #Função que recebe e trata o pacote recebido na camada de enlace
    def receivePackage(self):
        
        #Verifica se foi recebido mais de um pacote no mesmo instante de tempo, colisão
        if(len(self._phyLayer._receivePackages) > 1):
            self._phyLayer._receivePackages.clear()
            print("ID",self._phyLayer._id,": Colisão neste host")
        
        #Verifica se tem pacote para recever
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

    #Função que adiciona um pacote na camada de enlace
    def addPackage(self, package, macDestiny):
        
        header = Header("LINK", self._phyLayer._id, macDestiny, 0, -1, -1, -1)
        package.addHeader(header)
        self._phyLayer._sendPackages.append(package)