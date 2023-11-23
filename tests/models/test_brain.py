import pytest

from animal_generator.models.brain import Brain, BrainException
from animal_generator.models.neuron import Neuron
from animal_generator.services.zoo_viewer import ZooViewer

animal = ZooViewer.find_animal('example_animal')
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
    brain = Brain(animal, example_neurons, [example_synapse])
    assert isinstance(brain, Brain)
    assert len(brain.neurons) == 2
    assert len(brain.synapses) == 1


def test_get_neuron_by_id():
    brain = Brain(animal, example_neurons, [example_synapse])
    neuron = brain.get_neuron_by_id(1)
    assert isinstance(neuron, Neuron)


def test_get_neuron_by_id_failure():
    brain = Brain(animal, example_neurons, [example_synapse])
    with pytest.raises(BrainException):
        brain.get_neuron_by_id(3)


def test_get_neurons_by_layer_success():
    brain = Brain(animal, example_neurons, [example_synapse])
    neurons_at_input = brain.get_neurons_by_layer("input")
    assert len(neurons_at_input) == 1


def test_get_neurons_by_layer_failure():
    brain = Brain(animal, example_neurons, [example_synapse])
    with pytest.raises(BrainException):
        brain.get_neurons_by_layer(1)


def test_reset_scores():
    brain = Brain(animal, example_neurons, [example_synapse])
    brain.neurons[0].score = 10
    brain.reset_scores()
    for neuron in brain.neurons:
        assert neuron.score is None


def test_get_synapse_by_output_id_non_empty():
    from animal_generator.models.synapse import Synapse

    brain = Brain(animal, example_neurons, [example_synapse])
    synapses = brain.get_synapse_by_output_id(2)
    assert len(synapses) == 1
    assert isinstance(synapses[0], Synapse)


def test_get_synapse_by_output_id_empty():
    brain = Brain(animal, example_neurons, [example_synapse])
    synapses = brain.get_synapse_by_output_id("fake_id")
    assert len(synapses) == 0
