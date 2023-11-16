from animal_generator.models.ecosystem import Ecosystem, AnimalPopulation

test_ecosystem = {
    "name": "example_ecosystem",
    "dangerousness": 0,
    "animals": [
        {
            "name": "example_animal",
            "quantity": 1
        }
    ]
}


def test_initial_values():
    ecosystem = Ecosystem(test_ecosystem)
    assert ecosystem.name == "example_ecosystem"
    assert ecosystem.dangerousness == 0


def test_animal_creation():
    ecosystem = Ecosystem(test_ecosystem)
    assert len(ecosystem.animals) == 1
    assert isinstance(ecosystem.animals[0], AnimalPopulation)


def test_compute_total_population():
    ecosystem = Ecosystem(test_ecosystem)
    assert ecosystem.total_population == 1
