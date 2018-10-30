class Header:

    #Construtor da classe Header
    def __init__(self, type, macOrigin, macDestiny, number, request, sequenceNumber, sequenceList):


        if(type == "LINK"):

            self._type = "LINK"
            self._macOrigin = macOrigin
            self._macDestiny = macDestiny
            self._number = number

        elif(type == "NETWORK"):

            self._type = "NETWORK"
            self._macDestiny = macDestiny
            self._request = request
            self._sequenceNumber = sequenceNumber
            self._sequenceList = sequenceList