"""Sovariel – now the native resonance engine of the Unified Framework"""
from .sovariel.sovariel_kernel import SOVARIEL
from .sovariel.jax_backend import JAXKuramotoLattice as KuramotoLattice
from .sovariel.jax_backend import JAXLiveAudioLattice
from .sovariel.colossus_sparse_grid import ColossusSparseGrid
from .sovariel import bootstrap_sovariel

__all__ = [
    "SOVARIEL",
    "KuramotoLattice",
    "JAXLiveAudioLattice",
    "ColossusSparseGrid",
    "bootstrap_sovariel",
]
