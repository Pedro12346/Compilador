
import ply.yacc as yacc
from lex import tokens
from DirectoryTable import DirectoryTable
from CuboSemantico import CuboSemantico
from QuadManager import QuadManager
from AVAIL import AVAIL
import json

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

directory = None
cuboSemantico = CuboSemantico()
AVAIL = AVAIL()
quadManager = QuadManager()
consTable = {}
operands = []
operators = []
jumps = []
callNumOfArguments = 0
functionToCall = ""
currArrVar= []
incrementarVariableRepeticiónQuads = []
drawingArgs = []
calledFunc = []

# Gramaticas
def p_PROGRAMA(p):
    ''' PROGRAMA : programa id init_dir ';' DECLARACION_VARIABLES DECLARACION_FUNCIONES empieza_main principal '(' ')' BLOQUE
                 '''
    p[0] = "Expresión valida"

#Se crea la tabla de directorios y se agrega el goto que mandará el apuntador a main
def p_init_dir(p):
    "init_dir : "
    global directory
    directory = DirectoryTable(p[-1])
    quadManager.add((operTable["goto"], "-", "-", "-"))
    jumps.append(0)


#Cambia dentro del directorio la funcion que se esta procesado a la funcion global
#Agrega la linea donde empieza el main al goto del cuadruplo 1
def p_empieza_main(p):
    "empieza_main : "
    global directory
    directory.changeCurrentFuncToGlobal()
    line = jumps[-1]
    jumps.pop(-1)
    quadManager.modify(line, 3, quadManager.next())

def p_DECLARACION_VARIABLES(p):
    ''' DECLARACION_VARIABLES : variables DECLARACION_VARIABLES_AUX finVar
                              | empty'''

def p_DECLARACION_VARIABLES_AUX(p):
    ''' DECLARACION_VARIABLES_AUX : TIPO change_current_type ':' LISTA_IDS ';'
                                  | TIPO change_current_type ':' LISTA_IDS ';' DECLARACION_VARIABLES_AUX'''

def p_change_current_type(p):
    "change_current_type : "
    global directory
    directory.changeCurrentType(p[-1])
    p[0] = p[-1]

def p_LISTA_IDS(p):
    ''' LISTA_IDS : id '[' cte_i ']' add_var_arr
                  | id add_var
                  | id add_var ',' LISTA_IDS
                  | id '[' cte_i ']' add_var_arr ',' LISTA_IDS '''

#Agrega una variable de tipo arreglo al directorio de variables de la funcion que se este procesando
def p_add_var_arr(p):
    "add_var_arr : "

    arrNode = {}
    noAddresses = p[-2]
    if directory.programName == directory.currentFunc:
        dir = AVAIL.getAddress("G", directory.currentType, noAddresses)
    else:
        dir = AVAIL.getAddress("L", directory.currentType, noAddresses)


    arrNode["m"] = AVAIL.getConsAddress(0, "entero")
    arrNode["linf"] = AVAIL.getConsAddress(0, "entero")
    arrNode["lsup"] = AVAIL.getConsAddress(p[-2] - 1, "entero")

    size = p[-2] + 1

    directory.addToLocalVariableArr(p[-4], dir, directory.currentType, arrNode, size)

#Agrega la variable al directorio de variables de la funcion que se este procesando
def p_add_var(p):
    "add_var : "
    global directory, AVAIL

    if directory.programName == directory.currentFunc:
        dir = AVAIL.getAddress("G", directory.currentType, 1)
    else:
        dir = AVAIL.getAddress("L", directory.currentType, 1)

    directory.addToLocalVariable(p[-1], dir, directory.currentType)
    p[0] = dir

def p_DECLARACION_FUNCIONES(p):
    ''' DECLARACION_FUNCIONES : FUNCION DECLARACION_FUNCIONES
                              | empty'''

def p_FUNCION(p):
    ''' FUNCION : TIPO_RETORNO change_current_type funcion id add_function '(' PARAMETROS ')'  ';' DECLARACION_VARIABLES BLOQUE declaracion_funcion_termina '''

