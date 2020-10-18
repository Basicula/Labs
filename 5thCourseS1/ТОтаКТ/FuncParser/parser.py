from common import *

import copy
import matplotlib.pyplot as plt

class Function:
    def __init__(self, func_string):
        self.string = func_string
        self.curr_id = 0
        self.prepare_string()
        
    def __call__(self, x):
        self.curr_id = 0
        x = copy.copy(x)
        return self.parse_expression(x)
        
    def prepare_string(self):
        for ch in WHITESPACES:
            self.string = self.string.replace(ch, "")
        
    def has_next(self):
        return len(self.string) > self.curr_id
        
    def peek(self):
        return self.string[self.curr_id]
        
    def parse_expression(self, x):
        return self.parse_addition(x)
        
    def parse_addition(self, x):
        res = self.parse_multiplication(x)
        
        while self.has_next():
            ch = self.peek()
            
            if not ch in "+-":
                break
            
            self.curr_id += 1
            
            if ch == '+':
                res += self.parse_multiplication(x)
            else:
                res -= self.parse_multiplication(x)
        
        return res
        
    def parse_multiplication(self, x):
        res = self.parse_parentheses(x)
        
        while self.has_next():
            ch = self.peek()
            
            if not ch in "*/":
                break
            
            self.curr_id += 1
            temp = self.parse_parentheses(x)

            if ch == '*':
                res *= temp
            else:
                res /= temp
                
        return res
        
    def parse_parentheses(self, x):
        ch = self.peek()
        
        if ch == '(':
            self.curr_id += 1
            
            val = self.parse_expression(x)
            
            ch = self.peek()
            if ch != ')':
                raise Exception("missing closing bracket")
            self.curr_id += 1
            return val
        return self.parse_negative(x)
        
    def parse_negative(self, x):
        ch = self.peek()
        if ch == '-':
            self.curr_id += 1
            return -1 * self.parse_parentheses(x)
        return self.parse_value(x)
        
    def parse_value(self, x):
        ch = self.peek()
        if ch in NUMBERS:
            return self.parse_number()
        return self.parse_name(x)
        
    def parse_number(self):
        decimal_found = False
        number = ''
        
        while self.has_next():
            ch = self.peek()
            
            if ch == '.':
                if decimal_found:
                    raise Exception("double dot in the number")
                decimal_found = True
                number += ch
            elif ch in NUMBERS:
                number += ch
            else:
                break
            self.curr_id += 1
        
        return string_to_float(number)

    def parse_name(self, x):
        name = ''
        while self.has_next():
            ch = self.peek()
            if ch in NAMECHARS:
                name += ch
            else:
                break
            self.curr_id += 1
        
        if name in FUNCTIONS.keys():
            return FUNCTIONS[name](self.parse_parentheses(x))
        
        if name in CONSTANTS.keys():
            return CONSTANTS[name]
            
        if name in VARNAMES:
            return copy.copy(x)
            
        raise Exception("undefined name " + name)

    
if __name__ == "__main__":
    func = Function("2 + 2")
    print(func(12312))
    x = np.array([123,12312,31,23,12,3],dtype=float)
    func = Function("x+2*x")
    print(func(x))
    x = np.arange(-2,2,0.01)
    func = Function("pow(x,2)")
    plt.plot(x, func(x))
    func = Function("tg(sin(x*x/0.25)*cos(x + 5))")
    plt.plot(x, func(x))
    func = Function("2*sin(1/(exp(3*x)+1)-tg(x+PI/2))")
    plt.plot(x, func(x))
    plt.show()
    
    
    