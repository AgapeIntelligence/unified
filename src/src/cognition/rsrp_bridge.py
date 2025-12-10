from unified.resonance import JAXKuramotoLattice
from spiralcore.rsrp_operator import RSRP
from spiralcore.telemetry.dashboard import monitor_mi

class RSRPBridge:
    def induce_transition(self, lattice, recursive_state):
        rsrp = RSRP(n_substrates=6)
        transition, mi, fractal_dim, topo_var = rsrp.induce_phase_transition(recursive_state)
        lattice.phases = transition.flatten()[:lattice.n]
        lattice.sync()
        monitored = monitor_mi(transition)
        return lattice.order_parameter(), monitored  # Low-entropy R=1.0
