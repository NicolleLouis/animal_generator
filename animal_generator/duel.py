import random


class Duel:
    random_value = 5

    def __init__(self, own_value, other_value):
        self.is_win = None

        self.own_value = own_value
        self.other_value = other_value

    def resolve(self):
        own_random = self.own_value + self.random()
        other_random = self.other_value + self.random()
        self.is_win = own_random >= other_random

    @classmethod
    def random(cls):
        return random.randint(0, cls.random_value)
