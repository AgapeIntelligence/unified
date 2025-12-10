from qiskit import QuantumCircuit, Aer, execute

def bootstrap_phase1a(num_qubits=9, shots=1024, node_id=0):
    """Simulate a Phase 1A qubit lattice, scalable per node."""
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(0)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    qc.measure_all()

    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=shots)
    result = job.result()
    return {f"node_{node_id}": result.get_counts(qc)}
