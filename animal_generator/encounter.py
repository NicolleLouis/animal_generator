from animal_generator.duel import Duel


class Encounter:
    maximum_turn = 5

    def __init__(self, animal_1, animal_2):
        self.first_animal = None
        self.second_animal = None
        self.turn_number = 0
        self.finished = False

        self.compute_first_animal(animal_1, animal_2)

    def run(self):
        while not self.finished:
            self.turn()

    def compute_first_animal(self, animal_1, animal_2):
        initiative_duel = Duel(animal_1.speed, animal_2.speed)
        initiative_duel.resolve()
        if initiative_duel.is_win:
            self.first_animal = animal_1
            self.second_animal = animal_2
        else:
            self.first_animal = animal_2
            self.second_animal = animal_1

    def turn(self):
        self.turn_number += 1
        if self.finished:
            return

        self.action(self.first_animal, self.second_animal)
        self.check_finish()
        if self.finished:
            return

        self.action(self.second_animal, self.first_animal)
        self.check_finish()

    def action(self, animal_1, animal_2):
        action = animal_1.compute_action(animal_2)
        match action:
            case "chill":
                self.chill(animal_1)
            case "heal":
                self.heal(animal_1)
            case "flee":
                self.flee(animal_1, animal_2)
            case "attack":
                self.attack(animal_1, animal_2)

    @staticmethod
    def chill(animal):
        animal.chill()

    @staticmethod
    def heal(animal):
        animal.heal()

    def flee(self, fleeing_animal, other_animal):
        flight_duel = Duel(fleeing_animal.speed, other_animal.speed)
        flight_duel.resolve()
        if flight_duel.is_win:
            self.finish()

    @staticmethod
    def attack(attacking_animal, victim_animal):
        victim_seen_duel = Duel(attacking_animal.perception, victim_animal.discretion)
        victim_seen_duel.resolve()
        if not victim_seen_duel.is_win:
            return

        attacking_seen_duel = Duel(victim_animal.perception, attacking_animal.discretion)
        attacking_seen_duel.resolve()
        if not attacking_seen_duel.is_win:
            victim_animal.hurt(attacking_animal.attack)

        speed_duel = Duel(attacking_animal.speed, victim_animal.speed)
        speed_duel.resolve()
        if speed_duel.is_win:
            victim_animal.hurt(attacking_animal.attack)

    def finish(self):
        self.finished = True

        if not self.first_animal.alive:
            self.second_animal.eat(self.first_animal)
            return

        if not self.second_animal.alive:
            self.first_animal.eat(self.second_animal)
            return

    def check_finish(self):
        if self.turn_number >= self.maximum_turn:
            self.finish()

        if not self.first_animal.alive:
            self.finish()

        if not self.second_animal.alive:
            self.finish()
