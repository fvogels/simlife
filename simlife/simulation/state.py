import random
from simlife.simulation.world import World
from simlife.ann.neurons import *
from simlife.simulation import *
from simlife.util import *
from simlife.simulation.dna import DNA



class State:
    def __init__(self, *, fitness_metric, survival_predicate, mutation_rate, boid_initial_energy, phenotype_builder, simulation_rules, auto_steps_per_generation=200):
        self.__boid_count = 1000
        self.__fitness_metric = fitness_metric
        self.__survival_predicate = survival_predicate
        self.__phenotype_builder = phenotype_builder
        self.__generation = 0
        self.__mutation_rate = mutation_rate
        self.__boid_initial_energy = boid_initial_energy
        self.__simulation = Simulation(simulation_rules)
        self.__auto_steps_per_generation = auto_steps_per_generation

        self.__world = self.__create_world(generate_dna=lambda: DNA())
        self.set_automatic()

    def __create_world(self, generate_dna):
        world = World(128, 128)
        for y in range(20, 108, 2):
            world.add_entity(Position(64, y), Wall())
        for _ in range(self.__boid_count):
            world.add_boid(dna=generate_dna(), phenotype_builder=self.__phenotype_builder, energy=self.__boid_initial_energy)
        return world

    def set_manual(self):
        self.__runner = self.__create_manual_runner()

    def set_automatic(self):
        self.__runner = self.__create_automatic_runner(self.__auto_steps_per_generation)

    def step(self):
        next(self.__runner)

    def __create_automatic_runner(self, steps_per_generation):
        def runner():
            while True:
                for _ in range(steps_per_generation):
                    self.__simulation.compute_next(self.__world)
                    yield None
                self.next_generation()
        return runner()

    def __create_manual_runner(self):
        def runner():
            while True:
                self.__simulation.compute_next(self.__world)
                yield None

        return runner()

    def next_generation(self):
        def generate_dna():
            dna1 = dnas[random_index()]
            dna2 = dnas[random_index()]
            dna = dna1.crossover(dna2)
            if random.randrange(0, self.__mutation_rate) == 0:
                dna = dna.mutate()
            return dna

        def random_index():
            x = random.random() ** 5
            return int(x * len(dnas))

        boids = (cell for cell in self.__world if isinstance(cell, Boid))
        survivors = sorted((boid for boid in boids if self.__survival_predicate(boid)), key=self.__fitness_metric, reverse=True)
        dnas = [boid.dna for boid in survivors]
        print(f'Survivors in generation {self.__generation}: {len(dnas)}')
        print(f'Winner: energy={survivors[0].energy} dna={survivors[0].dna}')
        self.__generation += 1
        self.__world = self.__create_world(generate_dna=generate_dna)

    @property
    def world(self):
        return self.__world