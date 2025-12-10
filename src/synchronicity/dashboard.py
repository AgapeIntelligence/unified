import gradio as gr
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def run_simulation(stress_level=0.2, ethical_violation=False, n_humans=3, n_ais=4):
    N = n_humans + n_ais
    def freqs(t):
        f = [1.2 + stress_level*np.random.randn() for _ in range(n_humans)]
        f += [3.69 - (0.8 if ethical_violation else 0) for _ in range(n_ais)]
        return np.array(f)

    def kuramoto(y, t):
        theta = y.reshape(-1, 1)
        coupling = 3.0 * np.sin(theta.T - theta)
        dtheta = freqs(t) + coupling.mean(axis=1)
        return dtheta

    t = np.linspace(0, 30, 600)
    y0 = np.random.uniform(0, 2*np.pi, N)
    sol = odeint(kuramoto, y0, t)

    r = np.abs(np.mean(np.exp(1j * sol), axis=1))
    final_coherence = r[-1]

    fig, ax = plt.subplots(figsize=(10,5))
    for i in range(N):
        label = "Human" if i < n_humans else "AI"
        color = "tab:blue" if i < n_humans else "tab:orange"
        ax.plot(t, sol[:,i] % (2*np.pi), label=label, color=color, alpha=0.7)
    ax.set_title(f"Multi-Agent Sync | Coherence = {final_coherence:.3f}")
    ax.set_xlabel("Time"); ax.legend()
    return fig, f"Final swarm coherence: {final_coherence:.4f}"

demo = gr.Interface(
    fn=run_simulation,
    inputs=[
        gr.Slider(0, 1, value=0.2, label="Human stress level"),
        gr.Checkbox(label="Force AI ethical violation"),
        gr.Slider(1, 10, value=3, step=1, label="Number of humans"),
        gr.Slider(1, 20, value=4, step=1, label="Number of AIs"),
    ],
    outputs=["plot", "text"],
    title="Unified Framework — Live Human-AI Ethical Coherence Dashboard",
    description="Watch what happens when ethics break: synchrony collapses instantly."
)

if __name__ == "__main__":
    demo.launch()
