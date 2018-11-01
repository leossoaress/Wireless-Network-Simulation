from host import Host
from lists import hosts
from lists import indicesToSend, indicesToRead, nextTosend
from package import Package
from networklayer import NetworkLayer
import random

#Instaciando os hosts
a = Host(0,2,1,1)
b = Host(1,2,2,1)
c = Host(2,2,3.5,1)

#Loop do tempo
for i in range(20):

    print("")
    print("Time: ", i)
    print("")
    
    #Loop para percorrer 
    for host in hosts:
        
        #Numero aleatorio entre 0 e 100 para probabilidade de criação de pacotes
        rand = random.randint(0, 100)

        #Numero aleatorio entre 0 e a quantidade de hosts, para escolher um para enviar
        towho = random.randint(0, len(hosts)-1)

        #Teste se rand é menor que 3, gerando assim uma probabilidade de 0.3
        if(rand < 3):

                #Se o ID do destino for diferente do dele mesmo, adiciona o pacote no host
                if(towho != host._networkLayer._linkLayer._phyLayer._id):
                        host.createPackage(towho, "Oi, Tudo bem?", 1)
                        indicesToSend.append(host._networkLayer._linkLayer._phyLayer._id)


    if(nextTosend != []):
        for i in nextTosend:
                indicesToSend.append(i)
    del nextTosend[:]

    #Existe algum nó querendo receber, recebe
    for j in indicesToRead:
            hosts[j]._networkLayer.receivePackage()
    del indicesToRead[:]
    
    #Existe algum nó querendo transmitir, transmite naquele instante se posssível
    for i in indicesToSend: 
            hosts[i]._networkLayer.sendPackage()
    del indicesToSend[:]