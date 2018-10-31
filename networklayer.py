from physicallayer import PhysicalLayer
from package import Package
from headers import Header
from linklayer import LinkLayer
from lists import indicesToSend
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
        
        for index,mac in enumerate(header._sequenceList):
            if(mac == self._linkLayer._phyLayer._id):
                
                nextDestiny = header._sequenceList[index+1]
                nextPackage = package
                self._linkLayer.addPackage(nextPackage, nextDestiny)
                break
       
       # self._linkLayer.addPackage(package, -1)


    def sendRREQ(self, macDestiny):
    
        sequence = []
        sequence.append(self._linkLayer._phyLayer._id)
        sequenceNumber = random.randint(1,128733788) 
        self._listRREQs.append(sequenceNumber)

        header = Header ("NETWORK", self._linkLayer._phyLayer._id, macDestiny, -1, 0, sequenceNumber, sequence)
        package = Package("", 1)
        package.addHeader(header)
        
        print("ID", self._linkLayer._phyLayer._id, ": Enviando um RREQ com destino para ", header._macDestiny)
        self._linkLayer.addPackage(package, -1)
        

    def receivePackage(self):

        self._linkLayer.receivePackage()

        if(self._linkLayer._readedPackages != []):
            
            package = self._linkLayer._readedPackages.pop(0)
            header = package.getNetworkHeader()

            if(header._request == -1):
                
                if(header._macDestiny == self._linkLayer._phyLayer._id):
                    print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote normal: ", package._data)
                else:
                    print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote normal mas não é pra mim")
                    for index,mac in enumerate(package._headers[0]._sequenceList):
                        if(mac == self._linkLayer._phyLayer._id):
                            nextDestiny = header._sequenceList[index-1]
                            break

                    package._headers.pop(1)
                    self._linkLayer.addPackage(package, nextDestiny)
                    indicesToSend.append(self._linkLayer._phyLayer._id)

            elif(header._request == 0):
                
                print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote RREQ")
                
                if(not header._sequenceNumber in self._listRREQs):
                    self._listRREQs.append(header._sequenceNumber)
                    header._sequenceList.append(self._linkLayer._phyLayer._id)

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

            elif(header._request == 1):
                
                destiny = header._macDestiny
                print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote RREP: ", header._sequenceList)
                
                if(destiny == self._linkLayer._phyLayer._id):
                    print("ID", self._linkLayer._phyLayer._id, ": Eu sou o destino do RREP")
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


    def addPackage(self, macDestiny, message, time):

        package = Package(message, time)
        header = Header("NETWORK",self._linkLayer._phyLayer._id, macDestiny, -1, -1, -1, None)
        package.addHeader(header)
        self._listPackages.append(package)


    def sendPackage(self):
        
        if(self._listPackages != []):

            package = self._listPackages[0]
            header = package.getNetworkHeader()
            sequence = None

            for route in self._routes:
                if(route._destiny == package._headers[0]._macDestiny):
                    sequence = route._sequence  
                    if (package._headers[0]._macDestiny in self._waitingRouteToList):
                        self._waitingRouteToList.remove(package._headers[0]._macDestiny)

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

        self._linkLayer.sendPackage()