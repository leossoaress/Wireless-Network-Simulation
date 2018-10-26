from linklayer import LinkLayer
from physicallayer import PhysicalLayer
from lists import hosts
from package import Package
from headers import Header

class Host:

    #Construtor da classe Host
    def __init__(self, id, range, x, y):
        
        #Identificador único para o host
        self._id = id

        #Adiciona a própria instacia na lista de hosts globais
        hosts.append(self)

        #Inicializa a camada de enlace
        self._linkLayer = LinkLayer(PhysicalLayer(x, y, id, range))
    
    def createPackage(self, message, destination, duration):
        package = Package(message, duration)
        header = Header(1, id, destination)
        package.addHeader(header)
        self._linkLayer._phyLayer._sendPackages.append(package)