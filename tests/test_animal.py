from animal_generator.animal import Animal

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


def test_initial_values():
    animal = Animal(test_animal)
    assert animal.age == 0
    assert animal.alive
    assert animal.max_hp == 1000
    assert animal.max_energy == 1000
    assert animal.hp == animal.max_hp
    assert animal.energy == animal.max_energy
    assert animal.energy_consumption is not None


def test_die():
    animal = Animal(test_animal)
    animal.die()
    assert not animal.alive


def test_check_death_hp():
    animal = Animal(test_animal)
    animal.hp = 0
    animal.check_death()
    assert not animal.alive


def test_check_death_energy():
    animal = Animal(test_animal)
    animal.energy = 0
    animal.check_death()
    assert not animal.alive


def test_check_death_age():
    animal = Animal(test_animal)
    animal.age = 1001
    animal.check_death()
    assert not animal.alive


def test_clean():
    animal = Animal(test_animal)
    animal.hp = animal.max_hp + 1
    animal.energy = animal.max_energy + 1
    animal.clean()
    assert animal.hp == animal.max_hp
    assert animal.energy == animal.max_energy


def test_turn():
    animal = Animal(test_animal)
    animal.turn()
    assert animal.age == 1
    assert animal.hp == 1000
    assert animal.energy < 1000


def test_turn_dead():
    animal = Animal(test_animal)
    animal.die()
    animal.turn()
    assert animal.age == 0


def test_chill():
    animal = Animal(test_animal)
    animal.energy_consumption = 100
    animal.chill()
    assert animal.energy == animal.max_energy + 10


def test_heal():
    animal = Animal(test_animal)
    animal.heal()
    assert animal.hp == animal.max_hp + animal.size


def test_hurt_no_armor():
    damage = 100
    animal = Animal(test_animal)
    animal.armor = 0
    animal.hurt(damage)
    assert animal.hp == animal.max_hp - damage


def test_hurt_armor():
    damage = 100
    animal = Animal(test_animal)
    animal.armor = 100
    animal.hurt(damage)
    assert animal.hp == animal.max_hp - damage / 2


def test_compute_action():
    animal_1 = Animal(test_animal)
    animal_2 = Animal(test_animal)
    assert animal_1.compute_action(animal_2) in Animal.actions
