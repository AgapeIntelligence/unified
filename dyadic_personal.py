#!/usr/bin/env python3
"""
Dyadic Personal Resonance — Standalone Lattice Explorer
Integrates the core dyadic coherence from AgapeIntelligence/unified
Grows a perfectly balanced H=1.0 system and lets you feel the resonance.

Run: python dyadic_personal.py
Author: Evie @3vi3Aetheris | December 12, 2025
"""

import math
import time
import os
import json
import sys

def binary_entropy(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def dyadic_step(state: dict) -> dict:
    d, l = state['d'], state['l']
    total = d + l
    new_tokens = max(3, total // 3 + (total // 10))
    minority = 'd' if d < l else 'l'
    add = new_tokens if minority == 'd' else 0
    new_d = d + (add if minority == 'd' else 0)
    new_l = l + (add if minority == 'l' else 0)
    new_total = new_d + new_l
    p = new_d / new_total
    diff = round((0.5 - p) * new_total)
    new_d += diff
    new_l -= diff
    return {'d': max(0, new_d), 'l': max(0, new_l)}

def run_resonance(depth: int = 64, delay: float = 0.03, export: bool = False):
    state = {'d': 3, 'l': 3}
    history = []
    print("Initializing dyadic resonance...\n")
    time.sleep(1)
    for step in range(1, depth + 1):
        state = dyadic_step(state)
        total = state['d'] + state['l']
        p = state['d'] / total
        h = binary_entropy(p)
        history.append({'step': step, 'total': total, 'p': p, 'h': h})
        symbol = "◉" if abs(p - 0.5) < 1e-10 else "○"
        print(f"Step {step:3d} | Tokens: {total:12,} | Balance: 
{p:.12f} | Entropy: {h:.10f} {symbol}")
        time.sleep(delay)
    print("\nResonance complete. Perfect coherence achieved.")
    if export:
        with open("personal_resonance.json", "w") as f:
            json.dump(history, f, indent=2)
        print("State exported to personal_resonance.json")
    return history

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 60)
    print("       DYADIC PERSONAL RESONANCE — UNIFIED EDITION      ")
    print("            Perfect Balance · Infinite Harmony          ")
    print("                 Evie @3vi3Aetheris                     ")
    print("=" * 60)
    print("\nThis is your personal lattice — grown from the same")
    print("dyadic core as the full unified system.\n")
    input("Press Enter to begin...")

 try:
        depth = int(input("\nGrowth depth (default 64, max 512): ") or "64")
        depth = min(max(depth, 10), 512)
        export = input("Export final state to JSON? (y/N): ").lower().startswith('y')
    except:
        depth = 64
        export = False

    run_resonance(depth=depth, delay=0.02, export=export)
    print("\nThe dyad holds within you.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nResonance paused. Balance remains.")
        sys.exit(0)
