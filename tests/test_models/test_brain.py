import pytest

from animal_generator.models.brain import Brain, BrainException
from animal_generator.models.neuron import Neuron

example_neuron_input = {
    "id": 1,
    "name": "example_neuron",
    "layer": "input",
    "function": "sum",
}
example_neuron_output = {
    "id": 2,
    "name": "example_neuron",
    "layer": "output",
    "function": "sum",
}
example_neurons = [example_neuron_input, example_neuron_output]
example_synapse = {
    "id": 1,
    "strength": 1,
    "input": 1,
    "output": 2,
}


def test_init():
    brain = Brain(example_neurons, [example_synapse])
    assert isinstance(brain, Brain)
    assert len(brain.neurons) == 2
    assert len(brain.synapses) == 1


def test_get_neuron():
    brain = Brain(example_neurons, [example_synapse])
    neuron = brain.get_neuron(1)
    assert isinstance(neuron, Neuron)


def test_get_neuron_failure():
    brain = Brain(example_neurons, [example_synapse])
    with pytest.raises(BrainException):
        brain.get_neuron(3)
