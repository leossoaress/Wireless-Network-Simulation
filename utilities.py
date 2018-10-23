import math as math

#Variaveis globais
coordinates = []
hosts = []
packages = []

#Função retorna se um host alcança outro
def inRange(centerX, centerY, radius, x, y):
    dist = math.sqrt((centerX - x) ** 2 + (centerY - y) ** 2)
    return dist <= radius