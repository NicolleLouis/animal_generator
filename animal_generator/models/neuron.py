class Neuron:
    def __init__(self, raw_neuron):
        self.id = raw_neuron["id"]
        self.name = raw_neuron["name"]
        self.layer = raw_neuron["layer"]
        self.function = raw_neuron["function"]
