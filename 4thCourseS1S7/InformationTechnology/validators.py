from PyQt5.QtGui import QValidator


class CharValidator(QValidator):
    def __init__(self):
        QValidator.__init__(self)

    def validate(self, s, pos):
        if len(s) > 1:
            return (QValidator.Invalid, s, pos)
        return (QValidator.Acceptable, s, pos)

    def fixup(self, s):
        pass


def smartCheckGood(n, mn):
    d1 = mn - n
    n *= 10
    d2 = mn - n
    if d2 < d1:
        return True
    else:
        return False


class RealInvlValidator(QValidator):
    def __init__(self, lineeditor):
        QValidator.__init__(self)
        self.min = float("-inf")
        self.max = float("inf")
        self.lineeditor = lineeditor

    def setRange(self, min, max):
        self.min = min
        self.max = max

    def validate(self, s, pos):
        if len(s) == 0 or s == '-':
            return (QValidator.Intermediate, s, pos)
        try:
            n = float(s)
        except:
            return (QValidator.Invalid, s, pos)
        if n > self.max:
            return (QValidator.Invalid, s, pos)
        if n < self.min:
            if smartCheckGood(n, self.min):
                return (QValidator.Intermediate, s, pos)
            else:
                return (QValidator.Invalid, s, pos)
        return (QValidator.Acceptable, s, pos)

    def fixup(self, s):
        self.lineeditor.setText(str(self.min))
