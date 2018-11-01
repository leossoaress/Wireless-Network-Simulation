from linklayer import LinkLayer
from physicallayer import PhysicalLayer
from networklayer import NetworkLayer
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
        self._networkLayer = NetworkLayer(LinkLayer(PhysicalLayer(x, y, id, range)))


    #Função para criar um pacote
    def createPackage(self, macDestiny, message, duration):
        
        print("ID", self._networkLayer._linkLayer._phyLayer._id, ": Pacote criado com destino para", macDestiny )
        self._networkLayer.addPackage(macDestiny, message, duration)
    
        