#agrega el id de la función a la tabla de funciones y el numero de quadruplo en donde empieza
#agrega el id a la tabla de variables global si es una funcion de retorno
def p_add_function(p):
    'add_function : '
    global directory
    funcName = p[-1]
    returnType = p[-3]

    directory.addFunction(funcName, "local", quadManager.next())

    if returnType != "void":
        dir = AVAIL.getAddress("G", returnType, 1)
        directory.addFunctionAsGlobalVariable(funcName, dir, returnType)

    p[0] = p[-1]

#Al terminar la función, se agrega dónde queda la linea final de la función
#se agrega el quadruplo de endfunc y se reinicia la memoria local, temporal y de pointers
def p_declaracion_funcion_termina(p):
    'declaracion_funcion_termina : '
    quadManager.add((operTable["endfunc"], "-", "-", "-"))
    AVAIL.reset()
    p[0] = p[-1]

def p_TIPO_RETORNO(p):
    ''' TIPO_RETORNO : TIPO
                     | void '''
    p[0] = p[1]

def p_TIPO(p):
    ''' TIPO : entero
             | flotante
             | char '''
    p[0] = p[1]

def p_PARAMETROS(p):
    ''' PARAMETROS : TIPO change_current_type ':' id add_var agregar_tipo_a_tabla_param
                   | TIPO change_current_type ':' id add_var agregar_tipo_a_tabla_param ',' PARAMETROS
                   | empty '''

def p_agregar_tipo_a_tabla_param(p):
    'agregar_tipo_a_tabla_param : '
    dir = p[-1]
    directory.addVarToParamTable(dir)
    p[0] = p[-1]

def p_BLOQUE(p):
    ''' BLOQUE   : '{' BLOQUE2 '}'
                 '''
def p_BLOQUE2(p):
    ''' BLOQUE2  : ESTATUTOS
                 | ESTATUTOS BLOQUE2
                 '''

def p_ESTATUTOS(p):
    ''' ESTATUTOS : ASIGNACION ';'
                 | FUNCION_RETORNO ';'
                 | LECTURA ';'
                 | ESCRIBE ';'
                 | LLAMADA_FUNCION ';'
                 | LINEA ';'
                 | PUNTO ';'
                 | CIRCULO ';'
                 | ARCO ';'
                 | PENUP ';'
                 | PENDOWN ';'
                 | COLOR ';'
                 | GROSOR ';'
                 | LIMPIAR ';'
                 | ROTAR_IZQUIERDA ';'
                 | ROTAR_DERECHA ';'
                 | ESTATUTO_DE_DECISION
                 | REPETICION_CONDICIONAL
                 | REPETICION_NO_CONDICIONAL
                 | empty '''

def p_LINEA(p):
    ''' LINEA : linea '(' EXP ')' agregar_linea_quad
              '''

def p_agregar_linea_quad(p):
    'agregar_linea_quad : '
    oper = operands[-1]["operand"]
    type = operands[-1]["type"]

    if type != "entero":
        print("Error: type must be an integer")

    quadManager.add((operTable["linea"], oper, "-", "-"))

def p_PUNTO(p):
    ''' PUNTO : punto '(' EXP agregar_dibujo_arg ',' EXP  agregar_dibujo_arg ')' agregar_punto_quad
              '''

def p_agregar_dibujo_arg(p):
    'agregar_dibujo_arg :'
    global drawingArgs

    oper = operands[-1]["operand"]
    type = operands[-1]["type"]

    if type != "entero":
        print("ERROR: value must be an integer")

    drawingArgs.append(oper)
    p[0] = p[-1]

def p_agregar_punto_quad(p):
    'agregar_punto_quad : '
    global drawingArgs
    quadManager.add((operTable["punto"], drawingArgs[-2], drawingArgs[-1], "-"))
    drawingArgs.pop()
    drawingArgs.pop()

