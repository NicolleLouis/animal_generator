from unittest.mock import MagicMock

import pytest

from animal_generator.models.brain import Brain
from animal_generator.services.brain.brain_computer import BrainComputer, BrainComputerException

neuron_input = {
    "id": 1,
    "name": "constant",
    "layer": "input",
    "function": "sum",
}
neuron_output = {
    "id": 2,
    "name": "neuron",
    "layer": "output",
    "function": "sum",
}
neuron_layer_0 = {
    "id": 3,
    "name": "neuron",
    "layer": 0,
    "function": "sum",
}
neuron_layer_1 = {
    "id": 4,
    "name": "neuron",
    "layer": 1,
    "function": "sum",
}
synapse_0 = {
    "id": 1,
    "strength": 2,
    "input": 1,
    "output": 3,
}
synapse_1 = {
    "id": 1,
    "strength": 2,
    "input": 3,
    "output": 4,
}
example_neurons = [
    neuron_input,
    neuron_layer_0,
    neuron_layer_1,
    neuron_output,
]
synapse_2 = {
    "id": 1,
    "strength": 2,
    "input": 4,
    "output": 2,
}
example_synapse = [synapse_0, synapse_1, synapse_2]


def test_init():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    assert isinstance(brain_computer, BrainComputer)
    assert isinstance(brain_computer.brain, Brain)


def test_compute_neuron_single_link():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    input_neuron = brain.get_neuron_by_id(1)
    input_neuron.score = 1
    neuron = brain.get_neuron_by_id(3)
    assert neuron.score is None
    brain_computer.compute_neuron(neuron)
    assert neuron.score == 2


def test_compute_neuron_missing_input_neuron_score():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    neuron = brain.get_neuron_by_id(3)
    assert neuron.score is None
    with pytest.raises(BrainComputerException):
        brain_computer.compute_neuron(neuron)


def test_compute_neuron_input_constant():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    neuron = brain.get_neuron_by_id(1)
    assert neuron.score is None
    brain_computer.compute_neuron(neuron)
    assert neuron.score == 1


def test_compute_neuron_input_unrecognized():
    neuron_input_unrecognized = {
        "id": 1,
        "name": "not_a_good_name",
        "layer": "input",
        "function": "sum",
    }
    brain = Brain([neuron_input_unrecognized], [])
    brain_computer = BrainComputer(brain)
    neuron = brain.get_neuron_by_id(1)
    assert neuron.score is None
    with pytest.raises(BrainComputerException):
        brain_computer.compute_neuron(neuron)


def test_get_input_scores():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    input_neuron = brain.get_neuron_by_id(1)
    input_neuron.score = 1
    neuron = brain.get_neuron_by_id(3)
    input_scores = [2]
    assert brain_computer.get_input_scores(neuron) == input_scores


def test_sort_neurons():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    sorted_neurons = brain_computer.sort_neurons()
    assert len(sorted_neurons) == 4
    assert sorted_neurons[0].layer == "input"
    assert sorted_neurons[1].layer == 0
    assert sorted_neurons[2].layer == 1
    assert sorted_neurons[3].layer == "output"


def test_compute_brain_should_reset():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    brain.reset_scores = MagicMock()
    brain_computer.compute_brain()
    brain.reset_scores.assert_called_once()


def test_compute_brain():
    brain = Brain(example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    brain_computer.compute_brain()
    assert brain.neurons[0].score == 1
    assert brain.neurons[1].score == 2
    assert brain.neurons[2].score == 4
    assert brain.neurons[3].score == 8
