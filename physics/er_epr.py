# /unified/physics/er_epr.py
# ER/EPR toy toolkit – fully working, no truncation
import math
import numpy as np
import torch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d
from typing import Callable, Sequence, Optional

_dtype = torch.complex64
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Utils ─────────────────────────────────────
def to_tensor(x): return torch.tensor(x, dtype=_dtype, device=device)
ket0   = lambda: to_tensor([[1.0], [0.0]])
ket1   = lambda: to_tensor([[0.0], [1.0]])
pauli_x = lambda: to_tensor([[0.0, 1.0], [1.0, 0.0]])
pauli_y = lambda: to_tensor([[0.0, -1j], [1j, 0.0]])
pauli_z = lambda: to_tensor([[1.0, 0.0], [0.0, -1.0]])
I2 = lambda: torch.eye(2, dtype=_dtype, device=device)
I4 = lambda: torch.eye(4, dtype=_dtype, device=device)
kron = torch.kron
# ── Phi field interpolator (with resonant_scalar support) ─────────────────────
class PhiFieldInterpolator:
    def __init__(self, profile: str = "gaussian", **kwargs):
        self.profile = profile
        self.params = kwargs
        self.resonant_phi = None
        self.r_grid = None
        if profile == "resonant_scalar":
            self._load_resonant_scalar()

    def _load_resonant_scalar(self):
        try:
            from resonant_scalar_increase import build_initial_phi, sovariel_recursion
            Phi0 = build_initial_phi()
            Phi_final, _ = sovariel_recursion(Phi0)
            Nr = Phi_final.shape[1]
            self.r_grid = np.linspace(0, 1, Nr)
            theta_idx = Phi_final.shape[0] // 2
            self.resonant_phi = Phi_final[theta_idx, :]
        except ImportError as e:
            raise ImportError("resonant_scalar_increase.py missing from repo root") from e

    def __call__(self, r: float) -> float:

p = self.profile
        if p == "gaussian":
            c = self.params.get("center", 0.0)
            w = self.params.get("width", 1.0)
            a = self.params.get("amp", 1.0)
            return a * math.exp(-0.5 * ((r - c) / w) ** 2)
        if p == "tanh_throat":
            tr = self.params.get("throat_radius", 1.0)
            s  = self.params.get("steepness", 4.0)
            return math.tanh(s * (1.0 - abs(r) / tr))
        if p == "lorentzian":
            c = self.params.get("center", 0.0)
            g = self.params.get("gamma", 1.0)
            a = self.params.get("amp", 1.0)
            return a * g / ((r - c)**2 + g**2)
        if p == "resonant_scalar":
            interp = interp1d(self.r_grid, self.resonant_phi, kind='cubic', fill_value="extrapolate")
            return float(interp(r))
        raise ValueError(f"Unknown profile: {p}")
# ── Core evolution operators ───────────────────────────────────────────────────
def radial_geodesic(rmin=0.0, rmax=1.0, nsteps=201):
    return np.linspace(rmin, rmax, nsteps)

def er_bridge_unitary(r_path, phi: Callable[[float], float], dt=None):
    if dt is None: dt = float(np.mean(np.diff(r_path))) if len(np.diff(r_path)) else 1.0
    U = I2()
    for r in r_path:
        h = float(phi(r)) ** 2
        H = torch.tensor([[h, 0.0], [0.0, -h]], dtype=_dtype, device=device)
        U = torch.matrix_exp(-1j * H * dt) @ U
    return U

def er_bridge_unitary_with_twist(r_path, phi, twist_strength=0.1, twist_axis="x", dt=None):
    if dt is None: dt = float(np.mean(np.diff(r_path))) if len(np.diff(r_path)) else 1.0
    sigma = {"x": pauli_x(), "y": pauli_y(), "z": pauli_z()}[twist_axis]
    U = I2()
    for r in r_path:
        h = float(phi(r)) ** 2
        H = torch.tensor([[h, 0.0], [0.0, -h]], dtype=_dtype, device=device) + twist_strength * sigma
        U = torch.matrix_exp(-1j * H * dt) @ U
    return U
def two_qubit_er_unitary(r_path, phi, local_twist=0.0, entangling_phase=0.0, dt=None):
    if dt is None: dt = float(np.mean(np.diff(r_path))) if len(np.diff(r_path)) else 1.0
    X = pauli_x()
    U = I4()
    for r in r_path:
        h = float(phi(r)) ** 2
        HA = torch.tensor([[h, 0.0], [0.0, -h]], dtype=_dtype, device=device)
        Hloc = kron(HA, I2()) + kron(I2(), -HA)
        Htwist = local_twist * (kron(X, I2()) + kron(I2(), X))
        # minimal SWAP-like term
        SWAP_like = entangling_phase * (
            kron(to_tensor([[0,0],[0,1]]), to_tensor([[0,1],[0,0]])) +
            kron(to_tensor([[0,1],[0,0]]), to_tensor([[0,0],[0,1]]))
        )
        H = Hloc + Htwist + SWAP_like
        U = torch.matrix_exp(-1j * H * dt) @ U
    return U
