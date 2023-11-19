from unittest.mock import MagicMock, patch

from animal_generator.models.animal import Animal
from animal_generator.models.ecosystem import Ecosystem
from animal_generator.models.encounter import Encounter
from animal_generator.models.experience import Experience
from animal_generator.services.ecosystem_viewer import EcosystemViewer
from animal_generator.services.zoo_viewer import ZooViewer


def test_init():
    ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
    animal = ZooViewer.find_animal('example_animal')
    experience = Experience(ecosystem, animal)

    assert isinstance(experience.ecosystem, Ecosystem)
    assert isinstance(experience.animal, Animal)
    assert experience.turn_number == 0
    assert not experience.finished


def test_compute_fitness_dead():
    ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
    animal = ZooViewer.find_animal('example_animal')
    experience = Experience(ecosystem, animal)

    assert experience.animal.fitness_score is None

    experience.turn_number = 5
    experience.animal.die()

    experience.compute_fitness()
    assert experience.animal.fitness_score == 500


def test_compute_fitness_alive():
    ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
    animal = ZooViewer.find_animal('example_animal')
    experience = Experience(ecosystem, animal)

    assert experience.animal.fitness_score is None

    experience.turn_number = 5
    experience.animal.hp = 50
    experience.animal.max_hp = 100
    experience.animal.energy = 50
    experience.animal.max_energy = 100

    experience.compute_fitness()
    assert experience.animal.fitness_score == 600


def test_turn():
    with patch.object(Encounter, 'run') as mock:
        ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
        animal = ZooViewer.find_animal('example_animal')
        experience = Experience(ecosystem, animal)

        assert experience.turn_number == 0

        experience.turn()

        assert experience.turn_number == 1
        mock.assert_called_once()
        assert animal.energy < animal.max_energy


def test_check_finish_false():
    ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
    animal = ZooViewer.find_animal('example_animal')
    experience = Experience(ecosystem, animal)
    experience.check_finish()

    assert not experience.finished


def test_check_finish_turn_number():
    ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
    animal = ZooViewer.find_animal('example_animal')
    experience = Experience(ecosystem, animal)
    experience.turn_number = Experience.ENCOUNTER_NUMBER + 1
    experience.check_finish()

    assert experience.finished


def test_check_finish_turn_animal_dead():
    ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
    animal = ZooViewer.find_animal('example_animal')
    experience = Experience(ecosystem, animal)
    animal.die()
    experience.check_finish()

    assert experience.finished


def test_run():
    ecosystem = EcosystemViewer.find_ecosystem('example_ecosystem')
    animal = ZooViewer.find_animal('example_animal')
    experience = Experience(ecosystem, animal)
    with patch.object(Encounter, 'run'):
        experience.run()

        assert experience.animal.fitness_score > 0
