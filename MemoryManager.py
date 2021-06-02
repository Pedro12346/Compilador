from Memory import Memory

class MemoryManager:

    globalAddresses = [1000, 4000, 7000]
    localAddresses = [10000, 14000, 17000]
    consAddresses = [30000, 34000, 37000]
    pointerAddresses = 40000

    globalMemory = None
    localMemory = []
    consTable = None

    def __init__(self, consTable):
        self.consTable = consTable

    #Crea un espacio de memoria, si es local entonces lo pone al tope del stack
    def createMemory(self, type, ERA):
        if type == "Global":
            self.globalMemory = Memory(ERA, self.globalAddresses[0], self.globalAddresses[1], self.globalAddresses[2])
        elif type == "Local":
            self.localMemory.append(Memory(ERA, self.localAddresses[0], self.localAddresses[1], self.localAddresses[2]))

    #Elimina el espacio de memoria de la función que se esta procesando
    def popMemory(self):
        self.localMemory.pop()

    #Cambia el valor que guarda una dirección
    def setValue(self, addr, value):
        type = self.__addressType(addr)
        if type == "Global":
            self.globalMemory.setValue(addr, value)
        elif type == "Local":
            self.localMemory[-1].setValue(addr, value)
        elif type == "Temporal" or type == "Pointer":
            if len(self.localMemory) == 0:
                self.globalMemory.setValue(addr, value)
            else:
                self.localMemory[-1].setValue(addr, value)

    #Regresa el valor que guarda una dirección
    def getValue(self, addr):
        type = self.__addressType(addr)
        if type == "Global":
            return self.globalMemory.getValue(addr)
        elif type == "Local":
            return self.localMemory[-1].getValue(addr)
        elif type == "Temporal" or type == "Pointer":
            if len(self.localMemory) == 0:
                return self.globalMemory.getValue(addr)
            else:
                return self.localMemory[-1].getValue(addr)
        elif type == "Constant":
            return self.consTable[addr]["value"]

    #Guarda en la dirección del pointer la dirección a la que apunta
    def setReferenceAddressToPointer(self, addr, ref):
        if len(self.localMemory) == 0:
            self.globalMemory.setReferenceAddressToPointer(addr, ref)
        else:
            self.localMemory[-1].setReferenceAddressToPointer(addr, ref)

    #Métodos privados

    #Regresa el tipo del valor que guarda una dirección
    def __valueType(self, addr):
        type = self.__addressType(addr)
        if type == "Global":
            return self.globalMemory.valueType(addr)
        elif type == "Local":
            return self.localMemory[-1].valueType(addr)
        elif type == "Temporal":
            if len(self.localMemory) == 0:
                return self.globalMemory.valueType(addr)
            else:
                return self.localMemory[-1].valueType(addr)
        elif type == "Constant":
            return self.consTable[addr]["type"]

    #Determina la sección a la que pertenece una dirección de memoria
    def __addressType(self, addr):
        if addr >= 1000 and addr < 10000:
            return "Global"
        elif addr >= 10000 and addr < 20000:
            return "Local"
        elif addr >= 20000 and addr < 30000:
            return "Temporal"
        elif addr >= 30000 and addr < 40000:
            return "Constant"
        elif addr  >= self.pointerAddresses:
            return "Pointer"
