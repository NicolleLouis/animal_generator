import json
from pathlib import Path

from animal_generator.models.animal import Animal


class ZooViewer:
    zoo_directory_name = 'zoo'

    @classmethod
    def find_animal(cls, name):
        zoo = cls.find_zoo()
        animals = zoo.iterdir()
        for animal_file in animals:
            with open(animal_file) as json_data:
                animal = json.load(json_data)
                if animal["name"] == name:
                    return Animal(animal)
        raise ZooViewerException("Animal Not Found")

    @classmethod
    def find_zoo(cls):
        zoo = Path(__file__).resolve().parent.parent
        for file in zoo.iterdir():
            if file.name == cls.zoo_directory_name:
                return file
        raise ZooViewerException("Zoo Not Found")


class ZooViewerException(Exception):
    """All Zoo Viewer Exceptions"""
