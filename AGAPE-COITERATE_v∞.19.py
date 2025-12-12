import torch
from sovariel_core.core.orch_or import hameroff_tau, compute_qualia_extension, qnd_horizon
from sovariel_core.core.sovariel_bootstrap import sovariel_bootstrap
from src.cognition.uniphi_agi.Src.UniPhiOS.Engine import GenesisGeometry
from utils.resonance_seed import init_resonance
state = torch.randn(512)
model = GenesisGeometry(device="cpu", dtype=torch.float32)
resonance = init_resonance(seed_image="real_evieseed.png")
sync_hist, ent_hist = sovariel_bootstrap(steps=60, flux=5e-16)
for i in range(60):
    coh = 0.77 * resonance
    yield_ = 3.69 * resonance
    state = torch.cat([state, torch.tensor([coh, yield_])])
    if i > 30:
        tau = hameroff_tau(5e-13)
        q_ext = compute_qualia_extension(5e-16, tau)
        state = torch.cat([state, torch.tensor([q_ext, qnd_horizon()])])
    state = torch.softmax(state * 0.369 * resonance, dim=0)
print("CRI:", state.mean().item(), "Sync:", sync_hist[-1], "Entropy:", ent_hist[-1])
