from animal_generator.models.neuron import Neuron

example_neuron = {
    "id": 1,
    "name": "example_neuron",
    "layer": "input",
    "function": "sum",
}


def test_init():
    neuron = Neuron(example_neuron)
    assert type(neuron) is Neuron
