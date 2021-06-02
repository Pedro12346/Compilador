class Memory:

    localMemory = {} #crea los espacios de memoria y guarda los valores relacionados a las variables declaradas en la función.
    intBase = None
    floatBase = None
    charBase = None

    intTempBase = 20000
    floatTempBase = 24000
    charTempBase = 27000

    pointerBase = 40000

    temporalMemory = {} #crea los espacios de memoria y guarda los valores relacionados a los temporales usados en la función.
    pointerMemory = {} #crea los espacios de memoria y guarda los valores relacionados a los apuntadores usados en la función.

    def __init__(self, ERA, intBase, floatBase, charBase):

        self.localMemory = {
            "entero": [None] * ERA["vars"]["entero"],
            "flotante": [None] * ERA["vars"]["flotante"],
            "char": [None] * ERA["vars"]["char"]
        }

        self.temporalMemory = {
            "entero": [None] * ERA["temporals"]["entero"],
            "flotante": [None] * ERA["temporals"]["flotante"],
            "char": [None] * ERA["temporals"]["char"]
        }

        #establece en que dirección de memoria se guardan las variables declaradas en la función
        self.intBase = intBase
        self.floatBase = floatBase
        self.charBase = charBase

    #Determina si una dirección es un temporal
    def __isAddressATemporal(self, addr):
        if addr >= 20000 and addr < 30000:
            return True
        return False

    #Determina si una dirección es un pointer
    def __isAddressAPointer(self, addr):
        if addr >= 40000:
            return True
        return False

    #Agrega a una dirección de la sección temporal un valor
    #Resta la dirección dada con la base para obtener el indice de donde se tiene que agregar el valor.
    def __addValueToTempAddr(self, addr, value):
        if addr >= self.intTempBase and addr < self.floatTempBase:
            self.temporalMemory["entero"][addr - self.intTempBase] = int(value)
        elif addr >= self.floatTempBase and addr < self.charTempBase:
            self.temporalMemory["flotante"][addr - self.floatTempBase] = float(value)
        else:
            self.temporalMemory["char"][addr - self.charTempBase] = value

    #Agrega a una dirección de la sección principal un valor
    #Resta la dirección dada con la base para obtener el indice de donde se tiene que agregar el valor.
    def __addValueToLocalAddr(self, addr, value):
        if addr >= self.intBase and addr < self.floatBase:
            self.localMemory["entero"][addr - self.intBase] = int(value)
        elif addr >= self.floatBase and addr < self.charBase:
            self.localMemory["flotante"][addr - self.floatBase] = float(value)
        else:
            self.localMemory["char"][addr - self.charBase] = value

    #Va a la memoria referenciada y asigna el valor
    def __addValueToPointerAddr(self, addr, value):
        self.__addValueToLocalAddr(self.pointerMemory[addr], value)


    #Agrega una dirección de memoria a la dirección de un apuntador
    def setReferenceAddressToPointer(self, addr, ref):
        self.pointerMemory[addr] = ref

    #Regresa el valor asociado a una variable temporal
    def __getValueFromTempAddr(self, addr):
        if addr >= self.intTempBase and addr < self.floatTempBase:
            return self.temporalMemory["entero"][addr - self.intTempBase]
        elif addr >= self.floatTempBase and addr < self.charTempBase:
            return self.temporalMemory["flotante"][addr - self.floatTempBase]
        else:
            return self.temporalMemory["char"][addr - self.charTempBase]

    #Regresa el valor de asociado a una variable en memoria local
    def __getValueFromLocalAddr(self, addr):
        if addr >= self.intBase and addr < self.floatBase:
            return self.localMemory["entero"][addr - self.intBase]
        elif addr >= self.floatBase and addr < self.charBase:
            return self.localMemory["flotante"][addr - self.floatBase]
        else:
            return self.localMemory["char"][addr - self.charBase]


    #Regresa el valor asociado de la dirección asociada a un pointer
    def __getValueFromPointerAddr(self, addr):
        return self.getValue(self.pointerMemory[addr])

    #Regresa el tipo del valor asociado a una dirección local
    def __valueTypeLocal(self, addr):
        if addr >= self.intBase and addr < self.floatBase:
            return "entero"
        elif addr >= self.floatBase and addr < self.charBase:
            return "flotante"
            return self.localMemory["flotante"][addr - self.floatBase]
        else:
            return "char"

    #Regresa el tipo del valor asociado a una dirección temporal
    def __valueTypeTemp(self, addr):
        if addr >= self.intTempBase and addr < self.floatTempBase:
            return "entero"
        elif addr >= self.floatTempBase and addr < self.charTempBase:
            return "flotante"
        else:
            return "char"

    def print(self):
        print("Local memory")
        for key in self.localMemory:
            print(key, " - ", self.localMemory[key])

        print("Temporal memory")
        for key in self.temporalMemory:
            print(key, " - ", self.temporalMemory[key])

    #Métodos publicos

    #Regresa el valor asociado a una dirección
    def getValue(self, addr):
        if self.__isAddressATemporal(addr):
            return self.__getValueFromTempAddr(addr)
        elif self.__isAddressAPointer(addr):
            return self.__getValueFromPointerAddr(addr)
        else:
            return self.__getValueFromLocalAddr(addr)

    #Función que agrega a una dirección de memoria un valor
    def setValue(self, addr, value):
        if self.__isAddressATemporal(addr):
            self.__addValueToTempAddr(addr, value)
        elif self.__isAddressAPointer(addr):
            self.__addValueToPointerAddr(addr, value)
        else:
            self.__addValueToLocalAddr(addr, value)

    #Regresa el tipo del valor asociado a una dirección
    def valueType(self, addr):
        if self.__isAddressATemporal(addr):
            return self.__valueTypeTemp(addr)
        else:
            return self.__valueTypeLocal(addr)
