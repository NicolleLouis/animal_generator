import json
from pathlib import Path


class ZooViewer:
    zoo_path = '../zoo/'

    @classmethod
    def find_animal(cls, name):
        zoo = cls.find_zoo()
        animals = zoo.iterdir()
        for animal_file in animals:
            with open(animal_file) as json_data:
                animal = json.load(json_data)
                if animal["name"] == name:
                    return animal
        raise "Animal Not Found"

    @classmethod
    def find_zoo(cls):
        zoo = Path(__file__).resolve().parent.parent
        for file in zoo.iterdir():
            if file.name == 'zoo':
                return file
        raise "Zoo Not Found"
