from unittest.mock import patch

import pytest

from animal_generator.models.animal import Animal
from animal_generator.models.ecosystem import Ecosystem, AnimalPopulation, EcosystemException
from animal_generator.services.random import RandomService

test_ecosystem = {
    "name": "example_ecosystem",
    "dangerousness": 0,
    "animals": [
        {
            "name": "example_animal",
            "quantity": 1
        },
        {
            "name": "example_animal",
            "quantity": 2
        },
    ]
}


def test_initial_values():
    ecosystem = Ecosystem(test_ecosystem)
    assert ecosystem.name == "example_ecosystem"
    assert ecosystem.dangerousness == 0


def test_animal_creation():
    ecosystem = Ecosystem(test_ecosystem)
    assert len(ecosystem.animals) == 2
    assert isinstance(ecosystem.animals[0], AnimalPopulation)


def test_compute_total_population():
    ecosystem = Ecosystem(test_ecosystem)
    assert ecosystem.total_population == 3


def test_pick_animal():
    ecosystem = Ecosystem(test_ecosystem)
    assert isinstance(ecosystem.pick_animal(), Animal)


def test_pick_animal_impossible_pick():
    ecosystem = Ecosystem(test_ecosystem)
    with patch.object(RandomService, 'pick_n_among') as mock:
        mock.return_value = False
        with pytest.raises(EcosystemException):
            ecosystem.pick_animal()
