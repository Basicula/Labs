class DayTime:
    def __init__(self, day, time):
        self.day = day
        self.time = time

    def __eq__(self, other):
        return self.day == other.day and self.time == other.time

    def __repr__(self):
        return self.day + " " + self.time
