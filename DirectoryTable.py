class DirectoryTable:

    dirProc = {}
    currentType = ""
    currentFunc = ""
    programName = ""

    def __init__(self, name = None):
        self.programName = name
        self.currentType = "void"
        self.addFunction(name, "global", 0)

    #Método que añade una función al directorio de funciones, recibe como parámetro el alcance
    #de la función y la linea del cuadruplo en donde empiezan los cuadruplos de la función.
    def addFunction(self, id, scope, quadStartIndex):
        if self.alreadyInDir(id):
            print("Error : " + id + " function already in directory")
            return

        self.dirProc[id] = {
            "scope" : scope,
            "varTable": {},
            "signature": [],
            "signatureAddresses": [],
            "ERA": {
               "vars": {
                "entero": 0,
                "flotante" : 0,
                "char": 0
               },
               "temporals": {
                "entero": 0,
                "flotante": 0,
                "char": 0
               }
            },
            "returnType": self.currentType,
            "quadStartIndex": quadStartIndex
        }

        self.currentFunc = id

    def addFunctionAsGlobalVariable(self, id, dir, type):
        self.dirProc[self.programName]["varTable"][id] = {"type" : type, "dir": dir}
        self.dirProc[self.programName]["ERA"]["vars"][type] = self.dirProc[self.programName]["ERA"]["vars"][type] + 1

    #Agrega una variable a la tabla de variables de la función  que se esta procesando y actualiza el ERA
    def addToLocalVariable(self, id, dir, type):
        if self.alreadyInVarTable(id):
            print("Error in " + self.currentFunc + " varTable: " + id + " variable already in func's vartable")
            return

        self.dirProc[self.currentFunc]["varTable"][id] = {"type" : self.currentType, "dir": dir}
        self.dirProc[self.currentFunc]["ERA"]["vars"][type] = self.dirProc[self.currentFunc]["ERA"]["vars"][type] + 1

    #Agrega una variable de tipo arreglo a la tabla de variables de la función  que se esta procesando y actualiza el ERA
    def addToLocalVariableArr(self, id, dir, type, node, size):
        if self.alreadyInVarTable(id):
            print("Error in " + self.currentFunc + " varTable: " + id + " variable already in func's vartable")
            return

        self.dirProc[self.currentFunc]["varTable"][id] = {"type" : self.currentType, "dir": dir, "dim": node}
        self.dirProc[self.currentFunc]["ERA"]["vars"][type] = self.dirProc[self.currentFunc]["ERA"]["vars"][type] + size
        print(self.dirProc[self.currentFunc]["ERA"])

    def alreadyInDir(self, funcName):
        if funcName in self.dirProc:
            return True
        return False

    def alreadyInVarTable(self, variableName):
        varTable = self.dirProc[self.currentFunc]["varTable"]
        if variableName in varTable:
            return True
        return False

    def checkIfFuncExists(self, id):
        if id in self.dirProc:
            return True
        print("Error: ", id ," is not a function")
        return False

    def checkIfVarExists(self, id):
        funcVarTable = self.dirProc[self.currentFunc]["varTable"]
        globalVarTable = self.dirProc[self.programName]["varTable"]
        if id in funcVarTable:
            return True
        if id in globalVarTable:
            return True

        print("Error: ", id ," is not declared in the function and is not a global variable")
        return False

    def getVarType(self, id):
        funcVarTable = self.dirProc[self.currentFunc]["varTable"]
        globalVarTable = self.dirProc[self.programName]["varTable"]
        if id in funcVarTable:
            return funcVarTable[id]["type"]
        if id in globalVarTable:
            return globalVarTable[id]["type"]

        print("Error:  variable", id  ," not declared")
        return "error"

    def getVarDir(self, id):
        funcVarTable = self.dirProc[self.currentFunc]["varTable"]
        globalVarTable = self.dirProc[self.programName]["varTable"]
        if id in funcVarTable:
            return funcVarTable[id]["dir"]
        if id in globalVarTable:
            return globalVarTable[id]["dir"]

        print("Error:  variable", id  ," not declared")
        return "error"

    def getFuncQuadStartIndex(self, id):
        if id in self.dirProc:
            return self.dirProc[id]["quadStartIndex"]
        print("Error: function " + id + " not declared")

    def getFuncSignature(self, id):
        if id in self.dirProc:
            return self.dirProc[id]["signature"]
        print("Error: function " + id + " not declared")

    def getFuncSignatureAddresses(self, id):
        if id in self.dirProc:
            return self.dirProc[id]["signatureAddresses"]
        print("Error: function " + id + " not declared")

    def addVarToParamTable(self, dir):
        self.dirProc[self.currentFunc]["signature"].append(self.currentType)
        self.dirProc[self.currentFunc]["signatureAddresses"].append(dir)

    def incrementTemporalCount(self, type):
        if type == "entero":
            self.dirProc[self.currentFunc]["ERA"]["temporals"][type] = self.dirProc[self.currentFunc]["ERA"]["temporals"][type] + 1
        elif type == "flotante":
            self.dirProc[self.currentFunc]["ERA"]["temporals"][type] = self.dirProc[self.currentFunc]["ERA"]["temporals"][type] + 1
        elif type == "char":
            self.dirProc[self.currentFunc]["ERA"]["temporals"][type] = self.dirProc[self.currentFunc]["ERA"]["temporals"][type] + 1

    def setNumberOfTemporals(self, id, total):
        if id in self.dirProc:
            self.dirProc[id]["temporals"] = total
            return
        print("Error: function " + id + " not declared")

    def changeCurrentFunc(self, funcName):
        self.currentFunc = funcName

    def changeCurrentFuncToGlobal(self):
        self.currentFunc = self.programName

    def changeCurrentType(self, type):
        self.currentType = type

    def isArray(self, id):
        print(self.dirProc[self.currentFunc]["varTable"])
        if "dim" in self.dirProc[self.currentFunc]["varTable"][id]:
            return True
        return False

    def getDim(self, id):
        if self.isArray(id):
            return self.dirProc[self.currentFunc]["varTable"][id]["dim"]

    def getBaseAddress(self, id):
        return self.dirProc[self.currentFunc]["varTable"][id]["dir"]

    def era(self, id):
        if id in self.dirProc:
            return self.dirProc[id]["ERA"]
        print("Error: function " + id + " not declared")

    def printDir(self):
        print("printing procedure directory")
        for func in self.dirProc:
            print(func, "  scope: ", self.dirProc[func]["scope"], " signature = ", self.dirProc[func]["signature"], " signatureAddresses = ",  self.dirProc[func]["signatureAddresses"],"  returnType: " + self.dirProc[func]["returnType"], " quadStart = ", self.dirProc[func]["quadStartIndex"], " ERA = ", self.dirProc[func]["ERA"])
            if "temporals" in self.dirProc[func]:
                print(" temporals = ", self.dirProc[func]["temporals"])
            for key in self.dirProc[func]["varTable"]:
                print("     " + key + "  info: ", self.dirProc[func]["varTable"][key])
