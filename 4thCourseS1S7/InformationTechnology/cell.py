from datatype import *


def isInteger(data):
    try:
        int(data)
    except ValueError:
        return False
    return True


def isReal(data):
    try:
        float(data)
    except ValueError:
        return False
    return True
    
def isRealInvl(data,interval):
    if interval is None:
        return isReal(data)
    if not isReal(data):
        return False
    data = float(data)
    return data >= interval[0] and data <= interval[1]

def isChar(data):
    return len(data) < 2


class Cell:
    def __init__(self, data="", type=DataType.String):
        self.data = data
        self.type = type
        self.optionalInfo = None
        self.required = False

    def isPresentData(self):
        return self.data != ""

    def setData(self, data):
        if self.optionalInfo != None and not Cell.isValidData(data, self.type,self.optionalInfo[1]) or not Cell.isValidData(data, self.type):
            print(data,self.type)
            raise Exception("Invalid data for current cell")
        self.data = data

    @property
    def __dict__(self):
        if self.optionalInfo == None:
            return {
                'data': self.data,
                'type': self.type
            }
        else:
            return {
                'data': self.data,
                'type': self.type,
                self.optionalInfo[0] : self.optionalInfo[1]
            }

    @staticmethod
    def fromDict(dict):
        if 'interval' in dict.keys() :
            res = Cell(dict['data'], DataType.fromDict(dict['type'])) 
            res.optionalInfo = ['interval',dict['interval']]
            return res
        return Cell(dict['data'], DataType.fromDict(dict['type']))

    @staticmethod
    def isValidData(data, type, optionalInfo = None):
        if type == DataType.Integer:
            return isInteger(data)
        elif type == DataType.Real:
            return isReal(data)
        elif type == DataType.Char:
            return isChar(data)
        elif type == DataType.String:
            return True
        elif type == DataType.Picture:
            return True
        elif type == DataType.RealInvl:
            return isRealInvl(data,optionalInfo)
        else:
            return False
