"""Qiskit timeline collapse — real measurement, pre-authored outcomes."""

from __future__ import annotations

from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


@dataclass(frozen=True)
class CollapseResult:
    outcome_index: int
    measured_bitstring: str
    counts: dict[str, int]


def collapse_timeline(choice_history: list[int], seed: int, shots: int = 1024) -> CollapseResult:
    qc = QuantumCircuit(3, 3)

    for i, choice in enumerate(choice_history):
        if choice:
            qc.x(i % 3)

    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = AerSimulator()
    collapse_seed = (seed * 104729 + sum(choice_history) * 7919) & 0xFFFFFFFF
    job = simulator.run(qc, shots=shots, seed_simulator=collapse_seed)
    counts = job.result().get_counts()

    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    measured_bitstring = ranked[0][0]
    outcome_index = int(measured_bitstring, 2) % 3

    return CollapseResult(
        outcome_index=outcome_index,
        measured_bitstring=measured_bitstring,
        counts=counts,
    )
