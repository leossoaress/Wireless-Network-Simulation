from host import Host
from lists import hosts
from package import Package

#Instaciando os hosts
a = Host(0,5,2,1)
b = Host(1,5,2,5)
c = Host(2,5,4,4)

a.createPackage("Eu sou o host A", -1, 2)
b.createPackage("Eu sou o host B", -1, 2)
c.createPackage("Eu sou o host C", -1, 2)

for i in range(15):

    print("Time: ", i)

    for host in hosts:
        host._linkLayer.receivePackage(host._id)
        host._linkLayer.sendPackage()


