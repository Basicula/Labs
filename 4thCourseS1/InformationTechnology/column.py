from datatype import *


class Column:
    def __init__(self, header, type):
        self.header = header
        self.type = type
        self.optionalInfo = None

    @property
    def __dict__(self):
        if self.optionalInfo == None:
            return {
                'header': self.header,
                'type': self.type.__dict__
            }
        else:
            return {
                'header': self.header,
                'type': self.type.__dict__,
                self.optionalInfo[0]: self.optionalInfo[1]
            }

    @staticmethod
    def fromDict(dict):
        column = Column(dict['header'], DataType.fromDict(dict['type']))
        if 'interval' in dict:
            column.optionalInfo = ['interval',dict['interval']]
        return column
