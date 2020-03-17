from lesson import *
from day_time import *

from prettytable import PrettyTable
import random

class Schedule:
    def __init__(self, data):
        self.data = data
        self.conflicts_cnt = 0
        self.fitness = -1
        self.lessons = []

    def random(self):
        for group in self.data.groups:
            for subject in group.subject_list:
                room = random.choice(self.data.rooms)
                teacher = random.choice(subject.teachers)
                time = random.choice(self.data.times)
                self.lessons.append(Lesson(room, time, teacher, group, subject))

    def calculate_fitness(self):
        self.conflicts_cnt = 0
        for i in range(len(self.lessons)):
            if self.lessons[i].room.capacity < self.lessons[i].group.size:
                self.conflicts_cnt += 1
            for j in range(i+1, len(self.lessons)):
                if self.lessons[i].time == self.lessons[j].time:
                    if self.lessons[i].room == self.lessons[j].room:
                        self.conflicts_cnt += 1
                    if self.lessons[i].teacher == self.lessons[j].teacher:
                        self.conflicts_cnt += 1
        return 1 / (self.conflicts_cnt + 1)

    def __repr__(self):
        table = PrettyTable()
        table.field_names = [""] + self.data.groups;

        for day in self.data.days:
            for time_interval in self.data.time_intervals:
                time = DayTime(day, time_interval)
                row = [time] + [""]*len(self.data.groups)
                for lesson in self.lessons:
                    if lesson.time == time:
                        idx = self.data.groups.index(lesson.group) + 1
                        row[idx] += repr(lesson)
                table.add_row(row)
        return str(self.conflicts_cnt) + "\n" + str(table)
