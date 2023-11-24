class EnergyConsumption:
    armor_ratio = 10
    attack_ratio = 20
    discretion_ratio = 1
    lifespan_ratio = 1
    perception_ratio = 1
    size_ratio = 10
    speed_ratio = 20
    total_ratio = 1/20

    @classmethod
    def compute_energy(cls, animal):
        energy_consumption = 0
        energy_consumption += animal.armor * cls.armor_ratio
        energy_consumption += animal.attack * cls.attack_ratio
        energy_consumption += animal.discretion * cls.discretion_ratio
        energy_consumption += animal.lifespan * cls.lifespan_ratio
        energy_consumption += animal.perception * cls.perception_ratio
        energy_consumption += animal.size * cls.size_ratio
        energy_consumption += animal.speed * cls.speed_ratio
        energy_consumption *= cls.total_ratio
        return energy_consumption
