import random
from datetime import datetime


class GeneticAlgorithm:
    def __init__(self, path):
        self.path = path

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
        print('Sub 1: ' + str(subject_mid_1) + '\n')
        print('Sub 2: ' + str(subject_mid_2) + '\n')
        pairs = []
        for i in range(0, len(subject_mid_1)):
            pairs.append([subject_mid_1[i], subject_mid_2[i]])
        print('Pary: ' + str(pairs) + '\n')
        while True:
            for i in range(0, len(pairs)):
                for k in range(i + 1, len(pairs)):
                    if pairs[i][1] == pairs[k][0]:
                        pairs.append([pairs[i][0], pairs[k][1]])
                        del pairs[i]
                        del pairs[k - 1]
                        break
            finished = True
            for i in range(0, len(pairs)):
                for k in range(i + 1, len(pairs)):
                    if pairs[i][1] == pairs[k][0]:
                        finished = False
                        break
            if finished:
                break
        for i in range(0, len(pairs)):
            if pairs[i][0] == pairs[i][1]:
                del pairs[i]
        print('Przefiltrowane: ' + str(pairs))

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
        print('Parent 1: ' + str(subject_1))
        print('Parent 2: ' + str(subject_2))
        print('Child 1: ' + str(child_1))
        print('Child 2: ' + str(child_2))
        return child_1, child_2


obj = GeneticAlgorithm([1, 2, 3])

obj.pmx_method([1, 2, 3, 4, 5, 6, 7], [5, 4, 6, 7, 2, 1, 3])
