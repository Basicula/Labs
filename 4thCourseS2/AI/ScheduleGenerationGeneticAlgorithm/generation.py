from data import *

import random
import string

class Population:
    def __init__(self, size = 0, data = None):
        self.size = size
        self.data = data
        self.schedules = []
        if not data is None:
            for i in range(self.size):
                schedule = Schedule(self.data)
                schedule.random()
                self.schedules.append(schedule)

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
        crossover = Schedule(self.data)
        crossover.random()
        for i in range(len(crossover.lessons)):
            crossover.lessons[i] = random.choice(schedules).lessons[i]
        return crossover

    def mutate_schedule(self, schedule):
        temp_schedule = Schedule(self.data)
        temp_schedule.random()
        for i in range(len(schedule.lessons)):
            if self.mutation_rate > random.random():
                schedule.lessons[i] = temp_schedule.lessons[i]
        return schedule

    def select_tournament_population(self, population):
        tournament_population = Population()
        for i in range(self.tournament_selection):
            tournament_population.schedules.append(random.choice(population.schedules))
        return tournament_population


if __name__ == "__main__":
    data = generate_random_data(20,10,10,10)
    population = Population(10, data)
    genalgo = GeneticAlgorithm(data)
    num_conflicts = 10000
    while num_conflicts > 0:
        population = genalgo.evolve(population)
        schedules = population.schedules
        schedules.sort(key = lambda x : x.calculate_fitness(), reverse=True)
        if schedules[0].conflicts_cnt < num_conflicts:
            print(schedules[0])
            num_conflicts = schedules[0].conflicts_cnt
