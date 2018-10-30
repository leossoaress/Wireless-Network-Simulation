from host import Host
from lists import hosts
from lists import hosts
from package import Package
from networklayer import NetworkLayer

#Instaciando os hosts
a = Host(0,2,1,1)
b = Host(1,2,2,1)
c = Host(2,2,3.5,1)

a.createPackage(b._id, "Eu sou o host A", 2)

for i in range(15):

    print("")
    print("Time: ", i)
    print("")

    for host in hosts:
        host._networkLayer.receivePackage()
        host._networkLayer.sendPackage()