EOF 
cat >> physics/er_epr.py << 'EOF'
# ── Diagnostics ───────────────────────────────────────────────────────────────
def fidelity(a, b): return float(abs((a.conj().T @ b).item())**2)
def pure_rho(psi): return psi @ psi.conj().T
def reduced_rho(rho, sys=0):
    r = rho.reshape(2,2,2,2)
    return r.trace(dim1=1, dim2=3) if sys==0 else r.trace(dim1=0, dim2=2)
def von_neumann_entropy(rho):
    vals = torch.linalg.eigvals(rho).real.clamp(min=1e-12)
    return float(- (vals * torch.log(vals)).sum())
def concurrence(psi):
    sy = torch.tensor([[0,-1j],[1j,0]], dtype=_dtype, device=device)
    SYY = kron(sy,sy)
    return float(abs((psi.conj().T @ SYY @ psi).item()))


def plot_bloch(psi, title="Bloch sphere"):
    a, b = psi[:,0]
    x = 2*(a*torch.conj(b)).real.item()
    y = 2*(a*torch.conj(b)).imag.item()
    z = (abs(a)**2 - abs(b)**2).item()
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0,0,0,x,y,z,color='r',length=1,normalize=True)
    u,v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    ax.plot_wireframe(np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), np.cos(v),
                      color="gray", alpha=0.15)
    ax.set_title(title)
    plt.show()
# ── Demos ─────────────────────────────────────────────────────────────────────
def demo_single():
    print("=== Single-qubit ER bridge (resonant_scalar) ===")
    r = radial_geodesic(0.0, 1.0, 301)
    phi = PhiFieldInterpolator(profile="resonant_scalar")
    U = er_bridge_unitary_with_twist(r, phi, twist_strength=0.15, twist_axis="x")
    plus = (ket0() + ket1()) / math.sqrt(2)
    final = U @ plus
    print(f"Fidelity after throat transit: {fidelity(plus, final):.7f}")
    plot_bloch(final, "Single qubit after 3-6-9 ER bridge")


def demo_epr():
    print("\n=== Two-qubit EPR transport (resonant_scalar) ===")
    r = radial_geodesic(0.0, 1.0, 201)
    phi = PhiFieldInterpolator(profile="resonant_scalar")
    U = two_qubit_er_unitary(r, phi, local_twist=0.08, entangling_phase=0.025)
    bell = (kron(ket0(), ket0()) + kron(ket1(), ket1())) / math.sqrt(2)
    final = U @ bell
    rho_red = reduced_rho(pure_rho(final))
    print(f"Fidelity: {fidelity(bell, final):.7f}")
    print(f"Von Neumann entropy: {von_neumann_entropy(rho_red):.7f}")
    print(f"Concurrence: {concurrence(final):.7f}")

if __name__ == "__main__":
    print(f"Device: {device}")
    demo_single()
    demo_epr()
import math, numpy as np, torch, matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d

_dtype = torch.complex64
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
T = lambda x: torch.tensor(x, dtype=_dtype, device=device)
ket0, ket1 = T([[1],[0]]), T([[0],[1]])
X = T([[0,1],[1,0]])
I2 = lambda: torch.eye(2, dtype=_dtype, device=device)
I4 = lambda: torch.eye(4, dtype=_dtype, device=device)
kron = torch.kron

class PhiFieldInterpolator:
    def __init__(self, profile="resonant_scalar"):
        self.profile = profile
        if profile == "resonant_scalar":
            from resonant_scalar_increase import build_initial_phi, sovariel_recursion
            Phi0 = build_initial_phi()
            Phi, _ = sovariel_recursion(Phi0)
            self.phi_r = Phi[Phi.shape[0]//2, :]
            self.r = np.linspace(0, 1, len(self.phi_r))

    def __call__(self, r):
        f = interp1d(self.r, self.phi_r, kind='cubic', fill_value="extrapolate")
        return float(f(r))

def evolve(r_path, phi):
    dt = np.mean(np.diff(r_path))
    U = I2()
    for r in r_path:
        h = phi(r)**2
        H = T([[h,0],[0,-h]]) + 0.15*X
        U = torch.matrix_exp(-1j*H*dt) @ U
    return U

def plot_bloch(psi):
    a,b = psi[:,0]
    x,y,z = 2*(a*b.conj()).real.item(), 2*(a*b.conj()).imag.item(), (abs(a)**2-abs(b)**2).item()
    fig = plt.figure(); ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0,0,0,x,y,z,color='red',length=1,normalize=True)
    u,v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
    ax.plot_wireframe(np.sin(v)*np.cos(u), np.sin(v)*np.sin(u), np.cos(v), color="gray", alpha=0.1)
    plt.show()

if __name__ == "__main__":
    r = np.linspace(0, 1, 401)
    phi = PhiFieldInterpolator()
    plus = (ket0 + ket1)/math.sqrt(2)
    final = evolve(r, phi) @ plus
    print(f"Single-qubit fidelity: {(abs((plus.conj().T @ final))**2):.7f}")
    plot_bloch(final)
