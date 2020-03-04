class Lesson:
    def __init__(self, room, time, teacher, group, subject):
        self.room = room
        self.time = time
        self.teacher = teacher
        self.group = group
        self.subject = subject

    def __repr__(self):
        return self.subject.name + "\n" + repr(self.room) + "\n" + self.teacher
