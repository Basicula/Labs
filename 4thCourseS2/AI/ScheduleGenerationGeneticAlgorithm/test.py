import random
import string

class Teacher:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
        
class Room:
    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity
    
    def __repr__(self):
        return "R" + str(self.number) + "(" + str(self.capacity) + ")"

class Subject:
    def __init__(self, name, teachers):
        self.name = name
        self.teachers = teachers

    def __repr__(self):
        return self.name
    
class Group:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.subject_list = []
        
    def add_subjects(self, subjects):
        self.subject_list += subjects
        
    def __repr__(self):
        return self.name + "(" + str(self.size) + ")"
        
class Time:
    def __init__(self, day, time):
        self.day = day
        self.time = time
    
    def __repr__(self):
        return self.day + " " + self.time
    
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

class Lesson:
    def __init__(self, room, time, teacher, group, subject):
        self.room = room
        self.time = time
        self.teacher = teacher
        self.group = group
        self.subject = subject

class Data:
    def __init__(self):
        self.teachers = []
        self.rooms = []
        self.subjects = []
        self.groups = []
        
        self.generate_times()
        
    def generate_times(self):
        days = ["MON", "TUE", "WED", "THU", "FRI"]
        times = ["08:40-10:15", "10:35-12:10", "12:20-13:55"]
        self.times = []
        for day in days:
            for time in times:
                self.times.append(Time(day, time))

    def add_rooms(self, rooms):
        self.rooms += rooms

    def add_teachers(self, teachers):
        self.teachers += teachers

    def add_subjects(self, subjects):
        self.subjects += subjects

    def add_groups(self, groups):
        self.groups += groups

class Population:
    def __init__(self, size = 0, data = None):
        self.size = size
        self.data = data
        self.schedules = []
        if not data is None:
            for i in range(self.size):
                self.schedules.append(Schedule(self.data).random())

class GeneticAlgorithm:
    def __init__(self, data, mutation_rate = 0.1, elit_cnt = 2, population_size = 10, tournament_selection = 5):
        self.data = data
        self.mutation_rate = mutation_rate
        self.elit_cnt = elit_cnt
        self.population_size = population_size
        self.tournament_selection = tournament_selection
        
    def evolve(self, population):
        return self.mutate_population(self.crossover_population(population))
        
    def crossover_population(self, population):
        crossover = Population()
        crossover.schedules = population.schedules[0:self.elit_cnt]
        i = self.elit_cnt
        while i < self.population_size:
            schedule1 = self.select_tournament_population(population).schedules[0]
            schedule2 = self.select_tournament_population(population).schedules[0]
            crossover.schedules.append(self.crossover_schedule([schedule1, schedule2]))
            i+=1
        return crossover
        
    def mutate_population(self, population):
        for i in range(self.elit_cnt, self.population_size):
            self.mutate_schedule(population.schedules[i])
        return population
        
    def crossover_schedule(self, schedules):
        crossover = Schedule(self.data).random()
        for i in range(len(crossover.lessons)):
            crossover.lessons[i] = random.choice(schedules).lessons[i]
        return crossover

    def mutate_schedule(self, schedule):
        temp_schedule = Schedule(self.data).random()
        for i in range(len(schedule.lessons)):
            if self.mutation_rate > random.random():
                schedule.lessons[i] = temp_schedule.lessons[i]
        return schedule
        
    def select_tournament_population(self, population):
        tournament_population = Population()
        for i in range(self.tournament_selection):
            tournament_population.schedules.append(random.choice(population.schedules))
        return tournament_population
        
        
def generate_random_data(rooms_cnt, teachers_cnt, groups_cnt, max_subjects_for_group):
    data = Data()
    room_capacities = [15, 30]
    for i in range(rooms_cnt):
        data.rooms.append(Room(random.randrange(0,100), random.choice(room_capacities)))
    print(data.rooms)
        
    letters = list(string.ascii_letters)
    for i in range(teachers_cnt):
        random.shuffle(letters)
        length = random.randrange(5,len(letters))
        data.teachers.append(''.join(letters[:length]))
    print(data.teachers)
        
    subjects_name = ["AI", "NN", "Refactoring", "MATH", "PHYSICS"]
    teachers = data.teachers
    for i in range(len(subjects_name)):
        available_teachers = random.randrange(1, teachers_cnt / 2)
        random.shuffle(teachers)
        subject_teachers = teachers[0:available_teachers]
        data.subjects.append(Subject(random.choice(subjects_name), subject_teachers))
    print(data.subjects)
    
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
    print(data.groups)
        
    return data


if __name__ == "__main__":
    data = generate_random_data(10,10,10,5)
    population = Population(10, data)
    genalgo = GeneticAlgorithm(data)
    