from unittest.mock import MagicMock

import pytest

from animal_generator.models.brain import Brain
from animal_generator.services.brain.brain_computer import BrainComputer, BrainComputerException
from animal_generator.services.zoo_viewer import ZooViewer

animal = ZooViewer.find_animal('example_animal')
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

example_neurons = [
    neuron_input,
    neuron_layer_0,
    neuron_layer_1,
    neuron_output,
]

synapse_0 = {
    "id": 1,
    "strength": 2,
    "input": 1,
    "output": 3,
}
synapse_1 = {
    "id": 2,
    "strength": 2,
    "input": 3,
    "output": 4,
}
synapse_2 = {
    "id": 3,
    "strength": 2,
    "input": 4,
    "output": 2,
}
example_synapse = [synapse_0, synapse_1, synapse_2]


def test_init():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    assert isinstance(brain_computer, BrainComputer)
    assert isinstance(brain_computer.brain, Brain)


def test_compute_neuron_single_link():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    input_neuron = brain.get_neuron_by_id(1)
    input_neuron.score = 1
    neuron = brain.get_neuron_by_id(3)
    assert neuron.score is None
    brain_computer.compute_neuron(neuron, animal)
    assert neuron.score == 2


def test_compute_neuron_missing_input_neuron_score():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    neuron = brain.get_neuron_by_id(3)
    assert neuron.score is None
    with pytest.raises(BrainComputerException):
        brain_computer.compute_neuron(neuron, animal)


def test_compute_neuron_input_constant():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    neuron = brain.get_neuron_by_id(1)
    assert neuron.score is None
    brain_computer.compute_neuron(neuron, animal)
    assert neuron.score == 1


def test_compute_neuron_input_unrecognized():
    neuron_input_unrecognized = {
        "id": 1,
        "name": "not_a_good_name",
        "layer": "input",
        "function": "sum",
    }
    brain = Brain(animal, [neuron_input_unrecognized], [])
    brain_computer = BrainComputer(brain)
    neuron = brain.get_neuron_by_id(1)
    assert neuron.score is None
    with pytest.raises(BrainComputerException):
        brain_computer.compute_neuron(neuron, animal)


def test_get_input_scores():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    input_neuron = brain.get_neuron_by_id(1)
    input_neuron.score = 1
    neuron = brain.get_neuron_by_id(3)
    input_scores = [2]
    assert brain_computer.get_input_scores(neuron) == input_scores


def test_sort_neurons():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    sorted_neurons = brain_computer.sort_neurons()
    assert len(sorted_neurons) == 4
    assert sorted_neurons[0].layer == "input"
    assert sorted_neurons[1].layer == 0
    assert sorted_neurons[2].layer == 1
    assert sorted_neurons[3].layer == "output"


def test_compute_brain_should_reset():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    brain.reset_scores = MagicMock()
    brain_computer.compute_brain(animal)
    brain.reset_scores.assert_called_once()


def test_compute_brain():
    brain = Brain(animal, example_neurons, example_synapse)
    brain_computer = BrainComputer(brain)
    brain_computer.compute_brain(animal)
    assert brain.neurons[0].score == 1
    assert brain.neurons[1].score == 2
    assert brain.neurons[2].score == 4
    assert brain.neurons[3].score == 8


def test_compute_final_result():
    neuron_output_1 = {
        "id": 2,
        "name": "not_the_result",
        "layer": "output",
        "function": "sum",
    }
    neuron_output_2 = {
        "id": 3,
        "name": "true_result",
        "layer": "output",
        "function": "sum",
    }
    synapse_output_1 = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 2,
    }
    synapse_output_2 = {
        "id": 2,
        "strength": 2,
        "input": 1,
        "output": 3,
    }
    brain = Brain(
        animal,
        [neuron_input, neuron_output_1, neuron_output_2],
        [synapse_output_1, synapse_output_2]
    )
    brain_computer = BrainComputer(brain)
    brain_computer.compute_brain(animal)
    assert brain_computer.result == "true_result"


def test_compute_all_inputs():
    neuron_constant = {
        "id": 1,
        "name": "constant",
        "layer": "input",
        "function": "sum",
    }
    neuron_own_hp = {
        "id": 2,
        "name": "own_hp",
        "layer": "input",
        "function": "sum",
    }
    neuron_own_energy = {
        "id": 3,
        "name": "own_energy",
        "layer": "input",
        "function": "sum",
    }
    neuron_other_hp = {
        "id": 4,
        "name": "other_hp",
        "layer": "input",
        "function": "sum",
    }
    neuron_other_size = {
        "id": 5,
        "name": "other_size",
        "layer": "input",
        "function": "sum",
    }
    neuron_other_speed = {
        "id": 6,
        "name": "other_speed",
        "layer": "input",
        "function": "sum",
    }
    neuron_other_attack = {
        "id": 7,
        "name": "other_attack",
        "layer": "input",
        "function": "sum",
    }
    neuron_other_armor = {
        "id": 8,
        "name": "other_armor",
        "layer": "input",
        "function": "sum",
    }

    output = {
        "id": 9,
        "name": "neuron",
        "layer": "output",
        "function": "sum",
    }
    brain = Brain(
        animal,
        [
            neuron_constant,
            neuron_own_hp,
            neuron_own_energy,
            neuron_other_armor,
            neuron_other_attack,
            neuron_other_speed,
            neuron_other_size,
            neuron_other_hp,
            output
        ],
        []
    )
    brain_computer = BrainComputer(brain)
    brain_computer.compute_brain(animal)
    assert brain.get_neuron_by_id(1).score == 1
    assert brain.get_neuron_by_id(2).score == 100
    assert brain.get_neuron_by_id(3).score == 100
    assert brain.get_neuron_by_id(4).score == 100
    assert brain.get_neuron_by_id(5).score == 1
    assert brain.get_neuron_by_id(6).score == 1
    assert brain.get_neuron_by_id(7).score == 1
    assert brain.get_neuron_by_id(8).score == 1
    assert brain.get_neuron_by_id(9).score == 0
