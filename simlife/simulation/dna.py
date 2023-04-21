import random


class DNA:
    def __init__(self, genes):
        self.__genes = genes

    @staticmethod
    def create_random(length):
        return DNA([random.randint(-10, 10) / 10 for _ in range(length)])

    def __len__(self):
        return len(self.__genes)

    def __getitem__(self, key):
        index = key
        if 0 <= index < len(self.__genes):
            return self.__genes[index]
        else:
            return 0

    def crossover(self, other):
        index = random.randrange(0, len(self))
        genes = [
            *(self[i] for i in range(index)),
            *(other[i] for i in range(index, len(other)))
        ]
        return DNA(genes)

    def __str__(self):
        genes_string = ", ".join(map(str, self.__genes))
        return f'DNA[{genes_string}]'
