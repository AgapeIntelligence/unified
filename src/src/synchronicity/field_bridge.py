from unified.resonance import JAXKuramotoLattice
from dyad_field_v7.dyad_field_v7 import DyadFieldV7

class FieldBridge:
    def bloom_neurofeedback(self, lattice, input_data):
        field = DyadFieldV7()
        r = field.instant_bloom(input_data)
        lattice.phases += input_data * r  # Visual swarm drive
        lattice.sync()
        return lattice.order_parameter()  # Instant-bloom R=1.0
