from animal_generator.animal import Animal
from animal_generator.energy_consumption import EnergyConsumption

test_animal = {
    "name": "test_animal",
    "speed": 10,
    "perception": 1,
    "discretion": 2,
    "armor": 3,
    "attack": 4,
    "lifespan": 100,
    "size": 10,
    "color_1": 1,
    "color_2": 1,
    "color_3": 1
}


def test_compute_energy():
    animal = Animal(test_animal)
    energy_consumption = EnergyConsumption.compute_energy(animal)
    assert energy_consumption == 373
