class Group:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.subject_list = []

    def add_subjects(self, subjects):
        self.subject_list += subjects

    def __repr__(self):
        return self.name + "(" + str(self.size) + ")"