def p_CIRCULO(p):
    ''' CIRCULO : circulo '(' EXP ')'  agregar_circulo_quad '''

def p_agregar_circulo_quad(p):
    'agregar_circulo_quad : '

    oper = operands[-1]["operand"]
    type = operands[-1]["type"]

    if type != "entero":
        print("Error: type must an integer")

    quadManager.add((operTable["circulo"], oper, "-", "-"))

def p_ARCO(p):
    ''' ARCO : arco '(' EXP agregar_dibujo_arg ',' EXP agregar_dibujo_arg ')' agregar_arco_quad '''

def p_agregar_arco_quad(p):
    'agregar_arco_quad : '
    global drawingArgs
    quadManager.add((operTable["arco"], drawingArgs[-2], drawingArgs[-1], "-"))
    drawingArgs.pop()
    drawingArgs.pop()

def p_PENUP(p):
    ''' PENUP : penUp '(' ')'  agregar_penup_quad '''

def p_agregar_penup_quad(p):
    'agregar_penup_quad : '
    quadManager.add((operTable["penUp"], "-", "-", "-"))

def p_PENDOWN(p):
    ''' PENDOWN : penDown '(' ')'  agregar_pendown_quad '''

def p_agregar_pendown_quad(p):
    'agregar_pendown_quad : '
    quadManager.add((operTable["penDown"], "-", "-", "-"))

def p_COLOR(p):
    ''' COLOR : color '(' EXP ')'  agregar_color_quad '''

def p_agregar_color_quad(p):
    'agregar_color_quad : '

    oper = operands[-1]["operand"]
    type = operands[-1]["type"]

    if type != "char":
        print("Error: type must be a char")

    quadManager.add((operTable["color"], oper, "-", "-"))

def p_GROSOR(p):
    ''' GROSOR : grosor '(' EXP ')' agregar_grosor_quad '''

def p_agregar_grosor_quad(p):
    'agregar_grosor_quad : '

    oper = operands[-1]["operand"]
    type = operands[-1]["type"]

    if type != "entero":
        print("Error: type must be a number")

    quadManager.add((operTable["grosor"], oper, "-", "-"))

def p_LIMPIAR(p):
    ''' LIMPIAR : limpiar '(' ')' agregar_limpiar_quad '''

def p_agregar_limpiar_quad(p):
    'agregar_limpiar_quad : '
    quadManager.add((operTable["limpiar"], "-", "-", "-"))

def p_ROTAR_IZQUIERDA(p):
    ''' ROTAR_IZQUIERDA : rotarIzquierda '(' EXP ')' agregar_rotar_izquierda_quad '''

def p_agregar_rotar_izquierda_quad(p):
    'agregar_rotar_izquierda_quad : '

    oper = operands[-1]["operand"]
    type = operands[-1]["type"]

    if type != "entero":
        print("Error: value must be an integer")

    quadManager.add((operTable["ri"], oper, "-", "-"))

def p_ROTAR_DERECHA(p):
    ''' ROTAR_DERECHA : rotarDerecha '(' EXP ')' agregar_rotar_derecha_quad '''

def p_agregar_rotar_derecha_quad(p):
    'agregar_rotar_derecha_quad : '

    oper = operands[-1]["operand"]
    type = operands[-1]["type"]

    if type != "entero":
        print("Error: value must be an integer")

    quadManager.add((operTable["rd"], oper, "-", "-"))

def p_ASIGNACION(p):
    ''' ASIGNACION : id check_if_var_exists seen_operando_variable '=' seen_operador ASIGNACION_AUX termina_asignacion
                   | id check_if_var_exists actualizar_curr_var seen_operando_variable '[' checar_si_es_arreglo  EXP  ']' termina_acceso_arreglo '=' seen_operador ASIGNACION_AUX termina_asignacion '''

def p_ASIGNACION_AUX(p):
        ''' ASIGNACION_AUX : EXPRESION
                        | EXPRESION ASIGNACION_AUX
                        '''

