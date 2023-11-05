from unittest.mock import MagicMock

from animal_generator.animal import Animal
from animal_generator.encounter import Encounter

animal_slow = {
    "name": "animal_1",
    "speed": 0,
    "perception": 10,
    "discretion": 0,
    "armor": 0,
    "attack": 1,
    "lifespan": 100,
    "size": 10,
    "color_1": 1,
    "color_2": 1,
    "color_3": 1
}

animal_fast = {
    "name": "animal_2",
    "speed": 6,
    "perception": 10,
    "discretion": 0,
    "armor": 0,
    "attack": 1,
    "lifespan": 100,
    "size": 10,
    "color_1": 1,
    "color_2": 1,
    "color_3": 1
}


def test_initialisation():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    assert encounter.second_animal == animal_1
    assert encounter.first_animal == animal_2

    assert encounter.turn_number == 0
    assert not encounter.finished


def test_compute_first_animal():
    animal_1 = Animal(animal_fast)
    animal_2 = Animal(animal_slow)
    encounter = Encounter(animal_1, animal_2)
    assert encounter.first_animal == animal_1
    assert encounter.second_animal == animal_2


def test_finish():
    animal_1 = Animal(animal_fast)
    animal_2 = Animal(animal_slow)
    encounter = Encounter(animal_1, animal_2)
    assert not encounter.finished
    encounter.finish()
    assert encounter.finished


def test_check_finish_turn_number():
    animal_1 = Animal(animal_fast)
    animal_2 = Animal(animal_slow)
    encounter = Encounter(animal_1, animal_2)
    assert not encounter.finished
    encounter.turn_number = Encounter.maximum_turn + 1
    encounter.check_finish()
    assert encounter.finished


def test_check_second_animal_death():
    animal_1 = Animal(animal_fast)
    animal_2 = Animal(animal_slow)
    animal_2.alive = False
    encounter = Encounter(animal_1, animal_2)
    assert not encounter.finished
    encounter.check_finish()
    assert encounter.finished


def test_check_first_animal_death():
    animal_1 = Animal(animal_fast)
    animal_1.alive = False
    animal_2 = Animal(animal_slow)
    encounter = Encounter(animal_1, animal_2)
    assert not encounter.finished
    encounter.check_finish()
    assert encounter.finished


def test_chill():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    animal_1.chill = MagicMock()
    encounter = Encounter(animal_1, animal_2)
    encounter.chill(animal_1)
    animal_1.chill.assert_called_once()


def test_heal():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    animal_1.heal = MagicMock()
    encounter = Encounter(animal_1, animal_2)
    encounter.heal(animal_1)
    animal_1.heal.assert_called_once()


def test_flee_lose():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.flee(animal_1, animal_2)
    assert not encounter.finished


def test_flee_win():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.flee(animal_2, animal_1)
    assert encounter.finished


def test_attack_win():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.attack(animal_2, animal_1)
    assert animal_1.hp == animal_1.max_hp - 1


def test_attack_victim_hidden():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    animal_1.discretion = animal_2.perception + 6
    encounter = Encounter(animal_1, animal_2)
    encounter.attack(animal_2, animal_1)
    assert animal_1.hp == animal_1.max_hp


def test_attack_slow_attacker_hidden():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    animal_1.discretion = animal_2.perception + 6
    encounter = Encounter(animal_1, animal_2)
    encounter.attack(animal_1, animal_2)
    assert animal_2.hp == animal_2.max_hp - 1


def test_attack_fast_attacker_hidden():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    animal_2.discretion = animal_1.perception + 6
    encounter = Encounter(animal_1, animal_2)
    encounter.attack(animal_2, animal_1)
    assert animal_1.hp == animal_1.max_hp - 2


def test_attack_lose():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.attack(animal_1, animal_2)
    assert animal_2.hp == animal_2.max_hp


def test_action_chill():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.chill = MagicMock()
    animal_1.compute_action = MagicMock(return_value="chill")
    encounter.action(animal_1, animal_2)
    encounter.chill.assert_called_once()


def test_action_heal():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.heal = MagicMock()
    animal_1.compute_action = MagicMock(return_value="heal")
    encounter.action(animal_1, animal_2)
    encounter.heal.assert_called_once()


def test_action_flee():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.flee = MagicMock()
    animal_1.compute_action = MagicMock(return_value="flee")
    encounter.action(animal_1, animal_2)
    encounter.flee.assert_called_once()


def test_action_attack():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.attack = MagicMock()
    animal_1.compute_action = MagicMock(return_value="attack")
    encounter.action(animal_1, animal_2)
    encounter.attack.assert_called_once()


def test_turn_security_already_finished():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.finish()
    encounter.action = MagicMock()
    encounter.turn()
    encounter.action.assert_not_called()
    assert encounter.turn_number == 1
    assert encounter.finished


def test_turn_security_finished_after_first_action():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    animal_2.compute_action = MagicMock(return_value="flee")
    encounter.action = MagicMock(side_effect=encounter.action)
    encounter.turn()
    encounter.action.assert_called_once()
    assert encounter.turn_number == 1
    assert encounter.finished


def test_turn_both_animal_should_act():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.action = MagicMock()
    encounter.turn()
    assert encounter.action.call_count == 2


def test_last_turn_should_close_encounter():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    encounter.turn_number = Encounter.maximum_turn
    encounter.turn()
    assert encounter.finished


def test_run_all_chill():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    Animal.compute_action = MagicMock(return_value="chill")
    encounter.run()
    assert encounter.finished
    assert encounter.turn_number == Encounter.maximum_turn


def test_end_encounter_by_death():
    animal_1 = Animal(animal_slow)
    animal_2 = Animal(animal_fast)
    encounter = Encounter(animal_1, animal_2)
    animal_2.eat = MagicMock()
    animal_1.die()
    encounter.run()
    animal_2.eat.assert_called_once()
