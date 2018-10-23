from utilities import hosts, inRange
from package import Package

class PhysicalLayer:

    #Construtor da classe PhysicalLayer
    def __init__(self, x, y, id, range):
        self._x = x
        self._y = y
        self._id = id
        self._range = range
        self._neighboors = []
        self._package = []

    #Função que descobre o nós vizihos
    def checkNeighboor(self):
        for host in hosts:
            if((host._id != self._id) and (inRange(self._x, self._y, self._range, host._linkLayer._phyLayer._x, host._linkLayer._phyLayer._y))):
                    self._neighboors.append(host) 

    #Função que transmite o pacote para o meio
    def sendPackage(self):
        self.checkNeighboor()
        for host in self._neighboors:
            host._linkLayer._phyLayer._package.append(self._package[-1])

    #Função que avisa aos vizinhos que o meio está ocupado
    def getMediumAcess(self):
        for host in self._neighboors:
            host._linkLayer._mediumacess = False

    #Função que avisa aos vizinhos que o meio está livre
    def FreeMediumAcess(self):
        for host in self._neighboors:
            host._linkLayer._mediumacess = True