#Se genera el cuadruplo que asigna el valor resultante al lado izquierdo de la asignación
def p_termina_asignacion(p):
    'termina_asignacion : '
    print("TERMINA_ASIGNACION")
    rightOperand = operands[-1]["operand"]
    rightType = operands[-1]["type"]
    operands.pop(-1)
    leftOperand = operands[-1]["operand"]
    leftType = operands[-1]["type"]
    operands.pop(-1)
    operator = operators[-1]
    operators.pop(-1)
    resultType = cuboSemantico.getResultType(operator, leftType, rightType)
    print("operator = ", operator, "leftOperand = ", leftOperand, " rightOperand = ", rightOperand, " resultType = ", resultType)
    if resultType != "error":
        quadruple = (operTable[operator], rightOperand, "-", leftOperand)
        operands.append({"operand": leftOperand, "type": resultType})
        quadManager.add(quadruple)
        print(quadruple)
    else:
        print("Error: type mismatch")

#checa si la variable existe en la funcion actual o a nivel global
def p_check_if_var_exists(p):
    "check_if_var_exists : "
    directory.checkIfVarExists(p[-1])
    p[0] = p[-1]

def p_actualizar_curr_var(p):
    'actualizar_curr_var : '
    global currArrVar
    currArrVar.append(p[-1])
    p[0] = p[-1]

#verifica si la funcion a llamar existe
def p_check_if_func_exists(p):
    "check_if_func_exists : "
    global functionToCall
    functionToCall = p[-2]
    directory.checkIfFuncExists(p[-2])
    p[0] = p[-1]

def p_EXPRESION(p):
    ''' EXPRESION : EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion '>' seen_operador EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion '<' seen_operador EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion greaterOrEqual seen_operador EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion lessOrEqual seen_operador EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion equal seen_operador EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion not_equal seen_operador EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion '&' seen_operador EXP checar_pila_operadores_comparacion
                  | EXP checar_pila_operadores_comparacion '|' seen_operador EXP checar_pila_operadores_comparacion
                   '''
    p[0] = operands[-1]["operand"]

def p_EXP(p):
    ''' EXP : TERMINO checar_pila_operadores_suma_resta
            | TERMINO checar_pila_operadores_suma_resta '+' seen_operador EXP
            | TERMINO checar_pila_operadores_suma_resta '-' seen_operador EXP '''

def p_TERMINO(p):
    ''' TERMINO : FACTOR checar_pila_operadores_multi_div
                | FACTOR checar_pila_operadores_multi_div '*' seen_operador TERMINO
                | FACTOR checar_pila_operadores_multi_div '/' seen_operador TERMINO '''

def p_FACTOR(p):
    ''' FACTOR : LLAMADA_FUNCION_RETORNO
               | VAR_CTE
               | '(' agregar_fondo EXPRESION ')' quitar_fondo
               '''

def p_VAR_CTE(p):
    ''' VAR_CTE : id check_if_var_exists seen_operando_variable
                | id check_if_var_exists actualizar_curr_var seen_operando_variable '[' checar_si_es_arreglo agregar_fondo EXP  ']' quitar_fondo termina_acceso_arreglo
                | cte_i seen_operando_entero
                | cte_f seen_operando_flotante
                | cte_c seen_operando_char '''

    p[0] = p[1]

def p_LLAMADA_FUNCION_RETORNO(p):
    ''' LLAMADA_FUNCION_RETORNO : id '(' check_if_func_exists  agregar_era_quad guardar_funcion_a_llamar_ret agregar_fondo ARGUMENTOS ')' quitar_fondo verificar_argumentos termina_llamada_con_retorno
                                | id '(' check_if_func_exists  agregar_era_quad guardar_funcion_a_llamar_ret  ')' verificar_argumentos termina_llamada_con_retorno
     '''

