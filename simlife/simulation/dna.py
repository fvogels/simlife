import random


class DNA:
    def __init__(self, values):
        self.__values = values

    @staticmethod
    def create_random(length):
        return DNA([random.randint(-10, 10) / 10 for _ in range(length)])

    def __len__(self):
        return len(self.__values)

    def __getitem__(self, key):
        index = key
        if 0 <= index < len(self.__values):
            return self.__values[index]
        else:
            return 0

    def crossover(self, other):
        index = random.randrange(0, len(self))
        genes = [
            *(self[i] for i in range(index)),
            *(other[i] for i in range(index, len(other)))
        ]
        return DNA(genes)
