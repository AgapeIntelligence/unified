import argparse
import multiprocessing as mp
from .bootstrap import bootstrap_phase1a
from ..utils.logging import log_result

def run_node(args):
    return bootstrap_phase1a(args.qubits, args.shots, args.node_id)

def main():
    parser = argparse.ArgumentParser(description="Phased Bootstrap CLI")
    parser.add_argument("--phase", type=str, default="1A")
    parser.add_argument("--qubits", type=int, default=9)
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--nodes", type=int, default=512)
    parser.add_argument("--output", type=str, default="phase1a_results.txt")
    args = parser.parse_args()

    if args.phase == "1A":
        print(f"Running Phase 1A across {args.nodes} nodes...")
        capped = min(args.nodes, mp.cpu_count() * 10)
        if capped < args.nodes:
            print(f"Capped to {capped} nodes (local CPU limit)")

        with mp.Pool() as pool:
            tasks = [{'qubits': args.qubits, 'shots': args.shots, 'node_id': i} for i in range(capped)]
            results = pool.map(run_node, tasks)

        all_results = {k: v for d in results for k, v in d.items()}
        log_result(all_results, args.output)
        print(f"Results saved → {args.output}")

if __name__ == "__main__":
    main()
