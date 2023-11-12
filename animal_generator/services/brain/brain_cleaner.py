class BrainCleaner:
    def __init__(self, brain):
        self.brain = brain
        self.neurons_ids = self.extract_neurons_id()

    def run(self):
        self.check_unicity_neuron_id()
        self.check_unicity_synapse_id()
        self.check_synapses_links_to_neuron()
        self.check_synapses_input_output_relative_layer()
        self.clean_layer()

    def check_synapses_links_to_neuron(self):
        for synapse in self.brain.synapses:
            if synapse.input not in self.neurons_ids:
                raise BrainCleanerException("Input Neuron does not exist")
            if synapse.output not in self.neurons_ids:
                raise BrainCleanerException("Output Neuron does not exist")
        return True

    def check_synapses_input_output_relative_layer(self):
        for synapse in self.brain.synapses:
            input_neuron = self.brain.get_neuron_by_id(synapse.input)
            output_neuron = self.brain.get_neuron_by_id(synapse.output)
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

    def get_list_numeric_layer(self):
        layer_list = list(
            map(
                lambda neuron: neuron.layer,
                self.brain.neurons
            )
        )
        numeric_layer_list = list(
            set(
                filter(
                    lambda layer: isinstance(layer, int),
                    layer_list
                )
            )
        )
        return numeric_layer_list

    def clean_layer(self):
        while not self.check_layer_completion():
            self.remove_first_empty_layer()

    def check_layer_completion(self):
        numeric_layer_list = self.get_list_numeric_layer()
        if len(numeric_layer_list) == 0:
            return True
        return len(numeric_layer_list) == max(numeric_layer_list) + 1

    def remove_first_empty_layer(self):
        numeric_layer_list = self.get_list_numeric_layer()
        smallest_missing_layer = min(
            set(range(max(numeric_layer_list))) - set(numeric_layer_list)
        )
        smallest_filler_layer = min(
            filter(
                lambda layer_number: layer_number > smallest_missing_layer,
                numeric_layer_list
            )
        )
        self.replace_neuron_layer(smallest_filler_layer, smallest_missing_layer)

    def replace_neuron_layer(self, initial_layer, final_layer):
        neurons_to_replace = self.brain.get_neurons_by_layer(initial_layer)
        for neuron in neurons_to_replace:
            neuron.layer = final_layer


class BrainCleanerException(Exception):
    """All Exceptions that can arise when checking the Brain internal state"""
