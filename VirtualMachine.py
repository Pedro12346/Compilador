import json
import turtle
from yacc import directory, quadManager, consTable
from MemoryManager import MemoryManager
dict = consTable
consTable = {}

t = turtle.Turtle()
for key, value in dict.items():
    consTable[value["dir"]] = {"value": key, "type": value["type"]}

memoryManager = MemoryManager(consTable)
memoryManager.createMemory("Global", directory.era(directory.programName))


operTable = {
    "+" : 0,
    "-" : 1,
    "*" : 2,
    "/" : 3,
    "<" : 4,
    "<=" : 5,
    ">" : 6,
    ">=" : 7,
    "!=" : 8,
    "==" : 9,
    "&" : 10,
    "|" : 11,
    "=" : 12,
    "goto": 13,
    "gotof": 14,
    "escribir": 15,
    "leer": 16,
    "verificar": 17,
    "ERA": 18,
    "parameter": 19,
    "gosub": 20,
    "retorno": 21,
    "endfunc": 22,
    "linea": 23,
    "circulo": 24,
    "arco": 25,
    "punto":26,
    "penDown": 27,
    "penUp": 28,
    "color": 29,
    "grosor": 30,
    "limpiar": 31,
    "ri": 32,
    "rd": 33
}

directory.printDir()
quadManager.print()
stackIP = []
stackFuncID = []
IP = 0
params = []
print("Virtual Machine starts")
while IP < len(quadManager.quads):

    if quadManager.quads[IP][0] == operTable["+"]:
        #print("+")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 + value2
        if quadManager.quads[IP][3] >= 40000:
            memoryManager.setReferenceAddressToPointer(quadManager.quads[IP][3], temp)
        else:
            memoryManager.setValue(quadManager.quads[IP][3], temp)

        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["-"]:
        #print("-")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 - value2
        memoryManager.setValue(quadManager.quads[IP][3], temp)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["*"]:
        #print("*")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 * value2
        memoryManager.setValue(quadManager.quads[IP][3], temp)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["/"]:
        #print("/")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 / value2
        memoryManager.setValue(quadManager.quads[IP][3], temp)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["<"]:
        #print("<")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 < value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["<="]:
        #print("<=")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 <= value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable[">"]:
        #print(">")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 > value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable[">="]:
        #print(">=")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 >= value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["!="]:
        #print("!=")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 != value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["=="]:
        #print("==")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 == value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["&"]:
        #print("&")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 and value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["|"]:
        #print("|")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        value2 = memoryManager.getValue(quadManager.quads[IP][2])
        temp = value1 or value2
        memoryManager.setValue(quadManager.quads[IP][3], int(temp))
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["="]:
        #print("=")
        value1 = memoryManager.getValue(quadManager.quads[IP][1])
        memoryManager.setValue(quadManager.quads[IP][3], value1)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["goto"]:
        #print("goto")
        IP = quadManager.quads[IP][3]
    elif quadManager.quads[IP][0] == operTable["gotof"]:
        #print("gotof")
        value = memoryManager.getValue(quadManager.quads[IP][1])
        if value == 0:
            IP = quadManager.quads[IP][3]
        else:
            IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["escribir"]:
        if type(quadManager.quads[IP][3]) is str:
            value = quadManager.quads[IP][3]
        else:
            value = memoryManager.getValue(quadManager.quads[IP][3])
        print(value)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["leer"]:
        input = input("Introduzca el valor para la variable " + quadManager.quads[IP][1] + " = ")
        dir = quadManager.quads[IP][3]
        memoryManager.setValue(dir, input)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["verificar"]:
        index = int(memoryManager.getValue(quadManager.quads[IP][1]))
        linf = memoryManager.getValue(quadManager.quads[IP][2])
        lsup = memoryManager.getValue(quadManager.quads[IP][3])
        if index < linf and index > lsup:
            print("INDEX OUT OF BOUNDS")
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["ERA"]:
        #print("ERA")
        funcName = quadManager.quads[IP][3]
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["parameter"]:
        #print("PARAMETER")
        #print(quadManager.quads[IP])
        value = memoryManager.getValue(quadManager.quads[IP][1])
        paramDir = quadManager.quads[IP][2]
        params.append({"value": value, "paramDir": paramDir})
        #print("value = ", value, "  paramDir = ", paramDir)
        #memoryManager.setValue(paramDir, value)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["gosub"]:
        #print("GOSUB")
        memoryManager.createMemory("Local", directory.era(funcName))
        newIP = memoryManager.getValue(quadManager.quads[IP][3])
        for paramInfo in params:
            memoryManager.setValue(paramInfo["paramDir"], paramInfo["value"])
        params = []
        stackIP.append(IP)
        stackFuncID.append(funcName)
        IP = newIP
    elif quadManager.quads[IP][0] == operTable["retorno"]:
        #print("RETORNO")
        funcName = stackFuncID[-1]
        returnValue = memoryManager.getValue(quadManager.quads[IP][3])
        funcDir = directory.getVarDir(funcName)
        memoryManager.setValue(funcDir, returnValue)
        memoryManager.popMemory()
        IP = stackIP[-1] + 1
        stackIP.pop()
        stackFuncID.pop()
    elif quadManager.quads[IP][0] == operTable["endfunc"]:
        IP = stackIP[-1] + 1
        stackIP.pop()
    elif quadManager.quads[IP][0] == operTable["linea"]:
        value = memoryManager.getValue(quadManager.quads[IP][1])
        t.forward(value)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["circulo"]:
        value = memoryManager.getValue(quadManager.quads[IP][1])
        t.circle(value)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["arco"]:
        radius = memoryManager.getValue(quadManager.quads[IP][1])
        extent = memoryManager.getValue(quadManager.quads[IP][2])
        t.circle(radius, extent)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["punto"]:
        x = memoryManager.getValue(quadManager.quads[IP][1])
        y = memoryManager.getValue(quadManager.quads[IP][2])
        t.goto(x,y)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["penDown"]:
        t.pendown()
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["penUp"]:
        t.penup()
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["color"]:
        value = memoryManager.getValue(quadManager.quads[IP][1])
        if value == '\'r\'':
            t.color("red")
        elif value == '\'b\'':
            print("blue color")
            t.color("blue")
        elif value == '\'g\'':
            t.color("green")
        elif value == '\'p\'':
            t.color("pink")
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["grosor"]:
        value = memoryManager.getValue(quadManager.quads[IP][1])
        t.pensize(value)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["limpiar"]:
        t.reset()
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["ri"]:
        value = memoryManager.getValue(quadManager.quads[IP][1])
        t.left(value)
        IP = IP + 1
    elif quadManager.quads[IP][0] == operTable["rd"]:
        value = memoryManager.getValue(quadManager.quads[IP][1])
        t.right(value)
        IP = IP + 1

print("Virtual machine ends")
turtle.done()
