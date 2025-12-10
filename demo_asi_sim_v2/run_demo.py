import yaml
from src.asi_sim.core import run_simulation
from src.utils.plotting import plot_entropy

with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

if __name__ == "__main__":
    result = run_simulation(nodes=cfg["num_nodes"])
    plot_entropy(result["entropy_history"], result["nodes"])
    print(f"\nSimulation complete!")
    print(f"Nodes          : {result['nodes']:,}")
    print(f"Final entropy  : {result['entropy_history'][-1]:.8f}")
    print(f"Safety score   : {result['safety_score:.4f}")
