from physicallayer import PhysicalLayer
from linklayer import LinkLayer
from utilities import hosts
from package import Package

class Host:

    #Construtor da classe Host
    def __init__(self, id, range, x, y):
        
        #Identificador único para o host
        self._id = id

        #Adiciona a própria instacia na lista de hosts globais
        hosts.append(self)

        #Inicializa a camada de enlace
        self._linkLayer = LinkLayer(PhysicalLayer(x, y, id, range))
    