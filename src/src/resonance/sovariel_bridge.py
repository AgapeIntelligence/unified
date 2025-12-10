from sovariel.jax_backend import JAXLiveAudioLattice
from sovariel.sovariel_kernel import SOVARIEL

class SovarielBridge:
    def boot_resonance(self, n_oscillators=10_000_000):
        SOVARIEL.bootstrap()
        lattice = JAXLiveAudioLattice(n_oscillators)
        lattice.sync(steps=3)
        return lattice.order_parameter()  # R=1.0 ≤3 steps
