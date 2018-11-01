from physicallayer import PhysicalLayer
from linklayer import LinkLayer
from lists import indicesToSend
from package import Package
from headers import Header
from route import Route
import random

class NetworkLayer:

    #Construtor da classe Network
    def __init__(self, linkLayer): 
        
        #Camada de rede do host
        self._linkLayer = linkLayer
        #Lista de pacotes na camada de rede para serem enviados
        self._listPackages = []
        #Lista de número de sequencia dos pacotes de RREQ
        self._listRREQs = []
        #Lista de rotas para certo destino ainda não salvas
        self._waitingRouteToList = []
        #Lista de rotas
        self._routes = []


    #Função que manda o pacote de resposta de rota
    def sendRREP(self, macDestiny, sequence, route):
        
        #Cria um pacote e inseri o cabeçalho da camada de rede
        header = Header("NETWORK", self._linkLayer._phyLayer._id, macDestiny, -1, 1, -1, sequence)
        package = Package(route, 1)
        package.addHeader(header)
        
        print("ID", self._linkLayer._phyLayer._id, ": Enviando um RREP com destino para ", header._macDestiny)
        
        #Define a rota requisitada
        for index,mac in enumerate(header._sequenceList):
            if(mac == self._linkLayer._phyLayer._id):       
                nextDestiny = header._sequenceList[index+1]
                nextPackage = package
                self._linkLayer.addPackage(nextPackage, nextDestiny)
                break
       

    #Função que manda o pacote de requisição de rota
    def sendRREQ(self, macDestiny):
        
        #Inicializa uma sequencia e coloca o seu ID como primeiro
        sequence = []
        sequence.append(self._linkLayer._phyLayer._id)
        sequenceNumber = random.randint(1,128733788) 
        self._listRREQs.append(sequenceNumber)

        #Cria um pacote e inseri o cabeçalho da camada de rede
        header = Header ("NETWORK", self._linkLayer._phyLayer._id, macDestiny, -1, 0, sequenceNumber, sequence)
        package = Package("", 1)
        package.addHeader(header)
        
        print("ID", self._linkLayer._phyLayer._id, ": Enviando um RREQ com destino para ", header._macDestiny)
        self._linkLayer.addPackage(package, -1)
        
    #Função que recebe e trata o pacote recebido na camada de rede
    def receivePackage(self):

        #Chama a função de tratar pacote recebido na camada de enlace
        self._linkLayer.receivePackage()

        #Verifica se tem pacotes recebidos
        if(self._linkLayer._readedPackages != []):
            
            package = self._linkLayer._readedPackages.pop(0)
            header = package.getNetworkHeader()

            #Se o pacote for recebido for de dados
            if(header._request == -1):
                
                #Verifica se o pacote é para mim
                if(header._macDestiny == self._linkLayer._phyLayer._id):
                    print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote de dadis: ", package._data)
                else:
                    print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote de dados mas não é pra mim")
                    print("ID", self._linkLayer._phyLayer._id, ": Enviando pacote de dados para o nó seguinte")
                    for index,mac in enumerate(package._headers[0]._sequenceList):
                        if(mac == self._linkLayer._phyLayer._id):
                            nextDestiny = header._sequenceList[index-1]
                            break

                    package._headers.pop(1)
                    self._linkLayer.addPackage(package, nextDestiny)
                    indicesToSend.append(self._linkLayer._phyLayer._id)


            #Se o pacote for recebido for um RREQ
            elif(header._request == 0):
                
                print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote RREQ: ", header._sequenceNumber )
                
                #Verifica se eu já recebi esse RREQ
                if(not header._sequenceNumber in self._listRREQs):
                    self._listRREQs.append(header._sequenceNumber)
                    header._sequenceList.append(self._linkLayer._phyLayer._id)

                    #Verifica se o RREQ é para mim
                    if(header._macDestiny == self._linkLayer._phyLayer._id):
                        print("ID", self._linkLayer._phyLayer._id, ": Eu sou o destino do RREQ")
                        route = header._sequenceList
                        macDestiny = route[0]
                        sequenceToSource = route 
                        sequenceToSource.reverse()
                        self.sendRREP(macDestiny,sequenceToSource, route)
                        indicesToSend.append(self._linkLayer._phyLayer._id)

                    else:
                        print("ID", self._linkLayer._phyLayer._id, ": Eu não sou o destino do RREQ")
                        self._linkLayer.addPackage(package, -1)
                        indicesToSend.append(self._linkLayer._phyLayer._id)
                
                else:
                    print("ID", self._linkLayer._phyLayer._id, ": Ja tenho esse RREQ: ", header._sequenceNumber)


            #Se o pacote for recebido for um RREP
            elif(header._request == 1):
                
                destiny = header._macDestiny
                print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote RREP: ", header._sequenceList)
                
                #Verifica se o RREP é para mim
                if(destiny == self._linkLayer._phyLayer._id):
                    print("ID", self._linkLayer._phyLayer._id, ": Eu sou o destino do RREP")
                    print("ID", self._linkLayer._phyLayer._id, ": Enviando pacote de dados")
                    sequenceToDestiny = package._data
                    route = Route(header._sequenceList[0],sequenceToDestiny)
                    self._routes.append(route)
                    indicesToSend.append(self._linkLayer._phyLayer._id)

                else:
                    
                    print("ID", self._linkLayer._phyLayer._id, ": Eu não sou o destino do RREP")
                    
                    for index,mac in enumerate(header._sequenceList):
                        if(mac == self._linkLayer._phyLayer._id):
                            nextDestiny = header._sequenceList[index+1]
                            nextPackage = package
                            package._headers.pop(1)
                            self._linkLayer.addPackage(nextPackage, nextDestiny)
                            indicesToSend.append(self._linkLayer._phyLayer._id)
                            break


    #Função responsável por criar um pacote novo e adicionar o cabeçalho de rede
    def addPackage(self, macDestiny, message, time):
        package = Package(message, time)
        header = Header("NETWORK",self._linkLayer._phyLayer._id, macDestiny, -1, -1, -1, None)
        package.addHeader(header)
        self._listPackages.append(package)


    #Função que envia os pacotes da camada de rede
    def sendPackage(self):
        
        #Verifica pacotes a serem enviados
        if(self._listPackages != []):

            package = self._listPackages[0]
            header = package.getNetworkHeader()
            sequence = None

            for route in self._routes:
                if(route._destiny == package._headers[0]._macDestiny):
                    sequence = route._sequence  
                    if (package._headers[0]._macDestiny in self._waitingRouteToList):
                        self._waitingRouteToList.remove(package._headers[0]._macDestiny)


            #Verifica se a rota para o destino é conhecida
            if(sequence != None):
                package.updateSequence(sequence)
                self._listPackages.pop(0)

                for index,mac in enumerate(package._headers[0]._sequenceList):
                    if(mac == self._linkLayer._phyLayer._id):
                        nextDestiny = header._sequenceList[index-1]
                        break
                             
                self._linkLayer.addPackage(package, nextDestiny)
                indicesToSend.append(self._linkLayer._phyLayer._id)

            elif(not header._macDestiny in self._waitingRouteToList):

                self._waitingRouteToList.append(package._headers[0]._macDestiny)
                self.sendRREQ(package._headers[0]._macDestiny)


        #Chama a função de enviar pacotes da camada de enlace
        self._linkLayer.sendPackage()