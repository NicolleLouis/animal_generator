from unittest.mock import MagicMock

import pytest

from animal_generator.models.brain import Brain
from animal_generator.services.brain_cleaner import BrainCleaner, BrainCleanerException

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
example_neuron_layer_0 = {
    "id": 3,
    "name": "example_neuron",
    "layer": 0,
    "function": "sum",
}
example_neuron_layer_1 = {
    "id": 4,
    "name": "example_neuron",
    "layer": 1,
    "function": "sum",
}
example_neurons = [
    example_neuron_input,
    example_neuron_output,
    example_neuron_layer_0,
    example_neuron_layer_1
]
example_synapse = {
    "id": 1,
    "strength": 1,
    "input": 1,
    "output": 2,
}


def test_extract_neuron_ids():
    brain = Brain(example_neurons, [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    expected_neuron_ids = [1, 2, 3, 4]
    assert brain_cleaner.extract_neurons_id() == expected_neuron_ids


def test_check_synapses_links_to_neuron():
    brain = Brain(example_neurons, [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    assert brain_cleaner.check_synapses_links_to_neuron()


def test_check_synapses_links_to_neuron_case_fail_input():
    BrainCleaner.run = MagicMock()
    unplugged_input_synapse = {
        "id": 1,
        "strength": 1,
        "input": 10,
        "output": 2,
    }
    brain = Brain(example_neurons, [example_synapse, unplugged_input_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_synapses_links_to_neuron()


def test_check_synapses_links_to_neuron_case_fail_output():
    BrainCleaner.run = MagicMock()
    unplugged_input_synapse = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 20,
    }
    brain = Brain(example_neurons, [example_synapse, unplugged_input_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_synapses_links_to_neuron()


def test_check_synapses_input_output_relative_layer_success():
    synapse_1 = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 3,
    }
    synapse_2 = {
        "id": 1,
        "strength": 1,
        "input": 3,
        "output": 4,
    }
    synapse_3 = {
        "id": 1,
        "strength": 1,
        "input": 4,
        "output": 2,
    }
    BrainCleaner.run = MagicMock()
    synapses = [
        example_synapse,
        synapse_1,
        synapse_2,
        synapse_3
    ]
    brain = Brain(example_neurons, synapses)
    brain_cleaner = BrainCleaner(brain)
    assert brain_cleaner.check_synapses_input_output_relative_layer()


def test_check_synapses_input_output_relative_layer_failure_same_layer_number():
    neuron_0 = {
        "id": 1,
        "name": "example_neuron",
        "layer": 0,
        "function": "sum",
    }
    neuron_1 = {
        "id": 2,
        "name": "example_neuron",
        "layer": 0,
        "function": "sum",
    }
    example_synapse = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 2,
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_0, neuron_1], [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_synapses_input_output_relative_layer()


def test_check_synapses_input_output_relative_layer_failure_same_layer_input():
    neuron_0 = {
        "id": 1,
        "name": "example_neuron",
        "layer": "input",
        "function": "sum",
    }
    neuron_1 = {
        "id": 2,
        "name": "example_neuron",
        "layer": "input",
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_0, neuron_1], [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_synapses_input_output_relative_layer()


def test_check_synapses_input_output_relative_layer_failure_input_output():
    neuron_0 = {
        "id": 1,
        "name": "example_neuron",
        "layer": "output",
        "function": "sum",
    }
    neuron_1 = {
        "id": 2,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_0, neuron_1], [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_synapses_input_output_relative_layer()


def test_check_synapses_input_output_relative_layer_failure_output_input():
    neuron_0 = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    neuron_1 = {
        "id": 2,
        "name": "example_neuron",
        "layer": "input",
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_0, neuron_1], [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_synapses_input_output_relative_layer()


def test_check_synapses_input_output_relative_layer_failure_input_lower_level():
    neuron_0 = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    neuron_1 = {
        "id": 2,
        "name": "example_neuron",
        "layer": 0,
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_0, neuron_1], [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_synapses_input_output_relative_layer()
