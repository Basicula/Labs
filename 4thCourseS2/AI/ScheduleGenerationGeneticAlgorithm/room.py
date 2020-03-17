class Room:
    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity

    def __repr__(self):
        return "R" + str(self.number) + "(" + str(self.capacity) + ")"
