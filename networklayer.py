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
        
        for index,mac in enumerate(header._sequenceList):
            if(mac == self._linkLayer._phyLayer._id):
                
                nextDestiny = header._sequenceList[index+1]
                nextPackage = package
                print("ID", self._linkLayer._phyLayer._id, ": Repassando RREP por ", nextDestiny)
                self._linkLayer.addPackage(nextPackage, nextDestiny)
                break
       
       # self._linkLayer.addPackage(package, -1)


    def sendRREQ(self, macDestiny):
    
        sequence = []
        sequence.append(self._linkLayer._phyLayer._id)
        sequenceNumber = random.randint(1,128733788) 

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

            elif(header._request == 0):
                
                print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote RREQ")
                
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
                print("ID", self._linkLayer._phyLayer._id, ": Chegada de pacote RREP: ", header._sequenceList)

                if(destiny == self._linkLayer._phyLayer._id):

                    sequenceToDestiny = package._data
                    route = Route(header._sequenceList[0],sequenceToDestiny)
                    self._routes.append(route)

                else:

                    for index,mac in enumerate(header._sequenceList):

                        if(mac == self._linkLayer._phyLayer._id):

                            nextDestiny = header._sequenceList[index+1]
                            nextPackage = package
                            self._linkLayer.addPackage(nextPackage, nextDestiny)
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
                self._linkLayer.addPackage(package, package._headers[0]._macDestiny)
                
            elif(not header._macDestiny in self._waitingRouteToList):

                self._waitingRouteToList.append(package._headers[0]._macDestiny)
                self.sendRREQ(package._headers[0]._macDestiny)

        self._linkLayer.sendPackage()