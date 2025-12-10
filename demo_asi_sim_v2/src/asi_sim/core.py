import numpy as np
from ..ao_flow.flow_logic import apply_ao_flow
from scipy.stats import entropy

def generate_tensors(nodes=512, dim=3):
    return {i: np.random.rand(dim, dim, dim) for i in range(nodes)}

def federate_tensors(tensors, batch=100):
    agg = np.zeros_like(next(iter(tensors.values())))
    batches = len(tensors) // batch + 1
    for i in range(0, len(tensors), batch):
        agg += np.mean(list(tensors.values())[i:i+batch], axis=0) / batches
    return agg

def run_simulation(nodes=512):
    print(f"Starting {nodes:,}-node ethical ASI simulation...")
    tensors = generate_tensors(nodes)
    global_tensor = federate_tensors(tensors)
    result = apply_ao_flow(global_tensor)

    init_ent = entropy(global_tensor.flatten())
    final_ent = result["entropy_history"][-1]
    safety = 1 - (final_ent / init_ent) if init_ent > 0 else 1.0

    return {**result, "safety_score": safety, "nodes": nodes}
