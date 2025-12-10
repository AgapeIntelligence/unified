import numpy as np
from scipy.stats import entropy
from .cyclic_shift import apply_cyclic_shift
from ..utils.logging import log_progress

def apply_ao_flow(tensor: np.ndarray,
                  alpha_weight: float = 0.1,
                  omega_weight: float = 0.9,
                  iterations: int = 20,
                  damping_rate: float = 0.02) -> dict:
    current = tensor.copy()
    history = []

    for i in range(iterations):
        probs = current.flatten()
        probs /= probs.sum()
        ent = entropy(probs, base=2)
        history.append(ent)

        shifted = apply_cyclic_shift(current)
        omega = np.zeros_like(current)
        current = (alpha_weight * shifted + omega_weight * omega) * (1 - damping_rate)
        current = np.clip(current, 0, None)

        log_progress(f"AO-flow {i+1:02d}/{iterations} → entropy {ent:.6f}")
        if ent < 0.001:
            break

    return {"refined_tensor": current, "entropy_history": np.array(history)}
