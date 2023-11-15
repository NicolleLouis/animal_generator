import functools


class BrainComputer:
    def __init__(self, brain):
        self.brain = brain
        self.result = None

    def compute_final_result(self):
        output_neurons = self.brain.get_neurons_by_layer("output")
        maximum_neuron = max(output_neurons, key=lambda neuron: neuron.score)
        self.result = maximum_neuron.name

    def compute_brain(self):
        self.brain.reset_scores()
        ordered_neurons = self.sort_neurons()
        for neuron in ordered_neurons:
            self.compute_neuron(neuron)
        self.compute_final_result()

    def compute_neuron(self, neuron) -> None:
        if neuron.layer == "input":
            neuron.score = self.compute_input_neuron(neuron)
        else:
            input_scores = self.get_input_scores(neuron)
            neuron.score = sum(input_scores)

    @staticmethod
    def compute_input_neuron(neuron):
        match neuron.name:
            case "constant":
                return 1
        raise BrainComputerException(f"Name: {neuron.name} not recognized")

    def get_input_scores(self, neuron):
        input_scores = []
        input_synapses = self.brain.get_synapse_by_output_id(neuron.id)
        for synapse in input_synapses:
            linked_neuron = self.brain.get_neuron_by_id(synapse.input)
            if linked_neuron.score is None:
                raise BrainComputerException(f"Neuron {linked_neuron.id} was not computed correctly")
            input_scores.append(synapse.strength * linked_neuron.score)
        return input_scores

    @staticmethod
    def has_bigger_layer(neuron_a, neuron_b):
        if neuron_a.layer == "input" or neuron_b.layer == "output":
            return -1
        if neuron_a.layer == "output" or neuron_b.layer == "input":
            return 1
        return neuron_a.layer - neuron_b.layer

    def sort_neurons(self):
        return sorted(
            self.brain.neurons,
            key=functools.cmp_to_key(self.has_bigger_layer)
        )


class BrainComputerException(Exception):
    """All Brain Computer Exceptions"""
