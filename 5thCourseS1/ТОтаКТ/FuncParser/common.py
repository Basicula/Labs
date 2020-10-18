import numpy as np
import math

CONSTANTS = {
    'PI'    : math.pi,
    'E'     : math.e,
}

PFUNCTIONS = {
    'abs'   : abs,
    'cos'   : np.cos,
    'exp'   : np.exp,
    'pow'   : np.power,
    'sin'   : np.sin,
    'sqrt'  : np.sqrt,
    'tg'    : np.tan,
    'sqrt'  : np.sqrt
}

FUNCTIONS = {
    '+'     : {'priority' : 4, 'assoc' : 'left', 'arity' : 2, 'func' : lambda a, b : a + b}, 
    '-'     : {'priority' : 4, 'assoc' : 'left', 'arity' : 2, 'func' : lambda a, b : a - b}, 
    '*'     : {'priority' : 3, 'assoc' : 'left', 'arity' : 2, 'func' : lambda a, b : a * b}, 
    '/'     : {'priority' : 3, 'assoc' : 'left', 'arity' : 2, 'func' : lambda a, b : a / b}, 
    'abs'   : {'priority' : 2, 'assoc' : 'left', 'arity' : 1, 'func' : abs},
    'cos'   : {'priority' : 2, 'assoc' : 'left', 'arity' : 1, 'func' : np.cos},
    'exp'   : {'priority' : 2, 'assoc' : 'left', 'arity' : 1, 'func' : np.exp},
    'pow'   : {'priority' : 2, 'assoc' : 'left', 'arity' : 2, 'func' : np.power},
    'sin'   : {'priority' : 2, 'assoc' : 'left', 'arity' : 1, 'func' : np.sin},
    'sqrt'  : {'priority' : 2, 'assoc' : 'left', 'arity' : 1, 'func' : np.sqrt},
    'tg'    : {'priority' : 2, 'assoc' : 'left', 'arity' : 1, 'func' : np.tan},
}

NUMBERS = '0123456789'

WHITESPACES = ' \t\n\r'

NAMECHARS = '_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'

VARNAMES = 'x'

def string_to_float(number):
    val = 0
    try:
        val = float(number)
    except ValueError:
        raise Exception("invalid number " + number)
    else:
        if len(number) == 0:
            raise Exception("no number")
        if number[0] == '0' and number[1] != '.':
            raise Exception("number can't have leading zero")
        if number.count('.') > 1:
            raise Exception("strange number with dots")
    return val


def is_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False