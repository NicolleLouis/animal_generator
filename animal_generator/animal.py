from animal_generator.energy_consumption import EnergyConsumption


class Animal:
    size_ratio = 100

    def __init__(self, json):
        self.energy_consumption = None

        self.armor = json["armor"]
        self.attack = json["attack"]
        self.color_1 = json["color_1"]
        self.color_2 = json["color_2"]
        self.color_3 = json["color_3"]
        self.discretion = json["discretion"]
        self.lifespan = json["lifespan"]
        self.perception = json["perception"]
        self.size = json["size"]
        self.specie = json["name"]
        self.speed = json["speed"]

        self.age = 0
        self.max_energy = self.size_ratio * self.size
        self.energy = self.max_energy
        self.max_hp = self.size_ratio * self.size
        self.hp = self.max_hp
        self.alive = True

        self.set_energy_consumption()

    def turn(self):
        if not self.alive:
            return

        self.age += 1
        self.energy -= self.energy_consumption
        self.regen()
        self.clean()
        self.check_death()

    def clean(self):
        self.hp = min(self.hp, self.max_hp)
        self.energy = min(self.energy, self.max_energy)

    def set_energy_consumption(self):
        self.energy_consumption = EnergyConsumption.compute_energy(self)

    def regen(self):
        self.hp += self.size

    def check_death(self):
        if self.hp == 0:
            self.die()

        if self.energy == 0:
            self.die()

        if self.age > self.lifespan:
            self.die()

    def die(self):
        self.alive = False
