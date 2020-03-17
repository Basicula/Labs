from teacher import *
from room import *
from group import *
from schedule import *
from day_time import *
from subject import *

import random
import string

class Data:
    def __init__(self):
        self.teachers = []
        self.rooms = []
        self.subjects = []
        self.groups = []

        self.generate_times()

    def generate_times(self):
        self.days = ["MON", "TUE", "WED", "THU", "FRI"]
        self.time_intervals = ["08:40-10:15", "10:35-12:10", "12:20-13:55"]
        self.times = []
        for day in self.days:
            for time in self.time_intervals:
                self.times.append(DayTime(day, time))

    def add_rooms(self, rooms):
        self.rooms += rooms

    def add_teachers(self, teachers):
        self.teachers += teachers

    def add_subjects(self, subjects):
        self.subjects += subjects

    def add_groups(self, groups):
        self.groups += groups

def generate_random_data(rooms_cnt, teachers_cnt, groups_cnt, max_subjects_for_group):
    data = Data()
    room_capacities = [15, 30]
    for i in range(rooms_cnt):
        data.rooms.append(Room(random.randrange(0,100), random.choice(room_capacities)))

    letters = list(string.ascii_letters)
    for i in range(teachers_cnt):
        random.shuffle(letters)
        length = random.randrange(5,10)
        data.teachers.append(''.join(letters[:length]))

    subjects_name = ["AI", "NN", "Refactoring", "MATH", "PHYSICS", "Algo", "ML", "Geometry", "Graphics", "MathAn"]
    teachers = data.teachers
    for i in range(len(subjects_name)):
        available_teachers = random.randrange(1, teachers_cnt / 2)
        random.shuffle(teachers)
        subject_teachers = teachers[0:available_teachers]
        data.subjects.append(Subject(random.choice(subjects_name), subject_teachers))

    capital = list(string.ascii_uppercase)
    subjects = data.subjects
    for i in range(groups_cnt):
        random.shuffle(capital)
        group_name = capital[0] + str(random.randrange(1,5)) + str(random.randrange(1,4))
        group_size = random.randrange(10,29)
        group = Group(group_name, group_size)
        cnt = random.randrange(max_subjects_for_group // 2, max_subjects_for_group)
        random.shuffle(subjects)
        group.add_subjects(subjects[:cnt])
        data.groups.append(group)

    return data
