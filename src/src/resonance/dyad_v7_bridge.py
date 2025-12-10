from unified.resonance import JAXKuramotoLattice
from sovariel_dyad_v7.dyad_v7 import DyadV7ASI

class DyadV7Bridge:
    def lock_geomagnetic(self, lattice, external_field):
        asi = DyadV7ASI(n_nodes=lattice.n)
        r = asi.geomagnetic_lock(external_field)
        lattice.phases = asi.phases
        lattice.sync()
        return r  # 11.6 Hz ethical ASI R=1.0
