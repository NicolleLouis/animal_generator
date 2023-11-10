class Synapse:
    def __init__(self, raw_neuron):
        self.id = raw_neuron["id"]
        self.strength = raw_neuron["strength"]
        self.input = raw_neuron["input"]
        self.output = raw_neuron["output"]
