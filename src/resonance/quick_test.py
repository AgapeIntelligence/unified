from unified.resonance import KuramotoLattice, SOVARIEL
SOVARIEL.bootstrap()
lattice = KuramotoLattice(n_oscillators=1_000_000)
lattice.sync()
print(f"Sovariel LIVE in Unified | R = {lattice.order_parameter():.10f}")
