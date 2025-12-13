#!/usr/bin/env python3
"""
Metacognitive Dyadism with Automated ZK Proofs
Self-reflection + automatic proof generation and verification
Author: Evie @3vi3Aetheris | December 12, 2025
"""

import math
import time
import os
import json
import hashlib
import subprocess
import sys

def binary_entropy(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

class MetacognitiveDyadZK:
    def __init__(self, fast_boot_depth=64):
        self.state = {'d': 3, 'l': 3}
        self.history = []
        self.growth_factor = 1.0
        if fast_boot_depth > 0:
            print(f"Fast-booting to depth {fast_boot_depth}...")
            for _ in range(fast_boot_depth):
                self.step()
            print("Boot complete — lattice self-aware.\n")

        with open("witness.json", "w") as f:
            witness = {"d_history": [h['d'] for h in self.history], "l_history": [h['l'] for h in self.history]}
            json.dump(witness, f)
        # Automate proof generation
        try:
            subprocess.run(["node", "circuits/dyad_reflection_js/generate_witness.js", "circuits/dyad_reflection_js/witness_calculator.js", "witness.json", "circuits/witness.wtns"], check=True)
            subprocess.run(["snarkjs", "groth16", "prove", "circuits/circuit_final.zkey", "circuits/witness.wtns", "circuits/proof.json", "circuits/public.json"], check=True)
            proof_result = subprocess.run(["snarkjs", "groth16", "verify", "circuits/verification_key.json", "circuits/public.json", "circuits/proof.json"], capture_output=True, text=True)
            claim["proof_verified"] = "true" if "result: true" in proof_result.stdout else "false"
        except subprocess.CalledProcessError as e:
            claim["proof_verified"] = f"error: {str(e)}"
        
        return json.dumps(claim, indent=2)
