import matplotlib.pyplot as plt

def plot_entropy(history, nodes=512):
    plt.figure(figsize=(10, 6))
    plt.plot(history)
    plt.title(f"Entropy Convergence – {nodes:,} Nodes")
    plt.xlabel("Iteration")
    plt.ylabel("Shannon Entropy (bits)")
    plt.grid(True, alpha=0.3)
    plt.savefig("entropy_convergence.png", dpi=200)
    plt.close()
    print("Plot saved → entropy_convergence.png")