#se guarda la funcion a llamar para después obtener la dirección donde se guarda el valor de retorno
def p_guardar_funcion_a_llamar_ret(p):
    ''' guardar_funcion_a_llamar_ret : '''
    global calledFunc
    calledFunc.append(p[-4])
    p[0] = p[-1]

#al terminar la funcion con retorno, se agrega un quadruplo para asignar el valor de retorno de la funcion a un temporal
def p_termina_llamada_con_retorno(p):
    ''' termina_llamada_con_retorno :  '''
    global calledFunc

    type = directory.getVarType(calledFunc[-1])
    returnDir = directory.getVarDir(calledFunc[-1])

    dir = AVAIL.getAddress("T", type, 1);
    directory.incrementTemporalCount(type)
    operands.append({"operand": dir, "type": type})
    print("Dir = ", dir , "    returnDir = ", directory.getVarDir(calledFunc[-1]))
    quadManager.add((operTable["="], returnDir, "-", dir))
    calledFunc.pop()



#verifica si una variable es un arreglo
def p_checar_si_es_arreglo(p):
    'checar_si_es_arreglo : '

    if not directory.isArray(currArrVar[-1]):
        print(id, " is not an array")

    operands.pop()
    p[0] = p[-1]

#Se obtiene el operando que contiene el numero del index, se crea el cuadruplo de verificar si el valor esta dentro de los limites
#Se agrega a la dirección base el offset y se guarda la memoria en pointer(se crea un cuadruplo)
def p_termina_acceso_arreglo(p):
    'termina_acceso_arreglo : '
    s1 = operands[-1]["operand"]
    s1Type = operands[-1]["type"]
    operands.pop()

    if s1Type != "entero" and s1Type != "flotante":
        print("ERROR: Index debe ser un entero")

    dimInfo = directory.getDim(currArrVar[-1])
    quadManager.add((operTable["verificar"], s1, dimInfo["linf"], dimInfo["lsup"]))
    pointer = AVAIL.getAddress("P", "entero", 1)
    baseAddr = directory.getBaseAddress(currArrVar[-1])
    baseConsAddr = AVAIL.getConsAddress(baseAddr, "entero")
    quadManager.add((operTable["+"], s1, baseConsAddr, pointer)) # + base
    operands.append({"operand": pointer, "type": "entero"})
    currArrVar.pop()

def p_agregar_fondo(p):
    'agregar_fondo : '
    operators.append("(")

def p_quitar_fondo(p):
    'quitar_fondo : '
    operators.pop(-1)

#checar si hay un operador de comparacion pendiente y evaluarlo primero
def p_checar_pila_operadores_comparacion(p):
    'checar_pila_operadores_comparacion : '
    oper = [">", "<", ">=", "lessOrEqual", "==", "!=", "&", "|"]
    p[0] = p[-1]
    if len(operators) == 0:
        return

    if operators[-1] in oper:
        crearCuadruploExpresion()


#checar si hay un operador de suma o resta pendiente y evaluarlo primero
def p_checar_pila_operadores_suma_resta(p):
    'checar_pila_operadores_suma_resta : '
    p[0] = p[-1]

    if len(operators) == 0:
        return

    if operators[-1] == "+" or operators[-1] == '-':
        crearCuadruploExpresion()

#checar si hay un operador de multiplicación o division pendiente y evaluarlo primero
def p_checar_pila_operadores_multi_div(p):
    'checar_pila_operadores_multi_div : '
    p[0] = p[-1]
    if len(operators) == 0:
        return

    if operators[-1] == "*" or operators[-1] == '/':
        crearCuadruploExpresion()

def crearCuadruploExpresion():
    rightOperand = operands[-1]["operand"]
    rightType = operands[-1]["type"]
    operands.pop(-1)
    leftOperand = operands[-1]["operand"]
    leftType = operands[-1]["type"]
    operands.pop(-1)
    operator = operators[-1]
    operators.pop(-1)

    resultType = cuboSemantico.getResultType(operator, leftType, rightType)
    #print("operator = ", operator, "leftOperand = ", leftOperand, " rightOperand = ", rightOperand, " resultType = ", resultType)

    if resultType != "error":
        result = AVAIL.getAddress("T", resultType, 1)
        directory.incrementTemporalCount(resultType)
        quadruple = (operTable[operator], leftOperand, rightOperand, result)
        operands.append({"operand": result, "type": resultType})
        quadManager.add(quadruple)
    else:
        print("Error: type mismatch")

