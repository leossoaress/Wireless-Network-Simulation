from physicallayer import PhysicalLayer
from package import Package
from headers import Header
from linklayer import LinkLayer
from route import Route
import random

class NetworkLayer:

    def __init__(self, linkLayer): 
    
        self._linkLayer = linkLayer

        self._listPackages = []

        self._listRREQs = []

        self._waitingRouteToList = []

        self._routes = []


    def sendRREP(self, macDestiny, sequence, route):
        
        header = Header("NETWORK", self._linkLayer._phyLayer._id, macDestiny, -1, 1, -1, sequence)
        package = Package(route, 1)
        package.addHeader(header)
        
        print("ID", self._linkLayer._phyLayer._id, ": Enviando um RREP com destino para ", header._macDestiny)
        self._linkLayer.addPackage(package, macDestiny)


    def sendRREQ(self, macDestiny):
    
        sequence = []
        sequence.append(self._linkLayer._phyLayer._id)
        sequenceNumber = random.randint(1,128733788) 

        header = Header ("NETWORK", self._linkLayer._phyLayer._id, macDestiny, -1, 0, sequenceNumber, sequence)
        package = Package("", 1)
        package.addHeader(header)
        
        print("ID", self._linkLayer._phyLayer._id, ": Enviando um RREQ com destino para ", header._macDestiny)
        self._linkLayer.addPackage(package, macDestiny)
        

    def receivePackage(self):

        self._linkLayer.receivePackage()
        print("ID", self._linkLayer._phyLayer._id, ": Dentro da função de receber pacote")

        if(self._linkLayer._readedPackages != []):
            
            print("ID", self._linkLayer._phyLayer._id, ": Tem pacote sendo recebido")
            package = self._linkLayer._readedPackages.pop(0)
            header = package.getNetworkHeader()

            if(header._request == -1):
                
                print("ID", self._linkLayer._phyLayer._id, ": O pacote é normal")
                if(header._macDestiny == self._linkLayer._phyLayer._id):
                    print("ID", self._linkLayer._phyLayer._id, ": Pacote chegou: ", package._data)

            elif(header._request == 0):
                
                print("ID", self._linkLayer._phyLayer._id, ": O pacote é um RREQ")
                if(not header._sequenceNumber in self._listRREQs):
                    self._listRREQs.append(header._sequenceNumber)
                    header._sequenceList.append(self._linkLayer._phyLayer._id)

                    if(header._macDestiny == self._linkLayer._phyLayer._id):
                        route = header._sequenceList
                        macDestiny = route[0]
                        sequenceToSource = route 
                        sequenceToSource.reverse()
                        self.sendRREP(macDestiny,sequenceToSource, route)

                    else:
                        self._linkLayer.addPackage(package, -1)

            elif(header._request == 1):
                
                destiny = header._macDestiny
                print("ID", self._linkLayer._phyLayer._id, ": O pacote é um RREP")

                if(destiny == self._linkLayer._phyLayer._id):

                    sequenceToDestiny = package._data
                    route = Route(header._sequenceList[0],sequenceToDestiny)
                    self._routes.append(route)

                else:

                    for index,mac in enumerate(header.sequenceList):

                        if(mac == self._linkLayer._phyLayer._id):

                            nextDestiny = header._sequenceList(index+1)
                            nextPackage = package
                            self._linkLayer.addPackage(nextPackage, nextDestiny)


    def addPackage(self, macDestiny, message, time):

        package = Package(message, time)
        header = Header("NETWORK",self._linkLayer._phyLayer._id, macDestiny, -1, -1, -1, None)
        package.addHeader(header)
        self._listPackages.append(package)


    def sendPackage(self):
        
        print("ID", self._linkLayer._phyLayer._id, ": Dentro da funcao de enviar")
        
        if(self._listPackages != []):
            
            print("ID", self._linkLayer._phyLayer._id, ": Tem pacotes para enviar")
            package = self._listPackages[0]
            header = package.getNetworkHeader()
            sequence = None

            for route in self._routes:
                if(route._destiny == package._headers[0]._macDestiny):
                    sequence = route._sequence  
                    self._waitingRouteToList.remove(package._headers[0]._macDestiny)

            if(sequence != None):
                
                print("ID", self._linkLayer._phyLayer._id, ": Não tem sequencia para o destinatario")
                package.updateSequence(sequence)
                self._listPackages.pop(0)
                self._linkLayer.addPackage(package, package._headers[0]._macDestiny)
                
            elif(not header._macDestiny in self._waitingRouteToList):

                print("ID", self._linkLayer._phyLayer._id, ": Esta esperando o caminho para enviar")
                self._waitingRouteToList.append(package._headers[0]._macDestiny)
                self.sendRREQ(package._headers[0]._macDestiny)

        self._linkLayer.sendPackage()