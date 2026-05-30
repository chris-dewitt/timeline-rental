"""Quantum photo superposition — three variants coexist until observation."""

from __future__ import annotations

from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


@dataclass(frozen=True)
class PhotoSuperposition:
    weights: tuple[float, float, float]
    dominant_variant: int
    counts: dict[str, int]


def photo_superposition(seed: int, shots: int = 512) -> PhotoSuperposition:
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = AerSimulator()
    job = simulator.run(qc, shots=shots, seed_simulator=seed)
    counts = job.result().get_counts()
    total = sum(counts.values()) or 1

    variant_counts = [0, 0, 0]
    for bitstring, count in counts.items():
        idx = int(bitstring, 2) % 3
        variant_counts[idx] += count

    weights = tuple(round(v / total, 3) for v in variant_counts)
    dominant = max(range(3), key=lambda i: weights[i])

    return PhotoSuperposition(
        weights=weights,
        dominant_variant=dominant,
        counts=counts,
    )


def glitch_variant(frame: int, weights: tuple[float, float, float]) -> int:
    """Cycle variants weighted by quantum amplitudes — visible superposition."""
    cycle = (frame // 14) % 6
    if cycle < 2:
        return 0
    if cycle < 4:
        return 1
    if weights[2] >= max(weights[0], weights[1]):
        return 2
    return 0 if weights[0] >= weights[1] else 1
