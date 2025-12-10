from numba import njit
import numpy as np

@njit
def apply_cyclic_shift(tensor: np.ndarray, dim: int = 3) -> np.ndarray:
    """S₁ cyclic operator with optional 369-lattice periodicity."""
    shifted = tensor.copy()
    for _ in range(dim):
        shifted = np.roll(shifted, 1, axis=(_ % 3))
    if tensor.shape[0] >= 9:
        shifted = np.roll(shifted, 3, axis=0)  # 369 step
    return shifted
