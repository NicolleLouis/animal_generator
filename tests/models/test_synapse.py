from animal_generator.models.synapse import Synapse

example_synapse = {
    "id": 1,
    "strength": 1,
    "input": 1,
    "output": 1,
}


def test_init():
    synapse = Synapse(example_synapse)
    assert type(synapse) is Synapse
