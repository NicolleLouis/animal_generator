from animal_generator.services.random import RandomService
from animal_generator.services.zoo_viewer import ZooViewer


class Ecosystem:
    def __init__(self, json):
        self.name = json["name"]
        self.dangerousness = json["dangerousness"]

        self.animals = []
        self.add_animals(json["animals"])

        self.total_population = self.compute_total_population()

    def add_animals(self, json):
        for animal_json in json:
            animal_name = animal_json["name"]
            animal_quantity = animal_json["quantity"]
            animal = ZooViewer.find_animal(animal_name)
            self.animals.append(
                AnimalPopulation(
                    animal,
                    animal_quantity
                )
            )

    def compute_total_population(self):
        total_population = 0
        for animal in self.animals:
            total_population += animal.number
        return total_population

    def pick_animal(self):
        remaining_animal_population = self.total_population
        for animal_population in self.animals:
            if RandomService.pick_n_among(animal_population.number, remaining_animal_population):
                return animal_population.animal
            else:
                remaining_animal_population -= animal_population.number
        raise EcosystemException('Failure while picking an animal')


class AnimalPopulation:
    def __init__(self, animal, number):
        self.animal = animal
        self.number = number


class EcosystemException(Exception):
    """All Ecosystem Exceptions"""
