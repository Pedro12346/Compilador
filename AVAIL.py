class AVAIL:
    memory = {
     "G": {"entero": 1000, "flotante": 4000, "char": 7000},
     "L": {"entero": 10000, "flotante": 14000, "char": 17000}, #parametros y variables declaradas en una funcion
     "T": {"entero": 20000, "flotante": 24000, "char": 27000},
     "C": {"entero": 30000, "flotante": 34000, "char": 37000},
     "P": {"entero": 40000}
     }

    consTable = {}

    def getConsAddress(self, val, type):
        if val in self.consTable:
            return self.consTable[val]["dir"]

        dir = self.memory["C"][type]
        self.memory["C"][type] = self.memory["C"][type] + 1
        self.consTable[val] = {}
        self.consTable[val]["dir"] = dir
        self.consTable[val]["type"] = type
        return dir

    def getAddress(self, section, type, size):
        dir = self.memory[section][type]
        self.memory[section][type] = self.memory[section][type] + size
        return dir

    def reset(self):
        self.memory["L"] = {"entero": 10000, "enteroPointer": 12000, "flotante": 14000, "flotantePointer": 16000, "char": 17000, "charPointer": 19000}
        self.memory["T"] = {"entero": 20000, "enteroPointer": 22000, "flotante": 24000, "flotantePointer": 26000, "char": 27000, "charPointer": 29000}
        self.memory["P"] = {"entero": 40000}

    def getConsAddressWithValue(self, value):
        return self.consTable[value]["dir"]

    def isAddressATemporal(self, addr):

        if addr >= 20000 and addr < 30000:
            return True
        return False
