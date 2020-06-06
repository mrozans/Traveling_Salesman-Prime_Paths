import random
from datetime import datetime
import pandas as pd
from list_organizing import total_distance


class GeneticAlgorithm:
    def __init__(self, path, df_cities, prev_id, next_id, prime_cities):
        self.path = path
        self.population = []
        self.population_size = 100
        self.iterations = 200
        self.parents = []
        self.children = []
        self.fitness = []
        self.df_cities = df_cities
        self.prev_id = prev_id
        self.next_id = next_id
        self.prime_cities = prime_cities

    def pmx_method(self, subject_1, subject_2):
        random.seed(datetime.now())
        borders = random.sample(range(0, len(subject_1)), 2)
        borders.sort()
        subject_front_1 = subject_1[:borders[0]]
        subject_front_2 = subject_2[:borders[0]]
        subject_mid_1 = subject_1[borders[0]: borders[1]]
        subject_mid_2 = subject_2[borders[0]:borders[1]]
        subject_end_1 = subject_1[borders[1]:]
        subject_end_2 = subject_2[borders[1]:]
        pairs = []
        for i in range(0, len(subject_mid_1)):
            pairs.append([subject_mid_1[i], subject_mid_2[i]])
        while True:
            for i in range(0, len(pairs)):
                for k in range(i + 1, len(pairs)):
                    if pairs[i][1] == pairs[k][0]:
                        pairs.append([pairs[i][0], pairs[k][1]])
                        del pairs[i]
                        del pairs[k - 1]
                        break
                    elif pairs[i][0] == pairs[k][1]:
                        pairs.append([pairs[k][0], pairs[i][1]])
                        del pairs[i]
                        del pairs[k - 1]
                        break
            finished = True
            for i in range(0, len(pairs)):
                for k in range(i + 1, len(pairs)):
                    if pairs[i][1] == pairs[k][0] or pairs[i][0] == pairs[k][1]:
                        finished = False
                        break
            if finished:
                break
        same_pairs = []
        for i in range(0, len(pairs)):
            if pairs[i][0] == pairs[i][1]:
                same_pairs.insert(0, i)
        for i in same_pairs:
            del pairs[i]
        for i in range(0, len(subject_front_1)):
            for pair in pairs:
                if subject_front_1[i] == pair[1]:
                    subject_front_1[i] = pair[0]
                if subject_front_2[i] == pair[0]:
                    subject_front_2[i] = pair[1]
        for i in range(0, len(subject_end_1)):
            for pair in pairs:
                if subject_end_1[i] == pair[1]:
                    subject_end_1[i] = pair[0]
                if subject_end_2[i] == pair[0]:
                    subject_end_2[i] = pair[1]
        child_1 = subject_front_1 + subject_mid_2 + subject_end_1
        child_2 = subject_front_2 + subject_mid_1 + subject_end_2
        return child_1, child_2

    def generate_population(self):
        for i in range(self.population_size):
            chromosome = []
            gens = list(self.path.copy())
            random.shuffle(gens)
            for gen in gens:
                chromosome.append(gen)
            self.population.append(chromosome)

    def calculate_fitness(self):
        self.fitness = []
        total = 0
        for i in range(self.population_size):
            self.fitness.append(total_distance(self.df_cities, [self.prev_id] + self.population[i] + [self.next_id],
                                               self.prime_cities))
            total += self.fitness[i]
        for i in range(self.population_size):
            self.fitness[i] = (1 - self.fitness[i]/total) / (self.population_size - 1)

    def get_best(self):
        max_fitness = self.fitness[0]
        index = 0
        for i in range(1, len(self.fitness)):
            if self.fitness[i] > max_fitness:
                max_fitness = self.fitness[i]
                index = i
        return self.population[index], self.fitness[index]

    def roulette_wheel(self):
        self.parents = []
        for i in range(self.population_size):
            roll = random.uniform(0, 1)
            so_far = 0
            for j in range(self.population_size):
                so_far += self.fitness[j]
                if so_far >= roll:
                    self.parents.append(self.population[j])
                    break

    def mutate(self):
        for child in self.children:
            i = random.randrange(1)
            if i != 0:
                continue
            a = random.randrange(len(child))
            b = random.randrange(len(child))
            child[a], child[b] = child[b], child[a]

    def crossover(self):
        index = -1
        skip = False
        for parent in self.parents:
            if skip:
                skip = False
                continue
            index = index + 1
            i = random.randrange(10)
            if i > 6 and index > (len(self.parents)-2):
                self.children.append(parent)
                continue
            a, b = self.pmx_method(parent, self.parents[index + 1])
            self.children.append(a)
            self.children.append(b)
            skip = True

    def insert_elite(self, elite, elite_fitness):
        for i in range(self.population_size):
            if self.fitness[i] < elite_fitness:
                self.population[i] = elite
                self.fitness[i] = elite_fitness
                return

    def calculate(self):
        self.generate_population()
        self.calculate_fitness()
        for i in range(self.iterations):
            elite, elite_fitness = self.get_best()
            self.roulette_wheel()
            self.crossover()
            self.mutate()
            self.population = self.children.copy()
            self.children = []
            self.calculate_fitness()
            self.insert_elite(elite, elite_fitness)
        result, result1 = self.get_best()
        return result


