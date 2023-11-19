import random


class RandomService:
    @staticmethod
    def pick_n_among(n, total_number):
        return random.random() * total_number <= n