#se agrega  el operador al stack de operadores
def p_seen_operador(p):
    'seen_operador : '
    operators.append(p[-1])
    p[0] = p[-1]

#Agrega una variable a la pila de operandos junto con su tipo
def p_seen_operando_variable(p):
    'seen_operando_variable : '
    operands.append({"operand": directory.getVarDir(p[-1]), "type": directory.getVarType(p[-1])})
    p[0] = p[-1]

#Agrega una constante a la pila de operandos junto con su tipo
def p_seen_operando_entero(p):
    'seen_operando_entero : '
    operands.append({"operand": AVAIL.getConsAddress(p[-1], "entero"), "type": "entero"})
    p[0] = p[-1]

def p_seen_operando_flotante(p):
    'seen_operando_flotante : '
    operands.append({"operand": AVAIL.getConsAddress(p[-1], "flotante"), "type": "flotante"})
    p[0] = p[-1]

def p_seen_operando_char(p):
    'seen_operando_char : '
    operands.append({"operand": AVAIL.getConsAddress(p[-1], "char"), "type": "char"})
    p[0] = p[-1]

def p_LLAMADA_FUNCION(p):
    ''' LLAMADA_FUNCION : id '(' check_if_func_exists agregar_era_quad  ARGUMENTOS ')'  verificar_argumentos
                        | id '(' check_if_func_exists agregar_era_quad ')' verificar_argumentos
     '''

def p_agregar_era_quad(p):
    'agregar_era_quad : '
    quadManager.add((operTable["ERA"], '-', '-', p[-3]))
    p[0] = p[-1]

def p_ARGUMENTOS(p):
    ''' ARGUMENTOS : EXP incrementar_numero_argumentos
                      | EXP incrementar_numero_argumentos ',' ARGUMENTOS
     '''

#incrementa el numero de argumentos en la llamada a la función
def p_incrementar_numero_argumentos(p):
    'incrementar_numero_argumentos : '
    global callNumOfArguments
    callNumOfArguments = callNumOfArguments + 1

#verifica si los argumentos son validos para una funcion
#-verifica si el numero de argumentos es el mismo que los parametros de la funcion
#-Por cada argumento verifica si su tipo es compatible con el parametro correspondiente
def p_verificar_argumentos(p):
    'verificar_argumentos : '
    global callNumOfArguments, functionToCall

    funcSignature = directory.getFuncSignature(functionToCall)
    paramAddresses = directory.getFuncSignatureAddresses(functionToCall)

    print("verificar_argumentos functionToCall = ", functionToCall)

    if len(funcSignature) != callNumOfArguments:
        print("Error when calling function ", functionToCall ," : given ", callNumOfArguments, " arguments, expected ", len(funcSignature))
        return

    for i in reversed(range(0, callNumOfArguments)):
        res = operands[-1]["operand"]
        resType = operands[-1]["type"]
        operands.pop()
        if cuboSemantico.getResultType('=', funcSignature[i], resType) == "error":
            print("Error when calling function ", functionToCall, " argument ", i, " : expected ", funcSignature[i], " recieved ", resType)
            return
        quadManager.add((operTable["parameter"], res, paramAddresses[i], "-"))

    funcStartIndex = directory.getFuncQuadStartIndex(functionToCall)
    quadManager.add((operTable["gosub"], functionToCall, "-", AVAIL.getConsAddress(funcStartIndex, "entero")))
    callNumOfArguments = 0

def p_FUNCION_RETORNO(p):
    ''' FUNCION_RETORNO : regresa '(' EXP ')' funcion_retorno_quad
     '''

