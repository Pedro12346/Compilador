import ply.lex as lex

reserved = {
    'programa': 'programa',
    'variables': 'variables',
    'entero': 'entero',
    'flotante': 'flotante',
    'void' : 'void',
    'char': 'char',
    'funcion': 'funcion',
    'principal': 'principal',
    'regresa': 'regresa',
    'leer': 'leer',
    'escribir': 'escribir',
    'si': 'si',
    'entonces': 'entonces',
    'sino': 'sino',
    'mientras': 'mientras',
    'hacer': 'hacer',
    'desde': 'desde',
    'hasta': 'hasta',
    'linea': 'linea',
    'circulo': 'circulo',
    'arco': 'arco',
    'penUp': 'penUp',
    'penDown': 'penDown',
    'color': 'color',
    'grosor': 'grosor',
    'punto': 'punto',
    'limpiar': 'limpiar',
    'rotarDerecha': 'rotarDerecha',
    'rotarIzquierda': 'rotarIzquierda',
    'finVar' : 'finVar',
}

tokens = [
   'equal',
   'not_equal',
   'greaterOrEqual',
   'lessOrEqual',
   'cte_string',
   'or',
   'cte_i',
   'cte_f',
   'cte_c',
   'id',
] + list(reserved.values());

literals = ['+', '-', '*', '/', '(', ')', '{', '}', '&', '|', '=', ';', ':', '>', '<', '<', '>', ',', '[', ']'];

t_equal = r'=='
t_greaterOrEqual = r'>='
t_lessOrEqual = r'<='
t_not_equal = r'!='
t_cte_string = r'\".*?\"'

def t_cte_f(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_cte_i(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_cte_c(t):
    r'\'[a-zA-Z0-9]\' '
    return t

def t_id(t):
    r'[a-zA-Z][a-zA-z0-9]*'
    t.type = reserved.get(t.value, 'id');
    return t

def t_comment(t):
    r'%%.*\n'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'

lexer = lex.lex()
