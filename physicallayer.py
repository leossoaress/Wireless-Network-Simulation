from utilities import inRange
from package import Package
from lists import hosts

class PhysicalLayer:

    #Construtor da classe PhysicalLayer
    def __init__(self, x, y, id, range):
        self._x = x
        self._y = y
        self._id = id
        self._range = range
        self._neighboors = []
        self._sendPackages = []
        self._receivePackages = []
        self._backupPackages = []

    #Função que descobre o nós vizihos
    def checkNeighboor(self):
        for host in hosts:
            if((host._id != self._id) and (inRange(self._x, self._y, self._range, host._networkLayer._linkLayer._phyLayer._x, host._networkLayer._linkLayer._phyLayer._y))):
                self._neighboors.append(host) 


    #Função que transmite o pacote para o meio
    def sendPackage(self):
        self.checkNeighboor()
        for host in self._neighboors:
            host._networkLayer._linkLayer._phyLayer.receivePackage(self._sendPackages[0])
        self._backupPackages.append(self._sendPackages.pop(0))

    def receivePackage(self, package):
        self._receivePackages.append(package)
