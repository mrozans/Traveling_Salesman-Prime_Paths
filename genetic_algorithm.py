import random
from datetime import datetime
import pandas as pd
from algorithm import total_distance


class GeneticAlgorithm:
    def __init__(self, path, df_cities):
        self.path = path
        self.population = []
        self.population_size = 100
        self.parents = []
        self.children = []
        self.df_cities = df_cities

    def pmx_method(self, subject_1, subject_2):
        random.seed(datetime.now())
        borders = random.sample(range(0, len(subject_1)), 2)
        borders = [1,4]
        borders.sort()
        subject_front_1 = subject_1[:borders[0]]
        subject_front_2 = subject_2[:borders[0]]
        subject_mid_1 = subject_1[borders[0]: borders[1]]
        subject_mid_2 = subject_2[borders[0]:borders[1]]
        subject_end_1 = subject_1[borders[1]:]
        subject_end_2 = subject_2[borders[1]:]
        # print('Sub 1: ' + str(subject_mid_1) + '\n')
        # print('Sub 2: ' + str(subject_mid_2) + '\n')
        pairs = []
        for i in range(0, len(subject_mid_1)):
            pairs.append([subject_mid_1[i], subject_mid_2[i]])
        # print('Pary: ' + str(pairs) + '\n')
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
        #print('Przefiltrowane: ' + str(pairs))

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
        if len(child_1) > len(set(child_1)):
            print("xd")
        child_2 = subject_front_2 + subject_mid_1 + subject_end_2
        if len(child_2) > len(set(child_2)):
            print(borders)
            print(subject_1)
            print(subject_2)
            print(child_1)
            print(child_2)
        # print('Parent 1: ' + str(subject_1))
        # print('Parent 2: ' + str(subject_2))
        # print('Child 1: ' + str(child_1))
        # print('Child 2: ' + str(child_2))
        return child_1, child_2

    def generate_population(self):
        for i in range(self.population_size):
            chromosome = []
            gens = list(self.path.copy())
            random.shuffle(gens)
            for gen in gens:
                chromosome.append(gen)
            self.population.append(chromosome)

    def roulette_wheel(self):
        self.parents = []
        fitness = []
        total = 0
        for i in range(self.population_size):
            fitness.append(total_distance(self.df_cities, self.population[i]))
            total += fitness[i]
        for i in range(self.population_size):
            fitness[i] = (1 - fitness[i]/total) / (self.population_size - 1)
        for i in range(self.population_size):
            roll = random.uniform(0, 1)
            so_far = 0
            for j in range(self.population_size):
                so_far += fitness[j]
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
            if i > 6 and index != (len(self.parents)-1):
                self.children.append(parent)
                continue
            a, b = self.pmx_method(parent, self.parents[index + 1])
            self.children.append(a)
            self.children.append(b)
            skip = True


df_cities = pd.read_csv('input/cities2.csv')
obj = GeneticAlgorithm([2, 3, 4, 5, 6, 7], df_cities)
obj.generate_population()
obj.roulette_wheel()
obj.crossover()
for i in obj.children:
    if len(i) > len(set(i)):
        print("wow")
obj.mutate()
for i in obj.children:
    if len(i) > len(set(i)):
        print("lol")


