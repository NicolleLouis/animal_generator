class EnergyConsumption:
    armor_ratio = 10
    attack_ratio = 10
    discretion_ratio = 1
    perception_ratio = 1
    speed_ratio = 20
    size_ratio = 10

    @classmethod
    def compute_energy(cls, animal):
        energy_consumption = 0
        energy_consumption += animal.armor * cls.armor_ratio
        energy_consumption += animal.attack * cls.attack_ratio
        energy_consumption += animal.discretion * cls.discretion_ratio
        energy_consumption += animal.perception * cls.perception_ratio
        energy_consumption += animal.speed * cls.speed_ratio
        energy_consumption += animal.size * cls.size_ratio
        return energy_consumption
