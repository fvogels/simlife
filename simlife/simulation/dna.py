import random


class DNA:
    def __init__(self, genes=None):
        self.__genes = genes or []

    def __len__(self):
        return len(self.__genes)

    def __getitem__(self, index):
        while index >= len(self.__genes):
            self.__genes.append(DNA.__random_weight())
        return self.__genes[index]

    def crossover(self, other):
        index = random.randrange(0, len(self))
        genes = [
            *(self[i] for i in range(index)),
            *(other[i] for i in range(index, len(other)))
        ]
        return DNA(genes)

    def mutate(self):
        genes = self.__genes[:]
        index = random.randrange(0, len(genes))
        genes[index] = DNA.__random_weight()
        return DNA(genes)

    def __str__(self):
        genes_string = ", ".join(map(str, self.__genes))
        return f'DNA[{genes_string}]'

    @staticmethod
    def __random_weight():
        return random.randint(-100, 100) / 10