from animal_generator.models.neuron import Neuron
from animal_generator.models.synapse import Synapse


class Brain:
    def __init__(self, raw_neurons, raw_synapses):
        self.neurons = self.generate_neurons(raw_neurons)
        self.synapses = self.generate_synapses(raw_synapses)
        self.clean()

    def clean(self):
        from animal_generator.services.brain_cleaner import BrainCleaner

        BrainCleaner(self).run()

    def get_neuron_by_id(self, neuron_id):
        for neuron in self.neurons:
            if neuron.id == neuron_id:
                return neuron
        raise BrainException(f"Neuron with id: {neuron_id} does not exist")

    def get_neurons_by_layer(self, layer_number):
        neurons_at_layer = list(
            filter(
                lambda neuron: neuron.layer == layer_number,
                self.neurons
            )
        )
        if len(neurons_at_layer) == 0:
            raise BrainException(f"No neuron at layer: {layer_number}")
        return neurons_at_layer

    @staticmethod
    def generate_neurons(raw_neurons):
        neurons = []
        for raw_neuron in raw_neurons:
            neurons.append(Neuron(raw_neuron))
        return neurons

    @staticmethod
    def generate_synapses(raw_synapses):
        synapses = []
        for raw_synapse in raw_synapses:
            synapses.append(Synapse(raw_synapse))
        return synapses


class BrainException(Exception):
    """All Brain Exceptions"""
