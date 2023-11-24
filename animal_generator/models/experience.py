from animal_generator.models.encounter import Encounter


class Experience:
    """
    Experience to compute the fitness of an animal
    Making it run n encounter, win 100 points per encounter,
    then if he survives all encounters, points per energy and hp remaining (Up to 100pts per scale)
    """
    ENCOUNTER_NUMBER = 100

    def __init__(self, ecosystem, animal):
        self.ecosystem = ecosystem
        self.animal = animal
        self.animal.reset()

        self.turn_number = 0
        self.finished = False

    def run(self):
        while not self.finished:
            self.turn()
            self.check_finish()
        self.compute_fitness()

    def compute_fitness(self):
        fitness_score = 100 * self.turn_number
        if self.animal.alive:
            fitness_score += int(100 * self.animal.hp / self.animal.max_hp)
            fitness_score += int(100 * self.animal.energy / self.animal.max_energy)
        self.animal.fitness_score = fitness_score

    def turn(self):
        other_animal = self.ecosystem.pick_animal()
        encounter = Encounter(self.animal, other_animal)
        encounter.run()
        self.animal.turn()
        self.turn_number += 1

    def check_finish(self):
        if self.turn_number >= self.ENCOUNTER_NUMBER:
            self.finished = True
        if not self.animal.alive:
            self.finished = True