def p_funcion_retorno_quad(p):
    ''' funcion_retorno_quad :
    '''
    quadManager.add((operTable["retorno"], "-", "-", operands[-1]["operand"]))

def p_LECTURA(p):
    ''' LECTURA : leer '(' LECTURA_AUX ')'
     '''

def p_LECTURA_AUX(p):
    ''' LECTURA_AUX : id check_if_var_exists lectura_quad
                    | id check_if_var_exists lectura_quad ',' LECTURA_AUX
     '''

def p_lectura_quad(p):
    'lectura_quad : '
    varName = p[-1]
    dir = directory.getBaseAddress(varName)
    quadManager.add((operTable["leer"], varName, "-", dir))
    p[0] = p[-1]

def p_ESCRIBE(p):
    ''' ESCRIBE : escribir '(' ESCRIBE_AUX ')'
     '''

def p_ESCRIBE_AUX(p):
    ''' ESCRIBE_AUX : cte_string escribe_quad_string
                    | EXPRESION escribe_quad_expresion
                    | cte_string escribe_quad_string ',' ESCRIBE_AUX
                    | EXPRESION escribe_quad_expresion ',' ESCRIBE_AUX
     '''

def p_escribe_quad_string(p):
    'escribe_quad_string : '
    dir = AVAIL.getConsAddress(p[-1], "char")
    quadManager.add((operTable["escribir"], "-", "-",  dir))
    p[0] = p[-1]

def p_escribe_quad_expresion(p):
    'escribe_quad_expresion : '
    quadManager.add((operTable["escribir"], "-", "-",  operands[-1]["operand"]))
    p[0] = p[-1]


def p_ESTATUTO_DE_DECISION(p):
    ''' ESTATUTO_DE_DECISION : si '(' EXPRESION ')' agregar_gotof entonces BLOQUE ESTATUTO_DE_DECISION_AUX agregar_linea_a_ultimo_salto
     '''

def p_ESTATUTO_DE_DECISION_AUX(p):
    ''' ESTATUTO_DE_DECISION_AUX : sino agregar_goto BLOQUE
                                 | empty
     '''

def p_agregar_gotof(p):
    'agregar_gotof : '

    res = operands[-1]["operand"]
    resType = operands[-1]["type"]

    if resType != "entero":
        print("ERROR: Not an integer(boolean)")

    jumps.append(quadManager.next())
    quadManager.add((operTable["gotof"], res, "-", "-"))
    p[0] = p[-1]

#Agregar la linea del goto en la pila de saltos
#Poner en el gotof pendiente la linea donde empieza la parte else del IF
def p_agregar_goto(p):
    'agregar_goto : '
    gotoFline = jumps[-1]
    jumps.pop(-1)
    jumps.append(quadManager.next())
    quadManager.add((operTable["goto"], "-", "-", "-"))
    quadManager.modify(gotoFline, 3, quadManager.next())
    p[0] = p[-1]

#Agregar la linea donde termina al cuadruplo que quedo pendiente(gotof o goto)
def p_agregar_linea_a_ultimo_salto(p):
    'agregar_linea_a_ultimo_salto : '
    line = jumps[-1]
    jumps.pop(-1)
    quadManager.modify(line, 3, quadManager.next())
    p[0] = p[-1]

def p_REPETICION_CONDICIONAL(p):
    ''' REPETICION_CONDICIONAL : mientras '(' agregar_a_pila_salto EXPRESION ')' agregar_gotof hacer BLOQUE rep_cond_termina
     '''

def p_agregar_a_pila_salto(p):
    'agregar_a_pila_salto : '
    jumps.append(quadManager.next())
    p[0] = p[-1]

#Agrega un goto para regresar a la linea donde empieza la expresión
#Agregar al gotof que se encuentra después de la expresión la linea donde termina la repeticion
def p_rep_cond_termina(p):
    'rep_cond_termina : '
    gotoFline = jumps[-1]
    jumps.pop(-1)
    expStartLine = jumps[-1]
    quadManager.add((operTable["goto"], "-", "-", expStartLine))
    jumps.pop(-1)
    quadManager.modify(gotoFline, 3, quadManager.next())
    p[0] = p[-1]

