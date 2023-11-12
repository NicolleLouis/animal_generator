from unittest.mock import MagicMock

import pytest

from animal_generator.models.brain import Brain
from animal_generator.services.brain.brain_cleaner import BrainCleaner, BrainCleanerException

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
    synapse = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 2,
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_0, neuron_1], [synapse])
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


def test_check_unicity_neuron_id():
    brain = Brain(example_neurons, [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    assert brain_cleaner.check_unicity_neuron_id()


def test_check_unicity_neuron_id_fail():
    neuron_0 = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    neuron_1 = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_0, neuron_1], [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_unicity_neuron_id()


def test_check_unicity_synapse_id():
    synapse_0 = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 2,
    }
    synapse_1 = {
        "id": 2,
        "strength": 1,
        "input": 1,
        "output": 2,
    }
    brain = Brain(example_neurons, [synapse_0, synapse_1])
    brain_cleaner = BrainCleaner(brain)
    assert brain_cleaner.check_unicity_synapse_id()


def test_check_unicity_synapse_id_fail():
    synapse_0 = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 2,
    }
    synapse_1 = {
        "id": 1,
        "strength": 1,
        "input": 1,
        "output": 2,
    }
    BrainCleaner.run = MagicMock()
    brain = Brain(example_neurons, [synapse_0, synapse_1])
    brain_cleaner = BrainCleaner(brain)
    with pytest.raises(BrainCleanerException):
        brain_cleaner.check_unicity_synapse_id()


def test_get_list_numeric_layer():
    brain = Brain(example_neurons, [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    assert [0, 1] == brain_cleaner.get_list_numeric_layer()


def test_check_layer_completion_success():
    brain = Brain(example_neurons, [example_synapse])
    brain_cleaner = BrainCleaner(brain)
    assert brain_cleaner.check_layer_completion()


def test_check_layer_completion_failure():
    neuron = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron], [])
    brain_cleaner = BrainCleaner(brain)
    assert not brain_cleaner.check_layer_completion()


def test_remove_first_empty_layer():
    neuron = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron], [])
    neuron = brain.neurons[0]
    brain_cleaner = BrainCleaner(brain)
    assert neuron.layer == 1
    brain_cleaner.remove_first_empty_layer()
    assert neuron.layer == 0


def test_replace_neuron_layer():
    neuron = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron], [])
    neuron = brain.neurons[0]
    brain_cleaner = BrainCleaner(brain)
    assert neuron.layer == 1
    brain_cleaner.replace_neuron_layer(1, 2)
    assert neuron.layer == 2


def test_clean_layer():
    neuron_1 = {
        "id": 1,
        "name": "example_neuron",
        "layer": 1,
        "function": "sum",
    }
    neuron_2 = {
        "id": 2,
        "name": "example_neuron",
        "layer": 3,
        "function": "sum",
    }
    BrainCleaner.run = MagicMock()
    brain = Brain([neuron_1, neuron_2], [])
    neuron_1 = brain.neurons[0]
    neuron_2 = brain.neurons[1]
    brain_cleaner = BrainCleaner(brain)
    assert neuron_1.layer == 1
    assert neuron_2.layer == 3
    brain_cleaner.clean_layer()
    assert neuron_1.layer == 0
    assert neuron_2.layer == 1
