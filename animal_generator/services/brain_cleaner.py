class BrainCleaner:
    def __init__(self, brain):
        self.brain = brain
        self.neurons_ids = self.extract_neurons_id()

    def run(self):
        self.check_unicity_neuron_id()
        self.check_unicity_synapse_id()
        self.check_synapses_links_to_neuron()
        self.check_synapses_input_output_relative_layer()

    def check_synapses_links_to_neuron(self):
        for synapse in self.brain.synapses:
            if synapse.input not in self.neurons_ids:
                raise BrainCleanerException("Input Neuron does not exist")
            if synapse.output not in self.neurons_ids:
                raise BrainCleanerException("Output Neuron does not exist")
        return True

    def check_synapses_input_output_relative_layer(self):
        for synapse in self.brain.synapses:
            input_neuron = self.brain.get_neuron(synapse.input)
            output_neuron = self.brain.get_neuron(synapse.output)
            if input_neuron.layer == output_neuron.layer:
                raise BrainCleanerException("Synapse Neurons on the same layer")
            if input_neuron.layer == "output":
                raise BrainCleanerException("Synapse input on output layer")
            if output_neuron.layer == "input":
                raise BrainCleanerException("Synapse output on input layer")
            if isinstance(output_neuron.layer, str) or isinstance(input_neuron.layer, str):
                continue
            if output_neuron.layer < input_neuron.layer:
                raise BrainCleanerException("Synapse output below input")
        return True

    def extract_neurons_id(self):
        return list(
            map(
                lambda neuron: neuron.id,
                self.brain.neurons
            )
        )

    def check_unicity_neuron_id(self):
        id_number = len(list(set(self.neurons_ids)))
        if id_number != len(self.brain.neurons):
            raise BrainCleanerException("Duplicate Neurons Ids")
        return True

    def check_unicity_synapse_id(self):
        id_number = len(
            list(
                set(
                    map(
                        lambda synapse: synapse.id,
                        self.brain.synapses
                    )
                )
            )
        )
        if id_number != len(self.brain.synapses):
            raise BrainCleanerException("Duplicate Synapses Ids")
        return True


class BrainCleanerException(Exception):
    """All Exceptions that can arise when checking the Brain internal state"""