def p_REPETICION_NO_CONDICIONAL(p):
    ''' REPETICION_NO_CONDICIONAL : desde id check_if_var_exists crear_quad_incremento '=' seen_operador EXP iniciar_contador_no_condicional_quad hasta EXP agregar_comparacion_quad hacer BLOQUE  repeticion_no_cond_termina
                                  | desde id seen_operando_variable check_if_var_exists crear_quad_incremento actualizar_curr_var '[' checar_si_es_arreglo EXP ']' termina_acceso_arreglo '=' seen_operador EXP iniciar_contador_no_condicional_quad hasta  EXP agregar_comparacion_quad hacer BLOQUE repeticion_no_cond_termina
     '''

#Generar el quad donde la variable que depende el ciclo de repeticion se suma + 1
#Agregar quad a stack de repeticion
def p_crear_quad_incremento(p):
    'crear_quad_incremento : '
    global incrementarVariableRepeticiónQuads
    quad = (operTable["+"], directory.getVarDir(p[-1]), AVAIL.getConsAddress(1, "entero"), directory.getVarDir(p[-1]))
    incrementarVariableRepeticiónQuads.append(quad)
    p[0] = p[-1]

#Agregar el cuadruplo que inicializa el contador con el resultado la expresión
#Se agrega a la linea de saltos el numero de cuadruplo donde empieza la expresión del hasta
def p_iniciar_contador_no_condicional_quad(p):
    'iniciar_contador_no_condicional_quad : '
    res = operands[-1]["operand"]
    resType = operands[-1]["type"]
    varDir = incrementarVariableRepeticiónQuads[-1][3]

    if resType != "entero":
        print("ERROR: Not an integer")

    quadManager.add((operTable["="], res, "-", varDir))
    jumps.append(quadManager.next())

    p[0] = p[-1]

#Agregar el cuadruplo de incrementar el contador del ciclo, agregar cuadruplo goto que envia de regreso a la expresión del hasta
#Agregar la linea donde termina la repeticion al gotof pendiente
def p_repeticion_no_cond_termina(p):
    'repeticion_no_cond_termina : '
    quadManager.add(incrementarVariableRepeticiónQuads[-1])
    incrementarVariableRepeticiónQuads.pop()
    line = jumps[-1]
    jumps.pop(-1)
    quadManager.add((operTable["goto"], "-", "-", jumps[-1]))
    jumps.pop(-1)
    quadManager.modify(line, 3, quadManager.next())
    p[0] = p[-1]

#Genera el cuadruplo que compare la expresión de salida con el contador del ciclo actual
#Agrega un cuadruplo de gotof en caso de que ya no se continue en el ciclo
def p_agregar_comparacion_quad(p):
    'agregar_comparacion_quad : '
    result = AVAIL.getAddress("T", "entero", 1)
    directory.incrementTemporalCount("entero")
    varDir = incrementarVariableRepeticiónQuads[-1][3]

    res = operands[-1]["operand"]
    resType = operands[-1]["type"]

    if cuboSemantico.getResultType("<=", "entero", resType) == "error":
        print("ERROR: Not possible to compare ", resType, " with integer")

    quadManager.add((operTable["<="], varDir, res, result))
    operands.append({"operand": result, "type": "entero"})
    jumps.append(quadManager.next())
    quadManager.add((operTable["gotof"], result, "-", "-"))
    p[0] = p[-1]

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print(p)
    print("ERROR DE SINTAXIS")

# Build the parser
parser = yacc.yacc()

while True:

    file = open("pruebas.txt","r+")

    code = ""

    for line in file.readlines():
        code = code + line

    print("CODE")
    print(code)

    result = parser.parse(code)

    consTable = AVAIL.consTable

    break
