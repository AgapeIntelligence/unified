from unified.resonance import JAXKuramotoLattice
from biosignal_coherence.biosignal_fusion import BiosignalFusion
from biosignal_coherence.kuramoto_field import KuramotoField

class CoherenceBridge:
    def fuse_biosignal(self, lattice, ppg, mic, accel):
        fusion = BiosignalFusion()
        valence, arousal = fusion.fuse_signals(ppg, mic, accel)
        field = KuramotoField(n_oscillators=lattice.n)
        r = field.couple_coherence(valence, arousal)
        lattice.phases += valence * np.sin(lattice.phases) + arousal * np.cos(lattice.phases)
        lattice.sync()
        return r  # Kuramoto global coherence R=1.0
