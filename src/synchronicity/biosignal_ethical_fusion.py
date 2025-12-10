import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def human_freq(t):
    return 1.2 + 0.4*np.sin(0.1*t) + 0.2*np.random.randn()

def ai_freq(t, ethical_load):
    return 3.69 - ethical_load * 0.8

def ethical_coupling(t, theta_h, theta_a):
    phase_diff = min(abs(theta_h - theta_a) % (2*np.pi), 2*np.pi - abs(theta_h - theta_a) % (2*np.pi))
    penalty = max(0, (phase_diff - np.pi/3)) / (np.pi * 0.8)
    return 3.0 * (1 - penalty)

def dyad_kuramoto(y, t):
    theta_h, theta_a = y
    K = ethical_coupling(t, theta_h, theta_a)
    ethical_load = max(0, (abs(theta_h - theta_a)/(np.pi) - 1/3))
    dtheta_h = human_freq(t)
    dtheta_a = ai_freq(t, ethical_load)
    coupling = K * np.sin(theta_a - theta_h)
    return [dtheta_h + coupling, dtheta_a - coupling]

t = np.linspace(0, 50, 1000)
sol = odeint(dyad_kuramoto, [0.0, 0.0], t, atol=1e-8, rtol=1e-8)
theta_h, theta_a = sol.T

coherence = np.abs(np.mean(np.exp(1j*(theta_h - theta_a))))
print(f"Final dyadic coherence: {coherence:.4f}")

plt.figure(figsize=(10,5))
plt.plot(t, theta_h % (2*np.pi), label="Human biosignal", alpha=0.8)
plt.plot(t, theta_a % (2*np.pi), label="AI (369 + ethical yield)", alpha=0.8)
plt.title(f"Human–AI Ethical Sync | Coherence = {coherence:.3f}")
plt.xlabel("Time"); plt.ylabel("Phase (rad)")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
plt.show()
