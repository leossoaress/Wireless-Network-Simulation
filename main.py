from host import Host
from utilities import hosts
from package import Package

#Instaciando os hosts
a = Host(0,5,2,1)
b = Host(1,5,2,5)
c = Host(2,5,4,2)


#Definindo o cronograma de envio
def schedule(i):
    if(i == 1):
        package = Package.createPackage("Hello!")
        a._linkLayer.sendPackage(package, 0, 1)
        b._linkLayer.receivePackage(b._id)
        c._linkLayer.receivePackage(c._id)
    

#Loop de execução com 10 unidades de tempo
for i in range(10):
    
    #Executando o cronograma dependendo do tempo
    schedule(i)

    #Percorrer todos os hosts e verifica a transmissão
    for host in hosts:

        #Diminuir o tempo de duração do envio
        host._linkLayer.update()

        #Escrevendo na tela informações
        if(host._linkLayer._sending):
            print("O host ", host._id, " está enviando dados")
        elif(host._linkLayer._receiving):
            print("O host ", host._id, " está recebendo dados")
        else:
            print("Host sem fazer nada")

