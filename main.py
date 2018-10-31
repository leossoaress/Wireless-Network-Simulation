from host import Host
from lists import hosts
from lists import indicesToSend, indicesToRead
from package import Package
from networklayer import NetworkLayer
import random

#Instaciando os hosts
a = Host(0,2,1,1)
b = Host(1,2,2,1)
c = Host(2,2,2,2)

for i in range(20):

    print("")
    print("Time: ", i)
    print("")
    
    if(i == 2):
        a.createPackage(c._id, "Eu sou o host um host A", 1)
        indicesToSend.append(a._networkLayer._linkLayer._phyLayer._id)

    for host in hosts:

        rand = random.randint(0, 100)
        towho = random.randint(0, len(hosts))

        #if(rand < 5):
        #        if(towho != host._networkLayer._linkLayer._phyLayer._id):
        #                host.createPackage(towho, "Eu sou o host um host", 1)
        #                indicesToSend.append(host._networkLayer._linkLayer._phyLayer._id)


    for j in indicesToRead:
            hosts[j]._networkLayer.receivePackage()
    del indicesToRead[:]

    for i in indicesToSend: 
            hosts[i]._networkLayer.sendPackage()
    del indicesToSend[:]