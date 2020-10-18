import matplotlib.pyplot as plt
from common import *

class ShuntingYard:
    def __init__(self, expression):
        self.expression = expression
        self.prepare_string()
        self.tokenize()
        self.infix()
        
        #check
        self.postfix(0)
        
    def __call__(self, x):
        return self.postfix(x)
        
    def prepare_string(self):
        for ch in WHITESPACES:
            self.expression = self.expression.replace(ch, "")
        
    def infix(self):
        operator_stack = []
        self.postfix_tokens = []
        
        for token in self.tokens:
            if is_number(token):
                self.postfix_tokens.append(token)
            elif token in CONSTANTS:
                self.postfix_tokens.append(token)
            elif token in VARNAMES:
                self.postfix_tokens.append(token)
            elif token in FUNCTIONS:
                operator = FUNCTIONS[token]
                while operator_stack:
                    if not operator_stack[-1] in FUNCTIONS:
                        break
                    curr_stack_operator = FUNCTIONS[operator_stack[-1]]
                    if curr_stack_operator['priority'] <= operator['priority'] and operator['assoc'] == 'left':
                        self.postfix_tokens.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')' or token == ',':
                if not '(' in operator_stack:
                    raise Exception("Missing opening bracket")
                while operator_stack and operator_stack[-1] != '(':
                    self.postfix_tokens.append(operator_stack.pop())
                if operator_stack[-1] == '(' and token == ')':
                    operator_stack.pop()
            else:
                raise Exception("Invalid or unsupported function " + token)
        
        if '(' in operator_stack:
            raise Exception("Missing closing brakcet")
        
        while operator_stack:
            self.postfix_tokens.append(operator_stack.pop())
    
    def postfix(self, x):
        result_stack = []
        tokens = self.postfix_tokens[:]
        
        while tokens:
            token = tokens.pop(0)
            if token in FUNCTIONS:
                operator = FUNCTIONS[token]
                args = []
                for i in range(operator['arity']):
                    if len(result_stack) == 0:
                        raise Exception("Too few operands for operation " + token)
                    args.append(result_stack.pop())
                    args.reverse()
                
                result_stack.append(operator['func'](*args))
            elif token in CONSTANTS:
                result_stack.append(CONSTANTS[token])
            elif is_number(token):
                result_stack.append(token)
            elif token in VARNAMES:
                result_stack.append(x)
        
        return result_stack.pop()
        
    def collect_while(self, from_id, custom_condition):
        to_id = from_id
        while to_id < len(self.expression) and custom_condition(self.expression[to_id]):
            to_id += 1
        return self.expression[from_id:to_id]
        
    def tokenize(self):
        self.tokens = []
        
        token_start = 0
        expression_curr = 0
        
        while expression_curr < len(self.expression):
            token_start_char = self.expression[token_start]
            
            token = ''
            if token_start_char in NUMBERS:
                condition = lambda ch : ch in NUMBERS or ch == '.'
                token = self.collect_while(token_start, condition)
                self.tokens.append(string_to_float(token))
                expression_curr += len(token)
            elif token_start_char in NAMECHARS:
                condition = lambda ch : ch in NAMECHARS
                token = self.collect_while(token_start, condition)
                if token in FUNCTIONS or token in CONSTANTS or token in VARNAMES:
                    self.tokens.append(token)
                else:
                    raise Exception("undefind name " + token)
                expression_curr += len(token)
            else:
                self.tokens.append(token_start_char)
                expression_curr += 1
                
            token_start = expression_curr
        
    def plot(self, x1, x2):
        if x2 < x1:
            raise Exception("Wrong interval")
        x = np.arange(x1, x2, (x2-x1)/1000)
        plt.plot(x, self(x))
        plt.show()
        
    def tabulate(self, x1, x2, step = 0.1):
        if x2 < x1:
            raise Exception("Wrong interval")
            
        xs = np.arange(x1, x2 + step, step)
        ys = self(xs)
        
        print('x\ty')
        for x, y in zip(xs, ys):
            print('{0:0.2f}'.format(x),'\t', '{0:0.2f}'.format(y))
    
if __name__ == '__main__':
    test = ShuntingYard("1+2+3+4")
    print(test(1))
    test = ShuntingYard("2 + 2 * 2")
    print(test(12))
    test = ShuntingYard("2*sin(1/(exp(3*x)+1)-tg(x+PI/2))")
    print(test(12))
    test = ShuntingYard("sin ( cos ( 3 ) / 3 * PI )")
    print(test(1))
    test = ShuntingYard("pow(x,0.5)")
    test.tabulate(0, 4)
    print(test(9))
    
    expression = ShuntingYard("2*sin(1/(exp(3*x)+1)-tg(x+PI/2))")
    expression(0)
    expression(2)
    
    
    
    